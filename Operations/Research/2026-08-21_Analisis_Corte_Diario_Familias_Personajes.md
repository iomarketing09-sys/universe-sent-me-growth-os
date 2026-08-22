---
title: "Análisis del corte diario por familias y personajes"
purpose: "Desglosar el corte observado del 21 de agosto y revisar hipótesis con shares y comentarios."
status: Active
created: 2026-08-21
updated: 2026-08-21
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-21_Corte_Diario_Metricas_2200.md"
  - "Operations/Research/2026-08-20_Revision_Claude_Hipotesis_Taxonomia_Humor.md"
  - "Operations/Research/2026-08-17_Taxonomia_Editorial_Contenido_USM.md"
  - "GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md"
organization: "Operations/Research"
---

# Alcance y método
El análisis usa el corte diario capturado el 21 de agosto a las 22:03 en `America/Matamoros`: 12 publicaciones reales, 10 imágenes/posts y 2 Reels. Las cifras son acumulados observables al momento de extracción. La familia es una clasificación primaria y provisional; no se asignan varias familias a la misma publicación para evitar doble conteo. `Caption_Treatment` se analiza por separado.

## Resumen por formato
| Formato | n | Interacciones | Media | Mediana | Shares | Comentarios |
|---|---:|---:|---:|---:|---:|---:|
| Imágenes/posts | 10 | 475 | 47.5 | 42.5 | 128 | 18 |
| Reels | 2 | 20 | 10.0 | 10.0 | 4 | 2 |
| Total editorial | 12 | 495 | 41.25 | 35.0 | 132 | 20 |

## Rendimiento por familia primaria
| Familia | n | Interacciones | Media | Mediana | Shares | Comentarios | Shares/post | Comentarios/post | Evidencia |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Character_POV_reveal | 1 | 9 | 9.0 | 9 | 1 | 1 | 1.0 | 1.0 | Señal descriptiva |
| Conversación_Relacional | 1 | 29 | 29.0 | 29 | 3 | 2 | 3.0 | 2.0 | Señal descriptiva |
| Difusión_Minimal | 3 | 148 | 49.33 | 49 | 33 | 7 | 11.0 | 2.33 | Señal para seguimiento |
| Personaje_Marcador | 1 | 78 | 78.0 | 78 | 24 | 2 | 24.0 | 2.0 | Señal descriptiva |
| Relatable_Social | 3 | 156 | 52.0 | 57 | 52 | 2 | 17.33 | 0.67 | Señal para seguimiento |
| Sequential_visual_reaction | 1 | 11 | 11.0 | 11 | 3 | 1 | 3.0 | 1.0 | Señal descriptiva |
| Ácido_Interpersonal | 2 | 64 | 32.0 | 32.0 | 16 | 5 | 8.0 | 2.5 | Señal descriptiva |

## Rendimiento por personaje principal
| Personaje | n | Interacciones | Media | Mediana | Shares | Comentarios | Shares/post | Comentarios/post | Nota |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Elara | 1 | 30 | 30.0 | 30 | 7 | 2 | 7.0 | 2.0 | n=1; no inferir efecto de personaje. |
| Evan | 1 | 11 | 11.0 | 11 | 3 | 1 | 3.0 | 1.0 | n=1; no inferir efecto de personaje. |
| Ganso | 1 | 78 | 78.0 | 78 | 24 | 2 | 24.0 | 2.0 | n=1; no inferir efecto de personaje. |
| Maeve | 1 | 29 | 29.0 | 29 | 3 | 2 | 3.0 | 2.0 | n=1; no inferir efecto de personaje. |
| No identificado | 1 | 57 | 57.0 | 57 | 19 | 0 | 19.0 | 0.0 | No identificado: no atribuir al personaje por filename. |
| Universe | 6 | 256 | 42.67 | 42.5 | 67 | 10 | 11.17 | 1.67 | Señal descriptiva; no causal. |
| Wilfred | 1 | 34 | 34.0 | 34 | 9 | 3 | 9.0 | 3.0 | n=1; no inferir efecto de personaje. |

## Lectura de shares y comentarios
Los shares representan la señal de difusión y los comentarios la señal de conversación; no se combinan en una sola conclusión causal. La mayor concentración de shares pertenece a piezas de imagen con caption mínimo y situación reconocible, pero la muestra mezcla reuse, personajes y franjas. Por ello, `Difusión_Minimal`, `Relatable_Social` y `Personaje_Marcador` quedan como direcciones de prueba, no como familias ganadoras.

## Revisión de hipótesis actuales
| Hipótesis | Evidencia del corte | Estado actualizado | Implicación |
|---|---|---|---|
| TAX-02 — situación reconocible/compartibilidad explican mejor que personaje aislado | Los líderes de shares fueron 2607794/Universe (26), 2608038/Ganso (24), 2607838/sin personaje confirmado (19), 260635/Universe (16) y 260508/Universe (12). La señal atraviesa más de un personaje y favorece situaciones/plantillas compartibles. | Compatible pero no demostrada; reforzada direccionalmente | Priorizar hooks transferibles y remates fáciles de compartir; no atribuir el resultado a Universe o Ganso por sí solos. |
| HUM-06 — caption mínimo/emojis pueden favorecer difusión | Las piezas de imagen con caption mínimo acumularon 128 shares; el reporte no contiene un control balanceado por familia, personaje y horario. | Compatible pero no universal; señal operativa | Mantener caption mínimo como tratamiento a probar, separándolo de Caption_Function y comparándolo con refuerzo/conversacional. |
| HUM-02 — conflicto interpersonal comprensible amplifica humor ácido | Wilfred ácido logró 9 shares/3 comentarios y Elara romance ácido 7/2, pero son n=1 por personaje y no hay control pareado. | Exploratoria, no confirmada | Crear casos comparables de observacional, diálogo ácido y autodesprecio por separado. |
| FAM-05 — personaje visualmente marcado sostiene difusión | Ganso 24 shares y Wilfred 9 shares, pero Universe también concentra shares y el caso sin personaje confirmado obtuvo 19. | Compatible pero no demostrada | Usar personajes como variables de prueba, no como explicación automática del rendimiento. |
| HB-REEL-MOTION-POV-MEME-01 — movimiento + POV/meme | Los dos Reels del corte tienen 4 shares y 2 comentarios básicos, pero sin views/reach/retención; el corte no permite evaluarla. | No evaluable con este corte | Mantener la generación de nuevos casos aprobados y leer Reels en una capa propia de métricas de video. |

## Decisiones operativas
1. Mantener `Relatable_Social`, `Difusión_Minimal` y `Personaje_Marcador` como direcciones de producción, no como ganadoras.
2. Usar shares como métrica principal para hipótesis de difusión y comentarios como señal separada para conversación.
3. No canonizar Universe, Ganso, Wilfred o Elara por este corte.
4. Mantener el caso sin personaje confirmado en `No identificado` hasta contar con revisión visual.
5. Continuar con Motion + POV/Meme en Reels, sin comparar sus interacciones básicas con las imágenes.

## Fuentes
- `Operations/Research/2026-08-21_Corte_Diario_Metricas_2200.json`.
- `Operations/Research/2026-08-16_Calendario_Operativo_17_30_Agosto.csv`.
- `Operations/Research/2026-08-17_Taxonomia_Editorial_Contenido_USM.md`.
- `Operations/Research/2026-08-20_Revision_Claude_Hipotesis_Taxonomia_Humor.md`.
- `GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md`.
