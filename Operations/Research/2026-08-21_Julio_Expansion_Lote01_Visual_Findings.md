---
title: "Hallazgos visuales — ampliación individual de julio, lote 01"
purpose: "Conservar la evidencia de la revisión visual Meta→Drive de los candidatos prioritarios de julio antes de integrar filas históricas."
status: Active
created: 2026-08-21
updated: 2026-08-21
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-21_Julio_Expansion_Individual_Lote01.csv"
  - "Operations/Research/2026-08-21_Julio_Expansion_Lote01_Visual_Matches.csv"
  - "Operations/Research/2026-08-21_Julio_Expansion_Lote01_Visual_Contact_Sheet.jpg"
  - "Operations/Research/2026-08-17_Lista_Confirmacion_Assets_Julio.csv"
organization: "Operations/Research"
---

# Hallazgos visuales — ampliación individual de julio, lote 01

## Método

Se seleccionaron 17 publicaciones de julio: la unión de las 12 con más shares y las 12 con más comentarios, excluyendo las seis publicaciones ya reconciliadas individualmente (`CNT-074`–`CNT-079`). Meta aportó la imagen de cada publicación mediante una sola consulta batch y Drive aportó 189 imágenes de la carpeta `07 Julio` mediante sus miniaturas. La similitud perceptual se usó únicamente para ordenar candidatos; la decisión de match se revisó visualmente en el contact sheet.

## Resultado de la revisión visual

El contact sheet muestra **16 coincidencias visuales de alta confianza** y un caso que no debe integrarse todavía. En los 16 casos de alta confianza, la composición, personajes, fondo y texto incrustado coinciden entre la imagen de Meta y la miniatura de Drive. Los matches no se asignaron por filename: el filename se conserva como resultado de la evidencia visual ya comprobada.

| Estado | Casos | Regla aplicada |
|---|---:|---|
| `Visual_Candidate_High` | 16 | Coincidencia visual clara entre Meta y Drive; lista para integración de evidencia, sin CNT automático |
| `Visual_Candidate_Review` | 1 | La imagen de Meta es una composición de dos paneles; el candidato Drive contiene la misma escena, pero la miniatura no permite confirmar que sea el archivo editorial exacto sin revisar el asset original |
| Total | 17 | Ningún caso recibe CNT en esta fase |

El caso borderline corresponde a `Meta_ID 1036844829507460_122142624879072582`, con 1,018 interacciones, 95 shares y 23 comentarios. Meta muestra una composición de dos paneles con una pareja abrazada y globos de texto; el candidato `Universe - Existencial 2607984.jpeg` de Drive muestra la misma pareja y el mismo fondo en dos paneles. La miniatura es demasiado estrecha para confirmar con seguridad el texto completo y la correspondencia editorial exacta. Se mantiene como `Candidate_Review`, no como match confirmado.

Los 16 casos de alta confianza quedan preparados para la siguiente fase: integrar sus `Asset_Ref` normalizados y `Drive_ID` en una capa histórica individual ampliada, conservar el `Meta_ID` y las métricas lifetime existentes, y aplicar taxonomía visual. La integración debe seguir sin crear CNT masivos ni modificar el calendario.

## Limitaciones y control

La consulta de Meta y el inventario de Drive son capas de evidencia. El resultado no reconstruye ventanas de 24/72 horas y no debe mezclarse con P0 o Wave 1 de agosto. Tampoco permite inferir personajes canónicos por el nombre `Universe - Existencial`; la taxonomía de cada caso debe basarse en la imagen y el caption observados.

Antes de marcar el caso borderline como confirmado se requiere descargar o abrir el original de Drive, no solo la miniatura. Si la revisión original confirma texto y composición, podrá promoverse a `Visual_Match_Confirmed`; de lo contrario permanecerá fuera de la integración.

## Archivos de evidencia

- `2026-08-21_Julio_Expansion_Lote01_Visual_Matches.csv`: ranking reproducible de coincidencias y distancias perceptuales.
- `2026-08-21_Julio_Expansion_Lote01_Visual_Contact_Sheet.jpg`: comparación Meta izquierda / Drive derecha.
- `2026-08-21_Julio_Expansion_Lote01_Review_Pair.jpg`: vista ampliada del caso borderline.
- `2026-08-21_Julio_Drive_Asset_Index.json`: índice local de 189 imágenes de `07 Julio` con Drive ID y miniatura.
