# Production Queue

**Propósito:** Lista de contenido que requiere producción nueva (generación de assets, edición, redacción de guiones) antes de poder ser programado.
**Estado:** Active
**Fecha de creación:** 2026-07-31
**Última actualización:** 2026-08-09
**Versión:** 1.1
**Autor:** Manus AI
**Documentos relacionados:** `01_00_Arquitectura_Calendario_Escalable.md`, `01_02_Content_Backlog.md`

---

## Contenido en Producción o Pendiente de Producción

| ID_Pieza | Título | Personaje Principal | Formato | Dificultad | Estado Actual | Dependencias / Notas |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| CNT-002 | Wilfred reseña su propio peluche | @char_USM_wilfred | Reel (~14s) | Media | **Publicado** (FB, 30-Jul 9:16 AM) | 4 shots. Contraste de estilos (cel-shaded vs fotorrealista). |
| CNT-023 | Sección recurrente '¿Qué me llegó?' | Rotativo | Reel recurrente | Baja | Pendiente de producción (Episodio 2) | Formato repetible. Episodio 1 = CNT-002 (ya publicado 30-Jul). Requiere productos de afiliación. |
| CNT-003 | Trailer 001 — Universe Sent Me | @char_USM_universe | Trailer (~32s) | Alta | Pendiente de producción | 5 shots. Requiere música folk-orquestal y edición final. |
| CNT-008 | Elara — cartas mágicas y astrología | @char_USM_elara | Foto / Reel / Carrusel | Media | Idea | Requiere aprobación de identidad visual diferenciada (no tarot). |
| CNT-015 | Fantasma — contenido contemplativo | @char_USM_fantasma | Reel / Foto / Frase | Media | **Publicado** (5 Ago 2026) | 4 shots en Flow. Cascada: FB, IG, TT, YT. Audio + copy + hashtags en `Operations/Production/CNT015_Copy_Hashtags_Audio.md`. Pendiente de métricas post-publicación. |
| CNT-004 | La Búsqueda del Frasco Olvidado | @char_USM_universe | Carruseles + Reels | Alta | Bloqueado | **Bloqueado por 5 contradicciones de canon.** Requiere reescritura. |
| CNT-005 | HB-001: Wilfred existencial vs humorístico | @char_USM_wilfred | Reel (2 variantes) | Media | Pendiente de aprobación | Experimento Growth OS. Requiere aprobación de Fernando. |
| CNT-026 | Banco de memes fin de semana 16–17 de agosto (Fantasma, Wilfred, Universe, Pareja, minimalista) | Multichar | Foto (frase en copy) | Baja | **Propuestas listas** — Draft, pendientes de aprobación de Fernando | 5 propuestas con score ≥ 8.5 (`Operations/Production/CNT026_Memes_FinDeSemana_16_17_Ago.md`). M1/M2/M4/M5 usan bases 2K existentes del proyecto; M3 requiere imagen nueva de Maeve + Chico de los Pantalones (alternativa M3-B solo Maeve incluida). Generación final en Flow (Nano Banana 2/Pro). |
| CNT-025 | Experimentos Growth OS — tests A/B | Variable | Reel (parejas) | Media-Alta | Pendiente de aprobación | Requiere aprobación de Fernando. |

---

## Pipeline de Producción (Manus / Make)

Para escalar la producción, el flujo debe seguir estos pasos:

1. **Selección:** Se toma la pieza de mayor prioridad de esta cola.
2. **Generación (Manus/Flow/Higgsfield):** Se generan los assets visuales (shots, imágenes).
3. **Revisión Canon (Claude/Manus):** Se verifica que no existan contradicciones con las reglas de diseño.
4. **Aprobación (Fernando):** Se aprueba el asset final.
5. **Transición:** El estado cambia a `Aprobado` y la pieza pasa a la cola de `Programado`.
