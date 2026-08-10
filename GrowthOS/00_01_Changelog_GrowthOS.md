# Changelog — Growth OS

**Propósito:** Registro centralizado de hitos, integraciones, cambios estratégicos y actualizaciones de arquitectura. Este documento permite a los agentes (Manus, Claude, etc.) sincronizar contexto rápidamente sin re-leer todo el repositorio.
**Estado:** Active
**Fecha de creación:** 2026-08-05
**Última actualización:** 2026-08-10
**Versión:** 1.6
**Autor:** Manus AI (CGO); entradas [1.1.1], [1.2.4], [1.2.5], [1.2.6] añadidas por Claude
**Documentos relacionados:** `00_Índice.md`, `09_00_Estandar_Documentacion_Interna.md`, `Studio_Governance.md`

---

## [1.2.6] — 2026-08-10 (Claude)
### Añadido
- **Sistema de Dos Capas:** `12_00_Sistema_Dos_Capas_Contenido_Canon.md`. Formaliza dirección estratégica de Fernando: separa la capa de memes/reels (libre, orientada a algoritmo y audiencia amplia no-seguidora) de la capa de canon (Biblia, decisiones permanentes). Margen amplio confirmado para todos los personajes sin distinción de círculo — los memes son proceso de descubrimiento tanto para elenco nuevo como establecido. Define 3 límites duros que aplican incluso en capa libre (identidad física fija, vínculos que comprometan narrativa futura, Gramática Emocional Invisible). Formaliza mecanismo de promoción deliberada meme→canon: Claude alerta cuando un patrón cruza umbral (3+ piezas/30 días con rendimiento consistente), Fernando decide, nunca automático.
### Nota
- Documenta explícitamente que `Canon_Contradictions_Report.md` aplica solo a narrativa seria (historias/episodios), nunca a memes sueltos — 3 de sus 5 contradicciones históricas resultaron ser falta de registro formal de nombres (Silvio/Maeve/Kiri), no errores de contenido, evidencia que motivó esta separación.
- Sección 5 deja abierto un futuro registro cualitativo de insights de comunidad (comentarios con historias personales/puntos de vista) — pendiente de primer uso real, sin ejemplo generado en esta sesión.

---

## [1.2.5] — 2026-08-10 (Claude)
### Añadido
- **Calendario 10-16 agosto:** `05_03_Calendario_10_16_Agosto.md`. Cambio de estrategia por instrucción de Fernando: reduce proporción de reuse a máximo 1 pieza/día (solo "top" ya validados por datos), prioriza 14 piezas nuevas de personajes del elenco extendido (Maeve, Kael, Silvio, Evan, Kiri, Elara, Universe). Horarios elegidos por análisis de mediana horaria/diaria sobre 99 posts reales (Windsor.ai, julio), no por suposición. Reels diarios quedan como TBD — Fernando define contenido día a día.
### Nota
- Fernando indicó que varias de las 14 piezas nuevas no pasaron revisión formal de canon y pidió posponer esa revisión a sesión dedicada — documentado explícitamente en el nuevo calendario, sección 8 (pendientes). También mencionó estar considerando invertir el flujo canon→contenido (que los datos de rendimiento de memes informen la Biblia); queda registrado como dirección en discusión, no como cambio de proceso implementado.
- `05_02_Calendario_04_09_Agosto.md` marcado como Superseded en el índice (semana ya cerrada).

---

## [1.2.4] — 2026-08-08 (Claude)
### Añadido
- **Reporte mensual Junio-Julio 2026:** `../Operations/Research/2026-08-08_Reporte_Mensual_Junio_Julio_2026.md`. Cierra el vacío de datos entre el reporte de mayo (`mayo_2026_top_posts_metaBS.md`) y el análisis de 28 días de agosto (`agosto_2026_analisis_28_dias.md`). 61 días cubiertos vía Windsor.ai (`facebook_organic`), métrica de reacciones+comentarios+shares (misma metodología que el ciclo diario de agosto, ya que alcance/impresiones está deprecado). Julio creció +269% en interacciones totales vs. junio. Confirma con datos propios tres posts ya listados por alcance en `08_00_Metricas_Baseline_Plataformas.md` (21 jul, 28 jul, 24 jul), subiendo la confianza del patrón minimalista de "hipótesis reciente" a "tendencia de 3 meses".

---

## [1.2.3] — 2026-08-08
### Añadido
- **Ciclo diario de métricas 24h (Manus CGO, rutina programada):** primer ciclo automatizado registrado en `../Operations/Research/2026-08-08_Ciclo_Diario_Metricas_24h.md`. 6 posts FB en 24h (128 interacciones, 23 shares). Post top: Fantasma minimalista 👻 (42 reacciones, 11 shares). Hipótesis nuevas H11-H14 registradas en el Sheet "USM Growth OS".
### Corregido
- **Limitación de API:** las métricas de alcance/impresiones (`post_impressions`, `page_impressions`, etc.) están deprecadas en Graph API v21.0 para la página; el ciclo usa conteos de objeto (`reactions.summary`, `comments.summary`, `shares`) como workaround validado y propone `shares/interacciones ≥ 0.25` como proxy provisional de viralidad.
- **Instagram:** la vinculación del conector se cambió de @firmabordados a @universe_sent_me_0326; el conector aún reporta "not connected" y requiere re-autorización en la interfaz de Manus.
---

## [1.2.2] — 2026-08-07
### Corregido
- **Reestructuración del Catálogo de Productos:** `12_00_Catalogo_Productos_MercadoLibre.md` pasa a versión 2.0 con enfoque "Historia → Personaje → Producto" en lugar de "Personaje → Producto". Se eliminaron productos genéricos (audífonos, organizadores, cámara WiFi) que no conectan con la identidad de la página. Se reemplazaron las tiras LED RGB de Silvio por productos de caos visual (máquina de humo, bola disco, máscara LED, máquina de burbujas). Se agregaron pools de productos por personaje (Wilfred, Elara, Universe, Fantasma, Kiri, Silvio).

---

## [1.2.1] — 2026-08-06
### Corregido
- **Actualización de Tendencias:** El catálogo de productos (`12_00_Catalogo_Productos_MercadoLibre.md`) se basaba en datos de tendencias de enero 2026. Se ha actualizado la referencia para reflejar las tendencias actuales de Q3 2026 (agosto), validando que la mayoría de los productos seleccionados (como el Proyector LED Galaxia) siguen siendo virales y pertinentes para la temporada.

---

## [1.2.0] — 2026-08-05
### Añadido
- **Integración de Monetización:** Creación de la estrategia de Mercado Libre Afiliados (`11_00_Estrategia_Monetizacion_MercadoLibre.md`).
- **Sección Story-Commerce:** Activación del formato "¿Qué me llegó?" en el Content Backlog (`CNT-023`).
- **KPIs de Afiliados:** Incorporación de métricas de conversión y clics en `08_00_Metricas_Baseline_Plataformas.md`.
- **Este Changelog:** Creación de `00_01_Changelog_GrowthOS.md` para gestión de contexto.

### Actualizado
- **Calendario Editorial:** Añadido calendario oficial 4-9 de agosto validado por Fernando.
- **Reportes de Análisis:** Actualización de reportes de agosto con datos de Top Memes y métricas de Facebook.

---

## [1.1.1] — Corrección y contexto de canon faltante (Claude, 2026-08-05)

### Corregido
- Fecha real de desbloqueo de Silvio y Kiri: **2026-08-03**, no 08-04. Ver commits `f7bebca` y `8e9fe9a` en el repositorio de canon (`universe-sent-me-1`).

### Añadido — hitos de canon no reflejados antes en este changelog
Este changelog vive en Growth OS, pero varios de los hitos de esta semana ocurrieron en el repositorio de canon (`universe-sent-me-1`), donde Manus tiene solo lectura. Se registran aquí para que ningún agente tenga que adivinarlos:

- **Silvio (El Payaso):** su primer reference sheet usaba el arquetipo del "payaso triste" clásico (lágrimas pintadas, mueca de tristeza), lo cual contradecía la regla de diseño ya cerrada. Fernando aprobó un diseño corregido (sonrisa cómplice, ceja levantada) — **ese es el único diseño válido para producción.** Corolario visual documentado en `02 Personajes/Primer Círculo/Payaso/03 Reglas de diseño.md` (canon, commit `8e9fe9a`).
- **Kiri (El Hada):** además del nombre, se confirmó una varita como objeto personal (canon, `00 Resumen.md` de Hada, commit `990a69c`). Su función narrativa todavía no se ha desarrollado.
- **Dos lugares nuevos, ambos en estado PROPUESTA (no CANON todavía):**
  - `La Hoguera.md` — punto de encuentro cercano a la ciudad, de escala íntima a grupal, posible entrada al Bosque.
  - `La Ciudad.md` — ficha deliberadamente incompleta. Confirmado: dirección visual (arquitectura arena/terracota) y una criatura gigante en el cielo, sin historia todavía, vista con naturalidad, sin interacción de ningún personaje — es una restricción narrativa activa, no un vacío a llenar.
- **Maeve (Chica del Suéter):** su diseño está confirmado y aprobado (carpeta Drive revisada), pero **todavía no tiene commit formal en el repo de canon** — a diferencia de Kiri y Silvio, que ya están cerrados. Tratar como "aprobado por Fernando, pendiente de registro en Biblia" hasta nuevo aviso.

---

## [1.1.0] — 2026-08-04
### Añadido
- **Kit de Hashtags USM:** Creación de `10_00_Kit_de_Hashtags_USM.md` para estandarizar etiquetas.
- **Desbloqueo de Personajes:** Desbloqueo operativo de Silvio y Kiri tras validación de canon.

### Corregido
- **Corrección de Identidad:** Ajuste de tags Maeve/MaeveUSM y LoresUSM para consistencia con publicaciones previas.

---

## [1.0.0] — 2026-08-03
### Añadido
- **Estándar de Documentación:** Formalización de `09_00_Estandar_Documentacion_Interna.md`.
- **Métricas Baseline:** Integración de datos reales de Windsor.ai para FB e IG.
- **Arquitectura CGO v3.0:** Implementación de la máquina de estados de contenido y colas de producción.

### Corregido
- **Ajuste de Canon:** Corrección masiva (6 archivos) sobre la "inmovilidad" del Fantasma; aclarado como bloqueo emocional, no físico.

---

## [0.9.0] — 2026-08-01 a 2026-08-02
### Añadido
- **Registro Maestro de Reels:** Creación de `07_00_Registro_Maestro_Reels.md`.
- **Auditoría Higgsfield:** Documentación para la candidatura al Filmmaker Grant.
- **Blueprint de Producción:** Storyboard y guion para el Showreel de USM.

---

## Guía para Agentes (Instrucción de Lectura)
Al iniciar una nueva sesión o tarea, los agentes deben:
1. Leer `00_01_Changelog_GrowthOS.md` para identificar cambios desde su última interacción.
2. Verificar el `00_Índice.md` para ubicar nuevos documentos mencionados en el changelog.
3. No proponer cambios que contradigan hitos marcados como "Active" o "Canon" en este registro.
4. Recordar que este changelog vive en Growth OS, pero puede registrar hitos ocurridos en el repositorio de canon (`universe-sent-me-1`) cuando afectan la producción — Manus tiene acceso de solo lectura ahí y debe confiar en lo que Claude/Fernando documenten aquí sobre ese repositorio, sin asumir que un silencio significa que no hubo cambios.
