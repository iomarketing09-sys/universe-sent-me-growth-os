# Reuse Queue

**Propósito:** Lista del contenido con mayor potencial para ser reutilizado durante las próximas semanas, priorizando formatos de bajo costo y alta viralidad.
**Estado:** Active
**Fecha de creación:** 2026-07-31
**Última actualización:** 2026-08-01
**Versión:** 1.0
**Autor:** Manus AI
**Documentos relacionados:** `01_00_Arquitectura_Calendario_Escalable.md`, `01_02_Content_Backlog.md`

---

## Ingreso masivo: Mayo 2026

El 1 de agosto de 2026 se procesaron 168 memes publicados en mayo. De estos, 111 fueron clasificados automáticamente y se han registrado en `Operations/Memories/Reuse_Queue_Mayo_2026.csv`.

**Resumen de Mayo 2026:**
- **Total procesados:** 168
- **Clasificados:** 111
- **Personaje principal:** Universe (53), Wilfred (16), Elara (12), Mixto (12).
- **Temas principales:** Relatable (52), Absurdo (17), Sarcástico (16).

### Tabla de Contenido Prioritario (Top 5)

| ID_Pieza | Título | Personaje Principal | Formato | Potencial de Reutilización | Acción Requerida |
| :--- | :--- | :--- | :--- | :--- | :--- |
| MAYO-001 | Top 10 Memes Universe (Relatable) | @char_USM_universe | Foto / Carrusel | **Muy Alto** | Seleccionar los 10 memes de Universe con mayor engagement del CSV para republicar. |
| MAYO-002 | Top 5 Memes Wilfred (Absurdo/Sarcástico) | @char_USM_wilfred | Foto / Reel | **Alto** | Seleccionar los 5 mejores memes de Wilfred para Reels o imágenes. |
| MAYO-003 | Compilación Memes Elara (Emocional/Reflexivo) | @char_USM_elara | Foto / Carrusel | **Alto** | Crear un carrusel con los memes emocionales de Elara. |
| CNT-006 | Tarot de Universe (contenido evergreen) | @char_USM_universe | Foto / Carrusel / Reel | **Muy Alto** | Reciclar las imágenes/cartas más virales de Facebook para crear nuevos Reels o Carruseles. |
| CNT-024 | Frase del día — personaje + principio filosófico | Rotativo | Foto / Historia | **Muy Alto** | Crear plantillas base para asignar frases de los 9 Principios a los personajes del Primer Círculo. |

---

## Contenido Prioritario para Reutilización (Histórico)

El siguiente contenido ha sido identificado como reutilizable (`Es_Reutilizable == Sí`) y debe ser considerado primero para llenar los espacios del calendario antes de producir piezas nuevas. **Nota:** Bajo la política del Growth OS, solo se pueden reutilizar piezas que hayan cumplido al menos 30 días desde su última publicación.

| ID_Pieza | Título | Personaje Principal | Formato | Potencial de Reutilización | Acción Requerida |
| :--- | :--- | :--- | :--- | :--- | :--- |
| CNT-006 | Tarot de Universe (contenido evergreen) | @char_USM_universe | Foto / Carrusel / Reel | **Muy Alto** (1.36M vistas históricas) | Reciclar las imágenes/cartas más virales de Facebook para crear nuevos Reels o Carruseles. |
| CNT-001 | Mi gato: tarotista (meme-to-reel) | @char_USM_universe | Reel (~9s) | **Alto** (Meme ya viral) | Revisar continuidad de los 3 shots (actualmente generados en Flow) y aprobar para publicación. |
| CNT-024 | Frase del día — personaje + principio filosófico | Rotativo | Foto / Historia | **Muy Alto** (Bajo costo) | Crear plantillas base para asignar frases de los 9 Principios a los personajes del Primer Círculo. |
| CNT-007 | Wilfred — sabiduría del bosque | @char_USM_wilfred | Foto / Reel / Frase | **Alto** | Extraer citas filosóficas del canon de Wilfred para publicaciones de bajo esfuerzo. |
| CNT-016 | Filosofía — Principios como contenido | Variable | Foto / Carrusel / Frase / Reel | **Alto** | Adaptar los 9 principios filosóficos a formatos visuales simples. |

---

## Reglas de Reutilización y Estrategia

1. **No reutilizar por existir:** Nunca reutilices contenido únicamente porque existe. Antes de recomendar una reutilización debes verificar:
   - Tiempo desde la última publicación.
   - Temporada del contenido.
   - Contexto actual.
   - Rendimiento histórico.
   - Saturación del personaje.
   - Saturación del formato.
   - Objetivos actuales del Growth OS.

**Criterios Específicos para Reels:**
- **Prioridad Alta:** Reels con alto alcance a no-seguidores (>90%) y buen tiempo de reproducción (>7 segundos).
- **Personajes Clave:** Fantasma y Universe (gato con lentes) en situaciones visualmente ricas.
- **Duración Óptima:** Idealmente entre 7 y 12 segundos, con gancho visual más fuerte en los primeros 3 segundos.
- **Evitar:** Reels de texto genérico o con baja retención.

2. **Regla de Antigüedad (30 días):** Ninguna pieza puede ser reutilizada si han pasado menos de 30 días desde su `Fecha_Ultima_Publicacion`.
3. **Bloqueo Canon:** Ninguna pieza en esta cola puede ser reutilizada si su campo `Bloqueado_Canon` es `Sí`.
4. **Automatización Make:** El flujo de Make `Flujo de Generación de Calendario` debe filtrar automáticamente esta cola (`Es_Reutilizable == Sí` Y `Dias_Desde_Publicacion` >= 30) para llenar los días vacíos del calendario semanal.
