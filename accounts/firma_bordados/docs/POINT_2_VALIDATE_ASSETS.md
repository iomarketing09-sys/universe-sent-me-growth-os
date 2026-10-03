# Punto 2 – Validar los assets disponibles y asignarles los campos necesarios en el CSV de GrowthOS

## Objetivo
Pasar de los archivos sueltos (fotos, videos, catálogos, documentos) almacenados en Google Drive a un inventario estructurado dentro del CSV `pieces_firmabordados.csv` de GrowthOS, de modo que cada pieza cuente con los campos mínimos requeridos para ser utilizada en los flujos de publicación y métricas (puntos 1 y 3).

## 1. Inventario de assets disponibles (según la auditoría)

Desde la carpeta de Google Drive de Firma Bordados (ruta base en la auditoría: `/auditoria_firma_bordados/Firma_Bordados - Drive`) se identificaron los siguientes grupos:

| Ruta (relativa) | Tipo | Ejemplos de archivos |
|-----------------|------|----------------------|
| `Catalogos/` | PDF (catálogos) | `CATÁLOGO_BIGBANG_2019.pdf`, `Catalogo MyO 3.pdf`, `SOUL&BLUES 2025.pdf` |
| `Firma Bordados/` | Imágenes (PNG/JPG) y video | `01_lunes_detalle_uniforme.png`, `FB_IMG_*.jpg`, `VID-20260821-WA0002.mp4`, `Professional_photographic_restor…_2K_202608102219.jpeg` |
| `Logo_Firma_Bordados.jpeg` / `Logotipo - Firma Bordados.jpeg` | Logotipo de marca | – |
| Otros folders (`Archivo/`, `Manus/`, `Publicaciones Agosto/`) contienen documentación, planes, protocolos y material de campaña que no se trata como “piezas de contenido” para publicación directa, pero pueden ser referenciados si se requiere. |

> **Nota:** Los nombres de archivo suelen seguir una convención que incluye fecha, descripción y versión (p. ej. `01_lunes_detalle_uniforme.png`, `VID-20260821-WA0002.mp4`). Esta convención facilita la extracción de metadatos básicos.

## 2. Campos requeridos en el CSV de GrowthOS

Según el modelo `Piece` (`growthos/core/models.py`) y el CSV actual (`new-growth-os/data/pieces_firmabordados.csv`), los campos que deben poblarse para cada asset son:

| Campo (nombre en CSV) | Descripción | Formato / Ejemplo | Comentario |
|-----------------------|-------------|-------------------|------------|
| `ID_Pieza` | Identificador único de la pieza | `CNT-0001` (secuencial) o `FB-0001` si se mantiene legado | El validador actual espera `^CNT-\d{1,4}$`. Si se decide conservar el legado `FB-####`, sería necesario ajustar el validador o aceptar que esas filas se salten al importar. |
| `Titulo` | Título descriptivo legible | `"Catálogo Soul & Blues 2025"` | Puede derivarse del nombre de archivo o ser más legible. |
| `Tipo_Contenido` | Tipo de material (según enum `TipoContenido`) | `"Carrusel"`, `"Reel / Meme adaptado"`, `"PDF"` | Debe coincidir con un valor del enum; si no, el campo queda vacío y requerirá revisión humana (C_REAL). |
| `Plataforma` | Plataforma destino (enum `Plataforma`) | `"Instagram"`, `"Facebook"` | |
| `Objetivo` | Breve descripción del objetivo de la pieza | `"Promover catálogo Soul & Blues 2025"` | Texto libre. |
| `Hipotesis_ID` | ID de la hipótesis de marketing asociada (opcional) | `"HB-001"` | Útil para el ciclo de experimentación. |
| `Estado` | Estado actual del contenido (enum `EstadoPieza`) | `"Idea"`, `"Pendiente de Producción"`, `"Publicado"` | |
| `Prioridad` | Prioridad (enum `Prioridad`) | `"Alta"`, `"Media"`, `"Baja"` | |
| `Dificultad_Produccion` | Dificultad (enum `DificultadProduccion`) | `"Media"`, `"Baja"` | |
| `Es_Reutilizable` | ¿Se puede reutilizar? (enum `Reutilizable`) | `"Sí"` / `"No"` | |
| `Fecha_Ultima_Publicacion` | Fecha de última publicación (si aplica) | `2026-08-15` | Formato `YYYY-MM-DD` (vacío si aún no se ha publicado). |
| `Fuente` | Origen del asset (ej. Google Drive, cámara interna) | `"Google Drive - Folder: Firma Bordados/Catalogos"` | |
| `Formato` | Formato de archivo | `"PDF"`, `"PNG"`, `"JPG"`, `"MP4"` | |
| `Categoria` | Categoría de contenido (enum `Categoria`) | `"Marca / Narrativa / Resonancia"` | |
| `Bloqueado_Canon` | ¿Está bloqueado por canon? (enum `BloqueadoCanon`) | `"No"` | |
| `Asset_Ref_Confirmado` | Referencia canónica del asset (nombre de archivo en Drive) | `"CATALOGO_SOUL_BLUES_2025.pdf"` | Debe coincidir exactamente con el nombre del archivo en Drive (sin ruta). |
| `Asset_Ref_Candidato` | Referencia alternativa (si se está probando un nuevo nombre) | *vacío* | |
| `Drive_ID` | ID del archivo o carpeta en Google Drive (extraíble de la URL de compartir) | `"1abc123def456"` | Necesario para construir enlaces de descarga o vista previa. |
| `Drive_Reference_ID` | Texto descriptivo que ya aparece en el CSV (ej. “Drive file ID: 1abc123…”) | `"Drive file ID: 1abc123..."` | Puede mantenerse para trazabilidad; el campo `Drive_ID` es el que se usará programáticamente. |
| `Asset_Set`, `Asset_Ref`, `Asset_Filename` | Campos adicionales para versionado y referencia | `"catalogos_2019"`, `"BigBang_2019.pdf"` | Se pueden rellenar con información de versión o conjunto. |
| `Estado_Operacion_Normalizado`, `Estado_Canon_Normalizado`, `Estado_Produccion`, `Estado_Publicacion` | Estados normalizados (se llenan tras procesos de reconciliación) | `"Idea"`, `"Canon_Clear_or_Unverified"` | Se dejan vacíos inicialmente y se completan con los scripts de auditoría. |
| `Reconciliacion_Estado`, `Reconciliacion_Confianza`, `Reconciliacion_Fuente`, `Reconciliacion_Nota` | Resultados de la reconciliación (se llenan tras ejecutar `audit_inventory.py`) | Vacíos inicialmente | |
| `Ultima_Sincronizacion` | Timestamp de la última sincronización con Drive | `2026-08-29 10:00:00` | Se actualiza cada vez que se corre el script de exportación/importación. |
| `Motivo_Revision_Normalizado` | Motivo de revisión (si aplica) | Vacío | |
| Campos de taxonomía (`Personaje_Principal_Normalizado`, `Tipo_Humor_Normalizado`, etc.) | Se llenan tras procesos de etiquetado automático o manual | Vacíos inicialmente | |
| `Dias_Desde_Publicacion` | Campo calculado (no se escribe) | – | Se calcula automáticamente por el modelo. |

**Resumen de los campos críticos para el primer cargue**  
`ID_Pieza`, `Titulo`, `Tipo_Contenido`, `Plataforma`, `Objetivo`, `Estado`, `Prioridad`, `Dificultad_Produccion`, `Es_Reutilizable`, `Asset_Ref_Confirmado`, `Drive_ID`, `Fuente`, `Formato`, `Categoria`, `Fecha_Ultima_Publicacion` (opcional).

## 3. Plan de acción para asignar los campos

| Acción | Detalle | Herramienta / Script sugerido |
|--------|---------|------------------------------|
| **3.1. Exportar lista de archivos de Drive** | Obtener nombre, ID, tipo MIME y ruta relativa de cada archivo dentro de `Firma Bordados/` y sus subcarpetas. | Usar la API de Google Drive vía `composio` o un script Python simple (`drive.service.files().list`). Guardar el resultado en un CSV temporal (`drive_inventory_raw.csv`). |
| **3.2. Normalizar nombres y extraer metadatos** | - Quitar rutas y dejar solo el nombre de archivo → `Asset_Ref_Confirmado`.<br>- Detectar tipo de contenido a partir de extensión o nombre (PDF → `"PDF"`, PNG/JPG → `"Imagen"`, MP4 → `"Video"`).<br>- Si el nombre contiene palabras clave como `"reel"`, `"historia"`, `"catalog"`, `"guía"`, asignar `Tipo_Contenido` y `Categoria` según reglas predefinidas.<br>- Si el nombre incluye una fecha (`YYYYMMDD`) o descripción (`_lunes_`, `_detalle_`), usar eso para `Titulo` o `Objetivo`. | Script Python (`normalize_assets.py`) que lee `drive_inventory_raw.csv` y produce un CSV intermedio con los campos básicos llenos. |
| **3.3. Asignar IDs de pieza** | - Generar IDs siguiendo el patrón `CNT-####` (secuencial) **o** mantener el legado `FB-####` si se decide no cambiar el validador.<br>- Llevar un registro de los IDs ya usados (puedes leer el CSV actual para evitar colisiones). | Mismo script de normalización puede añadir una columna `ID_Pieza` usando un contador o leyendo el último ID del CSV existente. |
| **3.4. Poblar campos de estado y prioridad** | Por defecto, marcar todos los assets nuevos como `Estado = Idea`, `Prioridad = Media`, `Dificultad_Produccion = Media`, `Es_Reutilizable = Sí` (a menos que el nombre indique lo contrario, ej. “oferta flash” → `Prioridad = Alta`). | Reglas simples en el script de normalización. |
| **3.5. Vincular a hipótesis (opcional)** | Si el asset forma parte de una campaña ya planificada (ej. del calendario semanal que creaste), asignar la `Hipotesis_ID` correspondiente (HB‑001, HB‑002, …). Puedes usar una tabla de búsqueda basada en el rango de fechas o en el nombre del archivo. | Archivo de referencia `hypothesis_mapping.csv` (fecha → HB‑) que el script consulta. |
| **3.6. Generar CSV final para GrowthOS** | Unir los campos normalizados con las columnas que faltan (dejando vacío aquellos que se poblarán después de la publicación, como `Fecha_Ultima_Publicacion`, `Meta_Publication_ID`, etc.). | Salida: `pieces_firmabordados_ready.csv` listo para ser importado con `CSVAdapter.import_csv(Piece, path)`. |
| **3.7. Validar antes de importar** | Ejecutar el script de auditoría (`audit_inventory.py`) en modo `--print-stats` sobre el CSV generado para ver cuántas filas quedan en `C_REAL` (requieren revisión humana) y corregir esos casos antes de cargar. | `python growthos/scripts/audit_inventory.py --source piezas_firmabordados_ready.csv --print-stats`. |
| **3.8. Importar a GrowthOS** | Si el reporte muestra 0 `C_REAL` (o un número bajo que ya tienes planeado revisar), usar `CSVAdapter.import_csv` para añadir las nuevas piezas al inventario. | Script pequeño o llamada directa desde una consola de Python. |

### Flujo resumido (pseudocódigo)

```text
1. drive_inventory_raw.csv ← listar archivos de Drive (nombre, id, mimeType, ruta)
2. normalized.csv ←
 - Asset_Ref_Confirmado = nombre_archivo
      - Drive_ID = id
      - Fuente = "Google Drive - Folder: " + ruta_relativa
      - Formato = extensión.upper()
      - Tipo_Contenido = map_extensión_a_enum(extensión)  # PDF, Imagen, Video
      - Categoria = inferir_categoria_desde_nombre(nombre_archivo)
      - Titulo = limpiar_nombre_para_titulo(nombre_archivo)
      - Objetivo = generar_desde_palabras_clave(nombre_archivo)
      - ID_Pieza = generar_id_secuencial()
      - Estado = "Idea"
      - Prioridad = determinar_prioridad(nombre_archivo)
      - Dificultad_Produccion = "Media"
      - Es_Reutilizable = "Sí"
      - Hipotesis_ID = buscar_hipotesis_por_fecha_o_nombre(nombre_archivo)
3. pieces_firmabordados_ready.csv ← normalized.csv + columnas vacías (fecha publicación, métricas, etc.)
4. Ejecutar auditoría → revisar C_REAL → corregir manualmente si es necesario
5. Importar CSV final a GrowthOS
```

## 4. Próximos pasos (sin hacer cambios todavía)

1. **Recolectar la lista actual de archivos** desde la carpeta de Drive (puedes usar la interfaz web o un comando `rclone lsjson` si tienes rclone instalado).  
2. **Revisar el CSV actual** (`/home/universe-sent-me/new-growth-os/data/pieces_firmabordados.csv`) para ver qué IDs ya están en uso y evitar duplicados.  
3. **Diseñar las reglas de mapeo** (extensión→Tipo_Contenido, palabras clave→Categoria/Hipotesis_ID) basándote en el contenido de los archivos que viste (catalogos, imágenes de uniforme, videos de proceso, etc.).  
4. **Crear un script de prueba** (en un entorno seguro) que genere un CSV de muestra con unos pocos archivos y lo pase por la auditoría para asegurarte de que no haya errores de validación.  
5. **Una vez validado el flujo**, podrás programar la ejecución periódica (por ejemplo, cada viernes antes del push a `main`) para mantener el inventario sincronizado con los nuevos assets que se suban a Drive.  

Con este plan tendrás una base clara para pasar de los archivos sueltos en Drive a un inventario estructurado dentro de GrowthOS, listo para ser usado en la generación dinámica de contenido en el sitio web de Firma Bordados y para alimentar el ciclo de métricas y experimentación.  

---  
*Fin del punto 2.*  
