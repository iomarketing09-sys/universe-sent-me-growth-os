import worker, { runChecks } from "../src/index.js";

const checks = [];
const check = (name, condition, extra = "") => {
  checks.push({ name, condition, extra });
  console.log(`  ${condition ? "OK " : "FAIL"}  ${name}${extra ? ` ${extra}` : ""}`);
};

class FakeDB {
  constructor(rows = new Map()) {
    this.rows = rows;
    this.batches = 0;
  }

  prepare(sql) {
    const db = this;
    const statement = (args) => ({
      async first() {
        if (String(sql).includes("FROM monitor_state")) {
          const value = db.rows.get(args[0]);
          return value === undefined ? null : { value };
        }
        if (String(sql).includes("SELECT 1")) return { ok: 1 };
        return null;
      },
      async run() {
        if (String(sql).includes("INSERT INTO monitor_state")) {
          db.rows.set(args[0], args[1]);
        }
        return { success: true };
      },
    });
    return {
      ...statement([]),
      bind(...args) {
        return statement(args);
      },
    };
  }

  async batch(statements) {
    this.batches += 1;
    for (const statement of statements) await statement.run();
  }
}

const baseEnv = (overrides = {}) => ({
  DB: new FakeDB(),
  MONITOR_TOKEN: "monitor-token-123",
  TELEGRAM_BOT_TOKEN: "telegram-token",
  TELEGRAM_CHAT_ID: "123",
  WHATSAPP_HEALTH_URL: "https://webhook.example/health",
  HEARTBEAT_TIMEOUT_SECONDS: "600",
  WEBHOOK_FAILURE_THRESHOLD: "2",
  ...overrides,
});

const originalFetch = globalThis.fetch;
let telegramMessages = [];
let webhookResponse = { status: 200, body: { status: "ok" } };

globalThis.fetch = async (url, init = {}) => {
  if (String(url).includes("api.telegram.org")) {
    telegramMessages.push(JSON.parse(init.body));
    return new Response(JSON.stringify({ ok: true }), { status: 200 });
  }
  if (String(url).includes("webhook.example")) {
    return new Response(JSON.stringify(webhookResponse.body), { status: webhookResponse.status });
  }
  throw new Error(`fetch inesperado: ${url}`);
};

const call = (url, env) => worker.fetch(new Request(url), env);

console.log("== health ==");
let response = await call("https://monitor.example/health", baseEnv());
let body = await response.json();
check("200", response.status === 200);
check("D1 verificado", body.checks.d1 === "ok");
check("token configurado", body.checks.monitor_token === "configured");

console.log("== heartbeat ==");
let env = baseEnv();
response = await call("https://monitor.example/heartbeat?token=incorrecto", env);
check("403 con token incorrecto", response.status === 403);
response = await call("https://monitor.example/heartbeat?token=monitor-token-123", env);
check("200 con token correcto", response.status === 200);
check("timestamp guardado en D1", Boolean(env.DB.rows.get("last_heartbeat_at")));

console.log("== host caído ==");
telegramMessages = [];
env = baseEnv();
let result = await runChecks(env, new Date("2026-11-03T12:00:00Z"));
check("estado degradado", result.status === "degraded");
check("heartbeat down", result.heartbeat.status === "down");
check("webhook ok", result.webhook.status === "ok");
check("alerta enviada", telegramMessages.length === 1, `-> ${telegramMessages.length}`);
check("alerta identifica host", telegramMessages[0].text.includes("host-heartbeat"));

console.log("== recuperación del host ==");
telegramMessages = [];
env.DB.rows.set("last_heartbeat_at", "2026-11-03T11:59:30Z");
result = await runChecks(env, new Date("2026-11-03T12:00:00Z"));
check("heartbeat ok", result.heartbeat.status === "ok");
check("aviso de recuperación", telegramMessages.some((message) => message.text.includes("RECUPERADO")));

console.log("== umbral de webhook ==");
telegramMessages = [];
webhookResponse = { status: 503, body: { status: "degraded" } };
env = baseEnv();
env.DB.rows.set("last_heartbeat_at", "2026-11-03T11:59:30Z");
result = await runChecks(env, new Date("2026-11-03T12:00:00Z"));
check("primer fallo degradado", result.webhook.status === "degraded");
check("sin alerta al primer fallo", telegramMessages.length === 0);
webhookResponse = { status: 503, body: { status: "degraded" } };
result = await runChecks(env, new Date("2026-11-03T12:05:00Z"));
check("segundo fallo down", result.webhook.status === "down");
check("alerta al segundo fallo", telegramMessages.length === 1);

console.log("== recuperación del webhook ==");
telegramMessages = [];
webhookResponse = { status: 200, body: { status: "ok" } };
result = await runChecks(env, new Date("2026-11-03T12:10:00Z"));
check("webhook ok", result.webhook.status === "ok");
check("aviso de recuperación", telegramMessages.some((message) => message.text.includes("RECUPERADO")));

globalThis.fetch = originalFetch;
const failures = checks.filter((item) => !item.condition);
console.log(`\nRESULTADO: ${checks.length - failures.length} OK / ${failures.length} fallas`);
process.exit(failures.length ? 1 : 0);
