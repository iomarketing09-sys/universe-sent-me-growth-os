---
title: "Análisis de rendimiento de 28 días — Instagram y Facebook"
purpose: "Analizar el rendimiento verificable de Instagram y Facebook entre el 22 de julio y el 18 de agosto de 2026, manteniendo separadas las plataformas, los formatos y las ventanas temporales."
status: "Active"
created: 2026-08-18
updated: 2026-08-19
version: "1.1"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-14_Comparativo_Desempeno_Junio_Julio_Agosto_Datos.csv"
  - "Operations/Research/2026-08-15_Publication_Log.csv"
  - "Operations/Research/2026-08-17_Protocolo_P0_Metricas_y_Veredictos.md"
  - "Operations/Research/2026-08-19_Auditoria_Reels_y_Monetizacion.md"
  - "Operations/Research/2026-08-19_Meta_Reels_Audit.json"
  - "Operations/Research/2026-08-17_Instagram_Republicacion_2608036_2608060.json"
  - "Operations/Research/2026-08-19_Windsor_Instagram_28D_Normalizado.json"
  - "Operations/Research/2026-08-19_Windsor_Facebook_Organic_28D_Normalizado.json"
organization: "Operations/Research"
---

# Análisis de rendimiento de 28 días — Instagram y Facebook

## Resumen ejecutivo

El corte analizado comprende del **22 de julio al 18 de agosto de 2026**, inclusive. Facebook dispone de una muestra cuantificable y amplia: 119 publicaciones, 30,729 interacciones acumuladas y una mediana de 37 interacciones por publicación. El rendimiento fue claramente más fuerte en la parte de julio incluida en el período que en agosto: la mediana bajó de 43 a 29 interacciones y la media descendió de 335.2 a 192.1.

Instagram ya fue consultado mediante **Windsor.ai** y verificado con el conector de Instagram. Windsor devolvió **34 piezas de media** dentro del corte con métricas de engagement, alcance, views, guardados, shares y watch time para Reels. Tres comprobaciones cruzadas —dos Reels y una imagen— devolvieron exactamente los mismos valores en Windsor y en el conector de Instagram. La Graph API directa sigue siendo la ruta canónica para IDs y publicación, pero el token actual no tiene `instagram_manage_insights`, por lo que no es la fuente efectiva de Insights en este corte.

> **Veredicto:** Facebook muestra una base de distribución fuerte pero concentrada en pocos posts; Reels presentan una señal de interacción mucho menor que el conjunto general de publicaciones. Instagram ya tiene una medición útil de 34 piezas mediante Windsor, con Reels como formato dominante, y cuenta con validación puntual del conector de Instagram. Graph API directa queda reservada para identidad, publicación y reconciliación hasta autorizar `instagram_manage_insights`.

## Definición del corte y comparabilidad

| Elemento | Definición |
|---|---|
| Período | 22 de julio–18 de agosto de 2026, inclusive |
| Facebook general | Publicaciones del dataset histórico de la página, con reacciones, comentarios, shares e interacciones actuales |
| Facebook Reels | 12 Reels de la auditoría Meta dentro del período, con interacciones actuales acumuladas |
| Instagram | Windsor devuelve 34 piezas con Insights; el conector confirma valores puntuales; Graph API directa mantiene la identidad y publicación |
| Métrica principal | Mediana de interacciones por publicación |
| Precaución | Los valores de Facebook general y Facebook Reels son acumulados actuales; no deben interpretarse como ventanas exactas 24/72 horas |

La métrica de interacción utilizada es `reacciones + comentarios + shares`. El protocolo del Growth OS prioriza la mediana porque evita que unos pocos virales dominen el diagnóstico. Los valores de alcance, views, guardados, shares y watch time están disponibles para Instagram mediante Windsor. Las métricas de Facebook general proceden del histórico/Meta y no son idénticas en definición a `post_engagements` de Windsor, por lo que el Growth OS conservará su métrica canónica por plataforma.

## Facebook: rendimiento general

| Métrica | 22 jul–18 ago |
|---|---:|
| Publicaciones | 119 |
| Interacciones acumuladas | 30,729 |
| Media de interacciones por publicación | 258.2 |
| Mediana de interacciones por publicación | 37.0 |
| Percentil 90 | 452.0 |
| Reacciones | 21,990 |
| Comentarios | 468 |
| Shares | 8,271 |

La distribución es muy desigual. La media de 258.2 supera ampliamente la mediana de 37, lo que indica que un grupo pequeño de publicaciones elevó el total. Los shares representan aproximadamente el 26.9% de las interacciones registradas, una señal de difusión relevante; sin embargo, este porcentaje debe tratarse como composición de interacciones y no como tasa, porque no se dispone de alcance por publicación.

### Evolución dentro del corte

| Subperíodo | Publicaciones | Interacciones | Media | Mediana | Shares |
|---|---:|---:|---:|---:|---:|
| 22–31 julio | 55 | 18,436 | 335.2 | 43.0 | 4,754 |
| 1–18 agosto | 64 | 12,293 | 192.1 | 29.0 | 3,517 |

La mediana de agosto fue aproximadamente **32.6% menor** que la de la parte de julio incluida en el corte. La media fue aproximadamente **42.7% menor**. Esto apunta a una pérdida de rendimiento típico y no solamente a la ausencia de un viral, aunque la atribución causal requiere separar formato, personaje, horario, copy y estado nuevo/reuse.

### Mejores publicaciones de Facebook por interacciones

| Fecha | Interacciones | Reacciones | Comentarios | Shares | Señal visible |
|---|---:|---:|---:|---:|---|
| 4 ago | 4,103 | 2,858 | 30 | 1,215 | Copy mínimo / reacción rápida |
| 28 jul | 3,726 | 2,367 | 18 | 1,341 | Fantasma + humor relatable |
| 24 jul | 3,002 | 2,336 | 41 | 625 | Humor relatable + astrología |
| 27 jul | 2,979 | 2,249 | 16 | 714 | Humor ácido |
| 22 jul | 2,747 | 1,722 | 10 | 1,015 | Humor relatable + vida real |

Los cinco mejores posts suman 16,557 interacciones, aproximadamente el 53.9% del total del período. La estrategia que parece más replicable combina **copy muy corto o reconocible, humor relatable, Fantasma o una situación cotidiana y potencial de compartir**. Esto es una hipótesis de trabajo, no una regla canonizada, porque el dataset no contiene una taxonomía completa de formato y personaje para cada fila.

## Facebook Reels

| Métrica | 22 jul–18 ago |
|---|---:|
| Reels | 12 |
| Interacciones acumuladas | 211 |
| Media de interacciones por Reel | 17.6 |
| Mediana de interacciones por Reel | 19.5 |
| Reacciones | 171 |
| Comentarios | 24 |
| Shares | 16 |

Los Reels representan un carril de interacción considerablemente más débil que el conjunto general de publicaciones de Facebook en este corte. La mediana de 19.5 frente a 37.0 para todas las publicaciones no constituye una comparación causal perfecta, porque los Reels tienen otra distribución, objetivos y ventanas de medición. Sí justifica tratarlos como un experimento separado.

Los mejores Reels por interacciones fueron `Un rock bien gótico vs. una canción de Juan Gabriel` con 28, el Reel de Wilfred con 26 y `Mi gato sabe hacer de todo` con 25. En agosto, la mediana de Reels fue 17.0, frente a 25.5 en los cuatro Reels de julio incluidos en el período. La muestra es pequeña y no contiene vistas ni retención, por lo que no permite saber si el problema está en distribución inicial, hook, duración o conversión a interacción.

## Instagram: rendimiento obtenido mediante Windsor

| Métrica | Total 34 piezas | Mediana por pieza |
|---|---:|---:|
| Engagement | 59 | 1.0 |
| Reach | 1,216 | — |
| Views | 1,646 | — |
| Likes | 44 | — |
| Guardados | 5 | — |
| Shares | 6 | — |

| Formato | Piezas | Engagement | Mediana | Reach | Views |
|---|---:|---:|---:|---:|---:|
| Reels | 14 | 47 | 2.0 | 1,137 | 1,447 |
| Imágenes | 17 | 12 | 0.0 | 70 | 168 |
| Carruseles | 3 | 0 | 0.0 | 9 | 31 |

Los Reels son el formato claramente dominante en Instagram durante el corte: concentran aproximadamente el **79.7% del engagement**, el **93.5% del reach** y el **87.9% de las views** de las 34 piezas. El mejor Reel fue `Cultiva la paz interior`, con 19 interacciones, 247 de reach y 354 views. Le siguieron `Dicen que si lo ves caminando, no lo sigas`, con 7 interacciones, y `Mi gato sabe hacer de todo`, con 5.

La evolución también muestra una caída de julio a agosto: la media de engagement pasó de 4.86 a 0.93 por pieza y el total de reach de 680 a 536, aunque agosto tiene una composición de formatos distinta y muchos posts con distribución muy baja. La señal es suficiente para investigar, pero no para atribuir causalidad sin estratificar por formato, personaje, copy y horario.

## Verificación entre fuentes

| Fuente | Resultado de la prueba | Uso recomendado |
|---|---|---|
| Windsor.ai | 34 piezas y métricas completas por media; consulta masiva rápida | Fuente analítica principal para Instagram |
| Conector Instagram | Cuenta, publicaciones y insights por post; coincidió con Windsor en tres muestras | Fuente secundaria de validación y lectura puntual |
| Graph API directa | IDs, media e identidad correctos; Insights bloqueados por permiso `instagram_manage_insights` | Fuente canónica para identidad, publicación y reconciliación |

La conclusión correcta es **Instagram medido con Windsor y verificado puntualmente por el conector**, no rendimiento cero ni ausencia de datos. Facebook conserva su métrica canónica histórica `reacciones + comentarios + shares`; no se deben sumar directamente los agregados `post_engagements` de Windsor porque su definición puede incluir acciones adicionales y su fecha diaria puede usar otra normalización temporal.


## Diagnóstico y acciones prioritarias

1. **Mantener Facebook general y Facebook Reels como carriles separados.** El conjunto general tiene una mediana de 37 interacciones; los Reels, 19.5. No se debe usar el rendimiento de imágenes para declarar que los Reels han fallado creativamente.

2. **Priorizar la captura de distribución y retención para cada Reel.** El ledger debe incluir vistas, alcance, retención a 3 segundos, tiempo promedio visto, completaciones, shares, comentarios y seguidores ganados, además de hook, duración, personaje, formato, CTA y estado nuevo/reuse.

3. **Conectar Instagram y extraer sus insights antes de comparar plataformas.** Las publicaciones activas de Instagram tienen que recibir una fila de métricas con fecha de extracción y ventana, aunque los valores iniciales sean cortes observados y no 24/72 horas exactas.

4. **Investigar la caída de agosto en Facebook.** La siguiente comparación debe estratificar por formato, personaje, horario, copy mínimo, humor relatable, Fantasma y contenido nuevo/reuse. La concentración del 53.9% de las interacciones en cinco posts hace necesario usar medianas y no promedios como criterio principal.

5. **No mezclar este corte con TikTok o YouTube.** Esos canales todavía no tienen datos documentados dentro del Growth OS.

## Fuentes internas

[1]: `Operations/Research/2026-08-14_Comparativo_Desempeno_Junio_Julio_Agosto_Datos.csv` — export histórico de publicaciones de Facebook.
[2]: `Operations/Research/2026-08-19_Meta_Reels_Audit.json` — auditoría de Reels de Facebook.
[3]: `Operations/Research/2026-08-15_Publication_Log.csv` — registro de publicaciones y estados de Instagram/Facebook.
[4]: `Operations/Research/2026-08-17_Protocolo_P0_Metricas_y_Veredictos.md` — reglas de comparabilidad y uso de medianas.
[5]: `Operations/Research/2026-08-17_Instagram_Republicacion_2608036_2608060.json` — evidencia de dos republicaciones reales de Instagram.
