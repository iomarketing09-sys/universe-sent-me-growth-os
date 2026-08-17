---
title: "Prioridad de siguientes pendientes del Growth OS"
purpose: "Ordenar el trabajo posterior al análisis visual y taxonómico de julio según impacto, urgencia, dependencia y criterio de cierre."
status: "Active"
created: 2026-08-17
updated: 2026-08-17
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-17_Analisis_Julio_Taxonomia_y_Pendientes_Growth_OS.md"
  - "Operations/Research/2026-08-15_Auditoria_General_Growth_OS.md"
  - "Operations/Research/2026-08-15_Deuda_Documental_P2.md"
  - "GrowthOS/00_01_Changelog_GrowthOS.md"
organization: "Operations/Research"
---

# Prioridad de siguientes pendientes del Growth OS

## Decisión CGO

Después del análisis visual de junio y julio, el siguiente trabajo no debe ser modificar el canon ni producir más recomendaciones aisladas. La prioridad es cerrar la trazabilidad experimental de agosto y ampliar la muestra de julio con la taxonomía ya corregida.

## Orden de trabajo

| Prioridad | Pendiente | Por qué importa | Dependencias | Criterio de cierre |
|---|---|---|---|---|
| P0 | Cerrar el ciclo de aprendizaje de la prueba activa | Sin métricas comparables no sabemos si los cambios de frecuencia, reuse y horario funcionaron | Publicación real, timestamps y snapshots válidos | Cada fila elegible tiene baseline, corte 24h/72h o corte observado separado, y el experimento tiene veredicto |
| P1 | Monitorear la ola Facebook 17–30 | Es la prueba actual que debe validar o invalidar la estrategia | Ledger de publicación y estado `Programada → Publicada` | Todas las filas publicadas tienen permalink, timestamp y métricas registradas |
| P1 | Ampliar la recopilación individual de julio | Los seis top posts son una muestra útil pero parcial | Más Meta IDs, assets y comentarios priorizados por shares/comentarios | Nuevo lote reconciliado con asset, Meta ID, métricas y taxonomía visual |
| P1 | Consolidar la fuente maestra por pieza | Evita duplicados y permite automatizar sin perder trazabilidad | Campos normalizados y validación de IDs | Una fila por pieza conecta CNT, Asset_Ref, Drive ID, Meta ID, permalink, canon, producción y publicación |
| P2 | Actualizar baseline separando Facebook e Instagram | Las métricas de canal no deben mezclarse | Ventanas válidas del lote 15–16 y publicaciones posteriores | Baseline con definiciones, timestamps y canal separados |
| P2 | Revisar la Biblia con Claude | Los datos deben informar hipótesis, no modificar canon automáticamente | Changelog, taxonomía y evidencia histórica | Cada regla queda clasificada como sustentada, compatible, contradicha o sin evidencia |
| P2 | Continuar atención comunitaria incremental | La comunidad aporta aprendizaje y oportunidades de respuesta | Cursor vigente y aprobación humana | Solo comentarios reales y pendientes; ninguna respuesta automática no aprobada |
| P2 | Mantener Instagram controlado | El scheduler histórico produjo errores y no debe reactivarse sin playbook | Playbook autocontenido e idempotencia | Nueva campaña aprobada, fila por fila, sin duplicados ni ejecución tardía |
| Diferido | CNT-004 | Tiene conflicto narrativo y el usuario decidió no desarrollarlo | Nueva decisión creativa | Permanece fuera de producción y no se usa como evidencia activa |
| Controlado | Make heredado | Solo debe conservarse como trazabilidad histórica | Ninguna | No aparece como arquitectura activa en documentos de control |

## Secuencia recomendada

La primera acción debe ser el monitoreo y la medición de la prueba activa de Facebook. La taxonomía histórica de julio ya está lista para recibir un nuevo lote, pero no debe distraer del experimento vigente. La segunda acción será ampliar julio con los posts que tengan más shares y comentarios, porque esos registros aportarán más evidencia que una ampliación aleatoria.

Después conviene consolidar la fuente maestra y actualizar la baseline por canal. La revisión con Claude debe ocurrir cuando la evidencia esté organizada; así Claude revisará datos trazables y no interpretaciones aisladas de la conversación.

## No hacer todavía

No modificar el canon solo porque un personaje, humor o horario aparezca asociado a un post exitoso. No declarar que Universe es el motor del rendimiento de julio. No mezclar lifetime histórico con 24/72 horas. No reactivar el scheduler histórico de Instagram ni usar CNT-004 en producción.
