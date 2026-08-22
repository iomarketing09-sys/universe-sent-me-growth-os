---
title: "Propuesta de cadencia 5–6 piezas — bloque de revisión humana 31 agosto–2 septiembre"
purpose: "Aplicar de forma gradual el playbook de cadencia diaria, con cinco publicaciones por día, mezcla controlada de contenido nuevo y reuse, y sin ejecutar programación o publicación antes del gate humano."
status: Review
created: 2026-08-22
updated: 2026-08-22
version: "1.1"
author: "Manus AI (CGO)"
related_documents:
  - "2026-08-14_Diseno_Prueba_Calendario_2_Semanas.md"
  - "2026-08-16_Calendario_Operativo_17_30_Agosto.md"
  - "2026-08-22_Drive_Memes_Visual_Review_Notes.md"
  - "2026-08-22_Drive_Memes_Seed_Inventory.csv"
  - "2026-08-18_Cola_Reuse_Junio_Aprobada.csv"
  - "../../GrowthOS/01_03_Reuse_Queue.md"
  - "../../GrowthOS/01_04_Production_Queue.md"
  - "../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
organization: "Operations/Research"
---

# Propuesta de cadencia 5–6 piezas — bloque de revisión humana

## 1. Corrección de fuente

La selección anterior de los assets `2608030`, `2608033`, `2608036`, `2608037` y `2608060` queda anulada como contenido nuevo: Fernando confirmó que ya fueron publicados. La carpeta `Humor existencial` no tiene memes nuevos disponibles para este bloque.

La fuente correcta es el target de Drive `1BpKZpUBIT5jBjkvw7epymlsD3Gp4lwzE`, visible como la carpeta `Memes` dentro de `Universe sent me > Ideas`. La consulta de solo lectura encontró 14 semillas visuales. Estas semillas no son assets USM listos para publicar; son referencias que deben transformarse en propuestas originales con personajes y estilo oficial de Universe Sent Me.

## 2. Dictamen operativo

La aprobación de Fernando permite preparar la siguiente ola con una banda de **5–6 publicaciones reales por día**, una mezcla de **65%–70% contenido nuevo y 30%–35% reuse**, y denominadores separados para imágenes, Reels, Instagram y afiliados. La propuesta de este documento es un **bloque piloto de tres días —31 de agosto al 2 de septiembre— con cinco slots diarios**, equivalente a 15 filas de revisión.

No se modifica el calendario activo 17–30 de agosto. Ese calendario ya contiene 74 slots para 14 días —5.28 slots asignados por día— y se mantiene como está. Este bloque posterior es una propuesta nueva para probar la ejecución de la mezcla correcta, no una ampliación retrospectiva.

## 3. Composición del bloque

| Tipo | Filas | Proporción | Fuente | Estado de preparación |
|---|---:|---:|---|---|
| Nueva | 10 | 66.7% | Semillas reales de Drive/Memes | Requieren adaptación original USM, producción y aprobación |
| Reuse | 5 | 33.3% | Cola compacta de reuse de junio | Superan 30 días; requieren filename exacto y revisión de copy |
| Total | 15 | 100% | Facebook propuesto | Todas permanecen en `Review` y `Human_Approval=PENDING` |

El bloque utiliza cinco slots diarios: **10:00, 11:00, 13:30, 17:00 y 19:00**, en `America/Matamoros`. Esta versión no abre todavía el sexto slot; primero comprueba si la cartera mínima de cinco puede ejecutarse con una mezcla saludable y sin huecos de preflight.

## 4. Distribución propuesta

| Fecha | Slots | Nuevas | Reuse | Mezcla diaria | Propósito |
|---|---:|---:|---:|---:|---|
| 31 agosto | 5 | 3 | 2 | 60% / 40% | Probar dos mecánicas recientes y dos anclas históricas |
| 1 septiembre | 5 | 3 | 2 | 60% / 40% | Combinar aura, llegada y humor de identidad con reuse controlado |
| 2 septiembre | 5 | 4 | 1 | 80% / 20% | Aumentar novedad y evaluar semillas de mayor riesgo por separado |

El agregado del bloque queda en 10 nuevas y 5 reuse, **66.7%/33.3%**, dentro del objetivo global. La mezcla diaria puede variar; lo importante es que el bloque completo no dependa de reuse improvisado.

## 5. Qué significa “nueva” en este CSV

Las 10 filas nuevas son conceptos derivados de semillas de Drive, no publicaciones autorizadas. El CSV utiliza las siguientes fuentes: `DRIVE-MEME-001`, `DRIVE-MEME-002`, `DRIVE-MEME-003` y `DRIVE-MEME-006` como referencias recientes claras; `DRIVE-MEME-004` y `DRIVE-MEME-005` como inspiración externa que no debe copiarse; `DRIVE-MEME-007` y `DRIVE-MEME-014` como semillas antiguas que requieren una decisión editorial; y `DRIVE-MEME-008` y `DRIVE-MEME-009` como plantillas de cupón que permanecen en revisión de riesgo.

Ninguna de estas filas puede pasar directamente a programación. Para convertirse en asset publicable se requiere definir la mecánica, recrear la escena con personajes y referencias oficiales USM, guardar el archivo final en la carpeta operativa correcta de Drive, confirmar nombre e ID exactos, revisar identidad visual, cerrar caption y obtener aprobación humana. La publicación directa de las capturas está bloqueada.

La semilla de Maldita Summer (`DRIVE-MEME-004`) se mantiene como inspiración únicamente porque presenta autoría identificable. La semilla de anime (`DRIVE-MEME-005`) tampoco debe copiarse. Las plantillas de cupones se mantienen fuera de afiliados y no se convierten en CTA comerciales por defecto.

## 6. Reuse histórico

El bloque usa `CNT-080`, `CNT-081`, `CNT-082`, `CNT-083` y `CNT-084` de la cola compacta de junio. Todos superan la regla de antigüedad de 30 días, pero siguen bloqueados hasta confirmar filename exacto, copy, contexto y plataforma. `CNT-085` queda como reserva administrativa, no como publicación automática.

Una fila de reuse puede pasar a `Aprobada` solo cuando el original de Drive y la relación histórica estén verificados. El nuevo uso debe registrar su propia fecha, Meta ID y métricas; no sobrescribe el hecho de publicación histórico.

## 7. Gates de revisión humana

Antes de convertir cualquier fila a `Aprobada`, Fernando debe revisar el concepto, asset exacto, legibilidad, tono, treatment de caption y compatibilidad de plataforma. Las semillas externas requieren además una decisión de adaptación original y no pueden entrar como imágenes directas.

| Estado | Significado |
|---|---|
| `Blocked_Seed_Not_USM_Asset` | La semilla existe, pero falta recreación con assets oficiales USM |
| `Blocked_Inspiration_Only` | La referencia tiene autoría o medio externo; solo puede inspirar una pieza original |
| `Blocked_High_Risk_Seed_Review` | La semilla de cupón o contenido sensible necesita decisión editorial separada |
| `Blocked_Exact_Filename_and_Copy_Review` | El reuse supera 30 días, pero falta confirmar archivo y copy |
| `Human_Approval=PENDING` | No programar ni publicar |

Si una fila no supera el gate, se conserva como `Blocked`, se reemplaza por una reserva aprobada o se registra `Slot_No_Publicado`. No se agrega contenido de afiliado, Reel o Instagram al bloque de imágenes.

## 8. Medición

El corte diario debe registrar publicaciones reales, slots vacíos, desviaciones horarias, mediana de interacciones, shares, comentarios y concentración top 1/top 5. El reporte diario permanece como fuente principal de aprendizaje. Las conclusiones de familia, personaje y horario se mantienen direccionales hasta contar con al menos tres casos comparables.

`Affiliate_Status` queda en `Excluded` para las 15 filas. Reels se mantiene fuera del CSV de imágenes y continúa bajo el protocolo L0–L4. Instagram no se publica por inferencia: cualquier crosspost requerirá una orden y un registro de plataforma separado.

## 9. Siguiente gate

La propuesta queda lista para revisión humana en [`2026-08-31_Propuesta_Cadencia_5_6_Review.csv`](2026-08-31_Propuesta_Cadencia_5_6_Review.csv). La revisión debe decidir qué semillas pasan a brief de producción, qué reuse queda aprobado y cuál se conserva como reserva. Solo después se prepara el CSV final de programación; esta propuesta no autoriza programación, publicación ni movimiento de originales en Drive.

## Referencias

[1]: 2026-08-14_Diseno_Prueba_Calendario_2_Semanas.md "Playbook operativo de cadencia diaria"
[2]: 2026-08-16_Calendario_Operativo_17_30_Agosto.md "Calendario activo 17–30 de agosto"
[3]: 2026-08-22_Drive_Memes_Visual_Review_Notes.md "Revisión visual de semillas Drive/Memes"
[4]: 2026-08-22_Drive_Memes_Seed_Inventory.csv "Inventario de semillas Drive/Memes"
[5]: 2026-08-18_Cola_Reuse_Junio_Aprobada.csv "Cola compacta de reuse aprobado"
[6]: ../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md "Fuente maestra y ledgers del Growth OS"
