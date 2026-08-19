import fs from 'node:fs'
import path from 'node:path'

const root = '/home/ubuntu/universe-sent-me-growth-os'
const social = JSON.parse(fs.readFileSync(path.join(root, 'Operations/Research/2026-08-19_Social_Performance_28D_Normalizado.json'), 'utf8'))
const fbAudit = JSON.parse(fs.readFileSync(path.join(root, 'Operations/Research/2026-08-19_Meta_Reels_Audit.json'), 'utf8'))
const costInventory = JSON.parse(fs.readFileSync(path.join(root, 'Operations/Research/2026-08-19_Inventario_Coste_Reels_28D.json'), 'utf8'))
const youtubeNative = JSON.parse(fs.readFileSync(path.join(root, 'Operations/Research/2026-08-19_YouTube_Metadata_Nativo.json'), 'utf8'))
const historicalAdjudications = JSON.parse(fs.readFileSync(path.join(root, 'Operations/Research/2026-08-19_Publicaciones_Historicas_Adjudicadas.json'), 'utf8'))
const reconciliationDecisions = JSON.parse(fs.readFileSync(path.join(root, 'Operations/Research/2026-08-19_Decisiones_Reconciliacion_Reels.json'), 'utf8'))
const youtubeDates = new Map(youtubeNative.rows.map((row) => [row.video, row]))
const highEvidenceLinks = JSON.parse(fs.readFileSync(path.join(root, 'Operations/Research/2026-08-19_Relaciones_Reels_Alta_Evidencia.json'), 'utf8'))
const highEvidenceConceptByContentId = new Map(highEvidenceLinks.relationships.flatMap((relationship) => relationship.publications.map((publication) => [publication.content_id, relationship.canonical_concept_id])))
const driveAssetInventory = JSON.parse(fs.readFileSync(path.join(root, 'Operations/Research/2026-08-19_Inventario_Assets_Drive_Reels.json'), 'utf8'))
const driveEvidenceByContentId = new Map(driveAssetInventory.asset_links.flatMap((link) => link.platform_content_ids.map((contentId) => [contentId, link])))
const reconciliationDecisionByContentId = new Map(reconciliationDecisions.decisions.map((decision) => [decision.content_id, decision]))
const evidenceLabels = {
  'CON-2026-08-05-Instante_suspendido': { content_asset_id: 'CNT-015', experiment_id: 'Sin_etiqueta_historica', hypothesis_ids: [], evidence: 'GrowthOS/07_00_Registro_Maestro_Reels.md: CNT-015 publicado en cascada el 5 de agosto.' },
}
const conceptIdFor = (contentId, text) => highEvidenceConceptByContentId.get(contentId) ?? driveEvidenceByContentId.get(contentId)?.canonical_concept_id ?? canonicalConcept(text)

const normalize = (value = '') => value
  .toLowerCase()
  .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
  .replace(/#\S+/g, ' ')
  .replace(/[^a-z0-9\s]/g, ' ')
  .replace(/\s+/g, ' ')
  .trim()

const detectCharacter = (value = '') => {
  const text = value
    .toLowerCase()
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/#/g, ' ')
    .replace(/[^a-z0-9\s]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
  if (text.includes('wilfred')) return 'Wilfred'
  if (text.includes('fantasma')) return 'Fantasma'
  if (text.includes('elara')) return 'Elara'
  if (text.includes('kiri') || text.includes('hada')) return 'Kiri'
  if (text.includes('evan')) return 'Evan'
  if (text.includes('universe') || text.includes('gato')) return 'Universe'
  return 'Sin clasificar'
}

const canonicalConcept = (value = '') => {
  const text = normalize(value)
  if (text.includes('mi gato sabe hacer de todo')) return 'CON-2026-07-30-Gato_hace_de_todo'
  if (text.includes('rock bien gotico') || text.includes('juan gabriel')) return 'CON-2026-07-29-Rock_vs_Juan_Gabriel'
  if (text.includes('muros vemos') || text.includes('inbox no sabemos')) return 'CON-2026-08-01-Muros_e_Inbox'
  if (text.includes('vitamina b') || text.includes('instante suspendido')) return 'CON-2026-08-05-Instante_suspendido'
  if (text.includes('sabiduria del bosque es clara') || text.includes('verdadero caos esta en el mensaje directo')) return 'CON-2026-08-02-Muros_e_Inbox'
  if (text.includes('hay conversaciones que no llegan a ningun lado')) return 'CON-2026-08-03-Conversaciones_atrancadas'
  if (text.includes('sales de la realidad') || text.includes('espacio liminal definitivo')) return 'CON-2026-08-04-Fantasma_Backrooms'
  if (text.includes('universe no sabe que trae en la caja')) return 'CON-2026-08-09-Caja_de_Luna'
  if (text.includes('ojos correctos')) return 'CON-2026-08-05-Ojos_correctos'
  if (text.includes('habilidades no vienen en el manual') || text.includes('habilidades que no vienen en el manual')) return 'CON-2026-08-03-Habilidades_manual'
  return null
}

const records = []
for (const reel of fbAudit.video_reels) {
  const engagement = (reel.reactions ?? 0) + (reel.comments ?? 0) + (reel.shares ?? 0)
  records.push({
    platform: 'Facebook', content_id: reel.id, published_at: reel.created_time, content_type: 'Reel',
    title_or_caption: reel.message, character: detectCharacter(reel.message), canonical_concept_id: conceptIdFor(reel.id, reel.message),
    engagement, views: null, reach: null, source: '2026-08-19_Meta_Reels_Audit.json', evidence_status: 'Confirmado_por_Meta_API',
  })
}
for (const row of historicalAdjudications.rows) {
  if (records.some((record) => record.content_id === row.content_id)) continue
  records.push({
    platform: row.platform, content_id: row.content_id, published_at: row.published_at, content_type: row.content_type,
    title_or_caption: row.title_or_caption, character: detectCharacter(row.title_or_caption), canonical_concept_id: conceptIdFor(row.content_id, row.title_or_caption),
    engagement: null, views: null, reach: null, source: row.source, evidence_status: row.evidence_status,
  })
}
for (const row of social.platforms.Instagram.content_rows.filter((row) => row.content_type === 'Reel')) {
  records.push({ platform: 'Instagram', content_id: row.content_id, published_at: row.published_at, content_type: 'Reel', title_or_caption: row.caption, character: detectCharacter(row.caption), canonical_concept_id: conceptIdFor(row.content_id, row.caption), engagement: row.engagement, views: row.views, reach: row.reach, source: row.source, evidence_status: 'Confirmado_por_Windsor' })
}
for (const row of social.platforms.TikTok.content_rows) {
  records.push({ platform: 'TikTok', content_id: row.content_id, published_at: row.published_at, content_type: 'Video', title_or_caption: row.caption, character: detectCharacter(row.caption), canonical_concept_id: conceptIdFor(row.content_id, row.caption), engagement: row.engagement, views: row.views, reach: row.reach, source: row.source, evidence_status: 'Confirmado_por_Windsor' })
}
for (const row of social.platforms.YouTube.lifetime_snapshots) {
  const native = youtubeDates.get(row.content_id)
  records.push({ platform: 'YouTube', content_id: row.content_id, published_at: native?.published_at ?? null, content_type: 'Video / Short', title_or_caption: row.title, character: detectCharacter(row.title), canonical_concept_id: conceptIdFor(row.content_id, row.title), engagement: row.engagement, views: row.lifetime_views_snapshot, reach: null, source: native ? 'Windsor.ai:youtube; metadata nativo' : row.source, evidence_status: native ? 'Confirmado_por_Windsor; fecha_publicacion_confirmada' : 'Confirmado_por_Windsor; fecha_publicacion_pendiente' })
}

const concepts = Object.values(records.reduce((acc, row) => {
  if (!row.canonical_concept_id) return acc
  const cluster = acc[row.canonical_concept_id] ?? { canonical_concept_id: row.canonical_concept_id, publications: [] }
  cluster.publications.push({ platform: row.platform, content_id: row.content_id, evidence_status: row.evidence_status })
  acc[row.canonical_concept_id] = cluster
  return acc
}, {}))
const crossPlatformConcepts = concepts.filter((concept) => new Set(concept.publications.map((publication) => publication.platform)).size > 1)
const crossPlatformContentIds = new Set(crossPlatformConcepts.flatMap((concept) => concept.publications.map((publication) => publication.content_id)))

const costMap = new Map(costInventory.rows.map((row) => [`${row.platform}|${row.content_id}`, row.cost_mxn]))
const enriched = records.map((row) => {
  const label = row.canonical_concept_id ? evidenceLabels[row.canonical_concept_id] : null
  const decision = reconciliationDecisionByContentId.get(row.content_id)
  return {
    ...row,
    cost_mxn: costMap.get(`${row.platform}|${row.content_id}`) ?? null,
    drive_asset_evidence: driveEvidenceByContentId.get(row.content_id) ?? null,
    content_asset_id: label?.content_asset_id ?? null,
    experiment_id: label?.experiment_id ?? 'Sin_etiqueta_historica',
    hypothesis_ids: label?.hypothesis_ids ?? [],
    experiment_evidence: label?.evidence ?? 'No existe Experiment_ID o Hypothesis_ID explícito en las fuentes auditadas; no se infiere.',
    reconciliation_decision: decision?.resolution_type ?? null,
    crosspost_status: decision?.crosspost_status ?? null,
  }
})
const unlinkedRecords = enriched.filter((row) => !crossPlatformContentIds.has(row.content_id))
const pendingReviewRecords = unlinkedRecords.filter((row) => !reconciliationDecisionByContentId.get(row.content_id)?.review_closed)
const result = {
  title: 'Historial consolidado de Reels y videos cortos',
  purpose: 'Inventario reconciliable de Reels y videos cortos publicados; no infiere cross-posts sin evidencia explícita.',
  status: 'Active',
  created_at: '2026-08-19',
  last_updated: '2026-08-19',
  version: '1.4',
  author: 'Manus AI',
  related_documents: [
    '2026-08-19_Relaciones_Reels_Alta_Evidencia.json',
    '2026-08-19_Inventario_Assets_Drive_Reels.json',
    '2026-08-19_Piezas_Sin_Cascada_Revision.json',
    '2026-08-19_Publicaciones_Historicas_Adjudicadas.json',
    '2026-08-19_Decisiones_Reconciliacion_Reels.json',
    '../../GrowthOS/07_00_Registro_Maestro_Reels.md',
    '../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md',
  ],
  period: social.cut,
  records: enriched,
  explicit_cross_platform_concepts: crossPlatformConcepts,
  summary: {
    total_records: enriched.length,
    by_platform: Object.fromEntries(['Facebook', 'Instagram', 'TikTok', 'YouTube'].map((platform) => [platform, enriched.filter((row) => row.platform === platform).length])),
    explicit_cross_platform_concepts: crossPlatformConcepts.length,
    unlinked_records: unlinkedRecords.length,
    pending_cross_platform_review: pendingReviewRecords.length,
    closed_without_crosspost: unlinkedRecords.length - pendingReviewRecords.length,
    records_with_drive_asset_evidence: enriched.filter((row) => row.drive_asset_evidence).length,
    records_with_explicit_experiment_evidence: enriched.filter((row) => row.experiment_id !== 'Sin_etiqueta_historica').length,
  },
  limitations: [
    'Facebook audit identifica Reels por attachment_type=video/video_inline; no se infiere formato para posts estáticos.',
    'Los conceptos entre plataformas solo se agrupan mediante frase o título explícitamente coincidente, por relación de alta evidencia documentada, o por confirmación explícita de Fernando vinculada a un asset identificable de Drive.',
    'Las seis piezas de YouTube incluidas en este corte ya tienen fecha nativa confirmada; futuras piezas deben recuperar el mismo campo antes de la reconciliación.',
  ],
}

const target = path.join(root, 'Operations/Research/2026-08-19_Historial_Reels_Consolidado.json')
fs.writeFileSync(target, JSON.stringify(result, null, 2) + '\n')
console.log(JSON.stringify(result.summary, null, 2))
console.log(`OUTPUT ${target}`)
