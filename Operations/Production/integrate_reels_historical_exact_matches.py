import json
from pathlib import Path

path = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/2026-08-19_Historial_Reels_Consolidado.json')
data = json.loads(path.read_text(encoding='utf-8'))
records = data.setdefault('records', [])
existing = {r.get('content_id') for r in records}

new_records = [
    {
        'platform': 'Facebook',
        'content_id': '1036844829507460_122123860587072582',
        'published_at': '2026-05-24T21:33:33+0000',
        'content_type': 'Reel',
        'title_or_caption': '¡Descubre esta app de dramas! 🫠✨ https://apiv2.free-reels.com/frv2-api/l/2s4HnG6B0Iw',
        'character': 'Fantasma',
        'canonical_concept_id': 'CON-2026-05-24-Fantasma_tranquilo_viento',
        'engagement': 3,
        'views': None,
        'reach': None,
        'source': 'Meta historical feed; Drive exact visual crossmatch XMR-001',
        'evidence_status': 'Confirmado_por_Meta_API_y_revision_visual_Drive',
        'drive_asset_evidence': ['175XnmOVnBPgVCFlwyDWCZ3jCAmB2MOjO'],
        'content_asset_id': None,
        'experiment_id': 'Sin_etiqueta_historica',
        'hypothesis_ids': [],
        'experiment_evidence': 'No se atribuye a experimento; caption contiene URL externa.',
        'reconciliation_decision': 'Match_Visual_Exacto',
        'crosspost_status': 'No_verificado_en_esta_extension',
        'meta_reel_id': '1877535942934184',
        'permalink_url': 'https://www.facebook.com/reel/1877535942934184/',
        'is_published': True,
        'metrics_status': 'Meta_interactions_lifetime_consulted; views_reach_pendientes',
        'editorial_qualification': 'Exclude_from_clean_editorial_comparables_until_external_url_treatment_is_coded',
    },
    {
        'platform': 'Facebook',
        'content_id': '1036844829507460_122130226041072582',
        'published_at': '2026-06-14T00:13:49+0000',
        'content_type': 'Reel',
        'title_or_caption': 'Enculate de mi 🫠',
        'character': 'Man_unknown_character',
        'canonical_concept_id': 'CON-2026-06-14-Hoodie_Anillos_Energia',
        'engagement': 11,
        'views': None,
        'reach': None,
        'source': 'Meta historical feed; Drive exact visual asset-set crossmatch XMR-003',
        'evidence_status': 'Confirmado_por_Meta_API_y_revision_visual_Drive',
        'drive_asset_evidence': ['1vFRModK-KTYj6D9ZXhYBFhMOr3B-fS5F', '18GoVQOBam-Tgox4rXNyRwwZk19BBeEzF'],
        'content_asset_id': None,
        'asset_relationship': 'Asset_Set_Match',
        'experiment_id': 'Sin_etiqueta_historica',
        'hypothesis_ids': [],
        'experiment_evidence': 'Dos clips de Drive forman la secuencia del mismo Reel; no crear dos publicaciones.',
        'reconciliation_decision': 'Match_Visual_Exacto_Asset_Set',
        'crosspost_status': 'No_verificado_en_esta_extension',
        'meta_reel_id': '2417378928740605',
        'permalink_url': 'https://www.facebook.com/reel/2417378928740605/',
        'is_published': True,
        'metrics_status': 'Meta_interactions_lifetime_consulted; views_reach_pendientes',
        'editorial_qualification': 'Historical_editorial_record; character_not_canonized_from_filename',
    },
    {
        'platform': 'Facebook',
        'content_id': '1036844829507460_122134608507072582',
        'published_at': '2026-06-30T18:45:55+0000',
        'content_type': 'Reel',
        'title_or_caption': 'Ya le entendí a la vida banda... #universesentme #merlin #fifaworldcup',
        'character': 'Duck_unknown_character',
        'canonical_concept_id': 'CON-2026-06-30-Pato_Villano_EresAries',
        'engagement': 14,
        'views': None,
        'reach': None,
        'source': 'Meta historical feed; Drive exact visual crossmatch XMR-004',
        'evidence_status': 'Confirmado_por_Meta_API_y_revision_visual_Drive',
        'drive_asset_evidence': ['14Jwguu1pUljEBQtzZPWxc_fEOCWpwkKW'],
        'content_asset_id': None,
        'experiment_id': 'Sin_etiqueta_historica',
        'hypothesis_ids': [],
        'experiment_evidence': 'No se asigna hipótesis; el archivo conserva watermark/trait de IA para clasificación editorial.',
        'reconciliation_decision': 'Match_Visual_Exacto',
        'crosspost_status': 'No_verificado_en_esta_extension',
        'meta_reel_id': '1049041731412120',
        'permalink_url': 'https://www.facebook.com/reel/1049041731412120/',
        'is_published': True,
        'metrics_status': 'Meta_interactions_lifetime_consulted; views_reach_pendientes',
        'editorial_qualification': 'Exclude_from_clean_comparables_until_AI_watermark_and_external_character_treatment_are_coded',
    },
]

added = []
for record in new_records:
    if record['content_id'] not in existing:
        records.append(record)
        added.append(record['content_id'])

data['period'] = {'start': '2026-05-24', 'end': '2026-08-21'}
data['last_updated'] = '2026-08-21'
data['version'] = '1.6'
data['historical_extension_note'] = 'Three exact visual Drive↔Meta matches were integrated from May/June. Wilfred potion remains pending visual review; date proximity alone never creates a match.'
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'added': added, 'total_records': len(records), 'version': data['version']}, ensure_ascii=False))
