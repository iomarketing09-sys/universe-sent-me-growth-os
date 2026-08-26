---
title: "Bam in a Can — CAN-003: corte inicial multicanal"
purpose: "Preservar el primer corte de CAN-003, distinguiendo evidencia directa de YouTube Studio, cache temprana autenticada de TikTok e indexación pendiente de Instagram."
status: "Active — evidencia T+3 directa de YouTube y TikTok incorporada; Instagram pendiente de indexación"
created: 2026-08-25
updated: 2026-08-26
version: "1.1"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Production/2026-08-20_Plan_Lanzamiento_Audiencia_Bam_In_A_Can.md"
  - "Operations/Production/2026-08-21_Bam_In_A_Can_Semana01_Calendario_Publicacion.md"
  - "Operations/Production/2026-08-21_Bam_In_A_Can_Semana01_Paquete_Lanzamiento.md"
  - "Operations/Research/Bam_In_A_Can_Distribution_Ledger.csv"
  - "Operations/Research/2026-08-23_Bam_CAN002_Chequeo_Inicial.md"
organization: "Operations/Research"
---

# Bam in a Can — CAN-003: corte inicial multicanal

## Propósito del corte

CAN-003, *Do Not Insert Coins After Midnight*, cerró su cascada el 25 de agosto. El corte se solicitó después de la ventana T+3 de YouTube Shorts. La evidencia no tiene la misma frescura en las tres plataformas y por ello no se usa para elaborar un ranking cross-platform ni para validar causalidad de audio, horario o formato.

| Plataforma | T0 y edad disponible | Fuente | Estado del dato |
|---|---|---|---|
| TikTok | T0 recuperado del ID: 25 Ago, 20:15:39 CDT. La fila disponible es T+7 min 13 s. | Windsor.ai `tiktok_organic` | Cache temprana; no representa T+3. |
| Instagram Reels | T0 no recuperable desde la vista pública actual. | Windsor.ai por shortcode sin rango de fechas | Sin fila; el inventario sin filtro solo devolvió CAN-002. Indexación pendiente, no cero. |
| YouTube Shorts | T0 público: 25 Ago, 20:54:05 CDT. Evidencia recibida a las 23:15:46 CDT, T+2 h 21 min 41 s. | Capturas directas de YouTube Studio | Evidencia directa preferente para este corte. |

## Métricas disponibles

| Plataforma | Métricas | Lectura limitada |
|---|---|---|
| TikTok | 2 views; 0 likes; 0 comentarios; 0 shares; 0 favoritos; avg. watch 2.99 s; full-watch rate 7.14 %. | La fila fue recuperada a T+7 min 13 s y permanecía cacheada al solicitar el corte. El valor bruto de total watch `251` no es consistente con views × avg. watch; se conserva como raw del conector, pero no se interpreta ni se convierte a segundos. |
| Instagram Reels | Sin fila autenticada de CAN-003 en la consulta individual ni en el inventario mínimo. | No se registra como 0 views, 0 reach o 0 engagement. Requiere una reconsulta posterior por shortcode `DcfDsCIMrpx`, sin fechas y en bloques reducidos. |
| YouTube Shorts | 578 views; 6 likes; 1 share; visualización media de 10 s; hito de primer Short del canal en alcanzar 500 views. | Studio indica que 10 s está por encima de lo habitual. Dado que CAN-003 dura 10 s, esta lectura es consistente con consumo de la duración completa o replay, pero no sustituye una tasa numérica de finalización. |

## Lectura de hipótesis

La señal de YouTube es claramente más fuerte que el arranque previo de CAN-002 en la misma fuente, pero no se atribuye aún a una variable única. CAN-003 combina una anomalía visible desde el inicio, cortes editoriales, SFX de control y un contenido distinto; no es una prueba aislada del hook, los SFX o el horario.

`H-BAM-TT-HOOK-01` no puede evaluarse todavía: TikTok solo aportó una fila T+7 min. `H-BAM-IG-PACKAGING-01` permanece sin evaluación: Instagram aún no indexa la pieza en Windsor. La próxima evidencia útil es el corte T+24 por plataforma, con una reconsulta de Instagram por shortcode y una nueva captura de Studio para YouTube.

## Actualización T+3 — YouTube Studio y TikTok Studio

Fernando aportó capturas directas de YouTube Studio y TikTok Studio dentro de la ventana reportada de tres horas. YouTube Studio muestra **853 views**, **11 likes** y **1 share**. Frente a la captura directa previa de 578 views y 6 likes, esto añade 275 views y 5 likes; el share permanece en 1. La evidencia anterior de YouTube también indicaba visualización media de 10 s sobre 10 s de duración, por encima de lo habitual según Studio.

TikTok Studio reporta 101 views, 0 likes, 0 comentarios, 0 shares, 0 guardados, 0 nuevos seguidores, 4 min 38 s de watch time total, avg. watch de **2.6 s**, duración de **10.05 s** y full-watch rate de **5.61 %**. El average watch equivale a **25.0 %** de la duración. El tráfico llega principalmente desde Para ti (97.2 %), con 1.9 % desde Otras y 0.9 % desde Perfil personal. La gráfica y el mensaje de la interfaz indican una caída pronunciada posterior al inicio; el reporte no permite asignar esa caída a un audio, hora o elemento creativo particular.

Instagram continuaba mostrando dos views según el reporte manual de Fernando. Como Windsor todavía no devuelve fila para `DcfDsCIMrpx`, este valor se conserva como evidencia manual de estado y no como métrica autenticada comparable.

Estas señales permiten formular hipótesis preliminares de hook y replay, documentadas en el Plan de lanzamiento de audiencia. No validan una hipótesis: CAN-003 es un solo activo, cada plataforma tiene distribución y medición distinta, y la respuesta de Instagram todavía no está disponible.

## Evidencia archivada

![Métrica directa de CAN-003 en YouTube Studio a T+2 h 21 min 41 s](2026-08-25_Bam_CAN003_YouTube_Studio_T2h21m41s.jpg)

![Aviso de visualización media de CAN-003 en YouTube Studio](2026-08-25_Bam_CAN003_YouTube_Studio_AvgWatch10s_T2h21m51s.jpg)

![Métrica de CAN-003 a la ventana reportada de tres horas en YouTube Studio](2026-08-26_Bam_CAN003_YouTube_Studio_T3h_853views.jpg)

![Métricas tempranas y fuentes de tráfico de CAN-003 en TikTok Studio](2026-08-26_Bam_CAN003_TikTok_Studio_early_window.jpg)

## Documentos relacionados que requieren actualización posterior

El ledger de distribución y el Plan de lanzamiento de audiencia se actualizan en este mismo cambio. En el corte T+24 se actualizarán este snapshot y el ledger; el Plan se ajustará solo si CAN-003 y la siguiente pieza comparable ofrecen evidencia repetida suficiente para aceptar, revisar o descartar las hipótesis activas. El calendario y paquete de lanzamiento no requieren cambios adicionales, salvo que Fernando confirme los T0, volumen o etiqueta IA pendientes de TikTok e Instagram.
