---
title: "G-SEC-2.4c-P — Procedimiento preliminar para una futura propuesta mínima — Universe Sent Me"
purpose: "Definir una secuencia documental previa para preparar, bajo una autorización posterior independiente, una propuesta mínima revisable contra G-SEC-2, sin crearla, emitirla, solicitar consentimiento ni autorizar una operación."
status: Review
created: 2026-08-27
updated: 2026-08-27
version: "1.2"
author: "Manus AI"
related_documents:
  - "Operations/Automation/2026-08-27_Gate_Diseno_Propuesta_Hipotetica_Unica_GSEC2_4cP1_USM.md"
  - "Operations/Automation/2026-08-27_Ficha_Propuesta_Minima_Comparacion_Alcance_USM.md"
  - "Operations/Automation/2026-08-27_Plantilla_Tarjeta_Consentimiento_Puntual_USM.md"
  - "Operations/Automation/2026-08-25_Consentimiento_Piloto_Real_Shadow_Ledger_USM.md"
  - "Operations/Automation/2026-08-27_Revision_Final_Consolidacion_GSEC2_USM.md"
  - "Operations/Automation/2026-08-25_Plan_Decision_Cifrado_Local_G-NORM-4R.md"
  - "GrowthOS/todo.md"
organization: "Operations/Automation"
---

# G-SEC-2.4c-P — Procedimiento preliminar para una futura propuesta mínima

## Propósito y frontera de este diseño

**G-SEC-2.4c-P** describe únicamente cómo debería organizarse, en el futuro, la preparación documental de una propuesta mínima. No es una propuesta, no es una copia de la ficha G-SEC-2.4c, no es una tarjeta de consentimiento y no es un gate que habilite datos u operaciones. Su única función es conservar una secuencia clara para que una propuesta futura no se confunda con una autorización.

> **Límite decisivo:** este procedimiento no permite completar, copiar ni emitir la ficha pública; no permite pedir, registrar o inferir consentimiento; y no permite abrir información privada, ejecutar preflights o realizar una operación G-NORM-4R.

Los únicos materiales que este diseño puede nombrar son documentos públicos de política y sus estados: G-SEC-2, la plantilla vacía, la ficha pública G-SEC-2.4c y la consolidación G-SEC-2.6. No se usan capturas, métricas, valores, contenido, IDs, URLs, cuentas, rutas protegidas, tokens, configuración, evidencia ni logs.

## Estado cero obligatorio

La condición inicial es que **no existe una propuesta futura**. La ficha pública se mantiene vacía, todos sus marcadores permanecen como `[PENDIENTE — no emitir]` o `[PENDIENTE — no comparar]`, y no hay tarjeta, vigencia, solicitud ni operación asociada.

| Artefacto | Estado documental actual | Qué puede aportar al procedimiento | Qué no permite |
|---|---|---|---|
| G-SEC-2 | `Review` | Límites de datos, retención, read-only y consentimiento. | Activar G-NORM-4R o leer datos privados. |
| Plantilla de tarjeta | `Review`, vacía | Estructura que una tarjeta futura tendría que satisfacer. | Emitir o solicitar la tarjeta. |
| Ficha pública G-SEC-2.4c | `Review`, vacía | Los diez controles de comparación y sus límites. | Copiarla o completar una propuesta. |
| Consolidación G-SEC-2.6 | `Review` | Evidencia de coherencia documental pública. | Sustituir consentimiento o autorizar una operación. |
| Este procedimiento G-SEC-2.4c-P | `Draft` | Secuencia de preparación y bloqueos. | Crear una instancia de propuesta. |

## Secuencia preliminar para una futura preparación

La secuencia siguiente es descriptiva. Cada etapa posterior requerirá una autorización nueva, explícita y limitada. Ninguna autorización de un paso se transfiere al siguiente.

| Etapa futura | Acción que podría diseñarse bajo un gate separado | Salida documental permitida | Prohibición que se mantiene |
|---|---|---|---|
| 1. Revisar este procedimiento | Confirmar que la secuencia, los bloqueos y el estado cero se comprenden. | Cambio de este documento de `Draft` a `Review`, si se autoriza. | No copiar la ficha ni proponer una operación. |
| 2. Autorizar el diseño de una propuesta hipotética | Delimitar un nuevo gate exclusivamente documental para describir una sola propuesta futura no sensible. | Borrador de alcance, solo si el gate lo autoriza expresamente. | No incluir datos, fechas, vigencia, IDs, valores, cuentas, rutas ni secretos. |
| 3. Comparar el borrador | Usar los diez controles de G-SEC-2.4c contra la propuesta que un gate posterior haya permitido crear. | `scope_compatible_for_separate_human_request` o `consent_scope_mismatch`. | No emitir tarjeta ni pedir consentimiento. |
| 4. Diseñar la tarjeta puntual | Solo si la comparación completa es compatible y existe otro gate específico. | Diseño de tarjeta aún no emitida. | No declarar consentimiento ni ejecutar preflight. |
| 5. Solicitud humana posterior | Pedir una decisión puntual sobre una única tarjeta completa y vigente. | Decisión humana explícita, si se autoriza en una conversación nueva. | No ejecutar automáticamente ni ampliar el alcance. |

## Condiciones previas antes de cualquier etapa posterior

Antes de avanzar desde el estado cero, una revisión futura debe confirmar de manera documental que G-SEC-2, la plantilla y la ficha continúan en `Review`; que G-SEC-2.1a, G-SEC-2.2a, G-SEC-2.3a, G-SEC-2.4a y G-SEC-2.5 conservan el alcance de PASS sintético o estático; y que G-SEC-2.6 conserva su dictamen de consolidación pública. Si alguna referencia falta, cambia o resulta ambigua, el único resultado es `consent_scope_mismatch`.

También debe comprobarse que no exista una autorización vigente interpretada como consentimiento, ni una tarjeta emitida, ni una propuesta en curso. Las confirmaciones históricas de cifrado LUKS, collectors, normalización, pruebas sintéticas, fichas o plantillas no pueden reutilizarse como permiso operativo.

## Separación de documentos y datos

Este procedimiento protege la diferencia entre una política pública y una futura operación privada. GitHub conserva únicamente políticas, plantillas vacías, estados de gates y resultados agregados sin datos reales. Una hipotética instancia de propuesta, si un gate posterior la habilitara, tendría que crearse exclusivamente bajo LUKS y con el contenido mínimo que el gate correspondiente autorice.

| Clase de información | Ubicación permitida en este diseño | Tratamiento |
|---|---|---|
| Reglas, límites, estados y nombres de gates | Documentación pública del repositorio. | Se pueden revisar y versionar. |
| Marcadores vacíos de ficha y tarjeta | Documentación pública del repositorio. | No se completan ni se convierten en una instancia. |
| Datos de plataformas, métricas, contenido, IDs y evidencia | Ninguna en este procedimiento. | No se leen, anotan, comparan ni transmiten. |
| Tokens, secretos, configuración y rutas privadas | Ninguna en este procedimiento. | No se consultan, copian ni nombran con detalle. |
| Futura propuesta mínima, si llegara a autorizarse | Solo almacenamiento local LUKS bajo un gate distinto. | Sin GitHub, Drive, Sheets, correo, chat, IA ni salida externa. |

## Criterios de detención obligatoria

La preparación debe detenerse sin reparación improvisada si aparece una diferencia entre los documentos, se pretende completar la ficha sin gate, se intenta usar una aprobación anterior como consentimiento, se propone más de una operación, se excede cualquier límite de muestra o retención, o se solicita abrir datos/integraciones. En todos esos casos el resultado requerido es `consent_scope_mismatch` y solo podría documentarse un motivo mínimo no sensible si otro gate lo permite.

No se ejecutan scripts, validadores, collectors, OAuth/API, red, cron, Docker, OmniRoute, ledger, IA ni servicios como parte de la detención. Tampoco se crean archivos temporales o persistentes fuera de la documentación de política.

## Estado y siguiente acción permitida

### Registro de revisión humana — 2026-08-27

Fernando confirmó que comprende el procedimiento preliminar, el estado cero, las condiciones de detención y la separación entre documentación pública y una futura propuesta local. El estado documental cambia de `Draft` a `Review`. Esta confirmación revisa únicamente el diseño del procedimiento; no crea, copia o completa una propuesta, no emite una tarjeta, no solicita o registra consentimiento y no autoriza una operación.

Este procedimiento permanece como una guía de preparación documental. G-SEC-2 continúa en `Review` y G-NORM-4R sigue bloqueado. No se abrió información privada, red, collectors, OAuth/API, ledger, cron, Docker, OmniRoute, Drive, Sheets, GitHub como destino de datos, IA o salida externa.

El gate documental `2026-08-27_Gate_Diseno_Propuesta_Hipotetica_Unica_GSEC2_4cP1_USM.md` v1.0 fue diseñado en `Draft` para delimitar una propuesta hipotética de una sola operación sin crearla. Hasta que ese gate reciba una revisión humana independiente y exista una autorización posterior adicional, la ficha pública, la tarjeta y todos sus marcadores permanecen vacíos.

## Referencias

[1] [Ficha pública de propuesta mínima y comparación manual](2026-08-27_Ficha_Propuesta_Minima_Comparacion_Alcance_USM.md)

[2] [Plantilla vacía de tarjeta de consentimiento puntual](2026-08-27_Plantilla_Tarjeta_Consentimiento_Puntual_USM.md)

[3] [Contrato G-SEC-2](2026-08-25_Consentimiento_Piloto_Real_Shadow_Ledger_USM.md)

[4] [Revisión final y consolidación G-SEC-2.6](2026-08-27_Revision_Final_Consolidacion_GSEC2_USM.md)

[5] [Plan de cifrado local y G-NORM-4R](2026-08-25_Plan_Decision_Cifrado_Local_G-NORM-4R.md)
