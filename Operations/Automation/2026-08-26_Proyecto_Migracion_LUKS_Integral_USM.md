---
title: "Proyecto de migración integral a LUKS — Universe Sent Me"
purpose: "Definir los gates y la secuencia reversible para reinstalar Xubuntu con cifrado LUKS integral después de validar el respaldo cifrado previo."
status: Active
created: 2026-08-26
updated: 2026-08-27
version: "1.24"
author: "Manus AI"
related_documents:
  - "Operations/Automation/2026-08-25_Plan_Decision_Cifrado_Local_G-NORM-4R.md"
  - "Operations/Automation/2026-08-25_Diseno_Respaldo_Cifrado_Pre_LUKS_USM.md"
  - "Operations/Automation/2026-08-25_Inventario_Previa_Migracion_LUKS_Xubuntu_USM.md"
  - "Operations/Automation/2026-08-25_Consentimiento_Piloto_Real_Shadow_Ledger_USM.md"
  - "Operations/Automation/2026-08-26_Plan_B_rEFInd_Seleccion_USB_USM.md"
  - "Operations/Automation/preflight_usm_synthetic_after_luks.sh"
  - "Operations/Automation/inspect_omniroute_passive_after_luks.sh"
  - "Operations/Automation/preflight_collectors_static_after_luks.sh"
  - "Operations/Automation/validate_collectors_static_contract.py"
  - "Operations/Automation/validate_synthetic_boundary_suite.py"
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

## Medio oficial propuesto para G-MIG-LUKS-1.3

El objetivo propuesto es **Xubuntu 26.04 LTS, Desktop 64-bit**. La ISO se descargará desde el canal oficial de Xubuntu a una carpeta local del sistema, nunca directamente a la USB, y se contrastará contra el archivo oficial `SHA256SUMS` antes de elegir el medio. Xubuntu identifica 26.04 como una versión LTS publicada en abril de 2026 y ofrece el checksum SHA-256 oficial para sus ISOs. [2]

Para la creación del USB se usará preferentemente **Startup Disk Creator** en la interfaz de Xubuntu, tras verificar visualmente que el destino sea la USB `STORE N GO` de 28.9 GB. La documentación oficial indica que el proceso sobrescribe y destruye los datos del USB, por lo que no se usará un comando `dd` manual. [3] Justo antes de escribir, se repetirá `lsblk` y se exigirá que `sda` y `sdc` sigan identificados como disco interno y disco de respaldo, respectivamente. Si cambian letras, capacidad, modelo o montajes, el proceso se detiene.

### Decisión de reutilización del instalador existente

La inspección posterior detectó la USB existente como `sdd`, USB de 7.2 GB modelo Cruze. Contiene `Xubuntu 26.04 amd64` en ISO9660, partición ESP y una partición `writable`; por tanto, satisface el objetivo de medio Xubuntu 26.04 LTS y se reutilizará sin reescritura. El checksum del respaldo en `Fernando` volvió a validar `OK` durante la inspección. `STORE N GO` no se borrará mientras esta USB siga disponible y legible.

El siguiente gate es iniciar una **revisión visual del instalador** desde la USB reutilizada. Esta revisión permite comprobar que el medio arranca y que ofrece cifrado, pero se detiene antes de cualquier pantalla que pueda modificar `sda`. Arrancar desde USB exige una autorización de reinicio separada; no equivale a autorización de instalación.

## Arquitectura objetivo

La ruta objetivo es una instalación limpia de Xubuntu con **LUKS protegido por frase de arranque**. El cargador y la partición EFI pueden permanecer sin cifrar por necesidades de arranque; el sistema de archivos raíz y los datos de usuario deben residir dentro del volumen LUKS. Se elegirá el flujo exacto que ofrezca el instalador oficial de la versión verificada en el momento de la instalación; no se asumirá soporte TPM ni se improvisará una tabla de particiones manual.

El nuevo usuario local debe conservar el nombre `universe-sent-me` salvo que Fernando decida otra cosa antes del gate de instalación. Mantenerlo facilita restaurar las rutas autorizadas sin alterar los límites documentados, pero no elimina la necesidad de validar permisos y funcionamiento después de restaurar.

## Gates de migración

| Gate | Propósito | ¿Escribe o modifica discos? |
|---|---|---|
| G-MIG-LUKS-1.1 | Confirmar USB vacío de al menos 16 GB, acceso al disco externo, tiempo de mantenimiento, alimentación estable y decisión de reinstalación limpia. | No. |
| G-MIG-LUKS-1.2 | Inspección final de solo lectura: identidad de `sda`, montaje del respaldo y verificación de checksum. | No. |
| G-MIG-LUKS-1.3 | Crear medio booteable oficial y verificar su integridad. | Sí, solo borra el USB aprobado. |
| G-MIG-LUKS-1.4f | Instalar opcionalmente rEFInd para seleccionar la USB, bajo un plan reversible y autorización independiente. | Sí, solo ESP/NVRAM; no particiones, cifrado ni datos. |
| G-MIG-LUKS-1.4 | Revisión visual del instalador y confirmación de que apunta al disco interno correcto. | No hasta el paso de confirmación del instalador. |
| G-MIG-LUKS-1.4g | Verificar visualmente la ruta guiada `Erase disk` → `Encrypt with a passphrase` y la pantalla de resumen, sin confirmar instalación. | No. |
| G-MIG-LUKS-1.5 | Instalar Xubuntu con LUKS integral mediante el instalador, borrando exclusivamente el disco interno aprobado. | Sí, operación destructiva sobre `sda`. |
| G-MIG-LUKS-1.6 | Verificar después del primer arranque que la raíz está respaldada por `crypto_LUKS`/`crypt`, que arranca con frase y que no hay error de montaje. | No. |
| G-MIG-LUKS-1.7 | Instalar herramientas mínimas y restaurar selectivamente el entorno USM desde el ciphertext, con la frase ingresada localmente. | Sí, escribe sobre el nuevo sistema cifrado. |
| G-MIG-LUKS-1.8 | Validar herramientas recuperadas con fixtures sintéticos, sin red, sin servicios y sin datos reales; OmniRoute y collectors se revisan primero solo por presencia/configuración. | No datos reales persistentes. |

## Secuencia operativa propuesta

| Fase | Acción | Criterio para continuar |
|---|---|---|
| A. Preparar | Elegir USB exclusivamente para instalador y resguardar el disco `Fernando` como respaldo fuera de línea. | G-MIG-LUKS-1.1 aprobado. |
| B. Verificar | Identificar por modelo/tamaño el disco interno y comprobar nuevamente el ciphertext sin descifrar. | G-MIG-LUKS-1.2 aprobado. |
| C. Medio | Descargar la ISO oficial correspondiente, verificar su checksum y escribir el USB aprobado. | G-MIG-LUKS-1.3 aprobado. |
| C.1 Selector opcional | Recuperar un selector USB mediante teclado compatible o rEFInd reversible, si el firmware sigue bloqueando Option/Alt. | G-MIG-LUKS-1.4f aprobado por separado si usa rEFInd. |
| D. Confirmar cifrado | Verificar dentro del instalador la página guiada de cifrado por frase y el resumen de instalación, sin aplicar. | G-MIG-LUKS-1.4g aprobado. |
| E. Instalar | Arrancar desde USB, elegir cifrado en el instalador oficial y detenerse en el resumen antes de cualquier confirmación destructiva. | G-MIG-LUKS-1.5 aprobado por separado. |
| F. Verificar LUKS | Confirmar cadena de bloques cifrada, arranque, red y actualización base. | G-MIG-LUKS-1.6 completado. |
| G. Recuperar USM | Instalar `age`, restaurar solo las raíces autorizadas al sistema ya cifrado, comprobar scripts y mantener el backup externo intacto. | G-MIG-LUKS-1.7 aprobado. |
| H. Retomar operación | Ejecutar pruebas sintéticas/read-only y revisar privacidad antes de abrir gates de datos reales. | G-MIG-LUKS-1.8 completado; siguen pendientes controles humanos de privacidad, retención, operación read-only y consentimiento granular. |

## Requisitos antes de crear el medio de instalación

La siguiente decisión práctica es reservar un USB vacío de **al menos 16 GB** para el instalador. Ese USB se borrará completamente durante la creación del medio y no debe ser el disco externo `Fernando`, el cual conserva el respaldo cifrado. También se requiere acceso continuo a la frase de arranque LUKS que Fernando elegirá y a las dos copias físicas de la frase de recuperación `age`, sin compartir ninguna de ellas por chat.

## Bloqueo de selección USB y Plan B rEFInd

La USB reutilizada contiene un instalador Xubuntu 26.04 válido, pero no pudo seleccionarse desde el iMac Intel con el teclado actual: Option/Alt no fue reconocido, la entrada rEFInd histórica `Boot0080` estaba rota y un intento de `BootNext` volvió al sistema interno. La consola GRUB del sistema interno tampoco expuso el cargador de la USB. Ninguno de esos diagnósticos modificó particiones, archivos EFI, orden persistente de arranque ni datos.

El proyecto conserva dos rutas: conseguir temporalmente un teclado Apple/Mac compatible por cable, sin cambios persistentes; o instalar rEFInd mediante el plan Draft `2026-08-26_Plan_B_rEFInd_Seleccion_USB_USM.md`. La segunda ruta requiere una aprobación distinta porque instala un paquete, escribe una ruta nueva bajo `EFI/refind` y puede crear una entrada UEFI/NVRAM. No autoriza la instalación Xubuntu ni G-MIG-LUKS-1.5.

Fernando autorizó y ejecutó G-MIG-LUKS-1.4f. El paquete `refind` creó `EFI/refind/refind_x64.efi` y la entrada nueva `Boot0001`, dejando `Boot0000` y `EFI/ubuntu` presentes. El instalador cambió el orden a `0001,0000,0080`; rEFInd arrancó después tanto la USB reutilizada como el Xubuntu interno, el cual permanece sano.

La revisión visual G-MIG-LUKS-1.4 llegó a **Disk setup** sin seleccionar ni confirmar ninguna operación. La lista inicial mostró instalar junto a Ubuntu, borrar Ubuntu, borrar disco e instalación manual. La documentación oficial de Ubuntu 26.04 aclara que la ruta de cifrado aparece **después de seleccionar** `Erase disk and install Ubuntu`: allí se puede elegir `Encrypt with a passphrase`, la opción recomendada que combina LVM con cifrado de disco. [4] [5]

G-MIG-LUKS-1.4g confirmó esta ruta en el instalador Xubuntu: la pantalla **Encryption and file system** mostró `Encrypt with a passphrase` con el texto `This uses LVM with LUKS encryption`. No se seleccionó opción, no se ingresó frase, no se avanzó al resumen y el instalador se cerró. El Xubuntu interno volvió a iniciar correctamente. Por tanto, el método guiado propuesto está validado; G-MIG-LUKS-1.5 sigue separado y bloqueado hasta contar con el preflight final y la autorización destructiva específica.

## Ejecución y verificación LUKS completadas

Tras el preflight final, Fernando autorizó explícitamente borrar solo el disco interno `ST3500418AS / sda`. El resumen del instalador identificó ese disco, Xubuntu Desktop, **LUKS (LVM)** y todas las particiones de la USB Xubuntu `sdc` como `Unchanged`. Después de pulsar el único botón irreversible `Install`, la instalación terminó y solicitó la frase LUKS antes de abrir el escritorio nuevo.

La validación G-MIG-LUKS-1.6 se ejecutó antes de conectar `Fernando` o restaurar USM. La evidencia de solo lectura confirmó Ubuntu 26.04, `/dev/sda3` con `crypto_LUKS`, el mapper activo `dm_crypt-0`, el volumen lógico `ubuntu--vg-ubuntu--lv` montado como raíz `/`, `/dev/sda2` como `/boot` y `/dev/sda1` como ESP. Esta topología es consistente con el cifrado LUKS guiado por frase validado en el instalador. El gate G-MIG-LUKS-1.7 permanece separado: requiere un preflight y una autorización específica para conectar, verificar y restaurar selectivamente desde el ciphertext `age`.

El preflight G-MIG-LUKS-1.7a ya confirmó en el sistema cifrado `age` 1.2.1, Git 2.53.0 y el clon canónico del repositorio. Con `Fernando` conectado como `/dev/sdc3` `vfat`, se verificaron sin descifrar las cinco piezas del backup y el SHA-256 del ciphertext de 307,792,785 bytes. El diseño de G-MIG-LUKS-1.7b restaurará selectivamente `bin` y las tres raíces privadas aprobadas, mientras conserva el repositorio actual clonado desde GitHub como fuente canónica. Sigue pendiente una autorización específica para descifrar localmente y mover esas rutas al sistema LUKS.

G-MIG-LUKS-1.7b se completó tras autorización: el wrapper volvió a validar el ciphertext, solicitó la frase `age` solo localmente y restauró `bin` y las tres raíces privadas aprobadas al volumen LUKS. Los cuatro destinos quedaron con modo `0700` y propietario `universe-sent-me`; no quedó staging temporal, el repositorio GitHub se preservó y no se iniciaron procesos de OmniRoute o USM. `Fernando` no recibió escritura. El siguiente gate G-MIG-LUKS-1.8 se limita a reinstalar y probar herramientas locales con fixtures sintéticos/read-only, sin datos reales persistentes ni automatización activa.

## Diseño de preflight G-MIG-LUKS-1.8

G-MIG-LUKS-1.8 inicia con el wrapper `preflight_usm_synthetic_after_luks.sh`. Su modo `--plan` no lee el entorno operativo; `--preflight` revisa exclusivamente la presencia del repositorio, Python local, fixtures y scripts candidatos, y comprueba que no haya procesos OmniRoute, Docker Compose, collectors, cron o servicios de datos activos. No importa configuraciones privadas, no abre evidencia, no llama APIs y no escribe archivos.

La primera prueba candidata es `validate_synthetic_boundary_suite.py`, ejecutada solo con Python estándar y la opción `-B` para no producir bytecode. El suite intercepta la apertura de sockets, ejecuta el normalizador contra `fixtures/normalization_dry_run_synthetic.json` y prueba el shadow ledger únicamente en un `TemporaryDirectory`; su resultado debe incluir `synthetic_only`, `network_socket_blocked`, `temporary_ledger_only` y `no_canonical_write`.

| Subgate | Acción permitida | Prohibiciones |
|---|---|---|
| G-MIG-LUKS-1.8a | Ejecutar preflight de inventario y el suite sintético sin red, tras una aprobación separada. | No instalar dependencias de collectors, no leer tokens/evidencia, no crear ledger persistente. |
| G-MIG-LUKS-1.8b | Diseñar por separado la comprobación de presencia de Docker/OmniRoute, sin iniciar contenedores. | No iniciar OmniRoute ni enviar entradas, aun sintéticas, hasta revisar configuración y puertos. |
| G-MIG-LUKS-1.8c | Revisar contratos y dependencias de collectors solo por código/configuración de ejemplo. | No ejecutar collectors, OAuth, API GET, escritura de evidencia, cron o Sheets. |

El éxito de G-MIG-LUKS-1.8a no abre G-NORM-4R. Antes de cualquier observación real siguen siendo obligatorios la renovación de privacidad, retención, consentimiento granular y la decisión humana de permitir una operación real mínima.

G-MIG-LUKS-1.8a se ejecutó tras autorización en Python 3.14.4. El preflight confirmó los fixtures, el repositorio y la ausencia de procesos OmniRoute, Docker Compose o collectors. El suite validó NORM-01 a NORM-12 y cinco protecciones del shadow ledger; reportó `synthetic_only`, `network_socket_blocked`, `temporary_ledger_only` y `no_canonical_write`. No instaló paquetes, no importó configuraciones privadas, no inició procesos, no accedió a red ni produjo datos reales. G-MIG-LUKS-1.8b queda como el siguiente subgate de diseño para revisar Docker/OmniRoute exclusivamente por presencia.

### Diseño G-MIG-LUKS-1.8b — inspección pasiva de Docker y OmniRoute

El wrapper `inspect_omniroute_passive_after_luks.sh` no tiene modo de inicio ni instalación. Solo informa: existencia, propietario y modo del directorio `~/omniroute-pilot`; nombres de archivos esperados hasta dos niveles sin abrir su contenido; presencia/versiones de cliente Docker o Docker Compose; procesos con nombres de OmniRoute o Compose; y si el puerto local `127.0.0.1:20128` está en escucha. No llama a `docker info`, `docker compose up`, `docker start`, APIs, proveedores, servidores remotos ni archivos `.env`.

| Resultado pasivo | Criterio | Significado |
|---|---|---|
| PASS de estructura | Directorio privado presente y se identifican solo nombres de artefactos Docker/configuración. | El entorno restaurado puede revisarse sin revelar secretos. |
| Docker ausente | No se encuentra binario o plugin Docker. | Se documenta como dependencia pendiente; no se instala en este subgate. |
| Servicio detectado | Proceso OmniRoute/Compose o escucha en `127.0.0.1:20128`. | Se detiene el gate y se investiga; no se envían entradas ni se modifica el estado. |
| Sin servicio activo | No hay proceso ni puerto de OmniRoute en escucha. | Cumple el aislamiento requerido para el siguiente diseño. |

G-MIG-LUKS-1.8b no prueba solicitudes, rutas, proveedores, fallback, API keys ni borradores. Eso requerirá un gate independiente con una fixture no sensible, consentimiento específico y un control previo del arranque de Docker.

La primera ejecución pasiva devolvió un falso positivo porque el patrón `pgrep` coincidió con la propia línea de comando del wrapper. Este resultado no indica un servicio OmniRoute activo: el inventario sí confirmó el directorio privado con modo `0700` y ausencia de Docker/Compose. Una exclusión inicial por PID no cubrió la invocación `bash` que lanzó el archivo; la corrección final excluye por nombre exacto el wrapper de inspección y conserva cualquier proceso OmniRoute/Compose ajeno. La sintaxis fue validada sin ejecución, instalación, inicio, lectura de `.env`, apertura de puertos ni red. La repetición sigue usando la autorización ya otorgada para G-MIG-LUKS-1.8b.

G-MIG-LUKS-1.8b pasó tras aplicar la corrección: `~/omniroute-pilot` sigue presente con modo `0700`, Docker y Docker Compose no están instalados, no se detectaron procesos OmniRoute/Compose y `127.0.0.1:20128` no está en escucha. No se modificó configuración, no se abrió archivo `.env`, no se inició contenedor, no se llamó red y no se usaron entradas sintéticas o reales. El resultado es inventario técnico, no autorización para instalar Docker ni iniciar OmniRoute.

### Diseño G-MIG-LUKS-1.8c — revisión estática de collectors

La revisión estática usa `preflight_collectors_static_after_luks.sh` y `validate_collectors_static_contract.py`. El primero verifica la presencia de siete artefactos públicos requeridos por el gate y el segundo usa `ast.parse` y lectura de texto para revisar esos contratos y el autorizador TikTok público, sin importar módulos de collectors. Por diseño, no lee `~/.config/usm-metrics`, `~/.local/share/usm-metrics`, variables de entorno, token alguno, `.env` ni evidencia.

| Artefacto | Contrato revisado de manera estática | No se ejecuta |
|---|---|---|
| TikTok | Collector: marca USM, referencia a configuración TikTok, token y llamadas Display API. Autorizador/configuración pública: PKCE, callback loopback, variables locales y scopes `user.info.basic`/`video.list`. | PKCE, callback, refresh o `video.list`. |
| YouTube | Scopes exactos de lectura/rendimiento/monetización, referencia a directorio de evidencia configurado y preservación de `not_available`. | OAuth, refresh, canal o Analytics API. |
| Facebook e Instagram | Variable temporal Meta, `requests.get` y ausencia estática de POST/PUT/PATCH/DELETE. | Token, Graph API, feed, media o evidencia. |
| Meta probe | Contrato GET-only de validación de cuenta y ausencia de llamadas de escritura. | OAuth, conexión, página o cuenta Instagram. |
| Requisitos y ejemplo | Dependencias públicas y topología de marca/rutas sin valores secretos. | Instalación de paquetes o copia a configuración privada. |

El `--execute` del wrapper solo lanza el analizador AST con `PYTHONDONTWRITEBYTECODE=1` y `python3 -B`; no instala dependencias porque el análisis usa biblioteca estándar. G-MIG-LUKS-1.8c no habilita collectors, cron, evidencia real, Sheets, Drive, OmniRoute, shadow ledger persistente ni G-NORM-4R. Cualquier fallo estático bloquea el gate y se corrige primero en código público.

La primera ejecución autorizada completó el preflight, pero el analizador devolvió `static_contract_blocked`. La causa fue una expectativa de ubicación incorrecta: buscaba los nombres de variables de TikTok y rutas de evidencia directamente en collectors que consumen referencias de configuración, aunque los valores se declaran en el autorizador TikTok y en `official_metrics_config.example.json`. No se trató de un acceso a datos privados ni de una ejecución de integración.

La corrección pública publicada en el commit `757c6ab` alinea el análisis con el contrato real: el collector verifica sus referencias de configuración, el autorizador público verifica PKCE/callback/scopes y el ejemplo público verifica el directorio de evidencia, variables locales y scopes TikTok. La sintaxis y el análisis se validaron antes de publicar. Tras actualizar el clon LUKS, Fernando ejecutó de nuevo el preflight y el modo confirmado: obtuvo `STATUS=preflight_complete_static_only_no_private_read_no_network`, `status=static_contract_passed`, cero fallos y `STATUS=collectors_static_review_complete_no_private_read_no_network`.

G-MIG-LUKS-1.8c queda completado exclusivamente como revisión estática. La totalidad de los collectors, OAuth, APIs, tokens, configuraciones privadas, evidencia real, instalación de dependencias, cron, Docker, OmniRoute, shadow ledger persistente y G-NORM-4R permanece bloqueada. El diseño de esos controles posteriores ahora existe como G-SEC-2 en `2026-08-25_Consentimiento_Piloto_Real_Shadow_Ledger_USM.md` v3.4 y quedó en `Review` tras confirmación humana. Sus cuatro subgates técnicos G-SEC-2.1a, 2.2a, 2.3a y 2.4a ya pasaron exclusivamente con fixtures ficticios: no hubo red, salida, automatización, lectura privada, mutación de archivos ni consentimiento real. La tarjeta real vacía y su procedimiento de solicitud puntual están documentados en `2026-08-27_Plantilla_Tarjeta_Consentimiento_Puntual_USM.md` v1.6, también en `Review`, sin campos emitidos ni solicitud activa. La ficha de propuesta pública mínima `2026-08-27_Ficha_Propuesta_Minima_Comparacion_Alcance_USM.md` v1.2 está en `Draft`, no contiene propuesta y no activa una integración. G-SEC-2.5 pasó revisando estáticamente estas piezas públicas, sin red ni lectura privada; G-SEC-2.6 solo prepara su revisión final y consolidación documental.

## Diseño de desbloqueo G-MIG-LUKS-1.5

El método candidato es **instalación limpia guiada en el disco interno con `Erase disk and install Xubuntu` seguido de `Encrypt with a passphrase`**. Ubuntu documenta esta alternativa como el cifrado recomendado y especifica que configura LVM con cifrado de disco. [5] El método usa LUKS a nivel de bloque y desbloqueo con una frase ingresada localmente. [1]

La opción de cifrado respaldado por hardware queda excluida: la comprobación local indicó ausencia de Secure Boot, mientras Ubuntu requiere Secure Boot UEFI, TPM 2.0 e IOMMU para esa modalidad. [6] La ruta manual también queda excluida de este proyecto mientras no exista un diseño de particionado aprobado por separado; no es necesaria si la ruta guiada de frase está disponible.

### G-MIG-LUKS-1.4g — prueba visual de cifrado guiado

Este gate no escribe en disco. Con la USB Xubuntu conectada y `Fernando` desconectado, se inicia la sesión de prueba por rEFInd. En **Disk setup** se selecciona temporalmente `Erase disk and install Xubuntu` y se pulsa continuar únicamente para abrir la pantalla **Encryption and file system**. El criterio de PASS es observar `Encrypt with a passphrase` y, si se muestra, la indicación de LVM/cifrado. No se escribe ninguna frase, no se avanza a usuario, zona horaria ni resumen, y se cierra el instalador sin aplicar cambios.

### G-MIG-LUKS-1.5 — punto de no retorno y preflight obligatorio

Solo después de que G-MIG-LUKS-1.4g pase, este es el checklist que debe completarse el mismo día de la instalación. No se acepta una confirmación genérica: cada renglón se confirma explícitamente antes del botón final.

| Control | Evidencia requerida antes de avanzar | Resultado si falla |
|---|---|---|
| Respaldo | Confirmar que el ciphertext `age` y la restauración controlada aprobada siguen documentados; el disco `Fernando` se desconecta antes de arrancar el instalador. | No se reinicia para instalar. |
| Identidad del destino | Desde la sesión live, verificar por modelo, tamaño y montaje que existe un solo disco interno objetivo de aproximadamente 465.8 GB; nunca decidir por la letra `/dev/sdX`. | Detenerse y documentar la discrepancia. |
| Aislamiento físico | Mantener conectada solo la USB Xubuntu junto al disco interno; `Fernando` y `STORE N GO` desconectados. | No llegar a Disk setup. |
| Método de cifrado | Seleccionar exclusivamente `Erase disk and install Xubuntu` → `Encrypt with a passphrase`; no usar alongside, manual, LVM sin cifrar ni hardware-backed encryption. | Volver al escritorio live sin instalar. |
| Frase LUKS | Fernando crea e ingresa la frase solo localmente y la conserva fuera del equipo; no se dicta, muestra, pega ni registra en chat, GitHub, Drive o scripts. | No continuar. |
| Resumen final | Revisar que el resumen nombre solo el disco interno verificado y el cifrado por frase. | No pulsar instalar. |
| Última autorización | Fernando autoriza expresamente **en ese momento** borrar solo el disco interno identificado para instalar Xubuntu Desktop cifrado con frase. | No pulsar `Install`. |

El único punto destructivo es pulsar el botón final `Install` desde el resumen ya verificado. Todo lo anterior sirve para observar, comparar y cancelar. Tras ese clic no se intenta una cancelación ni se desconecta la alimentación; la siguiente acción es esperar el final, retirar la USB cuando el instalador lo pida y completar G-MIG-LUKS-1.6.

Antes de la instalación debe haber alimentación estable, tiempo suficiente para interrupciones y la confirmación de que no existe otro sistema operativo o dato no inventariado en `sda` que deba preservarse. El proyecto asume reinstalación limpia del único disco interno; si aparece una partición o requisito nuevo, el plan se detendrá y se revisará.

## Exclusiones y controles de separación

La migración no mezcla datos, código ni credenciales de Firma Bordados, Bam in a Can u otras marcas. No sube el ciphertext a Drive ni a GitHub, no usa Drive como ledger y no habilita automatización, Sheets, cron, OmniRoute con datos reales ni G-NORM-4R. La restauración posterior se realizará solo al sistema ya cifrado y nunca desde el medio externo en formato abierto.

## Referencias

[1] [Ubuntu Security Documentation — Full disk encryption](https://documentation.ubuntu.com/security/security-features/storage/encryption-full-disk/)

[2] [Xubuntu — Release 26.04](https://xubuntu.org/release/26.04/)

[3] [Ubuntu Desktop Documentation — Create a bootable USB stick](https://ubuntu.com/desktop/docs/en/latest/how-to/create-a-bootable-usb-stick/)

[4] [Ubuntu Desktop Documentation — Install Ubuntu Desktop, Disk setup](https://ubuntu.com/desktop/docs/en/latest/tutorial/install-ubuntu-desktop/)

[5] [Ubuntu Desktop Documentation — Advanced disk setup features](https://ubuntu.com/desktop/docs/en/latest/reference/advanced-disk-setup-features/)

[6] [Ubuntu Desktop Documentation — Encrypt your disk with TPM](https://ubuntu.com/desktop/docs/en/latest/how-to/encrypt-your-disk-with-tpm/)
