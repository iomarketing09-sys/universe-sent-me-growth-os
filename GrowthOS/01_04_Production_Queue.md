# Production Queue

**Propósito:** Lista de contenido que requiere producción nueva (generación de assets, edición, redacción de guiones) antes de poder ser programado.
**Estado:** Active
**Fecha de creación:** 2026-07-31
**Última actualización:** 2026-08-16
**Versión:** 1.4
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
| CNT-004 | La Búsqueda del Frasco Olvidado | @char_USM_universe | Carruseles + Reels | Alta | Diferido — no desarrollar por ahora | **Pendiente canónico conservado; si se retoma requerirá texto fuente, revisión y aprobación.** |
| CNT-005 | HB-001: Wilfred existencial vs humorístico | @char_USM_wilfred | Reel (2 variantes) | Media | Pendiente de aprobación | Experimento Growth OS. Requiere aprobación de Fernando. |
| CNT-026 | Banco de memes fin de semana 16–17 de agosto (Fantasma, Wilfred, Universe, Pareja, minimalista) | Multichar | Foto (frase en copy) | Baja | **Propuestas listas** — Draft, pendientes de aprobación de Fernando | 5 propuestas con score ≥ 8.5 (`Operations/Production/CNT026_Memes_FinDeSemana_16_17_Ago.md`). M1/M2/M4/M5 usan bases 2K existentes del proyecto; M3 requiere imagen nueva de Maeve + Chico de los Pantalones (alternativa M3-B solo Maeve incluida). Generación final en Flow (Nano Banana 2/Pro). |
| CNT-025 | Experimentos Growth OS — tests A/B | Variable | Reel (parejas) | Media-Alta | Pendiente de aprobación | Requiere aprobación de Fernando. |
| CNT-027 | Meme Fantasma "Ghosting eterno" (derivado de Drive Ideas-Memes) | @char_USM_fantasma | Foto (frase en copy) | Baja | **Propuesta lista** — Draft, pendiente de aprobación de Fernando | Score 9.10/10 (`Operations/Production/CNT027_Meme_Fantasma_Ghosting_DriveIdeas.md`). Base visual: asset 2K existente del proyecto (Fantasma levitando sobre el bosque); solo requiere copy en publicación. Slot sugerido 4:00–5:00 PM. |
| CNT-028 | Banco de 5 memes adaptados de Drive (frase intacta + marca en imagen) | Multichar (Fantasma, Kael+Maeve, Silvio, Wilfred, Universe) | Foto adaptada | Baja | **Imágenes listas** — Draft, pendientes de aprobación de Fernando | 5 imágenes ya generadas y verificadas palabra por palabra (`Operations/Production/CNT028_Memes_Adaptados_Drive_Frase_Intacta.md`). Modo "Adaptado" formalizado en `03_00`. Assets: 01–05 en archivos compartidos del proyecto.

### Ingreso de Drive — 15 de agosto de 2026

Se incorporaron **38 memes nuevos** directamente desde la raíz operativa `My Drive/Universe sent me/USM/Humor existencial`. El inventario detallado, las referencias de Drive y la primera clasificación visual están en [`Operations/Research/2026-08-15_Inventario_Memes_Nuevos_Drive.md`](../Operations/Research/2026-08-15_Inventario_Memes_Nuevos_Drive.md) y [`Operations/Research/2026-08-15_Inventario_Memes_Nuevos_Drive.csv`](../Operations/Research/2026-08-15_Inventario_Memes_Nuevos_Drive.csv). Todos permanecen en estado `Nuevo_Pendiente_Revision`; no entran automáticamente al calendario hasta aprobación.

---

## Pipeline de Producción (Manus / Graph API)

Para escalar la producción, el flujo vigente debe seguir estos pasos:

1. **Selección:** Se toma la pieza de mayor prioridad de esta cola.
2. **Generación (Manus/Flow/Higgsfield):** Se generan los assets visuales (shots, imágenes).
3. **Revisión Canon (Claude/Manus):** Se verifica que no existan contradicciones con las reglas de diseño.
4. **Aprobación (Fernando):** Se aprueba el asset final.
5. **Transición:** El estado cambia a `Aprobado`; Manus prepara la orden de publicación, valida plataforma, asset, copy y horario, y utiliza Graph API de Meta cuando Fernando autoriza la ejecución.
