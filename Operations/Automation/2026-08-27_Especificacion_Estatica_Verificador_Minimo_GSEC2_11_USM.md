---
title: "Especificación estática del verificador mínimo G-SEC-2.11 — Universe Sent Me"
purpose: "Definir, sin crear código ni ejecutar consultas, la interfaz pública, las precondiciones, el método lógico, las categorías agregadas y la detención fail-closed de un posible verificador local de una sola pasada para G-SEC-2.11."
status: Review
created: 2026-08-27
updated: 2026-08-27
version: "1.7"
author: "Manus AI"
related_documents:
  - "Operations/Automation/2026-08-27_Gate_Tecnico_Pasivo_Observacion_Real_Minima_GSEC2_11_USM.md"
  - "Operations/Automation/2026-08-27_Contrato_Artefacto_Codigo_Publico_Verificador_Minimo_GSEC2_11_USM.md"
  - "Operations/Automation/2026-08-27_Implementacion_Nucleo_Politica_Publico_GSEC2_11_USM.md"
  - "Operations/Automation/policy_core_gsec211.py"
  - "Operations/Automation/test_policy_core_gsec211_synthetic.py"
  - "Operations/Automation/2026-08-27_Gate_Superficie_Unica_Ejecucion_Servicios_No_Ejecucion_GSEC2_9_USM.md"
  - "Operations/Automation/2026-08-27_Gate_Analisis_Documental_Superficie_Ejecucion_No_Ejecucion_GSEC2_10_USM.md"
  - "Operations/Automation/2026-08-25_Consentimiento_Piloto_Real_Shadow_Ledger_USM.md"
  - "GrowthOS/todo.md"
organization: "Operations/Automation"
---

# Especificación estática del verificador mínimo G-SEC-2.11

## Propósito y límite decisivo

Esta especificación describe el comportamiento permitido de un **posible verificador local de una sola pasada** bajo G-SEC-2.11. Es únicamente un contrato de diseño público y estático: no contiene código, comandos ejecutables, nombres reales de procesos, rutas, credenciales, configuración ni resultados de sistema.

> **Límite decisivo:** esta especificación está en `Review`, pero no existe un verificador autorizado ni un registro de componentes aprobado. Por tanto, no hay una consulta técnica permitida ni una afirmación sobre los servicios o collectors reales de Universe Sent Me.

## Registro de revisión humana independiente

Fernando confirmó el registro vacío por defecto, las entradas admisibles, las precondiciones, la una sola pasada, las salidas agregadas, la precedencia y la detención fail-closed. Como resultado, esta especificación pasa de `Draft` a `Review`.

> **Alcance confirmado:** la revisión valida exclusivamente el contrato estático. No crea código, no registra nombres reales, no consulta servicios, collectors, procesos, red, puertos, datos, configuración o rutas privadas, y no habilita G-NORM-4R.

Para mantener la coherencia, esta revisión actualiza G-SEC-2.11, G-SEC-2.9, el pendiente operativo y el changelog central. G-SEC-2, G-SEC-2.8 y G-SEC-2.10 conservan sus estados y prohibiciones sin cambios.

## Entrada pública mínima y registro vacío por defecto

La única entrada lógica admisible sería un registro efímero, autorizado para una ventana única, de componentes **previamente declarados públicos, exactos y no sensibles**. Esta especificación deja dicho registro vacío. No debe añadir nombres reales por inferencia, inspección ni lectura del equipo.

| Campo lógico | Regla de contenido | Prohibición |
|---|---|---|
| `component_label` | Etiqueta pública y genérica, no identificadora. | Cuenta, usuario, host, ruta, token o dato de plataforma. |
| `component_kind` | Uno de: `service`, `automation`, `dedicated_wrapper` o `dedicated_process`. | `collector_generic`, `network`, `daemon` o categorías abiertas. |
| `exact_public_name` | Nombre exacto, previamente aprobado, que no revele información sensible. | Patrones, comodines, expresiones regulares, argumentos o rutas. |
| `window_authorization` | Autorización humana puntual, con alcance y vigencia declarados. | Consentimiento general, recurrente o reutilizable. |

Un registro vacío, ambiguo, duplicado, con nombres genéricos o con datos sensibles se considera no utilizable. La salida correcta sería `observation_incomplete_or_blocked` o `scope_mismatch`, según corresponda; nunca una ausencia observada.

Los collectors que solo pueden distinguirse por intérprete genérico, argumentos, rutas o variables siguen excluidos. Su observación requeriría primero un diseño distinto de wrapper dedicado y no sensible; esta especificación no crea ni autoriza tal wrapper.

## Precondiciones obligatorias de una ejecución futura

Antes de toda consulta futura, el operador tendría que confirmar en memoria —sin leer archivos privados ni persistir el resultado— que todos los requisitos siguientes se cumplen. La ausencia de uno basta para no empezar.

| Precondición | Verificación conceptual permitida | Si falla |
|---|---|---|
| Gate en `Review` | G-SEC-2.11 y esta especificación fueron revisados documentalmente. | No ejecutar. |
| Autorización de ventana | Existe autorización humana explícita, única y vigente para esa lista exacta. | `observation_incomplete_or_blocked`. |
| Registro finito | La lista contiene al menos un nombre exacto, sin duplicados ni categorías genéricas. | `observation_incomplete_or_blocked`. |
| Superficie mínima | Cada entrada pertenece a la única superficie de ejecución local USM. | `scope_mismatch`. |
| Método sin privilegios | La consulta puede realizarse sin elevación, red, daemon ni lectura adicional. | `observation_incomplete_or_blocked`. |
| Salida no persistente | Se puede descartar todo valor intermedio y emitir solo una categoría agregada. | `observation_incomplete_or_blocked`. |

## Método lógico de una sola pasada

La futura implementación, si recibiera autorización separada, deberá reducirse a la siguiente secuencia lógica. Esta sección define comportamiento, no comandos ni lenguaje de programación.

| Orden | Acción lógica permitida | Límite obligatorio |
|---:|---|---|
| 1 | Validar precondiciones y lista autorizada. | Si una falla, no consultar el equipo. |
| 2 | Consultar de forma dirigida cada `exact_public_name` registrado. | Sin listar procesos, unidades o tareas ajenas. |
| 3 | Reducir cada consulta a `present` o `not_present` solo en memoria. | No conservar PID, usuario, argumentos, rutas, unidad ni texto de salida. |
| 4 | Aplicar la precedencia fail-closed de G-SEC-2.11. | Detener en el primer caso bloqueante o candidato. |
| 5 | Emitir una única categoría agregada al operador. | Sin archivo, log, captura, hash, evidencia, red o destino externo. |

Una sola pasada significa que no hay espera, repetición, bucle, timeout prolongado, vigilancia, tarea programada ni ejecución en segundo plano. El verificador no puede iniciar, detener, reiniciar, importar, configurar, reparar o instalar ningún componente.

## Categorías de salida y precedencia

Las cuatro categorías son mutuamente excluyentes. Su orden evita que una consulta parcial o excesiva produzca una salida positiva.

| Precedencia | Condición | Salida agregada | Cierre obligatorio |
|---:|---|---|---|
| 1 | La solicitud o una entrada exige elementos fuera de alcance. | `scope_mismatch` | No consultar o detener sin ampliar técnica. |
| 2 | Falta precondición, autorización, capacidad sin privilegios o descarte de salida. | `observation_incomplete_or_blocked` | Detener sin reintento, depuración ni evidencia. |
| 3 | Se observa un nombre exacto previamente registrado. | `registered_execution_candidate_observed` | Detener sin atribuir causa, abrir detalles o modificar estado. |
| 4 | Todas las consultas autorizadas concluyen y ninguna observa un nombre registrado. | `registered_non_execution_observed` | Comunicar solo la categoría, sin inferir que el sistema completo está inactivo. |

Las salidas no son una prueba de seguridad ni un permiso operativo. En especial, `registered_non_execution_observed` describe únicamente una ausencia dentro de una lista finita de nombres y una ventana única.

## Matriz de detención fail-closed

| Situación detectada | Punto de detención | Resultado permitido | Acción prohibida |
|---|---|---|---|
| Lista vacía, duplicada, genérica o ambigua | Antes de consultar. | `observation_incomplete_or_blocked`. | Completarla mediante inspección o usar patrones. |
| Nombre, ruta o argumento sensible | Antes de consultar. | `scope_mismatch`. | Sanitizar con datos del sistema o revelar detalles. |
| Necesidad de red, puerto, socket, daemon o plataforma externa | Antes de consultar. | `scope_mismatch`. | Consultar conectividad, Docker, Compose, API u OAuth. |
| Necesidad de permisos adicionales o cambio de estado | Antes de consultar. | `observation_incomplete_or_blocked`. | Usar elevación, instalar o cambiar permisos. |
| Salida intermedia inesperada o no descartable | Durante la pasada. | `observation_incomplete_or_blocked`. | Guardar, analizar o transmitir la salida. |
| Nombre autorizado observado | Durante la pasada. | `registered_execution_candidate_observed`. | Investigar, atribuir, detener o continuar buscando. |
| Consulta autorizada sin coincidencia | Tras completar toda la lista. | `registered_non_execution_observed`. | Declarar seguridad global o ausencia de collectors genéricos. |

## Datos, redes y persistencia explícitamente excluidos

El posible verificador no puede acceder a rutas privadas, variables de entorno, secretos, credenciales, tokens, evidencia, métricas, contenido de plataformas, discos, LUKS, medios externos, configuración, argumentos de procesos, usuarios, identificadores de host, puertos, sockets, DNS, tráfico, Docker, Compose, OmniRoute, APIs, OAuth, Drive, Sheets, GitHub como destino de datos, IA, cron, schedulers ni servicios externos.

No crea archivos, scripts, logs, capturas, hashes, ledger, reportes, copias, cachés ni pruebas automatizadas. Esta especificación tampoco autoriza usar esta comprobación de forma recurrente o integrarla a un flujo de producción.

## Estado y siguiente acción permitida

Esta especificación está en `Review`. La implementación limitada `2026-08-27_Implementacion_Nucleo_Politica_Publico_GSEC2_11_USM.md` v1.5 y el runner estándar `2026-08-27_Runner_Sintetico_Estandar_GSEC2_11_USM.md` v1.2 están en `Review`; ninguno se ha importado ni ejecutado. No registran nombres reales, no observan el sistema, no usan datos ni abren red. Una prueba sintética ejecutada necesitaría una autorización humana nueva y no permitiría compilar, importar o ejecutar contra el equipo real.

Para conservar coherencia, el estado `Review` se refleja en G-SEC-2.11, G-SEC-2.9, el pendiente operativo y el changelog central. G-SEC-2, G-SEC-2.8 y G-SEC-2.10 no requieren cambio de estado porque sus límites siguen sin alteración.

## Referencias

[1] [Gate técnico pasivo de observación real mínima G-SEC-2.11](2026-08-27_Gate_Tecnico_Pasivo_Observacion_Real_Minima_GSEC2_11_USM.md)

[2] [Gate de superficie única G-SEC-2.9](2026-08-27_Gate_Superficie_Unica_Ejecucion_Servicios_No_Ejecucion_GSEC2_9_USM.md)

[3] [Gate de análisis documental G-SEC-2.10](2026-08-27_Gate_Analisis_Documental_Superficie_Ejecucion_No_Ejecucion_GSEC2_10_USM.md)

[4] [Contrato G-SEC-2](2026-08-25_Consentimiento_Piloto_Real_Shadow_Ledger_USM.md)
