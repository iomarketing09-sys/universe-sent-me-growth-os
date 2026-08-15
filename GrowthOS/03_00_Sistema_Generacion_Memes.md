# Sistema de Generación y Gestión de Memes

**Propósito:** Documentar el flujo de trabajo para la ingesta, aprobación y adaptación de memes en el universo de Universe Sent Me.
**Estado:** Active
**Fecha de creación:** 2026-08-01
**Última actualización:** 2026-08-15
**Versión:** 2.3
**Autor:** Manus AI
**Documentos relacionados:** `01_00_Arquitectura_Calendario_Escalable.md`, `01_03_Reuse_Queue.md`, `13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md`, `Integracion_Growth_OS.md`

---

## 1. Arquitectura de Ingesta y Almacenamiento

El sistema de memes se centra exclusivamente en Google Drive como punto único de ingesta y almacenamiento, eliminando la complejidad de repositorios de GitHub.

### 1.1 Fase de Propuestas (Google Drive)

Toda la gestión de memes ocurre en Drive. Esta carpeta sirve como bandeja de entrada y archivo visual.

-   **Ubicación:** `Universe Sent Me > USM > Meme_Proposals`
-   **Estructura:**
    -   `Proposed/`: Memes de referencia subidos por Fernando para su revisión.
    -   `Generated_By_Gemini/`: Contiene las imágenes procesadas y adaptadas al canon por Manus tras ser aprobadas.
    -   `Processed_Log/`: Contiene los metadatos JSON de cada meme procesado.

---

## 2. Flujo de Trabajo (Pipeline)

El ciclo de vida de un meme sigue estos pasos:

1.  **Propuesta:** Fernando sube una imagen de referencia a la carpeta `Proposed` en Drive.
2.  **Revisión y Aprobación:** Fernando revisa los memes propuestos en Drive.
3. **Procesamiento y Clasificación (Manus):**
    -   Manus detecta la imagen en la carpeta `Proposed` de Drive.
    -   Se utiliza Vision (Gemini) para clasificar el meme (personaje, tema, texto, emoción).
    -   Manus registra los metadatos en `Processed_Log` (JSON) y en el inventario local.
4. **Generación Final (Flow / Nano Banana):**
    -   Para garantizar la máxima consistencia visual de los personajes (Canon Guarding), el usuario realiza la generación final en **Flow** utilizando los modelos **Nano Banana 2** o **Nano Banana Pro**.
    -   Manus actúa como el gestor de metadatos y estratega de programación, sugiriendo los mejores slots en el calendario.
5.  **Ingreso al Growth OS:** La pieza se registra en la base de datos central (Google Sheets) con estado `Idea` o `Pendiente de Producción`.

---

## 3. Automatización Programada

El sistema cuenta con una tarea programada en Manus que se ejecuta **diariamente a las 9:00 AM (America/Matamoros)**:

> **Revisión diaria de memes en Drive**
> 1. Revisa la carpeta `Proposed` en Google Drive
> 2. Lista las imágenes que esperan revisión.
> 3. Ejecuta `usm_meme_generator.py` para adaptar las imágenes aprobadas al canon con Gemini 2.5 Flash Image.
> 4. Sube las imágenes generadas a `Generated_By_Gemini` y registra los metadatos.
> 5. Reporta resumen al usuario.

**Nota:** La tarea se ejecuta en modo `ask_user`, lo que significa que se dispara pero requiere confirmación para procesar. Esto previene costos innecesarios si hay imágenes en la carpeta que aún no están listas para generación.

---

## 4. Análisis de Costos

El costo real del sistema es la API de Gemini, ya que el almacenamiento en Drive es gratuito.

| Concepto | Costo |
| :--- | :--- |
| Costo por meme (lectura + descripción + generación) | ~$0.008 USD |
| Costo mensual (150 memes) | ~$1.20 USD |
| Costo anual (1,800 memes) | ~$14.40 USD |
| Almacenamiento Drive | Gratis (5.1 TB disponibles) |

---

## 5. Modos de Producción de Memes

Existen dos modos de producción, ambos válidos dentro del Sistema de Dos Capas (`12_00`). La elección depende de si el chiste de la referencia vive en la frase incrustada o fuera de la imagen.

| Modo | Descripción | Cuándo usarlo | Regla de marca |
| :--- | :--- | :--- | :--- |
| **Estándar (frase en copy)** | Foto estática sin texto incrustado; la frase va en el copy de la publicación | El chiste funciona con el personaje observando/viviendo la situación; formato con mayor evidencia de ER en USM | Sin marca en imagen; hashtags oficiales en copy |
| **Adaptado (frase intacta)** | Recreación de un meme viral externo con el personaje USM y la frase original en español **palabra por palabra** incrustada en la imagen | La referencia externa tiene un chiste cuya fórmula completa (texto + composición) es la pieza; solo referencias de autoría abierta sin crédito identificable | Marca "UniverseSentMe" en letra fina blanca, baja opacidad, integrada en la textura de la escena |

**Reglas duras del modo Adaptado:** (1) la frase original nunca se traduce, parafrasea ni acorta — se verifica palabra por palabra antes de aprobar; (2) se descartan referencias con insultos graves o vulgaridad (incompatibles con la línea "ácido ≠ insulto"), con autoría ajena identificada con crédito explícito (riesgo de reporte o conflicto de crédito), y sin frase en español cuando el formato exige frase; (3) el personaje elegido debe calzar con la escena emocional de la referencia, no forzarse; (4) las piezas adaptadas siguen siendo Capa 1 (memes libres) y el mecanismo de promoción a canon del documento `12_00` aplica normalmente; (5) **identidad física y estilo de animación no negociables**: toda pieza gráfica debe generarse usando como referencia los assets oficiales del proyecto (assets 2K en archivos compartidos) o los diseños aprobados en la Biblia de canon (`universe-sent-me-1`, carpeta `02 Personajes/`); nunca referencias improvisadas. Si un personaje no tiene asset oficial (ej. Kael, Maeve), el diseño propuesto se somete a validación explícita de Fernando antes de publicar. Ejemplos del primer banco adaptado: `Operations/Production/CNT028_Memes_Adaptados_Drive_Frase_Intacta.md` (v2.0).

---

## 6. Integración con la Máquina de Estados

Los memes se integran en la arquitectura del calendario escalable con las siguientes consideraciones:

-   **Estado Inicial:** `Idea`
-   **Dificultad de Producción:** `Baja` (al ser generados por IA).
-   **Es_Reutilizable:** `Sí` (generalmente, salvo que sea un experimento específico).

Los memes ya publicados (como el archivo de mayo) entran directamente en la `Reuse Queue` (Cola de Reutilización) del Growth OS para ser adaptados o republicados según las reglas de 30 días.

---

## 7. Documentación Relacionada

-   **Pipeline vigente de publicación:** `GrowthOS/13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md` y `GrowthOS/Integracion_Growth_OS.md`
-   **Cola de Reutilización:** `GrowthOS/01_03_Reuse_Queue.md`
-   **Script de Generación:** `usm_meme_generator.py` (en el entorno de Manus)
-   **Script de Procesamiento Drive:** `usm_meme_drive_processor.py` (en el entorno de Manus)
-   **Banco de memes adaptados (modo Adaptado):** `../Operations/Production/CNT028_Memes_Adaptados_Drive_Frase_Intacta.md`
