# Sistema de Dos Capas: Contenido Libre vs. Canon Deliberado

**Propósito:** Formalizar la separación entre la capa de memes/reels (exploración libre, orientada a algoritmo y audiencia amplia) y la capa de canon (Biblia, decisiones deliberadas y permanentes sobre personajes). Define qué tan libre es cada capa, cómo un patrón de la capa 1 puede promoverse a la capa 2, y qué límites duros aplican incluso en la capa libre.
**Estado:** Aprobado
**Fecha de creación:** 2026-08-10
**Última actualización:** 2026-08-10
**Versión:** 1.3
**Autor:** Claude, formalizando dirección estratégica de Fernando
**Documentos relacionados:** `03_00_Sistema_Generacion_Memes.md` (pipeline técnico de producción), `Canon_Contradictions_Report.md` (histórico de fricciones que motivaron este sistema), `Operations/Memories/mayo_2026_top_posts_metaBS.md` (evidencia original que originó esta discusión)

---

## 1. Por qué existe este documento

Entre marzo y mayo de 2026, Fernando encontró el tono y estilo visual del proyecto por prueba y error en Facebook — antes de que existiera ningún documento de canon. Las visualizaciones se dispararon a millones/mes con contenido arriesgado (explícito, directo, a veces vulgar) que no se derivó de la Biblia; la Biblia se escribió después, con otro propósito (consistencia narrativa a largo plazo para historias y episodios).

Desde entonces, ambas capas han convivido sin una regla explícita que las separe, generando fricción real y documentada: el `Canon_Contradictions_Report.md` registra 5 contradicciones entre contenido producido y canon cerrado, de las cuales 3 resultaron ser errores de lectura o nombres pendientes de registrar (Silvio, Maeve, Kiri) y 2 siguen bloqueadas por ser narrativa seria (mini-historia "El Frasco Olvidado"), no memes sueltos. Esa proporción — la mayoría de "contradicciones" resueltas sin reescribir nada, solo por falta de registro formal — es la señal de que el problema no era el contenido, era la falta de esta distinción.

Fernando identificó además una segmentación de audiencia que sostiene esta separación: existen seguidores reales, pero también una órbita amplia de personas que reaccionan o comentan durante semanas sin seguir la página — quienes llegan principalmente vía algoritmo. El contenido libre (capa 1) está dirigido a capturar y sostener esa órbita amplia; el canon (capa 2) es lo que eventualmente convierte a alguien de esa órbita en seguidor real, cuando encuentra algo con lo que decide quedarse.

## 2. Las dos capas

### Capa 1 — Memes y Reels basados en memes (exploración libre)

- **Objetivo:** algoritmo, alcance, la órbita amplia de reacciones/comentarios no-seguidores.
- **Libertad:** tono, actitud, nivel de explicitud, lenguaje directo, ruptura de cuarta pared, y matices de personalidad quedan libres de seguir al pie de la letra las Reglas de Diseño ya cerradas de cada personaje. Esto aplica igual para personajes del Primer Círculo y del Segundo Círculo/elenco extendido — no hay distinción de margen por antigüedad del personaje. Los memes SON el proceso de descubrimiento, tanto para personajes nuevos como para explorar registros no vistos aún en los ya establecidos.
- **No requiere aprobación de canon.** No pasa por el flujo de bloqueo del `Canon_Contradictions_Report.md` — ese reporte es exclusivamente para narrativa seria (historias, episodios, mini-historias serializadas).

### Capa 2 — Canon (Biblia)

- **Objetivo:** consistencia narrativa a largo plazo, identidad permanente de cada personaje, base para historias/episodios/eventual expansión (merch, alianzas, etc.).
- **Se alimenta de la Capa 1 solo por promoción deliberada** (ver sección 4) — nunca automáticamente. Que un meme funcione bien no lo convierte en canon por sí solo.

## 3. Límite duro (aplica incluso en Capa 1, sin excepción)

Con margen amplio para todos los personajes, sigue habiendo una frontera que ningún meme puede cruzar, porque protege lo que hace que un personaje siga siendo reconociblemente él mismo, no lo que dice o cómo actúa en una pieza suelta:

1. **Identidad física fija.** Ejemplo: las gafas de Universe, su forma de gato. Un meme puede hacer que Universe diga o haga casi cualquier cosa; no puede quitarle las gafas ni cambiar su especie/forma base.
2. **Vínculos/relaciones inventadas que comprometan narrativa futura.** Un meme no debe establecer una relación entre dos personajes (pareja, parentesco, historia compartida específica) que luego Fernando no quiera arrastrar como hecho narrativo. Si surge una relación así y funciona, se resuelve por promoción deliberada (sección 4), no queda fija solo por haberse publicado una vez.
3. **Zonas ya protegidas de la Biblia:** la Gramática Emocional Invisible (ningún personaje nombra o diagnostica un Estado Permanente o una máscara, ni dentro de la ficción ni en el copy de un meme) sigue aplicando siempre, sin excepción de capa.

Todo lo demás — tono, actitud, explicitud, humor, lenguaje, registro emocional momentáneo — es terreno libre de Capa 1.

## 4. Mecanismo de promoción: de meme a canon

**Quién decide:** Fernando, siempre. No hay promoción automática por métricas.

**Rol de Claude:** alertar activamente cuando un patrón cruce un umbral observable en los datos, para que Fernando tenga la información a tiempo de decidir — no decidir en su lugar.

### 4.1 Qué cuenta como "patrón" a vigilar

- El mismo personaje repite un tono, actitud, o tipo de humor específico en **3 o más piezas** dentro de un periodo de 30 días.
- Esas piezas, en conjunto, muestran rendimiento consistente por encima de la mediana del personaje o de la cuenta (no un solo pico aislado — un pico único es una pieza afortunada, no un patrón).
- El patrón no ha sido ya registrado como rasgo permanente en la ficha del personaje.

### 4.2 Qué hace Claude cuando detecta esto

Alerta explícitamente a Fernando, con formato consistente:

> 🔔 **Candidato a promoción de canon:** [personaje] — [descripción del patrón]. Apareció en [N] piezas entre [fechas], con [métrica de rendimiento]. ¿Lo revisamos para posible ficha permanente, o lo dejamos como recurso libre de Capa 1?

Claude no escribe la ficha de canon ni la propone redactada de antemano — solo señala el patrón y espera la decisión de Fernando sobre si vale la pena convertirlo en rasgo permanente.

### 4.3 Qué pasa si Fernando aprueba la promoción

1. Fernando confirma explícitamente qué del patrón se vuelve permanente (puede ser solo una parte del meme, no toda la pieza).
2. Claude redacta la actualización de canon correspondiente (nueva Regla de Diseño, o ajuste a una existente) y la somete a la misma disciplina de commits ya establecida (unidad lógica única, nunca mezclada con cambios administrativos).
3. Se hace commit + push al repo `universe-sent-me-1` con el mensaje describiendo el patrón de origen y la evidencia que lo sustenta.
4. El registro incluye una referencia a las piezas de Capa 1 que originaron la promoción, para trazabilidad.

### 4.4 Qué pasa si Fernando decide NO promoverlo

Se queda como recurso libre de Capa 1 — se puede seguir usando en memes indefinidamente sin que eso implique una obligación futura de mantenerlo. Claude no vuelve a alertar sobre el mismo patrón exacto salvo que Fernando lo pida, para no generar ruido repetido.

### 4.5 Log de promociones

| Fecha | Personaje | Patrón promovido | Evidencia | Commit canon |
|---|---|---|---|---|
| 2026-08-10 | Universe | Registro sarcástico/cortante en formato meme corto (adicional a su curiosidad/observación ya cerrada) | 3+ piezas jun-ago 2026 con rendimiento consistentemente alto ("No me importa lo que tú pienses...", "😒", entre otras) | `universe-sent-me-1@e8b6f22` |
| 2026-08-10 | Universe (ampliación) | Mismo registro sarcástico confirmado también en formato cinemático/composición elaborada, no solo minimalista | "yo Aura Fuerte" (110,510 visualizaciones, pico más alto de junio), "No todos los ex son malos...", "sexo increíblemente apasionado O comunicación saludable" | `universe-sent-me-1@b52ea42` |
| 2026-08-10 | Kael + Maeve | Creación de canon (personajes nuevos, Segundo Círculo) + relación de pareja establecida | 3+ piezas jun 2026 con fricción cotidiana resuelta en humor/ternura ("casi nos dejamos y lo que teníamos era hambre", "lo hice porque si alguien te hace bien..."), hasta 110,510 visualizaciones en una pieza relacionada de Universe del mismo lote de evidencia | `universe-sent-me-1@a994354` |

## 5. Registro cualitativo de comunidad (nueva pieza de datos, no capturada antes)

Fernando reporta que la comunidad deja en comentarios contenido valioso que ningún reporte de métricas captura: historias personales, puntos de vista profundos, agradecimiento explícito por el tono de respuesta de la página ("por esto amamos esta página"). Esto es evidencia cualitativa en vivo de la Tesis Emocional del proyecto ("las personas se sienten menos solas cuando descubren que alguien más ya vivió lo mismo") y merece un lugar de registro propio, distinto de las métricas cuantitativas (reacciones, shares, alcance).

**Propuesta de formato** (a definir con Fernando en su primer uso real): un documento tipo `Operations/Memories/comunidad_insights_[mes].md`, donde se registre — sin exponer identidad de usuarios reales salvo que Fernando decida lo contrario — el tipo de comentario, qué pieza lo generó, y si aporta señal para posible promoción a canon (ej. si varias personas reaccionan con su propia historia a un mismo patrón de humor, eso refuerza la señal cuantitativa de la sección 4).

Este registro queda como pendiente de implementación — no se generó ningún ejemplo en esta sesión porque no había datos concretos de comentarios a mano.

## 6. Lo que este sistema NO cambia

- El flujo de aprobación de historias/episodios narrativos serios (`Canon_Contradictions_Report.md`, `07 Historias/00 Estándar de Historias.md`) sigue vigente sin cambios — ese bloqueo aplica solo a narrativa seria, nunca a memes sueltos.
- Las Reglas de Diseño ya cerradas de cada personaje siguen siendo CANON y siguen rigiendo toda narrativa formal (historias, episodios, guiones de Reels con arco).
- El pipeline técnico de producción de memes (`03_00_Sistema_Generacion_Memes.md`) sigue igual — este documento no toca cómo se generan o procesan las imágenes, solo qué reglas de contenido aplican una vez producidas.

## 8. Canal externo — grupos de Facebook (distinto de Capa 1)

Fernando distribuye contenido regularmente en grupos de Facebook ajenos a la página (no le pertenecen), donde se ha ganado espacio para publicar tras un período de aprobación previa del grupo. El principal es **"Polvo de estrellas"**, con publicación regular; hay otros grupos con más restricciones donde también publica, pero con menor prioridad de tracking por ahora.

**Por qué esto NO es lo mismo que la Capa 1 (memes en la página propia):**

- El nivel de explicitud en estos grupos puede ser mayor que en la página (ejemplo confirmado: contenido con desnudos estilizados y texto directo, con buen desempeño — 4.4K likes, 143 comentarios, 1.4K shares en un post; otro llegó a 400K vistas y mil shares). Ese límite lo fija el grupo anfitrión, no Universe Sent Me — no debe leerse como "hasta dónde puede llegar la marca propia" ni usarse como evidencia directa para promoción de canon (sección 4), aunque sí es señal real de qué tan fuerte es el contenido cuando compite sin la ventaja de audiencia propia cautiva.
- Es territorio de otra página/comunidad, con sus propias reglas y cola de aprobación — no bajo control operativo de Fernando.

**Riesgo operativo identificado:** las aprobaciones de estos grupos externos no son inmediatas y a veces se acumulan; ya ocurrió que ~5 publicaciones represadas se aprobaron el mismo día, y ese aluvión de publicaciones externas coincidiendo en fecha impactó negativamente el rendimiento de la página propia ese día (competencia por atención de la misma red de contactos/algoritmo, o dilución de foco). No hay control directo sobre cuándo se libera la cola de aprobación del grupo externo.

**Tratamiento en Growth OS:** Polvo de estrellas queda como el único canal externo a trackear por ahora (los demás grupos, con más restricciones, quedan fuera de tracking por decisión de Fernando). Su rendimiento se registra por separado de las métricas de la página — nunca sumado ni promediado junto con Facebook Orgánico propio — y no alimenta directamente el mecanismo de promoción a canon de la sección 4, salvo que Fernando decida explícitamente lo contrario para un caso puntual.

## 9. Pendientes

1. Implementar el primer registro cualitativo real de comunidad cuando Fernando tenga comentarios concretos a mano (sección 5).
2. Revisar retroactivamente los memes de mayo-agosto ya publicados en busca de patrones que ya cumplan el umbral de la sección 4.1, como primera aplicación práctica del sistema (sesión dedicada, ya mencionada en conversaciones anteriores).
3. Confirmar con Fernando si el "Canon_Contradictions_Report.md" debe actualizarse con una nota que aclare explícitamente que su alcance es solo narrativa seria, para evitar que una futura sesión lo aplique por error a un meme suelto.
4. Definir si conviene registrar en el calendario editorial las fechas en que Fernando publica en Polvo de estrellas, para poder correlacionar caídas de rendimiento de la página propia con posibles aluviones de aprobación del grupo externo (sección 8) — por ahora es una observación puntual, no un patrón confirmado con datos suficientes.
