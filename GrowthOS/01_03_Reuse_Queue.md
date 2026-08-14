# Reuse Queue

**Propósito:** Lista del contenido con mayor potencial para ser reutilizado durante las próximas semanas, priorizando formatos de bajo costo y alta viralidad.
**Estado:** Active
**Fecha de creación:** 2026-07-31
**Última actualización:** 2026-08-14
**Versión:** 1.3
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

## Ranking de rendimiento de mayo — 2026-08-14

La selección de reuse de mayo debe usar el cruce reproducible entre Drive y Meta documentado en [`Operations/Research/2026-08-14_Revision_Reuse_Mayo_Junio.md`](../Operations/Research/2026-08-14_Revision_Reuse_Mayo_Junio.md). El ranking completo de 123 assets con coincidencia histórica está en [`Operations/Research/2026-08-14_Reuse_Mayo_Ranking.csv`](../Operations/Research/2026-08-14_Reuse_Mayo_Ranking.csv), y el cruce bruto de 205 publicaciones está en [`Operations/Research/2026-08-14_Reuse_Mayo_Meta_Cruce_Datos.csv`](../Operations/Research/2026-08-14_Reuse_Mayo_Meta_Cruce_Datos.csv).

Para la prueba de dos semanas, seleccionar primero 28 piezas desde la raíz operativa de `05 Mayo`, priorizando `Confirmed_Image_Likely`, máximo y mediana de interacciones, shares, diversidad de personajes y ausencia de bloqueos de canon. Los assets sin coincidencia visual confirmada deben permanecer como `Sin_Historial_Visual_Confirmado` hasta revisión manual. Las carpetas de piezas reutilizadas en julio y agosto quedan fuera de la selección actual por la regla de antigüedad.

## Assets manuales sin historial visual confirmado — 2026-08-14

La revisión manual de los ocho assets sin coincidencia visual añadió dos candidatos directos a la cola experimental:

| Asset | Estado | Uso recomendado |
|---|---|---|
| `260583 - Universe.png` | `Manual_Approved_Candidate` | Reuse Top; humor afectivo de Universe |
| `260673 - Universe.png` | `Manual_Approved_Candidate` | Reuse Top; humor absurdo de Universe |
| `260514 - Que feo fingir que estas bien.png` | `Pending_Copy_Review` | No programar hasta corregir/confirmar `agarrarte las TAs` |
| `260539 - Evan+Kiri.png` | `Pending_Tone_Review` | Requiere aprobación por copy sexualizado |
| `260563.png` | `Pending_Canon_Review` | Confirmar personaje y canon |
| `260663 - Kiri.png` | `Pending_Copy_Review` | Confirmar punchline y evitar repetición de Kiri |
| `Universe - Existencial 260507.png` | `Pending_Tone_Review` | Validar territorio romántico |
| `humor4.16.png` | `Excluded_Brand_Safety` | No usar en la prueba |

La clasificación completa está en [`Operations/Research/2026-08-14_Reuse_Mayo_Unmatched_Review.csv`](../Operations/Research/2026-08-14_Reuse_Mayo_Unmatched_Review.csv). Las dos piezas aprobadas deben mantener separación de personaje dentro de la matriz 3:2 y no publicarse en slots consecutivos de Universe.

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
4. **Validación directa de Manus:** Manus debe filtrar esta cola (`Es_Reutilizable == Sí` Y `Dias_Desde_Publicacion` >= 30) antes de llenar los días vacíos del calendario semanal. La selección no publica automáticamente: cada pieza debe conservar aprobación, bloqueo de canon y trazabilidad.
