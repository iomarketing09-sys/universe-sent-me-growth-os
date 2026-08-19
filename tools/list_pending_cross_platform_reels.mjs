import fs from 'node:fs'
import path from 'node:path'

const root = '/home/ubuntu/universe-sent-me-growth-os'
const historyPath = path.join(root, 'Operations/Research/2026-08-19_Historial_Reels_Consolidado.json')
const reviewPath = path.join(root, 'Operations/Research/2026-08-19_Piezas_Sin_Cascada_Revision.json')
const history = JSON.parse(fs.readFileSync(historyPath, 'utf8'))
const priorReview = fs.existsSync(reviewPath) ? JSON.parse(fs.readFileSync(reviewPath, 'utf8')) : { pieces: [] }
const priorReviewByContentId = new Map((priorReview.pieces ?? []).map((piece) => [piece.content_id, piece]))
const crossPlatformIds = new Set(history.explicit_cross_platform_concepts.flatMap((concept) => concept.publications.map((publication) => publication.content_id)))
const pending = history.records
  .filter((record) => !crossPlatformIds.has(record.content_id))
  .sort((a, b) => String(a.published_at ?? '').localeCompare(String(b.published_at ?? '')))
  .map((record, index) => {
    const prior = priorReviewByContentId.get(record.content_id)
    return {
    review_id: prior?.review_id ?? `P${String(index + 1).padStart(2, '0')}`,
    platform: record.platform,
    published_at: record.published_at,
    content_type: record.content_type,
    content_id: record.content_id,
    title_or_caption: record.title_or_caption,
    character: record.character,
    canonical_concept_id: record.canonical_concept_id ?? 'Sin_concepto_confirmado',
    drive_asset_evidence: record.drive_asset_evidence
      ? { strength: record.drive_asset_evidence.strength, assets: record.drive_asset_evidence.drive_assets.map((asset) => ({ id: asset.id, name: asset.name })) }
      : null,
    review_status: prior?.review_status ?? 'Pendiente_de_confirmacion_de_Fernando',
    ...(prior?.confirmed_platforms_by_fernando ? { confirmed_platforms_by_fernando: prior.confirmed_platforms_by_fernando } : {}),
    ...(prior?.reconciliation_gap ? { reconciliation_gap: prior.reconciliation_gap } : {}),
  }
  })

const artifact = {
  title: 'Piezas sin cascada cross-platform confirmada — revisión guiada',
  purpose: 'Presentar las publicaciones que aún no pertenecen a una relación multicanal verificada y registrar decisiones explícitas del usuario.',
  status: 'Review',
  created_at: '2026-08-19',
  last_updated: '2026-08-19',
  version: '1.2',
  author: 'Manus AI',
  related_documents: [
    '2026-08-19_Historial_Reels_Consolidado.json',
    '2026-08-19_Inventario_Assets_Drive_Reels.json',
    '2026-08-19_Relaciones_Reels_Alta_Evidencia.json',
    '../../GrowthOS/07_00_Registro_Maestro_Reels.md',
  ],
  count: pending.length,
  pieces: pending,
  decision_rule: 'Solo se agregará una relación cross-platform al historial consolidado cuando Fernando confirme las publicaciones y se recupere un Platform_Content_ID, URL o fecha que permita identificarlas de manera inequívoca.',
}

fs.writeFileSync(reviewPath, JSON.stringify(artifact, null, 2) + '\n')
console.log(JSON.stringify({ count: artifact.count, pieces: artifact.pieces }, null, 2))
console.log(`OUTPUT ${reviewPath}`)
