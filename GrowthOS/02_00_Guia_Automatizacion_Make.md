# Guía de Automatización con Make (Growth OS)

**Propósito:** Documentar la estructura de campos, flujos y reglas de negocio necesarias para implementar el sistema de calendario en Make y escalar a 1,000+ piezas.
**Estado:** Active
**Fecha de creación:** 2026-07-31
**Última actualización:** 2026-07-31
**Versión:** 1.0
**Autor:** Manus AI
**Documentos relacionados:** `01_00_Arquitectura_Calendario_Escalable.md`, `GrowthOS/Integracion_Growth_OS.md`

---

## 1. Estructura de la Base de Datos (Google Sheets / Airtable)

Para que Make pueda leer y escribir sin errores, la base de datos debe tener exactamente estos campos y formatos. Se recomienda usar Google Sheets para el MVP por su facilidad de integración con Make.

### Hoja 1: `Content_Database`

| Nombre del Campo | Tipo de Dato | Descripción / Formato |
| :--- | :--- | :--- |
| `ID_Pieza` | Texto | Identificador único (Ej: `CNT-001`). No debe repetirse. |
| `Fecha_Creacion` | Fecha | Formato `YYYY-MM-DD`. |
| `Ultima_Modificacion` | Fecha | Formato `YYYY-MM-DD`. |
| `Estado` | Texto (Select) | Ver Sección 2 (Máquina de Estados). |
| `Titulo` | Texto | Título o logline. |
| `Tipo_Contenido` | Texto (Select) | `Reel`, `Carrusel`, `Foto`, `Historia`, `Trailer`, `Texto`. |
| `Personaje_Principal` | Texto | `@char_USM_[nombre]` o `Variable`. |
| `Personajes_Secundarios` | Texto | Lista separada por comas. |
| `Lugar` | Texto | `@loc_USM_[nombre]` o `N/A`. |
| `Categoria` | Texto (Select) | `Humor`, `Filosofía`, `Tarot`, `Magia`, `Narrativa`, `Afilación`, `Educación`. |
| `Plataforma` | Texto (Select) | `Instagram`, `TikTok`, `YouTube Shorts`, `Facebook`, `Multi`. |
| `Hipotesis_ID` | Texto | `HB-###` o vacío. |
| `Objetivo` | Texto | Propósito estratégico. |
| `Prioridad` | Texto (Select) | `Alta`, `Media`, `Baja`. |
| `Dificultad_Produccion` | Texto (Select) | `Muy_Baja`, `Baja`, `Media`, `Alta`. |
| `Es_Reutilizable` | Casilla (Checkbox) | `Sí` / `No`. |
| `Bloqueado_Canon` | Casilla (Checkbox) | `Sí` / `No`. |
| `Notas_Canon` | Texto | Justificación del bloqueo (opcional). |

### Hoja 2: `HypothesisBank`

| Nombre del Campo | Tipo de Dato | Descripción |
| :--- | :--- | :--- |
| `Hipotesis_ID` | Texto | Identificador único (Ej: `HB-001`). |
| `Descripcion` | Texto | La hipótesis completa. |
| `Estado` | Texto (Select) | `Pendiente`, `Validada`, `Invalidada`. |
| `Resultado` | Texto | Conclusiones extraídas. |

---

## 2. Máquina de Estados (Make Triggers)

Make debe disparar flujos basándose en cambios en el campo `Estado`. Para evitar bucles infinitos o acciones no autorizadas, Make solo debe permitir las siguientes transiciones:

| Estado Origen | Estado Destino | Acción de Make |
| :--- | :--- | :--- |
| `Idea` | `Pendiente de Producción` | Ninguna. |
| `Pendiente de Producción` | `En Producción` | Ninguna. |
| `Pendiente de Producción` | `Reutilizado` | Enviar a cola de programación rápida. |
| `En Producción` | `Pendiente Revisión Claude` | Notificar a Manus/Claude para validación de canon. |
| `Pendiente Revisión Claude` | `Pendiente Aprobación Fernando` | Notificar a Fernando (Telegram/Email). |
| `Pendiente Aprobación Fernando` | `Aprobado` | Enviar a cola de programación (`Scheduled`). |
| `Pendiente Aprobación Fernando` | `Rechazado / Requiere Reescritura` | Notificar a Fernando con los motivos. |
| `Rechazado / Requiere Reescritura` | `En Producción` | Ninguna. |
| `Aprobado` | `Programado` | Programar en la plataforma correspondiente (API Meta/TikTok). |
| `Programado` | `Publicado` | Mover a cola de análisis. |
| `Publicado` | `En Análisis` | Esperar 7 días y extraer métricas. |
| `En Análisis` | `Archivado` | Cerrar pieza. |
| `En Análisis` | `Reutilizado` | Enviar a cola de reutilización. |

---

## 3. Flujos Recomendados de Make (Automatizaciones)

### Flujo 1: Notificación de Aprobación (ROI Alto)
**Propósito:** Reducir el tiempo de espera entre la aprobación de Fernando y la programación.
**Trigger:** `Watch Rows` (Google Sheets) donde `Estado` cambia a `Aprobado`.
**Acciones:**
1. Formatear mensaje: "🟢 *Aprobado:* {Titulo} ({ID_Pieza}) listo para programación."
2. Enviar a Telegram/Slack al canal del equipo.

### Flujo 2: Generación Semanal del Calendario (ROI Alto)
**Propósito:** Crear el borrador del calendario sin intervención manual.
**Trigger:** `Scheduled` (Cada domingo a las 23:00).
**Acciones:**
1. `Search Rows` en `Content_Database` donde `Estado` == `Aprobado` Y `Es_Reutilizable` == `Sí`.
2. `Search Rows` donde `Estado` == `Aprobado` Y `Es_Reutilizable` == `No`.
3. Combinar ambas listas priorizando las reutilizables.
4. Aplicar reglas de equilibrio (filtrar por `Personaje_Principal` para asegurar variedad).
5. Crear nuevas filas con `Estado` == `Programado` y asignar las fechas de la próxima semana.
6. Enviar resumen a Fernando para revisión final.

### Flujo 3: Bloqueo de Canon de Emergencia (ROI Medio)
**Propósito:** Evitar la publicación accidental de contenido que viola el canon.
**Trigger:** `Watch Rows` donde `Bloqueado_Canon` cambia a `Sí`.
**Acciones:**
1. Verificar si `Estado` es `Programado` o `Publicado`.
2. Si es así, cambiar `Estado` a `Archivado` inmediatamente.
3. Enviar alerta roja a Telegram: "🔴 *BLOQUEO CANON:* {Titulo} ha sido bloqueado y archivado por seguridad."

### Flujo 4: Análisis Automático de Publicaciones (ROI Alto - Growth OS)
**Propósito:** Recopilar métricas para validar hipótesis.
**Trigger:** `Scheduled` (Cada lunes a las 09:00).
**Acciones:**
1. `Search Rows` donde `Estado` == `En Análisis`.
2. Llamar a las APIs de Instagram/TikTok/YouTube para extraer Vistas, Retención e Interacciones.
3. Actualizar las filas con las métricas.
4. Si la pieza tiene `Hipotesis_ID`, actualizar el estado de la hipótesis en `HypothesisBank` según los resultados.
5. Cambiar el `Estado` de la pieza a `Archivado`.
