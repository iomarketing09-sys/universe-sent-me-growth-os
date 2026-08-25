---
title: "Guía del piloto local con APIs oficiales de métricas — Universe Sent Me"
purpose: "Preparar en Xubuntu los collectors locales de TikTok y YouTube sin exponer secretos, sin escritura canónica y con monetización de YouTube cuando esté disponible."
status: Draft
created: 2026-08-25
updated: 2026-08-25
version: "1.7"
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

## Estado del documento

La guía es operativa pero no autoriza cron ni escrituras canónicas. Después de completar el consentimiento sandbox y las dos lecturas de prueba, deberá actualizarse junto con el documento de diseño, `GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md`, las pestañas derivadas de `USM Growth OS` y el changelog.

## Referencias

[1]: https://developers.tiktok.com/docs/en/app-review-guidelines "TikTok for Developers — App Review Guidelines"
[2]: https://developers.tiktok.com/doc/add-a-sandbox/ "TikTok for Developers — Add a Sandbox"
