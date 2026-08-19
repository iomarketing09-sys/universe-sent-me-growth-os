---
title: "Comparación de snapshots multicanal — corte 28D"
purpose: "Distinguir variaciones observadas entre la extracción inicial y el corte renovado del mismo rango de publicación, sin atribuir erróneamente snapshots lifetime a crecimiento por período."
status: Active
created: 2026-08-19
updated: 2026-08-19
version: "1.0"
author: "Manus AI"
related_documents:
  - "2026-08-19_Comparacion_Snapshots_28D.json"
  - "2026-08-19_Corte_Multicanal_28D_1600.md"
  - "2026-08-19_Social_Performance_28D_Normalizado.json"
  - "../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
---

# Comparación de snapshots multicanal — corte 28D

## Conclusión ejecutiva

El rango de publicación no cambió: ambos snapshots cubren **22 de julio–18 de agosto de 2026**. Por ello, esta comparación no es un período anterior contra uno posterior; mide la actualización de métricas sobre las mismas piezas. La única señal clara de incremento es **YouTube**, con **+26 views lifetime** en seis Shorts. Instagram muestra una variación marginal de **+4 views** y **+2 de reach**; TikTok no cambió. Facebook no permite inferir tendencia: Windsor devolvió la misma marca de extracción en caché.

| Plataforma | Cambio observado | Interpretación correcta |
|---|---:|---|
| Instagram | +4 views; +2 reach; -3 acciones agregadas | Movimiento marginal de snapshot; no prueba caída de rendimiento. |
| TikTok | 0 views; 0 engagement | Sin nueva variación observable en las siete piezas. |
| YouTube | +26 views lifetime; 0 comentarios | Crecimiento real posterior de catálogo, pero pequeño y no atribuible a una pieza sin un delta por video. |
| Facebook | No comparable | El lote analítico estaba en caché; se requiere una extracción con `data_fetched_at` nuevo para medir tendencia. |

## Lectura operativa

> **No existe evidencia suficiente de una tendencia de crecimiento multicanal acelerada entre estos dos snapshots.** El lapso entre lecturas es demasiado corto y varias fuentes son acumulados lifetime.

El crecimiento orgánico verificable debe medirse en cortes consecutivos con fechas de extracción distintas y cohortes de publicaciones equivalentes. La acción más útil es programar el siguiente corte cuando existan nuevas publicaciones maduras y comparar la actividad diaria de YouTube, los deltas por `media_id` de Instagram y los deltas por `video_id` de TikTok. Para Facebook, se debe forzar una lectura que no use el resultado cacheado antes de emitir una conclusión de tendencia.

## Señales por publicación

El incremento de YouTube está distribuido, no concentrado en un solo Short: `Escribiendo…` sumó **7** views; `Me hace falta vitamina B` **6**; `Fantasma` **5**; `El verdadero caos…` y `Habilidades que no vienen…` **3** cada uno; y `En los ojos correctos…` **2**. Esto respalda una señal de descubrimiento ligero de catálogo, no un breakout demostrable. Instagram solo sumó cuatro views distribuidas entre piezas, por lo que no hay evidencia para cambiar el mix de formatos aún.
