---
title: "G-SEC-2.4c-P.2 — Gate para el formato vacío de propuesta hipotética — Universe Sent Me"
purpose: "Definir el control documental que permite diseñar y revisar un formato completamente vacío para una futura propuesta hipotética de una sola operación, sin crear una instancia, emitir tarjeta, solicitar consentimiento ni habilitar ejecución."
status: Review
created: 2026-08-27
updated: 2026-08-27
version: "1.3"
author: "Manus AI"
related_documents:
  - "Operations/Automation/2026-08-27_Gate_Auditoria_Trazabilidad_Local_Formato_Vacio_GSEC2_4cP3_USM.md"
  - "Operations/Automation/2026-08-27_Formato_Vacio_Propuesta_Hipotetica_Unica_GSEC2_4cP2_USM.md"
  - "Operations/Automation/2026-08-27_Gate_Diseno_Propuesta_Hipotetica_Unica_GSEC2_4cP1_USM.md"
  - "Operations/Automation/2026-08-27_Procedimiento_Preliminar_Propuesta_Minima_GSEC2_4c_USM.md"
  - "Operations/Automation/2026-08-27_Ficha_Propuesta_Minima_Comparacion_Alcance_USM.md"
  - "Operations/Automation/2026-08-27_Plantilla_Tarjeta_Consentimiento_Puntual_USM.md"
  - "Operations/Automation/2026-08-25_Consentimiento_Piloto_Real_Shadow_Ledger_USM.md"
  - "GrowthOS/todo.md"
organization: "Operations/Automation"
---

# G-SEC-2.4c-P.2 — Gate para el formato vacío de propuesta hipotética

## Propósito y límite decisivo

**G-SEC-2.4c-P.2** define cómo diseñar un formato vacío que, en un futuro y solo bajo gates adicionales, serviría para estructurar una propuesta hipotética de una sola operación. El resultado de este gate es una referencia de campos bloqueados; no es una propuesta y no permite generar una copia para rellenar.

> **Límite decisivo:** el gate y su formato vacío no contienen una instancia de propuesta. No incluyen referencia, finalidad, fecha, muestra, plataforma seleccionada, métrica seleccionada, vigencia, resultado, tarjeta o consentimiento.

Solo pueden revisarse documentos públicos de política y sus estados. Están excluidos datos de plataformas, métricas, valores, cuentas, contenido, IDs, URLs, evidencia, tokens, configuraciones, rutas privadas y logs.

## Condiciones previas de diseño

El gate solo se considera coherente si G-SEC-2, G-SEC-2.4c, G-SEC-2.4c-P y G-SEC-2.4c-P.1 siguen en `Review`, las plantillas conservan sus marcadores vacíos y G-SEC-2.6 conserva su consolidación documental. Esta comprobación es textual y documental; no abre recursos privados ni ejecuta validadores.

| Condición | Estado requerido | Efecto si falta o es ambiguo |
|---|---|---|
| Contrato G-SEC-2 | `Review` | `consent_scope_mismatch`. |
| Ficha, procedimiento y gate P.1 | `Review`, sin instancias emitidas | `consent_scope_mismatch`. |
| Plantilla de tarjeta | `Review`, vacía | `consent_scope_mismatch`. |
| Formato de este gate | Todos los campos con marcador de no emisión | `consent_scope_mismatch`. |
| Datos e integraciones | No usados ni referenciados con detalle | `consent_scope_mismatch`. |

## Diseño permitido del formato vacío

El formato puede nombrar únicamente **categorías de campo**, reglas fijas y marcadores de no emisión. Cada celda variable debe permanecer vacía con un marcador explícito. Los límites permanentes se expresan como reglas de política, no como selección de una operación.

| Elemento del formato | Diseño permitido | Diseño prohibido |
|---|---|---|
| Identificación | Etiqueta de campo y marcador vacío. | Referencia, ID, fecha, nombre de operación o titular. |
| Alcance | Regla de una operación hipotética y marca USM únicamente. | Objetivo concreto, cuenta, plataforma activa o lote. |
| Muestra y métricas | Límites máximos y conjunto permitido como política. | Cantidad, plataforma o métrica seleccionadas. |
| Retención y método | Reglas de máximo 30 días y modo manual/local/read-only. | Calendario, ejecución, script, preflight o tarea programada. |
| Egress y salida | Prohibición de destinos externos y regla de salida agregada segura. | Destino, valor, fila, ID, ruta, hash o evidencia. |
| Vigencia y revocación | Máximo de 24 horas y revocabilidad como norma futura. | Hora, fecha, firma, decisión o consentimiento vigente. |

## Controles de preservación del vacío

La revisión futura de este gate deberá comprobar los controles siguientes sin rellenar el formato. Cualquier resultado distinto de `Compatible` detiene el flujo y no permite corregir el contenido durante la misma revisión.

| Control | Criterio de `Compatible` | Bloqueo |
|---|---|---|
| Marcadores | Todos los campos variables indican `[PENDIENTE — no emitir]`. | Un valor, ejemplo operativo o selección concreta. |
| Operación única | Solo se describe el límite de una operación hipotética. | Lote, repetición, automatización o ejecución. |
| Datos excluidos | No aparecen datos, valores, IDs, URLs, cuentas, tokens o evidencia. | Cualquier dato privado o identificable. |
| Límites G-SEC-2 | Se mantienen marca, cuatro observaciones, métricas no financieras, 30 días, read-only, no egress y 24 horas. | Falta, ampliación o ambigüedad de un límite. |
| Separación documental | Formato público de política, sin instancia de propuesta. | Copia rellenable, tarjeta o consentimiento. |
| Próxima etapa | Requiere gate y autorización nuevos. | Tratar este diseño como permiso de creación o ejecución. |

## Autorizaciones estrictamente separadas

| Etapa | Autorización requerida | Resultado máximo |
|---|---|---|
| Diseñar G-SEC-2.4c-P.2 | Solicitud documental específica. | Gate y formato vacío en `Draft`. |
| Revisar G-SEC-2.4c-P.2 | Confirmación humana independiente. | Gate y formato vacío en `Review`. |
| Diseñar una eventual instancia hipotética | Un gate posterior adicional, explícito y documental. | Diseño de instancia, no emisión. |
| Comparar una eventual instancia | Autorización nueva para los diez controles. | Dictamen de alcance, sin tarjeta. |
| Solicitar consentimiento | Gate y tarjeta completos posteriores. | Decisión humana puntual, nunca automática. |

Las aprobaciones de etapas anteriores no son transferibles. Un PASS sintético, una revisión de política, la existencia de LUKS o la aprobación de este gate no equivalen a permiso para crear o completar una propuesta.

## Prohibiciones permanentes

G-SEC-2.4c-P.2 no ejecuta scripts, preflights o validadores; no abre sockets, rutas privadas, variables de entorno, collectors, OAuth/API, ledger, cron, Docker, OmniRoute, IA o servicios. No usa Drive, Sheets, GitHub, correo, mensajería ni otra salida externa como destino de datos. Tampoco crea archivos temporales con datos ni modifica la ficha o la tarjeta.

## Estado y siguiente acción permitida

### Registro de revisión humana — 2026-08-27

Fernando confirmó el gate, el formato vacío, sus marcadores, límites fijos, separación documental y condiciones de detención. El estado de este gate cambia de `Draft` a `Review`. La revisión se limita al diseño: no crea una instancia, no completa la ficha, no emite tarjeta, no solicita o registra consentimiento y no autoriza una operación.

El formato relacionado recibió la misma revisión independiente y también cambia a `Review`, conservando todos sus campos variables como `[PENDIENTE — no emitir]`. G-SEC-2 permanece en `Review` y G-NORM-4R continúa bloqueado. No se abrió información privada, red, collectors, OAuth/API, ledger, cron, Docker, OmniRoute, Drive, Sheets, GitHub como destino de datos, IA o salida externa.

El gate G-SEC-2.4c-P.3 recibió su revisión humana independiente como `Review` en `2026-08-27_Gate_Auditoria_Trazabilidad_Local_Formato_Vacio_GSEC2_4cP3_USM.md` v1.1. Fija reglas de auditoría y trazabilidad local de política sin crear un ledger o una instancia. Cualquier continuación requiere un gate y autorización nuevos; no se puede crear, copiar o completar una propuesta, tarjeta, vigencia o solicitud de consentimiento.

## Referencias

[1] [Formato vacío de propuesta hipotética](2026-08-27_Formato_Vacio_Propuesta_Hipotetica_Unica_GSEC2_4cP2_USM.md)

[2] [Gate de diseño G-SEC-2.4c-P.1](2026-08-27_Gate_Diseno_Propuesta_Hipotetica_Unica_GSEC2_4cP1_USM.md)

[3] [Procedimiento preliminar G-SEC-2.4c-P](2026-08-27_Procedimiento_Preliminar_Propuesta_Minima_GSEC2_4c_USM.md)

[4] [Ficha pública de propuesta mínima](2026-08-27_Ficha_Propuesta_Minima_Comparacion_Alcance_USM.md)

[5] [Contrato G-SEC-2](2026-08-25_Consentimiento_Piloto_Real_Shadow_Ledger_USM.md)
