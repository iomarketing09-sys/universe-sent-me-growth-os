---
title: "Actualización de movimiento del staging — Firma Bordados"
purpose: "Registrar la decisión de conservar Cloudflare Pages como ruta de hosting y el alcance de movimiento ligero aplicado al staging Color que Trabaja."
status: Active
created: 2026-08-23
updated: 2026-08-23
version: "1.0"
author: "Manus AI"
related_documents:
  - "Operations/Production/2026-08-23_Guia_Staging_Cloudflare_Pages_Firma_Bordados.md"
  - "Operations/Production/2026-08-23_Evaluacion_Migracion_Wix_Hosting_IA.md"
  - "Operations/Production/2026-08-23_Ruta_Staging_WordPress_Firma_Bordados.md"
  - "GrowthOS/00_01_Changelog_GrowthOS.md"
organization: "Operations/Production"
---

# Actualización de movimiento del staging — Firma Bordados

## 1. Decisión

Fernando confirmó que Cloudflare Pages vuelve a ser la ruta preferida para el sitio de Firma Bordados debido a su menor coste y menor carga de mantenimiento frente a WordPress. La alternativa WordPress queda archivada como referencia; no se iniciará una cuenta, contrato ni reconstrucción en WordPress mientras esta decisión esté vigente.

El staging React/Vite se actualizó únicamente en la capa de presentación. Wix, DNS, catálogos, URLs de redes, formulario `mailto:`, textos y datos de contacto no cambiaron.

## 2. Movimiento aplicado

| Capa | Implementación | Límite de seguridad y accesibilidad |
| :--- | :--- | :--- |
| Puntada principal | Ruta SVG azul con puntos rojo/amarillo dibujada una vez en la hero | No cubre contenido, no se repite y no procesa datos |
| Revelado de contenido | Opacidad y desplazamiento de 16 px activados una sola vez al entrar una sección al viewport | Navegación y contenido crítico permanecen disponibles sin animación |
| Microinteracción | Catálogos se elevan, su flecha se desplaza y botones responden con escala táctil | Duración corta; solo usa `transform` y `opacity` donde corresponde |
| Identidad persistente | Reglas de puntada, puntos de registro y metadata de fichas de prenda/servicio en secciones principales | Refuerza Color que Trabaja sin video, parallax, carruseles, partículas ni loops decorativos |
| Preferencia de usuario | `prefers-reduced-motion` desactiva la animación no esencial | El sitio conserva lectura, navegación y acciones completas |

El bloque de contacto mantiene azul Firma como ancla de conversión, equilibrado con una ruta textil amarilla, un punto rojo/amarillo y ritmo editorial claro. Las tarjetas de capacidad y catálogo se ajustaron a fichas de prenda/servicio con etiquetas, metadata y divisores de puntada, evitando el lenguaje visual de tarjetas SaaS genéricas.

## 3. Validación

Se completaron la comprobación de tipos y la compilación Vite. La salida estática continúa generándose en `dist/public`, por lo que permanece compatible con la configuración documentada de Cloudflare Pages. Se revisó visualmente el staging en escritorio de 1280 px y móvil de 375 px; navegación, contenido y CTA siguen legibles, y no se detectó una alteración funcional de Wix o DNS.

La mejora se publicó únicamente en el staging de Manus asociado al proyecto. El posterior paso a Cloudflare Pages sigue requiriendo preparar activos bajo control del cliente, crear su cuenta/repo y obtener autorización explícita antes de cualquier conexión de hosting o dominio.
