# Integración Growth OS ↔ Canon

**Documento de sincronización entre el Growth OS (Manus) y la Biblia de Canon (Claude)**

---

| Campo | Valor |
| :--- | :--- |
| **Última sincronización** | 2026-08-15T22:56:57Z |
| **Fuente de canon** | Repo GitHub administrado por Claude: `iomarketing09-sys/universe-sent-me-1`, rama `main`, HEAD `1daaad5342c278909b78076a54d8b220fa51e023`. Ficha de sincronización recibida por Claude mediante clonación directa. |
| **Estado del documento** | v2.5.1 — Resincronizado contra HEAD `1daaad5`; Maeve = Chica del Suéter y Kael = Chico de los Pantalones; Silvio/Kiri y cambios de Universe actualizados; La Hoguera y La Ciudad marcadas como propuestas; conflictos de Growth OS separados del canon |
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
| Universe | `@char_USM_universe` | La profundidad nunca debe aparecer antes que el humor. Conoce el mecanismo pero nunca entiende completamente el propósito ni tiene acceso total. No es orquestador del conflicto. Canon actualiza el color de pelaje a blanco/crema y añade un registro sarcástico/cortante permitido en memes y composiciones cinematográficas, siempre limitado por Anti-tono: se ríe con, no de, y no muestra desprecio hacia otro personaje o el público. | `02 Personajes/Primer Círculo/Universe/03 Reglas de diseño.md` | 2026-08-12 (commits `94aa9e8`, `e8b6f22`, `b52ea42`; HEAD `1daaad5`) |
| Wilfred | `@char_USM_wilfred` | Guardián del bosque con barba blanca larga, gorro rojo, personalidad enfocada en sabiduría y humor seco. No moraliza explícitamente ni diagnostica a otros personajes. | `02 Personajes/Primer Círculo/Wilfred/03 Reglas de diseño.md` | 2026-07-31 (commit `939752c`) |
| Elara | `@char_USM_elara` | Lectora de cartas mágicas conectada con astrología y naturaleza. Rol diferenciado de Universe (no es tarotista principal — ese es Universe). | `02 Personajes/Primer Círculo/Elara/03 Reglas de diseño.md` | 2026-07-31 (commit `939752c`) |
| Ganso | `@char_USM_ganso` | *(Pendiente: consultar ficha canónica para regla de diseño activa)* | `02 Personajes/Primer Círculo/Ganso/03 Reglas de diseño.md` | 2026-07-31 (commit `939752c`) |
| Payaso / Silvio | `@char_USM_payaso` | Silvio es el nombre propio confirmado de El Payaso. El diseño corregido y su expresión aprobada quedaron registrados en canon; `#SilvioUSM` está autorizado. | `02 Personajes/Primer Círculo/Payaso/03 Reglas de diseño.md`, `GrowthOS/Canon_Contradictions_Report.md` | 2026-08-03 (canon commit `8e9fe9a`; constancia local `c9730ee6`) |

### 1.2 Personajes — Segundo Círculo

| Personaje | ID Canon | Nota | Fuente | Última sincronización |
| :--- | :--- | :--- | :--- | :--- |
| Hada (Kiri) | `@char_USM_hada` | Nombre propio confirmado: Kiri. Su territorio emocional es el asombro genuino. Su varita es un objeto personal canonizado como elemento visual/identitario; su función narrativa y relación con el lenguaje de Resonancia siguen abiertas. | `02 Personajes/Segundo Círculo/Hada/00 Resumen.md`, `01 Territorio emocional.md`, `03 Reglas de diseño.md` | 2026-08-04 (commits `f7bebca`, `990a69c`; HEAD `1daaad5`) |
| Evan | `@char_USM_evan` | La relación de Evan con Elara y Kiri puede generar lecturas de cercanía o “chisme”, pero ninguna es romántica en canon. La ambigüedad queda abierta deliberadamente y no debe resolverse automáticamente. | `02 Personajes/Segundo Círculo/Evan/02 Relaciones.md` | 2026-08-12 (commit `1daaad5`) |
| Kael | `@char_USM_kael` | Personaje canonizado del Segundo Círculo. Forma una pareja establecida con Maeve. **Alias visual/editorial: Chico de los Pantalones.** Su relación narrativa con Universe existe visualmente, pero aún no está definida. | `02 Personajes/Segundo Círculo/Kael/00 Resumen.md`, `01 Territorio emocional.md`, `02 Relaciones.md`, `03 Reglas de diseño.md` | 2026-08-11 (commit `a994354`) |
| Maeve | `@char_USM_maeve` | Personaje canonizado del Segundo Círculo. **Alias visual/editorial: Chica del Suéter.** Forma una pareja establecida con Kael. Su relación narrativa con Universe existe visualmente, pero aún no está definida. | `02 Personajes/Segundo Círculo/Maeve/00 Resumen.md`, `01 Territorio emocional.md`, `02 Relaciones.md`, `03 Reglas de diseño.md` | 2026-08-11 (commit `a994354`) |
| Fantasma | `@char_USM_fantasma` | Congelado emocionalmente en un instante que nunca cerró — no es incapacidad física. Puede actuar, pero no puede resolver esa identidad ni "salvar el día" de forma heroica y dramáticamente visible dentro de una misma pieza. La regla no cambió en el delta actual. | `02 Personajes/Segundo Círculo/Fantasma/01 Territorio emocional.md`, `03 Reglas de diseño.md` | 2026-08-02 (sin cambios desde antes de `939752c`; confirmado en HEAD `1daaad5`) |

### 1.3 Lugares

| Lugar | ID Canon | Nota | Fuente | Última sincronización |
| :--- | :--- | :--- | :--- | :--- |
| El Bosque | `@loc_USM_bosque` | Bosque Ancestral — territorio de Wilfred | `06 Lugares/El Bosque.md` | 2026-07-31 (commit `939752c`) |
| Jardines Eternos | `@loc_USM_jardines` | *(Pendiente: consultar ficha)* | `06 Lugares/Jardines Eternos.md` | 2026-07-31 (commit `939752c`) |
| La Plaza del Mercado | `@loc_USM_plaza` | *(Pendiente: consultar ficha)* | `06 Lugares/La Plaza del Mercado.md` | 2026-07-31 (commit `939752c`) |
| Mar de Nubes | `@loc_USM_mar_nubes` | *(Pendiente: consultar ficha)* | `06 Lugares/Mar de Nubes.md` | 2026-07-31 (commit `939752c`) |
| La Hoguera | `(ID pendiente; no asignar)` | Propuesta de lugar; no es canon y no debe tratarse como cerrado. | `06 Lugares/La Hoguera.md` | 2026-08-04 (commit `9dcf9d4`) |
| La Ciudad | `(ID pendiente; no asignar)` | Propuesta parcial con dirección visual; no es canon y no debe tratarse como cerrado. | `06 Lugares/La Ciudad.md` | 2026-08-04 (commit `9dcf9d4`) |

### 1.4 Reglas de Diseño de Historias

| Regla | Descripción | Fuente | Última sincronización |
| :--- | :--- | :--- | :--- |
| Profundidad después del humor | La profundidad nunca debe aparecer antes que el humor. | `01 ADN/01.04 Anti-tono.md` | 2026-07-31 (commit `939752c`) |
| Sin moralización explícita | Una historia no puede existir para ilustrar una lección. Ningún personaje puede diagnosticar a otro. La lección debe sentirse sin nombrarse. | `07 Historias/00 Estándar de Historias.md` | 2026-07-31 (commit `939752c`) |
| Fantasma congelado emocionalmente | El Fantasma no puede resolver ni superar de forma dramática y visible su identidad congelada dentro de una misma pieza. No tiene restricción de movilidad física ni de acción. *(Corregido 2026-08-02 por Claude — "Fantasma inmovilizado" describía incapacidad física, que no existe en canon.)* | `02 Personajes/Segundo Círculo/Fantasma/01 Territorio emocional.md`, `03 Reglas de diseño.md` | 2026-08-02 (corrección) |
| Universe limitado | Universe conoce el mecanismo pero nunca entiende completamente el propósito. No es orquestador de conflictos. | `02 Personajes/Primer Círculo/Universe/03 Reglas de diseño.md` | 2026-07-31 (commit `939752c`) |

### 1.5 Delta canónico posterior a 939752c

La siguiente tabla resume únicamente los cambios confirmados por la ficha de sincronización de Claude hasta el HEAD `1daaad5`. Las propuestas permanecen separadas del canon.

| Commit | Elemento | Estado y efecto vigente |
|---|---|---|
| `8e9fe9a` | Payaso / Silvio | `CANON v1.1`, cerrado. Silvio es el nombre propio; el diseño aprobado usa sonrisa ladeada cómplice y ceja levantada, no el payaso triste. |
| `f7bebca`, `990a69c` | Hada / Kiri | `CANON v1.2`, cerrado. Kiri y su varita están confirmados como identidad visual; la función narrativa de la varita sigue abierta. |
| `94aa9e8`, `e8b6f22`, `b52ea42` | Universe | Pelaje blanco/crema y registro sarcástico/cortante canonizados. El registro aplica a memes y composiciones cinematográficas, siempre limitado por Anti-tono. |
| `9dcf9d4` | La Hoguera y La Ciudad | `Propuesta`; no son lugares canonizados y no deben tratarse como estados cerrados. No se asignan IDs canon en este bridge. |
| `a994354` | Kael y Maeve | `CANON v1.0` cada uno; pareja establecida. La relación narrativa con Universe sigue abierta. |
| `1daaad5` | Evan, Kiri y Elara | La cercanía que genera lecturas de “chisme” queda abierta y no es romance canon. No debe resolverse automáticamente. |
| `aa948c5` | Excepción de Anti-tono en Reels | `PENDIENTE`, no canon. No modifica reglas activas ni IDs. |

### 1.6 Contenido de Growth OS evaluado contra reglas canónicas

`La Búsqueda del Frasco Olvidado` no es un documento del repositorio canónico; vive en el espacio de producción del Growth OS y debe evaluarse contra reglas que sí están cerradas en la Biblia.

| Elemento | Estado vigente | Acción requerida |
|---|---|---|
| Capítulo 10 — Universe omnisciente | Contradicción activa | Reescribir: Universe no puede revelar que conocía todo el plan ni actuar como orquestador omnisciente. |
| Capítulo 8 — moralización de Wilfred | Contradicción activa | Reescribir diálogo y CTA para que la lección se sienta, no se nombre ni se diagnostique. |
| Elara como tarotista | Conflicto de diferenciación activo | Reasignar el ángulo hacia astrología y naturaleza; no duplicar el rol tarotista de Universe. |
| Capítulo 7 — Fantasma | Relectura requerida | Revisar el texto directo para determinar si “salvar el día” resuelve visiblemente su identidad congelada. La regla canónica no cambió. |
| Silvio / Contradicción #5 | Resuelto | No es un bloqueo vigente; tratar Silvio como canon cerrado. |

Estos conflictos no representan cambios del canon remoto. `CNT-004` permanece `Blocked_Operational` en el inventario del Growth OS hasta que la historia sea corregida y aprobada por Fernando o Claude.

---

## 2. Calendario Editorial (Roadmap)

> **Bloqueo operativo:** Ningún contenido puede publicarse automáticamente mientras `Estado` ≠ "Aprobado".
> El cambio a "Aprobado" solo puede ser realizado por Fernando o Claude.
> Manus no puede ejecutar una publicación con estado ≠ "Aprobado" ni con `Bloqueado_Canon == Sí`.

> **v2.1:** La arquitectura del calendario sigue documentada en `GrowthOS/01_00_Arquitectura_Calendario_Escalable.md`; la operación vigente vive en `GrowthOS/01_01_Calendario_Semanal.md`, y Manus valida cada orden y utiliza la API de Graph de Meta para programar o publicar. Las guías de automatización heredadas se conservan únicamente como archivo histórico.

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
| `EXP-2026-08-BASELINE-01` | HB-005 | Cohortes junio 1–14, julio 1–14 y agosto 1–14 | Facebook | Foto/meme | 2026-06-01 a 2026-08-14 | Cerrada | — | — | Veredicto consolidado: julio es la referencia principal; agosto cae frente a julio, pero supera a junio por pieza. |
| `EXP-2026-08-BASELINE-02` | HB-003 | Cohortes 4–9 y 10–14 de agosto | Facebook | Foto/meme | 2026-08-04 a 2026-08-14 | Cerrada / señal preliminar | — | — | La mediana 37 frente a 26 es compatible con la ampliación horaria, pero no es causal por confusión de contenido y día. |
| `EXP-2026-08-BASELINE-03` | HB-004 | Mix de reuse del 4–9 de agosto | Facebook | Foto/meme | 2026-08-04 a 2026-08-09 | Inconclusa | — | — | Se observaron al menos 14 reuse sobre aproximadamente 32 publicaciones; queda en prueba con Reuse_Top frente a Nueva. |
| `EXP-2026-08-CAL-01` | HB-003 / HB-004 / HB-005 | Lote Facebook 15–16 de agosto | Facebook | Imagen estática | 2026-08-15 a 2026-08-16 | Pendiente_24h | — | — | 9 publicaciones programadas; métricas e hipótesis se completan a 24/72 horas. |

---

## 5. Arquitectura del Sistema Escalable

> **Referencia completa:** Ver `GrowthOS/01_00_Arquitectura_Calendario_Escalable.md` para la definición completa de metadatos, estados y reglas de negocio.

El sistema se compone de:

1. **Fuente maestra de contenido:** `GrowthOS/Content_Inventory.csv` identifica una vez cada pieza creativa (`CNT-####`) y sus metadatos.
2. **Ledgers append-only:** `Operations/Research/2026-08-15_Publication_Log.csv` registra una fila por publicación/plataforma y `Operations/Research/2026-08-15_ExperimentLog.csv` registra una fila por observación de hipótesis.
3. **Colas y calendarios:** `Backlog`, `Reuse Queue`, `Production Queue`, `Approval Queue` y `Calendario Semanal` son vistas filtradas, no fuentes paralelas.
4. **Flujo directo Manus + Graph API:** Manus valida estado, canon, asset, copy, plataforma y fecha; después crea la orden de publicación y registra el resultado.
5. **Máquina de estados:** controla el flujo de cada pieza desde la idea hasta el archivo.
6. **Registro post-publicación:** Manus consulta solo métricas nuevas, actualiza el `HypothesisBank` y agrega el resultado al `ExperimentLog`.

---

## 6. Historial de Sincronización

| Fecha | Acción | Fuente (commit) | Autor |
| :--- | :--- | :--- | :--- |
| 2026-07-31 | Creación del documento puente (v1.0) | Repo `iomarketing09-sys/universe-sent-me-1` (commit `cf2ac53`) | Manus |
| 2026-07-31 | Implementación de arquitectura escalable (v2.0) | Repo `iomarketing09-sys/universe-sent-me-1` (commit `939752c`) | Manus |
| 2026-08-03 | Resolución de Silvio y diseño corregido | Canon commit `8e9fe9a`, registrado en `Canon_Contradictions_Report.md` | Fernando vía Claude |
| 2026-08-15 | Resincronización contra el HEAD canónico actual `1daaad5` | Ficha `canon_sync_fiche.md` proporcionada por Claude; consultada `2026-08-15T22:56:57Z` vía clonación directa | Manus |
| 2026-08-15 | Corrección de alias visuales de Kael y Maeve | Aclaración de Fernando: Chico de los Pantalones = Kael; Chica del Suéter = Maeve | Manus |

---

## 7. Reglas Operativas de Este Documento

1. Este documento vive y se versiona en el repositorio Growth OS. Es un puente condensado; la fuente de verdad del canon sigue siendo el repo GitHub `iomarketing09-sys/universe-sent-me-1`.
2. `GrowthOS/Content_Inventory.csv` es la fuente maestra de identidad de piezas; `Publication_Log.csv` y `ExperimentLog.csv` son ledgers append-only. Calendarios y colas no deben convertirse en fuentes paralelas.
3. Cada regla aquí debe llevar fecha de sincronización y commit de referencia.
4. El campo `Estado` en el Calendario Editorial es un **bloqueo operativo**, no una etiqueta. Manus no puede publicarlo si no dice literalmente "Aprobado".
5. El cambio de estado a "Aprobado" solo lo puede hacer Fernando o Claude. Nunca Manus, nunca una regla automática.
6. Antes de cada sesión de trabajo, Manus debe obtener de Claude una ficha o confirmación del HEAD actual del repositorio canónico. Si el HEAD cambia, este bridge debe marcarse desactualizado hasta resincronización.
7. `iomarketing09-sys/universe-sent-me-1` es administrado por Claude. Manus no modifica ese repositorio ni convierte contenido de Growth OS en canon; cualquier cambio de nombre, diseño, regla narrativa o aprobación debe aclararse con Claude y, cuando corresponda, Fernando.
8. La ficha recibida el 2026-08-15 confirma que `1daaad5342c278909b78076a54d8b220fa51e023` es el HEAD de `main`. Esta referencia es la autoridad de esta versión del bridge; si no existe una ficha nueva, no se deben inferir cambios posteriores.
9. **Nueva (v2.0):** La arquitectura completa del calendario vive en `GrowthOS/` del repositorio. Este documento mantiene la vista condensada del Calendario Editorial y el HypothesisBank.
10. **Nueva (v2.3):** Para ahorrar consultas y tokens, solo se consultan deltas de publicaciones y comentarios desde la última sincronización; no se vuelve a descargar toda la historia en cada sesión.
