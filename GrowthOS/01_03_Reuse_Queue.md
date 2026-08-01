# Reuse Queue

**Propósito:** Lista del contenido con mayor potencial para ser reutilizado durante las próximas semanas, priorizando formatos de bajo costo y alta viralidad.
**Estado:** Active
**Fecha de creación:** 2026-07-31
**Última actualización:** 2026-07-31
**Versión:** 1.0
**Autor:** Manus AI
**Documentos relacionados:** `01_00_Arquitectura_Calendario_Escalable.md`, `01_02_Content_Backlog.md`

---

## Contenido Prioritario para Reutilización

El siguiente contenido ha sido identificado como reutilizable (`Es_Reutilizable == Sí`) y debe ser considerado primero para llenar los espacios del calendario antes de producir piezas nuevas. **Nota:** Bajo la política del Growth OS, solo se pueden reutilizar piezas que hayan cumplido al menos 30 días desde su última publicación.

| ID_Pieza | Título | Personaje Principal | Formato | Potencial de Reutilización | Acción Requerida |
| :--- | :--- | :--- | :--- | :--- | :--- |
| CNT-006 | Tarot de Universe (contenido evergreen) | @char_USM_universe | Foto / Carrusel / Reel | **Muy Alto** (1.36M vistas históricas) | Reciclar las imágenes/cartas más virales de Facebook para crear nuevos Reels o Carruseles. |
| CNT-001 | Mi gato: tarotista (meme-to-reel) | @char_USM_universe | Reel (~9s) | **Alto** (Meme ya viral) | Revisar continuidad de los 3 shots (actualmente generados en Flow) y aprobar para publicación. |
| CNT-024 | Frase del día — personaje + principio filosófico | Rotativo | Foto / Historia | **Muy Alto** (Bajo costo) | Crear plantillas base para asignar frases de los 9 Principios a los personajes del Primer Círculo. |
| CNT-007 | Wilfred — sabiduría del bosque | @char_USM_wilfred | Foto / Reel / Frase | **Alto** | Extraer citas filosóficas del canon de Wilfred para publicaciones de bajo esfuerzo. |
| CNT-016 | Filosofía — Principios como contenido | Variable | Foto / Carrusel / Frase / Reel | **Alto** | Adaptar los 9 principios filosóficos a formatos visuales simples. |

---

## Reglas de Reutilización

1. **Regla de Antigüedad (30 días):** Ninguna pieza puede ser reutilizada si han pasado menos de 30 días desde su `Fecha_Ultima_Publicacion`.
2. **Validación de Formato:** Si un formato (ej. Foto de Tarot) demostró alta viralidad histórica, debe ser reutilizado con ligeras variaciones antes de probar formatos nuevos (siempre respetando la regla de 30 días).
3. **Bloqueo Canon:** Ninguna pieza en esta cola puede ser reutilizada si su campo `Bloqueado_Canon` es `Sí`.
4. **Automatización Make:** El flujo de Make `Flujo de Generación de Calendario` debe filtrar automáticamente esta cola (`Es_Reutilizable == Sí` Y `Dias_Desde_Publicacion` >= 30) para llenar los días vacíos del calendario semanal.
