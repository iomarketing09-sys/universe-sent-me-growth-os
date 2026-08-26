---
title: "Plan B rEFInd para selección temporal de USB — Universe Sent Me"
purpose: "Recuperar de forma reversible el selector de arranque necesario para revisar la USB instaladora de Xubuntu, sin autorizar todavía la instalación de Xubuntu ni operaciones de disco."
status: Review
created: 2026-08-26
updated: 2026-08-26
version: "1.2"
author: "Manus AI"
related_documents:
  - "Operations/Automation/2026-08-26_Proyecto_Migracion_LUKS_Integral_USM.md"
  - "Operations/Automation/2026-08-25_Plan_Decision_Cifrado_Local_G-NORM-4R.md"
  - "Operations/Automation/2026-08-25_Diseno_Respaldo_Cifrado_Pre_LUKS_USM.md"
  - "GrowthOS/todo.md"
organization: "Operations/Automation"
---

# Plan B rEFInd para selección temporal de USB

## Propósito y límite estricto

Este plan responde a un bloqueo concreto: el iMac Intel no reconoce de forma fiable la tecla Option/Alt del teclado no original, y el intento de una sola vez con la entrada rEFInd antigua `Boot0080` volvió al Xubuntu interno. La USB reutilizable de Xubuntu 26.04 sigue siendo legible y válida, pero todavía no ha sido arrancada para revisar visualmente su instalador.

El objetivo limitado es reinstalar **rEFInd como selector de arranque** para elegir la USB solo durante la revisión no destructiva G-MIG-LUKS-1.4. No instala Xubuntu, no cifra LUKS, no formatea, no particiona, no altera `EFI/ubuntu`, no toca el disco externo `Fernando` y no desbloquea los gates de datos reales. La instalación de rEFInd sí escribe archivos EFI y una entrada UEFI/NVRAM, por lo que requiere una autorización separada y explícita.

> `refind-install` instala rEFInd en la partición de sistema EFI (ESP) y, normalmente, crea una entrada NVRAM que describe su ubicación. [1]

## Hechos locales validados

| Control | Resultado validado | Implicación para el plan |
|---|---|---|
| Sistema de partida | Xubuntu actual arranca por `Boot0000` mediante `\EFI\ubuntu\shimx64.efi`. | Es la ruta de regreso que se preserva y prueba antes de cualquier retirada. |
| ESP | La ESP montada en `/boot/efi` mostró únicamente `EFI/BOOT` y `EFI/ubuntu`, con aproximadamente 1.1 GB disponibles. | No existe rEFInd actual que actualizar ni se requiere sobrescribir Ubuntu. |
| Entrada antigua | `Boot0080` apunta a `\EFI\refind\refind_x64.efi` en una ubicación antigua que ya no está presente. `BootNext=0080` se consumió y el equipo volvió a Ubuntu. | La entrada no se reutiliza ni se elimina como parte de esta fase; la nueva entrada se identificará después de instalar. |
| Paquete | `refind` candidato: `0.14.2-2.1` desde el repositorio Ubuntu configurado. | Se usará el paquete de la distribución, no un binario descargado manualmente. |
| Secure Boot | El equipo informó que no soporta Secure Boot. | No se planifican shim, MOK, firma local ni llaves adicionales. |
| USB instaladora | Xubuntu 26.04 amd64, USB Cruze, ISO9660 con ESP y cargador `EFI/boot/bootx64.efi`. | Debe estar conectada durante la prueba visual, sin reescribirla. |

Las letras `/dev/sdX` son variables y no forman parte de ningún comando de instalación. Cada preflight vuelve a identificar la ESP mediante su punto de montaje `/boot/efi`, no mediante una letra histórica.

## Alternativas vigentes

| Ruta | Cambio persistente | Ventaja | Límite | Estado |
|---|---|---|---|---|
| A. Teclado Apple o Mac compatible por cable | Ninguno. | Es la vía de menor riesgo; Apple indica Option/Alt para abrir Startup Manager en Mac Intel. [2] | Requiere disponer temporalmente de un teclado que el firmware reconozca. | Sigue disponible. |
| B. rEFInd documentado | Sí: paquete local, archivos bajo `EFI/refind` y una entrada NVRAM nueva. | No depende de que Option/Alt sea reconocido por el teclado actual. | Añade una etapa técnica que debe retirarse cuidadosamente si deja de ser necesaria. | Preferencia actual; aún no autorizado para ejecutar. |

## Preflight obligatorio, sin escritura

Antes de solicitar instalación se ejecutará exclusivamente `Operations/Automation/plan_refind_usb_selector.sh --plan`. El wrapper no usa `apt install`, `refind-install`, `efibootmgr -c`, `efibootmgr -o`, `efibootmgr -B`, montaje, borrado ni modificación de firmware. Solo informa el montaje de `/boot/efi`, espacio, árbol EFI, versión candidata, estado Secure Boot y, si el operador autoriza su lectura con contraseña local, las variables UEFI actuales.

El resultado debe confirmar que el Xubuntu actual sigue arrancado, que `/boot/efi` es una ESP `vfat` montada, que `EFI/ubuntu` continúa presente, que el paquete candidato existe y que Secure Boot no está soportado. La USB Xubuntu debe estar conectada para la prueba posterior, mientras que el disco externo `Fernando` debe permanecer desconectado para evitar ambigüedad de medios. No se pide, registra ni transmite ninguna frase de recuperación.

## Cambio propuesto para una autorización futura

La autorización futura debe decir expresamente que permite **instalar rEFInd desde el paquete Ubuntu y crear sus archivos EFI/NVRAM**, pero no permite instalar Xubuntu ni modificar el disco interno. Tras recibirla, la secuencia será la siguiente.

| Paso | Acción prevista | Cambio persistente | Control de seguridad |
|---|---|---|---|
| 1 | Volver a ejecutar el preflight y guardar una copia de `efibootmgr -v`, árbol `EFI` y `BootOrder` en una ruta local restringida. | Sí, solo evidencia local no sensible. | Si `Boot0000` o `EFI/ubuntu` no aparecen, se detiene. |
| 2 | Instalar el paquete `refind` desde el repositorio Ubuntu configurado, revisando sus mensajes interactivos. | Sí, instala paquete y puede colocar archivos EFI. | No se usa `--yes`, ni fuente externa, ni USB como destino. |
| 3 | Ejecutar o confirmar el resultado de `refind-install --nodrivers` solamente si el instalador del paquete no creó una instalación funcional. | Sí, copia rEFInd bajo `EFI/refind` y registra una entrada NVRAM. | La opción `--nodrivers` evita copiar controladores de filesystem no necesarios para este objetivo; no se usan shim ni `--usedefault`. [1] |
| 4 | Capturar el estado posterior y comparar `EFI/ubuntu`, `Boot0000`, la nueva ruta `EFI/refind` y el nuevo `Boot####` real. | Sí, evidencia local no sensible. | No se modifica `BootOrder` manualmente; se registra cualquier cambio producido por el instalador. |
| 5 | Reiniciar con la USB Xubuntu conectada y usar rEFInd para elegir la entrada que corresponda a la USB. | No modifica discos. | Se entra al instalador solo para revisión visual y se detiene antes de cualquier pantalla de cambio de disco. |
| 6 | Volver a Xubuntu actual y comprobar que `Boot0000` y `EFI/ubuntu` continúan arrancables. | No. | Esta comprobación es requisito previo para retirar rEFInd. |

El comando `refind-install` puede añadir una entrada NVRAM y copia archivos a la ESP; sus errores deben leerse antes de continuar. [1] El plan evita `--usedefault`, pues ese modo usa `EFI/BOOT/bootx64.efi`, una ubicación compartida que no se debe sustituir en este equipo. [1]

## Validación de la revisión USB

Al aparecer rEFInd se seleccionará únicamente la entrada que identifique la USB Xubuntu. Si rEFInd muestra solo el sistema interno, o si no aparece, se detiene y se vuelve a Xubuntu sin instalar nada. Una sesión rEFInd no es autorización para pulsar acciones del instalador que borren, particionen, formateen o cifren el disco interno.

La revisión G-MIG-LUKS-1.4 termina al comprobar visualmente si el instalador ofrece cifrado y al salir sin aplicar cambios. El siguiente gate destructivo G-MIG-LUKS-1.5 sigue siendo independiente y requerirá autorización nueva, explícita y específica para el disco interno identificado en ese momento.

## Ejecución registrada de G-MIG-LUKS-1.4f

Fernando autorizó la instalación y ejecutó el preflight final el 26 de agosto de 2026. El snapshot previo se guardó localmente bajo `/var/lib/usm-migration/refind-snapshots/20260826T181952Z`. Después, `apt` instaló `refind` `0.14.2-2.1` y su dependencia `gawk`, sin actualizaciones ni eliminaciones de paquetes.

| Verificación posterior | Resultado | Estado |
|---|---|---|
| Ruta nueva | Existe `EFI/refind/refind_x64.efi` y `EFI/refind/refind.conf`, junto con iconos, llaves y el driver `ext4_x64.efi`. | Confirmado. |
| Cargador Ubuntu | `EFI/ubuntu/shimx64.efi` y `EFI/ubuntu/grubx64.efi` continúan presentes. | Confirmado. |
| Entrada Ubuntu | `Boot0000` sigue apuntando a `\EFI\ubuntu\shimx64.efi`. | Confirmado. |
| Entrada rEFInd nueva | `Boot0001` apunta a `\EFI\refind\refind_x64.efi` sobre la misma ESP actual. | Confirmado. |
| Orden de arranque | El instalador dejó `BootOrder: 0001,0000,0080`; rEFInd quedó primero, Ubuntu segundo y `Boot0080` antiguo permanece sin tocar. | Confirmado; pendiente de prueba de arranque. |
| Discos y respaldo | No se instalaron Xubuntu ni LUKS, no se modificaron particiones y el disco `Fernando` permaneció fuera de la operación. | Confirmado. |

La comparación automatizada con `diff` no pudo leer la sustitución de proceso mediante `sudo` (`/dev/fd/63`), pero las salidas directas de EFI y NVRAM permiten verificar las rutas y entradas anteriores. El próximo control no escribe: reiniciar una sola vez con la USB Xubuntu conectada, observar rEFInd y seleccionar únicamente el medio USB. Si no aparece o no lista la USB, se vuelve a Ubuntu sin entrar al instalador y se detiene para diagnóstico.

## Validación de arranque y revisión visual completadas

El primer arranque de rEFInd fue correcto. Con el disco `Fernando` desconectado, rEFInd mostró la USB y la entrada `Boot EFI\boot\grubx64.efi from ESP`, consistente con el cargador de la USB Xubuntu previamente inspeccionada. Esa entrada llevó al escritorio de prueba de Xubuntu 26.04; no hubo modificación de medios.

Durante la revisión interactiva se seleccionaron idioma, teclado, red disponible, instalación interactiva y **Xubuntu Desktop**. Las dos opciones de software propietario y códecs se dejaron desmarcadas. La pantalla **Disk setup** mostró: instalar junto a Ubuntu 26.04 LTS, borrar Ubuntu 26.04 LTS, borrar el disco e instalación manual. No se seleccionó ni confirmó ninguna de ellas.

> La interfaz de disco observada no mostró una opción visible de cifrado LUKS dentro de los flujos guiados. Este hecho no prueba que el instalador no pueda configurarse manualmente con LUKS; confirma únicamente que no se encontró una ruta guiada de cifrado en esta revisión.

El instalador se cerró sin aplicar cambios. rEFInd volvió a mostrar el cargador interno `EFI\ubuntu\grubx64.efi` sobre el volumen FAT de 1 GiB, y el sistema actual inició correctamente. La comprobación posterior devolvió `BootCurrent=0001`, esperable porque el firmware inició rEFInd; `Boot0000` para `EFI\ubuntu\shimx64.efi` continúa intacto y `BootOrder=0001,0000,0080` mantiene Ubuntu como respaldo.

## Reversión condicionada a la evidencia posterior

La reversión no se ejecutará por suposición ni con identificadores heredados. Solo después de confirmar que `Boot0000` inicia correctamente y de registrar el `Boot####` realmente creado por el paso de instalación, el operador podrá autorizar una retirada separada.

| Orden | Acción futura de reversión | Condición obligatoria |
|---|---|---|
| 1 | Arrancar por el Ubuntu interno verificado y ejecutar un preflight final. | `Boot0000` y `EFI/ubuntu` están presentes y funcionan. |
| 2 | Comparar el snapshot antes/después e identificar el directorio EFI y `Boot####` creados realmente para rEFInd. | La evidencia coincide con la ruta y entrada de rEFInd; no se actúa sobre `Boot0080` antiguo. |
| 3 | Restituir el `BootOrder` anterior solo si el instalador lo cambió y solo usando la lista exacta capturada antes de instalar. | No se construye un orden por memoria ni se elimina `Boot0000`. |
| 4 | Eliminar exclusivamente la entrada UEFI recién creada mediante su identificador real y el directorio rEFInd confirmado. | Requiere autorización explícita de retirada y revisión humana del identificador. |
| 5 | Retirar el paquete y verificar que Ubuntu sigue arrancando por `Boot0000`. | La ruta Ubuntu sigue intacta; `EFI/ubuntu` nunca se borra ni modifica. |

`efibootmgr` documenta que `BootNext` aplica solo al siguiente arranque y se elimina tras su uso; por esa razón, el intento anterior no dejó un cambio de orden persistente. [3] La misma herramienta permite crear, borrar y cambiar el orden de las entradas, por lo que no se utilizarán sus opciones de escritura sin una autorización puntual que indique el identificador concreto. [3]

## Fuera de alcance

Este plan no modifica el respaldo cifrado `age`, no copia datos de USM a la ESP, no utiliza Drive o GitHub como respaldo, no inicia LUKS, no instala Xubuntu, no activa G-NORM-4R, no usa datos reales de collectors, no toca OmniRoute ni mezcla recursos de Firma Bordados o Bam in a Can.

## Referencias

[1] [Debian Manpages — refind-install(8)](https://manpages.debian.org/testing/refind/refind-install.8)

[2] [Apple Support — Mac startup key combinations](https://support.apple.com/en-us/102603)

[3] [Ubuntu Manpages — efibootmgr(8)](https://manpages.ubuntu.com/manpages/focal/man8/efibootmgr.8.html)
