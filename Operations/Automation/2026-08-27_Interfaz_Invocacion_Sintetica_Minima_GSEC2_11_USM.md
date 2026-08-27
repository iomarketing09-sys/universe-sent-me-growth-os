---
title: "Interfaz de invocación sintética mínima G-SEC-2.11 — Universe Sent Me"
purpose: "Definir la interfaz documental, pública y no ejecutable para una única llamada sintética y efímera al runner G-SEC-2.11, sin crear código, importar módulos, registrar nombres reales ni analizar el sistema."
status: Draft
created: 2026-08-27
updated: 2026-08-27
version: "1.0"
author: "Manus AI"
related_documents:
  - "Operations/Automation/2026-08-27_Runner_Sintetico_Estandar_GSEC2_11_USM.md"
  - "Operations/Automation/2026-08-27_Implementacion_Nucleo_Politica_Publico_GSEC2_11_USM.md"
  - "Operations/Automation/2026-08-27_Contrato_Artefacto_Codigo_Publico_Verificador_Minimo_GSEC2_11_USM.md"
  - "Operations/Automation/2026-08-27_Especificacion_Estatica_Verificador_Minimo_GSEC2_11_USM.md"
  - "Operations/Automation/2026-08-27_Gate_Tecnico_Pasivo_Observacion_Real_Minima_GSEC2_11_USM.md"
  - "GrowthOS/todo.md"
organization: "Operations/Automation"
---

# Interfaz de invocación sintética mínima G-SEC-2.11

## Propósito y frontera

Esta interfaz resuelve solamente el bloqueo documental de invocación del runner sintético estándar. Define cómo tendría que autorizarse y reducirse una futura **llamada única, local y efímera** a los cinco casos abstractos ya revisados. No define un comando, un wrapper, un archivo de código, una CLI ni una interfaz del sistema.

> **Frontera decisiva:** la interfaz recibe cero datos reales y no recibe nombres de componentes. Su conjunto de casos está cerrado y no admite parámetros, selección parcial, banderas, rutas, variables de entorno, destinos de salida ni detalles técnicos.

Mientras esté en `Draft`, no existe una forma aprobada de importar o ejecutar el runner.

## Solicitud conceptual cerrada

Una futura solicitud de invocación deberá referirse exactamente a este contrato y a los cinco casos ya definidos. No se permite agregar, omitir, ordenar de forma distinta ni reemplazar casos durante la solicitud.

| Campo conceptual | Valor permitido | Rechazo fail-closed |
|---|---|---|
| `purpose` | `validate_synthetic_policy_core_only` | Cualquier objetivo de observación, diagnóstico, collector o métrica. |
| `case_set` | Los cinco casos abstractos declarados por el runner en `Review`. | Selección parcial, nuevo caso o entrada proporcionada por el operador. |
| `run_count` | `1` | Reintento, bucle, monitorización, programación o concurrencia. |
| `data_class` | `synthetic_abstract_in_memory` | Nombres reales, rutas, PIDs, servicios, collectors, métricas, tokens o evidencia. |
| `result_scope` | Una categoría agregada efímera de suite. | Resultado por caso, detalles, consola extendida, log, archivo, red o destino externo. |

La solicitud humana deberá confirmar expresamente que se conserva este conjunto cerrado y que el resultado desaparece al terminar la sesión. No puede reutilizarse como consentimiento general para pruebas, código o datos de USM.

## Precondiciones de una futura llamada

La llamada no comenzará si falta cualquiera de estas condiciones. La comprobación de precondiciones será parte de una futura interfaz revisada, no de este documento.

| Precondición | Criterio documental | Si falta |
|---|---|---|
| Documentos revisados | G-SEC-2.11, especificación, contrato, implementación y runner permanecen en `Review`. | `synthetic_invocation_blocked`. |
| Autorización puntual | Fernando aprueba una sola ejecución de los cinco casos, con esta interfaz exacta. | `synthetic_invocation_blocked`. |
| Runner sin cambios | La revisión estática continúa aplicando al archivo público. | `synthetic_invocation_blocked`. |
| Entorno sin ampliación | No se requiere instalar software, añadir imports, crear archivos o exponer una CLI. | `synthetic_invocation_blocked`. |
| Resultado efímero | Se puede reducir a una sola categoría sin persistir datos. | `synthetic_invocation_blocked`. |

## Resultado único permitido

Una futura interfaz podrá comunicar una sola categoría de suite; no puede revelar el resultado individual de los cinco casos.

| Resultado | Significado limitado | No significa |
|---|---|---|
| `synthetic_policy_suite_passed` | Los cinco casos abstractos completaron el criterio declarado en memoria. | Que el núcleo sea seguro en producción o que el sistema real esté inactivo. |
| `synthetic_policy_suite_blocked` | Falta una precondición, existe cambio no revisado o no se puede preservar la ejecución efímera. | Que pueda reintentarse, depurarse o modificar código automáticamente. |
| `synthetic_policy_suite_failed` | Un caso abstracto no alcanza la expectativa declarada. | Que se conozca la causa o que pueda corregirse sin un diseño y autorización nuevos. |

No se permite una salida `PASS` sobre servicios, collectors, API, red, LUKS, datos, privacidad, retención, consentimiento real o G-NORM-4R.

## Límites obligatorios de la futura interfaz

La interfaz futura deberá ser de propósito único, sin parámetros provenientes del usuario y sin capacidades de descubrimiento. Su única tarea sería convocar el runner ya revisado una vez y reducir su resultado en memoria.

| Categoría | Permitido | Prohibido |
|---|---|---|
| Código | Una interfaz pública nueva solo tras diseño, revisión y autorización separados. | Modificar el núcleo o runner actual durante la invocación. |
| Ejecución | Una llamada local y única tras autorización puntual futura. | Importación ad hoc, CLI no revisada, bucles, reintentos, scheduler o ejecución de fondo. |
| Datos | Los cinco valores abstractos ya declarados. | Nombres reales, argumentos, rutas, configuración, secretos, métricas o evidencia. |
| E/S y red | Ninguna persistencia o salida externa. | Archivos, logs, cachés, consola detallada, red, sockets, APIs, Drive, Sheets o GitHub. |
| Sistema | Ninguna consulta de componentes. | Procesos, servicios, collectors, puertos, Docker, OmniRoute, entorno o rutas privadas. |

## Condiciones de detención fail-closed

La interfaz futura deberá detenerse antes de importar el runner si detecta un cambio de versión no revisado, una solicitud de caso adicional, una salida no efímera, una dependencia nueva, una necesidad de comando o una capacidad no prevista. No debe interpretar, corregir, reinvocar ni conservar el resultado parcial.

> La respuesta correcta ante cualquier ambigüedad es `synthetic_policy_suite_blocked`. No hay fallback hacia `pytest`, un intérprete alternativo, un wrapper improvisado ni una comprobación del sistema.

## Estado y siguiente acción permitida

Esta interfaz está en `Draft`. La siguiente acción permitida es una revisión humana independiente de este contrato: conjunto cerrado, precondiciones, resultado único, límites y detención fail-closed. Esa revisión solo podría cambiar este documento a `Review`; no crearía una interfaz de código, no importaría el runner y no ejecutaría los casos.

## Referencias

[1] [Runner sintético estándar G-SEC-2.11](2026-08-27_Runner_Sintetico_Estandar_GSEC2_11_USM.md)

[2] [Implementación del núcleo de política público G-SEC-2.11](2026-08-27_Implementacion_Nucleo_Politica_Publico_GSEC2_11_USM.md)

[3] [Contrato de código público G-SEC-2.11](2026-08-27_Contrato_Artefacto_Codigo_Publico_Verificador_Minimo_GSEC2_11_USM.md)
