# Regla de métricas automáticas para campañas

**Estado:** Activa
**Vigente desde:** 2026-10-30
**Dueño operativo:** CGO / `modules/intelligence`
**Documento relacionado:** `Studio_Governance.md`, `GrowthOS/00_Índice.md`, `modules/intelligence/README.md`

## Regla

Toda campaña de Meta Ads con `meta_ids.json` y una fecha válida de inicio debe
generar cortes automáticos de métricas por anuncio. La captura no depende de que
alguien recuerde ejecutarla.

## Cortes obligatorios

| Corte | Momento | Uso |
| --- | --- | --- |
| `E24` | 24 horas transcurridas | Señal temprana de entrega y CPA |
| `E48` | 48 horas transcurridas | Revisión principal de rendimiento por anuncio |
| `E72` | 72 horas transcurridas | Confirmar tendencia antes de decidir |
| `E96...` | Cada 24 horas hasta el cierre | Seguimiento de campañas de mayor duración |
| `FINAL` | 2 horas después del cierre | Cierre y aprendizaje de la campaña |

Los cortes se calculan con horas transcurridas reales. Un cambio de horario de
verano no mueve el checkpoint: para la campaña de Flexi iniciada el
`2026-10-30 17:36 CDT`, el `E48` corresponde al
`2026-11-01 16:36 CST`.

## Salidas

Cada corte genera el reporte de métricas y un plan de cambios local:

- `tenants/<tenant>/ads/insights/captures/<slug>/<checkpoint>.json`
- `tenants/<tenant>/ads/insights/captures/<slug>/<checkpoint>.md`
- `tenants/<tenant>/ads/plans/<slug>/<checkpoint>.json`
- `tenants/<tenant>/ads/plans/<slug>/<checkpoint>.md`

El estado idempotente vive en
`tenants/<tenant>/ads/insights/capture_state.json`. Los archivos operativos no
se versionan en Git.

Los planes viven fuera de la carpeta ignorada de capturas porque son evidencia
de una decisión propuesta y deben poder revisarse o aprobarse sin depender de
un archivo operativo que se pueda borrar.

El reporte incluye gasto, impresiones, clics, CTR, conversaciones y costo por
conversación de cada anuncio, acumulados desde el inicio de la campaña
(`date_preset=maximum`). Los anuncios por encima de `8 MXN` por conversación se
marcan como alerta.

## Frecuencia y tolerancia

- El planificador revisa cada 15 minutos.
- No llama a Meta si no hay un checkpoint vencido.
- Si el equipo estuvo apagado y hay varios cortes vencidos, captura el más
  reciente y marca los anteriores como `missed`; no inventa una foto histórica.
- Si Meta falla, el checkpoint no se marca como completado y se reintenta en la
  siguiente pasada.

La decisión del plan usa la antigüedad programada del corte, no el retraso de la
captura. Si el `E48` se captura a las 50 horas, sigue siendo una decisión de 48
horas y no puede convertirse accidentalmente en una pausa del `E72`.

## Plan de cambios y pausas

El plan siempre se marca como `recommendation_only`, con
`execution_allowed=false` y `writes_to_meta=false`. Propone acciones por
anuncio, pero no las aplica.

### Niveles de pausa

| Nivel | Qué detiene | Uso en esta automatización |
| --- | --- | --- |
| Anuncio | Solo ese creativo | **Único nivel que el plan puede recomendar** |
| Ad set | Todos los anuncios y la entrega de ese conjunto | Nunca automático; requiere revisión humana |
| Campaña | Toda la campaña y todos sus anuncios | Nunca automático; requiere revisión humana |

La campaña de Flexi usa presupuesto a nivel campaña (CBO). Por eso la acción
segura es pausar un anuncio concreto: el resto de creativos y el aprendizaje de
la campaña siguen operando. Pausar toda la campaña para corregir un solo
anuncio destruiría la comparación y detendría la entrega completa.

### Política por defecto

| Regla | Valor |
| --- | --- |
| CPA objetivo | `8 MXN` por conversación |
| Ventana mínima para proponer pausa | `72 h` |
| Gasto mínimo para decidir | `60 MXN` |
| Conversaciones mínimas para juzgar CPA | `3` |
| Candidato a escala | CPA `<= 5.6 MXN` y `>= 5` conversaciones |
| Rotar creativo | `>= 1000` impresiones y CTR `< 1%` |

Antes de `72 h`, una señal mala produce `watch`, no `pause_ad`. Una pausa solo
se propone cuando hay gasto suficiente y muestra suficiente (o gasto suficiente
sin ninguna conversación). La configuración por tenant puede sobrescribirse en
`tenants/<tenant>/ads/campaign_policy.json`.

Las acciones posibles son `pause_ad`, `watch`, `scale_candidate`,
`rotate_creative` y `keep`. Ninguna modifica presupuesto.

### Aprobación

1. El corte genera el plan automáticamente.
2. CGO revisa la evidencia y las precondiciones.
3. Fernando/CGO aprueba o rechaza cada acción.
4. Solo una capacidad de ejecución separada podría escribir en Meta; hoy no
   existe y este plan no la invoca.

Antes de cualquier ejecución futura, los IDs de campaña y ad set deben coincidir
entre `campaign.json`, `meta_ids.json` y `00_estado.md`. La captura reconcilia
automáticamente `campaign.json.published` usando primero los ad sets observados
en la respuesta de anuncios de Meta y, si no hay anuncios, `meta_ids.json`.

La corrección es solo local: no envía nada a Meta. Cada cambio queda registrado
en `campaign.json.metadata_reconciliation` con valor anterior, valor nuevo,
fecha y fuente. Si la campaña reporta varios ad sets o la metadata no se puede
leer, el plan marca `execution_blocked=true` y no corrige el dato.

En Flexi, el `2026-10-30` se reconcilió `published.adset_id` de
`120247658527640665` a `120247659400770665`; este último fue confirmado con una
lectura de Meta y pertenece a la campaña `120247658527630665`.

## Límite de automatización

La automatización **mide y recomienda**. No pausa anuncios, no cambia
presupuesto y no modifica la campaña. Cualquier decisión de gasto requiere
revisión humana según las reglas de `Studio_Governance.md`.

## Operación

```bash
# Ver cortes pendientes sin llamar a Meta
python3 scripts/run_ads_capture.py --all-tenants --dry-run

# Ejecutar capturas vencidas
python3 scripts/run_ads_capture.py --all-tenants

# Ver el estado persistido
cat tenants/flexi/ads/insights/capture_state.json

# Regenerar un plan local desde una captura, sin red ni cambios en Meta
python3 tools/ads_plan.py --tenant flexi \
  --campaign 120247658527630665 --checkpoint E48
```

El timer dedicado está en `scripts/growth-os-ads.timer`. Mientras no se instale,
el timer de Instagram, que ya corre cada 15 minutos, ejecuta el mismo latido de
cortes antes de su propia revisión. Al instalar el timer dedicado, el hook de
Instagram se desactiva automáticamente para evitar llamadas duplicadas.
