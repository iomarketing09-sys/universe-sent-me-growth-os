import fs from 'node:fs'
import path from 'node:path'

const root = '/home/ubuntu/universe-sent-me-growth-os'
const source = JSON.parse(fs.readFileSync(path.join(root, 'Operations/Research/2026-08-19_Social_Performance_28D_Normalizado.json'), 'utf8'))
const costPerReel = 15

const instagramReels = source.platforms.Instagram.content_rows
  .filter((row) => row.content_type === 'Reel')
  .map((row) => ({ platform: 'Instagram', content_id: row.content_id, published_at: row.published_at, label: row.caption.replace(/\s+/g, ' ').slice(0, 120), engagement: row.engagement, views: row.views, cost_mxn: costPerReel, engagement_per_mxn: row.engagement / costPerReel, window: row.window_type, source: row.source }))

const tiktokVideos = source.platforms.TikTok.content_rows
  .map((row) => ({ platform: 'TikTok', content_id: row.content_id, published_at: row.published_at, label: row.caption.replace(/\s+/g, ' ').slice(0, 120), engagement: row.engagement, views: row.views, cost_mxn: costPerReel, engagement_per_mxn: row.engagement / costPerReel, window: row.window_type, source: row.source }))

const youtubeVideos = source.platforms.YouTube.lifetime_snapshots
  .map((row) => ({ platform: 'YouTube', content_id: row.content_id, published_at: null, label: row.title, engagement: row.engagement, views: row.lifetime_views_snapshot, cost_mxn: costPerReel, engagement_per_mxn: row.engagement / costPerReel, window: row.window_type, source: row.source }))

const groups = { Instagram: instagramReels, TikTok: tiktokVideos, YouTube: youtubeVideos }
const platform_summary = Object.fromEntries(Object.entries(groups).map(([platform, rows]) => {
  const engagement = rows.reduce((sum, row) => sum + row.engagement, 0)
  const cost_mxn = rows.length * costPerReel
  return [platform, { pieces: rows.length, engagement, cost_mxn, engagement_per_mxn: cost_mxn ? engagement / cost_mxn : null }]
}))

const result = {
  period: source.cut,
  cost_assumption: { amount_mxn: costPerReel, applies_to: 'Cada Reel o video corto tratado como pieza de producción individual', status: 'Supuesto_aprobado_por_Fernando', hours_status: 'Pendiente' },
  comparability_warning: 'Los IDs no contienen un mapeo completo de asset fuente entre plataformas. No sumar plataformas como piezas independientes para un ROI total hasta reconciliar cross-posts. El inventario presenta retorno por publicación dentro de cada plataforma.',
  platform_summary,
  rows: Object.values(groups).flat(),
}

const target = path.join(root, 'Operations/Research/2026-08-19_Inventario_Coste_Reels_28D.json')
fs.writeFileSync(target, JSON.stringify(result, null, 2) + '\n')
console.log(JSON.stringify(platform_summary, null, 2))
console.log(`OUTPUT ${target}`)
