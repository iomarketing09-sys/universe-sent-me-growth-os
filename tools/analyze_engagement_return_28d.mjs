import fs from 'node:fs'
import path from 'node:path'

const root = '/home/ubuntu/universe-sent-me-growth-os'
const social = JSON.parse(fs.readFileSync(path.join(root, 'Operations/Research/2026-08-19_Social_Performance_28D_Normalizado.json'), 'utf8'))
const facebookRows = JSON.parse(fs.readFileSync(path.join(root, 'Operations/Research/2026-08-19_Windsor_Facebook_Organic_28D_Normalizado.json'), 'utf8')).rows

const sum = (rows, field) => rows.reduce((total, row) => total + Number(row[field] ?? 0), 0)
const instagramRows = social.platforms.Instagram.content_rows
const tikTokRows = social.platforms.TikTok.content_rows
const youtubeRows = social.platforms.YouTube.daily_rows
const facebook = { platform: 'Facebook', pieces: facebookRows.length, engagement: facebookRows.reduce((total, row) => total + Number(row.post_reactions_total ?? 0) + Number(row.post_comments_total ?? 0) + Number(row.post_activity_by_action_type_share ?? 0), 0), views: null, definition: 'reacciones + comentarios + shares', window: 'corte 22 jul–18 ago 2026' }
const records = [
  facebook,
  { platform: 'Instagram', pieces: instagramRows.length, engagement: sum(instagramRows, 'engagement'), views: sum(instagramRows, 'views'), definition: 'likes + comments + shares + guardados', window: 'snapshot actual / lifetime de piezas publicadas en el corte' },
  { platform: 'TikTok', pieces: tikTokRows.length, engagement: sum(tikTokRows, 'engagement'), views: sum(tikTokRows, 'views'), definition: 'likes + comments + shares + favoritos', window: 'snapshot actual / lifetime de piezas publicadas en el corte' },
  {
    platform: 'YouTube',
    pieces: social.platforms.YouTube.lifetime_snapshots.length,
    engagement: sum(youtubeRows, 'likes') + sum(youtubeRows, 'comments'),
    views: sum(youtubeRows, 'views'),
    definition: 'likes + comments + shares de actividad diaria acumulada',
    window: 'actividad diaria acumulada del corte',
  },
].map((record) => ({
  ...record,
  engagement_per_piece: record.engagement / record.pieces,
  engagement_per_100_views: record.views ? (record.engagement / record.views) * 100 : null,
}))

records.sort((a, b) => b.engagement_per_piece - a.engagement_per_piece)
const result = {
  period: social.cut,
  metric: 'engagement por pieza publicada',
  proxy_definition: 'Una pieza publicada equivale a una unidad de esfuerzo operativo. El resultado no representa horas de producción, costo de edición ni nivel de complejidad creativa.',
  records,
  recommendation: {
    primary_distribution: 'Facebook',
    video_growth_experiment: 'TikTok',
    selective_testing: 'YouTube',
    reduce_or_reframe: 'Instagram',
  },
}

const target = path.join(root, 'Operations/Research/2026-08-19_Retorno_Engagement_Esfuerzo_28D.json')
fs.writeFileSync(target, JSON.stringify(result, null, 2) + '\n')
console.log(JSON.stringify(result, null, 2))
