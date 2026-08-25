---
title: "Pendientes operativos de GrowthOS"
purpose: "Consolidar pendientes exclusivos de GrowthOS y Universe Sent Me sin mezclar operaciones, infraestructura ni datos de clientes externos."
status: Active
created: 2026-08-25
updated: 2026-08-25
version: "3.3"
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
- [ ] Crear una app de escritorio de TikTok con los scopes oficiales mínimos `user.info.basic` y `video.list`, callback local con PKCE, más un cliente OAuth local de Google con scopes de lectura para YouTube Data, YouTube Analytics y monetización.
- [ ] Reemplazar la consulta de Windsor.ai por scripts locales de TikTok y YouTube antes del fin del Trial, manteniendo Facebook e Instagram en sus rutas existentes.
- [ ] Aprobar un piloto programado de solo lectura con cortes diarios, reporte semanal, hoja derivada y análisis de OmniRoute etiquetado `Draft`; no activar publicaciones, respuestas automáticas ni escrituras canónicas.
