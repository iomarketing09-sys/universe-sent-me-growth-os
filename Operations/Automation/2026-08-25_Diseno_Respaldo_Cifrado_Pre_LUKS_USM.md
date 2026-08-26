---
title: "Diseño de respaldo cifrado previo a LUKS — Universe Sent Me"
purpose: "Definir una estructura de carpetas y un wrapper de cifrado local previo a escribir cualquier respaldo autorizado en el disco externo vfat."
status: Draft
created: 2026-08-25
updated: 2026-08-25
version: "1.3"
author: "Manus AI"
related_documents:
  - "Operations/Automation/2026-08-25_Plan_Decision_Cifrado_Local_G-NORM-4R.md"
  - "Operations/Automation/2026-08-25_Inventario_Previa_Migracion_LUKS_Xubuntu_USM.md"
  - "Operations/Automation/2026-08-25_Consentimiento_Piloto_Real_Shadow_Ledger_USM.md"
  - "Operations/Automation/create_usm_backup_tree.sh"
  - "GrowthOS/todo.md"
organization: "Operations/Automation"
---

# Diseño de respaldo cifrado previo a LUKS

## Propósito y estado

El disco externo Windows fue validado como destino físico condicionado: `sdc3`, formato `vfat`, 730.9 GiB libres. El formato permite guardar archivos, pero no cifra datos ni conserva permisos POSIX. Por ello, las categorías privadas solo pueden llegar al disco dentro de un archivo cifrado creado localmente.

Este documento y `prepare_usm_encrypted_backup.sh` son **diseño**. El script arranca en modo `--plan`, no crea carpetas ni archivos por defecto, y no se ejecutará en modo `--execute` hasta que G-SEC-1A.3b, G-SEC-1A.3c, G-SEC-1A.3e y la autorización específica de la primera copia estén aprobados.

## Herramienta seleccionada

El wrapper está diseñado alrededor de [age](https://github.com/FiloSottile/age), herramienta de cifrado de archivos moderna, composable y ampliamente mantenida. El README oficial documenta instalación en Ubuntu 22.04+ y la operación de cifrado/decrifrado mediante `age --passphrase` o claves de destinatario. [1]

Para este respaldo se diseña inicialmente el modo **passphrase interactivo**. La frase no se recibe por argumentos ni variables de entorno, no se escribe en el repositorio ni el disco externo, y se introduce solo en la terminal local de Fernando. La recuperación debe almacenarse fuera del disco, Drive, GitHub, chat, correo, OmniRoute y el archivo cifrado.

## Estructura propuesta en el disco externo

El árbol vacío fue creado y verificado mediante el wrapper independiente `create_usm_backup_tree.sh`, aprobado como G-SEC-1A.3a. La creación de ese árbol no ejecutó `prepare_usm_encrypted_backup.sh`, no generó archivos ni implica autorización de respaldo. La nomenclatura de archivos permanece como diseño para gates posteriores:

```text
/run/media/universe-sent-me/Fernando/
└── USM_PRE_LUKS_BACKUP/
    ├── archives/
    │   └── usm_pre_luks_<UTC>.tar.gz.age
    ├── manifests/
    │   ├── usm_pre_luks_<UTC>.manifest.txt
    │   └── usm_pre_luks_<UTC>.age-inspect.txt   # opcional, sin descifrar
    └── checksums/
        └── usm_pre_luks_<UTC>.sha256            # checksum del ciphertext
```

Los únicos datos privados del disco serán ciphertext `.age`. El manifest no enumera archivos internos, valores de métricas, IDs, tokens, rutas privadas, llaves ni contenido. El checksum se calcula sobre ciphertext y permite detectar cambios o daños del archivo cifrado sin exponer el contenido.

## Clasificación de fuentes

| Grupo | Rutas | Política |
|---|---|---|
| Código y reconstrucción | `~/universe-sent-me-growth-os`, `~/bin` | Se incluyen para recuperación de scripts y documentación. |
| Configuración y datos privados | `~/.config/usm-metrics`, `~/.local/share/usm-metrics`, `~/omniroute-pilot` | Excluidos por defecto; solo se incluyen con `--include-private` tras aprobación explícita. |
| Excluido | Browser profiles, SSH/GPG keys, correo, chat, cuentas de otras marcas, medias personales no aprobadas, Docker engine data y cache general. | Nunca se agrega al wrapper sin una decisión separada. |

## Controles del wrapper

| Control | Diseño |
|---|---|
| Modo seguro | `--plan` es predeterminado y no escribe. `--dry-run` verifica herramientas, metadata y montaje sin crear archivos. |
| Ejecución explícita | `--execute` requiere `--include-private` y la cadena exacta de confirmación. |
| Destino | Debe ser un punto de montaje existente, no una subcarpeta ni la raíz de Xubuntu. |
| Cifrado | `tar` transmite directamente a `age --passphrase`; no se conserva un `.tar.gz` abierto en el disco. |
| Llave | Interactiva, fuera de shell history, argumentos, variables, repo, Drive y disco externo. |
| Integridad | SHA-256 del ciphertext; `age-inspect` opcional sin descifrar. |
| Fallo | Archivo parcial se borra mediante `trap`; no se crea manifest de éxito si falla el cifrado. |
| Restauración | No se ejecuta aún. Requiere un test separado con un archivo no sensible y luego aprobación. |

## Gates antes de la primera copia

| Gate | Debe aprobarse explícitamente |
|---|---|
| G-SEC-1A.3a | **Completado el 2026-08-25.** Se aprobó y creó el árbol vacío en la raíz del volumen `vfat` confirmado. |
| G-SEC-1A.3b | Alcance: decidir si se incluyen las tres raíces privadas, además de código y scripts. |
| G-SEC-1A.3c | Instalar/verificar `age` desde fuente oficial y definir dónde Fernando conservará la recuperación de la frase. |
| G-SEC-1A.3d | Probar cifrado y restauración de un archivo ficticio no sensible en una carpeta temporal. |
| G-SEC-1A.3e | Revisar dry-run y aprobar ejecución manual única. |

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

La prueba confirma el mecanismo básico de cifrado/restauración e integridad de age, pero **no valida todavía** la operación real con frase interactiva, las fuentes privadas, el volumen vfat o la restauración de un respaldo autorizado. Esos pasos siguen detrás de G-SEC-1A.3b, G-SEC-1A.3c, G-SEC-1A.3e y una autorización independiente de la primera copia.

## Registro de ejecución G-SEC-1A.3a

Fernando aprobó el gate y ejecutó localmente `create_usm_backup_tree.sh` el 2026-08-25. Antes de escribir, el wrapper confirmó que el destino era el punto de montaje `/run/media/universe-sent-me/Fernando`, con fuente `/dev/sdc3` y filesystem `vfat`. El modo `--plan` terminó con `STATUS=plan_only_no_directories_created`; el modo `--execute` terminó con `STATUS=empty_tree_created`.

El wrapper se negó de forma explícita a operar si `USM_PRE_LUKS_BACKUP` ya existía. Por tanto, la ejecución confirmada creó solamente la raíz y sus cinco subcarpetas vacías; no reemplazó contenido previo ni dejó archivos de respaldo. La enumeración final mostró exclusivamente directorios. No se ejecutaron los wrappers de cifrado, no se instaló `age`, no se leyeron rutas privadas y no se produjeron ciphertexts, manifests, checksums ni evidencia de restauración.

## Árbol exacto de `USM_PRE_LUKS_BACKUP`

El siguiente árbol es el único diseño aprobado para la primera copia. Sus seis directorios vacíos ya existen en la raíz del volumen montado, no dentro de carpetas de Windows existentes. Los cinco nombres de archivo que aparecen son plantillas futuras: **ninguno existe todavía**.

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

G-SEC-1A.3a ya creó el árbol vacío. La siguiente autorización debe decidir el alcance privado (G-SEC-1A.3b), verificar o instalar `age` y definir la recuperación fuera de este volumen y de servicios cloud (G-SEC-1A.3c), y después ejecutar `--dry-run` contra el punto de montaje (G-SEC-1A.3e). Ninguna de esas acciones aprueba datos privados por sí sola. La primera copia seguirá requiriendo confirmación separada de fuentes y una frase de recuperación gestionada fuera de este volumen.

## Referencias

[1] [FiloSottile/age — repositorio y README oficial](https://github.com/FiloSottile/age)

[2] [C2SP age v1 — especificación del formato](https://age-encryption.org/v1)
