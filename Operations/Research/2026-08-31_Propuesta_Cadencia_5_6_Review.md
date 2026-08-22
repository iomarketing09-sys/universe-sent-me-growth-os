---
title: "Propuesta de cadencia 5–6 piezas — bloque de revisión humana 31 agosto–2 septiembre"
purpose: "Aplicar de forma gradual el playbook de cadencia diaria aprobado, con cinco publicaciones por día, mezcla controlada de contenido nuevo y reuse, y sin ejecutar programación o publicación antes del gate humano."
status: Review
created: 2026-08-22
updated: 2026-08-22
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "2026-08-14_Diseno_Prueba_Calendario_2_Semanas.md"
  - "2026-08-16_Calendario_Operativo_17_30_Agosto.md"
  - "2026-08-16_Clasificacion_Visual_35_Memes_Nuevos.csv"
  - "2026-08-18_Cola_Reuse_Junio_Aprobada.csv"
  - "../../GrowthOS/01_03_Reuse_Queue.md"
  - "../../GrowthOS/01_04_Production_Queue.md"
  - "../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
organization: "Operations/Research"
---

# Propuesta de cadencia 5–6 piezas — bloque de revisión humana

## 1. Dictamen operativo

La aprobación de Fernando permite preparar la siguiente ola con una banda de **5–6 publicaciones reales por día**, una mezcla de **65%–70% contenido nuevo y 30%–35% reuse**, y denominadores separados para imágenes, Reels, Instagram y afiliados. La propuesta de este documento es un **bloque piloto de tres días —31 de agosto al 2 de septiembre— con cinco slots diarios**, equivalente a 15 filas de revisión.

No se modifica el calendario activo 17–30 de agosto. Ese calendario ya contiene 74 slots para 14 días —5.28 slots asignados por día— y se mantiene como está. Este bloque posterior es una propuesta nueva para probar la ejecución de la mezcla correcta, no una ampliación retrospectiva.

## 2. Composición del bloque

| Tipo | Filas | Proporción | Estado de preparación |
|---|---:|---:|---|
| Nueva | 10 | 66.7% | Cinco assets nuevos de Drive pendientes de revisión y cinco propuestas CNT-028 pendientes de aprobación/asset local |
| Reuse | 5 | 33.3% | Candidatos de la cola de reuse de junio; todos superan 30 días, pero requieren filename exacto y revisión de copy |
| Total | 15 | 100% | Review; ninguna fila está autorizada para programar |

El bloque utiliza cinco slots diarios: **10:00, 11:00, 13:30, 17:00 y 19:00**, en `America/Matamoros`. Esta versión no abre todavía el sexto slot; primero comprueba si la cartera mínima de cinco puede ejecutarse con una mezcla saludable y sin huecos de preflight.

## 3. Distribución propuesta

| Fecha | Slots | Nuevas | Reuse | Mezcla | Propósito del día |
|---|---:|---:|---:|---:|---|
| 31 agosto | 5 | 3 | 2 | 60% / 40% | Abrir con relatable, difusión y dos anclas históricas |
| 1 septiembre | 5 | 3 | 2 | 60% / 40% | Probar dúos, absurdismo y una pieza de Ganso con reuse controlado |
| 2 septiembre | 5 | 4 | 1 | 80% / 20% | Aumentar novedad cuando la producción tenga mayor carga aprobada |

El agregado del bloque queda en 10 nuevas y 5 reuse, **66.7%/33.3%**, dentro del objetivo global. La mezcla diaria puede variar; lo importante es que el bloque completo no dependa de reuse improvisado.

## 4. Estado real de los candidatos

La clasificación no convierte automáticamente un asset en publicable. Los cinco assets nuevos restantes del inventario —`2608030`, `2608033`, `2608036`, `2608037` y `2608060`— permanecen como `Nuevo_Pendiente_Revision`. Las cinco propuestas CNT-028 tienen estado `Draft` y sus archivos no están disponibles en el checkout local; por tanto, no pueden programarse hasta que se confirme el asset exacto, la revisión visual y la aprobación humana.

La cola compacta de reuse aporta seis candidatos. Este bloque usa cinco: `CNT-080`, `CNT-081`, `CNT-082`, `CNT-083` y `CNT-084`. Todos superan la antigüedad mínima de 30 días, pero conservan bloqueos de revisión sobre filename, copy, contexto, atribución de personaje o salud mental. `CNT-085` queda como reserva administrativa, no como publicación automática.

## 5. Gates de revisión humana

Antes de convertir cualquier fila a `Aprobada`, Fernando debe revisar el asset exacto, la legibilidad, el tono, el tratamiento de caption y la compatibilidad de plataforma. Las filas de CNT-028 requieren además que el archivo exista en Drive o en almacenamiento operativo verificable; el CSV no inventa un `Drive_ID` cuando no está disponible.

El resultado actual es una cola de revisión, no un calendario aprobado:

| Estado | Significado |
|---|---|
| `Blocked_Visual_Review_Required` | Asset existe, pero falta revisión visual/copy final |
| `Blocked_Exact_Filename_and_Copy_Review` | Reuse supera 30 días, pero falta filename exacto y validación de copy |
| `Blocked_Asset_Not_Local_and_Human_Approval` | La propuesta existe documentalmente, pero el archivo no está disponible para preflight |
| `Human_Approval=PENDING` | No programar ni publicar |

Si una fila no supera el gate, se reemplaza solo por una reserva aprobada o se registra `Slot_No_Publicado`. No se agrega contenido de afiliado, Reel o Instagram al bloque de imágenes.

## 6. Medición

El corte diario debe registrar publicaciones reales, slots vacíos, desviaciones horarias, mediana de interacciones, shares, comentarios y concentración top 1/top 5. El reporte diario permanece como fuente principal de aprendizaje. Las conclusiones de familia, personaje y horario se mantienen direccionales hasta contar con al menos tres casos comparables.

`Affiliate_Status` queda en `Excluded` para las 15 filas. Reels se mantiene fuera del CSV de imágenes y continúa bajo el protocolo L0–L4. Instagram no se publica por inferencia: cualquier crosspost requerirá una orden y un registro de plataforma separado.

## 7. Siguiente gate

La propuesta queda lista para revisión humana en [`2026-08-31_Propuesta_Cadencia_5_6_Review.csv`](2026-08-31_Propuesta_Cadencia_5_6_Review.csv). La aprobación debe indicar qué filas pasan a `Aprobada`, cuáles requieren corrección y cuál se conserva como reserva. Solo después se puede producir el CSV final de programación; esta propuesta no autoriza programación, publicación ni movimiento de originales en Drive.

## Referencias

[1]: 2026-08-14_Diseno_Prueba_Calendario_2_Semanas.md "Playbook operativo de cadencia diaria"
[2]: 2026-08-16_Calendario_Operativo_17_30_Agosto.md "Calendario activo 17–30 de agosto"
[3]: 2026-08-16_Clasificacion_Visual_35_Memes_Nuevos.csv "Clasificación visual de memes nuevos"
[4]: 2026-08-18_Cola_Reuse_Junio_Aprobada.csv "Cola compacta de reuse aprobado"
[5]: ../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md "Fuente maestra y ledgers del Growth OS"
