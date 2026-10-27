-- GrowthOS Initial Schema
-- Version: 1
-- Description: Create all core tables

-- Pieces table
CREATE TABLE IF NOT EXISTS pieces (
    id_pieza TEXT PRIMARY KEY,
    fecha_creacion DATE,
    ultima_modificacion TIMESTAMP,
    estado_operativo TEXT,
    titulo TEXT,
    tipo_contenido TEXT,
    personaje_principal TEXT,
    personajes_secundarios TEXT,
    lugar TEXT,
    categoria_tematica TEXT,
    plataforma_principal TEXT,
    hipotesis_id TEXT,
    objetivo TEXT,
    prioridad TEXT,
    dificultad_produccion TEXT,
    es_reutilizable TEXT,
    bloqueado_canon TEXT,
    fecha_ultima_publicacion DATE,
    dias_desde_publicacion INTEGER,
    fuente TEXT,
    formato TEXT,
    bloqueado_canon_detalle TEXT,
    estado_operacion_normalizado TEXT,
    estado_canon_normalizado TEXT,
    asset_ref_confirmado TEXT,
    asset_ref_candidato TEXT,
    reconciliacion_estado TEXT,
    reconciliacion_confianza TEXT,
    reconciliacion_fuente TEXT,
    reconciliacion_nota TEXT,
    registro_relacionado TEXT,
    drive_reference_id TEXT,
    meta_publication_id TEXT,
    meta_permalink TEXT,
    asset_set TEXT,
    asset_ref TEXT,
    asset_filename TEXT,
    drive_id TEXT,
    estado_canon TEXT,
    estado_produccion TEXT,
    estado_publicacion TEXT,
    ultima_sincronizacion DATE,
    motivo_revision_normalizado TEXT,
    personaje_principal_normalizado TEXT,
    personajes_secundarios_normalizados TEXT,
    rol_narrativo TEXT,
    tipo_humor_normalizado TEXT,
    potencial_etiquetado TEXT,
    confianza_taxonomia TEXT,
    fuente_taxonomia TEXT,
    nota_taxonomia TEXT
);

-- Publications table
CREATE TABLE IF NOT EXISTS publications (
    publicacion_id TEXT PRIMARY KEY,
    id_pieza TEXT NOT NULL,
    fecha_publicacion DATE,
    hora_publicacion TEXT,
    plataforma TEXT,
    meta_post_id TEXT,
    meta_permalink TEXT,
    estado TEXT,
    asset_filename TEXT,
    caption TEXT,
    hashtags TEXT,
    error_message TEXT,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_pieza) REFERENCES pieces (id_pieza)
);

-- Experiments table
CREATE TABLE IF NOT EXISTS experiments (
    experiment_id TEXT PRIMARY KEY,
    hipotesis_id TEXT,
    id_pieza TEXT,
    publicacion_id TEXT,
    fecha_publicacion DATE,
    plataforma TEXT,
    formato TEXT,
    personaje TEXT,
    slot_horario TEXT,
    vistas INTEGER,
    retencion_pct REAL,
    interacciones INTEGER,
    interacciones_24h INTEGER,
    interacciones_72h INTEGER,
    shares INTEGER,
    comentarios INTEGER,
    reactions INTEGER,
    estado_canon TEXT,
    veredicto TEXT,
    conclusion TEXT,
    observaciones TEXT
);

-- Community Engagement table
CREATE TABLE IF NOT EXISTS community_engagement (
    comentario_id TEXT PRIMARY KEY,
    post_id TEXT,
    cnt_id TEXT,
    tipo TEXT,
    autor TEXT,
    texto TEXT,
    fecha_comentario DATE,
    respuesta_estado TEXT,
    respuesta_texto TEXT,
    fecha_respuesta DATE,
    accion_calendario TEXT,
    prioridad TEXT,
    ventana_revision TEXT
);

-- Metrics Snapshots table
CREATE TABLE IF NOT EXISTS metrics_snapshots (
    snapshot_id TEXT PRIMARY KEY,
    meta_post_id TEXT NOT NULL,
    publication_id TEXT,
    target_at_utc TEXT,
    window_type TEXT,
    reactions INTEGER,
    comments INTEGER,
    shares INTEGER,
    views INTEGER,
    reach INTEGER,
    retention_pct REAL,
    validation_status TEXT,
    raw_response TEXT,
    error_message TEXT
);

-- Asset Aliases table
CREATE TABLE IF NOT EXISTS asset_aliases (
    alias_id TEXT PRIMARY KEY,
    asset_ref TEXT,
    asset_filename TEXT,
    drive_id TEXT,
    meta_post_id TEXT,
    meta_permalink TEXT,
    fecha_publicacion DATE,
    hora_publicacion TEXT,
    sha256 TEXT,
    cnt_creation_allowed BOOLEAN DEFAULT FALSE,
    confidence TEXT,
    proposed_record_type TEXT,
    canon_impact TEXT,
    status TEXT,
    evidence_path TEXT,
    notes TEXT
);

-- Deals table
CREATE TABLE IF NOT EXISTS deals (
    deal_id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    lead_source TEXT,
    deal_stage TEXT DEFAULT 'New',
    funnel_line TEXT,
    amount REAL,
    currency TEXT DEFAULT 'MXN',
    contact_name TEXT DEFAULT '',
    contact_phone TEXT DEFAULT '',
    contact_email TEXT DEFAULT '',
    notes TEXT DEFAULT '',
    created_at DATE,
    updated_at DATE,
    closed_at DATE
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_pieces_estado ON pieces (estado_operativo);
CREATE INDEX IF NOT EXISTS idx_pieces_plataforma ON pieces (plataforma_principal);
CREATE INDEX IF NOT EXISTS idx_pieces_fecha_pub ON pieces (fecha_ultima_publicacion);
CREATE INDEX IF NOT EXISTS idx_publications_id_pieza ON publications (id_pieza);
CREATE INDEX IF NOT EXISTS idx_publications_meta_post ON publications (meta_post_id);
CREATE INDEX IF NOT EXISTS idx_metrics_meta_post ON metrics_snapshots (meta_post_id);
CREATE INDEX IF NOT EXISTS idx_deals_tenant ON deals (tenant_id);
CREATE INDEX IF NOT EXISTS idx_deals_stage ON deals (deal_stage);
