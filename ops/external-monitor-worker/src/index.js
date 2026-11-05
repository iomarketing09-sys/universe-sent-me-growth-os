const STATE_KEYS = [
  "last_heartbeat_at",
  "heartbeat_status",
  "heartbeat_detail",
  "heartbeat_checked_at",
  "webhook_status",
  "webhook_detail",
  "webhook_checked_at",
  "webhook_failures",
];

const CHECKS = {
  heartbeat: {
    id: "host-heartbeat",
    name: "Host Growth OS",
    owner: "Operations",
  },
  webhook: {
    id: "whatsapp-webhook",
    name: "Webhook WhatsApp Flexi",
    owner: "Communications",
  },
};

const RUNBOOK_URL = "https://github.com/iomarketing09-sys/growth-os/blob/main/docs/OPERACION_COMPARTIDA.md#monitor-externo";

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
    },
  });
}

function sameToken(given, expected) {
  if (!given || !expected || given.length !== expected.length) return false;
  let diff = 0;
  for (let i = 0; i < given.length; i += 1) {
    diff |= given.charCodeAt(i) ^ expected.charCodeAt(i);
  }
  return diff === 0;
}

function positiveInt(value, fallback) {
  const parsed = Number.parseInt(value, 10);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback;
}

function ageSeconds(iso, now) {
  if (!iso) return null;
  const timestamp = Date.parse(iso);
  if (!Number.isFinite(timestamp)) return null;
  return Math.max(0, Math.floor((now.getTime() - timestamp) / 1000));
}

function formatAge(seconds) {
  if (seconds === null) return "sin latido";
  if (seconds < 60) return `hace ${seconds} s`;
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `hace ${minutes} min`;
  const hours = Math.floor(minutes / 60);
  return `hace ${hours} h ${minutes % 60} min`;
}

async function loadState(env) {
  const state = {};
  for (const key of STATE_KEYS) {
    const row = await env.DB.prepare(
      "SELECT value FROM monitor_state WHERE key = ?",
    ).bind(key).first();
    state[key] = row && row.value !== null ? String(row.value) : "";
  }
  return state;
}

async function saveState(env, state, nowIso) {
  const statements = STATE_KEYS.map((key) => env.DB.prepare(
    "INSERT INTO monitor_state (key, value, updated_at) VALUES (?, ?, ?) "
      + "ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at",
  ).bind(key, String(state[key] ?? ""), nowIso));
  await env.DB.batch(statements);
}

async function probeWebhook(env) {
  const url = env.WHATSAPP_HEALTH_URL;
  if (!url) return { ok: false, detail: "WHATSAPP_HEALTH_URL no configurado" };

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 10_000);
  try {
    const response = await fetch(url, {
      method: "GET",
      headers: { accept: "application/json" },
      signal: controller.signal,
    });
    let body = null;
    try {
      body = await response.json();
    } catch {
      body = null;
    }
    const bodyStatus = body && typeof body.status === "string" ? body.status : "invalid";
    return {
      ok: response.status === 200 && bodyStatus === "ok",
      detail: `HTTP ${response.status}; status=${bodyStatus}`,
    };
  } catch (error) {
    return { ok: false, detail: `sin respuesta (${error && error.name ? error.name : "error"})` };
  } finally {
    clearTimeout(timer);
  }
}

function transition(check, previous, current, detail) {
  if (current === "down" && previous !== "down") return "down";
  if (current === "ok" && previous === "down") return "recovered";
  return null;
}

function alertText(kind, check, detail, now) {
  const isDown = kind === "down";
  const icon = isDown ? "🚨" : "✅";
  const state = isDown ? "CAÍDO" : "RECUPERADO";
  return [
    `${icon} Growth OS — ${check.name}: ${state}`,
    `Check: ${check.id}`,
    `Owner funcional: ${check.owner}`,
    `Detalle: ${detail}`,
    `Hora: ${now.toISOString()}`,
    `Runbook: docs/OPERACION_COMPARTIDA.md#monitor-externo`,
    RUNBOOK_URL,
  ].join("\n");
}

async function sendTelegram(env, text) {
  if (!env.TELEGRAM_BOT_TOKEN || !env.TELEGRAM_CHAT_ID) {
    console.error("telegram no configurado; alerta omitida");
    return false;
  }
  try {
    const response = await fetch(
      `https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendMessage`,
      {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          chat_id: env.TELEGRAM_CHAT_ID,
          text,
          disable_web_page_preview: true,
        }),
      },
    );
    if (!response.ok) {
      console.error(`telegram respondió HTTP ${response.status}`);
      return false;
    }
    return true;
  } catch (error) {
    console.error("error enviando alerta a telegram", error && error.name);
    return false;
  }
}

export async function runChecks(env, now = new Date()) {
  const state = await loadState(env);
  const heartbeatTimeout = positiveInt(env.HEARTBEAT_TIMEOUT_SECONDS, 600);
  const webhookThreshold = positiveInt(env.WEBHOOK_FAILURE_THRESHOLD, 2);
  const nowIso = now.toISOString();

  const heartbeatAge = ageSeconds(state.last_heartbeat_at, now);
  const heartbeatDown = heartbeatAge === null || heartbeatAge > heartbeatTimeout;
  const heartbeatStatus = heartbeatDown ? "down" : "ok";
  const heartbeatDetail = heartbeatDown
    ? `último latido ${formatAge(heartbeatAge)}; umbral ${heartbeatTimeout} s`
    : `último latido ${formatAge(heartbeatAge)}`;

  const probe = await probeWebhook(env);
  const previousFailures = Number.parseInt(state.webhook_failures, 10) || 0;
  const failures = probe.ok ? 0 : previousFailures + 1;
  const webhookStatus = probe.ok
    ? "ok"
    : failures >= webhookThreshold ? "down" : "degraded";
  const webhookDetail = `${probe.detail}; fallos consecutivos ${failures}/${webhookThreshold}`;

  const events = [];
  const heartbeatTransition = transition(
    CHECKS.heartbeat,
    state.heartbeat_status,
    heartbeatStatus,
    heartbeatDetail,
  );
  if (heartbeatTransition) {
    events.push({ kind: heartbeatTransition, check: CHECKS.heartbeat, detail: heartbeatDetail });
  }
  const webhookTransition = transition(
    CHECKS.webhook,
    state.webhook_status,
    webhookStatus,
    webhookDetail,
  );
  if (webhookTransition) {
    events.push({ kind: webhookTransition, check: CHECKS.webhook, detail: webhookDetail });
  }

  state.heartbeat_status = heartbeatStatus;
  state.heartbeat_detail = heartbeatDetail;
  state.heartbeat_checked_at = nowIso;
  state.webhook_status = webhookStatus;
  state.webhook_detail = webhookDetail;
  state.webhook_checked_at = nowIso;
  state.webhook_failures = String(failures);
  await saveState(env, state, nowIso);

  for (const event of events) {
    await sendTelegram(env, alertText(event.kind, event.check, event.detail, now));
  }

  return {
    status: heartbeatStatus === "ok" && webhookStatus === "ok" ? "ok" : "degraded",
    checked_at: nowIso,
    heartbeat: {
      status: heartbeatStatus,
      last_at: state.last_heartbeat_at || null,
      age_seconds: heartbeatAge,
      detail: heartbeatDetail,
    },
    webhook: {
      status: webhookStatus,
      detail: webhookDetail,
      failures,
    },
    alerts_sent: events.map((event) => ({ kind: event.kind, check: event.check.id })),
  };
}

async function handleHealth(env) {
  const checks = {
    d1: "ok",
    monitor_token: env.MONITOR_TOKEN ? "configured" : "missing",
    telegram: env.TELEGRAM_BOT_TOKEN && env.TELEGRAM_CHAT_ID ? "configured" : "missing",
  };
  try {
    await env.DB.prepare("SELECT 1 AS ok").first();
  } catch (error) {
    checks.d1 = "error";
    console.error("health: D1 no disponible", error && error.message);
  }
  const healthy = Object.values(checks).every((value) => value === "ok" || value === "configured");
  return json({
    status: healthy ? "ok" : "degraded",
    service: "growth-os-external-monitor",
    runtime: "cloudflare-worker",
    checks,
  }, healthy ? 200 : 503);
}

async function handleHeartbeat(url, env) {
  if (!sameToken(url.searchParams.get("token"), env.MONITOR_TOKEN)) {
    return new Response("forbidden", { status: 403 });
  }
  const now = new Date().toISOString();
  await env.DB.prepare(
    "INSERT INTO monitor_state (key, value, updated_at) VALUES (?, ?, ?) "
      + "ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at",
  ).bind("last_heartbeat_at", now, now).run();
  return json({ received: true, at: now });
}

async function handleStatus(url, env) {
  if (!sameToken(url.searchParams.get("token"), env.MONITOR_TOKEN)) {
    return new Response("forbidden", { status: 403 });
  }
  const state = await loadState(env);
  const now = new Date();
  return json({
    status: state.heartbeat_status === "ok" && state.webhook_status === "ok" ? "ok" : "degraded",
    heartbeat: {
      status: state.heartbeat_status || "unknown",
      last_at: state.last_heartbeat_at || null,
      age_seconds: ageSeconds(state.last_heartbeat_at, now),
      detail: state.heartbeat_detail || null,
      checked_at: state.heartbeat_checked_at || null,
    },
    webhook: {
      status: state.webhook_status || "unknown",
      detail: state.webhook_detail || null,
      checked_at: state.webhook_checked_at || null,
      failures: Number.parseInt(state.webhook_failures, 10) || 0,
    },
  });
}

async function handleCheck(url, env) {
  if (!sameToken(url.searchParams.get("token"), env.MONITOR_TOKEN)) {
    return new Response("forbidden", { status: 403 });
  }
  return json(await runChecks(env));
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname.replace(/\/+$/, "") || "/";
    if (request.method !== "GET") return json({ error: "método no permitido" }, 405);
    if (path === "/" || path === "/health") return handleHealth(env);
    if (path === "/heartbeat") return handleHeartbeat(url, env);
    if (path === "/status") return handleStatus(url, env);
    if (path === "/check") return handleCheck(url, env);
    return new Response("not found", { status: 404 });
  },

  async scheduled(controller, env) {
    const now = controller && controller.scheduledTime
      ? new Date(controller.scheduledTime)
      : new Date();
    await runChecks(env, now);
  },
};
