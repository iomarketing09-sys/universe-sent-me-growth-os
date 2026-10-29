-- Revenue Lite: campos de cobro y atribución para deals.
-- Los montos se guardan en MXN por defecto.

ALTER TABLE deals ADD COLUMN product_ref TEXT DEFAULT '';
ALTER TABLE deals ADD COLUMN amount_collected REAL DEFAULT 0;
ALTER TABLE deals ADD COLUMN payment_status TEXT DEFAULT 'pendiente';
ALTER TABLE deals ADD COLUMN payment_method TEXT DEFAULT '';
ALTER TABLE deals ADD COLUMN payment_date DATE;
ALTER TABLE deals ADD COLUMN source_publication_id TEXT DEFAULT '';
ALTER TABLE deals ADD COLUMN source_campaign_id TEXT DEFAULT '';
ALTER TABLE deals ADD COLUMN source_conversation_id TEXT DEFAULT '';
ALTER TABLE deals ADD COLUMN lost_reason TEXT DEFAULT '';

CREATE INDEX IF NOT EXISTS idx_deals_payment_status ON deals (payment_status);
