---
title: "Proyecto de migración integral a LUKS — Universe Sent Me"
purpose: "Definir los gates y la secuencia reversible para reinstalar Xubuntu con cifrado LUKS integral después de validar el respaldo cifrado previo."
status: Draft
created: 2026-08-26
updated: 2026-08-26
version: "0.2"
author: "Manus AI"
related_documents:
  - "Operations/Automation/2026-08-25_Plan_Decision_Cifrado_Local_G-NORM-4R.md"
  - "Operations/Automation/2026-08-25_Diseno_Respaldo_Cifrado_Pre_LUKS_USM.md"
  - "Operations/Automation/2026-08-25_Inventario_Previa_Migracion_LUKS_Xubuntu_USM.md"
  - "Operations/Automation/2026-08-25_Consentimiento_Piloto_Real_Shadow_Ledger_USM.md"
  - "GrowthOS/todo.md"
organization: "Operations/Automation"
---

# Proyecto de migración integral a LUKS

## Propósito y límite de esta fase

Universe Sent Me seleccionó la Ruta A: una reinstalación planificada de Xubuntu con cifrado LUKS integral. El respaldo externo previo ya existe, su checksum fue validado y una restauración controlada pasó; ello reduce el riesgo de recuperación, pero **no autoriza aún** modificar el disco interno.

Este documento es un plano de proyecto. No crea medios booteables, no descarga ISOs, no borra particiones, no ejecuta `cryptsetup`, no cifra discos y no restaura datos. Cada fase de escritura o cambio de disco requiere una autorización independiente.

> Ubuntu documenta que LUKS cifra datos a nivel de bloques y que el desbloqueo con contraseña depende de la fortaleza de esa contraseña. [1]

## Estado de partida validado

| Elemento | Estado actual |
|---|---|
| Disco interno | Un solo disco `sda` de aproximadamente 465.8 GB; raíz actual `sda2 ext4`, sin LUKS. |
| Ruta seleccionada | Reinstalación limpia con LUKS integral, no conversión in-place. |
| Respaldo previo | Ciphertext `age` único en `/dev/sdc3` (`vfat`, label `Fernando`), checksum y restauración controlada validados. |
| Recuperación del backup | Dos copias físicas separadas bajo control de Fernando; la frase no se almacena en este proyecto. |
| Datos reales y automatización | Siguen bloqueados hasta que la migración y su validación posterior estén completas. |

## Inspección final de medios G-MIG-LUKS-1.2

La inspección local de solo lectura confirmó `sda` como el único disco interno, con `sda2 ext4` montado en `/`. El respaldo `age` en `sdc3` (`vfat`, label `Fernando`) volvió a validar su checksum como `OK`. No se ejecutó ningún comando de montaje, borrado, formato o escritura.

La USB de 8 GB usada previamente aparece como `sdb`, pero informa capacidad `0 B`; se clasifica como **no utilizable**. El único candidato seleccionado para el medio de instalación es `sdd`: USB de 28.9 GB, partición `sdd1` `vfat`, label `STORE N GO`, montada en `/run/media/universe-sent-me/STORE N GO`. Esta selección no autoriza borrarla: cualquier creación de medio requerirá el gate G-MIG-LUKS-1.3 y una nueva confirmación explícita de que se acepta borrar **solo `sdd`**.

## Arquitectura objetivo

La ruta objetivo es una instalación limpia de Xubuntu con **LUKS protegido por frase de arranque**. El cargador y la partición EFI pueden permanecer sin cifrar por necesidades de arranque; el sistema de archivos raíz y los datos de usuario deben residir dentro del volumen LUKS. Se elegirá el flujo exacto que ofrezca el instalador oficial de la versión verificada en el momento de la instalación; no se asumirá soporte TPM ni se improvisará una tabla de particiones manual.

El nuevo usuario local debe conservar el nombre `universe-sent-me` salvo que Fernando decida otra cosa antes del gate de instalación. Mantenerlo facilita restaurar las rutas autorizadas sin alterar los límites documentados, pero no elimina la necesidad de validar permisos y funcionamiento después de restaurar.

## Gates de migración

| Gate | Propósito | ¿Escribe o modifica discos? |
|---|---|---|
| G-MIG-LUKS-1.1 | Confirmar USB vacío de al menos 16 GB, acceso al disco externo, tiempo de mantenimiento, alimentación estable y decisión de reinstalación limpia. | No. |
| G-MIG-LUKS-1.2 | Inspección final de solo lectura: identidad de `sda`, montaje del respaldo y verificación de checksum. | No. |
| G-MIG-LUKS-1.3 | Crear medio booteable oficial y verificar su integridad. | Sí, solo borra el USB aprobado. |
| G-MIG-LUKS-1.4 | Revisión visual del instalador y confirmación de que apunta al disco interno correcto. | No hasta el paso de confirmación del instalador. |
| G-MIG-LUKS-1.5 | Instalar Xubuntu con LUKS integral mediante el instalador, borrando exclusivamente el disco interno aprobado. | Sí, operación destructiva sobre `sda`. |
| G-MIG-LUKS-1.6 | Verificar después del primer arranque que la raíz está respaldada por `crypto_LUKS`/`crypt`, que arranca con frase y que no hay error de montaje. | No. |
| G-MIG-LUKS-1.7 | Instalar herramientas mínimas y restaurar selectivamente el entorno USM desde el ciphertext, con la frase ingresada localmente. | Sí, escribe sobre el nuevo sistema cifrado. |
| G-MIG-LUKS-1.8 | Validar collectors en modo sintético/read-only, OmniRoute local y el contrato de privacidad antes de abrir G-NORM-4R. | No datos reales persistentes. |

## Secuencia operativa propuesta

| Fase | Acción | Criterio para continuar |
|---|---|---|
| A. Preparar | Elegir USB exclusivamente para instalador y resguardar el disco `Fernando` como respaldo fuera de línea. | G-MIG-LUKS-1.1 aprobado. |
| B. Verificar | Identificar por modelo/tamaño el disco interno y comprobar nuevamente el ciphertext sin descifrar. | G-MIG-LUKS-1.2 aprobado. |
| C. Medio | Descargar la ISO oficial correspondiente, verificar su checksum y escribir el USB aprobado. | G-MIG-LUKS-1.3 aprobado. |
| D. Instalar | Arrancar desde USB, elegir cifrado en el instalador oficial y detenerse antes de cualquier pantalla que destruya `sda` para una última aprobación. | G-MIG-LUKS-1.4 y luego 1.5 aprobados por separado. |
| E. Verificar LUKS | Confirmar cadena de bloques cifrada, arranque, red y actualización base. | G-MIG-LUKS-1.6 completado. |
| F. Recuperar USM | Instalar `age`, restaurar solo las raíces autorizadas al sistema ya cifrado, comprobar scripts y mantener el backup externo intacto. | G-MIG-LUKS-1.7 aprobado. |
| G. Retomar operación | Ejecutar pruebas sintéticas/read-only y revisar privacidad antes de abrir gates de datos reales. | G-MIG-LUKS-1.8 completado. |

## Requisitos antes de crear el medio de instalación

La siguiente decisión práctica es reservar un USB vacío de **al menos 16 GB** para el instalador. Ese USB se borrará completamente durante la creación del medio y no debe ser el disco externo `Fernando`, el cual conserva el respaldo cifrado. También se requiere acceso continuo a la frase de arranque LUKS que Fernando elegirá y a las dos copias físicas de la frase de recuperación `age`, sin compartir ninguna de ellas por chat.

Antes de la instalación debe haber alimentación estable, tiempo suficiente para interrupciones y la confirmación de que no existe otro sistema operativo o dato no inventariado en `sda` que deba preservarse. El proyecto asume reinstalación limpia del único disco interno; si aparece una partición o requisito nuevo, el plan se detendrá y se revisará.

## Exclusiones y controles de separación

La migración no mezcla datos, código ni credenciales de Firma Bordados, Bam in a Can u otras marcas. No sube el ciphertext a Drive ni a GitHub, no usa Drive como ledger y no habilita automatización, Sheets, cron, OmniRoute con datos reales ni G-NORM-4R. La restauración posterior se realizará solo al sistema ya cifrado y nunca desde el medio externo en formato abierto.

## Referencias

[1] [Ubuntu Security Documentation — Full disk encryption](https://documentation.ubuntu.com/security/security-features/storage/encryption-full-disk/)
