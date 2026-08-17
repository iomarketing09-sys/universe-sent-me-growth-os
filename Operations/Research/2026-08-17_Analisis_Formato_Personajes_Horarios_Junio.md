---
title: "Análisis de formato, personajes y horarios de junio"
purpose: "Identificar patrones descriptivos de rendimiento en las 172 publicaciones de junio relacionadas con assets y posts editoriales."
status: "Review"
created: 2026-08-17
updated: 2026-08-17
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-17_Reporte_Final_Recopilacion_Junio.md"
  - "Operations/Research/2026-08-17_Junio_Analisis_Base.csv"
  - "Operations/Research/2026-08-17_Junio_Rendimiento_Personajes.csv"
  - "Operations/Research/2026-08-17_Junio_Rendimiento_Horarios.csv"
  - "Operations/Research/2026-08-17_Junio_Rendimiento_Formatos.csv"
organization: "Operations/Research"
---

# Análisis de formato, personajes y horarios de junio

## Resumen ejecutivo

El análisis utiliza 172 publicaciones de junio con relación confirmada entre asset y publicación editorial. Todas son piezas de **imagen estática**, por lo que junio no permite comparar formatos entre sí. La señal más útil aparece en la hora de publicación: las franjas de media mañana y noche presentan los promedios más altos, mientras que la tarde media muestra un rendimiento menor.

Los personajes no pueden evaluarse como grupos equilibrados porque la mayoría de los filenames genéricos contienen `Universe`; solo siete registros tienen etiquetas explícitas suficientemente identificables para personajes concretos o Aura. Esos casos son útiles como ejemplos editoriales, pero no como prueba estadística de que un personaje cause mejor rendimiento.

> **Conclusión CGO:** junio respalda una hipótesis de horario, no una conclusión definitiva de formato o personaje. La media mañana y la noche deben conservarse como ventanas prioritarias para futuras pruebas, mientras que los personajes requieren una taxonomía editorial más completa antes de compararlos.

## Cobertura y métrica

| Variable | Cobertura | Limitación |
|---|---:|---|
| Publicaciones relacionadas | 172 | Incluye el lote confirmado por Meta y validación manual |
| Métrica principal | Interacciones lifetime | No es una ventana uniforme de 24/72 horas |
| Formato | 172 imágenes | No hay Reels, carruseles o videos comparables en esta muestra |
| Hora local | 172/172 | Convertida a `America/Matamoros` desde `created_time` de Meta |
| Personajes explícitos | 7 filas concretas; 170 con alguna etiqueta detectada | `Universe` aparece en muchos filenames genéricos y contamina la comparación |

## Rendimiento por formato

| Formato | Posts | Interacciones | Promedio |
|---|---:|---:|---:|
| Imagen estática | 172 | 17,334 | 100.78 |

No es correcto concluir que la imagen es “el mejor formato” a partir de esta tabla: es el único formato observado. El resultado sí confirma que el sistema histórico de junio nació principalmente como un sistema de memes visuales estáticos; la comparación con Reels debe hacerse contra julio/agosto o mediante un experimento controlado.

## Rendimiento por personajes

Los nombres explícitos identificados fueron `Kael`, `Fantasma`, `Aura/Evan` y `Maeve`. Sus resultados deben interpretarse como **casos individuales**, no como promedios robustos de personaje.

| Etiqueta explícita | Posts | Interacciones | Promedio | Lectura |
|---|---:|---:|---:|---|
| Kael | 1 | 1,308 | 1,308 | Caso de alto rendimiento; no permite generalizar |
| Fantasma | 1 | 1,128 | 1,128 | Caso de alto rendimiento; requiere más piezas |
| Aura/Evan | 1 | 1,127 | 1,127 | Caso de alto rendimiento y conversación relevante |
| Maeve | 1 | 529 | 529 | Caso medio; muestra insuficiente |
| Universe / filename genérico | 167 | 12,824 | 76.79 | No es una comparación limpia: la etiqueta aparece por convención de archivo |
| Sin personaje explícito | 2 | 1,546 | 773.00 | Muestra demasiado pequeña |

La señal cualitativa más interesante no es que Kael, Fantasma o Evan “ganen” como personajes, sino que sus piezas de junio aparecen asociadas a composiciones con una situación clara, una reacción reconocible o una tensión social. Para la Biblia conviene registrar el **rol narrativo y la estructura del chiste**, no solo el nombre del personaje.

## Rendimiento por hora local

| Hora | Posts | Interacciones | Promedio |
|---:|---:|---:|---:|
| 11:00 | 10 | 2,459 | 245.90 |
| 21:00 | 13 | 2,795 | 215.00 |
| 19:00 | 18 | 2,833 | 157.39 |
| 13:00 | 11 | 1,542 | 140.18 |
| 10:00 | 14 | 1,780 | 127.14 |
| 23:00 | 10 | 1,137 | 113.70 |
| 18:00 | 11 | 968 | 88.00 |
| 15:00 | 11 | 950 | 86.36 |
| 17:00 | 13 | 807 | 62.08 |
| 16:00 | 14 | 860 | 61.43 |
| 12:00 | 11 | 598 | 54.36 |
| 09:00 | 2 | 71 | 35.50 |

La señal horaria tiene tres lecturas. Primero, **11:00** es la mejor hora individual de la muestra con diez posts, por lo que tiene una base más útil que una hora con uno o dos casos. Segundo, **21:00** y **19:00** combinan buen promedio con una cantidad de publicaciones razonable. Tercero, el bloque de **15:00–18:00** es más débil en junio, aunque esto puede estar mezclado con diferencias de contenido y no prueba que la audiencia rechace esas horas.

La noche no debe interpretarse como “publicar siempre tarde”: 21:00 funciona mejor que 23:00, y 19:00 tiene más volumen. La hipótesis práctica es probar una combinación de **10:00–11:00**, **13:00** y **19:00–21:00**, controlando el tipo de contenido.

## Patrones de éxito identificados

El primer patrón es la combinación de **situación reconocible y remate inmediato**. Las piezas con texto comprensible en un vistazo tienen más posibilidad de provocar reacción y share sin depender de un caption largo.

El segundo patrón es la **etiquetabilidad social**. Los posts que permiten pensar en una persona concreta tienden a tener más potencial de shares y comentarios, aunque esta variable todavía no está codificada de manera formal en los 172 registros.

El tercer patrón es la **tensión emocional o social clara**. Las publicaciones de Aura/Evan, Kael y Fantasma que destacaron en el lote no dependen únicamente del personaje: presentan una escena que permite al usuario reconocerse, etiquetar a alguien o discutir el remate.

El cuarto patrón es horario: **media mañana y noche temprana** aparecen como ventanas prioritarias. La hora debe probarse junto con el tipo de pieza; no se debe mover contenido débil a las mejores horas y atribuir la diferencia únicamente al horario.

## Recomendaciones para el Growth OS

Para la siguiente prueba conviene usar una matriz sencilla: tres ventanas horarias —10:00–11:00, 13:00–14:00 y 19:00–21:00— cruzadas con contenido nuevo, reuse y piezas con alto potencial de etiquetado. La métrica principal debe ser mediana de interacciones por publicación, complementada por shares y comentarios raíz.

También debe normalizarse el inventario de personajes. Cada asset futuro debería registrar personaje principal, personajes secundarios, rol narrativo, tipo de humor y potencial de etiquetado. Sin esa normalización, los resultados de “por personaje” seguirán confundidos por filenames genéricos como `Universe - Existencial`.

## Fuente de datos y archivos

La base detallada está en `2026-08-17_Junio_Analisis_Base.csv`; los agregados están en `2026-08-17_Junio_Rendimiento_Personajes.csv`, `2026-08-17_Junio_Rendimiento_Horarios.csv` y `2026-08-17_Junio_Rendimiento_Formatos.csv`. La gráfica de apoyo está en `/home/ubuntu/june_format_characters_schedule.png` y se entrega junto con este informe.

Este análisis modifica la interpretación de junio, por lo que el documento `2026-08-17_Reporte_Final_Recopilacion_Junio.md` debe considerarse relacionado y mantenerse sincronizado si cambian los registros históricos.
