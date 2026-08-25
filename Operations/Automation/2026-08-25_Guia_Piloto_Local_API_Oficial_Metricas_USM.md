---
title: "Guía del piloto local con APIs oficiales de métricas — Universe Sent Me"
purpose: "Preparar en Xubuntu los collectors locales de TikTok y YouTube sin exponer secretos, sin escritura canónica y con monetización de YouTube cuando esté disponible."
status: Draft
created: 2026-08-25
updated: 2026-08-25
version: "1.0"
author: "Manus AI"
related_documents:
  - "Operations/Production/2026-08-23_Diseno_Asistencia_Metricas_y_Respuestas_OmniRoute.md"
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

La creación de apps y los consentimientos se realizan en el navegador de Fernando, sin compartir claves en la conversación. Primero se crea la app de escritorio de TikTok con `video.list`, el callback `http://127.0.0.1:8765/callback/` y PKCE. Después se crea el cliente OAuth local de Google, se habilitan YouTube Data API y YouTube Analytics API, y se aprueban únicamente los scopes de lectura y monetización definidos en el documento de diseño.

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

## Estado del documento

La guía es operativa pero no autoriza cron ni escrituras canónicas. Después de completar los consentimientos y las dos lecturas de prueba, deberá actualizarse junto con el documento de diseño, `GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md`, las pestañas derivadas de `USM Growth OS` y el changelog.
