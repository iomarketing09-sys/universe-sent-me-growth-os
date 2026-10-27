-- Esquema del modo observación (solo-escucha). No hay tablas de envío a propósito.
CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  received_at TEXT NOT NULL,
  direction TEXT NOT NULL,          -- in | out_app | status
  wa_ts TEXT,
  local_time TEXT,                  -- America/Matamoros, "YYYY-MM-DD HH:MM"
  intent TEXT,
  type TEXT,
  text TEXT,
  text_len INTEGER,
  has_media INTEGER,
  is_reply_to_template INTEGER,
  contact_hash TEXT,                -- SHA-256 truncado (no se guarda el teléfono)
  contact_last4 TEXT,
  contact_name TEXT,
  status TEXT,
  message_id TEXT,
  -- Atribución de anuncios (click to WhatsApp). El worker ya las inserta;
  -- en la base desplegada se agregaron con migrations/001_referral_columns.sql.
  referral_source_url TEXT,
  referral_source_id TEXT,
  referral_source_type TEXT,
  referral_body TEXT,
  referral_headline TEXT,
  referral_media_type TEXT,
  referral_image_url TEXT,
  referral_ctwa_clid TEXT,
  referral_welcome_message_text TEXT
);

CREATE INDEX IF NOT EXISTS idx_events_received_at ON events(received_at);
CREATE INDEX IF NOT EXISTS idx_events_direction   ON events(direction);
CREATE INDEX IF NOT EXISTS idx_events_intent      ON events(intent);
CREATE INDEX IF NOT EXISTS idx_events_contact     ON events(contact_hash);

-- Reintentos de Meta: evita duplicar mensajes ya registrados.
CREATE UNIQUE INDEX IF NOT EXISTS idx_events_dedupe
  ON events(message_id)
  WHERE direction IN ('in', 'out_app') AND message_id IS NOT NULL;

-- Payload completo, solo para depurar.
CREATE TABLE IF NOT EXISTS raw_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  received_at TEXT NOT NULL,
  payload TEXT NOT NULL
);

-- Cada intento de verificación de Meta (nos faltó esto y nos costó un diagnóstico).
CREATE TABLE IF NOT EXISTS verifications (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  received_at TEXT NOT NULL,
  mode TEXT,
  ok INTEGER,
  challenge_len INTEGER,
  user_agent TEXT,
  country TEXT
);
