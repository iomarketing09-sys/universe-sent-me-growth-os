import fs from 'node:fs'
import path from 'node:path'

const root = '/home/ubuntu/universe-sent-me-growth-os'
const social = JSON.parse(fs.readFileSync(path.join(root, 'Operations/Research/2026-08-19_Social_Performance_28D_Normalizado.json'), 'utf8'))
const fbAudit = JSON.parse(fs.readFileSync(path.join(root, 'Operations/Research/2026-08-19_Meta_Reels_Audit.json'), 'utf8'))
const costInventory = JSON.parse(fs.readFileSync(path.join(root, 'Operations/Research/2026-08-19_Inventario_Coste_Reels_28D.json'), 'utf8'))

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
  return null
}

const records = []
for (const reel of fbAudit.video_reels) {
  const engagement = (reel.reactions ?? 0) + (reel.comments ?? 0) + (reel.shares ?? 0)
  records.push({
    platform: 'Facebook', content_id: reel.id, published_at: reel.created_time, content_type: 'Reel',
    title_or_caption: reel.message, character: detectCharacter(reel.message), canonical_concept_id: canonicalConcept(reel.message),
    engagement, views: null, reach: null, source: '2026-08-19_Meta_Reels_Audit.json', evidence_status: 'Confirmado_por_Meta_API',
  })
}
for (const row of social.platforms.Instagram.content_rows.filter((row) => row.content_type === 'Reel')) {
  records.push({ platform: 'Instagram', content_id: row.content_id, published_at: row.published_at, content_type: 'Reel', title_or_caption: row.caption, character: detectCharacter(row.caption), canonical_concept_id: canonicalConcept(row.caption), engagement: row.engagement, views: row.views, reach: row.reach, source: row.source, evidence_status: 'Confirmado_por_Windsor' })
}
for (const row of social.platforms.TikTok.content_rows) {
  records.push({ platform: 'TikTok', content_id: row.content_id, published_at: row.published_at, content_type: 'Video', title_or_caption: row.caption, character: detectCharacter(row.caption), canonical_concept_id: canonicalConcept(row.caption), engagement: row.engagement, views: row.views, reach: row.reach, source: row.source, evidence_status: 'Confirmado_por_Windsor' })
}
for (const row of social.platforms.YouTube.lifetime_snapshots) {
  records.push({ platform: 'YouTube', content_id: row.content_id, published_at: null, content_type: 'Video / Short', title_or_caption: row.title, character: detectCharacter(row.title), canonical_concept_id: canonicalConcept(row.title), engagement: row.engagement, views: row.lifetime_views_snapshot, reach: null, source: row.source, evidence_status: 'Confirmado_por_Windsor; fecha_publicacion_pendiente' })
}

const concepts = Object.values(records.reduce((acc, row) => {
  if (!row.canonical_concept_id) return acc
  const cluster = acc[row.canonical_concept_id] ?? { canonical_concept_id: row.canonical_concept_id, publications: [] }
  cluster.publications.push({ platform: row.platform, content_id: row.content_id, evidence_status: row.evidence_status })
  acc[row.canonical_concept_id] = cluster
  return acc
}, {}))

const costMap = new Map(costInventory.rows.map((row) => [`${row.platform}|${row.content_id}`, row.cost_mxn]))
const enriched = records.map((row) => ({ ...row, cost_mxn: costMap.get(`${row.platform}|${row.content_id}`) ?? null }))
const result = {
  purpose: 'Inventario reconciliable de Reels y videos cortos publicados; no infiere cross-posts sin evidencia explícita.',
  period: social.cut,
  records: enriched,
  explicit_cross_platform_concepts: concepts,
  summary: {
    total_records: enriched.length,
    by_platform: Object.fromEntries(['Facebook', 'Instagram', 'TikTok', 'YouTube'].map((platform) => [platform, enriched.filter((row) => row.platform === platform).length])),
    explicit_cross_platform_concepts: concepts.length,
    unlinked_records: enriched.filter((row) => !row.canonical_concept_id).length,
  },
  limitations: [
    'Facebook audit identifica Reels por attachment_type=video/video_inline; no se infiere formato para posts estáticos.',
    'Los conceptos entre plataformas solo se agrupan mediante frase o título explícitamente coincidente.',
    'YouTube requiere fecha de publicación primaria para su reconciliación temporal completa.',
  ],
}

const target = path.join(root, 'Operations/Research/2026-08-19_Historial_Reels_Consolidado.json')
fs.writeFileSync(target, JSON.stringify(result, null, 2) + '\n')
console.log(JSON.stringify(result.summary, null, 2))
console.log(`OUTPUT ${target}`)
