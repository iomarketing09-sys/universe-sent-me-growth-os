---
title: "Inventario previo a migración LUKS de Xubuntu — Universe Sent Me"
purpose: "Registrar los metadatos de aplicaciones, servicios y rutas que deben clasificarse para respaldo o recreación antes de una migración planificada de Xubuntu a LUKS integral."
status: Draft
created: 2026-08-25
updated: 2026-08-25
version: "1.0"
author: "Manus AI"
related_documents:
  - "Operations/Automation/2026-08-25_Plan_Decision_Cifrado_Local_G-NORM-4R.md"
  - "Operations/Automation/2026-08-25_Consentimiento_Piloto_Real_Shadow_Ledger_USM.md"
  - "Operations/Automation/2026-08-25_Hoja_Ruta_Automatizacion_Local_Segura_USM.md"
  - "GrowthOS/todo.md"
organization: "Operations/Automation"
---

# Inventario previo a migración LUKS de Xubuntu

## Propósito y estado

Este documento organiza el inventario previo al respaldo requerido por G-SEC-1A. La fuente de datos será el recolector `collect_xubuntu_backup_inventory.sh`, que obtiene metadatos locales no sensibles y no modifica el equipo. Aún no se ha recibido el reporte de Xubuntu; por ello, el inventario detallado de elementos presentes permanece pendiente.

## Exclusiones obligatorias

El recolector y este documento nunca deben incluir valores de variables de entorno, tokens, credenciales, API keys, datos raw, evidencia privada, IDs de contenido, hashes de evidencia, browser profiles, SSH/GPG keys, emails, mensajes, documentos, imágenes, videos o contenidos de OmniRoute. Los elementos privados se clasificarán por **ruta y categoría**, no por su contenido.

## Categorías de clasificación posteriores

| Categoría | Criterio | Ejemplos esperados |
|---|---|---|
| Respaldar en medio cifrado separado | No se puede reconstruir de forma segura y es necesario para continuidad. | Configuración privada USM y datos locales autorizados, revisados sin exponerlos. |
| Respaldar como código/documentación | Puede restaurarse desde un repositorio Git, pero conviene tener una copia adicional de recuperación. | Scripts locales y checkout del repositorio. |
| Recrear tras la migración | Se reinstala desde fuentes oficiales o manifest de paquetes. | Python, Docker, Git, Node, dependencias de venv y aplicaciones del sistema. |
| Validar y decidir manualmente | Puede contener secretos o datos privados; nunca se comparte en reporte. | OmniRoute data/config, perfiles de navegador, directorios USM privados. |
| Excluir del respaldo de proyecto | No es necesario para USM o pertenece a cuentas/marcas fuera de alcance. | Cachés, descargas temporales, artefactos regenerables y datos de otras marcas. |

## Rutas que requieren clasificación, no inspección de contenido

| Ruta o categoría | Acción de inventario | Decisión de respaldo pendiente |
|---|---|---|
| `~/bin` | Registrar nombres y tamaños de scripts. | Revisar scripts relevantes y respaldar como código. |
| `~/omniroute-pilot` | Registrar solo existencia, permisos y tamaño. | Revisar manualmente como configuración privada; no enviar contenido por chat. |
| `~/.config/usm-metrics` | Registrar solo metadatos. | Determinar copia cifrada local para continuidad, sin exponer secretos. |
| `~/.local/share/usm-metrics` | Registrar solo metadatos. | Determinar copia cifrada local; nunca enviar evidencia/raw a GitHub. |
| Entorno virtual USM | Registrar nombres/versiones de paquetes. | Recrear desde manifest después de migración; confirmar dependencias. |
| Contenedores locales | Registrar nombre, imagen y estado; no inspeccionar configuración. | Recrear con configuración privada revisada manualmente. |
| Documentos/media de usuario | Registrar solo tamaño de carpetas. | Fernando decide qué pertenece al respaldo general del equipo. |

## Siguiente acción no destructiva

Fernando ejecutará el recolector de metadatos en Xubuntu, revisará el texto generado y compartirá únicamente el reporte filtrado. Con el resultado se completará la tabla de aplicaciones y rutas presentes, se marcarán elementos para respaldo o recreación y se definirá una prueba de restauración. No se copiará, borrará, comprimirá ni migrará ningún archivo en esta fase.
