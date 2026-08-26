---
title: "Diseño de respaldo cifrado previo a LUKS — Universe Sent Me"
purpose: "Definir una estructura de carpetas y un wrapper de cifrado local previo a escribir cualquier respaldo autorizado en el disco externo vfat."
status: Draft
created: 2026-08-25
updated: 2026-08-25
version: "2.2"
author: "Manus AI"
related_documents:
  - "Operations/Automation/2026-08-25_Plan_Decision_Cifrado_Local_G-NORM-4R.md"
  - "Operations/Automation/2026-08-25_Inventario_Previa_Migracion_LUKS_Xubuntu_USM.md"
  - "Operations/Automation/2026-08-25_Consentimiento_Piloto_Real_Shadow_Ledger_USM.md"
  - "Operations/Automation/create_usm_backup_tree.sh"
  - "Operations/Automation/verify_local_age_tool.sh"
  - "Operations/Automation/validate_usm_restore_controlled.sh"
  - "Operations/Automation/validate_usm_restore_tree.py"
  - "GrowthOS/todo.md"
organization: "Operations/Automation"
---

# Diseño de respaldo cifrado previo a LUKS

## Propósito y estado

El disco externo Windows fue validado como destino físico condicionado: `sdc3`, formato `vfat`, 730.9 GiB libres. El formato permite guardar archivos, pero no cifra datos ni conserva permisos POSIX. Por ello, las categorías privadas solo pueden llegar al disco dentro de un archivo cifrado creado localmente.

Este documento cubre el respaldo inicial ya creado y el diseño de su restauración controlada. El wrapper de copia no permite una segunda versión sobre el árbol actual, y `validate_usm_restore_controlled.sh` inicia en modo `--plan`; este último no se ejecutará en modo `--execute` hasta una autorización separada de G-SEC-1A.3g.

## Herramienta seleccionada

El wrapper está diseñado alrededor de [age](https://github.com/FiloSottile/age), herramienta de cifrado de archivos moderna, composable y ampliamente mantenida. El README oficial documenta instalación en Ubuntu 22.04+ y la operación de cifrado/decrifrado mediante `age --passphrase` o claves de destinatario. [1]

Para este respaldo se diseña inicialmente el modo **passphrase interactivo**. La frase no se recibe por argumentos ni variables de entorno, no se escribe en el repositorio ni el disco externo, y se introduce solo en la terminal local de Fernando. Fernando aprobó que su recuperación se conserve en **dos copias físicas manuscritas y separadas**, bajo su control, fuera del disco, Drive, GitHub, chat, correo, OmniRoute y el archivo cifrado. El contenido de la frase no se solicita, registra ni transmite en este proyecto.

## Estructura propuesta en el disco externo

El árbol vacío fue creado y verificado mediante el wrapper independiente `create_usm_backup_tree.sh`, aprobado como G-SEC-1A.3a. La creación de ese árbol no ejecutó `prepare_usm_encrypted_backup.sh`, no generó archivos ni implica autorización de respaldo. La nomenclatura de archivos permanece como diseño para gates posteriores:

```text
/run/media/universe-sent-me/Fernando/
└── USM_PRE_LUKS_BACKUP/
    ├── 00_PROTOCOL/
    │   └── BACKUP_PROTOCOL_v1.txt
    ├── 10_CIPHERTEXT/
    │   └── usm_pre_luks_YYYYMMDDTHHMMSSZ.tar.gz.age
    ├── 20_MANIFEST/
    │   └── usm_pre_luks_YYYYMMDDTHHMMSSZ.manifest.txt
    ├── 30_INTEGRITY/
    │   └── usm_pre_luks_YYYYMMDDTHHMMSSZ.sha256
    └── 40_RESTORE_EVIDENCE/
        └── restore_check_YYYYMMDDTHHMMSSZ.txt
```

Los únicos datos privados del disco serán ciphertext `.age`. El manifest no enumera archivos internos, valores de métricas, IDs, tokens, rutas privadas, llaves ni contenido. El checksum se calcula sobre ciphertext y permite detectar cambios o daños del archivo cifrado sin exponer el contenido.

## Clasificación de fuentes

| Grupo | Rutas | Política |
|---|---|---|
| Código y reconstrucción | `~/universe-sent-me-growth-os`, `~/bin` | Se incluyen para recuperación de scripts y documentación. |
| Configuración y datos privados | `~/.config/usm-metrics`, `~/.local/share/usm-metrics`, `~/omniroute-pilot` | **Aprobados para un futuro ciphertext** bajo el perfil `code_scripts_and_approved_private`; siguen excluidos en `--plan` y `--dry-run`, y solo se leen con `--include-private` después de G-SEC-1A.3c, G-SEC-1A.3e y una autorización independiente de primera copia. |
| Excluido | Browser profiles, SSH/GPG keys, correo, chat, cuentas de otras marcas, medias personales no aprobadas, Docker engine data y cache general. | Nunca se agrega al wrapper sin una decisión separada. |

## Controles del wrapper

| Control | Diseño |
|---|---|
| Modo seguro | `--plan` es predeterminado y no escribe. `--dry-run` verifica herramientas, metadata y montaje sin crear archivos. |
| Ejecución explícita | `--execute` requiere `--include-private` y la cadena exacta de confirmación. |
| Destino | Debe ser el punto de montaje raíz existente, no una subcarpeta ni la raíz de Xubuntu; el wrapper exige específicamente `/dev/sdc3`, `vfat` y label `Fernando` antes de dry-run o ejecución. |
| Cifrado | `tar` transmite directamente a `age --passphrase`; no se conserva un `.tar.gz` abierto en el disco. |
| Llave | Interactiva, fuera de shell history, argumentos, variables, repo, Drive y disco externo. |
| Integridad | SHA-256 del ciphertext; `age-inspect` opcional sin descifrar. |
| Fallo | Archivo parcial se borra mediante `trap`; no se crea manifest de éxito si falla el cifrado. |
| Restauración | No se ejecuta aún. Requiere un test separado con un archivo no sensible y luego aprobación. |

## Gates antes de la primera copia

| Gate | Debe aprobarse explícitamente |
|---|---|
| G-SEC-1A.3a | **Completado el 2026-08-25.** Se aprobó y creó el árbol vacío en la raíz del volumen `vfat` confirmado. |
| G-SEC-1A.3b | **Completado el 2026-08-25.** Fernando aprobó incluir las tres raíces privadas exclusivamente dentro de un ciphertext futuro, junto con código y scripts. |
| G-SEC-1A.3c | **Completado el 2026-08-25.** Recuperación física aprobada en dos copias manuscritas y separadas; `age` verificado desde repositorios Ubuntu configurados, sin procesar datos USM. |
| G-SEC-1A.3d | Probar cifrado y restauración de un archivo ficticio no sensible en una carpeta temporal. |
| G-SEC-1A.3e | **Completado el 2026-08-25.** Dry-run contra el volumen validó montaje, herramienta, árbol y metadatos sin crear archivos. |
| G-SEC-1A.3f | **Completado el 2026-08-26.** Primera copia única creada tras validar `/dev/sdc3`, `vfat`, label `Fernando` y las cinco subcarpetas vacías. |
| G-SEC-1A.3g | Diseño v2.2 y dry-run completados. Falta aprobación independiente para descifrar temporalmente la copia real y ejecutar la validación. |

No se autoriza copia real, subida a Drive, sincronización, Drive como ledger, uso de OmniRoute, inserción de observaciones ni cambios de LUKS mediante este diseño.

## Prueba ficticia de cifrado y restauración

Fernando aprobó una prueba exclusivamente ficticia. Se usó el binario oficial temporal de age `v1.3.1` dentro de `/tmp`, sin instalación del sistema, sin acceso a rutas USM y sin disco externo. `validate_age_fictitious_roundtrip.sh` creó un fixture textual ficticio y un par de llaves efímeras de destinatario; este enfoque evita introducir una frase de recuperación humana durante el ensayo.

| Control | Resultado |
|---|---|
| Fixture | Texto artificial con marca explícita `synthetic`; sin datos USM. |
| Cifrado | Archivo ciphertext de 290 bytes creado en directorio temporal. |
| Restauración | El hash SHA-256 del fixture restaurado coincidió con el del origen. |
| Persistencia | El directorio del fixture y sus llaves efímeras fueron eliminados. |
| Entorno temporal externo | Dos directorios de descarga/prueba del sandbox se detectaron tras el primer intento de limpieza y se eliminaron manualmente; la verificación final confirmó ausencia de artefactos `usm-age-*` bajo `/tmp`. |
| Medios y datos USM | No se usó el disco externo, Drive, OmniRoute, `~/.config/usm-metrics`, `~/.local/share/usm-metrics` ni `~/omniroute-pilot`. |

La prueba confirma el mecanismo básico de cifrado/restauración e integridad de age, pero **no valida todavía** la operación real con frase interactiva, el volumen vfat o la restauración de un respaldo autorizado. Esos pasos siguen detrás de G-SEC-1A.3c, G-SEC-1A.3e y una autorización independiente de la primera copia.

## Registro de ejecución G-SEC-1A.3a

Fernando aprobó el gate y ejecutó localmente `create_usm_backup_tree.sh` el 2026-08-25. Antes de escribir, el wrapper confirmó que el destino era el punto de montaje `/run/media/universe-sent-me/Fernando`, con fuente `/dev/sdc3` y filesystem `vfat`. El modo `--plan` terminó con `STATUS=plan_only_no_directories_created`; el modo `--execute` terminó con `STATUS=empty_tree_created`.

El wrapper se negó de forma explícita a operar si `USM_PRE_LUKS_BACKUP` ya existía. Por tanto, la ejecución confirmada creó solamente la raíz y sus cinco subcarpetas vacías; no reemplazó contenido previo ni dejó archivos de respaldo. La enumeración final mostró exclusivamente directorios. No se ejecutaron los wrappers de cifrado, no se instaló `age`, no se leyeron rutas privadas y no se produjeron ciphertexts, manifests, checksums ni evidencia de restauración.

## Registro de alcance G-SEC-1A.3b

Fernando aprobó que `~/omniroute-pilot`, `~/.config/usm-metrics` y `~/.local/share/usm-metrics` formen parte del perfil futuro `code_scripts_and_approved_private`, junto con `~/universe-sent-me-growth-os` y `~/bin`. Esta aprobación define alcance, no transfiere datos: las tres raíces no fueron abiertas, enumeradas, copiadas ni hashadas durante este gate.

Al revisar el wrapper se detectó una diferencia heredada entre sus nombres internos de carpeta y el árbol físico aprobado. Se corrigió para exigir exactamente `00_PROTOCOL`, `10_CIPHERTEXT`, `20_MANIFEST`, `30_INTEGRITY` y `40_RESTORE_EVIDENCE`; no puede crear carpetas alternativas. La validación fue solo de sintaxis y `--plan`, que permaneció sin escrituras. El wrapper también exige que las cinco carpetas estén vacías para la primera copia y elimina protocolo, ciphertext, manifest y checksum si una futura ejecución falla antes de completarse.

## Registro de recuperación G-SEC-1A.3c

Fernando aprobó el mecanismo de recuperación: dos copias físicas manuscritas, separadas y bajo su control. Una futura frase se introducirá únicamente de forma interactiva en la terminal local cuando exista una autorización de primera copia; no debe copiarse al historial de shell ni compartirse con este proyecto.

La verificación local instaló `age` desde los repositorios Ubuntu configurados y confirmó `age_path=/usr/bin/age`, `age_version=1.2.1`, `package_version=1.2.1-1build1` y `STATUS=age_available_no_usm_data_processed`. No se leyeron fuentes USM, no se usó el disco externo, no se solicitó frase y no se creó ciphertext. Con ello G-SEC-1A.3c queda completado; el siguiente control sigue siendo el dry-run G-SEC-1A.3e.

## Registro de dry-run G-SEC-1A.3e

Fernando aprobó y ejecutó el dry-run contra `/run/media/universe-sent-me/Fernando`. La salida confirmó `target_mount=/run/media/universe-sent-me/Fernando`, `/dev/sdc3 vfat 930.8G 730.9G 21%`, `age_available=/usr/bin/age`, versión `1.2.1` y `STATUS=dry_run_complete_no_files_created`. El perfil de inclusión quedó en `private_roots_included=false`: el dry-run revisó solamente la presencia, tipo, modo y propietario de las dos rutas de código y las tres raíces privadas aprobadas, sin enumerar contenidos ni crear un archivo.

Una comprobación posterior de solo lectura devolvió `STATUS=backup_tree_contains_no_files`. Por tanto, `00_PROTOCOL`, `10_CIPHERTEXT`, `20_MANIFEST`, `30_INTEGRITY` y `40_RESTORE_EVIDENCE` siguen vacías; no existen protocolo, ciphertext, manifest, checksum ni evidencia de restauración. El dry-run no autoriza `--execute` ni reemplaza la aprobación separada G-SEC-1A.3f para una primera copia.

## Registro de primera copia G-SEC-1A.3f

Fernando confirmó físicamente las dos copias de recuperación y autorizó una única ejecución. El wrapper validó el volumen aprobado y creó `usm_pre_luks_20260826T042149Z.tar.gz.age` en `10_CIPHERTEXT`, junto con `BACKUP_PROTOCOL_v1.txt`, el manifest mínimo correspondiente y el checksum de ciphertext. El archivo cifrado mide 307,792,785 bytes. `sha256sum -c` devolvió `OK`; se verificó el ciphertext, pero **no se descifró ni inspeccionó su contenido**.

El manifest confirmó `encryption=age_passphrase_interactive`, `scope_profile=code_scripts_and_approved_private` y `restore_status=pending`. La estructura contiene exactamente cuatro archivos: protocolo, ciphertext, manifest y checksum. `40_RESTORE_EVIDENCE` continúa vacía. No hay archivos abiertos `.tar` o `.tar.gz`, no hubo subida a Drive, no se activó OmniRoute ni se modificó LUKS. La copia permite avanzar a un diseño de restauración controlada, pero no demuestra todavía la recuperabilidad de datos reales.

## Árbol exacto de `USM_PRE_LUKS_BACKUP`

El siguiente árbol es el único diseño aprobado. Sus seis directorios existen en la raíz del volumen montado, no dentro de carpetas de Windows existentes. La primera copia ya creó protocolo, ciphertext, manifest y checksum; la evidencia de restauración permanece como plantilla hasta G-SEC-1A.3g.

```text
USM_PRE_LUKS_BACKUP/
├── 00_PROTOCOL/
│   └── BACKUP_PROTOCOL_v1.txt
├── 10_CIPHERTEXT/
│   └── usm_pre_luks_YYYYMMDDTHHMMSSZ.tar.gz.age
├── 20_MANIFEST/
│   └── usm_pre_luks_YYYYMMDDTHHMMSSZ.manifest.txt
├── 30_INTEGRITY/
│   └── usm_pre_luks_YYYYMMDDTHHMMSSZ.sha256
└── 40_RESTORE_EVIDENCE/
    └── restore_check_YYYYMMDDTHHMMSSZ.txt
```

| Carpeta | Contenido permitido | Contenido prohibido |
|---|---|---|
| `00_PROTOCOL` | Instrucciones de recuperación y versión del diseño, sin información operativa sensible. | Frases, llaves, tokens, nombres de cuentas, rutas privadas o datos de métricas. |
| `10_CIPHERTEXT` | Un único archivo `.tar.gz.age` por ejecución aprobada. | Archivos abiertos `.tar`, `.tar.gz`, raw, evidencia, archivos parciales o copias sin cifrar. |
| `20_MANIFEST` | Fecha UTC, versión del protocolo, nombre del ciphertext, tipo de cifrado, scope profile y referencia al checksum. | Lista interna de archivos, rutas de origen, valores de métricas, IDs, hashes de evidencia, secretos o frase. |
| `30_INTEGRITY` | SHA-256 calculado exclusivamente sobre el archivo `.age`. | Checksums de archivos privados individuales o datos previos al cifrado. |
| `40_RESTORE_EVIDENCE` | Resultado agregado de una restauración aprobada: fecha, estado PASS/FAIL y checksum de ciphertext verificado. | Datos restaurados, rutas privadas, texto de archivos, llaves o detalles de cuentas. |

### Convención de nombres y retención

Todo nombre usa UTC sin espacios: `usm_pre_luks_YYYYMMDDTHHMMSSZ`. El primer respaldo se mantiene como `current` por convención documental, no mediante carpeta especial. No se crea una segunda versión ni se borra una anterior hasta que la restauración del primer ciphertext haya pasado y Fernando haya aprobado cualquier rotación.

Un archivo `.partial` puede existir solo durante la operación de streaming. Si queda después de un fallo, se elimina antes de un nuevo intento y no se registra como respaldo. Una carpeta o archivo fuera de este árbol se considera una desviación del gate y detiene la operación.

### Contenido del manifest

El manifest será texto simple y tendrá solo estas claves: `backup_type`, `protocol_version`, `created_utc`, `ciphertext_file`, `ciphertext_sha256_file`, `encryption`, `scope_profile`, `restore_status` y `operator_confirmation`. La clave `scope_profile` puede ser `code_and_scripts_only` o `code_scripts_and_approved_private`; no enumera rutas ni archivos.

### Secuencia después de crear el árbol

G-SEC-1A.3a creó el árbol vacío, G-SEC-1A.3b fijó el alcance autorizado, G-SEC-1A.3c verificó la herramienta y la recuperación, G-SEC-1A.3e validó el dry-run y G-SEC-1A.3f creó y verificó la primera copia cifrada. La siguiente barrera es G-SEC-1A.3g: diseñar y aprobar una restauración real controlada; no se descifrará ni restaurará nada sin esa autorización separada.

## Diseño de restauración controlada G-SEC-1A.3g

La finalidad de G-SEC-1A.3g es probar que el ciphertext real puede restaurarse y que los cinco grupos autorizados son lógicamente equivalentes a sus fuentes actuales, sin publicar archivos, rutas internas, valores de métricas, tokens ni contenido. La prueba **sí expone datos reales temporalmente** dentro de la ruta local no cifrada de Xubuntu; por eso requiere una aprobación distinta de la primera copia y un reconocimiento explícito de ese riesgo temporal.

| Elemento | Diseño aprobado para futura ejecución |
|---|---|
| Ciphertext de entrada | Únicamente `usm_pre_luks_20260826T042149Z.tar.gz.age`, después de validar su SHA-256. |
| Punto de montaje | Solo `/dev/sdc3`, `vfat`, label `Fernando`, raíz de montaje aprobada. |
| Ruta temporal | Directorio único creado con `mktemp` bajo `~/.config/.usm-restore-validation.<stamp>.XXXXXX`, con `umask 077` y modo `0700`. No se usa `/tmp`, el disco externo, Drive ni el repositorio. |
| Descifrado | `age --decrypt` solicita la frase exclusivamente en la terminal local; no recibe frases por argumentos, ambiente, archivos ni chat. |
| Restauración | El stream se extrae con `tar` al directorio temporal; no conserva un archivo `.tar` abierto. |
| Validación histórica | El validador confirma exclusivamente que el árbol restaurado contiene los cinco grupos requeridos y solo tipos permitidos —directorios, archivos regulares o symlinks—. No compara contra fuentes actuales, pues estas pueden haber cambiado desde el punto temporal del respaldo. |
| Integridad | SHA-256 del ciphertext se revisa antes y después de la restauración. |
| Limpieza | El directorio temporal se elimina tras PASS y mediante `trap` ante salida/fallo. Se confirma que la ruta ya no existe antes de escribir evidencia. |
| Límite de limpieza | La eliminación por ruta no equivale a borrado seguro de bloques en `ext4`; la ventana de plaintext temporal es el riesgo explícitamente reconocido por este gate. |
| Evidencia externa | Solo se escribe `40_RESTORE_EVIDENCE/restore_check_<stamp>.txt` tras PASS; contiene estados agregados, no contenido, rutas internas, hashes por archivo ni frase. |

### Requisitos de entrada y criterios de resultado

Antes de un futuro `--execute`, el wrapper exige el ciphertext, protocolo, manifest y checksum existentes; que el manifest conserve `scope_profile=code_scripts_and_approved_private` y `restore_status=pending`; que el destino siga siendo exactamente el volumen aprobado; que estén disponibles `age`, `tar`, `sha256sum` y Python local; y que aún no exista una evidencia de restauración para ese timestamp. Una ejecución requiere además `--acknowledge-temporary-plaintext` y la confirmación exacta `RUN_CONTROLLED_USM_RESTORE`.

La prueba pasa solo si ambos checksums del ciphertext son válidos, el descifrado autenticado y la extracción finalizan sin error, el árbol restaurado contiene los cinco grupos requeridos con tipos permitidos y la ruta temporal ya no existe tras la limpieza. No se compara el resultado contra fuentes actuales: la copia es evidencia de un momento anterior y esas fuentes pueden cambiar después. Si falla cualquier control, no se crea evidencia PASS; el `trap` intenta retirar la ruta temporal y el proceso termina en error. La limpieza no autoriza una migración por sí sola: el resultado deberá revisarse y documentarse antes de abrir un proyecto de migración LUKS.

### Límites y prohibiciones de G-SEC-1A.3g

G-SEC-1A.3g no publica, programa ni sube datos. No usa Drive, GitHub, Sheets, OmniRoute, APIs sociales, cron, shadow ledger ni otro producto de iO Marketing. No admite una segunda copia, no modifica el ciphertext, no actualiza el manifest original y no elimina los stashes locales de Git. La frase de recuperación no se muestra, registra ni comparte. La ejecución de este diseño sigue **no autorizada** hasta un consentimiento explícito posterior.

### Registro de dry-run G-SEC-1A.3g.1

Fernando aprobó y ejecutó el dry-run contra el ciphertext `usm_pre_luks_20260826T042149Z.tar.gz.age`. El wrapper validó el SHA-256, fuente `/dev/sdc3`, filesystem `vfat`, label `Fernando`, manifest y herramientas locales; devolvió `STATUS=restore_dry_run_complete_no_decrypt_no_temp_data_no_external_writes`. No se solicitó frase ni se invocó `age --decrypt`.

La verificación posterior devolvió `STATUS=restore_dry_run_left_no_temp_data_or_evidence`: no existe una ruta bajo `~/.config/.usm-restore-validation.20260826T042149Z.*` y `40_RESTORE_EVIDENCE` no contiene evidencia para este timestamp. G-SEC-1A.3g.2 sigue bloqueado hasta una autorización independiente de exposición temporal de datos reales.

## Referencias

[1] [FiloSottile/age — repositorio y README oficial](https://github.com/FiloSottile/age)

[2] [C2SP age v1 — especificación del formato](https://age-encryption.org/v1)
