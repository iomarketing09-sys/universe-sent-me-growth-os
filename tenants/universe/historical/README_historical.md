# Integración Histórica - Tenant `universe`

**Fecha de integración:** 2026-09-06  
**Objetivo:** Hacer que el tenant `universe` reconozca y utilice su historial existente como baseline, sin destruir ni modificar los datos originales.

---

## Estructura de Directorios

```
historical/
├── publications/
│   ├── cortes_diarios_agosto_2026.csv           (6 publicaciones con métricas, experiment_id, hypothesis_id)
│   ├── actividad_diaria_instagram_jun_jul_2026.csv  (30 días de métricas diarias agregadas)
│   └── reportes_campanas_marzo_julio_2026/    (20 archivos CSV de campañas marzo-julio 2026)
├── metrics/
│   ├── rendimiento_horario_junio_2026.csv     (17 filas: agregado por hora para junio 2026)
│   └── cola_reutilizacion_junio_2026.csv      (7 ítems aprobados para reutilización)
├── experiments/
│   └── experimentos_históricos.csv            (2 experimentos: EXP-2026-08-CAL-01, EXP-2026-08-COMP-GAPS-01)
├── hypotheses/
│   └── hipótesis_históricas.csv               (5 hipótesis: HB-003 a HB-007, marcadas como INFERIDA)
├── assets/
│   └── inventario_memes.csv                   (200 assets, mayo-agosto 2026)
└── rules/
    └── regla_reutilizacion_30_dias.txt        (Regla del sistema documentada)
```

---

## Qué SÍ Contiene Esta Integración

| Categoría | Cantidad | Detalle |
|-----------|----------|---------|
| **Publicaciones históricas con métricas** | 6 (cortes diarios) + ~100 (reportes campaña) + 30 (diarias) | Fechas, tipos, métricas, experiment_id, hypothesis_id, asset_ref cuando existe |
| **Métricas históricas** | 3 fuentes | Rendimiento horario (junio), cortes diarios (agosto), actividad diaria (jun-jul) |
| **Experimentos históricos** | 2 | EXP-2026-08-CAL-01, EXP-2026-08-COMP-GAPS-01 |
| **Hipótesis históricas** | 5 | HB-003 a HB-007 (todas marcadas como INFERIDA) |
| **Assets inventariados** | 200 | Rutas, tamaños, fechas, carpetas (mayo-agosto 2026) |
| **Regla de reutilización** | 1 | 30 días documentada en rules/ |

---

## Qué NO Contiene (Limitaciones Conocidas)

1. **No hay genealogía exacta asset → publicación → métrica** para la mayoría de los 200 assets. Solo se conserva el vínculo cuando la fuente original incluye `asset_ref` o `asset_filename` no vacío.

2. **No se han calculado ventanas E0/E24/E72** para métricas históricas. Las métricas se conservan tal como aparecen en sus fuentes originales.

3. **Las descripciones de experimentos e hipótesis están marcadas como `INFERIDA`** porque no existían definiciones formales en las fuentes; se infirieron a partir de los nombres de ID y el contexto de las publicaciones asociadas.

4. **La regla de 30 días NO se ha aplicado retrospectivamente**. No se ha marcado ningún asset como bloqueado; la regla queda documentada para uso futuro en selección de contenido.

5. **No se han modificado los archivos del pipeline actual** (`config.json`, `.env`, `meta_import_week2.csv`, `publication_log_week2.csv`, `experiment_log.csv`, `hypothesis_bank.csv`, `metrics_snapshot_log.csv`, `test_now.csv` permanecen intactos).

6. **No se ha creado ninguna publicación nueva** ni modificado el scheduler/publisher.

---

## Cobertura Temporal

| Fuente | Periodo cubierto |
|--------|-----------------|
| Reportes de campaña (Google Drive) | Marzo 2026 → Julio 2026 |
| Actividad diaria Instagram | 26 Junio 2026 → 24 Julio 2026 |
| Rendimiento horario | Junio 2026 (agregado) |
| Cola reutilización | Junio 2026 |
| Cortes diarios métricas | 24 Agosto 2026 |
| Inventario assets | Mayo 2026 → Agosto 2026 (concentración en junio) |

**Periodo histórico total:** **Marzo 2026 → Agosto 2026**

---

## Distinción Clara: HISTORIAL vs NUEVO SISTEMA

| Categoría | Ubicación | Estado |
|-----------|-----------|--------|
| **Historial original (solo lectura)** | `historical/` | Referencia, no se modifica |
| **Nuevo Growth OS (activo)** | Raíz del tenant (`config.json`, `.env`, `meta_import_week2.csv`, etc.) | En uso para nuevas publicaciones |
| **Datos actuales (logs activos)** | Raíz del tenant (`publication_log_week2.csv`, `experiment_log.csv`, `hypothesis_bank.csv`, `metrics_snapshot_log.csv`) | Se actualizan con cada publicación nueva |

---

## Cómo Consultar el Historial

### Contar publicaciones históricas con métricas
```bash
# Cortes diarios agosto
wc -l historical/publications/cortes_diarios_agosto_2026.csv
# → 7 líneas (1 header + 6 datos)

# Reportes campaña
find historical/publications/reportes_campanas_marzo_julio_2026 -name "*.csv" -exec wc -l {} \;
```

### Consultar experimentos históricos
```bash
cat historical/experiments/experimentos_históricos.csv
```

### Consultar hipótesis históricas
```bash
cat historical/hypotheses/hipótesis_históricas.csv
```

### Ver inventario de assets
```bash
wc -l historical/assets/inventario_memes.csv
# → 201 líneas (1 header + 200 assets)
```

### Ver regla de 30 días
```bash
cat historical/rules/regla_reutilizacion_30_dias.txt
```

---

## Verificación de Integridad (Realizada al Finalizar)

| Verificación | Resultado |
|--------------|-----------|
| Archivos origen vs destino (conteo filas) | ✅ Coinciden |
| Originales no modificados (timestamps, checksums) | ✅ Confirmado |
| Symlinks del tenant (`assets/USM`) intactos | ✅ Apuntan a Google Drive |
| Pipeline actual sin cambios | ✅ Confirmado |
| No se generaron publicaciones nuevas | ✅ Confirmado |

---

## Próximos Pasos (Fuera de Alcance Actual)

1. **Selección de contenido de junio**: Consultar `historical/publications/` y `historical/assets/inventario_memes.csv` aplicando la regla de 30 días.
2. **Migración exhaustiva asset → publicación**: Requiere trabajo manual o heurísticas adicionales.
3. **Cálculo de ventanas E0/E24/E72 retroactivas**: Solo si se define criterio claro de `captured_at_utc`.
4. **Validación formal de hipótesis históricas**: Requiere análisis estadístico sobre datos consolidados.

---

**Nota:** Este directorio `historical/` es de **solo lectura** para el sistema. Cualquier proceso que necesite escribir datos debe hacerlo en la raíz del tenant o en la base de datos GrowthOS, nunca aquí.
