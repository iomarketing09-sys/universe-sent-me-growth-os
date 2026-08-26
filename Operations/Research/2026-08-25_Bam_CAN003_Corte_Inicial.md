---
title: "Bam in a Can — CAN-003: corte inicial multicanal"
purpose: "Preservar el primer corte de CAN-003, distinguiendo evidencia directa de YouTube Studio, cache temprana autenticada de TikTok e indexación pendiente de Instagram."
status: "Active — evidencia de YouTube directa; TikTok con cache pre-T+3 e Instagram pendiente de indexación"
created: 2026-08-25
updated: 2026-08-25
version: "1.0"
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

## Evidencia archivada

![Métrica directa de CAN-003 en YouTube Studio a T+2 h 21 min 41 s](2026-08-25_Bam_CAN003_YouTube_Studio_T2h21m41s.jpg)

![Aviso de visualización media de CAN-003 en YouTube Studio](2026-08-25_Bam_CAN003_YouTube_Studio_AvgWatch10s_T2h21m51s.jpg)

## Documentos relacionados que requieren actualización posterior

El ledger de distribución se actualiza en este mismo cambio. En el corte T+24 se actualizarán este snapshot y el ledger; el Plan de lanzamiento de audiencia solo se ajustará si CAN-003 y CAN-004 ofrecen evidencia repetida suficiente para aceptar, revisar o descartar las hipótesis activas. El calendario y paquete de lanzamiento no requieren cambios adicionales, salvo que Fernando confirme los T0, volumen o etiqueta IA pendientes de TikTok e Instagram.
