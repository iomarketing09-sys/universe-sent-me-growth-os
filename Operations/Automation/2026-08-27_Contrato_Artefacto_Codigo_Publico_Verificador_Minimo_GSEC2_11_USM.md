---
title: "Contrato no ejecutable del artefacto de código público G-SEC-2.11 — Universe Sent Me"
purpose: "Definir la arquitectura lógica, las interfaces conceptuales, las validaciones y los bloqueos verificables de un futuro artefacto de código público para G-SEC-2.11, sin crear archivos de código, registrar componentes ni observar el sistema."
status: Review
created: 2026-08-27
updated: 2026-08-27
version: "1.4"
author: "Manus AI"
related_documents:
  - "Operations/Automation/2026-08-27_Especificacion_Estatica_Verificador_Minimo_GSEC2_11_USM.md"
  - "Operations/Automation/2026-08-27_Implementacion_Nucleo_Politica_Publico_GSEC2_11_USM.md"
  - "Operations/Automation/policy_core_gsec211.py"
  - "Operations/Automation/test_policy_core_gsec211_synthetic.py"
  - "Operations/Automation/2026-08-27_Gate_Tecnico_Pasivo_Observacion_Real_Minima_GSEC2_11_USM.md"
  - "Operations/Automation/2026-08-27_Gate_Superficie_Unica_Ejecucion_Servicios_No_Ejecucion_GSEC2_9_USM.md"
  - "Operations/Automation/2026-08-27_Gate_Analisis_Documental_Superficie_Ejecucion_No_Ejecucion_GSEC2_10_USM.md"
  - "Operations/Automation/2026-08-25_Consentimiento_Piloto_Real_Shadow_Ledger_USM.md"
  - "GrowthOS/todo.md"
organization: "Operations/Automation"
---

# Contrato no ejecutable del artefacto de código público G-SEC-2.11

## Propósito y límite decisivo

Este documento define cómo tendría que estructurarse un posible artefacto de código público para G-SEC-2.11. Es un contrato de arquitectura y cumplimiento, no una implementación: no contiene sintaxis de programación, comandos, archivos ejecutables, nombres reales de componentes, rutas, resultados ni llamadas al sistema.

> **Límite decisivo:** el artefacto futuro solo podría aplicar reglas sobre una entrada efímera ya autorizada. No puede descubrir nombres, inventariar el equipo, buscar collectors genéricos, interpretar argumentos ni proporcionar por sí mismo una autorización de ejecución.

Este contrato está en `Review`. Se creó el núcleo de política puro `policy_core_gsec211.py` y su archivo de prueba sintética no ejecutada, ambos bajo una autorización explícita y limitada. No existe una interfaz permitida para observar el sistema.

## Registro de revisión humana independiente

Fernando confirmó la arquitectura separada, la interfaz conceptual, el flujo, los invariantes, los límites de pruebas y las prohibiciones. Como resultado, este contrato pasa de `Draft` a `Review`.

> **Alcance confirmado:** la revisión valida solo el contrato documental. No crea código, no registra nombres reales, no selecciona comandos y no consulta servicios, collectors, procesos, red, puertos, datos, configuración o rutas privadas.

Para mantener la coherencia, esta revisión actualiza la especificación estática, G-SEC-2.11, G-SEC-2.9, el pendiente operativo y el changelog central. G-SEC-2, G-SEC-2.8 y G-SEC-2.10 conservan sus estados y prohibiciones sin cambios.

## Arquitectura lógica mínima

Un artefacto futuro deberá separar estrictamente las reglas puras de política de cualquier acceso potencial al equipo. Solo el núcleo de política podría diseñarse como código público; la capa que consulte el sistema no forma parte de este contrato y requeriría una decisión técnica y autorización posterior independientes.

| Capa conceptual | Responsabilidad permitida | Fuera de alcance |
|---|---|---|
| Núcleo de política | Validar la lista efímera, aplicar precedencia y reducir estados a una sola categoría. | Comandos, procesos, red, archivos, permisos o persistencia. |
| Adaptador de consulta | No definido ni autorizado en este contrato. | Invocar herramientas del sistema, leer `/proc`, enumerar unidades o consultar daemons. |
| Interfaz de ejecución | No definida ni autorizada. | CLI, servicio, API, tarea programada, UI, webhook o proceso de fondo. |
| Emisor de resultado | Comunicar una única categoría agregada en memoria al operador autorizado. | Logs, archivos, capturas, red, repositorio, Drive, Sheets o cualquier destino externo. |

Esta separación evita que una futura pieza de código de política acumule capacidades de descubrimiento, ejecución o almacenamiento. Ninguna capa autorizada puede sustituir una revisión humana o una autorización de ventana puntual.

## Interfaz conceptual admisible

La interfaz futura será de entrada finita, salida única y vida efímera. Todos los valores son categorías lógicas; el contrato no establece nombres, comandos ni mecanismos del sistema.

| Elemento | Contenido permitido | Validación obligatoria |
|---|---|---|
| `authorized_registry` | Lista temporal de cero o más entradas públicas previamente aprobadas. | Rechazar lista vacía para una ejecución, duplicados, comodines, rutas, argumentos o valores sensibles. |
| `authorization_context` | Prueba lógica de que hay una ventana única, vigente y exactamente acotada. | Rechazar autorización general, reutilizable, caducada o fuera de alcance. |
| `directed_observation` | Por cada entrada aprobada, solo un estado abstracto `present` o `not_present`. | Rechazar detalles como PID, usuario, host, ruta, argumento, unidad, puerto o texto fuente. |
| `aggregate_outcome` | Una de las cuatro categorías de salida aprobadas. | Emitir una sola categoría según la precedencia; no devolver una lista de hallazgos. |

El núcleo de política debe tratar cualquier campo no reconocido como exceso de alcance. No puede intentar corregirlo, normalizarlo con datos reales ni solicitar información adicional durante una ejecución.

## Flujo lógico requerido

El posible código público deberá poder describir su comportamiento mediante cinco pasos conceptuales y sin bifurcaciones ocultas.

| Orden | Operación lógica | Resultado si falla | Bloqueo obligatorio |
|---:|---|---|---|
| 1 | Validar que existe autorización puntual y que el gate/especificación aplicables están en `Review`. | `observation_incomplete_or_blocked`. | No iniciar consulta alguna. |
| 2 | Validar el registro temporal finito y no sensible. | `scope_mismatch` o `observation_incomplete_or_blocked`. | No descubrir ni completar entradas. |
| 3 | Aceptar solamente respuestas abstractas de una consulta dirigida autorizada. | `scope_mismatch`. | No aceptar ni conservar detalle técnico. |
| 4 | Aplicar la precedencia: alcance → bloqueo → candidato → ausencia limitada. | Una sola categoría agregada. | Detener ante el primer resultado de prioridad superior. |
| 5 | Entregar la categoría únicamente al operador de la ventana. | `observation_incomplete_or_blocked` si no puede mantenerse efímera. | No persistir ni enviar el resultado. |

Una implementación futura no podrá añadir reintentos, temporizadores, bucles de espera, mecanismos de fallback, ejecución concurrente, métricas, telemetría ni aprendizaje automático. Si un comportamiento necesita alguno de esos elementos, queda fuera de este contrato.

## Invariantes verificables antes de aprobar código

Antes de que exista un archivo de código, una revisión estática futura deberá confirmar que el diseño permite comprobar las siguientes invariantes sin ejecutarlo contra el sistema.

| Invariante | Evidencia estática admisible | Señal de rechazo |
|---|---|---|
| Sin acceso al sistema en el núcleo | Dependencias limitadas a tipos, validación y lógica pura. | Llamadas a procesos, sistema de archivos, red o permisos. |
| Sin persistencia | No hay interfaces de archivo, base de datos, caché, hash, log o reporte. | Cualquier escritura, captura o almacenamiento. |
| Sin red ni integración | No aparecen clientes de red, sockets, DNS, HTTP, OAuth/API o destinos externos. | Importación o configuración de conectividad. |
| Sin datos sensibles | Los tipos rechazan rutas, argumentos, usuarios, host, tokens e identificadores. | Campos libres no validados o ejemplos reales. |
| Una sola salida | La interfaz devuelve exactamente una categoría agregada. | Colecciones, detalles, trazas, excepciones expuestas o múltiples resultados. |
| Fail-closed | Todo error o valor desconocido termina en bloqueo o exceso de alcance. | Defaults positivos, reintentos o continuidad tras una anomalía. |

Estas invariantes solo serían requisitos de revisión de código público y sintético. No autorizan construir, compilar, ejecutar, probar contra el sistema ni registrar componentes reales.

## Límites de pruebas futuras

Si en un momento posterior se autorizara una prueba del núcleo de política, solo podría usar valores sintéticos y abstractos. No podrá simular nombres reales, rutas, PIDs, procesos, servicios, puertos, cuentas o datos de plataformas.

| Prueba conceptual futura | Entrada sintética permitida | Resultado esperado |
|---|---|---|
| Registro vacío | Lista sin entradas. | `observation_incomplete_or_blocked`. |
| Campo fuera de alcance | Entrada abstracta marcada como no admisible. | `scope_mismatch`. |
| Autorización ausente | Contexto abstracto no vigente. | `observation_incomplete_or_blocked`. |
| Candidato presente | Un estado abstracto `present`. | `registered_execution_candidate_observed`. |
| Ausencia limitada | Lista sintética finita con solo `not_present`. | `registered_non_execution_observed`. |

No se autorizan scripts de prueba, archivos de fixtures, comandos de terminal, compilar código, instalar dependencias ni pruebas con el equipo actual por medio de este contrato.

## Prohibiciones permanentes

Este contrato no autoriza crear, copiar, compilar, instalar, ejecutar, programar, distribuir o integrar código. No admite nombres reales, procesos, collectors, wrappers, servicios, argumentos, rutas, usuarios, PIDs, puertos, red, sockets, Docker, Compose, OmniRoute, variables de entorno, secretos, tokens, OAuth/API, datos, evidencia, métricas, discos, LUKS, medios externos, Drive, Sheets, GitHub como destino de datos, IA, cron, scheduler, logs, archivos temporales, cachés, hashes, capturas, ledger o backups.

No cambia G-SEC-2 de `Review`, no inicia una fase operativa y no desbloquea G-NORM-4R.

## Estado y siguiente acción permitida

Este contrato está en `Review`. El núcleo de política público y su prueba sintética existen como implementación `2026-08-27_Implementacion_Nucleo_Politica_Publico_GSEC2_11_USM.md` v1.4 en `Review`, sin nombres reales ni interfaz de ejecución. Se creó el runner estándar no ejecutado `2026-08-27_Runner_Sintetico_Estandar_GSEC2_11_USM.md` v1.0 en `Draft`, sin dependencias externas. La siguiente acción permitida es su revisión estática; una prueba sintética ejecutada seguiría requiriendo una autorización humana nueva y no autorizaría observar el sistema.

Para conservar coherencia, el estado `Review` se refleja en la especificación estática, G-SEC-2.11, G-SEC-2.9, el pendiente operativo y el changelog central. G-SEC-2, G-SEC-2.8 y G-SEC-2.10 no requieren cambio de estado porque sus límites continúan vigentes.

## Referencias

[1] [Especificación estática del verificador mínimo G-SEC-2.11](2026-08-27_Especificacion_Estatica_Verificador_Minimo_GSEC2_11_USM.md)

[2] [Gate técnico pasivo de observación real mínima G-SEC-2.11](2026-08-27_Gate_Tecnico_Pasivo_Observacion_Real_Minima_GSEC2_11_USM.md)

[3] [Gate de superficie única G-SEC-2.9](2026-08-27_Gate_Superficie_Unica_Ejecucion_Servicios_No_Ejecucion_GSEC2_9_USM.md)

[4] [Gate de análisis documental G-SEC-2.10](2026-08-27_Gate_Analisis_Documental_Superficie_Ejecucion_No_Ejecucion_GSEC2_10_USM.md)

[5] [Contrato G-SEC-2](2026-08-25_Consentimiento_Piloto_Real_Shadow_Ledger_USM.md)
