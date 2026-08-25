---
title: "Pendientes operativos de GrowthOS"
purpose: "Consolidar pendientes exclusivos de GrowthOS y Universe Sent Me sin mezclar operaciones, infraestructura ni datos de clientes externos."
status: Active
created: 2026-08-25
updated: 2026-08-25
version: "1.3"
author: "Manus AI"
related_documents:
  - "GrowthOS/00_01_Changelog_GrowthOS.md"
organization: "GrowthOS"
---

# Pendientes operativos de GrowthOS

## Activos

- [x] Elegir la modalidad de piloto de métricas multicanal de Universe Sent Me: Fernando autorizó la modalidad B, loop multicanal programado.
- [x] Verificar la ruta de lectura de Instagram de Universe Sent Me: la cuenta `@universe_sent_me_0326` está activa y devuelve perfil, publicaciones e insights nativos por post en modo solo lectura.
- [ ] Confirmar las rutas de lectura autorizadas para TikTok y YouTube, y validar que cada fuente entregue los campos mínimos, la ventana y la fecha de extracción antes de automatizarla.
- [ ] Definir el contrato de datos, la ubicación segura de secretos, idempotencia, límites de tasa, mecanismo de pausa y destino de la hoja derivada para el loop programado.
- [ ] Aprobar la creación de pestañas derivadas en la hoja `USM Growth OS` o, si se prefiere, una hoja nueva exclusivamente de consulta; no modificar las pestañas históricas existentes sin aprobación.
- [ ] Aprobar un piloto programado de solo lectura con cortes diarios, reporte semanal, hoja derivada y análisis de OmniRoute etiquetado `Draft`; no activar publicaciones, respuestas automáticas ni escrituras canónicas.
