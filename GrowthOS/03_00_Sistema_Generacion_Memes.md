# Sistema de Generación y Gestión de Memes

**Propósito:** Documentar el flujo de trabajo para la ingesta, aprobación y adaptación de memes en el universo de Universe Sent Me.
**Estado:** Active
**Fecha de creación:** 2026-08-01
**Última actualización:** 2026-08-01
**Versión:** 2.0
**Autor:** Manus AI
**Documentos relacionados:** `01_00_Arquitectura_Calendario_Escalable.md`, `01_03_Reuse_Queue.md`, `Integracion_Growth_OS.md`

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

## 5. Integración con la Máquina de Estados

Los memes se integran en la arquitectura del calendario escalable con las siguientes consideraciones:

-   **Estado Inicial:** `Idea`
-   **Dificultad de Producción:** `Baja` (al ser generados por IA).
-   **Es_Reutilizable:** `Sí` (generalmente, salvo que sea un experimento específico).

Los memes ya publicados (como el archivo de mayo) entran directamente en la `Reuse Queue` (Cola de Reutilización) del Growth OS para ser adaptados o republicados según las reglas de 30 días.

---

## 6. Documentación Relacionada

-   **Guía de Automatización Make:** `GrowthOS/02_00_Guia_Automatizacion_Make.md`
-   **Cola de Reutilización:** `GrowthOS/01_03_Reuse_Queue.md`
-   **Script de Generación:** `usm_meme_generator.py` (en el entorno de Manus)
-   **Script de Procesamiento Drive:** `usm_meme_drive_processor.py` (en el entorno de Manus)
