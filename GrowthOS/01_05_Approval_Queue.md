# Approval Queue

**Propósito:** Lista de contenido que únicamente espera revisión de Claude (validación de canon) o aprobación de Fernando (revisión narrativa/estratégica) antes de poder ser programado.
**Estado:** Active
**Fecha de creación:** 2026-07-31
**Última actualización:** 2026-08-16
**Versión:** 1.4
**Autor:** Manus AI
**Documentos relacionados:** `01_00_Arquitectura_Calendario_Escalable.md`, `01_02_Content_Backlog.md`

---

## Contenido Pendiente de Revisión / Aprobación

Este es el cuello de botella operativo del calendario. Ninguna pieza en esta cola puede ser publicada hasta que su estado cambie a `Aprobado`. CNT-004 se conserva como referencia de revisión futura, pero queda fuera de la cola activa por decisión operativa.

### Pendiente de Revisión de Canon (Claude / Manus)

| ID_Pieza | Título | Personaje Principal | Motivo de Revisión | Acción Requerida |
| :--- | :--- | :--- | :--- | :--- |
| CNT-001 | Mi gato: tarotista (meme-to-reel) | @char_USM_universe | Pendiente de revisión de continuidad visual | Verificar que los 3 shots generados mantengan la consistencia del outfit de Tarotista. |
| CNT-004 | La Búsqueda del Frasco Olvidado | @char_USM_universe | Diferido — no desarrollar por ahora; revisión canónica pendiente si se retoma | No entra en la cola activa. Si se reactiva, revisar texto fuente de capítulos 7, 8 y 10 y la escena de Elara; no reabrir Silvio, que permanece cerrado. |

### Pendiente de Aprobación Estratégica (Fernando)

| ID_Pieza | Título | Personaje Principal | Motivo de Aprobación | Acción Requerida |
| :--- | :--- | :--- | :--- | :--- |
| CNT-005 | HB-001: Wilfred existencial vs humorístico | @char_USM_wilfred | Validación de hipótesis Growth OS | Fernando debe aprobar el diseño del experimento A/B antes de la producción. |
| CNT-025 | Experimentos Growth OS — tests A/B | Variable | Validación de hipótesis Growth OS | Fernando debe aprobar el diseño de los tests A/B. |
| CNT-026 | Banco de memes fin de semana 16–17 de agosto (5 piezas) | Multichar | 5 propuestas con score ≥ 8.5 (`scripts/score_proposal.py`) listas para producir | Fernando debe aprobar las 5 propuestas (o elegir subconjunto) antes de producir las imágenes en Flow. |
| CNT-027 | Meme Fantasma "Ghosting eterno" (derivado de Drive Ideas-Memes) | @char_USM_fantasma | Propuesta con score 9.10/10 (`scripts/score_proposal.py`), base visual con asset 2K existente | Fernando debe aprobar la propuesta (copy + slot) antes de la publicación. |
| CNT-028 | Banco de 5 memes adaptados de Drive (frase intacta + marca en imagen) | Multichar (Fantasma, Kael+Maeve, Silvio, Wilfred, Universe) | 5 imágenes adaptadas generadas con frase original intacta y marca "UniverseSentMe" discreta | Fernando debe aprobar las 5 imágenes (o elegir subconjunto) antes de la publicación. |

---

## Reglas de Desbloqueo

1. **Revisión Canon:** Una vez que Claude/Manus confirme que no hay contradicciones, el estado debe cambiar a `Pendiente Aprobación Fernando`.
2. **Aprobación Fernando:** Solo Fernando puede cambiar el estado a `Aprobado`.
3. **Notificación y registro:** Manus registra el cambio y notifica a Fernando por el canal operativo acordado cuando una pieza pase de `En Producción` a `Pendiente Aprobación Fernando`; este flujo no tiene automatización activa.
