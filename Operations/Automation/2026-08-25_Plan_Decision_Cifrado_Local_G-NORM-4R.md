---
title: "Plan comparativo de cifrado local para G-NORM-4R — LUKS integral vs. volumen dedicado"
purpose: "Preparar una decisión reversible y respaldada sobre el almacenamiento cifrado necesario antes de considerar el piloto real G-NORM-4R."
status: Draft
created: 2026-08-25
updated: 2026-08-25
version: "1.15"
author: "Manus AI"
related_documents:
  - "Operations/Automation/2026-08-25_Consentimiento_Piloto_Real_Shadow_Ledger_USM.md"
  - "Operations/Automation/2026-08-25_Shadow_Ledger_Privado_Append_Only_USM.md"
  - "Operations/Automation/2026-08-25_Guia_Piloto_Local_API_Oficial_Metricas_USM.md"
  - "Operations/Automation/2026-08-25_Diseno_Respaldo_Cifrado_Pre_LUKS_USM.md"
  - "GrowthOS/todo.md"
organization: "Operations/Automation"
---

# Plan comparativo de cifrado local para G-NORM-4R

## Propósito y decisión pendiente

El diagnóstico del 25 de agosto de 2026 encontró que la raíz de Xubuntu está montada desde `sda2` como `ext4`, sin una capa `crypto_LUKS` ni dispositivo `crypt`. Por ello, G-NORM-4R permanece bloqueado: no hay shadow ledger persistente, inserciones reales ni materialización canónica.

Este documento no autoriza comandos, formateos, particiones, cifrado, migraciones ni cambios de arranque. Su función es comparar dos caminos antes de iniciar un **proyecto separado** con respaldo verificado y aprobación explícita.

## Decisión arquitectónica registrada

Fernando eligió la **Alternativa A: migración planificada de Xubuntu a cifrado LUKS integral** como la dirección preferida para el crecimiento de Universe Sent Me. La decisión se basa en que el proyecto probablemente conservará más evidencia, configuraciones y automatizaciones locales que un piloto mínimo de ledger.

Esta preferencia solo abre el gate de preparación G-SEC-1A: inventario, respaldo externo separado, prueba de restauración y ventana de mantenimiento. No autoriza todavía una migración, reinstalación, operación de disco, captura de datos reales ni activación de G-NORM-4R.

> La protección requerida es cifrado de datos en reposo. No elimina por sí sola otros riesgos: un volumen montado queda disponible para la sesión activa, y el cifrado no reemplaza respaldo, permisos ni control de acceso.

## Criterios de decisión

| Criterio | Pregunta de control |
|---|---|
| Alcance de protección | ¿Debe protegerse solo el ledger futuro o también evidencia, tokens, configuraciones y otros datos locales de USM? |
| Disrupción aceptable | ¿Se acepta una migración/reinstalación de Xubuntu con recuperación validada? |
| Medio físico | ¿Existe un disco interno libre o un dispositivo externo dedicado que se pueda borrar y reservar exclusivamente para el ledger? |
| Recuperación | ¿Existe un respaldo separado, probado y accesible sin depender del disco que se cifrará? |
| Operación diaria | ¿Se puede montar y desbloquear el volumen únicamente durante las tareas autorizadas y cerrarlo al terminar? |
| Escalabilidad | ¿El objetivo se limita al piloto de cuatro observaciones o se prevé ampliar el sistema local de métricas? |

## Comparación ejecutiva

| Dimensión | Alternativa A: migrar Xubuntu a LUKS integral | Alternativa B: volumen LUKS dedicado para el ledger |
|---|---|---|
| Qué queda cifrado en reposo | El disco o las particiones seleccionadas de Xubuntu, según el diseño de instalación. | Solo el volumen dedicado y los archivos guardados dentro de él. |
| Cobertura para USM | Alta: puede abarcar ledger, evidencia, configuraciones y artefactos locales bajo el sistema cifrado. | Limitada: protege el ledger futuro, no los datos existentes fuera del volumen. |
| Disrupción | Alta: normalmente requiere plan de respaldo, reinstalación o migración controlada y validación de arranque. | Menor: requiere un dispositivo/espacio dedicado que se pueda borrar y configurar de forma aislada. |
| Riesgo operativo principal | Recuperación incompleta, configuración de arranque o falta de respaldo válido. | Elegir el dispositivo equivocado, no desmontarlo o dejar trazas fuera del volumen. |
| Adecuación al piloto de cuatro observaciones | Funciona, pero puede ser más amplio que el piloto. | Adecuado si se busca un piloto estrictamente acotado y hay medio físico dedicado. |
| Adecuación a operación futura de USM | Preferible si se conservarán evidencia, automatizaciones o herramientas locales sensibles. | Requiere rediseñar/migrar de nuevo si el alcance crece más allá del ledger. |
| Recomendación condicional | Elegir si USM seguirá operando datos locales sensibles de forma regular. | Elegir solo si el objetivo sigue limitado al ledger del piloto y se acepta su cobertura parcial. |

Ubuntu indica que LUKS proporciona cifrado a nivel de bloque para una partición o disco, y que el mapeo cifrado aparece normalmente mediante `device-mapper` bajo `/dev/mapper/`. [1] `cryptsetup` recomienda LUKS frente a modo plain para evitar errores de configuración comunes y destaca que el respaldo sigue siendo obligatorio. [2]

## Alternativa A — Migración de Xubuntu a cifrado LUKS integral

### Resultado deseado

Contar con una instalación recuperable de Xubuntu donde los datos locales de USM autorizados residan en almacenamiento cifrado en reposo. Esta alternativa es la más coherente si se espera conservar, procesar o automatizar evidencia privada y configuraciones locales a largo plazo.

### Plan de preparación, sin ejecución

| Fase | Acción de planificación | Gate de salida |
|---|---|---|
| A0. Inventario | Identificar sistema, aplicaciones necesarias, archivos de proyecto, rutas privadas y dependencias que deben reconstruirse; no copiar secretos al repositorio. | Lista de restauración aprobada. |
| A1. Respaldo separado | Definir una copia de seguridad fuera del disco de destino, con inventario, comprobación de lectura y criterio de éxito de restauración. | Respaldo validado mediante prueba de lectura/restauración de archivos no sensibles. |
| A2. Diseño de instalación | Definir soporte de arranque, particiones, cifrado LUKS y método de desbloqueo; la frase de paso se introduce localmente por el usuario, nunca por chat o repositorio. | Diseño técnico revisado y ventana de mantenimiento aprobada. |
| A3. Ejecución humana separada | Realizar reinstalación o migración solo bajo una autorización nueva, con recuperación preparada. | Xubuntu inicia, desbloquea y opera correctamente. |
| A4. Verificación posmigración | Confirmar capa LUKS/dispositivo `crypt`, montaje desde el mapper, acceso local, permisos y recuperación. | Evidencia de verificación no sensible archivada. |
| A5. Gate de USM | Revalidar retención, paths, permisos, backups y prohibiciones antes de cualquier observación real. | G-SEC-2 aprobado; recién entonces puede evaluarse G-NORM-4R. |

### Ventajas y límites

Esta alternativa ofrece la mayor cobertura para datos en reposo y reduce el riesgo de que evidencia, configuraciones o archivos temporales de USM queden fuera del perímetro cifrado. Sin embargo, exige mayor preparación: una migración mal planificada puede interrumpir el sistema o dificultar la recuperación. Nunca debe emprenderse sin un respaldo separado y probado.

## Alternativa B — Volumen LUKS dedicado exclusivamente para el ledger

### Resultado deseado

Contar con un dispositivo o espacio local identificado y reservado para un único propósito: alojar el shadow ledger autorizado, bajo LUKS, con montaje solo cuando exista una tarea aprobada. La opción debe usar un medio que pueda borrarse sin afectar Xubuntu ni otras marcas.

### Plan de preparación, sin ejecución

| Fase | Acción de planificación | Gate de salida |
|---|---|---|
| B0. Elegibilidad física | Identificar un dispositivo interno libre o medio externo dedicado; confirmar propiedad, capacidad, estado y que puede borrarse. No usar una ruta ambigua ni un archivo dentro del root sin cifrar como sustituto. | Dispositivo dedicado identificado por el usuario. |
| B1. Respaldo y confirmación | Confirmar que no contiene datos necesarios y que no existe dependencia de otras marcas. | Autorización específica para el dispositivo, no genérica. |
| B2. Diseño de volumen | Planear LUKS2, filesystem dentro del mapper, punto de montaje exclusivo, permisos restrictivos y política de montaje/desmontaje. | Diseño de paths y permisos aprobado. |
| B3. Ejecución humana separada | Formatear/cifrar únicamente el dispositivo confirmado y crear el volumen. | El dispositivo correcto se abre y monta; Xubuntu permanece intacto. |
| B4. Verificación | Confirmar `crypto_LUKS`, mapper, filesystem, permisos, montaje manual y desmontaje/cierre; documentar solo resultados no sensibles. | Volumen verificado sin datos reales. |
| B5. Gate de USM | Crear rutas del ledger dentro del volumen y aplicar la retención de 30 días, sin backups automáticos. | G-SEC-2 aprobado; recién entonces puede evaluarse G-NORM-4R. |

### Ventajas y límites

Esta alternativa limita la superficie de cambio y puede ser adecuada para el piloto de cuatro observaciones. Su límite es importante: no cifra las rutas existentes de evidencia, configuraciones, tokens ni archivos temporales que permanezcan en el root actual. No debe confundirse con cifrado completo del entorno. Si el alcance de USM crece, probablemente exigirá una solución integral posterior.

## Requisitos comunes y no negociables

| Control | Requisito antes de G-NORM-4R |
|---|---|
| Respaldo | Copia separada y prueba de restauración antes de cualquier operación destructiva. `cryptsetup` advierte que el daño de header LUKS puede hacer inaccesibles los datos sin un respaldo de header. [2] |
| Frase de paso | El usuario la gestiona e introduce localmente; nunca se comparte por chat, GitHub, Drive, Sheets, OmniRoute o un modelo. |
| Verificación de cifrado | Debe observarse una capa `crypto_LUKS` y un mapper `crypt`/`/dev/mapper`, no únicamente `ext4`. |
| Permisos | Directorio del ledger con acceso restringido; no usar ubicaciones compartidas, repositorios ni rutas de otras marcas. |
| Alcance de datos | Máximo cuatro observaciones no financieras, una por plataforma, solo tras G-NORM-4R. |
| Retención | Máximo 30 días; no backups automáticos, cloud ni sincronización. |
| Recuperación | No reparar, editar ni borrar eventos append-only. La recuperación crea una nueva cadena bajo aprobación humana. |
| Destinos prohibidos | GitHub y Drive no son ledger activo; Sheets y OmniRoute continúan fuera del gate de almacenamiento. |

## Gates propuestos

| Gate | Decisión requerida | Resultado si no pasa |
|---|---|---|
| G-SEC-0: alcance | Elegir alternativa A o B y confirmar que no se ejecutará con ambigüedad. | Continuar solo sintético. |
| G-SEC-1: respaldo | Validar respaldo, restauración y medio de recuperación. | No tocar discos ni volúmenes. |
| G-SEC-2: cifrado | Comprobar LUKS y mapper correctos, permisos y paths dentro del destino cifrado. | No crear ledger real. |
| G-SEC-3: operación | Probar bloqueo/desbloqueo, montaje/desmontaje y recuperación sin datos reales. | Corregir el diseño o volver a modo sintético. |
| G-NORM-4R | Renovar consentimiento granular de cuatro observaciones, retención y no sincronización. | No insertar observaciones reales. |

## Decisión sugerida por escenario

| Si tu situación es… | Alternativa más coherente |
|---|---|
| El piloto será breve, el ledger será el único dato nuevo y existe un dispositivo dedicado que puede borrarse. | Volumen LUKS dedicado. |
| Se espera ampliar la automatización local de USM o proteger evidencia y configuración local de forma sostenida. | Migración de Xubuntu a LUKS integral. |
| No hay respaldo validado, no hay dispositivo dedicado o no se puede tolerar una migración. | Permanecer sintético; no abrir G-NORM-4R. |

## Prohibiciones hasta autorización nueva

No se ejecutan operaciones de particionado, formateo, `cryptsetup`, migración, instalación, montaje persistente, copia de evidencia, cambios de arranque ni creación de ledger real. Firma Bordados y Bam in a Can siguen completamente fuera de este plan. OmniRoute continúa local, draft-only y sin recibir datos del ledger.

## Capacidad del medio externo de respaldo

El inventario de Xubuntu reportó aproximadamente 24 GiB usados en la raíz actual. Se calcularon tres referencias: 30 GiB con margen de 25%, 36 GiB con margen de 50% y 48 GiB al duplicar el uso actual. Estas cifras son para un respaldo **lógico por archivos** previo a una reinstalación/migración LUKS, no para una imagen sector a sector del disco completo.

| Escenario | Capacidad estimada | Medio recomendado |
|---|---:|---|
| Copia lógica mínima con margen | 36 GiB | 64 GB como mínimo técnico, si solo se conservará una copia y no habrá crecimiento relevante. |
| Copia lógica con espacio para revisión, restauración y crecimiento | 48 GiB o más | 128 GB recomendado para G-SEC-1A. |
| Imagen completa del disco actual | Aproximadamente 465.8 GiB antes de margen | 1 TB recomendado; no es la vía elegida para la migración planificada, salvo que se apruebe una estrategia de imagen separada. |

La recomendación actual es un medio externo de **128 GB o mayor** para el respaldo lógico. Debe ser un dispositivo separado, fiable y dedicado al proceso de migración, con capacidad para crear y verificar una copia antes de modificar Xubuntu. La decisión de compra, proveedor y formato del medio sigue correspondiendo a Fernando; este documento no solicita ni autoriza ninguna compra ni formateo.

El disco Windows informado ya fue detectado sin escritura como `/dev/sdc3`, volumen `vfat` con label `Fernando`, montado en `/run/media/universe-sent-me/Fernando`, con 730.9 GiB disponibles. Es un destino físico condicional para ciphertext futuro, no un volumen LUKS ni un ledger. Como contiene datos existentes de Windows y `vfat` no cifra ni conserva permisos POSIX, permanece prohibido escribir datos USM abiertos, formatear, reparar, reorganizar o montar de forma persistente.

## Drive como contingencia cifrada futura

La cuenta de iO Marketing tiene capacidad suficiente en Google Drive, pero su capacidad no cambia la decisión de seguridad: Drive no sustituye un medio local verificable para G-SEC-1A, no puede ser el shadow ledger activo y no recibe datos USM ahora.

Solo podría evaluarse como una **segunda copia de contingencia**, después de completar una preparación separada:

| Gate propuesto | Requisito | Resultado si no pasa |
|---|---|---|
| G-BACKUP-DRIVE-0 | Definir exactamente qué categorías no sensibles o privadas autorizadas se respaldan; excluir ledger real, raw, tokens, credenciales y browser profiles. | No se crea archivo de backup. |
| G-BACKUP-DRIVE-1 | Crear un archivo cifrado localmente antes de cualquier subida; Drive solo recibe el cifrado final, nunca archivos abiertos. | No se usa Drive. |
| G-BACKUP-DRIVE-2 | Guardar la llave o frase de recuperación fuera de Drive, GitHub, chat, email, OmniRoute y el propio archivo. | No se sube el archivo. |
| G-BACKUP-DRIVE-3 | Verificar la restauración desde una copia descargada con un conjunto de archivos no sensibles. | El respaldo no se considera válido. |
| G-BACKUP-DRIVE-4 | Aprobación explícita para la subida manual; sin sincronización automática. | Drive continúa fuera del flujo. |

Incluso si estos gates se aprobaran, la copia cifrada de Drive sería contingencia de recuperación y no sustituiría el respaldo local ni los controles de LUKS. No se crea, cifra, sube ni prueba ningún archivo como parte de este documento.

## Medio físico de respaldo identificado

El disco externo Windows se detectó como `sdc3`, un volumen `vfat` de 930.8 GiB con 730.9 GiB disponibles. Puede servir como destino físico para el respaldo lógico previo a la migración, pero con dos límites: contiene información existente y `vfat` no aporta permisos POSIX ni cifrado en reposo.

Por ello, cualquier respaldo deberá usar una carpeta exclusiva aprobada y preservar los datos privados de USM en un formato cifrado antes de escribirlos al disco. El gate G-SEC-1A.3a creó exclusivamente el árbol vacío `USM_PRE_LUKS_BACKUP` en la raíz del volumen; G-SEC-1A.3b aprobó el alcance cifrado de `~/omniroute-pilot`, `~/.config/usm-metrics` y `~/.local/share/usm-metrics`, sin abrirlas ni transferirlas; G-SEC-1A.3c confirmó la recuperación física en dos copias separadas y `age` desde repositorios Ubuntu configurados (`/usr/bin/age`, `1.2.1`); y G-SEC-1A.3e completó el dry-run sobre `/dev/sdc3` `vfat`. Con autorización única G-SEC-1A.3f, se creó la primera copia ciphertext de 307,792,785 bytes y su checksum validó `OK`, sin descifrar contenido. El diseño G-SEC-1A.3g ya define el futuro restablecimiento temporal, comparación lógica y limpieza fail-closed, pero no se ha descifrado ningún dato. La migración LUKS y G-NORM-4R siguen bloqueados.

El diseño de estructura y wrapper previo se documenta en `2026-08-25_Diseno_Respaldo_Cifrado_Pre_LUKS_USM.md`. Usa `age` local por streaming; G-SEC-1A.3f creó una única primera copia y bloquea cualquier segunda copia porque las cinco subcarpetas ya no están vacías. `validate_usm_restore_controlled.sh` parte en `--plan` y requiere un dry-run, seguido de otra aprobación humana, antes de descifrar la primera copia. La restauración valida la autenticidad de age, los checksums y la presencia estructural de los cinco grupos del backup histórico; no compara contra fuentes actuales que pueden haber cambiado. No se habilita la migración hasta que G-SEC-1A.3g valide una restauración real controlada.

G-SEC-1A.3d ya tiene una prueba ficticia aprobada y pasada con age temporal: fixture artificial, cifrado, restauración, hashes iguales y limpieza verificada. La prueba no incluyó datos de USM ni el disco externo, por lo que no reduce los demás gates de alcance, recuperación de frase y dry-run sobre el volumen real.

El árbol exacto del destino físico se fija en el diseño de respaldo v2.0: `USM_PRE_LUKS_BACKUP` contiene protocolo no sensible, un ciphertext, manifest mínimo, checksum de ciphertext y evidencia agregada de restauración. G-SEC-1A.3f creó los cuatro primeros elementos y confirmó la integridad de ciphertext; no existe aún evidencia de restauración. No se autoriza una segunda copia, alteración del ciphertext ni migración LUKS sin el proyecto de restauración G-SEC-1A.3g.

## Referencias

[1] [Ubuntu Security Documentation — Full disk encryption](https://documentation.ubuntu.com/security/security-features/storage/encryption-full-disk/)

[2] [cryptsetup(8) — Linux manual page](https://man7.org/linux/man-pages/man8/cryptsetup.8.html)

[3] [Consentimiento de piloto real shadow ledger](2026-08-25_Consentimiento_Piloto_Real_Shadow_Ledger_USM.md)
