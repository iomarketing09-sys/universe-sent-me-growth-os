-- GrowthOS Initial Schema
-- Version: 1
-- Applied: Auto by database.init_schema()

-- Pieces table (Content Inventory)
CREATE TABLE IF NOT EXISTS pieces (
    id_pieza TEXT PRIMARY KEY,
    fecha_creacion DATE,
    ultima_modificacion TIMESTAMP,
    estado TEXT NOT NULL,
    titulo TEXT,
    tipo_contenido TEXT,
    personaje_principal TEXT,
    personajes_secundarios TEXT,
    lugar TEXT,
    categoria TEXT,
    plataforma TEXT,
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
    -- Normalized fields
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
    nota_taxonomia TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_pieces_estado ON pieces(estado);
CREATE INDEX IF NOT EXISTS idx_pieces_estado_canon ON pieces(estado_canon_normalizado);
CREATE INDEX IF NOT EXISTS idx_pieces_personaje ON pieces(personaje_principal);
CREATE INDEX IF NOT EXISTS idx_pieces_plataforma ON pieces(plataforma);
CREATE INDEX IF NOT EXISTS idx_pieces_fecha_pub ON pieces(fecha_ultima_publicacion);
CREATE INDEX IF NOT EXISTS idx_pieces_reutilizable ON pieces(es_reutilizable);

-- Publications table (Publication Log)
CREATE TABLE IF NOT EXISTS publications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pieza TEXT NOT NULL,
    publicacion_id TEXT UNIQUE,
    fecha_publicacion DATE,
    hora_publicacion TEXT,
    plataforma TEXT,
    meta_post_id TEXT UNIQUE,
    meta_permalink TEXT,
    estado TEXT,
    asset_filename TEXT,
    caption TEXT,
    hashtags TEXT,
    error_message TEXT,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_pieza) REFERENCES pieces(id_pieza)
);

CREATE INDEX IF NOT EXISTS idx_publications_id_pieza ON publications(id_pieza);
CREATE INDEX IF NOT EXISTS idx_publications_meta_post ON publications(meta_post_id);
CREATE INDEX IF NOT EXISTS idx_publications_fecha ON publications(fecha_publicacion);

-- Experiments table (Experiment Log)
CREATE TABLE IF NOT EXISTS experiments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    experiment_id TEXT UNIQUE NOT NULL,
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
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_pieza) REFERENCES pieces(id_pieza)
);

CREATE INDEX IF NOT EXISTS idx_experiments_id_pieza ON experiments(id_pieza);
CREATE INDEX IF NOT EXISTS idx_experiments_hipotesis ON experiments(hipotesis_id);
CREATE INDEX IF NOT EXISTS idx_experiments_fecha ON experiments(fecha_publicacion);

-- Community Engagement table
CREATE TABLE IF NOT EXISTS community_engagement (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comentario_id TEXT UNIQUE NOT NULL,
    post_id TEXT,
    cnt_id TEXT,
    tipo TEXT,
    autor TEXT,
    texto TEXT,
    fecha_comentario TIMESTAMP,
    respuesta_estado TEXT,
    respuesta_texto TEXT,
    fecha_respuesta TIMESTAMP,
    accion_calendario TEXT,
    prioridad TEXT,
    ventana_revision TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_community_post_id ON community_engagement(post_id);
CREATE INDEX IF NOT EXISTS idx_community_cnt_id ON community_engagement(cnt_id);
CREATE INDEX IF NOT EXISTS idx_community_fecha ON community_engagement(fecha_comentario);

-- Metrics Snapshots table (E0/E24/E72)
CREATE TABLE IF NOT EXISTS metrics_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_id TEXT UNIQUE NOT NULL,
    meta_post_id TEXT NOT NULL,
    publication_id TEXT,
    target_at_utc TIMESTAMP NOT NULL,
    captured_at_utc TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    window_type TEXT NOT NULL,  -- E0, E24, E72
    reactions INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    views INTEGER,
    reach INTEGER,
    retention_pct REAL,
    validation_status TEXT DEFAULT 'Pending',  -- Valid_E0, Invalid, Pending
    raw_response TEXT,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_metrics_meta_post ON metrics_snapshots(meta_post_id);
CREATE INDEX IF NOT EXISTS idx_metrics_target ON metrics_snapshots(target_at_utc);
CREATE INDEX IF NOT EXISTS idx_metrics_window ON metrics_snapshots(window_type);
CREATE INDEX IF NOT EXISTS idx_metrics_validation ON metrics_snapshots(validation_status);

-- Asset Aliases table (260####)
CREATE TABLE IF NOT EXISTS asset_aliases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alias_id TEXT UNIQUE NOT NULL,
    asset_ref TEXT NOT NULL,
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
    status TEXT DEFAULT 'Pending_Admin_Approval',
    evidence_path TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_aliases_asset_ref ON asset_aliases(asset_ref);
CREATE INDEX IF NOT EXISTS idx_aliases_meta_post ON asset_aliases(meta_post_id);
CREATE INDEX IF NOT EXISTS idx_aliases_status ON asset_aliases(status);
