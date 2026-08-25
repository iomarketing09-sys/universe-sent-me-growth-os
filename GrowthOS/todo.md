---
title: "Pendientes operativos de GrowthOS"
purpose: "Consolidar pendientes exclusivos de GrowthOS y Universe Sent Me sin mezclar operaciones, infraestructura ni datos de clientes externos."
status: Active
created: 2026-08-25
updated: 2026-08-25
version: "4.7"
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
- [ ] Validar en el flujo local que el token sandbox autorizado incluye exactamente `user.info.basic` y `video.list`, y que la llamada de lectura `video.list` funciona; si falla por producto no disponible, detenerse y revisar la configuración Sandbox sin añadir scopes o productos de escritura.
- [ ] Inventariar el sitio actual de Universe Sent Me en Wix y evaluar una migración futura como proyecto separado; no ejecutar cambios de Wix, DNS, dominio, analítica ni hosting durante esta evaluación.
- [ ] Crear una app de escritorio de TikTok con los scopes oficiales mínimos `user.info.basic` y `video.list`, callback local con PKCE, más un cliente OAuth local de Google con scopes de lectura para YouTube Data, YouTube Analytics y monetización.
- [ ] Reemplazar la consulta de Windsor.ai por scripts locales de TikTok y YouTube antes del fin del Trial, manteniendo Facebook e Instagram en sus rutas existentes.
- [ ] Aprobar un piloto programado de solo lectura con cortes diarios, reporte semanal, hoja derivada y análisis de OmniRoute etiquetado `Draft`; no activar publicaciones, respuestas automáticas ni escrituras canónicas.
