import fs from 'node:fs'
import path from 'node:path'

const root = '/home/ubuntu/universe-sent-me-growth-os'
const social = JSON.parse(fs.readFileSync(path.join(root, 'Operations/Research/2026-08-19_Social_Performance_28D_Normalizado.json'), 'utf8'))

const facebook = { platform: 'Facebook', pieces: 119, engagement: 30729, views: null, definition: 'reacciones + comentarios + shares', window: 'corte 22 jul–18 ago 2026' }
const records = [
  facebook,
  ...['Instagram', 'TikTok'].map((platform) => ({
    platform,
    pieces: social.platforms[platform].aggregates.content_count,
    engagement: social.platforms[platform].aggregates.engagement_total,
    views: social.platforms[platform].aggregates.views_total,
    definition: platform === 'Instagram' ? 'media_engagement nativo' : 'likes + comments + shares + favoritos',
    window: 'snapshot actual / lifetime de piezas publicadas en el corte',
  })),
  {
    platform: 'YouTube',
    pieces: social.platforms.YouTube.lifetime_snapshots.length,
    engagement: social.platforms.YouTube.daily_aggregates.engagement_total,
    views: social.platforms.YouTube.daily_aggregates.views_total,
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
