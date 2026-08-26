---
title: "Inventario previo a migración LUKS de Xubuntu — Universe Sent Me"
purpose: "Registrar los metadatos de aplicaciones, servicios y rutas que deben clasificarse para respaldo o recreación antes de una migración planificada de Xubuntu a LUKS integral."
status: Review
created: 2026-08-25
updated: 2026-08-25
version: "1.2"
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

## Resultado del inventario de Xubuntu

El recolector se ejecutó localmente y devolvió `inventory_metadata_only_complete`. El sistema reportado es Ubuntu 26.04 LTS sobre un único disco `sda` de 465.8 GB: `sda1` está destinado a EFI y `sda2` usa `ext4` para `/`. El volumen raíz dispone de 457 GB, con aproximadamente 24 GB en uso y 410 GB disponibles. No aparece un segundo medio utilizable: `sdb` reporta 0 B. Esto confirma que la alternativa seleccionada debe planear una migración integral respaldada, no un volumen dedicado sobre un disco ya disponible.

### Clasificación de aplicaciones y servicios

| Elemento identificado | Clasificación | Acción previa a migración |
|---|---|---|
| Ubuntu 26.04 LTS, Xubuntu Desktop y paquetes base | Recrear | Registrar la versión actual y preparar medio de instalación oficial; no respaldar el sistema como sustituto de una restauración probada. |
| Python 3.14.4, `pip`, Git, `curl`, `wget` | Recrear | Reinstalar desde fuentes oficiales y usar los manifests de dependencias para restaurar entornos. |
| Node 22.22.2 y npm 10.9.7 bajo NVM | Recrear con revisión | Registrar la versión NVM y reinstalar Node; las configuraciones personales de NVM se revisan como categoría privada. |
| Docker 29.1.3, servicio habilitado y activo | Recrear y validar | Reinstalar Docker y restaurar solo la configuración privada revisada manualmente; no se inspeccionó contenido de contenedores. |
| OmniRoute local | Respaldo protegido y recreación | El directorio `~/omniroute-pilot` existe y ocupa 8.0 MB. Su contenido no fue leído; debe revisarse manualmente como configuración privada antes de la migración. |
| Firefox, Thunderbird, Brave y WhatsApp Desktop | Decisión de respaldo general | No son requisitos del pipeline USM. Perfiles, mensajes y cuentas quedaron excluidos; Fernando decide el respaldo personal separado. |
| Snap, Flatpak y paquetes APT manuales | Recrear | El reporte conserva nombres/versiones suficientes para volver a instalar; no es necesario copiar cachés. |
| Timers de usuario | No restaurar por ahora | Solo se identificaron timers de mantenimiento del sistema, no una automatización USM activa. |

### Rutas de Universe Sent Me

| Ruta | Tamaño reportado | Clasificación | Tratamiento previo a migración |
|---|---:|---|---|
| `~/universe-sent-me-growth-os` | 281 MB | Código y documentación | Respaldar como copia de recuperación y confirmar que el remoto Git está sincronizado; no depende de datos raw. |
| `~/bin` | 8 KB | Scripts locales | Revisar nombres de scripts y respaldar como código; se identificó `omniroute-daily-wrapper.sh`. |
| `~/omniroute-pilot` | 8.0 MB | Configuración privada | Clasificar manualmente sin compartir su contenido; puede contener datos de operación o claves. |
| `~/.config/usm-metrics` | 20 KB, modo `0700` | Configuración privada sensible | Incluir solo en respaldo cifrado separado bajo revisión local; no enviar a GitHub, Drive o chat. |
| `~/.local/share/usm-metrics` | 151 MB, modo `0700` | Datos privados de métricas | Incluir solo en respaldo cifrado separado si se aprueba; no se leyó evidencia, raw ni tokens. |
| Entorno virtual USM | Paquetes identificados | Recrear | Generar un manifest de dependencias local tras revisión; el reporte identificó bibliotecas de Google OAuth/API y `requests`. |

### Rutas de usuario que requieren decisión de Fernando

| Ruta | Tamaño reportado | Decisión pendiente |
|---|---:|---|
| `~/Documents` | 24 KB | Determinar si contiene archivos personales o de trabajo que deban entrar al respaldo general. |
| `~/Pictures` | 5.0 MB | Determinar qué material pertenece a respaldo personal o a proyectos distintos de USM. |
| `~/Downloads` | 3.7 MB | Revisar y depurar manualmente antes de migrar; no se debe tratar como respaldo automático. |
| `~/Desktop` y `~/Videos` | 4 KB cada uno | Confirmar si son prescindibles o si contienen accesos/documentos relevantes. |

## Conclusiones para G-SEC-1A

El inventario confirma que no existe un dispositivo secundario listo para la alternativa B y que la decisión por LUKS integral es coherente con el estado actual. La siguiente preparación es seleccionar un **medio externo de respaldo**, con capacidad superior a los datos que Fernando decida conservar, y diseñar una copia separada que trate `~/.config/usm-metrics`, `~/.local/share/usm-metrics` y `~/omniroute-pilot` como categorías privadas que nunca se comparten por chat o repositorios.

Antes de solicitar autorización para migrar, todavía faltan: decisión de qué rutas personales se incluyen, medio de respaldo disponible, método de cifrado del respaldo, prueba de restauración de archivos no sensibles y ventana de mantenimiento. G-NORM-4R, la inserción real, cron, Google Sheets y OmniRoute con datos USM permanecen bloqueados.

## Capacidad recomendada para G-SEC-1A

Con 24 GiB usados en el sistema actual, una copia lógica con 50% de margen necesita aproximadamente 36 GiB y duplicar la ocupación actual requiere 48 GiB. Por ello, 64 GB es el mínimo técnico para una copia lógica limitada; se recomienda **128 GB o más** para conservar margen de revisión, prueba de restauración y crecimiento antes de migrar. Una imagen completa del disco no forma parte de esta ruta y requeriría un medio de aproximadamente 1 TB para evitar operar al límite.
