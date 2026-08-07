# Skill `usm-content-proposer` — Propuestas de Contenido con Score Mínimo 8.5

**Propósito:** Registrar la existencia y el propósito de la skill `usm-content-proposer` instalada en el entorno de Manus, que garantiza que toda propuesta de contenido nuevo de Universe Sent Me alcance un score mínimo de 8.5/10 contra los drivers validados del Growth OS.
**Estado:** Active
**Fecha de creación:** 2026-08-07
**Última actualización:** 2026-08-07
**Versión:** 1.0
**Autor:** Manus AI (CGO)
**Documentos relacionados:** `Operations/Production/CNT024_Frases_Wilfred_Manana_HumorAcido.md`, `Operations/Research/CNT024_Analisis_Comparativo_Propuestas_vs_28Dias.md`, `Operations/Production/CNT024_Frases_Viral_Elara_Evan_Pareja.md`, `GrowthOS/08_00_Metricas_Baseline_Plataformas.md`

## Qué hace la skill

La skill aplica un flujo de cinco pasos a cada propuesta de contenido: leer los baselines del Growth OS (`references/growth_os_baselines.md`), redactar la pieza con copy y hashtags, auto-evaluarla en un formulario JSON de seis criterios ponderados (relatable 30%, humor/emoción 25%, share hook 15%, giro moderno 10%, voz de personaje 10%, slot 5%) más dos binarios (formato correcto 3%, canon seguro 2%), ejecutar el scoring determinista (`scripts/score_proposal.py`) y reescribir o descartar si el score no llega a 8.5. Incluye también el roster oficial de hashtags USM y las reglas de tono no negociables (anti-moralización, restricciones de canon por personaje, prohibición de Reels de texto).

## Por qué existe

Antes de la skill, la calidad de las propuestas dependía de la memoria de contexto de cada tarea y de documentos dispersos del Growth OS. Esta skill consolida los drivers validados del análisis de 28 días en un sistema de scoring repetible y verificable, de modo que cualquier tarea futura que proponga contenido (frases CNT-024, memes, carruseles, slots nuevos) parta del mismo piso de calidad con evidencia numérica visible.

## Uso

Cualquier tarea del proyecto puede invocar la skill diciendo "propón contenido nuevo" para un personaje, horario o tema; la skill se activa automáticamente por su descripción. El primer usuario en activarla fue la propuesta de frases de Wilfred matutinas (CNT-024 W4), cuya evaluación de ejemplo (8.85/10 PASS) está incluida en la propia skill.

## Actualización de datos

Los baselines de `references/growth_os_baselines.md` están congelados al 2026-08-07 (análisis 7 Jul – 3 Ago). Cuando el proyecto produzca nuevos datos de rendimiento que invaliden los benchmarks actuales (nuevos top posts, horarios, share rates), la skill debe actualizarse con los datos nuevos — la fuente de verdad son los documentos de Research y el Registro Maestro del Growth OS.

*Nota de coherencia: este documento vincula la skill externa con el banco CNT-024 ya documentado, que fue de facto el primer caso de prueba de su rúbrica.*
