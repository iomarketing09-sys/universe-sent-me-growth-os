-- Columnas de atribución de anuncios para la tabla events.
-- Ejecutar una sola vez por base (ya aplicado en flexi_whatsapp_obs).
ALTER TABLE events ADD COLUMN referral_source_url TEXT;
ALTER TABLE events ADD COLUMN referral_source_id TEXT;
ALTER TABLE events ADD COLUMN referral_source_type TEXT;
ALTER TABLE events ADD COLUMN referral_body TEXT;
ALTER TABLE events ADD COLUMN referral_headline TEXT;
ALTER TABLE events ADD COLUMN referral_media_type TEXT;
ALTER TABLE events ADD COLUMN referral_image_url TEXT;
ALTER TABLE events ADD COLUMN referral_ctwa_clid TEXT;
ALTER TABLE events ADD COLUMN referral_welcome_message_text TEXT;

CREATE INDEX IF NOT EXISTS idx_events_referral ON events(referral_source_id);
