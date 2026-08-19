import fs from 'node:fs'
import { execFileSync } from 'node:child_process'

const root = '/home/ubuntu/universe-sent-me-growth-os'
const current = JSON.parse(fs.readFileSync(`${root}/Operations/Research/2026-08-19_Social_Performance_28D_Normalizado.json`, 'utf8'))
const prior = JSON.parse(execFileSync('git', ['show', '318624f^:Operations/Research/2026-08-19_Social_Performance_28D_Normalizado.json'], { cwd: root, encoding: 'utf8' }))
const sum = (rows, field) => rows.reduce((total, row) => total + Number(row[field] ?? 0), 0)
const comparable = (before, after, id, fields) => {
  const previous = new Map(before.map((row) => [row[id], row]))
  const shared = after.filter((row) => previous.has(row[id]))
  return Object.fromEntries(fields.map((field) => [field, { before: sum(shared.map((row) => previous.get(row[id])), field), after: sum(shared, field), delta: sum(shared, field) - sum(shared.map((row) => previous.get(row[id])), field) }]))
}
const ig = comparable(prior.platforms.Instagram.content_rows, current.platforms.Instagram.content_rows, 'content_id', ['views', 'reach', 'engagement', 'likes', 'shares', 'saves_or_favorites'])
const tt = comparable(prior.platforms.TikTok.content_rows, current.platforms.TikTok.content_rows, 'content_id', ['views', 'engagement', 'likes', 'shares', 'saves_or_favorites'])
const yt = comparable(prior.platforms.YouTube.lifetime_snapshots, current.platforms.YouTube.lifetime_snapshots, 'content_id', ['lifetime_views_snapshot', 'likes_snapshot', 'comments_snapshot'])
const detailDeltas = (before, after, id, label, field) => {
  const previous = new Map(before.map((row) => [row[id], row]))
  return after.filter((row) => previous.has(row[id])).map((row) => ({ id: row[id], label: row[label] ?? row[id], delta: Number(row[field] ?? 0) - Number(previous.get(row[id])[field] ?? 0) })).filter((row) => row.delta !== 0).sort((a, b) => b.delta - a.delta)
}
const report = {
  title: 'Comparación de snapshots 28D', purpose: 'Medir variación observada entre extracciones del mismo rango sin convertir snapshots lifetime en crecimiento atribuido al período.', status: 'Active', created: '2026-08-19', updated: '2026-08-19', version: '1.0', author: 'Manus AI', related_documents: ['2026-08-19_Social_Performance_28D_Normalizado.json', '2026-08-19_Retorno_Engagement_Esfuerzo_28D.json'],
  fixed_window: current.cut, prior_retrieved_at: prior.retrieved_at, current_retrieved_at: current.retrieved_at, comparison_type: 'same_window_snapshot_delta',
  platforms: { Instagram: { matched_pieces: current.platforms.Instagram.content_rows.length, metrics: ig, top_view_deltas: detailDeltas(prior.platforms.Instagram.content_rows, current.platforms.Instagram.content_rows, 'content_id', 'caption', 'views'), interpretation: 'Cambio observado de snapshots lifetime sobre las mismas piezas; no es crecimiento de publicaciones nuevas.' }, TikTok: { matched_pieces: current.platforms.TikTok.content_rows.length, metrics: tt, interpretation: 'Cambio observado de snapshots lifetime sobre las mismas piezas; no es crecimiento de publicaciones nuevas.' }, YouTube: { matched_pieces: current.platforms.YouTube.lifetime_snapshots.length, metrics: yt, top_view_deltas: detailDeltas(prior.platforms.YouTube.lifetime_snapshots, current.platforms.YouTube.lifetime_snapshots, 'content_id', 'title', 'lifetime_views_snapshot'), interpretation: 'Cambio de snapshot lifetime; separar de la actividad diaria del corte.' }, Facebook: { comparable: false, interpretation: 'El artefacto de Windsor se recuperó desde caché con el mismo data_fetched_at. No hay nueva variación temporal atribuible entre snapshots.' } },
  limits: ['Las cuatro plataformas comparten un rango de publicación, no una ventana idéntica de rendimiento.', 'Facebook no debe compararse con Instagram, TikTok o YouTube por engagement absoluto.', 'Un delta de snapshot lifetime no prueba crecimiento orgánico del período sin una nueva ventana temporal de actividad.']
}
fs.writeFileSync(`${root}/Operations/Research/2026-08-19_Comparacion_Snapshots_28D.json`, JSON.stringify(report, null, 2) + '\n')
console.log(JSON.stringify(report, null, 2))
