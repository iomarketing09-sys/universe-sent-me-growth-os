import worker from "../src/index.js";

const captured = [];
const env = {
  WHATSAPP_VERIFY_TOKEN: "token-de-prueba-123",
  DB: {
    prepare(sql) {
      return { bind: (...args) => ({ sql, args, run: async () => captured.push({ sql, args }) }) };
    },
    async batch(stmts) {
      for (const s of stmts) { if (s.sql) captured.push({ sql: s.sql, args: s.args }); }
      return [{ results: [{ mensajes: 1, contactos: 1, desde: "a", hasta: "b" }] },
              { results: [{ intent: "horario", n: 1 }] },
              { results: [{ dia: "2026-10-16", direction: "in", n: 1 }] },
              { results: [{ n: 1 }] }];
    },
  },
};
const pending = [];
const ctx = { waitUntil: (p) => pending.push(p) };

async function call(req) {
  const res = await worker.fetch(req, env, ctx);
  await Promise.allSettled(pending.splice(0));
  return res;
}

const base = "https://flexi-whatsapp-webhook.example.workers.dev"; // host ficticio: no se hace red
let pass = 0, fail = 0;
const check = (name, cond, extra = "") => {
  if (cond) { pass++; console.log(`  OK   ${name}`); }
  else { fail++; console.log(`  FALLA ${name} ${extra}`); }
};

console.log("== health ==");
let r = await call(new Request(`${base}/health`));
check("200", r.status === 200);
check("listen_only", (await r.json()).listen_only === true);

console.log("== verificación correcta ==");
r = await call(new Request(`${base}/webhook?hub.mode=subscribe&hub.verify_token=token-de-prueba-123&hub.challenge=CH-999`));
check("200", r.status === 200);
check("devuelve el challenge", (await r.text()) === "CH-999");
check("registra la verificación", captured.some(c => String(c.sql).includes("INSERT INTO verifications")));

console.log("== verificación con token incorrecto ==");
r = await call(new Request(`${base}/webhook?hub.mode=subscribe&hub.verify_token=malo&hub.challenge=nope`));
check("403", r.status === 403);
r = await call(new Request(`${base}/webhook?hub.mode=subscribe&hub.challenge=x`));
check("403 sin token", r.status === 403);

console.log("== POST con mensaje, eco y status ==");
const payload = {
  object: "whatsapp_business_account",
  entry: [{ id: "1087457280345914", changes: [{ field: "messages", value: {
    messaging_product: "whatsapp",
    metadata: { display_phone_number: "5218781385284", phone_number_id: "1327098437161178" },
    contacts: [{ profile: { name: "Ana" }, wa_id: "5218781112233" }],
    messages: [{ from: "5218781112233", id: "wamid.TEST1", timestamp: "1776000000", type: "text", text: { body: "Hola, a qué hora abren mañana?" } }],
    smb_message_echoes: [{ message: { type: "text", to: "5218781112233", id: "wamid.TEST2", timestamp: "1776000060", text: { body: "Hola! Abrimos de 9 a 8" } } }],
    statuses: [{ id: "wamid.TEST1", status: "delivered", timestamp: "1776000090", recipient_id: "5218781112233" }],
  } }] }],
};
r = await call(new Request(`${base}/webhook`, { method: "POST", body: JSON.stringify(payload) }));
check("200", r.status === 200);
const inserts = captured.filter(c => String(c.sql).includes("INSERT OR IGNORE INTO events"));
check("3 filas (in + out_app + status)", inserts.length === 3, `-> ${inserts.length}`);
const byDir = {}; inserts.forEach(i => byDir[i.args[1]] = i.args);
check("entrante clasificado como 'horario'", byDir.in[4] === "horario", `-> ${byDir.in[4]}`);
check("hora local Matamoros", /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$/.test(byDir.in[3]), `-> ${byDir.in[3]}`);
check("teléfono hasheado (no en claro)", !String(byDir.in[10]).includes("5218781"), byDir.in[10]);
check("últimos 4 dígitos", byDir.in[11] === "2233");
check("guardó nombre del contacto", byDir.in[12] === "Ana");
check("eco desde la app", byDir.out_app[1] === "out_app");
check("status registrado", byDir.status[1] === "status" && byDir.status[13] === "delivered");
check("guarda payload crudo", captured.some(c => String(c.sql).includes("INSERT INTO raw_events")));

console.log("== eco en formato de producción (message_echoes plano) ==");
captured.length = 0;
const prodPayload = {
  object: "whatsapp_business_account",
  entry: [{ id: "1087457280345914", changes: [{ field: "smb_message_echoes", value: {
    messaging_product: "whatsapp",
    metadata: { display_phone_number: "5218781385284", phone_number_id: "1327098437161178" },
    contacts: [],
    message_echoes: [{ from: "5218781385284", to: "5218781112233", id: "wamid.TEST3", timestamp: "1776000120", type: "text", text: { body: "Sí, sí tenemos" } }],
  } }] }],
};
r = await call(new Request(`${base}/webhook`, { method: "POST", body: JSON.stringify(prodPayload) }));
check("200 con message_echoes", r.status === 200);
const prodInserts = captured.filter(c => String(c.sql).includes("INSERT OR IGNORE INTO events"));
check("guarda el eco plano", prodInserts.length === 1 && prodInserts[0].args[1] === "out_app", `-> ${prodInserts.length}`);
check("eco plano trae texto", String(prodInserts[0] && prodInserts[0].args[6]).includes("tenemos"));

console.log("== otros casos ==");
r = await call(new Request(`${base}/webhook`, { method: "POST", body: "{ no es json" }));
check("400 con json inválido", r.status === 400);
r = await call(new Request(`${base}/stats`));
check("403 en /stats sin token", r.status === 403);
r = await call(new Request(`${base}/stats?token=token-de-prueba-123`));
check("200 en /stats con token", r.status === 200);
check("reporta modo solo-escucha", (await r.json()).listen_only === true);
r = await call(new Request(`${base}/otra-cosa`));
check("404 en ruta desconocida", r.status === 404);

console.log("== clasificación ==");
const casos = [["dónde están ubicados?", "ubicacion"], ["¿cuánto cuesta?", "precio"], ["tienen en 27?", "disponibilidad"],
               ["hay 2x1?", "promocion"], ["quiero apartar", "pedido"], ["buenas tardes", "saludo"],
               ["mejor un teléfono que otro", "otro"], ["", "otro"],
               ["tienen meses sin intereses?", "promocion"], ["hola, hay descuento?", "precio"],
               ["a qué hora cierran?", "horario"], ["quiero factura", "pedido"],
               ["sí hay de la negra en 26?", "disponibilidad"], ["cuánto mide mi pie?", "talla"]];
for (const [texto, esperado] of casos) {
  const pl = { entry: [{ changes: [{ value: { messages: [{ from: "1", id: "x" + texto, timestamp: "1", type: "text", text: { body: texto } }] } }] }] };
  await call(new Request(`${base}/webhook`, { method: "POST", body: JSON.stringify(pl) }));
  const last = captured.filter(c => String(c.sql).includes("INSERT OR IGNORE INTO events")).pop();
  check(`"${texto}" -> ${esperado}`, last.args[4] === esperado, `-> ${last.args[4]}`);
}
console.log(`\nRESULTADO: ${pass} OK / ${fail} fallas`);
process.exit(fail ? 1 : 0);
