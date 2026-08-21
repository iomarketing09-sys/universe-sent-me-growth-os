---
title: "Piloto Content Rewards — Bam in a Can"
purpose: "Definir la identidad, alcance, controles y secuencia de activación del piloto de Content Rewards operado por Bam in a Can, independiente de Universe Sent Me."
status: "Active"
created: 2026-08-20
updated: 2026-08-20
version: "1.1"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-20_Evaluacion_Content_Rewards_Capa_Monetizacion.md"
  - "GrowthOS/11_00_Estrategia_Monetizacion_MercadoLibre.md"
  - "Operations/Production/2026-08-19_Playbook_Tracking_Afiliados_MercadoLibre.md"
  - "Operations/Production/Brand_Assets/Bam_In_A_Can/Bam_in_a_can_Logo.png"
organization: "Operations/Production"
---

# Piloto Content Rewards — Bam in a Can

## 1. Mandato y separación de marca

**Bam in a Can** es una cápsula editorial de cultura rara de internet: cine extraño, memes absurdos, IA, internet culture y hallazgos que merecen ser “enlatados”. Su función dentro de este piloto es operar campañas de terceros autorizadas por Content Rewards, no monetizar los personajes, renders, audiencia ni activos de **Universe Sent Me**.

> **Posicionamiento:** “Bam in a Can” encuentra cosas anómalas de internet y las convierte en unidades editoriales coleccionables.

El logo de referencia aprobado por Fernando se conserva en `Operations/Production/Brand_Assets/Bam_In_A_Can/Bam_in_a_can_Logo.png`. La marca visual combina retro-futurismo, editorial absurda, found footage e internet culture; su base cromática es negro/carbono, crema envejecido, rojo tomate, gris metálico y acentos puntuales verde ácido.

## 2. Canales del piloto

| Plataforma | Identidad | Estado de piloto | Uso permitido |
|---|---|---|---|
| YouTube | `@bam_in_a_can` | Disponible | Shorts autorizados por cada campaña. |
| Instagram | `@bam_in_a_can` | Disponible | Reels autorizados por cada campaña. |
| TikTok | `@bam_in_a_can` | Disponible | Videos autorizados por cada campaña. |
| Facebook | Pendiente de crear | Fuera de la fase inicial | Considerar solo después de validar el piloto; no bloquea la activación. |

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

## 5. Diseño del piloto de 21 días

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

**Estado:** `CANDIDATE_REVIEWED — no unido, no enviado, no publicado`  
**URL pública:** https://contentrewards.com/discover/2b523257-cb89-4faf-90c2-770aea3db60a

Klap es una herramienta de IA que convierte videos largos, podcasts y webinars en clips cortos con captions. La campaña pública pide piezas con gancho viral a partir de UGC proporcionado que muestre Klap y anuncia libertad creativa condicionada a promover la herramienta y respetar las reglas del brief. La ficha pública indica TikTok, Instagram y YouTube Shorts como los destinos previstos, con un CPM de USD 2 y un presupuesto de USD 7,000; la interfaz visible mostraba USD 189 comprometidos, por lo que no se interpreta ese importe como presupuesto restante hasta la revisión autenticada.[4]

| Criterio | Lectura inicial |
|---|---|
| Encaje editorial | Alto: IA creativa, edición, cultura de clips y estética de internet son pilares de Bam. |
| Encaje de canales | Alto: coincide con los tres canales existentes `@bam_in_a_can`. Facebook no es requisito inicial. |
| Riesgo de marca | Medio-bajo, sujeto al brief: no pertenece a categorías excluidas, pero requiere disclosure y verificación de claims. |
| Riesgo de derechos | Pendiente: confirmar en el brief autenticado el alcance de los UGC, la licencia y si el material se puede editar bajo los términos del piloto. |
| Riesgo de operación | Pendiente: confirmar máximo por video, mínimo de pago, reglas de submit, límites de cross-post y cualquier limitación geográfica. |
| Decisión | **Candidata recomendada para auditar primero; no autoriza unirse todavía.** |

La campaña de CapCut/Seedance se mantiene como observación secundaria, no como primera prueba: aunque el CPM público era de USD 3, la interfaz mostraba una tasa visible de aprobación de 8%, un riesgo innecesario para el primer test. No se eligen campañas de apuestas, predicción, cripto, trading o categorías restringidas aunque tengan CPM superior.

## Referencias

[1]: https://contentrewards.com/discover "Content Rewards — Discover Campaigns"

[2]: https://www.contentrewards.com/terms-of-service/clippers "Content Rewards — Clippers Terms of Service"

[3]: https://www.contentrewards.com/faqs "Content Rewards — Frequently Asked Questions"

[4]: https://contentrewards.com/discover/2b523257-cb89-4faf-90c2-770aea3db60a "Content Rewards — Klap Viral Clipping"
