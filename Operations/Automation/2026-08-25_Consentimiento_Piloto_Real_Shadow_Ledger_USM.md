---
title: "G-SEC-2 — Controles de privacidad, retención, operación read-only y consentimiento granular — Universe Sent Me"
purpose: "Definir los controles separados que deben diseñarse, revisarse y aprobarse antes de considerar una única inserción real privada en el shadow ledger bajo G-NORM-4R."
status: Review
created: 2026-08-25
updated: 2026-08-27
version: "4.3"
author: "Manus AI"
related_documents:
  - "Operations/Automation/2026-08-25_Shadow_Ledger_Privado_Append_Only_USM.md"
  - "Operations/Automation/2026-08-25_Esquema_Normalizacion_Determinista_Multicanal_USM.md"
  - "Operations/Automation/2026-08-25_Guia_Piloto_Local_API_Oficial_Metricas_USM.md"
  - "Operations/Automation/2026-08-25_Plan_Decision_Cifrado_Local_G-NORM-4R.md"
  - "Operations/Automation/2026-08-26_Proyecto_Migracion_LUKS_Integral_USM.md"
  - "GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
  - "GrowthOS/todo.md"
  - "Operations/Automation/preflight_gsec2_readonly_barriers.sh"
  - "Operations/Automation/validate_gsec2_readonly_barriers_synthetic.py"
  - "Operations/Automation/preflight_gsec2_minimization_egress.sh"
  - "Operations/Automation/validate_gsec2_minimization_egress_synthetic.py"
  - "Operations/Automation/preflight_gsec2_retention_disposition.sh"
  - "Operations/Automation/validate_gsec2_retention_disposition_synthetic.py"
  - "Operations/Automation/preflight_gsec2_granular_consent.sh"
  - "Operations/Automation/validate_gsec2_granular_consent_synthetic.py"
  - "Operations/Automation/2026-08-27_Plantilla_Tarjeta_Consentimiento_Puntual_USM.md"
  - "Operations/Automation/2026-08-27_Ficha_Propuesta_Minima_Comparacion_Alcance_USM.md"
  - "Operations/Automation/2026-08-27_Procedimiento_Preliminar_Propuesta_Minima_GSEC2_4c_USM.md"
  - "Operations/Automation/2026-08-27_Gate_Diseno_Propuesta_Hipotetica_Unica_GSEC2_4cP1_USM.md"
  - "Operations/Automation/2026-08-27_Gate_Formato_Vacio_Propuesta_Hipotetica_GSEC2_4cP2_USM.md"
  - "Operations/Automation/preflight_gsec2_template_static_integrity.sh"
  - "Operations/Automation/validate_gsec2_template_static_integrity.py"
  - "Operations/Automation/2026-08-27_Revision_Final_Consolidacion_GSEC2_USM.md"
organization: "Operations/Automation"
---

# G-SEC-2 — Controles previos para un piloto real privado

## Propósito, estado y límite

**G-SEC-2** es el gate de diseño que separa la seguridad técnica ya verificada bajo LUKS de cualquier tratamiento de métricas reales. Su finalidad es fijar qué datos mínimos podría tratar un piloto, durante cuánto tiempo, bajo qué modo de lectura y con qué autorización humana específica. Este documento está en estado **Review**: Fernando confirmó los cuatro controles de diseño; no activa G-NORM-4R, no cambia scripts, no crea un ledger persistente y no autoriza llamadas de red.

> **Principio de decisión:** una confirmación de cifrado no es una autorización de tratamiento. Cada finalidad, categoría de dato, ventana temporal y salida posible requiere una autorización independiente y revocable.

El marco se inspira en gestión de riesgos de privacidad, minimización de datos y limitación de almacenamiento. No constituye asesoría legal ni sustituye obligaciones aplicables a iO Marketing o Universe Sent Me. El marco de NIST es voluntario y orientado a gestionar riesgo de privacidad; la guía del ICO resume la minimización como datos adecuados, relevantes y limitados a lo necesario para una finalidad definida. [1] [2]

## Estado de partida y resultado esperado

La migración LUKS, la restauración selectiva, la suite sintética, la inspección pasiva de OmniRoute y la revisión estática de collectors ya pasaron. Esos resultados solo confirman que el entorno puede permanecer aislado y que el código público tiene contratos revisados. **No confirman** que exista una base aprobada para retener observaciones reales ni permiten ejecutar ningún collector.

| Elemento | Estado al diseñar G-SEC-2 | Qué cambia este documento |
|---|---|---|
| Disco local LUKS | Validado. | Se mantiene como condición técnica, no como permiso de uso. |
| Evidencia, tokens y configuración privados | Restaurados con permisos restrictivos. | Permanecen cerrados y no se inspeccionan. |
| Collectors oficiales | Revisados de manera estática. | Siguen sin instalar dependencias ni ejecutarse. |
| Shadow ledger | Contrato `Review`; pruebas solo sintéticas y temporales. | No se crea archivo persistente. |
| G-NORM-4R | Bloqueado. | Solo podrá reconsiderarse tras aprobar y verificar los cuatro controles G-SEC-2. |

El resultado esperado de este gate es un paquete de decisiones verificables, no una automatización: un registro de minimización, una política de retención, una especificación de operación read-only y una tarjeta de consentimiento granular. Solo cuando las cuatro piezas estén aprobadas y comprobadas en un gate posterior puede proponerse el mínimo siguiente paso técnico.

### Registro de revisión humana — 2026-08-26

Fernando confirmó explícitamente los cuatro controles de diseño: alcance mínimo limitado a Universe Sent Me; retención propuesta de 30 días con revisión humana y sin mutación; operación manual estrictamente read-only; y consentimiento por una sola operación, con vigencia máxima de 24 horas y posibilidad de detenerla. Esta revisión cambia el estado documental de `Draft` a `Review` solamente. No constituye consentimiento granular para un piloto ni autorización para abrir datos, ejecutar collectors o crear un shadow ledger persistente.

## Clasificación de datos y frontera de salida

Para evitar que una métrica aparentemente inocua se convierta en un conjunto de datos más amplio, G-SEC-2 divide los datos por necesidad operativa. La clasificación se aplica antes de abrir una configuración o ejecutar un collector.

| Clase | Ejemplos | Permitido en un futuro piloto mínimo | Prohibido en todo el piloto G-NORM-4R |
|---|---|---|---|
| Credenciales | Tokens OAuth, secretos de cliente, claves, cookies, códigos de autorización. | Nunca en el ledger, documentación, salida de terminal ni herramientas externas. | Copiar, imprimir, subir, registrar o compartir. |
| Evidencia fuente privada | Respuestas API, archivos raw, IDs completos, timestamps de origen y metadatos de plataforma. | Solo lectura local temporal para formar la observación aprobada, si un gate futuro lo permite. | GitHub, Drive, Sheets, OmniRoute, IA, navegador compartido, backups automáticos o salida de consola. |
| Observación normalizada mínima | Plataforma, métrica nativa aprobada, ventana, disponibilidad, procedencia y el identificador minimizado exigido por el esquema. | Máximo una observación por plataforma; sin monetización ni contenido. | Captions, títulos, URLs, handles, nombres de personas, comentarios, audiencias, perfiles o rankings. |
| Metadatos operativos no sensibles | Versión de contrato, resultado PASS/BLOCKED, fecha del gate y motivo de detención. | Pueden documentarse en GitHub si no contienen datos reales ni rutas privadas. | IDs, valores de métricas, hashes de evidencia, rutas, errores que revelen secretos o configuraciones. |

La finalidad única propuesta es **probar la integridad append-only, idempotencia y retención limitada de cuatro observaciones mínimas**. No se permite analizar rendimiento, comparar redes, elaborar recomendaciones editoriales, medir audiencias, inferir personas ni entrenar o alimentar sistemas de IA. Recoger información “por si pudiera servir” queda fuera de la finalidad y de la minimización propuesta. [2]

## Arquitectura de control G-SEC-2

G-SEC-2 se divide en cuatro controles independientes. Un PASS de un control no permite omitir los demás. Cualquier resultado `BLOCKED`, información ambigua o cambio de alcance detiene el flujo y devuelve el trabajo a diseño, sin abrir datos reales.

| Subgate | Pregunta que resuelve | Evidencia mínima no sensible | No autoriza |
|---|---|---|---|
| G-SEC-2.1 Privacidad y minimización | ¿La finalidad, categorías, cuentas y salidas están limitadas a lo estrictamente necesario? | Matriz de datos permitidos/prohibidos y revisión humana de finalidad. | Abrir evidencia, ejecutar collectors o crear ledger. |
| G-SEC-2.2 Retención y disposición | ¿Cada categoría tiene plazo, disparador de revisión y método de disposición aprobado? | Calendario de retención y procedimiento de pausa/revisión sin datos reales. | Borrado automático, backups, archivado cloud o borrado de eventos existentes. |
| G-SEC-2.3 Operación estrictamente read-only | ¿La ejecución futura tiene barreras concretas contra escritura, egress y ampliación de scopes? | Checklist técnico y prueba sintética de bloqueo de modos no permitidos. | OAuth, API, Docker, cron, OmniRoute, Sheets o cualquier salida externa. |
| G-SEC-2.4 Consentimiento granular | ¿Fernando aprueba una sola operación, con alcance, vigencia y revocación explícitos? | Tarjeta de consentimiento completada solo cuando exista propuesta exacta. | Consentimiento permanente, lotes, métricas financieras o datos de otras marcas. |

## G-SEC-2.1 — Privacidad y minimización

El responsable de la futura ejecución debe declarar antes de tocar datos privados: finalidad única, plataforma, tipo de métrica, tipo de ventana, categoría de identificador indispensable y destino local. La revisión humana debe comprobar que cada campo responde a esa finalidad. Si un dato no es necesario para escribir la observación aprobada o comprobar el contrato, se excluye.

| Control | Regla de diseño | Criterio de PASS | Condición de bloqueo |
|---|---|---|---|
| Separación de marca | Solo Universe Sent Me y las cuatro cuentas previamente validadas. | La propuesta nombra exclusivamente Universe Sent Me. | Cualquier referencia a Bam in a Can, Firma Bordados, clientes, cuentas personales o ambigüedad. |
| Métrica mínima | Una métrica nativa no financiera por plataforma, conforme al esquema normalizado. | La tarjeta enumera solo las cuatro métricas aprobables. | Monetización, comentarios, perfiles, reach/impressions no comparables, texto o métricas derivadas. |
| Identificador | Conservar solo el identificador minimizado que el esquema requiera para idempotencia; no se muestra ni se exporta. | Se justifica por `observation_key` y no se agregan campos de contenido. | ID completo en consola, GitHub, archivos de reporte o salida externa. |
| Egress | No salen datos de observación, evidencia ni credenciales del directorio LUKS. | Destinos permitidos = almacenamiento local privado del piloto. | GitHub, Drive, Sheets, OmniRoute, IA, email, mensajería, navegador o sincronización. |
| Observabilidad segura | Los resultados operativos se reducen a PASS/BLOCKED y conteos sin valores. | El diseño de salida no revela filas ni paths privados. | Logs con valores, IDs, títulos, URLs, hashes de evidencia o secretos. |

La minimización debe revisarse antes de cada propuesta de ejecución y después de cualquier cambio en scripts, scopes, esquema o proveedores. La recomendación de revisar periódicamente lo conservado y eliminar lo innecesario se adopta como control operativo, no como afirmación de cumplimiento legal. [2]

## G-SEC-2.2 — Retención, revisión y disposición

La retención propuesta es **máximo 30 días desde cada captura** para evidencia fuente y observaciones del único piloto real. El plazo no comienza cuando se analiza un archivo ni se extiende automáticamente por una reejecución. Las credenciales no forman parte del piloto ni del ledger: conservan su ciclo de vida separado y nunca se incluyen en una revisión de retención de métricas.

| Categoría | Finalidad permitida | Retención propuesta | Revisión y disposición futura |
|---|---|---:|---|
| Evidencia fuente privada | Verificar la procedencia de la observación mínima durante el piloto. | 30 días desde `captured_at_utc`. | Al vencimiento, bloquear uso nuevo y solicitar revisión humana para eliminación local aprobada; no se sincroniza ni respalda. |
| Observación real del shadow ledger | Validar append-only, idempotencia y supersedencia del piloto. | 30 días desde `observed_at_utc`. | Al vencimiento, detener el piloto; una nueva cadena solo se crea bajo gate posterior. No se modifica una fila histórica. |
| Metadatos de ejecución no sensibles | Explicar el estado de gates sin exponer datos. | Mientras el proyecto lo requiera. | Se revisan en changelog; no incluyen observaciones, IDs, valores ni rutas privadas. |
| Credenciales y tokens | Autenticar una futura lectura oficial autorizada. | Fuera del alcance de G-NORM-4R. | No se inventaría ni se elimina por esta política; requiere control específico de credenciales. |

La regla de 30 días es un límite de producto para reducir exposición, no una razón para conservar datos “por si acaso”. La guía del ICO indica que los plazos deben justificarse por la finalidad, revisarse y permitir eliminación o anonimización cuando ya no sean necesarios. [3]

Para preservar el principio append-only, no habrá un proceso automático de borrado ni una edición silenciosa del JSONL. Al llegar a un vencimiento, el procedimiento diseñado es: **bloquear nuevas escrituras**, emitir únicamente un estado `retention_review_required`, revisar localmente la necesidad y solicitar una autorización humana separada para cualquier disposición. Esa futura autorización debe decidir entre eliminar el conjunto completo del piloto o mantenerlo temporalmente con justificación documentada; no puede reabrir ni reescribir eventos existentes. Este diseño no implementa el bloqueo, el reloj, la eliminación ni la revisión.

## G-SEC-2.3 — Operación estrictamente read-only

Una operación futura será read-only solo si todos sus límites técnicos y operativos son verdaderos a la vez. “Tener un token de lectura” no basta: el flujo completo debe impedir la publicación, la modificación, la programación y la salida de datos a otros destinos.

| Capa | Regla obligatoria de la futura operación | Bloqueo inmediato |
|---|---|---|
| Inicio | Solo ejecución manual, una vez, desde la sesión LUKS y después de consentimiento vigente. | Cron, servicio, Docker, OmniRoute, reintento automático o proceso en segundo plano. |
| Proveedor | Solo endpoint oficial ya revisado y scopes mínimos de lectura definidos en el contrato. | Scope nuevo, cuenta no esperada, OAuth nuevo, permiso de escritura o endpoint no revisado. |
| Método y contenido | TikTok/YouTube según contrato de lectura; Meta solamente GET; máximo la muestra aprobada. | Meta POST/PUT/PATCH/DELETE, publicación, comentario, mensaje, administración, anuncios o transferencia. |
| Procesamiento | Normalización determinista local de la única métrica autorizada, sin IA y sin consultas adicionales. | Modelo, OmniRoute, clasificación editorial, ranking, inferencia de audiencia o enriquecimiento. |
| Almacenamiento y salida | Solo directorio privado cifrado con permisos previstos; consola con estado seguro. | GitHub, Drive, Sheets, email, chat, copia externa, portapapeles, paths en logs o datos en pantalla compartida. |
| Fallo | `BLOCKED`, detener, no reintentar y no ampliar permisos. | Sustituir ausencias por cero, usar una fuente alternativa, corregir datos reales in-place o continuar parcialmente. |

Antes de cualquier ejecución real, se deberá diseñar una prueba **sintética** que demuestre que los modos de escritura, egress y automatización se rechazan. Esa prueba no importará collectors, no leerá configuración privada ni abrirá sockets. La autorización para diseñarla y ejecutarla será un subgate nuevo, no parte de este documento.

### G-SEC-2.3a — verificación sintética de barreras aprobada y pasada

G-SEC-2.3a se diseñó, aprobó explícitamente y pasó en el sistema LUKS. Usa el fixture versionado `fixtures/gsec2_readonly_barriers_synthetic.json`, el validador `validate_gsec2_readonly_barriers_synthetic.py` y el wrapper `preflight_gsec2_readonly_barriers.sh`. Los tres artefactos contienen únicamente casos ficticios y reglas de rechazo; no reciben parámetros de cuentas, métricas, ventanas, tokens, rutas privadas ni evidencia.

| Caso sintético | Resultado que deberá demostrar la suite | Barrera G-SEC-2 cubierta |
|---|---|---|
| `manual_local_minimum_allowed` | Se permite exclusivamente la validación manual en memoria de un fixture sintético. | Operación local mínima. |
| `external_egress_blocked` | Rechazo de un destino GitHub ficticio, sin crear salida. | Egress y destinos externos prohibidos. |
| `scheduler_blocked` | Rechazo de ejecución programada ficticia. | Sin cron, servicios ni automatización. |
| `private_evidence_blocked` | Rechazo de la clase simulada de evidencia privada. | No leer rutas ni datos privados. |
| `network_blocked` | Rechazo de la bandera de red y guardia de socket interceptada. | Sin red, OAuth ni API. |
| `financial_metric_blocked` | Rechazo de dato financiero ficticio. | Exclusión de monetización. |
| `cross_brand_blocked` | Rechazo de una marca ficticia distinta. | Separación estricta de marcas. |

El wrapper ofrece `--plan`, `--preflight` y `--execute --confirm RUN_USM_GSEC2_SYNTHETIC_BARRIERS`. El modo `--plan` no inspecciona el entorno. El preflight solo comprueba repositorio, Python, los dos artefactos públicos y nombres de procesos para detenerse si detecta un collector, OmniRoute o Docker Compose. El modo de ejecución usa `python3 -B` y `PYTHONDONTWRITEBYTECODE=1`, bloquea `socket.socket` y emite solo estado agregado, casos de rechazo y garantías. No crea archivos, incluso temporales, ni llama ningún servicio.

La ejecución autorizada devolvió `STATUS=preflight_complete_gsec2_synthetic_only_no_network_no_private_read`, seguido de `gsec2_synthetic_barriers_passed` y `STATUS=gsec2_synthetic_barriers_complete_no_network_no_private_read`. Permitió únicamente `manual_local_minimum_allowed` en memoria. Rechazó los seis casos esperados: egress externo, scheduler, clase de evidencia privada, red, dato financiero y marca ajena. La guardia de socket informó `blocked_as_designed`; no se detectaron servicios ni collectors activos.

Cualquier diferencia, proceso detectado o artefacto faltante será `BLOCKED`; no se corrige el entorno, no se instala software y no se reintenta sin revisar el resultado. El PASS demuestra solo las barreras sintéticas actuales: no cambia G-SEC-2 de `Draft`, no concede consentimiento granular y no abre G-NORM-4R.

### G-SEC-2.1a y G-SEC-2.2a — verificaciones sintéticas aprobadas y pasadas

Los dos subgates se prepararon como validaciones independientes de política con fixtures ficticios y pasaron tras aprobación explícita. No reciben datos de plataformas, no leen directorios privados ni entorno, no importan collectors y bloquean `socket.socket` antes de cualquier red. Cada wrapper tiene los modos `--plan`, `--preflight` y `--execute` con una cadena de confirmación distinta, de modo que la autorización quedó limitada a los dos controles sintéticos.

| Subgate | Permite solo en el fixture | Debe rechazar en el fixture | Confirmación futura exacta |
|---|---|---|---|
| G-SEC-2.1a minimización/egress | Campos agregados mínimos (`platform`, `metric_name`, `metric_value`, `window_type`, `availability`) en memoria temporal. | Caption, handle, respuesta raw, Drive, Sheets y otra marca. | `RUN_USM_GSEC2_MINIMIZATION_EGRESS_SYNTHETIC` |
| G-SEC-2.2a retención/disposición | Registro ficticio dentro de 30 días o, exactamente en el día 30, bloqueo de nuevas escrituras y solicitud de revisión humana sin mutación. | Retención vencida sin revisión, eliminación automática, reescritura in-place, archivo externo e indefinición. | `RUN_USM_GSEC2_RETENTION_DISPOSITION_SYNTHETIC` |

El preflight de G-SEC-2.1a confirmó Python, sus artefactos ficticios y la ausencia de procesos de servicio o collectors. Su suite devolvió `gsec2_minimization_egress_synthetic_passed`: permitió solo el agregado mínimo en memoria y rechazó caption, handle, respuesta raw, Drive, Sheets y otra marca. El preflight de G-SEC-2.2a confirmó las mismas condiciones de aislamiento y su suite devolvió `gsec2_retention_disposition_synthetic_passed`: permitió un registro ficticio dentro del plazo y el estado de revisión humana en el día 30; rechazó vencimiento sin revisión, eliminación automática, reescritura in-place, archivo externo y retención indefinida.

Ambas suites reportaron la guardia de socket `blocked_as_designed`, no leyeron rutas privadas ni variables de entorno, no importaron collectors y no escribieron ledger, evidencia, archivos canónicos o destinos externos. El preflight de cada una se limitó a repositorio, Python, sus dos archivos públicos y procesos por nombre; no modificó el entorno. Ambos PASS no abren G-NORM-4R ni constituyen consentimiento granular para una operación real.

## G-SEC-2.4 — Consentimiento granular, por operación y revocable

El consentimiento propuesto no será una autorización general para “usar métricas”. Es una decisión puntual de Fernando sobre una única operación definida. Debe ser solicitado solo después de que G-SEC-2.1, 2.2 y 2.3 estén completos y de que exista una propuesta técnica exacta, revisable y sin secretos.

| Campo de la tarjeta de consentimiento | Valor que debe completarse antes de aprobar | Regla |
|---|---|---|
| Referencia | Versión de contrato, fecha y subgates G-SEC-2 completados. | Si falta una referencia, no hay consentimiento válido. |
| Alcance de marca | `Universe Sent Me` únicamente. | Prohíbe explícitamente Bam in a Can, Firma Bordados y terceros. |
| Muestra | Máximo cuatro observaciones, una por plataforma. | Toda ampliación requiere una nueva tarjeta. |
| Métricas | TikTok `views_native`; YouTube `views_native` de periodo cerrado; Facebook `reactions_native`; Instagram `likes_native`. | Sin monetización, comentarios, texto, URLs, audiencias ni métricas derivadas. |
| Conservación | Máximo 30 días por evidencia/observación, sin backup ni sincronización. | No hay extensión automática. |
| Operación | Una ejecución manual, read-only, sin salida externa. | Prohíbe cron, Docker, OmniRoute, Sheets, Drive, GitHub e IA. |
| Vigencia | Una sola ejecución dentro de una ventana máxima de 24 horas. | Pasada la ventana, se requiere consentimiento nuevo. |
| Revocación | Fernando puede revocar antes de iniciar o detener durante el preflight. | Revocar bloquea la ejecución; no causa borrado automático. |
| Resultado esperado | Solo estado agregado de PASS/BLOCKED y conteos seguros. | No se reportan valores, filas, IDs, rutas ni evidencia. |

La aprobación debe contener una frase inequívoca que nombre el gate, la muestra, el plazo, la prohibición de salidas y la vigencia. Una aprobación de diseño, una aprobación histórica de collectors o una aprobación del cifrado LUKS no sustituye esta tarjeta. Si la persona que opera percibe cualquier diferencia entre la tarjeta y el entorno real, debe detenerse sin abrir datos y registrar únicamente `consent_scope_mismatch`.

### G-SEC-2.4a — verificación sintética de completitud de tarjeta aprobada y pasada

G-SEC-2.4a contiene una tarjeta ficticia de una operación y ocho tarjetas defectuosas dentro de `fixtures/gsec2_granular_consent_card_synthetic.json`. Su validador solo revisa estructura y límites en memoria. El marcador `synthetic_approval_marker` representa un caso de prueba y **no** es consentimiento de Fernando, no tiene efectos operativos ni puede convertirse en una autorización real.

| Caso sintético | Resultado previsto | Límite que verifica |
|---|---|---|
| `complete_single_operation_card_allowed` | Permitir solo la estructura ficticia completa. | Referencia, marca USM, muestra de cuatro, métricas exactas, 30 días, operación única read-only, 24 h, revocación y salida agregada. |
| `missing_reference_blocked` | Bloquear. | No existe tarjeta válida sin propuesta identificable. |
| `scope_expansion_blocked` y `financial_metric_blocked` | Bloquear. | No hay ampliación de muestra, otra plataforma ni monetización. |
| `retention_extension_blocked` | Bloquear. | El plazo no supera 30 días. |
| `non_readonly_execution_blocked` y `external_egress_blocked` | Bloquear. | Solo una operación manual read-only y sin salida. |
| `expired_or_nonrevocable_card_blocked` | Bloquear. | Vigencia exacta de 24 h y posibilidad de revocación. |
| `real_data_or_identifier_field_blocked` | Bloquear. | Un fixture de consentimiento no admite datos reales ni identificadores. |

El wrapper `preflight_gsec2_granular_consent.sh` mantiene los modos `--plan`, `--preflight` y `--execute --confirm RUN_USM_GSEC2_GRANULAR_CONSENT_SYNTHETIC`. Incluso el modo de ejecución no pide, guarda, valida ni concede consentimiento real. Solo puede emitir `gsec2_granular_consent_synthetic_passed`, casos agregados de rechazo y garantías. La guardia de socket bloquea red; no se leen variables de entorno, rutas privadas, tokens o evidencia y no se invoca collector, OAuth, API, servicio, scheduler, Docker u OmniRoute.

La ejecución autorizada pasó con `STATUS=preflight_complete_gsec2_granular_consent_synthetic_only_no_network_no_private_read`, `gsec2_granular_consent_synthetic_passed` y `STATUS=gsec2_granular_consent_synthetic_complete_no_network_no_private_read_no_real_consent`. Permitió únicamente la tarjeta ficticia completa y rechazó las ocho variantes esperadas: referencia ausente, ampliación de alcance, métrica financiera, retención extendida, ejecución no read-only, egress externo, vigencia/no revocación inválida y datos/identificadores simulados. Reportó guardia de socket bloqueada, sin procesos de servicios o collectors.

Este PASS valida únicamente la **plantilla ficticia**. La plantilla real vacía y el procedimiento de solicitud humana se documentan por separado en `2026-08-27_Plantilla_Tarjeta_Consentimiento_Puntual_USM.md` v1.3. Su revisión humana fue confirmada y el documento pasó a `Review`, sin pedir todavía datos, tokens o consentimiento y sin autorizar una operación. La ficha pública vacía y lista manual para comparar una futura propuesta contra esos límites se documentan en `2026-08-27_Ficha_Propuesta_Minima_Comparacion_Alcance_USM.md` v1.5, ahora en `Review` tras una confirmación humana independiente. La ficha continúa sin propuesta, campos completados, tarjeta o consentimiento. G-SEC-2.5 pasó su validación estática y G-SEC-2.6 consolidó documentalmente sus diez controles públicos, sin modificar estos límites. G-NORM-4R continúa bloqueado hasta un gate separado que incorpore una tarjeta real completa, consentimiento humano vigente y validación manual del alcance técnico.

### G-SEC-2.5 — integridad estática de plantillas diseñada

G-SEC-2.5 usa `fixtures/gsec2_template_static_integrity_expectations.json`, `validate_gsec2_template_static_integrity.py` y `preflight_gsec2_template_static_integrity.sh`. El gate solo puede leer los tres documentos públicos de contrato, plantilla y ficha dentro del repositorio. Comprueba estado documental, marcadores de límites, enlaces cruzados, campos pendientes y las diez filas de comparación; no interpreta propuestas, tarjetas o respuestas humanas.

| Comprobación estática | Resultado esperado | Límite de seguridad |
|---|---|---|
| Estados de documentos | G-SEC-2 y plantilla en `Review`; ficha en `Draft`. | No cambia estados ni emite artefactos. |
| Límites constantes | Marca USM, máximo 4 observaciones, 30 días y 24 horas. | No evalúa valores o datos de operación. |
| Campos pendientes | Marcadores de no emisión/no solicitud/no comparación permanecen presentes. | No completa ni solicita campos. |
| Enlaces y controles | Referencias mutuas y diez controles de comparación. | No abre rutas fuera del repositorio. |

El wrapper solo ofrece `--plan`, `--preflight` y `--execute --confirm RUN_USM_GSEC2_TEMPLATE_STATIC_INTEGRITY`. El modo de planificación validó su sintaxis y no leyó documentos. La ejecución autorizada confirmó los cuatro artefactos públicos y ausencia de procesos de collectors/servicios; el análisis devolvió `gsec2_template_static_integrity_passed` con marca USM, máximo de cuatro observaciones, 30 días, 24 horas y las diez filas de comparación. Una primera coincidencia textual de vigencia se corrigió en el fixture público, sin ampliar su lectura, y la repetición pasó. G-SEC-2.5 no leyó rutas privadas o entorno, no abrió sockets, no solicitó ni concedió consentimiento real y no habilita G-NORM-4R.

## Criterio de cierre de G-SEC-2 y siguiente gate posible

G-SEC-2 se considera **diseñado** cuando este documento y los documentos relacionados reflejen las mismas reglas. Se considera **revisado** solamente cuando Fernando confirme que entiende y acepta el diseño, sin que ello active datos reales. Un futuro G-SEC-2 de verificación requerirá demostrar los controles con fixtures sintéticos antes de solicitar el consentimiento granular de una operación real.

| Estado | Resultado | Consecuencia |
|---|---|---|
| Draft | Diseño documentado, con G-SEC-2.3a sintético ya pasado pero sin revisión humana completa de los cuatro controles. | G-NORM-4R bloqueado. |
| Review | Fernando confirmó los cuatro límites de diseño; G-SEC-2.1a, G-SEC-2.2a, G-SEC-2.3a, G-SEC-2.4a y G-SEC-2.5 pasaron exclusivamente con fixtures o documentos públicos. La ficha pública fue revisada y permanece vacía; siguen faltando una propuesta puntual futura, una tarjeta puntual real y consentimiento humano vigente. | Solo se puede diseñar pasos documentales posteriores, sin datos reales. |
| Active | Solo después de pruebas de control aprobadas y consentimiento puntual vigente. | Permite proponer, no ejecutar automáticamente, una única operación G-NORM-4R. |
| Blocked | Cualquier ambigüedad, salida externa, datos no permitidos, retención indefinida o consentimiento vencido. | No se abre evidencia ni se ejecuta ningún collector. |

Los documentos que requieren actualización conjunta son el contrato del shadow ledger, el plan de cifrado/G-NORM-4R, el proyecto de migración LUKS, la guía de APIs oficiales, `GrowthOS/todo.md` y el changelog. La actualización deberá registrar que G-SEC-2 está diseñado pero no aprobado para ejecutar datos reales.

### G-SEC-2.6 — consolidación final diseñada

La revisión final y matriz de consolidación se documentan en `2026-08-27_Revision_Final_Consolidacion_GSEC2_USM.md` v1.3. G-SEC-2.6 completó sus diez comprobaciones públicas como `Compatible` y registró `gsec2_consolidation_review_complete`. La revisión independiente posterior de G-SEC-2.4c confirmó la ficha pública vacía y sus diez controles, manteniéndola en `Review` sin propuesta, tarjeta o consentimiento. El procedimiento preliminar G-SEC-2.4c-P está documentado en `2026-08-27_Procedimiento_Preliminar_Propuesta_Minima_GSEC2_4c_USM.md` v1.5, también en `Review`, y solo describe la secuencia documental de una futura preparación sin crear una instancia. El gate G-SEC-2.4c-P.1 está documentado en `2026-08-27_Gate_Diseno_Propuesta_Hipotetica_Unica_GSEC2_4cP1_USM.md` v1.3, `Review`, y establece los límites previos de un diseño hipotético sin crearlo. G-SEC-2.4c-P.2 y su formato vacío están en `Review` como diseño documental, sin instancia de propuesta. Ninguno de estos resultados cambia el estado de este módulo ni permite tratar datos reales. G-SEC-2 permanece en `Review`.

## Referencias

[1] [NIST Privacy Framework](https://www.nist.gov/privacy-framework)

[2] [ICO — Principle (c): Data minimisation](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/data-minimisation/)

[3] [ICO — Principle (e): Storage limitation](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/storage-limitation/)

[4] [Shadow ledger privado append-only](2026-08-25_Shadow_Ledger_Privado_Append_Only_USM.md)

[5] [Plan comparativo de cifrado local para G-NORM-4R](2026-08-25_Plan_Decision_Cifrado_Local_G-NORM-4R.md)
