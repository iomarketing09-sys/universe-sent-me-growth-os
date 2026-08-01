# Sistema de Generación y Gestión de Memes

**Propósito:** Documentar el flujo de trabajo para la ingesta, adaptación y publicación de memes en el universo de Universe Sent Me.
**Estado:** Active
**Fecha de creación:** 2026-08-01
**Última actualización:** 2026-08-01
**Versión:** 1.0
**Autor:** Manus AI
**Documentos relacionados:** `01_00_Arquitectura_Calendario_Escalable.md`, `01_04_Production_Queue.md`, `Integracion_Growth_OS.md`

---

## 1. Arquitectura de Ingesta y Almacenamiento

El sistema de memes se divide en dos fases operativas: **Propuestas** (ingesta) y **Archivo Visual** (almacenamiento).

### 1.1 Fase de Propuestas (Google Drive)

La ingesta de nuevos memes ocurre exclusivamente a través de Google Drive. Esta carpeta sirve como bandeja de entrada para Manus.

-   **Ubicación:** `Universe Sent Me > USM > Meme_Proposals`
-   **Estructura:**
    -   `Generated_By_Gemini/`: Contiene las imágenes procesadas y adaptadas al canon por Manus.
    -   `Processed_Log/`: Contiene los metadatos JSON de cada meme procesado.

### 1.2 Fase de Archivo Visual (GitHub)

Para organizar, revisar y mantener el histórico de todos los memes (publicados, generados y descartados), se utiliza un repositorio dedicado en GitHub que despliega una galería web visual.

-   **Repositorio:** `iomarketing09-sys/universe-sent-me-meme-gallery`
-   **Estructura de Carpetas:**
    -   `gallery/Published/[Personaje]/`: Memes ya publicados en redes sociales.
    -   `gallery/Proposed/`: Memes sincronizados desde Drive.
    -   `gallery/Generated/`: Memes adaptados por Gemini.
    -   `gallery/Archived/`: Memes descartados.

---

## 2. Flujo de Trabajo (Pipeline)

El ciclo de vida de un meme sigue los siguientes pasos:

1.  **Propuesta:** Fernando sube una imagen de referencia a la carpeta `Meme_Proposals` en Google Drive.
2.  **Procesamiento (Manus):**
    -   Manus detecta la imagen en Drive.
    -   Se ejecuta el script `usm_meme_generator.py` utilizando el modelo `gemini-2.5-flash-image`.
    -   El prompt utiliza las reglas de diseño del canon (leídas de `Integracion_Growth_OS.md`).
3.  **Sincronización:** Manus sube la imagen generada a `Generated_By_Gemini` (Drive) y a `gallery/Generated/` (GitHub).
4.  **Ingreso al Growth OS:** La pieza se registra en la base de datos central (Google Sheets) con estado `Idea` o `Pendiente de Producción`.
5.  **Revisión y Aprobación:** Sigue el flujo estándar del Growth OS (Revisión Claude -> Aprobación Fernando).
6.  **Publicación y Archivo:** Una vez publicado, la imagen final se mueve a `gallery/Published/[Personaje]/` en el repositorio de GitHub.

---

## 3. Automatización Programada

El sistema cuenta con una tarea programada en Manus que se ejecuta **diariamente a las 9:00 AM (America/Matamoros)**:

> **Revisión diaria de memes en Drive**
> 1. Revisa la carpeta `Meme_Proposals` en Google Drive
> 2. Lista todas las imágenes nuevas encontradas
> 3. Ejecuta `usm_meme_generator.py` para adaptar cada imagen al canon con Gemini 2.5 Flash Image
> 4. Sube las imágenes generadas a `Generated_By_Gemini` (Drive) y `gallery/Generated/` (GitHub)
> 5. Registra metadatos de cada meme procesado
> 6. Reporta resumen al usuario

**Nota:** La tarea se ejecuta en modo `ask_user`, lo que significa que se dispara pero requiere confirmación para procesar. Esto previene costos innecesarios si la carpeta tiene imágenes que no deseas procesar.

---

## 4. Análisis de Costos

El costo real del sistema es la API de Gemini, ya que el almacenamiento en Drive y GitHub es gratuito.

| Concepto | Costo |
| :--- | :--- |
| Costo por meme (lectura + descripción + generación) | ~$0.008 USD |
| Costo mensual (150 memes) | ~$1.20 USD |
| Costo anual (1,800 memes) | ~$14.40 USD |
| Almacenamiento Drive | Gratis (5.1 TB disponibles) |
| Almacenamiento GitHub | Gratis (1 GB por repo) |

---

## 5. Integración con la Máquina de Estados

Los memes se integran en la arquitectura del calendario escalable con las siguientes consideraciones:

-   **Estado Inicial:** `Idea`
-   **Dificultad de Producción:** `Baja` (al ser generados por IA).
-   **Es_Reutilizable:** `Sí` (generalmente, salvo que sea un experimento específico).

---

## 4. Documentación Relacionada

-   **Guía de la Galería de GitHub:** `universe-sent-me-meme-gallery/GUIDE.md`
-   **Script de Generación:** `usm_meme_generator.py` (en el entorno de Manus)
-   **Script de Procesamiento Drive:** `usm_meme_drive_processor.py` (en el entorno de Manus)
