---
title: "Tarjeta de consentimiento puntual en Review — USM-GSEC2-4C-PREAL-20260827-01"
purpose: "Preparar, sin emitir, una tarjeta de consentimiento granular para una única operación manual read-only de Universe Sent Me, con ventana UTC y cuentas objetivo exactas."
status: Review
created: 2026-08-27
updated: 2026-08-27
version: "1.2"
author: "Manus AI"
related_documents:
  - "Operations/Automation/2026-08-27_Propuesta_Real_Minima_Una_Operacion_GSEC2_4c_USM.md"
  - "Operations/Automation/2026-08-27_Plantilla_Tarjeta_Consentimiento_Puntual_USM.md"
  - "Operations/Automation/2026-08-25_Consentimiento_Piloto_Real_Shadow_Ledger_USM.md"
  - "Operations/Automation/2026-08-27_Gate_Seguridad_Restriccion_Red_Formato_Vacio_GSEC2_4cP4_USM.md"
  - "Operations/Automation/2026-08-27_Gate_Cierre_Archivado_Ciclo_Preliminar_GSEC2_4cP5_USM.md"
  - "GrowthOS/todo.md"
organization: "Operations/Automation"
---

# Tarjeta de consentimiento puntual en Review

## Estado y frontera

Esta tarjeta es una **preparación documental en estado `Review`**. La revisión humana independiente confirmó la coherencia documental de su alcance, ventana UTC, cuentas objetivo y controles. **No es consentimiento, no ha sido presentada para aprobación y no autoriza ninguna operación.**

No se deben abrir datos, leer tokens, iniciar OAuth, llamar APIs, ejecutar collectors, comprobar vigencia de credenciales, crear evidencia real o escribir un ledger. G-SEC-2 permanece en `Review` y G-NORM-4R continúa bloqueado.

> La tarjeta no puede interpretarse como aprobada por el hecho de contener cuentas, fechas o una frase de solicitud. La aprobación humana debe emitirse después, de forma separada, inequívoca y únicamente para esta tarjeta exacta.

## Identificación de la solicitud futura

| Campo | Valor revisado | Estado |
|---|---|---|
| Referencia de propuesta | `USM-GSEC2-4C-PREAL-20260827-01` | Coincide con la propuesta en `Review`. |
| Referencia de tarjeta | `USM-CONSENT-20260827-01` | Identificador de esta tarjeta; no es un permiso. |
| Marca | `Universe Sent Me` | Alcance exclusivo. |
| Tipo de operación | Una lectura manual local estrictamente read-only | Pendiente de gates operativos. |
| Consentimiento | No emitido | `PENDING — NO SOLICITADO` |
| Operador | Fernando / Manus | La identidad no sustituye la aprobación. |

## Ventana UTC única

La ventana candidata queda fijada de forma cerrada para una futura solicitud:

| Campo | Valor exacto |
|---|---|
| Inicio UTC | `2026-08-28T00:00:00Z` |
| Fin UTC | `2026-08-28T23:59:59Z` |
| Duración máxima | 24 horas menos un segundo |
| Regla temporal | No se permiten extensiones, ventanas abiertas, reintentos ni segunda pasada. |
| Caducidad | Si no existe aprobación válida antes de iniciar, la tarjeta no puede utilizarse. |
| Revocación | Puede revocarse antes del inicio o durante el preflight; la revocación bloquea la operación. |

La ventana expresa el período de publicación/observación candidato, no una orden para consultar plataformas. Cualquier diferencia de zona horaria, fecha, inicio o fin obliga a detenerse con `consent_scope_mismatch`.

## Cuentas exactas y observación máxima

La operación candidata se limita a una observación por cada cuenta pública objetivo. Los identificadores siguientes solo fijan el alcance documental; no se han consultado ni validado durante la redacción de esta tarjeta.

| Plataforma | Cuenta objetivo exacta | Observación máxima | Métrica permitida |
|---|---|---:|---|
| TikTok | usuario `universe.sent.me` | 1 | `views_native` |
| YouTube | canal `@Universe_Sent_Me` | 1 | `views_native` del período cerrado |
| Facebook | Página con ID público `1036844829507460` de Universe Sent Me | 1 | `reactions_native` |
| Instagram | cuenta `@universe_sent_me_0326` | 1 | `likes_native` |

**Total máximo: cuatro observaciones.** No se permite sustituir, añadir, combinar o redirigir ninguna cuenta. En particular, quedan excluidos Bam in a Can, Firma Bordados, cuentas personales, clientes, cuentas ajenas y cualquier cuenta que no coincida exactamente con esta tabla.

## Datos permitidos y exclusiones

Solo se podrían tratar, si una aprobación posterior y los gates operativos lo permiten, el valor de la métrica aprobada, su disponibilidad, la ventana UTC, la procedencia de plataforma y la versión del contrato. No se permiten datos de contenido, captions, títulos, URLs, comentarios, perfiles, audiencias, nombres de personas, identificadores de publicaciones, credenciales, cookies, tokens, valores monetarios o métricas derivadas.

La ausencia de una métrica debe conservarse como `not_available` o `missing`, según el contrato aplicable. Nunca se sustituirá por cero ni se inferirá.

## Método, almacenamiento y salida

La operación candidata sería una única lectura manual, local y read-only. No se permite cron, scheduler, Docker, OmniRoute, ejecución en segundo plano, salida externa, GitHub, Drive, Sheets, IA, correo o mensajería. La evidencia fuente y cualquier observación real solo podrían manejarse bajo un gate operativo posterior y dentro del almacenamiento local protegido por LUKS.

La salida permitida sería exclusivamente un resumen agregado seguro: estado PASS/BLOCKED y conteos sin filas, valores crudos, IDs, URLs, rutas, tokens o evidencia. La retención propuesta es de un máximo de 30 días desde cada captura, sin backup ni sincronización automática, sujeta a G-NORM-4R.

## Checklist de compatibilidad de la tarjeta

| Control | Resultado documental revisado | Condición antes de cualquier operación |
|---|---|---|
| Propuesta de referencia | Compatible en diseño | Mantener la referencia exacta. |
| Marca | Compatible | Confirmar solo Universe Sent Me. |
| Muestra | Compatible | No superar cuatro observaciones. |
| Métricas | Compatible en diseño | No ampliar campos ni convertir ausencias en cero. |
| Exclusiones | Compatible | Bloquear contenido, personas, IDs, raw y credenciales. |
| Retención | Propuesta compatible | Requiere confirmación de G-NORM-4R. |
| Método | Propuesta compatible | Requiere gate read-only operativo. |
| Egress | Compatible | Confirmar cero destinos externos. |
| Vigencia | Propuesta compatible | Confirmar la ventana exacta y revocación. |
| Salida | Propuesta compatible | Validar resumen agregado antes de ejecutar. |

## Texto de aprobación — no emitir

El siguiente texto queda preparado como referencia, pero **no constituye una solicitud activa y no debe interpretarse como consentimiento**:

> Solicitud pendiente, no aprobada: se propone una única lectura manual, local y read-only para Universe Sent Me, limitada a las cuentas TikTok `universe.sent.me`, YouTube `@Universe_Sent_Me`, Facebook Page ID `1036844829507460` e Instagram `@universe_sent_me_0326`, con una observación máxima por cuenta y únicamente las cuatro métricas indicadas en esta tarjeta. La ventana UTC propuesta es `2026-08-28T00:00:00Z` a `2026-08-28T23:59:59Z`. Se excluyen contenido, personas, URLs, IDs de publicaciones, raw, evidencia, credenciales, monetización, métricas derivadas y cualquier salida externa. La conservación candidata es de hasta 30 días, sujeta a G-NORM-4R. La operación no se iniciará sin aprobación explícita de esta tarjeta exacta; puede revocarse antes de iniciar o durante el preflight.

## Reglas de detención

El proceso debe bloquearse si una cuenta no coincide exactamente, si la ventana cambia, si aparece una métrica adicional, si se solicita un dato excluido, si la autorización es genérica, si la tarjeta está vencida o revocada, si falta un gate operativo, si existe cualquier salida externa o si la respuesta humana no repite el alcance esencial.

El estado de bloqueo obligatorio es `consent_scope_mismatch`. No se debe corregir improvisando, ampliar la tarjeta, consultar la plataforma o convertir una aprobación anterior en consentimiento vigente.

## Registro de revisión humana independiente — 2026-08-27

Fernando revisó la tarjeta `USM-CONSENT-20260827-01` contra la propuesta `USM-GSEC2-4C-PREAL-20260827-01` y la plantilla vigente. Confirmó la coincidencia documental de la finalidad, marca, muestra máxima de cuatro observaciones, métricas, exclusiones, retención propuesta, método read-only, egress, ventana UTC, revocación y salida agregada. También confirmó que la ventana `2026-08-28T00:00:00Z`–`2026-08-28T23:59:59Z` y las cuatro cuentas objetivo están fijadas sin permitir sustituciones ni ampliaciones.

El dictamen es `consent_card_scope_compatible_for_separate_approval`. La tarjeta pasa de `Draft` a `Review`, pero no se emite consentimiento ni se autoriza una operación. Las condiciones de retención, método, vigencia y salida siguen sujetas a gates posteriores.

## Aprobación humana puntual recibida — 2026-08-27

Fernando aprobó explícitamente esta tarjeta exacta para continuar únicamente al siguiente gate, repitiendo la referencia, la ventana UTC, las cuatro cuentas y métricas, el límite de una sola operación, la prohibición de egress, la retención máxima de 30 días y la revocación. La aprobación incluyó expresamente: **no ejecutar todavía**.

El alcance de la aprobación queda clasificado como `approved_for_next_gate_only`. No se interpreta como autorización para ejecutar preflight, consultar plataformas, abrir OAuth/API, iniciar collectors, recibir métricas, escribir evidencia o activar G-NORM-4R. La tarjeta conserva las mismas condiciones y no se permite ampliarla.

## Estado y siguiente gate permitido

Esta tarjeta permanece en **`Review`**, con aprobación puntual registrada para continuar al siguiente gate, pero no ha sido emitida como permiso de ejecución. La siguiente acción permitida es preparar el preflight operativo read-only en un documento separado. La preparación no debe combinarse con una lectura de plataforma o una ejecución de collector.

No se ha ejecutado ninguna lectura, no se han consultado cuentas, no se han abierto tokens ni configuraciones y no se ha autorizado todavía la recepción de métricas reales.

## Referencias

[1] [Propuesta real mínima de una sola operación G-SEC-2.4c](2026-08-27_Propuesta_Real_Minima_Una_Operacion_GSEC2_4c_USM.md)

[2] [Plantilla de consentimiento puntual](2026-08-27_Plantilla_Tarjeta_Consentimiento_Puntual_USM.md)

[3] [Contrato G-SEC-2](2026-08-25_Consentimiento_Piloto_Real_Shadow_Ledger_USM.md)

[4] [Gate de seguridad y restricción de red G-SEC-2.4c-P.4](2026-08-27_Gate_Seguridad_Restriccion_Red_Formato_Vacio_GSEC2_4cP4_USM.md)
