---
title: "G-SEC-2.11 — Gate técnico pasivo de observación real mínima — Universe Sent Me"
purpose: "Definir la estructura y los límites de un gate separado que, tras revisiones y autorizaciones posteriores, podría permitir una única observación local y mínima de componentes de ejecución USM registrados, sin datos, red, cambios ni activación operativa."
status: Review
created: 2026-08-27
updated: 2026-08-27
version: "1.4"
author: "Manus AI"
related_documents:
  - "Operations/Automation/2026-08-27_Gate_Superficie_Unica_Ejecucion_Servicios_No_Ejecucion_GSEC2_9_USM.md"
  - "Operations/Automation/2026-08-27_Gate_Analisis_Documental_Superficie_Ejecucion_No_Ejecucion_GSEC2_10_USM.md"
  - "Operations/Automation/2026-08-27_Gate_Tecnico_Pasivo_Preparacion_No_Ejecucion_GSEC2_8_USM.md"
  - "Operations/Automation/2026-08-27_Especificacion_Estatica_Verificador_Minimo_GSEC2_11_USM.md"
  - "Operations/Automation/2026-08-25_Consentimiento_Piloto_Real_Shadow_Ledger_USM.md"
  - "GrowthOS/todo.md"
organization: "Operations/Automation"
---

# G-SEC-2.11 — Gate técnico pasivo de observación real mínima

## Propósito y frontera decisiva

**G-SEC-2.11** propone el único gate técnico que tendría que existir antes de observar un componente de ejecución real de Universe Sent Me. Su finalidad es responder una pregunta deliberadamente estrecha: si un **componente de ejecución previamente registrado y no sensible** se observa o no durante una única ventana local autorizada. No es una auditoría general del equipo ni una comprobación de seguridad integral.

> **Frontera decisiva:** G-SEC-2.11 solo podría observar componentes USM con un nombre público, exacto y no sensible previamente registrado. No puede inferir que todo el sistema está inactivo, que no existe otro proceso, ni que los collectors Python no estén ejecutándose por el solo hecho de no encontrar un nombre conocido.

Este documento es un diseño en `Review`. No ejecuta observaciones, no instala ni crea un verificador y no produce un resultado técnico sobre el equipo actual.

## Cadena de decisiones separadas

La revisión del diseño y la eventual observación real son decisiones distintas. Ninguna aprobación documental equivale a autorización para ejecutar la otra.

| Etapa | Decisión humana requerida | Resultado permitido | No autoriza |
|---|---|---|---|
| 1. Revisión de diseño | Confirmar alcance, registro de nombres, salidas y detención de G-SEC-2.11. | Cambio de `Draft` a `Review`. | Consultar el equipo. |
| 2. Diseño del verificador mínimo | Revisar un verificador local concreto antes de crearlo o usarlo. | Artefacto público y estático, sin secretos ni conexión. | Ejecutarlo contra el sistema. |
| 3. Autorización de una ventana | Autorizar una ejecución única, con fecha, operador y alcance exactos. | Una sola observación pasiva. | Reintento, programación o ampliación del alcance. |
| 4. Cierre humano | Interpretar solo la categoría agregada y decidir si hace falta otro diseño. | Registro no sensible del cierre, si se autoriza. | Corregir, investigar o activar servicios. |

G-SEC-2.9 y G-SEC-2.10 permanecen como antecedentes de alcance y coherencia documental. Este gate no los reemplaza, ni cambia G-SEC-2 de `Review`, ni desbloquea G-NORM-4R.

## Registro de revisión humana independiente

Fernando confirmó la superficie mínima, los nombres registrables, las salidas agregadas y la detención fail-closed. Como resultado, G-SEC-2.11 pasa de `Draft` a `Review`.

> **Alcance confirmado:** la revisión valida solamente la estructura documental del gate. No crea un verificador, no observa servicios, collectors, red, datos o procesos y no habilita G-NORM-4R, una fase operativa, una automatización o una integración.

Para mantener la coherencia, esta revisión actualiza el pendiente operativo, el changelog central y el estado de siguiente acción de G-SEC-2.9. G-SEC-2, G-SEC-2.8 y G-SEC-2.10 conservan sus estados y prohibiciones sin cambios.

## Superficie única que podría observarse

La superficie es **ejecución local de componentes USM previamente registrados**. Solo son observables los nombres que cumplan todos los criterios siguientes: son públicos, exactos, no contienen rutas, argumentos, identificadores ni credenciales, y permiten una consulta local directa sin enumerar procesos ajenos.

| Elemento | Permitido solo si cumple el registro previo | Siempre fuera de alcance |
|---|---|---|
| Servicio dedicado USM | Nombre exacto de ejecutable o unidad local, no sensible. | Enumerar todos los servicios, revisar configuración o controlar unidades. |
| OmniRoute | Únicamente un nombre de proceso dedicado previamente aprobado. | Abrir su directorio, configuración, API, socket, UI o registros. |
| Automatización dedicada USM | Nombre exacto de unidad o wrapper previamente registrado. | Listar cron, timers, workers, webhooks o tareas de otras aplicaciones. |
| Collector con wrapper dedicado | Solo si un wrapper futuro tiene nombre público y no sensible. | Buscar procesos Python por argumentos, rutas o texto de comando. |
| Docker o Compose | Solo como candidato no atribuido si existiera un nombre USM dedicado previamente registrado. | Consultar daemon, socket, contenedores, imágenes, Compose o redes. |

Los collectors actuales que dependen de un intérprete genérico no son observables de forma segura mediante una búsqueda de argumentos. Por ello, G-SEC-2.11 **no puede afirmar nada sobre su ejecución** hasta que exista un diseño separado de un wrapper dedicado, público y no sensible. Ese diseño no está autorizado por este gate.

## Método técnico futuro, mínimo y revisable

Una ejecución futura solo podría usar un verificador local de una sola vez, revisado previamente como texto público. Este debe consultar de forma directa cada nombre exacto registrado, reducir la respuesta a un valor booleano en memoria y descartar toda salida intermedia antes de informar el resultado agregado.

| Restricción de método | Regla obligatoria |
|---|---|
| Consulta dirigida | Solo nombres exactos aprobados; no patrones amplios, no comodines y no inventario general. |
| Sin argumentos | No leer líneas de comando, argumentos, rutas de ejecución, entorno o contenido de `/proc`. |
| Sin red | No consultar puertos, sockets, DNS, conectividad, OAuth/API ni tráfico. |
| Sin daemons | No llamar a Docker, Compose, OmniRoute, collectors, schedulers, servicios o APIs. |
| Sin privilegios adicionales | No usar `sudo`, elevación, cambios de permisos ni acceso a otros usuarios. |
| Una sola pasada | Sin reintentos, bucles, espera, vigilancia, cron, scheduler ni ejecución en segundo plano. |
| Sin persistencia | No crear logs, archivos temporales, capturas, hashes, evidencia, reportes, ledger o copias. |

Quedan expresamente prohibidas las búsquedas que expongan argumentos de procesos, el listado completo de procesos o unidades, y cualquier consulta a puertos, sockets o daemons. Si la observación no puede efectuarse con una consulta dirigida y no sensible, el resultado correcto será detenerse, no ampliar la técnica.

## Salidas agregadas y su significado limitado

La salida de una futura observación no puede contener PID, nombre de host, usuario, ruta, argumento, unidad, puerto, servicio, configuración, token, métrica ni contenido. No se guardará en GitHub ni en una evidencia persistente.

| Categoría permitida | Significado exacto | No significa |
|---|---|---|
| `registered_non_execution_observed` | Durante la única ventana, no se observó ninguno de los nombres exactos autorizados. | Que el sistema completo está seguro o libre de ejecución. |
| `registered_execution_candidate_observed` | Durante la ventana se observó al menos un nombre exacto autorizado. | Que se identificó su causa, que pertenece a USM en todos los casos o que deba detenerse. |
| `observation_incomplete_or_blocked` | Faltó un prerequisito, hubo ambigüedad, permiso insuficiente o una condición de detención. | Permiso para repetir, investigar o elevar privilegios. |
| `scope_mismatch` | La solicitud exige ver argumentos, servicios no registrados, collectors genéricos, red o datos. | Permiso para ampliar este gate. |

Ninguna categoría equivale a `PASS` técnico, certificación de seguridad, autorización de operación, consentimiento de datos reales o activación de G-NORM-4R.

## Revisión documental de detención y salidas

La revisión documental confirma que las categorías separan correctamente cuatro situaciones: ausencia observada dentro de una lista finita autorizada, presencia candidata de un nombre exacto, bloqueo o incompletitud del método, y una solicitud que excede el alcance. Para evitar que una salida positiva se interprete como una afirmación sobre todo el equipo, se aplicará la siguiente precedencia si una ejecución futura llegara a recibir autorización.

| Orden | Regla de decisión | Categoría permitida | Acción obligatoria |
|---|---|---|---|
| 1 | La solicitud excede la lista registrada o requiere argumentos, rutas, red, datos, daemons o privilegios. | `scope_mismatch` | No iniciar ninguna consulta. |
| 2 | Falta la autorización puntual, un prerequisito declarado o la consulta no puede finalizar dentro del método aprobado. | `observation_incomplete_or_blocked` | Detener sin reintento, ampliación ni investigación. |
| 3 | Una consulta dirigida observa al menos un nombre exacto registrado. | `registered_execution_candidate_observed` | Detener sin atribuir causa, abrir detalles ni cambiar estado alguno. |
| 4 | Todas las consultas dirigidas autorizadas terminan y ninguna observa un nombre registrado. | `registered_non_execution_observed` | Informar solo la categoría agregada, sin inferir el estado completo del sistema. |

> **Dictamen documental:** las condiciones son coherentes con una detención fail-closed, siempre que los casos de los órdenes 1 a 3 prevalezcan sobre el orden 4. Esta revisión no cambia el estado `Draft`, no prueba el método y no afirma nada sobre el sistema real.

## Condiciones de detención fail-closed

La ejecución futura deberá detenerse antes de observar nada, o interrumpirse sin reintento, si ocurre cualquiera de las condiciones siguientes.

| Condición | Respuesta obligatoria |
|---|---|
| Nombre no registrado, ambiguo o con información sensible | Emitir `scope_mismatch`; no consultar. |
| Necesidad de leer argumentos, ruta, entorno, configuración, archivos privados o datos | Emitir `scope_mismatch`; no ampliar el método. |
| Necesidad de consultar red, puertos, sockets, Docker, Compose, OAuth/API o una plataforma externa | Emitir `scope_mismatch`; no realizar la consulta. |
| Solicitud de `sudo`, permisos adicionales, cambio de estado o instalación | Emitir `observation_incomplete_or_blocked`; no elevar privilegios. |
| Resultado inesperado o parcialmente atribuido | Emitir `registered_execution_candidate_observed` o `observation_incomplete_or_blocked`; no investigar ni corregir. |
| Ausencia de la autorización de ventana exacta | No ejecutar; conservar el estado `Review` o `Draft` aplicable. |

La detención debe ocurrir antes de cualquier consulta cuando se conozca el exceso de alcance. Si un bloqueo aparece durante una consulta ya autorizada, se descarta su salida intermedia y se emite solo `observation_incomplete_or_blocked`, salvo que ya se haya observado un nombre exacto registrado; en ese caso se usa únicamente `registered_execution_candidate_observed`. Ningún caso permite continuar para recopilar detalles adicionales.

## Prohibiciones permanentes

G-SEC-2.11 no autoriza inicio, parada, reinicio, instalación, actualización, configuración, reparación o desinstalación de servicios. No abre las raíces privadas de USM, variables de entorno, secretos, tokens, OAuth/API, evidencia, métricas, discos, LUKS, medios externos, datos de plataformas, Drive, Sheets, GitHub como destino de datos, IA, OmniRoute, Docker, collectors, cron o schedulers.

No permite automatización, vigilancia continua, programación, red, uso de puertos, conexiones, backups, logs, capturas o persistencia. No modifica ni reemplaza los controles de privacidad, retención, consentimiento granular, read-only, egress o almacenamiento protegido ya definidos en G-SEC-2.

## Estado y siguiente acción permitida

G-SEC-2.11 está en `Review`. No habilita un verificador, una observación del sistema, datos, red, servicios, collectors, automatizaciones, integraciones ni G-NORM-4R. La especificación pública `2026-08-27_Especificacion_Estatica_Verificador_Minimo_GSEC2_11_USM.md` v1.1 fue revisada y está en `Review`; no creó código ni registró nombres reales. Si surge una necesidad concreta, cualquier diseño de artefacto de código requerirá una autorización humana separada y no permitirá ejecutarlo contra el sistema.

Para preservar la coherencia, el estado `Review` se refleja en el pendiente operativo, el changelog central y el estado de siguiente acción de G-SEC-2.9. El contrato G-SEC-2 y G-SEC-2.10 no requieren cambio de estado porque sus límites continúan vigentes.

## Referencias

[1] [Gate de superficie única G-SEC-2.9](2026-08-27_Gate_Superficie_Unica_Ejecucion_Servicios_No_Ejecucion_GSEC2_9_USM.md)

[2] [Gate de análisis documental G-SEC-2.10](2026-08-27_Gate_Analisis_Documental_Superficie_Ejecucion_No_Ejecucion_GSEC2_10_USM.md)

[3] [Gate técnico pasivo de preparación G-SEC-2.8](2026-08-27_Gate_Tecnico_Pasivo_Preparacion_No_Ejecucion_GSEC2_8_USM.md)

[4] [Contrato G-SEC-2](2026-08-25_Consentimiento_Piloto_Real_Shadow_Ledger_USM.md)
