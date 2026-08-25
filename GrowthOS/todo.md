---
title: "Pendientes operativos de GrowthOS"
purpose: "Consolidar pendientes exclusivos de GrowthOS y Universe Sent Me sin mezclar operaciones, infraestructura ni datos de clientes externos."
status: Active
created: 2026-08-25
updated: 2026-08-25
version: "5.8"
author: "Manus AI"
related_documents:
  - "GrowthOS/00_01_Changelog_GrowthOS.md"
organization: "GrowthOS"
---

# Pendientes operativos de GrowthOS

## Activos

- [x] Elegir la modalidad de piloto de métricas multicanal de Universe Sent Me: Fernando autorizó la modalidad B, loop multicanal programado.
- [x] Verificar la ruta de lectura de Instagram de Universe Sent Me: la cuenta `@universe_sent_me_0326` está activa y devuelve perfil, publicaciones e insights nativos por post en modo solo lectura.
- [x] Seleccionar las rutas propuestas para TikTok y YouTube: Fernando autorizó evaluar Windsor.ai únicamente en modo lectura para alimentar el loop local.
- [ ] Definir el contrato de datos, la ubicación segura de secretos, idempotencia, límites de tasa, mecanismo de pausa y destino de la hoja derivada para el loop programado.
- [x] Crear las pestañas derivadas `Metrics_Daily_View`, `Weekly_Growth_Draft` y `Data_Quality` dentro de `USM Growth OS`, sin modificar las pestañas históricas existentes.
- [x] Elegir el equipo Xubuntu local de Fernando, junto a OmniRoute, como runtime del loop; comparar antes el costo de una alternativa alojada independiente.
- [x] Autorizar una prueba de conexión de Windsor.ai en modo solo lectura y sin crear pagos, para confirmar la cobertura orgánica de TikTok y YouTube.
- [x] Comparar Windsor.ai contra las APIs oficiales de TikTok y YouTube, más alternativas gratuitas/de menor costo que entreguen métricas orgánicas suficientes para el loop local.
- [x] Validar Windsor.ai en modo solo lectura para TikTok: la cuenta Universe Sent Me devuelve métricas de video, alcance, acciones, watch time y tasa de finalización.
- [x] Identificar y excluir el canal `https://www.youtube.com/@Bam_in_a_can` como Bam in a Can; sus métricas no entran en el loop de Universe Sent Me.
- [x] Identificar el canal de YouTube exclusivo de Universe Sent Me como `https://www.youtube.com/@Universe_Sent_Me`; Firma Bordados permanece excluida de este loop.
- [x] Verificar en modo solo lectura que la conexión de Windsor.ai asociada al canal `@Universe_Sent_Me` devuelve métricas por Short, incluyendo views, engaged views, likes, comentarios, shares, porcentaje visto y suscriptores ganados.
- [x] Elegir la fuente sostenible: Fernando eligió APIs oficiales locales sin cuota de intermediario; Windsor.ai queda solo como referencia de lectura durante los cuatro días restantes de Trial.
- [ ] Añadir una capa de monetización de YouTube de solo lectura, con el scope monetario oficial y campos de ingresos únicamente si el canal es elegible y devuelve datos; mantener los importes crudos fuera de los briefs de OmniRoute salvo autorización financiera separada.
- [x] Aprobar el gate técnico para preparar clientes OAuth de solo lectura, scripts locales sin secretos y pruebas controladas de TikTok/YouTube con monetización; no incluye publicación, pagos ni permisos de escritura.
- [x] Confirmar una app de TikTok existente, vacía y creada por Fernando como contenedor exclusivo para el acceso de Universe Sent Me; no reutilizarla para Bam in a Can ni Firma Bordados.
- [x] Confirmar la URL pública existente de privacidad de Universe Sent Me: `https://iomarketin.wixstudio.com/universesentme/privacypolicyusm`.
- [ ] Confirmar la URL pública existente de términos de servicio de Universe Sent Me antes de reutilizar ambas rutas para TikTok.
- [x] Confirmar que Wix no permite publicar un archivo `.txt` arbitrario en la ruta exacta exigida por TikTok; no usar Media Manager ni pulsar `Verify` con una URL distinta.
- [x] Elegir GitHub Pages dedicado como host alternativo gratuito de Universe Sent Me para términos, privacidad y la firma de TikTok; Fernando autorizó crear un repositorio público mínimo sin métricas, credenciales, PII ni recursos de Firma Bordados.
- [x] Crear y enviar el contenido mínimo al repositorio público exclusivo `iomarketing09-sys/usm-metrics-public`: `index.html`, `/terms/`, `/privacy/` y reglas de no incluir secretos ni datos de otras marcas.
- [x] Habilitar GitHub Pages manualmente desde `Settings → Pages` usando `main` y `/(root)`; se validaron `https://iomarketing09-sys.github.io/usm-metrics-public/terms/` y `https://iomarketing09-sys.github.io/usm-metrics-public/privacy/` como rutas públicas.
- [x] Confirmar el canal público de contacto autorizado para las páginas de términos y privacidad: `io_marketin_09@gmail.com`; la versión desplegada fue verificada.
- [x] Sustituir las URLs Wix por las URLs públicas de Pages dentro de TikTok y publicar la firma de verificación de Terms of Use en su ruta exacta; HTTP `200`, tipo `text/plain` y contenido cotejado contra el archivo recibido.
- [x] Recibir la firma de verificación de Privacy Policy que TikTok generó para el prefijo GitHub Pages, publicarla bajo el directorio exacto solicitado y validar HTTP `200`, tipo `text/plain` y contenido idéntico antes de pulsar `Verify`.
- [x] Recibir, publicar y validar la firma de TikTok para la Web/Desktop URL principal en la raíz de GitHub Pages; HTTP `200`, tipo `text/plain` y contenido idéntico al archivo recibido.
- [ ] Pulsar `Verify` en TikTok para Terms of Use, Privacy Policy y Web/Desktop URL, registrar el resultado individual de cada bloque y no configurar productos o credenciales OAuth hasta que todas las validaciones estén confirmadas.
- [ ] Preparar el texto de App Review que explique exclusivamente Login Kit y Display API para Universe Sent Me, con scopes `user.info.basic` y `video.list`, lectura local y sin publicación, mensajes, comentarios, anuncios ni otros permisos.
- [ ] Grabar una demo real en el sandbox de TikTok que muestre el flujo completo de escritorio: inicio local, autorización de sandbox, callback loopback y lectura de datos de video; no incluir secretos, tokens visibles, datos de Bam in a Can ni Firma Bordados.
- [ ] Revisar que los productos y scopes mostrados en la demo coincidan exactamente con la solicitud antes de enviar App Review; retirar cualquier producto o scope no utilizado.
- [x] Elegir Sandbox de TikTok como ruta inmediata para el piloto local de Universe Sent Me; no enviar App Review ni afirmar que la app está lista para producción.
- [ ] Confirmar en TikTok el resultado de las tres verificaciones de URL (Terms of Use, Privacy Policy y Web/Desktop URL) antes de activar productos en el sandbox.
- [x] Crear el sandbox exclusivo `USM Metrics Read Only`, sin clonar productos de escritura y sin importar configuración a Production; Fernando reportó la configuración finalizada.
- [x] Añadir únicamente una cuenta TikTok propia de Universe Sent Me como Target User del sandbox; excluir Bam in a Can, Firma Bordados, cualquier cliente y cuentas ajenas; Fernando reportó la configuración finalizada.
- [x] Configurar en el sandbox únicamente Login Kit y TikTok API/Display API con `user.info.basic` y `video.list`, más `http://127.0.0.1:8765/callback/`; no activar Content Posting, comentarios, mensajes, anuncios ni scopes adicionales; Fernando reportó la configuración finalizada.
- [x] Confirmar visualmente en el Sandbox: Login Kit como único producto; `user.info.basic` y `video.list` como únicos scopes; callback `http://127.0.0.1:8765/callback/`; y un solo Target User `universe.sent.me` de Universe Sent Me. No aparecieron otros productos activos.
- [x] Validar en el flujo local que el token Sandbox autorizado incluye exactamente `user.info.basic` y `video.list`: el autorizador Desktop/PKCE confirmó `status=authorized` y `brand=Universe Sent Me`; el token quedó fuera del repositorio.
- [x] Ejecutar una primera lectura local con el collector TikTok y confirmar que `video.list` funciona en Sandbox: `status=collected`, `brand=Universe Sent Me`, `platform=TikTok`, `records=9`; evidencia cruda conservada solo en Xubuntu.
- [ ] Revisar de forma local y humana la evidencia privada del Sandbox para confirmar que los 9 registros son de la cuenta objetivo y que los campos nativos disponibles se ajustan al contrato; no normalizar, no escribir Google Sheets ni enviar raw a OmniRoute aún.
- [x] Cerrar el piloto TikTok en estado Sandbox validado, sin integrar a Production, sin cron y sin llevar sus datos a ledgers, Sheets u OmniRoute; toda futura integración requiere un gate separado.
- [x] Crear el proyecto de Google Cloud exclusivo `USM Local Metrics` para iO Marketing / Universe Sent Me y habilitar únicamente YouTube Data API v3 y YouTube Analytics API; no se mezclaron Firma Bordados ni clientes.
- [x] Configurar el consentimiento OAuth de Google para prueba local, crear el cliente Desktop `USM Metrics Xubuntu Local` y guardar el archivo descargado solo en `~/.config/usm-metrics/youtube-client-secret.json` con permisos restrictivos; no se subió a GitHub ni se compartió en chat.
- [x] Autorizar localmente el canal `@Universe_Sent_Me` con los scopes exactos `youtube.readonly`, `yt-analytics.readonly` y `yt-analytics-monetary.readonly`; no se solicitaron scopes de publicación, edición, comentarios, administración ni cuentas de otras marcas.
- [x] Ejecutar una primera lectura local de YouTube: `status=collected`, `brand=Universe Sent Me`, `platform=YouTube`, `performance_rows=8` y `monetization_status=not_available`; no se tratará la ausencia como cero.
- [ ] Revisar local y humanamente las ocho filas de rendimiento disponibles para confirmar atribución y ventanas de fecha; mantener cualquier importe o error de monetización en evidencia privada, fuera de OmniRoute y sin aprobación financiera separada.
- [ ] Mostrar localmente un resumen legible de las ocho filas de YouTube sin revelar IDs, rutas, tokens ni valores monetarios; conservar toda evidencia fuente en Xubuntu.
- [x] Inventariar el patrón local Meta existente sin leer ni exponer secretos y confirmar que la app aprobada y el token depurado corresponden exactamente a Universe Sent Me.
- [x] Preparar y compilar `validate_meta_local_readonly.py`, un validador oficial Meta GET-only que usa un token solo desde entorno local, guarda evidencia únicamente fuera del repositorio y no contiene POST/PUT/PATCH/DELETE.
- [x] Localizar y cargar temporalmente en Xubuntu el token depurado de la app Meta ya aprobada para Universe Sent Me; no se creó otra app, no se solicitaron permisos nuevos, no se expuso el token y no se persistió en el repositorio.
- [x] Ejecutar una prueba acotada GET-only mediante APIs oficiales locales: `status=validated`, `facebook_connection=validated` e `instagram_connection=validated` para las cuentas objetivo de Universe Sent Me; no hubo publicación, comentarios, respuestas, edición, Sheets, ledgers ni OmniRoute.
- [x] Registrar el resultado de la prueba Meta sin convertir datos ausentes en cero ni añadir scopes de escritura; la evidencia mínima quedó privada en Xubuntu.
- [x] Definir y documentar el contrato de los collectors Meta privados: campos nativos, ventanas de captura, cuenta objetivo, evidencia local y métricas que permanecerán `not_available` sin inferencia.
- [x] Implementar `fetch_facebook_official_metrics.py` y `fetch_instagram_official_metrics.py` como collectors locales GET-only de Universe Sent Me, usando solo el token temporal `USM_META_USER_ACCESS_TOKEN` y guardando raw bajo `~/.local/share/usm-metrics/evidence/`.
- [x] Compilar y revisar los collectors para prohibir POST/PUT/PATCH/DELETE, así como cualquier escritura en GitHub, Sheets, ledgers, contenido, comentarios, calendarios u OmniRoute.
- [x] Ejecutar una primera captura manual de ambos collectors: Facebook `status=collected`, `records=25`; Instagram `status=collected`, `records=25`, `available_native_fields=11`; no se ampliaron permisos ni se movió raw fuera de Xubuntu.
- [ ] Mostrar y revisar localmente resúmenes seguros de las primeras capturas Meta, sin IDs, textos de publicaciones, URLs, rutas de evidencia o datos de personas; no normalizar ni enviar raw a OmniRoute todavía.
- [ ] Inventariar el sitio actual de Universe Sent Me en Wix y evaluar una migración futura como proyecto separado; no ejecutar cambios de Wix, DNS, dominio, analítica ni hosting durante esta evaluación.
- [x] Configurar y autorizar la app de escritorio Sandbox de TikTok con los scopes oficiales mínimos `user.info.basic` y `video.list`, callback local y PKCE; el cliente OAuth local de Google con scopes de lectura y monetización sigue pendiente.
- [ ] Reemplazar la consulta de Windsor.ai por scripts locales de TikTok y YouTube antes del fin del Trial, manteniendo Facebook e Instagram en sus rutas existentes.
- [ ] Aprobar un piloto programado de solo lectura con cortes diarios, reporte semanal, hoja derivada y análisis de OmniRoute etiquetado `Draft`; no activar publicaciones, respuestas automáticas ni escrituras canónicas.
