---
title: "Auditoría de monetización por afiliación de Mercado Libre — Growth OS"
purpose: "Evaluar el estado operativo y comercial del piloto de productos afiliados de Mercado Libre en Facebook, identificar brechas de atribución y proponer acciones medibles para aumentar los clics."
status: "Review"
created: 2026-08-22
updated: 2026-08-22
version: "1.1"
author: "Manus AI (CGO)"
related_documents:
  - "GrowthOS/11_00_Estrategia_Monetizacion_MercadoLibre.md"
  - "Operations/Production/2026-08-19_Playbook_Tracking_Afiliados_MercadoLibre.md"
  - "Operations/Research/Affiliate_Link_Ledger.csv"
  - "Operations/Research/Affiliate_Metrics_Snapshots.csv"
  - "Operations/Research/Affiliate_Pilot_Assignments.csv"
  - "Operations/Research/2026-08-19_MercadoLibre_Facebook_Afiliados_Observacion.md"
organization: "Operations/Research"
---

# Auditoría ejecutiva

La monetización por afiliación de Mercado Libre está en estado **Ámbar: infraestructura preparada, validación granular todavía insuficiente**. El piloto tiene diez productos, diez enlaces afiliados y diez etiquetas únicas. Sin embargo, solo **1 de 10 publicaciones** tiene adjunción nativa confirmada en Facebook; las otras nueve permanecen pendientes. Por tanto, el sistema puede operar, pero todavía no existe una muestra granular suficiente para saber qué producto, personaje, horario o formato genera clics.

La evidencia comercial disponible es histórica y agregada: **3 clics, 2 unidades vendidas, $322.65 MXN en ventas brutas y $28.84 MXN de comisión estimada**, con las ventas todavía en revisión. La señal demuestra que el método de Facebook puede producir actividad comercial, pero no permite atribuir esos resultados a una publicación concreta. El piloto actual aún tiene **0 snapshots granulares**, por lo que no debe declararse ganador ningún producto ni personaje.

> **Veredicto:** el cuello de botella principal no es la creación de enlaces; es la activación consistente de las publicaciones y la captura de métricas por etiqueta después de cada publicación.

## 1. Estado actual del sistema

| Componente | Estado | Evidencia | Lectura |
|---|---|---|---|
| Estrategia story-commerce | Activa | `GrowthOS/11_00_Estrategia_Monetizacion_MercadoLibre.md` | El modelo narrativo está definido, pero todavía no se valida por cohortes. |
| Productos seleccionados | Completo | 10 filas del ledger | Cada oportunidad tiene producto y URL de producto. |
| Enlaces afiliados | Completo | 10 links `meli.la` | Cobertura técnica 10/10. |
| Etiquetas de tracking | Completo | 10 etiquetas únicas | Permite separar producto/publicación/superficie. |
| Adjunción nativa en Facebook | Inicial | 1/10 confirmadas | Cobertura operativa 10%; AFF-02–AFF-10 pendientes. |
| Publicaciones programadas | Parcialmente activas | 1 registrada como `Scheduled`; 9 como `Not_Attached` | La publicación y la monetización aún no están sincronizadas en el ledger. |
| Métricas granulares | Ausentes | 0 snapshots actuales | No hay clics por AFF, CTR, ventas por link ni comisión por publicación. |
| Histórico agregado | Disponible, limitado | 3 clics; 2 unidades; $28.84 MXN estimados | Señal positiva, pero no atribuible por publicación. |

## 2. Economía observada

El histórico agregado registra 3 clics y 2 unidades vendidas. La tasa visible es de 66.67%, pero el denominador es demasiado pequeño para usarla como benchmark. La comisión estimada equivale a $9.61 MXN por clic y la venta bruta a $107.55 MXN por clic; ambos valores son orientativos porque las ventas siguen en revisión y no existe atribución granular.

| Métrica histórica | Valor | Interpretación |
|---|---:|---|
| Clics | 3 | Actividad comercial observable, muestra mínima. |
| Compradores | 1 | Un comprador puede generar más de una orden. |
| Unidades | 2 | Ambas ventas están en revisión. |
| Ventas brutas | $322.65 MXN | No equivale todavía a ingreso confirmado. |
| Comisión estimada | $28.84 MXN | No es comisión aprobada. |
| Conversión visible | 66.67% | No usar como expectativa; n=3 clics. |
| Comisión estimada por clic | $9.61 MXN | Indicador provisional de valor del tráfico. |
| Tasa comisión/ventas brutas | 8.94% | Mezcla de productos con tasas distintas; no generalizar. |

## 3. Qué falta

### 3.1 Activación operativa

Falta adjuntar nativamente AFF-02 a AFF-10 en sus publicaciones correspondientes. La adjunción debe registrarse después de guardar en Facebook, junto con la fecha, el estado confirmado y, si Meta lo muestra, el identificador de producto nativo. No basta con que el enlace exista en el ledger de Mercado Libre.

### 3.2 Medición granular

Falta crear un snapshot después de cada publicación y luego en cortes comparables, como 24 horas, 72 horas y cierre de atribución. El snapshot mínimo debe contener etiqueta, publicación, fecha local, clics, ventas brutas, ventas aprobadas, unidades, comisión estimada, comisión confirmada y estado del reporte. El histórico agregado no debe mezclarse con el piloto.

### 3.3 Atribución entre contenido y comercio

Falta vincular cada resultado comercial con el `Content_ID`, personaje, formato, CTA, hora y producto. Las diez etiquetas ya permiten hacerlo, pero el ledger todavía no contiene métricas para AFF-01 y las nueve oportunidades restantes están sin adjunción confirmada.

### 3.4 Validación editorial

Falta comprobar si el producto aparece de forma natural en la publicación. Un enlace nativo puede generar exposición, pero si el contenido no crea una razón clara para explorar el producto, la presencia del enlace no garantiza clics. También debe evitarse presentar cada pieza como un anuncio aislado: el producto debe cumplir una función narrativa visible.

### 3.5 Transparencia y control

Falta estandarizar la mención de afiliación cuando corresponda y mantener una revisión humana de cada producto, precio, disponibilidad y coherencia con el contenido. Los precios y la disponibilidad pueden cambiar; por ello, la información del producto debe verificarse antes de cada publicación o actualización.

## 4. Cómo aumentar los clics

La prioridad es aumentar primero la **exposición cualificada** y después optimizar el porcentaje de personas que decide explorar el producto. No conviene insertar el enlace en todas las publicaciones sin una hipótesis, porque eso destruye la capacidad de comparar.

| Prioridad | Acción | Hipótesis | Medición |
|---|---|---|---|
| P0 | Adjuntar AFF-02–AFF-10 | Más publicaciones activas producirán una base suficiente de clics. | 10/10 adjuntas; snapshots por etiqueta. |
| P0 | Usar CTA explícito y único | “Mira el producto que recibió Fantasma” será más accionable que “link en bio”. | Clics por publicación y CTR sobre alcance/vistas disponibles. |
| P0 | Mostrar el producto en el primer segundo | Reconocimiento inmediato aumenta la intención de explorar. | Comparar clics por piezas con producto visible vs. solo mencionado. |
| P1 | Mantener un solo producto por publicación | Menos opciones reduce fricción y mejora la atribución. | Clics y conversión por producto. |
| P1 | Crear una razón narrativa para comprar | Utilidad, transformación o humor deben justificar el clic. | Clics por ángulo: utilidad, regalo, identidad, curiosidad. |
| P1 | Repetir ganadores con variaciones | Un producto/personaje con señal positiva merece una segunda prueba. | Segundo test con nuevo hook y misma etiqueta de producto en una nueva versión. |
| P1 | Usar comentarios fijados como apoyo | El comentario puede recuperar a quienes no hicieron clic al ver el post. | Comparar clics antes/después del comentario fijado, sin mezclar etiquetas. |
| P2 | Construir colecciones por personaje | Agrupar productos puede aumentar sesiones posteriores, pero añade fricción. | Clics a colección y clics por producto. |
| P2 | Llevar el formato a Mercado Libre Clips | El marketplace puede aportar tráfico de mayor intención. | Separar etiqueta/superficie y comparar CTR con Facebook. |

## 5. Recomendación de copy y estructura

Cada publicación afiliada debería responder rápidamente a tres preguntas: **qué apareció, por qué le importa al personaje y dónde se puede ver**. La estructura recomendada es un hook visual inmediato, una reacción del personaje, una demostración o remate y un CTA directo.

Ejemplo de patrón para Fantasma: “Fantasma quería asustar a todos y terminó decorando la casa. Mira la decoración con luz LED que llegó al universo. **Toca el producto para verlo.**” El copy exacto debe adaptarse al contenido real; no se debe prometer una característica que el producto no tenga.

Los CTA que deben probarse por cohortes son: **“Toca el producto para verlo”**, **“Mira qué le llegó a Fantasma”**, **“¿Lo usarías en tu casa?”** y **“Descubre el producto del episodio”**. No se deben probar todos en la misma pieza; cada CTA debe quedar registrado para poder compararlo.

## 6. Plan operativo de los próximos siete días

Primero, completar la adjunción nativa de AFF-02 a AFF-10, validando producto, nombre, enlace y publicación. Segundo, capturar un snapshot granular por etiqueta después de cada publicación y en el corte de 24 horas. Tercero, registrar alcance o vistas de Facebook cuando estén disponibles para calcular CTR; si Meta no entrega una métrica comparable, informar clics absolutos y no fabricar CTR. Cuarto, revisar qué piezas obtienen comentarios que expresen intención —por ejemplo, “¿dónde lo consigo?”— y convertir esa señal en una hipótesis, no en una venta. Quinto, al cierre del periodo, clasificar cada oportunidad como **Validada**, **Parcialmente validada**, **No validada** o **Inconclusa**.

## 7. Criterios de éxito del piloto

El piloto debe considerarse instrumentado cuando las diez publicaciones tengan adjunción confirmada y exista al menos un snapshot por etiqueta. Debe considerarse comercialmente informativo cuando haya suficiente volumen para comparar productos y piezas sin depender de una sola venta. Como regla prudente, no declarar un ganador con menos de 10 clics por variante; antes de ese umbral, los resultados son señales exploratorias.

Los indicadores principales serán clics por publicación, CTR sobre vistas o alcance cuando la fuente sea comparable, ventas aprobadas por clic y comisión confirmada por publicación. Las ventas brutas y las comisiones en revisión se conservarán como métricas tempranas, pero no como resultado final.

## 8. Documentos que requieren sincronización

La ejecución de este informe requiere mantener sincronizados `Affiliate_Link_Ledger.csv`, `Affiliate_Pilot_Assignments.csv`, `Affiliate_Metrics_Snapshots.csv` y el playbook de tracking. La estrategia de monetización debe conservar la distinción entre la señal histórica agregada y el piloto granular. La auditoría previa de Reels y monetización debe leerse como corte histórico del 19 de agosto; este documento actualiza el estado operativo del piloto al 22 de agosto y no invalida sus conclusiones sobre la falta de vistas/retención comparables.

## Fuentes internas

1. `Operations/Research/Affiliate_Link_Ledger.csv`
2. `Operations/Research/Affiliate_Metrics_Snapshots.csv`
3. `Operations/Research/Affiliate_Pilot_Assignments.csv`
4. `Operations/Research/2026-08-19_MercadoLibre_Facebook_Afiliados_Observacion.md`
5. `GrowthOS/11_00_Estrategia_Monetizacion_MercadoLibre.md`
6. `Operations/Production/2026-08-19_Playbook_Tracking_Afiliados_MercadoLibre.md`


## Addendum de reconciliación — 2026-08-22

La revisión ampliada confirmó que el trabajo de afiliación no se limita a las diez oportunidades AFF-01–AFF-10. El ledger contiene actualmente **18 enlaces individuales y 18 etiquetas únicas**, distribuidos así:

| Capa / campaña | Enlaces | Estado documentado | Lectura |
|---|---:|---|---|
| Piloto calendario AFF-01–AFF-10 | 10 | 10 `Native_Product_Attached_User_Confirmed` | Cobertura completa del piloto. |
| Capa 2 posts ganadores | 2 | 2 `Native_Product_Attached_User_Confirmed` | Wilfred/Xhp360 y Evan+Kiri/tiras LED. |
| Reel nativo adicional | 1 | `Published` + `Native_Product_Attached_User_Confirmed` | Universe, soporte de celular; etiqueta `usmfb20260819p01`. |
| Universe/Senales multicanal | 4 | Facebook e Instagram programados; TikTok y YouTube en espera | El link existe, pero no todas las superficies están activas o verificadas. |
| Histórico agregado | 1 registro sin link individual | 3 clics, 2 unidades, $322.65 MXN brutos, $28.84 MXN estimados | No atribuible a una publicación específica. |

La cifra correcta de cobertura operativa documentada es **14 de 18 enlaces individuales con publicación o adjunción confirmada**, mientras que cuatro filas de Universe/Senales permanecen programadas, en espera o sin publicación según la superficie. Esto corrige la lectura anterior de 1/10: esa cifra correspondía a un corte local anterior y quedó superada por las confirmaciones registradas posteriormente en GitHub.

## Evidencia de clics disponible

El archivo `Affiliate_Metrics_Snapshots.csv` contiene seis snapshots. El histórico agregado conserva 3 clics. Un corte manual de fecha registra 2 clics agregados para las etiquetas visibles del 18 de agosto, pero no los atribuye a un link individual. Otro corte registra **1 clic para AFF-07 / Elara / lámpara LED de lectura**. La etiqueta del Reel nativo adicional no fue visible en la tabla; su estado correcto es `Not_Visible_No_Inference`, no cero clics. No hay todavía una serie de CTR comparable por capa.

## Lectura actual de Growth

La conclusión estratégica cambia de “activar los enlaces” a **medir y optimizar una cartera ya activada**. La cobertura técnica y editorial es suficiente para iniciar aprendizaje, pero los datos siguen siendo escasos. La prioridad es capturar cortes de 24 horas, 48 horas y 7 días por etiqueta; separar Facebook, Instagram, TikTok y YouTube; y no mezclar el histórico agregado con los registros granulares.

También debe mantenerse separado el estado de una publicación programada, una publicación publicada y una adjunción nativa confirmada. Para cada fila se requiere `Content_ID`, superficie, fecha de publicación, fecha de adjunción, permalink o ID nativo, etiqueta, clics, ventas aprobadas y comisión confirmada.

## Inconsistencias pendientes

El catálogo visual conserva nombres que aparentemente no coinciden con algunos productos del ledger, especialmente `AFF-06_rose_gift.webp` frente al soporte de taza con abrazadera y `AFF-07_earbuds.webp` frente a la lámpara de lectura. Antes de reutilizar imágenes de producto, se debe verificar la correspondencia visual contra el producto afiliado real.

La estrategia de crecimiento debe priorizar ahora: **(1)** reconciliar los 18 enlaces por superficie; **(2)** obtener snapshots comparables; **(3)** repetir el análisis de AFF-07, que tiene la primera señal individual visible; **(4)** proteger al menos un post ganador como control sin producto en la Capa 2; y **(5)** probar hooks y CTA que hagan explícita la acción “toca el producto” sin alterar retroactivamente el contenido que ya demostró rendimiento.

Este addendum actualiza el diagnóstico operativo del 22 de agosto. El análisis histórico de la observación del 19 de agosto se conserva como evidencia de su fecha y no debe interpretarse como el estado actual completo.
