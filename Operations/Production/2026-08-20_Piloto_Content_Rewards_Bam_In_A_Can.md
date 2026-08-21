---
title: "Piloto Content Rewards — Bam in a Can"
purpose: "Definir la identidad, alcance, controles y secuencia de activación del piloto de Content Rewards operado por Bam in a Can, independiente de Universe Sent Me."
status: "Active — Audience Bootstrap; third-party campaigns paused"
created: 2026-08-20
updated: 2026-08-20
version: "1.3"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-20_Evaluacion_Content_Rewards_Capa_Monetizacion.md"
  - "GrowthOS/11_00_Estrategia_Monetizacion_MercadoLibre.md"
  - "Operations/Production/2026-08-19_Playbook_Tracking_Afiliados_MercadoLibre.md"
  - "Operations/Production/Brand_Assets/Bam_In_A_Can/Bam_in_a_can_Logo.png"
organization: "Operations/Production"
---

# Piloto Content Rewards — Bam in a Can

## 0. Decisión operativa vigente — construir antes de monetizar

El 20 de agosto Fernando confirmó que los tres perfiles `@bam_in_a_can` se acaban de crear. Por tanto, **Bam in a Can no inicia todavía ninguna campaña de Content Rewards**. La ruta de Klap permanece archivada como candidata evaluada, pero no se vinculan cuentas, no se aceptan briefs, no se descargan assets ni se publica contenido de terceros.

La prioridad inmediata es construir audiencia propia, lenguaje editorial y consistencia de formato. Content Rewards se reconsidera cuando Bam cuente con una base de seguidores y una distribución de audiencia que permita competir por campañas sin convertir la marca en una cuenta exclusiva de un anunciante.

## 1. Mandato y separación de marca

**Bam in a Can** es una cápsula editorial de cultura rara de internet: cine extraño, memes absurdos, IA, internet culture y hallazgos que merecen ser “enlatados”. Su función dentro de este piloto es operar campañas de terceros autorizadas por Content Rewards, no monetizar los personajes, renders, audiencia ni activos de **Universe Sent Me**.

> **Posicionamiento:** “Bam in a Can” encuentra cosas anómalas de internet y las convierte en unidades editoriales coleccionables.

El logo de referencia aprobado por Fernando se conserva en `Operations/Production/Brand_Assets/Bam_In_A_Can/Bam_in_a_can_Logo.png`. La marca visual combina retro-futurismo, editorial absurda, found footage e internet culture; su base cromática es negro/carbono, crema envejecido, rojo tomate, gris metálico y acentos puntuales verde ácido.

## 2. Canales del piloto

| Plataforma | Identidad | Estado de piloto | Uso permitido |
|---|---|---|---|
| YouTube | `@bam_in_a_can` | Recién creado | Prioridad: construir catálogo propio de Shorts. |
| Instagram | `@bam_in_a_can` | Recién creado | Prioridad: construir catálogo propio de Reels. |
| TikTok | `@bam_in_a_can` | Recién creado | Prioridad: construir catálogo propio de videos. |
| Facebook | Pendiente de crear | No prioritario | Evaluar tras validar los tres canales principales. |

Los canales deben ser públicos, pertenecer realmente a Fernando y vincularse a su perfil de Content Rewards conforme a las condiciones de la plataforma. No se crean cuentas ficticias, duplicadas ni automatizadas.

## 3. Lenguaje editorial de Bam

Cada pieza puede ser tratada como una unidad de colección `CAN 001`, `CAN 002`, `CAN 003`, etc. El número no es obligatorio en toda publicación; se emplea cuando aporte sensación de archivo, descubrimiento o serie. La marca no es un repositorio de clips: su criterio editorial debe conservar el gesto de **“¿qué demonios acabo de encontrar?”** y seleccionar solo material que pueda vivir con una identidad visual coherente.

| Pilar | Encaje con campañas de Content Rewards | Criterio de aceptación |
|---|---|---|
| Cine raro / cult | Alto | Derechos y assets expresamente autorizados; contenido apto para el tono editorial. |
| Memes / humor absurdo | Medio-alto | La campaña debe permitir una edición original y no una publicación repetitiva. |
| IA y cultura generativa | Alto | Herramientas creativas o IA, sin promesas engañosas ni uso de IP de USM. |
| Internet culture | Medio | Debe aportar una anomalía o hallazgo real, no solo notoriedad ajena. |
| Surrealismo / contenido inesperado | Alto | Debe ser compatible con el brief, la plataforma y la lista de exclusión. |

## 4. Barreras no negociables

1. **Cero assets de Universe Sent Me:** no usar personajes, escenarios, renders, música, archivo de producción, comunidad ni el nombre de USM en piezas para campañas de terceros.
2. **Lista de exclusión:** casino, apuestas, predicción, cripto especulativa, trading, política, alcohol, adulto, medicamentos/suplementos y promesas financieras.
3. **Manual y por brief:** cada publicación se crea y publica manualmente. Ninguna herramienta automatiza publicación, engagement, vistas o reutilización masiva.
4. **Disclosure visible:** usar el control comercial nativo de la plataforma cuando exista y la declaración requerida por el brief, como `Publicidad pagada` o `#ad`.
5. **Derechos primero:** no iniciar edición hasta comprobar que el brief permite el uso de los assets y que Fernando acepta la licencia de contenido asociada.
6. **Una campaña, una decisión:** no publicar un asset idéntico en cascada por defecto. Se siguen las plataformas autorizadas, el límite de reutilización y la modalidad de envío de la campaña concreta.

## 5. Diseño del piloto de 21 días — **pausado hasta la madurez de audiencia**

| Variable | Definición |
|---|---|
| Duración | 21 días desde la primera publicación aprobada en Content Rewards. |
| Máximo de campañas | 3. |
| Máximo de piezas | 6, incluyendo revisiones. |
| Presupuesto de medios | USD 0; no se ejecuta una campaña de marca de USM. |
| Categorías preferidas | Herramientas creativas, IA creativa, gaming apto, música con assets oficiales, cine/entretenimiento familiar. |
| Métrica principal | Pago neto confirmado por hora real de trabajo. |
| Métricas de control | Aprobación, vistas verificadas, rechazo, payout provisional, payout confirmado, horas y riesgos de marca. |
| Gate de continuidad | ≥80% de aprobación, cero incidente crítico, y pago neto confirmado que justifique el tiempo frente a la producción propia de USM. |

## 6. Ledger y secuencia de activación

Antes de unirse a una campaña, crear `Operations/Research/Content_Rewards_Pilot_Ledger.csv` con una fila por propuesta revisada o publicación. El ledger deberá registrar: `Campaign_Name`, `Campaign_URL`, `Brand`, `Category`, `Allowed_Platforms`, `CPM_or_Fixed_Rate`, `Budget_Remaining`, `Max_Payout_Per_Video`, `Minimum_Payout`, `Rights_Summary`, `Disclosure_Requirement`, `Bam_Channel`, `Asset_ID`, `Posted_At`, `Submitted_At`, `Approval_Status`, `Verified_Views`, `Gross_Payout_USD`, `Platform_Fee_USD`, `Net_Payout_USD`, `Hours_Actual`, `Risk_Status`, `Source` y `Notes`.

La primera campaña no se acepta de inmediato. Primero se audita su página por categoría, brand safety, derechos, CPM, presupuesto restante, plataformas permitidas, límite por video, mínimo de pago, reglas de contenido, disclosure y método de envío. Fernando conserva la aprobación específica para crear cuenta, vincular canales, introducir datos de pago, aceptar términos de una campaña o publicar.

## 7. Documentos que requieren actualización posterior

Al iniciar el piloto se crea el ledger indicado y se actualiza este brief con la campaña seleccionada. Al publicar una pieza se añade la fila correspondiente y se enlaza el resultado de métricas. La evaluación estratégica de `Operations/Research/2026-08-20_Evaluacion_Content_Rewards_Capa_Monetizacion.md` se actualiza al cierre del día 21 con la recomendación de escalar, iterar o cerrar el carril.

## 8. Primera candidata bajo revisión — Klap Viral Clipping

**Estado:** `CANDIDATE_PAUSED — cuentas de Bam recién creadas; no unido, no enviado, no publicado`
**URL pública:** https://contentrewards.com/discover/2b523257-cb89-4faf-90c2-770aea3db60a

Klap es una herramienta de IA que convierte videos largos, podcasts y webinars en clips cortos con captions. La campaña pide piezas con gancho viral a partir de UGC proporcionado que muestre Klap y anuncia libertad creativa condicionada a promover la herramienta y respetar las reglas del brief. La guía compartida por Fernando confirma TikTok, Instagram y YouTube Shorts como destinos, con CPM de USD 2, mínimo de USD 2, máximo de USD 500 por post y presupuesto total de USD 7,000. Los clips se envían exclusivamente por Content Rewards y deben mantenerse publicados durante 30 días.[4] [5]

| Criterio | Lectura inicial |
|---|---|
| Encaje editorial | Alto: IA creativa, edición, cultura de clips y estética de internet son pilares de Bam. |
| Encaje de canales | Alto: coincide con los tres canales existentes `@bam_in_a_can`. Facebook no es requisito inicial. |
| Riesgo de marca | Medio-bajo, sujeto al brief: no pertenece a categorías excluidas, pero requiere disclosure y verificación de claims. |
| Riesgo de derechos | UGC y formatos entregados por campaña. Antes de aceptar, confirmar dentro de Content Rewards el alcance de licencia aplicable a assets y clips finales. |
| Riesgo de operación | Alto hasta validar que al menos un canal de Bam cumple el mínimo de 1,000 seguidores y que su audiencia es compatible con el objetivo de 70% Tier 1/EE. UU. |
| Decisión | **Hold condicional.** Es candidata apta solo después de pasar los gates de entrada siguientes. |

### Gates de entrada verificados por la guía

| Gate | Requisito de Klap | Decisión para Bam in a Can |
|---|---|---|
| Nicho | Página relevante de IA/tech, edición, marketing, meme o tema compatible. | **PASS conceptual:** Bam opera en IA, memes e internet culture. |
| Seguidores | Página de nicho relevante con **1,000+ seguidores**; si no existe, el brief sugiere crear una página dedicada a Klap. | **PENDIENTE:** confirmar seguidores por canal. No crear una página paralela de Klap que diluya Bam. |
| Audiencia | Enfoque principal en mercado de EE. UU., 70% audiencia Tier 1. | **PENDIENTE:** confirmar audiencia disponible y producir en inglés si se entra. |
| Formatos | Revisar el documento obligatorio de formatos de edición antes de producir. | **PENDIENTE:** no descargar ni editar assets hasta revisarlo. |
| CTA | Etiquetar `@klap_ai`, usar `#klapaipropgda`, poner `https://klap.app/` en bio y dirigir el caption al enlace. | Compatible solo en el canal que se asigne al piloto. |
| Retención | Dejar cada clip publicado al menos 30 días. | Aceptar únicamente si Bam puede mantener la pieza visible. |
| Calidad | Sin money claims; subtítulos limpios, correctos, sin IA, sin animaciones/glow excesivos, sin skull edits ni reposts perezosos. | Compatible con la marca, pero requiere edición manual de subtítulos. |
| Watermarks | No usar watermark de otra marca ni del propio canal. | El avatar y la bio de Bam pueden permanecer; **no** incrustar el logo BAM dentro de los clips de Klap. |

La campaña puede encajar en el pilar de IA editorial de Bam, pero no debe forzar la marca a convertirse en una cuenta exclusiva de Klap. Como los perfiles están recién creados, esta campaña queda pausada de forma explícita. No se adopta la sugerencia del brief de abrir una página dedicada a Klap porque rompería la independencia de Bam y añadiría una cuenta cuyo único propósito sería una campaña de tercero. La evaluación se retoma únicamente después de completar la fase de audiencia propia.

La campaña de CapCut/Seedance se mantiene como observación secundaria, no como primera prueba: aunque el CPM público era de USD 3, la interfaz mostraba una tasa visible de aprobación de 8%, un riesgo innecesario para el primer test. No se eligen campañas de apuestas, predicción, cripto, trading o categorías restringidas aunque tengan CPM superior.

## Referencias

[1]: https://contentrewards.com/discover "Content Rewards — Discover Campaigns"

[2]: https://www.contentrewards.com/terms-of-service/clippers "Content Rewards — Clippers Terms of Service"

[3]: https://www.contentrewards.com/faqs "Content Rewards — Frequently Asked Questions"

[4]: https://contentrewards.com/discover/2b523257-cb89-4faf-90c2-770aea3db60a "Content Rewards — Klap Viral Clipping"

[5]: https://docs.google.com/document/d/1N6h5axvtkMlpNVBdB18sTf0ylo7UVKoT/edit "Klap UGC Clipping — Full Guide by Propaganda"
