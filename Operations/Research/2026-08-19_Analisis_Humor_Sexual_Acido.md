---
title: "Análisis de humor sexual y humor ácido — Junio"
purpose: "Comparar el rendimiento histórico de publicaciones con humor sexual y ácido usando métricas Meta y evidencia visual, sin convertir señales preliminares en reglas."
status: "Review"
created: 2026-08-19
updated: 2026-08-19
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-19_Humor_Sexual_Acido_Codificado.csv"
  - "Operations/Research/2026-08-19_Humor_Sexual_Acido_Resumen.csv"
  - "Operations/Research/2026-08-19_Hallazgos_Humor_Sexual_Acido.md"
  - "GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md"
organization: "Operations/Research"
---

# Análisis de humor sexual y humor ácido

## Método

Se seleccionaron publicaciones históricas de junio con captions o señales visuales relacionadas con humor sexual, insinuación, insulto, cinismo, autodesprecio o remate social mordaz. Se recuperaron las imágenes desde Meta y la clasificación final se hizo mediante revisión visual. Las métricas son lifetime observadas; no se mezclan con las ventanas 24/72h de la prueba activa de agosto.

La selección inicial por palabras produjo falsos positivos. “Amor”, “pareja”, “cuerpo” o “enamorarse” no bastan para clasificar una pieza como sexual. Se exigió contacto sexual, insinuación explícita, doble sentido corporal o remate sexual visible. El humor ácido se codificó cuando existe insulto, cinismo, crueldad verbal, autodesprecio o una observación social mordaz.

## Resultado agregado

| Tipo de humor | n | Mediana de interacciones | Mediana de comentarios | Mediana de shares | Veredicto |
|---|---:|---:|---:|---:|---|
| Humor ácido | 13 | 20 | 2 | 4 | Exploratoria |
| Humor sexual explícito | 1 | 47 | 2 | 4 | Inconclusa por muestra mínima |
| Humor sexual sugerente | 1 | 16 | 1 | 3 | Inconclusa por muestra mínima |

## Hallazgos

El humor ácido tiene una muestra suficientemente amplia para una señal exploratoria, pero su dispersión es extrema. El post de “ser el malo de la historia” alcanzó 1,308 interacciones y 392 shares, mientras que varias piezas ácidas quedaron por debajo de 20 interacciones. Por eso la mediana de 20 interacciones y 4 shares es más representativa que el total agregado, pero todavía conviene subdividir el humor ácido por función.

Las subcategorías más útiles para una siguiente revisión son: **relacional/antihéroe**, **insulto o autodesprecio**, **observacional**, **ansiedad/absurdo**, **infografía absurda** y **ciclos relacionales**. No es correcto tratar todo el humor ácido como una sola fórmula creativa.

El humor sexual no permite una comparación válida todavía. Solo hay un caso sexual explícito confirmado visualmente —hada besando a un humano, con remate sobre manosearse— y un caso sugerente relacionado con el cuerpo y la atracción. Ambos tienen pocos casos para establecer una diferencia contra el humor ácido.

El dato operativo más importante es que el caso sexual explícito no supera al outlier ácido en shares: obtuvo 47 interacciones y 4 shares. Esto no demuestra que el humor sexual funcione peor; demuestra que la muestra sexual es insuficiente y que no debe sobreinterpretarse una pieza aislada.

## Veredicto Growth OS

| Hipótesis | Estado | Decisión |
|---|---|---|
| El humor ácido aumenta la difusión | Señal exploratoria | Mantener como hipótesis; subdividir por función narrativa |
| El humor sexual explícito genera más shares | Inconclusa | No convertir en regla; reunir más casos comparables |
| El humor sexual debe separarse del humor ácido | Confirmada metodológicamente | Mantener categorías separadas |
| Caption sexual implica humor sexual | Rechazada | Exigir evidencia visual o remate explícito |

No se modifican calendario, CNT, Instagram ni canon. El resultado solo actualiza la taxonomía y la agenda de aprendizaje.

## Próximo lote recomendado

La siguiente ampliación debe reunir al menos cuatro casos sexuales visualmente confirmados y comparables, separando explícito de sugerente. Para el humor ácido, conviene analizar una pregunta más concreta: **qué subcategoría explica el outlier de difusión —relacional/antihéroe, insulto/autodesprecio u observacional—**. Si no se alcanzan cuatro casos sexuales comparables, el resultado debe permanecer inconcluso.
