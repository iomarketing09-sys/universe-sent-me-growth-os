---
title: "Guía del piloto local con APIs oficiales de métricas — Universe Sent Me"
purpose: "Preparar en Xubuntu los collectors locales de TikTok y YouTube sin exponer secretos, sin escritura canónica y con monetización de YouTube cuando esté disponible."
status: Draft
created: 2026-08-25
updated: 2026-08-25
version: "3.2"
author: "Manus AI"
related_documents:
  - "Operations/Production/2026-08-23_Diseno_Asistencia_Metricas_y_Respuestas_OmniRoute.md"
  - "Operations/Automation/2026-08-25_Textos_Publicos_Terminos_Privacidad_App_Metricas_USM.md"
  - "Operations/Automation/2026-08-23_Diseno_Captura_Baseline_E0_E24_E72.md"
  - "GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
  - "GrowthOS/todo.md"
organization: "Operations/Automation"
---

# Guía del piloto local con APIs oficiales de métricas — Universe Sent Me

## Propósito y límites

Este piloto utiliza el equipo Xubuntu de Fernando para leer métricas oficiales de TikTok y YouTube de **Universe Sent Me**. No depende de Windsor.ai para operar, no publica contenido, no lee comentarios, no modifica calendarios y no escribe en los ledgers canónicos ni en Google Sheets durante la primera prueba. Bam in a Can y Firma Bordados están excluidos.

Los tres scripts se guardan en `Operations/Automation/`, pero la configuración real, los clientes OAuth, los tokens y la evidencia cruda residen **fuera** del repositorio en `~/.config/usm-metrics/` y `~/.local/share/usm-metrics/`. Esos directorios deben tener permisos restrictivos y nunca se suben a GitHub.

## Archivos preparados

| Archivo | Función | Contiene secretos |
| :--- | :--- | :--- |
| `official_metrics_config.example.json` | Plantilla de rutas, scopes y marca. | No. |
| `official_metrics_requirements.txt` | Dependencias de Python para los collectors. | No. |
| `authorize_tiktok_desktop.py` | Obtiene el consentimiento local de TikTok con PKCE. | No; lee valores locales del entorno. |
| `fetch_tiktok_official_metrics.py` | Recupera videos públicos y sus contadores nativos. | No; lee token local. |
| `fetch_youtube_official_metrics.py` | Recupera rendimiento y monetización estimada de YouTube. | No; lee cliente/token local. |

## Secuencia de activación prevista

La creación de apps y los consentimientos se realizan en el navegador de Fernando, sin compartir claves en la conversación. Primero se crea la app de escritorio de TikTok con los scopes mínimos oficiales `user.info.basic` y `video.list`, el callback `http://127.0.0.1:8765/callback/` y PKCE. Después se crea el cliente OAuth local de Google, se habilitan YouTube Data API y YouTube Analytics API, y se aprueban únicamente los scopes de lectura y monetización definidos en el documento de diseño.

Antes de correr los scripts se copia la plantilla hacia `~/.config/usm-metrics/config.json`, se ajustan solo rutas locales si hiciera falta y se instala el archivo de cliente de Google únicamente en la ruta privada indicada. Los valores de TikTok quedan en variables de entorno de la sesión local; no se guardan en la plantilla.

| Etapa | Resultado esperado | Si falla |
| :--- | :--- | :--- |
| Consentimiento TikTok | Token local con el scope exacto `video.list`. | Cancelar y revisar app, callback o scope; no registrar datos parciales. |
| Consentimiento YouTube | Token local con scopes de rendimiento y monetización. | Si monetización no está disponible, conservar rendimiento y registrar `monetization_status = not_available`. |
| Collector TikTok | Archivo privado de evidencia con videos y contadores capturados. | Registrar `collection_deferred`; no sustituir el fallo con datos de Windsor. |
| Collector YouTube | Evidencia privada de rendimiento y, cuando exista, monetización preliminar. | Retener `not_available` para campos ausentes; no escribir cero. |
| Revisión humana | Confirmación de marca, canal, ventanas y valores antes de normalizar. | No alimentar ledger, hoja ni OmniRoute. |

## Tratamiento de monetización

Los ingresos de YouTube son estimados y pueden ajustarse al cierre mensual. El piloto conserva `financial_status = preliminary`, la moneda y la ventana de extracción. Los importes exactos no pasan a OmniRoute por defecto; el modelo solo podrá recibir señales agregadas de tendencia cuando Fernando apruebe una etapa posterior de normalización.

## Gate de App Review y demo sandbox de TikTok

Antes de enviar la aplicación de TikTok a revisión, se debe completar una demostración real del flujo en **Sandbox**. La solicitud no debe presentarse mientras solo exista una página de políticas o mientras la integración esté en construcción. TikTok exige que la app muestre cada producto y scope seleccionado, que el video cubra la interacción completa y que la experiencia web mostrada use el dominio configurado como sitio oficial. [1]

El sandbox es el entorno correcto para probar esta integración sin afectar la configuración productiva. El operador debe crear un sandbox de la app, añadir únicamente una cuenta TikTok propia de Universe Sent Me como `Target User`, y después ejecutar la autorización con PKCE. Nunca se escribirán contraseñas, `client_secret`, tokens, códigos de autorización ni respuestas crudas en el repositorio, en la grabación o en el chat. [2]

| Elemento | Configuración permitida | Debe verse en la demo | Prohibido |
| :--- | :--- | :--- | :--- |
| Login Kit | Desktop, callback `http://127.0.0.1:8765/callback/`, PKCE. | Acción voluntaria para conectar TikTok, consentimiento sandbox y retorno al cliente local. | Login oculto, credenciales visibles o cuentas de otras marcas. |
| `user.info.basic` | Lectura mínima para identificar el perfil autorizado. | Estado de conexión y datos básicos mínimos del perfil sandbox. | PII adicional, mensajes, contactos o cuentas no autorizadas. |
| `video.list` / Display API | Lectura de videos públicos autorizados y sus contadores nativos. | Lista visible de videos sandbox devuelta por el flujo; se puede ocultar IDs y valores exactos si es necesario. | Publicar, editar, borrar, comentar, enviar mensajes o gestionar anuncios. |

### Texto propuesto para “Explain how each product and scope works”

> The Universe Sent Me Metrics App is a local desktop analytics tool operated by iO Marketing for authorized Universe Sent Me social accounts. Login Kit is used only when the authorized operator selects “Connect TikTok” in the local app. The operator completes TikTok authorization and returns through the local loopback callback using PKCE. The app requests `user.info.basic` only to confirm the authorized TikTok profile, and `video.list` only to retrieve the operator-authorized account’s public video metadata and native engagement counters through the Display API. The local interface displays the connection state, basic profile confirmation, and a read-only recent-video list to support internal performance review. OAuth tokens and raw API responses are stored only in restricted local directories outside GitHub and are not sent to OmniRoute. The app does not post content, edit or delete videos, manage comments, send messages, run ads, transfer funds, or access Bam in a Can, Firma Bordados, or unrelated accounts.

Este texto queda por debajo del límite de 1,000 caracteres, pero solo puede usarse si la demo muestra de forma fiel la interfaz local y el flujo descrito. No se debe alegar una funcionalidad que no se haya implementado ni ocultar que el acceso está restringido a operadores autorizados.

### Guion mínimo de demo real

La demostración debe ser una grabación de pantalla única, sin música ni edición engañosa, de aproximadamente 45–90 segundos y menor a 50 MB. Se grabará después de configurar el sandbox y debe ocultar cualquier secreto o token.

| Tiempo | Acción visible | Evidencia requerida |
| :--- | :--- | :--- |
| 0–10 s | Abrir la página oficial `https://iomarketing09-sys.github.io/usm-metrics-public/`. | Enlaces visibles y activos a Terms y Privacy. |
| 10–25 s | Abrir la interfaz local real de la app y seleccionar `Connect TikTok`. | La UI identifica Universe Sent Me y explica que el acceso es de solo lectura. |
| 25–45 s | Completar la autorización del usuario objetivo dentro del sandbox. | Pantalla de consentimiento y retorno al callback local, sin mostrar códigos ni tokens. |
| 45–75 s | Mostrar perfil básico confirmado y la lista de videos obtenida mediante `video.list`. | Estado `Connected`, alcance de lectura y ausencia de controles de escritura. |
| 75–90 s | Mostrar la pantalla de privacidad local o aviso de almacenamiento. | Tokens y raw permanecen locales; no hay publicación, comentarios, anuncios ni mensajería. |

Si el sandbox o la interfaz local no están listos, se debe guardar el formulario como Draft y no subir un video simulado o generado por IA. La revisión debe demostrar una integración funcional, no una maqueta.

### Verificación visual del Sandbox — 25 de agosto de 2026

Fernando proporcionó evidencia visual de la configuración Sandbox. El producto visible es **Login Kit**; el modal de productos no muestra otros productos activos. La lista de scopes presenta únicamente `user.info.basic` —incluido por Login Kit— y `video.list`. El redirect URI de Desktop es exactamente `http://127.0.0.1:8765/callback/`. En `Target Users` aparece un único registro: `universe.sent.me`, atribuido por Fernando a Universe Sent Me.

La siguiente prueba no presupone que el acceso esté operativo: el autorizador local debe confirmar el scope devuelto y el collector debe comprobar una llamada de lectura a `video.list`. Si TikTok devuelve que falta habilitar un producto o permiso, se detiene la ejecución, se documenta el error y se revisa el Sandbox; no se añaden alternativas de escritura, contenidos, mensajería, anuncios o cuentas de otras marcas.

### Autorización local confirmada — 25 de agosto de 2026

El flujo Desktop con PKCE se completó para el usuario objetivo de Sandbox. El autorizador local confirmó `status = authorized`, `brand = Universe Sent Me` y el scope exacto `user.info.basic,video.list`. El primer intento se detuvo antes del consentimiento porque TikTok rechazó el identificador de cliente; no produjo token. Tras verificar que se usaban las credenciales de la app correcta, TikTok entregó el callback local y el script guardó el token únicamente en la ruta privada configurada fuera del repositorio.

La autorización no es evidencia de lectura de métricas todavía. El próximo comando debe usar el collector para comprobar `video.list` de forma local; se conservará el resultado crudo solo como evidencia privada y no se actualizarán ledgers, Google Sheets, OmniRoute, calendarios ni contenido hasta una revisión humana posterior.

### Primera lectura Sandbox confirmada — 25 de agosto de 2026

El collector oficial se ejecutó con `--max-pages 1` y devolvió `status = collected`, `brand = Universe Sent Me`, `platform = TikTok` y `records = 9`. El archivo de evidencia cruda permanece bajo el directorio privado de Xubuntu definido en la configuración; no se trasladó a GitHub, Google Sheets, OmniRoute ni a ningún servicio de otra marca.

Este resultado demuestra conectividad y alcance de solo lectura de `video.list` dentro del Sandbox, no rendimiento definitivo ni una autorización para operar en Production. Antes de cualquier normalización se debe realizar una revisión humana local para atribuir los registros al Target User y confirmar los campos realmente devueltos. El piloto sigue sin cron, sin escritura canónica, sin importes financieros y sin automatización de respuestas o publicaciones.

## YouTube: primera lectura local de rendimiento

El proyecto exclusivo `USM Local Metrics` habilitó únicamente YouTube Data API v3 y YouTube Analytics API. El consentimiento OAuth local se configuró en modo de prueba mediante el cliente Desktop `USM Metrics Xubuntu Local`, cuyos archivos y token permanecen bajo `~/.config/usm-metrics/` fuera del repositorio.

El collector de YouTube confirmó `status = collected`, `brand = Universe Sent Me`, `platform = YouTube` y `performance_rows = 8`. La solicitud de monetización devolvió `monetization_status = not_available`. Esta ausencia se preserva tal cual: no equivale a ingresos cero, no se reintenta con permisos de escritura y no se envían importes ni errores financieros a OmniRoute.

Antes de interpretar resultados o pasar valores agregados a una vista derivada, Fernando debe revisar localmente las ocho filas para atribución al canal y coherencia de ventana. La lectura continúa sin cron, Google Sheets, ledgers, contenido, comentarios, programación ni cambios en otros proyectos.

## Meta: validador local GET-only para Facebook e Instagram

El runner histórico `run_daily_metrics_cut.py` no se usa para este gate porque escribe evidencia y análisis dentro del repositorio. En su lugar, `validate_meta_local_readonly.py` valida exclusivamente la conectividad y la autorización con solicitudes `GET`: primero comprueba que el token local devuelve la página `1036844829507460` de Universe Sent Me y, después, que la cuenta profesional vinculada devuelve el usuario esperado `universe_sent_me_0326`.

El validador recibe `USM_META_USER_ACCESS_TOKEN` únicamente desde el entorno de la terminal; no lo lee de archivos de proyecto ni lo imprime. Conserva un resumen mínimo de éxito o bloqueo bajo `~/.local/share/usm-metrics/evidence/`, fuera del repositorio, y no consulta publicaciones, comentarios, mensajes, insights ni endpoints de escritura. Cualquier fallo de token, página o permiso debe documentarse como bloqueo, sin interpretar ausencias como cero ni añadir scopes de escritura.

### Validación local confirmada — 25 de agosto de 2026

Fernando cargó temporalmente el token depurado ya aprobado de Meta en Xubuntu y ejecutó el validador. El resultado fue `status = validated`, `facebook_connection = validated` e `instagram_connection = validated`. La prueba acredita únicamente que la app aprobada de Universe Sent Me puede identificar la página Facebook prevista y la cuenta profesional Instagram vinculada, bajo solicitudes `GET` y con el token local.

No se solicitaron permisos nuevos, no se crearon aplicaciones nuevas, no se consultaron publicaciones, comentarios, mensajes o insights y no se modificaron ledgers, Google Sheets, OmniRoute, contenido o cuentas de otras marcas. Un futuro collector de métricas debe conservar estas mismas restricciones y pasar un gate separado de revisión antes de leer media o insights.

### Contrato de collectors Meta privados — lectura nativa únicamente

Los collectors Meta se limitarán a capturas manuales de acumulados nativos por publicación o media, sin inferir ventanas E0/E24/E72 ni solicitar insights. Para Facebook se consultará el feed de la página de Universe Sent Me con `GET`, filtrando registros publicados y solicitando solamente `id`, `created_time`, `is_published`, agregados de reacciones y comentarios, y `shares`. No se solicitarán `message`, enlaces, autores, perfiles, adjuntos, media URLs o datos de personas. Meta exige `pages_read_engagement` y `pages_read_user_content` para leer el feed propio de una página. [1]

Para Instagram se consultarán únicamente las media de la cuenta profesional enlazada, mediante `GET`, con `id`, `timestamp`, `media_type`, `media_product_type`, `like_count`, `comments_count`, y, cuando Meta los devuelva, `saved_count`, `shares_count`, `total_like_count`, `total_comments_count`, `total_views_count` y `reposts_count`. No se pedirán caption, media URL, permalink, comentarios, mensajes o insights. Los contadores pueden faltar por configuración de visibilidad, tipo de media o limitaciones de la API; el collector conservará esas ausencias como `not_available`, nunca como cero. La lectura de media con Facebook Login requiere `instagram_basic` y `pages_read_engagement`. [2]

Cada collector usará como máximo 25 registros por plataforma por ejecución, guardará raw estrictamente bajo `~/.local/share/usm-metrics/evidence/`, imprimirá solo un resumen no sensible y verificará que la marca sea Universe Sent Me. Los scripts no podrán realizar POST, PUT, PATCH o DELETE, ni escribir en el repositorio, Google Sheets, ledgers, OmniRoute, contenido, comentarios, calendarios o cualquier activo de otras marcas.

### Implementación revisada

Se implementaron `fetch_facebook_official_metrics.py` y `fetch_instagram_official_metrics.py`. Ambos scripts compilan con Python y una revisión estática confirmó que no contienen invocaciones `requests.post`, `requests.put`, `requests.patch` ni `requests.delete`. Los dos requieren `USM_META_USER_ACCESS_TOKEN` solo como variable temporal, producen un resumen seguro de `status`, `brand`, `platform` y número de registros, y guardan el detalle crudo únicamente en Xubuntu.

El collector de Facebook deriva un Page token de la página objetivo con el token de usuario, consulta hasta 25 posts publicados y retiene solo identificador, fecha, reacciones, comentarios y shares nativos. El collector de Instagram redescubre la cuenta profesional desde la página objetivo, valida el username esperado y consulta hasta 25 media con los campos nativos del contrato. Cualquier error de permiso, campo no soportado o cuenta no coincidente queda como `blocked`, sin reintentos que amplíen permisos.

### Primera captura privada confirmada — 25 de agosto de 2026

Fernando ejecutó ambos collectors usando temporalmente el token Meta ya aprobado de Universe Sent Me. Facebook devolvió `status = collected`, `brand = Universe Sent Me`, `platform = Facebook` y `records = 25`. Instagram devolvió `status = collected`, `brand = Universe Sent Me`, `platform = Instagram`, `records = 25` y `available_native_fields = 11`.

La captura confirma acceso de lectura para los campos contratados, no una autorización de integración productiva. El detalle se conserva fuera del repositorio en Xubuntu. Antes de crear vistas derivadas o cualquier normalización, solo se podrán mostrar resúmenes locales que excluyan IDs, textos, URLs, rutas de evidencia y cualquier dato de personas.

### Resúmenes locales seguros

`summarize_meta_private_metrics.py` es un lector local de la evidencia más reciente de Facebook o Instagram. No realiza llamadas remotas ni escribe archivos. Para Facebook presenta únicamente el rango de publicación, número de registros y, para reacciones, comentarios y shares, registros disponibles/no disponibles, total de los valores disponibles y mediana. Para Instagram presenta esos mismos conceptos por contador nativo disponible, además de la distribución de tipos de media y de superficie.

El generador prohíbe explícitamente cualquier salida de IDs, captions, textos, URLs, rutas de evidencia, tokens, datos personales o registros individuales. Sus totales son descriptivos y corresponden a contadores de vida al momento de captura; no son una normalización por ventana, una clasificación de contenido ni una recomendación de Growth OS.

## Esquema multicanal en revisión

El diseño `2026-08-25_Esquema_Normalizacion_Determinista_Multicanal_USM.md` define la futura estructura común de observaciones para TikTok, YouTube, Facebook e Instagram. Normaliza identidad, procedencia, ventana, disponibilidad y unidad, pero conserva toda métrica nativa en su propio nombre y prohíbe una columna universal de engagement o views. El esquema se mantiene en `Review`: no crea un ledger nuevo, no transforma evidencia privada en datos canónicos y no llena las pestañas derivadas de Google Sheets.

Los collectors locales actuales permanecen limitados a captura privada y resumen seguro. Cualquier implementación posterior debe pasar los gates de validación del esquema, append-only e idempotencia descritos en ese diseño antes de registrar una observación canónica.

### G-NORM-2: normalizador sintético dry-run validado

`normalize_metrics_dry_run.py` acepta exclusivamente un fixture JSON con `synthetic = true`. No realiza solicitudes de red, no lee variables de entorno, tokens o evidencia local, y no escribe archivos, ledgers, Google Sheets u OmniRoute. Produce en stdout observaciones normalizadas con `observation_key`, `transform_run_id`, versión del normalizador y estado de validación.

El fixture cubre una observación Facebook disponible, una ausencia válida de saves de Instagram, una observación TikTok de vida y una métrica diaria de porcentaje visto de YouTube por encima de 100, que se conserva sin recorte. Además incluye casos de marca incorrecta y valor nulo marcado erróneamente como disponible. La batería `validate_normalization_dry_run.py` verificó `NORM-01` a `NORM-12`, incluidos duplicados, ausencia explícita, métricas derivadas incompletas, evidencia no hasheada, datos monetarios no restringidos y campo prohibido.

El resultado del gate fue `synthetic_validation_passed` con 3 filas válidas, 1 parcial, 2 rechazadas y 0 duplicados en el lote base. Este resultado no autoriza utilizar evidencia real: el próximo posible paso es `G-NORM-3`, un piloto local privado, y requiere aprobación adicional de Fernando.

### G-NORM-3: piloto privado de cobertura preparado

Con aprobación de Fernando, `normalize_metrics_private_pilot.py` quedó preparado para ejecutar G-NORM-3. Lee únicamente el archivo más reciente de evidencia privada por plataforma y procesa en memoria un máximo de ocho registros fuente por TikTok, YouTube, Facebook e Instagram. No hace solicitudes de red, no necesita token, no persiste observaciones normalizadas y no modifica evidencia fuente, ledgers, Google Sheets, OmniRoute o calendarios.

El reporte imprime exclusivamente estado, cantidad de registros fuente disponibles, tamaño de muestra procesada, cantidad de observaciones normalizadas en memoria, validaciones, cobertura por nombre de métrica y disponibilidad. Nunca imprime IDs, captions, títulos, URLs, valores nativos, rutas, tokens, hashes ni filas normalizadas. Para YouTube, todo el bloque de monetización queda excluido incluso si existe en la evidencia; el reporte solo trabaja con las filas de rendimiento de la ventana cerrada. La validación contra fixtures sintéticos cubrió Facebook, Instagram, TikTok y YouTube sin filas rechazadas y confirmó que las ausencias se registran como parciales.

### Resultado de G-NORM-3 — 25 de agosto de 2026

El piloto local privado devolvió `private_pilot_coverage_complete` en las cuatro plataformas. Facebook procesó una muestra de 8 de 25 posts fuente: 22 observaciones válidas y 2 parciales porque shares solo estuvo disponible para 6 de los 8 posts. Instagram procesó 8 de 25 media: 37 observaciones válidas y 11 parciales; saves no estuvo disponible en los ocho media y views solo en cinco. TikTok procesó 8 de 9 videos y sus 32 observaciones fueron válidas. YouTube procesó las 8 filas de rendimiento disponibles y generó 72 observaciones válidas, con monetización excluida.

No hubo rechazos ni duplicados. El porcentaje de muestreo fue 32.00% para Facebook e Instagram, 88.88% para TikTok y 100.00% para YouTube. Estas tasas describen únicamente cobertura de adaptadores; no miden rendimiento, no son una normalización por ventana y no autorizan clasificar contenido. El siguiente gate posible es G-NORM-4, un shadow ledger privado append-only que requerirá una nueva aprobación humana.

### G-NORM-4: shadow ledger sintético validado

El diseño privado `2026-08-25_Shadow_Ledger_Privado_Append_Only_USM.md` y los scripts `shadow_ledger_private.py` y `validate_shadow_ledger_synthetic.py` implementan G-NORM-4 sin acceso a datos reales. La batería se ejecutó sobre una ruta temporal y confirmó: una inserción inicial, una reejecución idempotente que no agrega línea, rechazo de una colisión que intenta reemplazar una observación existente y una corrección con supersedencia append-only.

El archivo real, si se ejecuta posteriormente, residirá solo bajo `~/.local/share/usm-metrics/shadow-ledger/` con permisos restrictivos. Aun así, la implementación actual solo acepta `synthetic = true`. La demostración local de este mecanismo sigue pendiente; la inserción de observaciones reales privadas requiere un consentimiento distinto y no forma parte de G-NORM-4.

La demostración sintética se completó en Xubuntu con `shadow_ledger_synthetic_validation_passed`. La prueba confirmó inserción inicial, reejecución idempotente, rechazo de actualización in-place y supersedencia append-only, con garantías de no red y no escritura canónica. La ruta temporal usada fue eliminada por la batería. El mecanismo de inserción real continúa desactivado y requiere un consentimiento separado.

### Bloqueo de G-NORM-4R por almacenamiento no cifrado

El diagnóstico de Xubuntu mostró `/` montado directamente desde `sda2` como `ext4`, sin una capa `crypto_LUKS` o `crypt`. Dado que el consentimiento del piloto real exige cifrado local confirmado, G-NORM-4R queda bloqueado. No se adaptará el escritor para datos reales, no se creará el shadow ledger persistente y no se procesará ninguna muestra real hasta que se apruebe y complete una alternativa de almacenamiento protegido.

El trabajo permitido mientras tanto es sintético: fixtures, pruebas temporales, diseño, documentación y revisión del contrato. Cualquier migración de disco o creación de volumen cifrado requiere un plan local separado con respaldo previo y no forma parte de esta guía.

### Cobertura sintética ampliada

Se añadió `validate_synthetic_boundary_suite.py` para ejecutar el normalizador y el shadow ledger en el mismo proceso sintético con sockets bloqueados. La matriz ahora incluye disponibilidad mixta, porcentaje nativo mayor a 100, periodo cerrado con tier `C3_exact_window`, unidad nativa de minutos y rechazo de supersedencia desconocida. El resultado fue `synthetic_boundary_suite_passed`.

La suite no lee variables de entorno, raw, rutas privadas o tokens. El shadow ledger existe solo en un directorio temporal dentro de la prueba y se elimina al terminar. No se habilita reparación automática, recuperación de evidencia, inserción real ni almacenamiento en Drive o GitHub.

### Detección de corrupción temporal

La validación `validate_shadow_ledger_corruption_synthetic.py` ejecuta tres corrupciones intencionales y puramente sintéticas: JSONL truncado, evento `genesis` ausente y supersedencia contra una clave inexistente. El inspector de solo lectura informa la clase de inconsistencia sin imprimir filas, IDs, rutas o evidencia.

Antes y después de inspeccionar cada archivo, la suite compara sus bytes. La igualdad confirma que no existe reparación automática, reordenamiento, borrado o escritura de compensación. Este ejercicio tampoco habilita el ledger persistente, Drive, GitHub, Google Sheets, OmniRoute, cron ni observaciones reales.

### Semántica inválida con JSONL válido

La cobertura de integridad agrega cuatro archivos JSONL sintéticos que son formalmente legibles pero no cumplen el contrato: `genesis` de marca incorrecta, `record_type` desconocido, colisión de `observation_key` y `ledger_entry_key` alterado. El inspector los rechazó como `genesis_contract_invalid`, `record_type_invalid`, `observation_key_collision` y `entry_key_invalid`, sin elegir, reescribir ni reconstruir eventos.

Todos los casos permanecen bajo directorio temporal, con sockets bloqueados y comparación byte a byte antes y después de inspección. No se habilita una ruta de recuperación automática, ni un ledger real, ni un cambio del bloqueo de G-NORM-4R.

### Revisión descriptiva de la primera captura — 25 de agosto de 2026

El resumen de Facebook abarcó 25 posts publicados entre el 22 y el 25 de agosto de 2026. Los contadores nativos disponibles acumularon 3,702 reacciones, 261 comentarios y 785 shares. La mediana por post fue 31 reacciones, 2 comentarios y 9 shares entre los 22 registros para los que Meta devolvió shares; tres registros quedaron sin dicho contador y se conservan como no disponibles. Como referencia descriptiva, los promedios calculados sobre valores disponibles son 148.08 reacciones y 10.44 comentarios por registro, y 35.68 shares por registro con share disponible.

El resumen de Instagram abarcó 25 media entre el 4 y el 25 de agosto de 2026: 13 imágenes, 10 videos y 2 carruseles; 15 superficies `FEED` y 10 `REELS`. Los valores nativos disponibles fueron 30 likes, 0 comentarios, 1 share y 3 reposts. `saved_count` no fue devuelto para ningún registro, por lo que se conserva como no disponible. `total_views_count` estuvo disponible para 10 de 25 media y sumó 760; esos diez registros tuvieron una mediana de 67 vistas. Los demás quince registros no deben interpretarse como cero vistas.

Estas capturas mezclan edades y formatos, y los contadores son de vida. Por lo tanto, se prohíbe derivar rankings, ganadores, benchmarks o hipótesis de contenido a partir de esta lectura. La siguiente posible capa es una normalización determinista por publicación y ventana, sujeta a autorización independiente.

## Referencias

[1] [Meta Page Feed Reference](https://developers.facebook.com/docs/graph-api/reference/page/feed/)

[2] [Meta Instagram Media Reference](https://developers.facebook.com/documentation/instagram-platform/reference/instagram-media)

## Estado del documento

La guía es operativa pero no autoriza cron ni escrituras canónicas. Después de completar el consentimiento sandbox y las dos lecturas de prueba, deberá actualizarse junto con el documento de diseño, `GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md`, las pestañas derivadas de `USM Growth OS` y el changelog.

## Referencias

[1]: https://developers.tiktok.com/docs/en/app-review-guidelines "TikTok for Developers — App Review Guidelines"
[2]: https://developers.tiktok.com/doc/add-a-sandbox/ "TikTok for Developers — Add a Sandbox"
