# Integración Growth OS ↔ Canon

**Documento de sincronización entre el Growth OS (Manus) y la Biblia de Canon (Claude)**

---

| Campo | Valor |
| :--- | :--- |
| **Última sincronización** | 2026-08-14 |
| **Fuente de canon** | Repo GitHub: `iomarketing09-sys/universe-sent-me-1` (commit `939752c`) |
| **Estado del documento** | v2.2 — Graph API de Meta como ruta operativa; Make archivado; HB-003 en prueba |
| **Propietario** | Manus (Manus AI) |
| **Guardián de Canon** | Claude (vía repo GitHub) |
| **Aprobador final** | Fernando |

---

## 1. Reglas de Diseño Activas (Caché de Canon)

> Cada entrada incluye fecha de sincronización y fuente exacta (archivo + commit).
> Si la fecha de sincronización es anterior a un commit del repo, el caché está desactualizado.

### 1.1 Personajes — Primer Círculo

| Personaje | ID Canon | Regla de Diseño (Resumen) | Fuente | Última sincronización |
| :--- | :--- | :--- | :--- | :--- |
| Universe | `@char_USM_universe` | La profundidad nunca debe aparecer antes que el humor. Conoce el mecanismo pero nunca entiende completamente el propósito ni tiene acceso total. No es orquestador del conflicto. | `02 Personajes/Primer Círculo/Universe/03 Reglas de diseño.md` | 2026-07-31 (commit `939752c`) |
| Wilfred | `@char_USM_wilfred` | Guardián del bosque con barba blanca larga, gorro rojo, personalidad enfocada en sabiduría y humor seco. No moraliza explícitamente ni diagnostica a otros personajes. | `02 Personajes/Primer Círculo/Wilfred/03 Reglas de diseño.md` | 2026-07-31 (commit `939752c`) |
| Elara | `@char_USM_elara` | Lectora de cartas mágicas conectada con astrología y naturaleza. Rol diferenciado de Universe (no es tarotista principal — ese es Universe). | `02 Personajes/Primer Círculo/Elara/03 Reglas de diseño.md` | 2026-07-31 (commit `939752c`) |
| Ganso | `@char_USM_ganso` | *(Pendiente: consultar ficha canónica para regla de diseño activa)* | `02 Personajes/Primer Círculo/Ganso/03 Reglas de diseño.md` | 2026-07-31 (commit `939752c`) |
| Payaso | `@char_USM_payaso` | *(Pendiente: consultar ficha canónica para regla de diseño activa)* **Nota:** El nombre "Silvio" NO existe en canon. No usar hasta confirmación explícita. | `02 Personajes/Primer Círculo/Payaso/03 Reglas de diseño.md` | 2026-07-31 (commit `939752c`) |

### 1.2 Personajes — Segundo Círculo

| Personaje | ID Canon | Nota | Fuente | Última sincronización |
| :--- | :--- | :--- | :--- | :--- |
| Hada (Kiri) | `@char_USM_hada` | Nombre propio confirmado por Fernando (2026-08-03): Kiri. Su territorio emocional es el asombro genuino — la primera vez que una emoción aparece antes del mecanismo para esconderla. Puede tocar la grieta de Wilfred con preguntas simples que la ironía no puede esquivar. | `02 Personajes/Segundo Círculo/Hada/00 Resumen.md`, `01 Territorio emocional.md`, `03 Reglas de diseño.md` | 2026-08-03 (commit `f7bebca`) |
| Evan | `@char_USM_evan` | *(Pendiente: consultar ficha)* | `02 Personajes/Segundo Círculo/Evan/03 Reglas de diseño.md` | 2026-07-31 (commit `939752c`) |
| Chica del Suéter | `@char_USM_chica_sweater` | *(Pendiente: consultar ficha)* | `02 Personajes/Segundo Círculo/Chica del Suéter/03 Reglas de diseño.md` | 2026-07-31 (commit `939752c`) |
| Chico de los Pantalones | `@char_USM_chico_pantalones` | *(Pendiente: consultar ficha)* | `02 Personajes/Segundo Círculo/Chico de los Pantalones/03 Reglas de diseño.md` | 2026-07-31 (commit `939752c`) |
| Fantasma | `@char_USM_fantasma` | Congelado emocionalmente en un instante que nunca cerró — no es incapacidad física. Se aferra por lógica de supervivencia interna, no por nostalgia (ver Territorio Emocional). Restricción real: no puede resolver esa identidad ni "salvar el día" de forma heroica y dramáticamente visible dentro de una misma pieza. *(Corregido 2026-08-02 por Claude — la nota original describía inmovilidad física, que no existe en canon.)* | `02 Personajes/Segundo Círculo/Fantasma/01 Territorio emocional.md`, `03 Reglas de diseño.md` | 2026-08-02 (corrección) |

### 1.3 Lugares

| Lugar | ID Canon | Nota | Fuente | Última sincronización |
| :--- | :--- | :--- | :--- | :--- |
| El Bosque | `@loc_USM_bosque` | Bosque Ancestral — territorio de Wilfred | `06 Lugares/El Bosque.md` | 2026-07-31 (commit `939752c`) |
| Jardines Eternos | `@loc_USM_jardines` | *(Pendiente: consultar ficha)* | `06 Lugares/Jardines Eternos.md` | 2026-07-31 (commit `939752c`) |
| La Plaza del Mercado | `@loc_USM_plaza` | *(Pendiente: consultar ficha)* | `06 Lugares/La Plaza del Mercado.md` | 2026-07-31 (commit `939752c`) |
| Mar de Nubes | `@loc_USM_mar_nubes` | *(Pendiente: consultar ficha)* | `06 Lugares/Mar de Nubes.md` | 2026-07-31 (commit `939752c`) |

### 1.4 Reglas de Diseño de Historias

| Regla | Descripción | Fuente | Última sincronización |
| :--- | :--- | :--- | :--- |
| Profundidad después del humor | La profundidad nunca debe aparecer antes que el humor. | `01 ADN/01.04 Anti-tono.md` | 2026-07-31 (commit `939752c`) |
| Sin moralización explícita | Una historia no puede existir para ilustrar una lección. Ningún personaje puede diagnosticar a otro. La lección debe sentirse sin nombrarse. | `07 Historias/00 Estándar de Historias.md` | 2026-07-31 (commit `939752c`) |
| Fantasma congelado emocionalmente | El Fantasma no puede resolver ni superar de forma dramática y visible su identidad congelada dentro de una misma pieza. No tiene restricción de movilidad física ni de acción. *(Corregido 2026-08-02 por Claude — "Fantasma inmovilizado" describía incapacidad física, que no existe en canon.)* | `02 Personajes/Segundo Círculo/Fantasma/01 Territorio emocional.md`, `03 Reglas de diseño.md` | 2026-08-02 (corrección) |
| Universe limitado | Universe conoce el mecanismo pero nunca entiende completamente el propósito. No es orquestador de conflictos. | `02 Personajes/Primer Círculo/Universe/03 Reglas de diseño.md` | 2026-07-31 (commit `939752c`) |

---

## 2. Calendario Editorial (Roadmap)

> **Bloqueo operativo:** Ningún contenido puede publicarse automáticamente mientras `Estado` ≠ "Aprobado".
> El cambio a "Aprobado" solo puede ser realizado por Fernando o Claude.
> Manus no puede ejecutar una publicación con estado ≠ "Aprobado" ni con `Bloqueado_Canon == Sí`.

> **v2.1:** La arquitectura del calendario sigue documentada en `GrowthOS/01_00_Arquitectura_Calendario_Escalable.md`, pero Make queda retirado de la estrategia operativa. El calendario semanal operativo vive en `GrowthOS/01_01_Calendario_Semanal.md`; Manus valida cada orden y utiliza la API de Graph de Meta para programar o publicar. La guía histórica de Make se conserva archivada en `GrowthOS/02_00_Guia_Automatizacion_Make.md`.

| Semana | Día | Fecha | Plataforma | Formato | Personaje/Lugar | Hook/Título | Brief | ID Canon consultado | Estado Canon | Responsable aprobación | Fecha aprobación |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W1 | Lun | 2026-08-04 | Instagram | Foto / Carrusel | `@char_USM_universe` | Tarot de hoy | Contenido evergreen reutilizable | CNT-006 | Reutilizado | Fernando | — |
| W1 | Mar | 2026-08-05 | Instagram / TikTok | Reel | `@char_USM_universe` | Mi gato: tarotista | Reutilización de meme viral | CNT-001 | Pendiente de Producción | Manus / Fernando | — |
| W1 | Mié | 2026-08-06 | Instagram / Facebook | Foto / Texto | `@char_USM_wilfred` | Frase filosófica (Principio 0) | Voz de Wilfred, bajo costo | CNT-024 | Pendiente de Producción | Manus | — |
| W1 | Jue | 2026-08-07 | Instagram | Reel / Foto | `@char_USM_fantasma` | El instante suspendido | Activación del Fantasma | CNT-015 | Pendiente de Producción | Manus | — |
| W1 | Vie | 2026-08-08 | Instagram | Carrusel / Foto | `@char_USM_elara` | Lectura de astros y naturaleza | Identidad diferenciada de Elara | CNT-008 | Pendiente de Producción | Manus | — |
| W1 | Sáb | 2026-08-09 | Instagram / YouTube Shorts | Reel | `@char_USM_wilfred` | Wilfred reseña su propio peluche | Sección recurrente de afiliación | CNT-023 | Pendiente de Producción | Manus | — |
| W1 | Dom | 2026-08-10 | Instagram | Reel | `@char_USM_wilfred` | Test A/B: Tono existencial vs humorístico | Validación de hipótesis Growth OS | CNT-025 | Pendiente de Aprobación | Fernando | — |

**Regla de bloqueo:**
- El campo `Estado` acepta solo estos valores: `Idea`, `Pendiente de Producción`, `En Producción`, `Pendiente Revisión Claude`, `Pendiente Aprobación Fernando`, `Aprobado`, `Programado`, `Publicado`, `En Análisis`, `Reutilizado`, `Archivado`, `Rechazado / Requiere Reescritura`.
- Cuando el estado es `Aprobado`, el contenido pasa a la cola de programación de Manus, que prepara la orden para Graph API de Meta.
- Cuando el estado es cualquier otro valor, **el Story Scheduler y cualquier automatización de publicación están bloqueados para esa fila**.
- El campo `Bloqueado_Canon` (checkbox) bloquea forzosamente cualquier transición hacia `Programado` o `Publicado`.

---

## 3. HypothesisBank

| ID | Hipótesis | Personaje/Lugar | Variable a testear | Formato | Métrica objetivo | Estado | Fecha creación | Fecha verificación | Resultado | Observaciones |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| HB-001 | Los videos de Wilfred con tono existencial retienen más que los de tono puramente humorístico | `@char_USM_wilfred` | Tono (existencial vs humorístico) | Reel | Retención % | Pendiente de aprobación | 2026-07-31 | — | — | Test A/B con 2 variantes. Pieza asociada: CNT-025. |
| HB-002 | El contenido de tarot de Universe mantiene alta viralidad en formato Reel (transición Facebook → Instagram) | `@char_USM_universe` | Formato (Foto vs Reel) | Reel | Vistas / Interacciones | Pendiente | 2026-07-31 | — | — | Pieza asociada: CNT-001. |
| HB-003 | La distribución de horarios ampliada —mañana, tarde y noche— mejora la interacción típica frente a la programación concentrada en pocas franjas, controlando por tipo de contenido y personaje | Facebook Page | Hora local y día de publicación | Foto/meme | Mediana de interacciones por publicación; shares/interacciones como señal secundaria | En prueba | 2026-08-14 | — | Señal preliminar: mediana 37 en 17 publicaciones del 10–14 ago frente a 26 en 33 publicaciones del 4–9 ago; no es concluyente por confusión de contenido, día y tamaño de muestra. | Asociada al ciclo `Operations/Research/2026-08-14_Ciclo_Aprendizaje_Horarios.md`. |
| HB-004 | Una proporción elevada de memes reutilizados de mayo reduce el rendimiento mediano por fatiga o menor novedad, aunque el reuse de piezas top puede conservar valor cuando se limita | Facebook Page | Nueva vs Reuse_Top vs Reuse_NoTop | Foto/meme | Mediana de interacciones por publicación; shares/interacciones | En prueba | 2026-08-14 | — | En el calendario del 4–9 agosto se observan al menos 14 reuse sobre aproximadamente 32 publicaciones; varios días concentran tres reuse de cuatro slots principales. | Asociada al comparativo junio–julio–agosto. |
| HB-005 | Mantener una frecuencia suficiente de publicaciones de calidad aumenta la superficie de descubrimiento y el rendimiento total diario entre seguidores y no seguidores | Facebook Page | Publicaciones por día | Foto/meme | Interacciones totales por día y mediana por publicación | En prueba | 2026-08-14 | — | En los primeros 14 días, la frecuencia pasó de 9.50 posts/día en junio a 6.71 en julio y 4.57 en agosto; agosto cae frente a julio en total diario y mediana, pero sigue sobre junio por publicación. | Asociada al comparativo junio–julio–agosto. |

---

## 4. ExperimentLog

| ID Exp | Hipótesis ID | Contenido publicado | Personaje/Lugar | Formato | Fecha publicación | Plataforma | Vistas | Retención % | Interacciones | Estado Canon | Veredicto | Conclusión | Observaciones |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| *(vacío)* | — | — | — | — | — | — | — | — | — | — | — | — | — |

---

## 5. Arquitectura del Sistema Escalable

> **Referencia completa:** Ver `GrowthOS/01_00_Arquitectura_Calendario_Escalable.md` para la definición completa de metadatos, estados y reglas de negocio.

El sistema se compone de:

1. **Fuente editorial central** (inventario estructurado, CSV o calendario Markdown): contiene las piezas y sus metadatos operativos.
2. **5 colas operativas** (vistas filtradas de la fuente): `Backlog`, `Reuse Queue`, `Production Queue`, `Approval Queue`, `Calendario Semanal`.
3. **Flujo directo Manus + Graph API:** Manus valida estado, canon, asset, copy, plataforma y fecha; después crea la orden de publicación en Facebook o Instagram y registra el resultado.
4. **Máquina de estados** (11 estados, 11 transiciones válidas): controla el flujo de cada pieza desde la idea hasta el archivo.
5. **Registro post-publicación:** Manus consulta métricas disponibles y actualiza el `HypothesisBank` y el `ExperimentLog`.

---

## 6. Historial de Sincronización

| Fecha | Acción | Fuente (commit) | Autor |
| :--- | :--- | :--- | :--- |
| 2026-07-31 | Creación del documento puente (v1.0) | Repo `iomarketing09-sys/universe-sent-me-1` (commit `cf2ac53`) | Manus |
| 2026-07-31 | Implementación de arquitectura escalable (v2.0) | Repo `iomarketing09-sys/universe-sent-me-1` (commit `939752c`) | Manus |
| — | *(próxima actualización)* | *(pendiente)* | — |

---

## 7. Reglas Operativas de Este Documento

1. Este documento NO vive en el repo de GitHub. Vive en Google Drive, carpeta del Growth OS.
2. El repo de GitHub (`iomarketing09-sys/universe-sent-me-1`) es la **única fuente de verdad** del canon. Este documento es un caché consultivo.
3. Cada regla aquí debe llevar fecha de sincronización y commit de referencia.
4. El campo `Estado` en el Calendario Editorial es un **bloqueo operativo**, no una etiqueta. Manus no puede publicarlo si no dice literalmente "Aprobado".
5. El cambio de estado a "Aprobado" solo lo puede hacer Fernando o Claude. Nunca Manus, nunca una regla automática.
6. Antes de cada sesión de trabajo, Manus debe verificar si el commit de referencia sigue siendo el HEAD del repo. Si no, debe marcar las reglas como desactualizadas.
7. **Nueva (v2.0):** La arquitectura completa del calendario vive en `GrowthOS/` del repositorio. Este documento mantiene la vista condensada del Calendario Editorial y el HypothesisBank.
