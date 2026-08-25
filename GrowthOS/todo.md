---
title: "Pendientes operativos de GrowthOS"
purpose: "Consolidar pendientes exclusivos de GrowthOS y Universe Sent Me sin mezclar operaciones, infraestructura ni datos de clientes externos."
status: Active
created: 2026-08-25
updated: 2026-08-25
version: "1.8"
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
- [ ] Identificar cuál de las cuentas/canales de YouTube administrados por iO Marketing corresponde exclusivamente a Universe Sent Me antes de consultar o automatizar datos de YouTube; excluir de este loop los datos de Bam in a Can y Firma Bordados.
- [ ] Elegir la fuente sostenible: APIs oficiales locales sin cuota de intermediario, Windsor.ai como integración de pago, o una combinación transitoria solo de lectura.
- [ ] Aprobar un piloto programado de solo lectura con cortes diarios, reporte semanal, hoja derivada y análisis de OmniRoute etiquetado `Draft`; no activar publicaciones, respuestas automáticas ni escrituras canónicas.
