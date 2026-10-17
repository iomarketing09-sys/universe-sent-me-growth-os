/**
 * Webhook de WhatsApp **solo-escucha** — tenant `flexi` (Cloudflare Worker + D1).
 *
 * Modo observación (`tenants/flexi/docs/PLAN_WHATSAPP_FLEXI.md`, Fase 0.5). Ventana de 2 semanas
 * para medir volumen, temas, uso de la app por la sucursal y tiempos de respuesta humana.
 *
 * Garantía dura: este archivo **no hace ninguna petición saliente a Meta**. No puede responder
 * ni enviar nada a un cliente; solo verifica el handshake y guarda lo que Meta entrega.
 *
 *   GET  /health          liveness
 *   GET  /stats?token=    conteos agregados (protegido con el verify token)
 *   GET  /webhook         handshake de Meta (hub.mode / hub.verify_token / hub.challenge)
 *   POST /webhook         eventos → tabla `events` (+ `raw_events`)
 *
 * Privacidad: los teléfonos se guardan hasheados (SHA-256 truncado + últimos 4 dígitos).
 */

const TIMEZONE = "America/Matamoros";

/**
 * Palabras clave con peso. Las genéricas ("hay", "tienen", "buenas") pesan 1 y las
 * específicas 2, para que "hay 2x1?" gane como promoción y no como disponibilidad.
 * Solo clasifica para el reporte; nunca dispara una respuesta.
 */
const INTENTS = [
  ["ubicacion", [["ubicacion", 2], ["direccion", 2], ["donde", 2], ["llegar", 2], ["mapa", 2],
                 ["sucursal", 2], ["estacionamiento", 2], ["ubicados", 2]]],
  ["horario", [["horario", 2], ["abren", 2], ["cierran", 2], ["abierto", 2], ["cerrado", 2],
               ["hora", 2], ["domingo", 1], ["sabado", 1], ["festivo", 2]]],
  ["talla", [["talla", 2], ["medida", 2], ["mide", 2], ["medir", 2], ["numero de pie", 2],
             ["centimetros", 2], ["cm", 2], ["calza", 2], ["ancho", 1], ["horma", 2]]],
  ["promocion", [["promo", 2], ["oferta", 2], ["meses sin intereses", 2], ["msi", 2], ["2x1", 2],
                 ["3x1", 2], ["envio gratis", 2], ["bono", 2], ["rebaja", 2]]],
  ["precio", [["precio", 2], ["cuanto", 2], ["costo", 2], ["cuesta", 2], ["barato", 2],
              ["descuento", 2]]],
  ["disponibilidad", [["disponible", 2], ["existencia", 2], ["stock", 2], ["tienen", 1], ["hay", 1],
                      ["modelo", 1], ["color", 1], ["negro", 1], ["blanco", 1], ["cafe", 1]]],
  ["pedido", [["pedido", 2], ["comprar", 2], ["apartar", 2], ["apartado", 2], ["pagar", 2],
              ["transferencia", 2], ["factura", 2]]],
  ["saludo", [["hola", 1], ["buenas", 1], ["buenos dias", 1], ["buenas tardes", 1],
              ["buenas noches", 1], ["que tal", 1]]],
];

function escapeRegExp(text) {
  return text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

/** Minúsculas y sin acentos, para que "ubicación" y "ubicacion" clasifiquen igual. */
function normalize(text) {
  return String(text || "")
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
}

function classify(text) {
  const clean = normalize(text);
  if (!clean.trim()) return "otro";
  let bestIntent = "otro";
  let bestScore = 0;
  for (const [intent, keywords] of INTENTS) {
    let score = 0;
    for (const [keyword, weight] of keywords) {
      if (new RegExp(`\\b${escapeRegExp(keyword)}`, "u").test(clean)) score += weight;
    }
    if (score > bestScore) { bestScore = score; bestIntent = intent; }
  }
  return bestIntent;
}

/** SHA-256 truncado + últimos 4 dígitos: agrupa contactos sin guardar el número. */
async function hashContact(waId) {
  const id = String(waId || "");
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(id));
  const hex = Array.from(new Uint8Array(digest), (b) => b.toString(16).padStart(2, "0")).join("");
  return [hex.slice(0, 12), id.slice(-4)];
}

/** Epoch de WhatsApp → hora local de la sucursal ("YYYY-MM-DD HH:MM"). */
function localTime(timestamp) {
  const seconds = Number(timestamp);
  if (!Number.isFinite(seconds) || seconds <= 0) return "";
  try {
    return new Intl.DateTimeFormat("sv-SE", {
      timeZone: TIMEZONE,
      year: "numeric", month: "2-digit", day: "2-digit",
      hour: "2-digit", minute: "2-digit", hour12: false,
    }).format(new Date(seconds * 1000));
  } catch {
    return "";
  }
}

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json; charset=utf-8" },
  });
}

/** Comparación sin cortocircuito por longitud (evita filtrar el token por timing). */
function sameToken(a, b) {
  const left = String(a || "");
  const right = String(b || "");
  if (!right || left.length !== right.length) return false;
  let diff = 0;
  for (let i = 0; i < left.length; i += 1) diff |= left.charCodeAt(i) ^ right.charCodeAt(i);
  return diff === 0;
}

function textOf(message) {
  const type = message.type || "desconocido";
  if (type === "text") return (message.text || {}).body || "";
  if (type === "interactive") {
    const interactive = message.interactive || {};
    return (interactive.button_reply || {}).title || (interactive.list_reply || {}).title || "";
  }
  if (type === "button") return (message.button || {}).text || "";
  return "";
}

const MEDIA_TYPES = new Set(["image", "audio", "video", "document", "sticker"]);

/** Convierte el payload de Meta en filas listas para D1 (no escribe nada). */
async function buildRows(payload, now) {
  const rows = [];
  for (const entry of payload.entry || []) {
    for (const change of entry.changes || []) {
      const value = change.value || {};

      const contacts = {};
      for (const contact of value.contacts || []) {
        contacts[contact.wa_id] = ((contact.profile || {}).name) || "";
      }

      for (const message of value.messages || []) {
        const waId = message.from || "";
        const [hash, last4] = await hashContact(waId);
        const text = textOf(message);
        rows.push({
          direction: "in",
          wa_ts: message.timestamp || "",
          local_time: localTime(message.timestamp),
          intent: classify(text),
          type: message.type || "desconocido",
          text,
          text_len: text.length,
          has_media: MEDIA_TYPES.has(message.type) ? 1 : 0,
          is_reply_to_template: ((message.context || {}).id) ? 1 : 0,
          contact_hash: hash,
          contact_last4: last4,
          contact_name: contacts[waId] || "",
          status: null,
          message_id: message.id || null,
        });
      }

      // Coexistencia: mensajes que la sucursal manda desde la app del teléfono.
      for (const echo of value.smb_message_echoes || []) {
        const message = echo.message || echo;
        const waId = message.to || message.from || "";
        const [hash, last4] = await hashContact(waId);
        const text = textOf(message);
        rows.push({
          direction: "out_app",
          wa_ts: message.timestamp || "",
          local_time: localTime(message.timestamp),
          intent: classify(text),
          type: message.type || "desconocido",
          text,
          text_len: text.length,
          has_media: MEDIA_TYPES.has(message.type) ? 1 : 0,
          is_reply_to_template: 0,
          contact_hash: hash,
          contact_last4: last4,
          contact_name: "",
          status: null,
          message_id: message.id || null,
        });
      }

      for (const status of value.statuses || []) {
        const [hash] = await hashContact(status.recipient_id || "");
        rows.push({
          direction: "status",
          wa_ts: status.timestamp || "",
          local_time: localTime(status.timestamp),
          intent: null,
          type: "status",
          text: "",
          text_len: 0,
          has_media: 0,
          is_reply_to_template: 0,
          contact_hash: hash,
          contact_last4: "",
          contact_name: "",
          status: status.status || "",
          message_id: null,
        });
      }
    }
  }
  return rows.map((row) => ({ ...row, received_at: now }));
}

const INSERT_SQL = `INSERT OR IGNORE INTO events (
  received_at, direction, wa_ts, local_time, intent, type, text, text_len,
  has_media, is_reply_to_template, contact_hash, contact_last4, contact_name,
  status, message_id
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`;

function insertStatements(env, rows) {
  return rows.map((row) => env.DB.prepare(INSERT_SQL).bind(
    row.received_at, row.direction, row.wa_ts, row.local_time, row.intent, row.type,
    row.text, row.text_len, row.has_media, row.is_reply_to_template, row.contact_hash,
    row.contact_last4, row.contact_name, row.status, row.message_id,
  ));
}

async function handleVerify(url, request, env, ctx) {
  const mode = url.searchParams.get("hub.mode") || "";
  const token = url.searchParams.get("hub.verify_token") || "";
  const challenge = url.searchParams.get("hub.challenge") || "";
  const ok = mode === "subscribe" && sameToken(token, env.WHATSAPP_VERIFY_TOKEN);

  // Nos faltó este registro la primera vez y el diagnóstico se volvió a ciegas.
  ctx.waitUntil(env.DB.prepare(
    `INSERT INTO verifications (received_at, mode, ok, challenge_len, user_agent, country)
     VALUES (?, ?, ?, ?, ?, ?)`,
  ).bind(
    new Date().toISOString(), mode, ok ? 1 : 0, challenge.length,
    request.headers.get("user-agent") || "",
    (request.cf || {}).country || "",
  ).run().catch(() => {}));

  if (ok) return new Response(challenge, { status: 200, headers: { "content-type": "text/plain" } });
  return new Response("forbidden", { status: 403 });
}

async function handleEvent(request, env, ctx) {
  const raw = await request.text();
  let payload;
  try {
    payload = JSON.parse(raw);
  } catch {
    return json({ error: "json inválido" }, 400);
  }

  // Meta reintenta si no recibe 200; respondemos siempre 200 y registramos aparte.
  const now = new Date().toISOString();
  ctx.waitUntil((async () => {
    try {
      const rows = await buildRows(payload, now);
      const statements = insertStatements(env, rows);
      statements.push(env.DB.prepare(
        "INSERT INTO raw_events (received_at, payload) VALUES (?, ?)",
      ).bind(now, raw));
      await env.DB.batch(statements);
    } catch (error) {
      console.error("error registrando evento", error && error.message);
    }
  })());

  return json({ received: true });
}

async function handleStats(url, env) {
  if (!sameToken(url.searchParams.get("token"), env.WHATSAPP_VERIFY_TOKEN)) {
    return new Response("forbidden", { status: 403 });
  }
  const [totals, byIntent, byDay, echoes] = await env.DB.batch([
    env.DB.prepare(`SELECT COUNT(*) AS mensajes, COUNT(DISTINCT contact_hash) AS contactos,
                           MIN(received_at) AS desde, MAX(received_at) AS hasta
                    FROM events WHERE direction = 'in'`),
    env.DB.prepare(`SELECT intent, COUNT(*) AS n FROM events WHERE direction = 'in'
                    GROUP BY intent ORDER BY n DESC`),
    env.DB.prepare(`SELECT substr(received_at, 1, 10) AS dia, direction, COUNT(*) AS n
                    FROM events GROUP BY dia, direction ORDER BY dia`),
    env.DB.prepare(`SELECT COUNT(*) AS n FROM verifications WHERE ok = 1`),
  ]);
  return json({
    listen_only: true,
    entrantes: (totals.results || [])[0] || {},
    por_intencion: byIntent.results || [],
    por_dia: byDay.results || [],
    verificaciones_ok: ((echoes.results || [])[0] || {}).n || 0,
  });
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname.replace(/\/+$/, "") || "/";

    if (path === "/health" || path === "/") {
      return json({
        status: "ok",
        service: "flexi-whatsapp-webhook",
        runtime: "cloudflare-worker",
        storage: "d1",
        listen_only: true,
      });
    }
    if (path === "/stats") return handleStats(url, env);
    if (path === "/webhook") {
      if (request.method === "GET" || request.method === "HEAD") {
        return handleVerify(url, request, env, ctx);
      }
      if (request.method === "POST") return handleEvent(request, env, ctx);
      return json({ error: "método no permitido" }, 405);
    }
    return new Response("not found", { status: 404 });
  },
};
