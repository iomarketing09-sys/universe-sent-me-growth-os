---
title: "Plantilla vacía y procedimiento de solicitud — tarjeta de consentimiento puntual USM"
purpose: "Proporcionar una plantilla no operativa para solicitar, en el futuro, consentimiento granular de una única operación manual y read-only, sin registrar consentimiento ni autorizar acciones actuales."
status: Review
created: 2026-08-27
updated: 2026-08-27
version: "1.6"
author: "Manus AI"
related_documents:
  - "Operations/Automation/2026-08-25_Consentimiento_Piloto_Real_Shadow_Ledger_USM.md"
  - "Operations/Automation/2026-08-25_Plan_Decision_Cifrado_Local_G-NORM-4R.md"
  - "Operations/Automation/2026-08-25_Shadow_Ledger_Privado_Append_Only_USM.md"
  - "Operations/Automation/2026-08-27_Ficha_Propuesta_Minima_Comparacion_Alcance_USM.md"
  - "Operations/Automation/validate_gsec2_template_static_integrity.py"
  - "Operations/Automation/2026-08-27_Revision_Final_Consolidacion_GSEC2_USM.md"
  - "GrowthOS/todo.md"
---

# Plantilla vacía y procedimiento de solicitud — tarjeta de consentimiento puntual USM

## Propósito y límite estricto

Esta es una **plantilla en blanco** para una posible solicitud futura. No es una tarjeta emitida, no contiene consentimiento de Fernando, no autoriza G-NORM-4R y no debe completarse con secretos, tokens, rutas privadas, IDs de contenido, valores de métricas, evidencia ni datos personales. Su única función actual es estandarizar una futura conversación humana, si y solo si existe un gate separado que lo permita. La plantilla está en `Review`: Fernando confirmó que comprende su alcance, pero no emitió ni solicitó una tarjeta.

> La presencia de esta plantilla no activa collectors, OAuth, API, shadow ledger persistente, cron, Docker, OmniRoute, Drive, Sheets, GitHub como destino de datos, IA ni salida externa.

## Condiciones previas no negociables

Antes de siquiera presentar una tarjeta real vacía para aprobación, se deben cumplir y verificar manualmente estas condiciones: G-SEC-2 permanece coherente en `Review`; G-SEC-2.1a, 2.2a, 2.3a y 2.4a tienen PASS sintético documentado; existe una propuesta técnica pública, precisa y sin secretos; no hay contradicción con el contrato del shadow ledger; y la acción propuesta sigue limitada a una sola ejecución manual read-only.

Una condición ausente, una diferencia entre la propuesta y este documento, o cualquier duda sobre datos/salidas obliga a detener el proceso con el estado `consent_scope_mismatch`. No se corrige el entorno, no se abre configuración privada y no se formula una solicitud de aprobación mientras exista el bloqueo.

## Plantilla vacía — no completar en este documento

Todos los campos marcados como `[PENDIENTE]` deben permanecer vacíos hasta un gate futuro explícitamente aprobado. La tarjeta real, cuando corresponda, debe ser una copia nueva de esta plantilla: **nunca debe editarse retroactivamente esta versión de referencia**.

| Campo obligatorio | Valor permitido en una tarjeta futura | Valor actual de esta plantilla |
|---|---|---|
| Referencia de propuesta | Identificador público y revisable de una única propuesta, sin secretos. | `[PENDIENTE — no emitir]` |
| Versión de controles | Referencias exactas a G-SEC-2 y subgates sintéticos ya aprobados. | `[PENDIENTE — no emitir]` |
| Marca | `Universe Sent Me` únicamente. | `Universe Sent Me` |
| Muestra | Máximo cuatro observaciones, una por TikTok, YouTube, Facebook e Instagram. | `[PENDIENTE — no emitir]` |
| Métricas permitidas | TikTok `views_native`; YouTube `views_native` de período cerrado; Facebook `reactions_native`; Instagram `likes_native`. | `[PENDIENTE — no emitir]` |
| Datos explícitamente excluidos | Monetización, comentarios, captions, texto, URLs, audiencias, IDs, raw, evidencia, tokens y métricas derivadas. | `Excluidos por diseño` |
| Conservación | Máximo 30 días por observación/evidencia; sin backup ni sincronización automática. | `30 días máximos` |
| Operación | Una ejecución manual, local, read-only y sin salida externa. | `[PENDIENTE — no emitir]` |
| Prohibiciones | Sin cron, scheduler, Docker, OmniRoute, Drive, Sheets, GitHub como destino de datos ni IA. | `Prohibidos por diseño` |
| Vigencia | Ventana única, máxima de 24 horas, con inicio y fin explícitos. | `[PENDIENTE — no emitir]` |
| Revocación | Puede revocarse antes de iniciar o durante el preflight; revocar bloquea sin borrar automáticamente. | `Requerida` |
| Resultado permitido | Solo PASS/BLOCKED agregado y conteos seguros; sin valores, filas, rutas o evidencia. | `Solo salida segura` |
| Aprobación humana | Frase inequívoca que repite referencia, alcance, plazo, no-egress, vigencia y revocación. | `[PENDIENTE — no solicitar]` |

## Texto de solicitud futura — borrador no utilizable aún

La siguiente forma solo puede copiarse a una solicitud futura después de completar las condiciones previas. Los corchetes no son instrucciones para proporcionar datos ahora y no deben reemplazarse en esta conversación.

> **Solicitud pendiente — no constituye aprobación.** Se propone una única operación manual read-only bajo `[REFERENCIA PÚBLICA]`, exclusivamente para Universe Sent Me, con una muestra máxima de cuatro observaciones y solo las métricas aprobadas en G-SEC-2. La conservación será de hasta 30 días, sin backup, sincronización ni salida externa. La ventana propuesta es de máximo 24 horas: `[INICIO]` a `[FIN]`. Se prohíben collectors no autorizados, cron, Docker, OmniRoute, Drive, Sheets, GitHub como destino de datos e IA. El resultado se limitará a estado agregado seguro. Puedes revocar antes de iniciar o durante el preflight; cualquier diferencia bloquea la operación sin abrir datos.

Una respuesta válida futura debe repetir, como mínimo, la referencia, el alcance, la vigencia, la prohibición de salidas y la posibilidad de revocación. Un “sí” genérico, una aprobación anterior, una aprobación del cifrado o el consentimiento al diseño no son suficientes.

## Procedimiento humano de solicitud futura

| Paso | Responsable | Acción permitida | Resultado que permite avanzar | Detención obligatoria |
|---|---|---|---|---|
| 1. Propuesta pública | Operador | Redactar una propuesta técnica sin secretos ni datos reales. | Referencia pública revisable. | Falta de precisión o inclusión de datos sensibles. |
| 2. Revisión de alcance | Operador y Fernando | Comparar manualmente la propuesta con los límites de G-SEC-2. | Todos los campos compatibles y dentro de límite. | `consent_scope_mismatch`. |
| 3. Crear copia de tarjeta | Operador | Copiar esta plantilla a un registro nuevo de solicitud, manteniendo vacíos los campos no autorizados. | Tarjeta completa pero aún no aprobada. | Cualquier dato real innecesario o secreto. |
| 4. Solicitud humana | Operador | Presentar una sola tarjeta completa y comprensible; no ejecutar nada mientras se espera. | Respuesta explícita y limitada a la tarjeta. | Respuesta ambigua, incompleta o fuera de alcance. |
| 5. Validar vigencia | Operador | Comprobar manualmente que no exceda 24 horas y que no haya revocación. | Tarjeta vigente y no revocada. | Vencimiento, revocación o cambio de alcance. |
| 6. Preflight separado | Operador | Ejecutar solo el preflight que un gate posterior apruebe expresamente. | Preflight PASS dentro de la ventana. | Cualquier estado BLOCKED; no corregir ni reintentar automáticamente. |
| 7. Decisión posterior | Fernando | Otorgar o negar una autorización distinta para la operación exacta. | Solo un gate posterior puede decidirlo. | Esta plantilla nunca habilita ejecución. |

## Reglas de archivo y trazabilidad futura

Una tarjeta real aprobada deberá conservarse únicamente dentro del almacenamiento local protegido por LUKS, con permisos restrictivos y sin sincronización o repositorio remoto. El repositorio GitHub conservará esta plantilla y la documentación de controles, pero nunca tarjetas completadas, respuestas de consentimiento, evidencia, datos reales o credenciales. La disposición al terminar el período debe seguir la política de retención; no debe realizarse eliminación automática ni reescritura del ledger.

## Estado y siguiente gate permitido

### Registro de revisión humana — 2026-08-27

Fernando confirmó la plantilla vacía y el procedimiento humano de solicitud. Confirma que la plantilla se mantiene vacía, que una tarjeta futura será puntual, limitada, revocable y sin salida externa, y que esta revisión no emite consentimiento ni habilita operación. No se introdujeron referencias de propuestas, fechas de vigencia, datos, tokens, rutas privadas o detalles de una operación.

Esta plantilla está en `Review` y no requiere acción del usuario. La ficha pública de propuesta mínima y la lista manual de comparación de alcance están documentadas en `2026-08-27_Ficha_Propuesta_Minima_Comparacion_Alcance_USM.md` v1.0, en estado `Draft`. G-SEC-2.5 ya pasó su revisión de integridad estática de ambos documentos y del contrato G-SEC-2, usando solo texto público. G-SEC-2.6 está diseñado para consolidar manualmente los controles públicos, sin emitir tarjeta, solicitar consentimiento o abrir G-NORM-4R.

## Referencias

[1] [Contrato de consentimiento G-SEC-2](2026-08-25_Consentimiento_Piloto_Real_Shadow_Ledger_USM.md)

[2] [Plan de cifrado local y G-NORM-4R](2026-08-25_Plan_Decision_Cifrado_Local_G-NORM-4R.md)

[3] [Shadow ledger privado append-only](2026-08-25_Shadow_Ledger_Privado_Append_Only_USM.md)
