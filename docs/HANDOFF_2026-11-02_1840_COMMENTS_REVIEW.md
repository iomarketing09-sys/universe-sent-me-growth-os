# Handoff — Comentarios Universe y revisión humana

**Fecha:** 2026-11-02 18:40 CST  
**Repo:** `/home/universe-sent-me/growth-os`  
**Rama:** `main`  
**Último commit:** `b89e417` — `feat(comments): separar revisión humana de publicación`

## Para continuar en un chat nuevo

Leer este archivo y revisar el estado real antes de actuar:

```text
Lee docs/HANDOFF_2026-11-02_1840_COMMENTS_REVIEW.md y continúa desde ahí.
No publiques, apruebes ni descartes comentarios sin instrucción humana explícita.
No commitees assets. La cola local es la fuente de verdad; Drive es solo backup.
```

## Estado operativo

Cola maestra:

`tenants/universe/comment_responses/facebook_comments/aprobaciones.json`

| Métrica | Valor |
|---|---:|
| Entradas totales | 54 |
| Publicadas | 42 |
| Descartadas | 12 |
| Pendientes de revisión | 0 |
| Aprobadas sin publicar | 0 |

- El último descarte autorizado fue `122179870935072582_2133805607219650`, por contenido sexual explícito. Fue una excepción explícita del usuario.
- La regla vigente es que el contenido sexual **no se descarta automáticamente**: se marca para revisión humana y no se responde solo.
- La detección determinista cubre palabras y emojis sexuales; el agente también puede clasificar `intent=sexual`.
- El publicador solo lee `aprobaciones.json` y lotes explícitos `aprobaciones_publish_*.json` con `kind: publish_batch`.
- Drive es backup de una sola vía; nunca sobrescribe la cola local.
- Los lotes cerrados y respaldos legacy están en `tenants/universe/comment_responses/facebook_comments/archive/`.
- La copia vieja de Drive quedó archivada en `GoogleDrive/Growth OS/archive/closed_batches/aprobaciones_nuevas_8.json`.

## Cambios ya publicados

El commit `b89e417` ya está en `origin/main` e incluye:

- Ruteo de contenido sexual a revisión humana en `modules/communications/agent.py` y `policy.py`.
- Conservación de la decisión `review` en el adaptador de `comments/facebook.py`.
- Worker restringido a la maestra y lotes publicables explícitos.
- Reconciliación de la cola y reconstrucción de `first_seen_at`.
- Archivado de 39 respaldos legacy y del lote cerrado, sin borrar contenido.
- Documentación y pruebas del flujo.

## Verificación

- `50 passed` en las pruebas focalizadas de comunicaciones, publicación, reconciliación y revisión.
- `comments_review`: 54 revisados, 42 aprobados/publicados, 12 descartados, 0 pendientes.
- `run_comments_publish --dry-run`: 0 colas con trabajo pendiente.
- La suite completa no fue concluyente por cuota de `/tmp` (`OSError: [Errno 122] Disk quota exceeded`), no por un fallo funcional observado en este bloque.

## Pendiente en Git

El working tree sigue mezclado y no tiene staging:

- 74 archivos rastreados modificados.
- 45 archivos sin rastrear.
- 0 archivos en staging.

**Decisión del usuario:** no commitear assets. Quedan fuera imágenes, videos, PDFs y cualquier material de campaña; no usar `git add -A` desde la raíz.

Bloques pendientes sugeridos:

1. **Operación y salud:** `modules/operations/`, `ops/services.yaml`, scripts de health, timers, `docs/OPERACION_COMPARTIDA.md`, pruebas de ops y configuración asociada.
2. **Meta/env y Social:** `modules/social/meta_publisher.py`, `modules/cgo/capabilities/meta_publishing.py`, `tests/test_env_config.py`, `tests/test_cgo.py` y cambios de monetización/sync relacionados.
3. **Flexi:** documentación, planes de ads, snapshots y logs de sincronización.
4. **GrowthOS/core:** documentación, inventarios canónicos y cambios de modelos; revisar aparte.

No incluir en ningún commit los assets de Micas ni archivos con extensiones de imagen/video/PDF/XLSX.

## Próximo orden sugerido

1. Revisar y commitear Operación/Salud como bloque independiente.
2. Revisar el bloque Meta/env/Social y sus pruebas.
3. Definir si Flexi y GrowthOS/core se publican por separado o quedan pendientes.
4. Mantener los assets completamente fuera de Git.

## Comandos útiles

```bash
python3 -m modules.cgo --mode comments_review --tenant universe
python3 scripts/run_comments_publish.py --tenant universe --dry-run --no-drive-sync
python3 scripts/run_ops_health.py --json
git status --short
git diff --cached --name-status
```

## Reglas de seguridad

- No publicar, aprobar ni descartar sin instrucción humana explícita.
- No publicar desde vistas de revisión ni lotes cerrados.
- No hacer que Drive sobrescriba la cola local.
- No automatizar el descarte de contenido sexual; enviarlo a revisión humana.
- No commitear assets.
- Revisar `git diff --cached --name-status` antes de cada commit.
