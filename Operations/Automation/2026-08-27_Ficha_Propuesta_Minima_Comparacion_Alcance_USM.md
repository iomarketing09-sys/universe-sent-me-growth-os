---
title: "Ficha pública de propuesta mínima y comparación manual de alcance USM"
purpose: "Proporcionar una referencia vacía para describir y comparar, en el futuro, una única propuesta técnica contra los límites G-SEC-2, sin emitir tarjeta, solicitar consentimiento ni autorizar operaciones."
status: Review
created: 2026-08-27
updated: 2026-08-27
version: "2.0"
author: "Manus AI"
related_documents:
  - "Operations/Automation/2026-08-27_Gate_Diseno_Propuesta_Hipotetica_Unica_GSEC2_4cP1_USM.md"
  - "Operations/Automation/2026-08-27_Gate_Formato_Vacio_Propuesta_Hipotetica_GSEC2_4cP2_USM.md"
  - "Operations/Automation/2026-08-27_Plantilla_Tarjeta_Consentimiento_Puntual_USM.md"
  - "Operations/Automation/2026-08-27_Procedimiento_Preliminar_Propuesta_Minima_GSEC2_4c_USM.md"
  - "Operations/Automation/2026-08-27_Revision_Final_Consolidacion_GSEC2_USM.md"
  - "Operations/Automation/2026-08-25_Consentimiento_Piloto_Real_Shadow_Ledger_USM.md"
  - "Operations/Automation/2026-08-25_Plan_Decision_Cifrado_Local_G-NORM-4R.md"
  - "GrowthOS/todo.md"
---

# Ficha pública de propuesta mínima y comparación manual de alcance USM

## Propósito y límites estrictos

Esta ficha permite **describir sin ejecutar** una única propuesta futura y compararla manualmente contra el contrato G-SEC-2 y la plantilla de consentimiento puntual. No es una propuesta emitida, no contiene datos reales, no solicita consentimiento ni determina que una operación sea admisible. Todos los campos variables permanecen vacíos para impedir que este documento se interprete como autorización.

> Esta ficha no activa G-NORM-4R, no abre datos privados ni configuración, no invoca collectors, OAuth o APIs y no permite ledger persistente, cron, Docker, OmniRoute, Drive, Sheets, GitHub como destino de datos, IA ni salidas externas.

## Condición previa para uso futuro

Antes de copiar esta ficha a un documento futuro, se debe verificar manualmente que G-SEC-2 y la plantilla de tarjeta continúan en `Review`, que G-SEC-2.1a, 2.2a, 2.3a y 2.4a siguen documentados como PASS sintéticos y que no existe un cambio de alcance pendiente. La copia futura debe residir bajo almacenamiento local LUKS; GitHub contiene solamente esta referencia vacía y documentos de política.

Si cualquiera de esas condiciones no se cumple, el resultado es `consent_scope_mismatch`. Se detiene el proceso sin abrir información privada, sin llenar una tarjeta y sin pedir una aprobación.

## Ficha pública mínima — referencia vacía

Las celdas `[PENDIENTE — no emitir]` no se completan en este documento ni en conversación. Su valor futuro, si existe un gate que lo permita, debe ser público, mínimo, no sensible y suficiente para revisar el alcance sin revelar datos de plataformas.

| Campo | Regla de la ficha futura | Estado de esta referencia |
|---|---|---|
| Referencia pública de propuesta | Identificador único, revisable y no secreto de una sola propuesta. | `[PENDIENTE — no emitir]` |
| Versión de contratos | Referencias exactas de G-SEC-2, plantilla de tarjeta y preflights aplicables. | `[PENDIENTE — no emitir]` |
| Objetivo técnico | Descripción mínima de una sola operación manual read-only; sin datos de cuenta, IDs, URLs o tokens. | `[PENDIENTE — no emitir]` |
| Marca | `Universe Sent Me` únicamente. | `Universe Sent Me` |
| Muestra | Máximo cuatro observaciones, una por plataforma aprobada. | `[PENDIENTE — no emitir]` |
| Métricas | Solo TikTok `views_native`, YouTube `views_native` de período cerrado, Facebook `reactions_native` e Instagram `likes_native`. | `[PENDIENTE — no emitir]` |
| Datos excluidos | Monetización, comentarios, contenido, caption, URL, audiencia, identificadores, raw, evidencia, credenciales y métricas derivadas. | `Excluidos por diseño` |
| Conservación | Máximo 30 días; sin backup ni sincronización. | `30 días máximos` |
| Método | Una ejecución manual, local y read-only. | `[PENDIENTE — no emitir]` |
| Egress e infraestructura | Sin salida externa; sin cron, Docker, OmniRoute, Drive, Sheets, GitHub como destino de datos o IA. | `Prohibidos por diseño` |
| Ventana y revocación | Máximo 24 horas, con revocación posible antes de iniciar o durante preflight. | `[PENDIENTE — no emitir]` |
| Resultado permitido | Estado PASS/BLOCKED agregado y conteos seguros únicamente. | `Solo salida segura` |

## Lista manual de comparación de alcance

Esta lista se llena solamente cuando exista una ficha futura lícita para revisar. La persona que compare debe elegir un resultado por fila: `Compatible`, `No compatible` o `No declarado`. Cualquier resultado distinto de `Compatible` bloquea el avance; no se “corrige” improvisando y no se solicita consentimiento.

| Control de comparación | Límite innegociable | Resultado futuro | Razón mínima no sensible |
|---|---|---|---|
| Referencia | Una propuesta pública identificable y sin secretos. | `[PENDIENTE — no comparar]` | `[PENDIENTE — no comparar]` |
| Marca | Universe Sent Me únicamente. | `[PENDIENTE — no comparar]` | `[PENDIENTE — no comparar]` |
| Muestra | Hasta cuatro observaciones, una por plataforma. | `[PENDIENTE — no comparar]` | `[PENDIENTE — no comparar]` |
| Métricas | Solo las cuatro métricas nativas no financieras definidas. | `[PENDIENTE — no comparar]` | `[PENDIENTE — no comparar]` |
| Exclusiones | Ningún dato de texto, audiencia, ID, raw, evidencia o credencial. | `[PENDIENTE — no comparar]` | `[PENDIENTE — no comparar]` |
| Retención | Máximo 30 días, sin extensión/backup automático. | `[PENDIENTE — no comparar]` | `[PENDIENTE — no comparar]` |
| Método | Una sola operación manual, local, read-only. | `[PENDIENTE — no comparar]` | `[PENDIENTE — no comparar]` |
| Egress | Ningún destino externo o infraestructura prohibida. | `[PENDIENTE — no comparar]` | `[PENDIENTE — no comparar]` |
| Vigencia | Hasta 24 horas y revocable. | `[PENDIENTE — no comparar]` | `[PENDIENTE — no comparar]` |
| Salida | Solo estado agregado y conteos seguros. | `[PENDIENTE — no comparar]` | `[PENDIENTE — no comparar]` |

## Dictamen manual y manejo de discrepancias

Una ficha futura solo puede declararse `scope_compatible_for_separate_human_request` cuando las diez filas de comparación sean `Compatible`, no haya campos sensibles y la propuesta no incluya instrucciones de ejecución. Este dictamen no emite una tarjeta, no registra consentimiento y no permite ejecutar preflight ni collectors.

El dictamen `consent_scope_mismatch` es obligatorio cuando falte un campo, se exceda un límite, aparezca un dato excluido, exista cualquier salida externa, se pretenda automatizar o el período de retención sea ambiguo. En ese caso se archiva solo el dictamen mínimo bajo LUKS si un gate posterior lo permite; no se guarda en GitHub, no se realiza reparación automática y no se intenta completar una tarjeta.

## Secuencia humana futura

| Etapa | Acción permitida | Resultado | Prohibición continua |
|---|---|---|---|
| 1. Preparar ficha | Copiar esta referencia y describir el alcance público mínimo. | Ficha futura sin tarjeta ni aprobación. | No incluir datos reales, secretos o IDs. |
| 2. Comparar | Completar manualmente las diez filas contra G-SEC-2. | `Compatible` o `consent_scope_mismatch`. | No abrir configuraciones ni ejecutar un preflight. |
| 3. Diseñar tarjeta | Solo si las diez filas son compatibles y un gate separado lo permite. | Tarjeta aún no emitida. | No solicitar consentimiento ni ejecutar operación. |
| 4. Solicitud posterior | Requiere un gate y una conversación nuevos. | Decisión humana puntual. | Esta ficha no reemplaza la tarjeta ni el consentimiento. |

## Estado y siguiente gate permitido

### Registro de revisión humana — 2026-08-27

Fernando confirmó que comprende esta ficha pública vacía y sus diez controles de comparación. Por ello, el estado documental cambia de `Draft` a `Review`. La confirmación revisa exclusivamente la estructura, los límites y el criterio de bloqueo; no completa ningún campo `[PENDIENTE — no emitir]` o `[PENDIENTE — no comparar]`, no emite una propuesta o tarjeta, no solicita ni registra consentimiento y no autoriza una operación.

G-SEC-2.5 validó estáticamente los marcadores pendientes, enlaces y los diez controles de comparación frente a G-SEC-2 y la plantilla de tarjeta. G-SEC-2.6 consolidó las diez comprobaciones públicas como `Compatible`. Estos resultados, junto con esta revisión, mantienen G-SEC-2 en `Review` y G-NORM-4R bloqueado.

El procedimiento preliminar `2026-08-27_Procedimiento_Preliminar_Propuesta_Minima_GSEC2_4c_USM.md` v1.5 fue revisado de manera humana independiente y está en `Review`. El gate `2026-08-27_Gate_Diseno_Propuesta_Hipotetica_Unica_GSEC2_4cP1_USM.md` v1.3 también fue revisado y está en `Review`; delimita una futura propuesta hipotética sin crearla. G-SEC-2.4c-P.2 y su formato vacío recibieron su revisión humana y están en `Review`, conservando todos los campos sin instancia concreta. No se deben copiar ni completar esta ficha, emitir una tarjeta, solicitar consentimiento, abrir datos o rutas privadas, invocar collectors, OAuth/API, ledger, cron, Docker, OmniRoute, Drive, Sheets, GitHub como destino de datos, IA o salidas externas. Cualquier continuación requiere un gate documental nuevo y autorizado.

## Referencias

[1] [Plantilla de tarjeta de consentimiento puntual](2026-08-27_Plantilla_Tarjeta_Consentimiento_Puntual_USM.md)

[2] [Contrato G-SEC-2](2026-08-25_Consentimiento_Piloto_Real_Shadow_Ledger_USM.md)

[3] [Plan de cifrado local y G-NORM-4R](2026-08-25_Plan_Decision_Cifrado_Local_G-NORM-4R.md)
