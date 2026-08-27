---
title: "Propuesta real mínima de una sola operación G-SEC-2.4c — Universe Sent Me"
purpose: "Describir una única operación real hipotética y mínima para recibir métricas nativas no financieras, de forma manual, local y read-only, sin emitir consentimiento ni habilitar datos."
status: Review
created: 2026-08-27
updated: 2026-08-27
version: "1.1"
author: "Manus AI"
related_documents:
  - "Operations/Automation/2026-08-27_Ficha_Propuesta_Minima_Comparacion_Alcance_USM.md"
  - "Operations/Automation/2026-08-27_Procedimiento_Preliminar_Propuesta_Minima_GSEC2_4c_USM.md"
  - "Operations/Automation/2026-08-27_Gate_Diseno_Propuesta_Hipotetica_Unica_GSEC2_4cP1_USM.md"
  - "Operations/Automation/2026-08-27_Gate_Formato_Vacio_Propuesta_Hipotetica_GSEC2_4cP2_USM.md"
  - "Operations/Automation/2026-08-27_Gate_Auditoria_Trazabilidad_Local_Formato_Vacio_GSEC2_4cP3_USM.md"
  - "Operations/Automation/2026-08-27_Gate_Seguridad_Restriccion_Red_Formato_Vacio_GSEC2_4cP4_USM.md"
  - "Operations/Automation/2026-08-27_Gate_Cierre_Archivado_Ciclo_Preliminar_GSEC2_4cP5_USM.md"
  - "Operations/Automation/2026-08-27_Plantilla_Tarjeta_Consentimiento_Puntual_USM.md"
  - "Operations/Automation/2026-08-25_Consentimiento_Piloto_Real_Shadow_Ledger_USM.md"
  - "Operations/Automation/2026-08-27_Interfaz_Invocacion_Sintetica_Minima_GSEC2_11_USM.md"
  - "Operations/Automation/2026-08-27_Runner_Sintetico_Estandar_GSEC2_11_USM.md"
  - "GrowthOS/todo.md"
organization: "Operations/Automation"
---

# Propuesta real mínima de una sola operación G-SEC-2.4c

## Propósito y estado

Este documento convierte la referencia pública vacía de comparación en una **propuesta concreta todavía no emitida**. Su función es permitir una revisión humana del alcance antes de preparar una tarjeta de consentimiento puntual. No es consentimiento, no es una orden de ejecución, no es un permiso OAuth/API y no habilita collectors, red, datos reales, shadow ledger ni G-NORM-4R.

El documento permanece en estado **Review** después de la revisión humana independiente del alcance y de los diez controles. Ningún campo de consentimiento se completa con este documento y ninguna persona puede interpretarlo como autorización para iniciar una lectura.

> **Regla de frontera:** diseñar el alcance no equivale a aprobar el tratamiento. La propuesta debe conservar una tarjeta de consentimiento separada y una autorización independiente antes de que pueda considerarse una operación real.

## Identificación pública de la propuesta

| Campo | Propuesta revisada | Límite
|---|---|---|
| Referencia | `USM-GSEC2-4C-PREAL-20260827-01` | Identificador documental no secreto; no es un ID de cuenta ni de plataforma. |
| Marca | `Universe Sent Me` | Se excluyen Bam in a Can, Firma Bordados, clientes y cuentas ajenas. |
| Finalidad única | Verificar la cobertura mínima de métricas nativas y la integridad del flujo read-only para una sola ventana cerrada. | No permite análisis editorial, ranking, recomendaciones, perfiles ni inferencias. |
| Tipo de operación | Una lectura manual local, única y read-only, posterior a consentimiento puntual. | No permite repetición, lote, scheduler, automatización o ejecución en segundo plano. |
| Estado | `Draft — no emitir` | Requiere revisión humana antes de diseñar la tarjeta. |

## Muestra y métricas propuestas

La muestra máxima es de **cuatro observaciones**, una por cada plataforma aprobada. La propuesta no fija todavía cuentas, IDs, URLs, fechas concretas ni valores; esos elementos solo podrían definirse en una tarjeta posterior si la propuesta pasa todos los controles y se obtiene consentimiento vigente.

| Plataforma | Una observación propuesta | Campo nativo mínimo | Condición de alcance |
|---|---:|---|---|
| TikTok | 1 | `views_native` | Solo contenido de Universe Sent Me y solo una ventana cerrada. |
| YouTube | 1 | `views_native` de período cerrado | No incluye monetización ni campos de audiencia. |
| Facebook | 1 | `reactions_native` | No incluye comentarios, shares, texto o perfiles. |
| Instagram | 1 | `likes_native` | No incluye comentarios, shares, saves, views ni perfiles. |

No se mezclarán contadores de vida con métricas de ventana cerrada. Si una plataforma no entrega el campo aprobado o no permite determinar su disponibilidad, el valor se marca como `not_available` y no se sustituye por cero ni se infiere.

## Ventana y frecuencia

La futura operación debe usar una sola ventana temporal cerrada en UTC, definida explícitamente en la tarjeta posterior. La ventana no podrá extenderse durante la ejecución ni reinterpretarse después. La vigencia máxima de la autorización será de 24 horas; la autorización caducará sin ejecución si no se inicia dentro de ese plazo.

La operación no incluirá una segunda pasada, reintento, comparación histórica, actualización incremental ni consulta de recuperación. Cualquier ambigüedad sobre fechas, zona horaria, cuenta, métrica o disponibilidad producirá `consent_scope_mismatch` y detendrá el proceso.

## Datos permitidos y excluidos

| Categoría | Tratamiento propuesto | Regla
|---|---|---|
| Observación nativa mínima | Solo el campo aprobado de cada plataforma, su disponibilidad, ventana, procedencia y versión de contrato. | Máximo cuatro observaciones. |
| Evidencia fuente | Solo lectura temporal local si un gate operativo posterior la permite. | Nunca GitHub, Drive, Sheets, OmniRoute, IA, correo o navegador compartido. |
| Identificadores | Solo el mínimo indispensable para formar la llave de observación; no se muestra en salida. | No IDs completos, handles, URLs, captions o títulos. |
| Credenciales | Ninguna en la propuesta ni en la salida. | No imprimir, copiar, registrar o compartir tokens, cookies, secretos o códigos. |
| Contenido y personas | Excluidos completamente. | No captions, comentarios, perfiles, audiencias, nombres o información personal. |
| Monetización | Excluida completamente. | No ingresos, RPM, anuncios o métricas financieras. |

## Método y salida prevista

Si una tarjeta posterior lo autorizara, el método sería una lectura manual, local, estrictamente read-only, usando únicamente los scopes ya aprobados para las cuentas de Universe Sent Me. La propuesta no autoriza comprobar si esos scopes o tokens siguen vigentes.

La salida permitida sería un resumen seguro con estado agregado, cantidad de observaciones y disponibilidad de campos. No se mostrarían valores crudos, IDs, URLs, texto, rutas privadas, tokens, errores sensibles ni evidencia fuente. La salida tampoco se enviaría a un destino externo.

El almacenamiento temporal y cualquier observación real quedarían sujetos a la confirmación independiente de G-NORM-4R. La retención propuesta sería de un máximo de 30 días desde cada captura, sin backup ni sincronización; la propuesta por sí sola no crea archivos ni un ledger persistente.

## Comparación preliminar contra los diez controles

Esta tabla registra el dictamen documental de la revisión humana independiente. No es un PASS operativo ni sustituye los gates posteriores.

| Control | Compromiso de esta propuesta | Estado revisado | Condición posterior |
|---|---|---|---|
| Referencia | Identificador público único, sin secretos. | Declarado | `Compatible` — diseño |
| Marca | Solo Universe Sent Me. | Declarado | `Compatible` — diseño |
| Muestra | Máximo cuatro observaciones, una por plataforma. | Declarado | `Compatible` — diseño |
| Métricas | Cuatro campos nativos no financieros definidos. | Declarado | `Compatible` — diseño |
| Exclusiones | Sin contenido, personas, IDs expuestos, raw, evidencia o credenciales. | Declarado | `Compatible` — diseño |
| Retención | Máximo 30 días, sin extensión, backup ni sincronización. | Propuesto | `Compatible` — sujeto a G-NORM-4R |
| Método | Una operación manual local read-only. | Propuesto | `Compatible` — sujeto a gate operativo |
| Egress | Ningún destino externo. | Declarado | `Compatible` — diseño |
| Vigencia | Máximo 24 horas y revocable. | Propuesto | `Compatible` — sujeto a tarjeta posterior |
| Salida | Estado agregado y conteos seguros. | Declarado | `Compatible` — sujeto a validar implementación |

Las diez filas fueron revisadas como compatibles en el plano documental, con las condiciones explícitas indicadas para retención, método, vigencia y salida. Este dictamen no equivale a un PASS operativo: si en una etapa posterior no se puede cumplir cualquiera de esas condiciones, el resultado obligatorio será `consent_scope_mismatch` y no se completará una tarjeta.

## Condiciones de detención

La propuesta debe detenerse antes de cualquier contacto con una plataforma si aparece una marca distinta, una métrica adicional, una cuenta no identificada, una ventana abierta, una necesidad financiera, un scope no aprobado, una salida externa, una solicitud de raw, una necesidad de automatización o una ambigüedad sobre la retención.

También debe detenerse si la tarjeta de consentimiento no coincide exactamente con esta referencia, si la autorización no es puntual, si revoca una finalidad distinta o si el estado de G-SEC-2, G-NORM-4R o los gates operativos relacionados cambia inesperadamente.

## Qué no autoriza este documento

Este documento en `Review` no autoriza recibir métricas, abrir archivos privados, leer tokens, inspeccionar cuentas, iniciar OAuth, llamar APIs, ejecutar collectors, revisar procesos, activar OmniRoute, crear cron, escribir el shadow ledger, guardar datos en GitHub o Drive, generar hojas derivadas, enviar información a IA ni modificar las políticas aprobadas.

El dictamen confirma compatibilidad documental para una solicitud humana separada, pero no compatibilidad operativa definitiva. La tarjeta posterior puede solicitar consentimiento solo dentro de su propio gate; únicamente gates posteriores pueden autorizar una operación real.

## Registro de revisión humana independiente — 2026-08-27

Fernando revisó la propuesta `USM-GSEC2-4C-PREAL-20260827-01` y sus diez controles de comparación. El dictamen documental es `scope_compatible_for_separate_human_request`: la finalidad, marca, muestra, métricas, exclusiones, egress y salida son compatibles con el diseño; retención, método y vigencia quedan expresamente sujetos a sus gates posteriores. No se detectaron ambigüedades que obliguen a bloquear la propuesta en esta fase.

La revisión cambia el estado de `Draft` a `Review`. No completa fechas, cuentas, IDs, URLs, valores de métricas ni credenciales; no emite la tarjeta de consentimiento, no solicita aprobación para una operación, no abre datos y no autoriza collectors.

## Estado y siguiente acción permitida

La propuesta se encuentra en `Review`. La siguiente acción permitida es preparar o revisar una tarjeta de consentimiento puntual separada, sin emitirla todavía, o detenerse si cambia el alcance. Antes de cualquier contacto con una plataforma deberán cumplirse los gates operativos y obtenerse consentimiento vigente para una única ventana.

G-SEC-2 permanece en `Review`, G-NORM-4R permanece bloqueado y no se habilita ninguna métrica real mediante este documento.

## Referencias

[1] [Ficha pública de propuesta mínima y comparación manual de alcance](2026-08-27_Ficha_Propuesta_Minima_Comparacion_Alcance_USM.md)

[2] [Procedimiento preliminar de propuesta mínima G-SEC-2.4c](2026-08-27_Procedimiento_Preliminar_Propuesta_Minima_GSEC2_4c_USM.md)

[3] [Plantilla de tarjeta de consentimiento puntual](2026-08-27_Plantilla_Tarjeta_Consentimiento_Puntual_USM.md)

[4] [Contrato G-SEC-2](2026-08-25_Consentimiento_Piloto_Real_Shadow_Ledger_USM.md)

[5] [Interfaz de invocación sintética mínima G-SEC-2.11](2026-08-27_Interfaz_Invocacion_Sintetica_Minima_GSEC2_11_USM.md)
