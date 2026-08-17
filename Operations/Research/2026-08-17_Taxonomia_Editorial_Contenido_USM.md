---
title: "Taxonomía editorial de contenido Universe Sent Me"
purpose: "Normalizar personajes, roles narrativos, tipos de humor y potencial de etiquetado para que el análisis del Growth OS no dependa de convenciones de filenames."
status: "Review"
created: 2026-08-17
updated: 2026-08-17
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "GrowthOS/Content_Inventory.csv"
  - "Operations/Research/2026-08-17_Analisis_Formato_Personajes_Horarios_Junio.md"
  - "Operations/Research/2026-08-17_Reporte_Final_Recopilacion_Junio.md"
organization: "Operations/Research"
---

# Taxonomía editorial de contenido Universe Sent Me

## Propósito

Esta taxonomía crea un vocabulario común para analizar contenido nuevo, reuse e histórico. No reemplaza los campos canónicos de personajes ni convierte inferencias editoriales en canon. Su función es analítica y operativa.

## Campos normalizados

| Campo | Valores recomendados | Regla |
|---|---|---|
| `personaje_principal_normalizado` | Nombre canónico o `No identificado` | Usar primero el campo existente y la evidencia editorial; no inferir solo por color o parecido visual |
| `personajes_secundarios_normalizados` | Lista separada por `;` | Registrar solo personajes explícitos o confirmados |
| `rol_narrativo` | `Protagonista`, `Dúo o pareja`, `Reparto coral`, `Narrador u observador`, `Reacción`, `Mascota o animal`, `Objeto o concepto`, `Sin personaje`, `No determinado` | Describe la función de la pieza, no el canon del personaje |
| `tipo_humor_normalizado` | `Relatable cotidiano`, `Existencial o absurdo`, `Observacional social`, `Humor ácido o negro`, `Autodepreciación`, `Sexual o insinuación`, `Fandom o referencia`, `Reacción o emoji`, `Mixto`, `No determinado` | Puede tener más de un valor separado por `;` |
| `potencial_etiquetado` | `Alto`, `Medio`, `Bajo`, `No determinado` | Alto si invita naturalmente a pensar en otra persona, etiquetar o compartir; no se asigna solo por tener personajes |
| `confianza_taxonomia` | `Alta`, `Media`, `Baja` | Alta: evidencia explícita en inventario/caption/asset; Media: inferencia editorial razonable; Baja: falta de información |
| `fuente_taxonomia` | `Inventario`, `Caption Meta`, `Filename`, `Revisión visual`, `Inferencia editorial` | Registrar la fuente dominante |
| `nota_taxonomia` | Texto libre | Explicar ambigüedades, convenciones de filename o decisiones especiales |

## Reglas de consistencia

El nombre `Universe` en un filename genérico no basta para asignar a Universe como protagonista si la pieza contiene otro personaje claramente identificado. Los nombres de archivo como `Universe - Existencial` se consideran evidencia de asset, no descripción narrativa completa.

`potencial_etiquetado` debe distinguir entre una pieza que invita a etiquetar a alguien y una pieza que simplemente tiene varias figuras. Se clasificará como Alto cuando exista una situación interpersonal reconocible, una frase dirigida a otra persona o una plantilla socialmente transferible.

La taxonomía no se usará para modificar el canon. Si existe conflicto entre una etiqueta analítica y un documento de Canon, el documento de Canon tiene prioridad y la discrepancia se registra en `nota_taxonomia`.

## Aplicación inicial

La primera aplicación se hará sobre las 79 filas actuales de `Content_Inventory.csv`. Los registros históricos de junio y julio se normalizarán en sus tablas analíticas relacionadas, conservando los campos originales y marcando las inferencias con su nivel de confianza.

La taxonomía deberá revisarse cuando el usuario confirme nuevos personajes, cuando se incorporen assets con evidencia visual adicional o cuando aparezcan categorías de humor que no encajen en el vocabulario actual.
