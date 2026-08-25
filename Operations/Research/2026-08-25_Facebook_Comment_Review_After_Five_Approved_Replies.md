---
title: "Facebook Comment Review After Five Approved Replies"
purpose: "Revisión, clasificación y registro de comentarios nuevos de Facebook posterior a las cinco últimas respuestas aprobadas."
status: Review
created: 2026-08-25
updated: 2026-08-25
version: "1.0"
author: "Manus AI"
related_documents:
  - Operations/Research/2026-08-25_Facebook_Comment_Review_After_Five_Approved_Replies.json
  - Operations/Research/2026-08-25_Facebook_Editorial_Review_After_Five_Approved_Replies.json
  - Operations/Research/2026-08-25_Facebook_Pending_Queue_After_Five_Approved_Replies.json
  - Operations/Research/2026-08-15_Community_Engagement_Log.csv
  - Operations/Research/2026-08-15_Community_Engagement_Log.md
  - Operations/Research/2026-08-15_Auditoria_Comentarios_Facebook.md
  - GrowthOS/00_01_Changelog_GrowthOS.md
organization: Operations/Research
---

# Revisión de comentarios de Facebook posterior a cinco respuestas aprobadas

La revisión de solo lectura se ejecutó con **Meta Graph API v26.0** a las `2026-08-25T00:53:35+00:00`. El cursor fue `2026-08-24T21:11:20+00:00`, correspondiente al cierre verificado de las cinco respuestas anteriores. Se revisaron 20 publicaciones propias, 234 comentarios raíz y 457 IDs de comentarios y réplicas, con 0 errores de API. En el alcance completo había 347 unidades sin respuesta directa; 101 eran nuevas y no estaban registradas.

## Resultado ejecutivo

| Resultado | Casos | Estado |
|---|---:|---|
| Unidades actuales sin respuesta directa en el alcance | 347 | Incluye backlog histórico |
| Comentarios nuevos sin respuesta directa | 101 | Registrados todos en el ledger |
| Propuestas específicas | 2 | `Pendiente_Fernando`; no publicadas |
| No requiere respuesta | 99 | `No_Requiere_Respuesta` |
| Publicaciones realizadas | 0 | No hubo autorización nueva |
| Errores de Meta API | 0 | Sin errores |

El corte no publicó respuestas. Las dos propuestas son referencias musicales identificables por título y artista; cualquier escritura futura requiere autorización nueva y específica de Fernando.

## Distribución del corte

| Publicación / referencia | Hallazgos | Tratamiento editorial |
|---|---:|---|
| Reel de Maeve — caption visible: `😳🛏️🔥 #MaeveUSM #MemesUSM #UniverseSentMe` | 81 | Predominan réplicas usuario-a-usuario y lenguaje sensible. |
| Meme de la frase confirmada `larga vida a esas mujeres que aprietan desde adentro`; caption visible: `😏🙈😂 #UniverseUSM #MemesUSM #UniverseSentMe` | 18 | Se conserva como señal contextual, breve o vacía. |
| Publicación de contexto breve — caption visible: `😌 #UniverseSentMe` | 2 | Se priorizaron dos referencias musicales identificables. |

## Propuestas pendientes de autorización

| Comentario | Referencia de la publicación | Respuesta propuesta | Por qué sí merece revisión |
|---|---|---|---|
| `122151376011072582_1051573194149891` — Contigo-karol g | Publicación de contexto breve — caption visible: `😌 #UniverseSentMe` | **«CONTIGO» de Karol G: el corazón sí sabe elegir soundtrack. 💗🎶** | Es una recomendación musical identificable por título y artista; la respuesta reconoce la canción y la conecta con el tono emocional de la publicación sin inventar una interpretación de la letra. |
| `122151376011072582_1458569976337294` — aventurera, Alberto plaza | Publicación de contexto breve — caption visible: `😌 #UniverseSentMe` | **«Aventurera» de Alberto Plaza: esa sí trae nostalgia con pasaporte propio. 🎶🌙** | Es una referencia musical identificable por título y artista; la propuesta responde a esa elección concreta y mantiene un remate USM breve, sin fingir que el comentario pidió análisis musical. |

## Casos cerrados sin acción

| Categoría | Casos | Criterio aplicado |
|---|---:|---|
| `Conversación_Usuario_Usuario` | 71 | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| `Baja_señal` | 14 | Aprobación, risa, saludo, agradecimiento o reacción breve sin una pregunta dirigida a Universe Sent Me. |
| `Conversación_Contextual` | 11 | Comentario contextual, anecdótico o crítico sin una solicitud inequívoca a Universe Sent Me; se conserva sin asumir intención. |
| `Lenguaje_Sensible` | 3 | Lenguaje sexual explícito o descripción íntima; no escalar ni competir desde la Página. |

La clasificación conserva los 101 IDs: las 71 réplicas se dejan en sus conversaciones laterales; los comentarios raíz se separan entre señales breves, contexto crítico o anecdótico y lenguaje sensible. No se respondió a recomendaciones de ejercicios ni se amplificaron descripciones íntimas desde la Página.

## Inventario completo de los 101 hallazgos

Todos los IDs recuperados en este corte están incluidos en el JSON editorial y en el ledger. La tabla siguiente permite auditar que ningún comentario quedó fuera.

| # | Comentario_ID | Tipo | Comentario | Decisión | Motivo resumido |
|---:|---|---|---|---|---|
| 1 | `122151376539072582_3629247200566034` | Replica_Anidada | M Rosario Hernández golosa | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 2 | `122151376539072582_1537246257644018` | Replica_Anidada | M Rosario Hernández jaa porque | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 3 | `122151376539072582_824930140646184` | Replica_Anidada | M Rosario Hernández y pork las manis | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 4 | `122151376539072582_1966682000687395` | Replica_Anidada | Natalia Gonzales obio dale sin miedo al exito,con todo pero tiene que ser en seco asy te va quedar comprobado cientificamente era tabla mi flaca y ahora mira como le a quedado de tanto que la he clavado. | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 5 | `122151376539072582_1334862625385714` | Replica_Anidada | A hay no gracias a Dios no me da eso de experimentar me imagino xq veo muchos comentarios,si muchos comentarios dicen q no es cierto es xq ya lo experimentaron y no vieron resultado ,y me imagino q lo único q les creció fue su * q más le pudo pasar ,pero todo por ver si deveras les crecen  las nalgas 🤣 pero en fin es umor y nada más | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 6 | `122151376539072582_1553957545664516` | Replica_Anidada | Soldado Gladiador jajajaja gracias a Dios no me gusta experimentar bobadas eso déjenlos para las q no tienen por donde 🤣 | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 7 | `122151376539072582_3225331231191062` | Replica_Anidada | Santiago D. Antonio lo que pasa es que hablaste como quien tiene experiencia 😃😃😛 | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 8 | `122151376539072582_1032393119612543` | Replica_Anidada | Santiago D. Antonio así anda | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 9 | `122151376539072582_3839496296192302` | Replica_Anidada | Santiago D. Antonio dame información. | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 10 | `122151376539072582_1389147076504884` | Replica_Anidada | Wendy Mendoza ay que probar | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 11 | `122151376539072582_940812491673231` | Replica_Anidada | Katlesy KuroNeko jajajaja hable por su experiencia jajaja | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 12 | `122151376539072582_27871947775764973` | Replica_Anidada | Katlesy KuroNeko y tu todabia no lo has hecho verdad | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 13 | `122151376539072582_2623172361447996` | Replica_Anidada | Lucrecia Montero tidabia lo lo sabes hacer verdad | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 14 | `122151376539072582_4294326110710970` | Replica_Anidada | Mayra Gdlp Valdespino que rico jue | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 15 | `122151376539072582_3280409785475854` | Replica_Anidada | Mayra Gdlp Valdespino jaa serio solo se ancho jj | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 16 | `122151376539072582_1098433855944969` | Replica_Anidada | Mayra Gdlp Valdespino ufff ..de todas maneras ganó algo | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 17 | `122151376539072582_1709419876983392` | Replica_Anidada | Mayra Gdlp Valdespino entonses si te cresieron verdad | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 18 | `122151376539072582_2159755157902785` | Replica_Anidada | Mayra Gdlp Valdespino ya me lo imaginaba Mayra Golosa 😏 | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 19 | `122151376539072582_3045290109135712` | Comentario_Raiz | Eso es pura mentira 😒😒🙄🙄 | `No_Requiere_Respuesta` | Aprobación, risa, saludo, agradecimiento o reacción breve sin una pregunta dirigida a Universe Sent Me. |
| 20 | `122151376539072582_1780817046966783` | Replica_Anidada | Marie Del Rio jaa será verdad jj | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 21 | `122151376539072582_1082436364148129` | Replica_Anidada | Marie Del Rio hola buenas noches | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 22 | `122151376539072582_1486031383350775` | Replica_Anidada | Juan Carlos Villagran buenas  noches | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 23 | `122151376539072582_2897324553945901` | Replica_Anidada | Marie Del Rio ya lo comptobastes verdad | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 24 | `122151376539072582_824700140669032` | Replica_Anidada | Laura Mar poreso lo tienes asi vefdad | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 25 | `122151376539072582_2152346335328118` | Replica_Anidada | Laura Mar si te ríes es porque ya la tienes toda rota amor Laura golosa | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 26 | `122151376539072582_2694738410943723` | Replica_Anidada | Monssesita Gomez agamos una prueba | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 27 | `122151376539072582_1970601450305452` | Replica_Anidada | Monssesita Gomez todabia no lo has hecho berdad | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 28 | `122151376539072582_2163046420910250` | Replica_Anidada | Luciia Huerta ya la dotaron | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 29 | `122151376539072582_1079445597916794` | Replica_Anidada | Luciia Huerta pues tú di cuando jejeje | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 30 | `122151376539072582_1493216886158293` | Replica_Anidada | Luciia Huerta ah | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 31 | `122151376539072582_1574150137526634` | Comentario_Raiz | Como les digo que si me paso 😢 y no me crecieron | `No_Requiere_Respuesta` | Comentario contextual, anecdótico o crítico sin una solicitud inequívoca a Universe Sent Me; se conserva sin asumir intención. |
| 32 | `122151376539072582_1431222802336376` | Replica_Anidada | Oliva Sánchez Feliciano como haci | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 33 | `122151376539072582_1274111231418126` | Replica_Anidada | Wendy Mendoza si no mas me dejaron uango el fundillo 😢 | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 34 | `122151376539072582_2358958818180416` | Comentario_Raiz | No gracias, ni aunque fuera cierto 🤣🤣 | `No_Requiere_Respuesta` | Aprobación, risa, saludo, agradecimiento o reacción breve sin una pregunta dirigida a Universe Sent Me. |
| 35 | `122151376539072582_1034005309470855` | Replica_Anidada | Angie Lyca tienes niedo verdax0 | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 36 | `122151376539072582_1383444600561933` | Replica_Anidada | Angie Lyca por qué | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 37 | `122151376539072582_1528829842259793` | Replica_Anidada | Angie Lyca si no lo habrás hecho hace rato!!!! Ajajaja golosa 😏 | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 38 | `122151376539072582_1587385739729103` | Comentario_Raiz | Si es verdad jaja | `No_Requiere_Respuesta` | Aprobación, risa, saludo, agradecimiento o reacción breve sin una pregunta dirigida a Universe Sent Me. |
| 39 | `122151376539072582_1065061669237716` | Replica_Anidada | Andriss García por qué lo dices | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 40 | `122151376539072582_1403189315091140` | Replica_Anidada | Wendy Mendoza por qie es verdad lo digo por mi..o sera mucha casualidad 😁 | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 41 | `122151376539072582_28536076102644174` | Replica_Anidada | Genesis Gutierrez hay que darle y así se salee de la duda o no | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 42 | `122151376539072582_1390798406567884` | Comentario_Raiz | alguna chica para ponerlo a prueba? | `No_Requiere_Respuesta` | Comentario contextual, anecdótico o crítico sin una solicitud inequívoca a Universe Sent Me; se conserva sin asumir intención. |
| 43 | `122151376539072582_1583143096535298` | Replica_Anidada | Nando Gonzalez no chingues pero para q quieres estar nalgon? | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 44 | `122151376539072582_1097548376119716` | Replica_Anidada | Adrian Sanchez jaja este we, | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 45 | `122151376539072582_1547014010789302` | Comentario_Raiz | Mentira. Jajajaja | `No_Requiere_Respuesta` | Aprobación, risa, saludo, agradecimiento o reacción breve sin una pregunta dirigida a Universe Sent Me. |
| 46 | `122151376539072582_1065809375935598` | Replica_Anidada | Ara Ballesteros quieres probar. | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 47 | `122151376539072582_2919560055075646` | Replica_Anidada | Ara Ballesteros lo ha intentado jj | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 48 | `122151376539072582_1418414816881513` | Replica_Anidada | Ara Ballesteros no lo has pribado verdad | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 49 | `122151376539072582_2104303970195451` | Replica_Anidada | Ara Ballesteros y tu como sabes | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 50 | `122151376539072582_1113893144548882` | Replica_Anidada | Ara Ballesteros ya lo probaste Ara??? Ajajajaja seguro que te quedo bien grande golosa | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 51 | `122151376539072582_1082529927556024` | Comentario_Raiz | Jajsjs | `No_Requiere_Respuesta` | Aprobación, risa, saludo, agradecimiento o reacción breve sin una pregunta dirigida a Universe Sent Me. |
| 52 | `122151376539072582_4577137382516535` | Replica_Anidada | Christian AC 🤣🤣 | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 53 | `122151376539072582_2099062040644066` | Comentario_Raiz | Todo sea por que crezcan más ☺️ | `No_Requiere_Respuesta` | Comentario contextual, anecdótico o crítico sin una solicitud inequívoca a Universe Sent Me; se conserva sin asumir intención. |
| 54 | `122151376539072582_904837582265695` | Comentario_Raiz | Obvio mor | `No_Requiere_Respuesta` | Aprobación, risa, saludo, agradecimiento o reacción breve sin una pregunta dirigida a Universe Sent Me. |
| 55 | `122151376539072582_2059530071591826` | Comentario_Raiz | Quiero intentarlo | `No_Requiere_Respuesta` | Comentario contextual, anecdótico o crítico sin una solicitud inequívoca a Universe Sent Me; se conserva sin asumir intención. |
| 56 | `122151376539072582_2124930988235183` | Replica_Anidada | Nicole Hernandez entonces voy para allá | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 57 | `122151376539072582_1554699623104008` | Replica_Anidada | Nicole Hernandez apoco | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 58 | `122151376539072582_3320882861426050` | Replica_Anidada | Linda Gomez si | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 59 | `122151376539072582_1143049124914395` | Comentario_Raiz | Pues yo digo que no es mito jeje | `No_Requiere_Respuesta` | Aprobación, risa, saludo, agradecimiento o reacción breve sin una pregunta dirigida a Universe Sent Me. |
| 60 | `122151376539072582_1634277098061381` | Replica_Anidada | Karen Alexa Rocha ya lo comprobastes verdad | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 61 | `122151376539072582_1721543212409091` | Replica_Anidada | Karen Alexa Rocha por qué | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 62 | `122151376539072582_28192243330425101` | Comentario_Raiz | Ah por eso es q yo soy nalgoncito 🥰🥰🥰🥰 | `No_Requiere_Respuesta` | Lenguaje sexual explícito o descripción íntima; no escalar ni competir desde la Página. |
| 63 | `122151376539072582_3971796692950837` | Replica_Anidada | Nayla Echeverria kieres tu estar asi verdad | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 64 | `122151376539072582_1018755814475045` | Comentario_Raiz | Noelia Pintos 🥴 | `No_Requiere_Respuesta` | Comentario contextual, anecdótico o crítico sin una solicitud inequívoca a Universe Sent Me; se conserva sin asumir intención. |
| 65 | `122151376539072582_1728556638228827` | Comentario_Raiz |  | `No_Requiere_Respuesta` | Comentario sin texto recuperable; se conserva para cobertura, sin intervención. |
| 66 | `122151376539072582_28538943389023684` | Replica_Anidada | Ximena Daniela Mora Marín que pasa | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 67 | `122151376539072582_1427770872554676` | Comentario_Raiz | Seraa?? 🤔😊 | `No_Requiere_Respuesta` | Aprobación, risa, saludo, agradecimiento o reacción breve sin una pregunta dirigida a Universe Sent Me. |
| 68 | `122151376539072582_2789908908077536` | Replica_Anidada | Mayra Gmorales agamos la prueba | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 69 | `122151376539072582_1074008315325944` | Replica_Anidada | Mayra Gmorales tidabia no lo has hecho verdad | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 70 | `122151376539072582_1751686982620959` | Replica_Anidada | Mayra Gmorales mmm | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 71 | `122151376539072582_2226067587953853` | Comentario_Raiz | La mentira más grande q pueden decir | `No_Requiere_Respuesta` | Aprobación, risa, saludo, agradecimiento o reacción breve sin una pregunta dirigida a Universe Sent Me. |
| 72 | `122151376539072582_1051642164527056` | Replica_Anidada | Flor Hernandez que ya lo intentó | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 73 | `122151376539072582_1607597654228222` | Replica_Anidada | Lopez Carlos x q cree q lo digo | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 74 | `122151376539072582_2336082013798235` | Replica_Anidada | Flor Hernandez ahhhh rico sintio | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 75 | `122151376539072582_1341732431279786` | Replica_Anidada | Flor Hernandez por qué lo dices | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 76 | `122151376539072582_1606221877827907` | Replica_Anidada | Flor Hernandez es encerio | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 77 | `122151376539072582_1561923678131227` | Replica_Anidada | Wendy Mendoza lo digo x q es mentira no t crece nada | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 78 | `122151376539072582_2708921846192992` | Replica_Anidada | Flor Hernandez Ay te pasas 🤣 te mandé solicitud | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 79 | `122151376539072582_2046151186046008` | Replica_Anidada | Wendy Mendoza De lo único q t puedo dar seguridad es q duele pero se aguanta 🤭😄 | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 80 | `122151376539072582_1968159011234296` | Comentario_Raiz | Es falzo cada semana quemaba 3 y nada asta yo me quede sin nalgas y ella tambien esa cosa me acabo y asta salia con dolor de espelda asta ahora | `No_Requiere_Respuesta` | Lenguaje sexual explícito o descripción íntima; no escalar ni competir desde la Página. |
| 81 | `122151376539072582_2286320748808243` | Comentario_Raiz | Ami exnovia le crecio las nalgas le funcionos | `No_Requiere_Respuesta` | Lenguaje sexual explícito o descripción íntima; no escalar ni competir desde la Página. |
| 82 | `122151376083072582_2320204928811719` | Replica_Anidada | Olivia Gonzalez así son los malagradecidos les gusta lo corriente jajaja no saben valorar lo q es bueno | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 83 | `122151376083072582_2290365748433045` | Replica_Anidada | Olivia Gonzalez enserio | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 84 | `122151376083072582_2639588369818287` | Replica_Anidada | Eriickaa Ross que rico se siente cuando se orinan. | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 85 | `122151376083072582_1094284033273756` | Replica_Anidada | MI Nina Hermoxxa tienes perrito si | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 86 | `122151376083072582_1568066251531511` | Replica_Anidada | Tay Ochoa Chavez yo no practique nada, ni investigue nada, lo descubrí sola y me salió así en el acto | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 87 | `122151376083072582_1744827256820334` | Replica_Anidada | Delfina Gonzalez tiene perrito | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 88 | `122151376083072582_1780266269971013` | Comentario_Raiz | Hagan los ejercicios  Kegel ! | `No_Requiere_Respuesta` | Comentario contextual, anecdótico o crítico sin una solicitud inequívoca a Universe Sent Me; se conserva sin asumir intención. |
| 89 | `122151376083072582_1775721873777990` | Comentario_Raiz | Larga vida para aquel que lo tenga grueso ☝🏻😌 | `No_Requiere_Respuesta` | Comentario contextual, anecdótico o crítico sin una solicitud inequívoca a Universe Sent Me; se conserva sin asumir intención. |
| 90 | `122151376083072582_1348284624134552` | Replica_Anidada | Annita M. López yo de Xalapa chulada | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 91 | `122151376083072582_1566634178573529` | Comentario_Raiz | Jesús Alberto Prado moriré | `No_Requiere_Respuesta` | Comentario contextual, anecdótico o crítico sin una solicitud inequívoca a Universe Sent Me; se conserva sin asumir intención. |
| 92 | `122151376083072582_1009033282205725` | Replica_Anidada | Melanie Forte vivirás eterna 🩷 | `No_Requiere_Respuesta` | Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte. |
| 93 | `122151376083072582_2853949818299554` | Comentario_Raiz | En serio hombres ....... Que sienten, digan algo !!! 🙄 | `No_Requiere_Respuesta` | Comentario contextual, anecdótico o crítico sin una solicitud inequívoca a Universe Sent Me; se conserva sin asumir intención. |
| 94 | `122151376083072582_1235167878755515` | Comentario_Raiz | Rico para ambooooossss !!! | `No_Requiere_Respuesta` | Aprobación, risa, saludo, agradecimiento o reacción breve sin una pregunta dirigida a Universe Sent Me. |
| 95 | `122151376083072582_1794107981772564` | Comentario_Raiz | Jajaja 😂 cuando lo apretaba decía que le gustaba igual me dejo... | `No_Requiere_Respuesta` | Comentario contextual, anecdótico o crítico sin una solicitud inequívoca a Universe Sent Me; se conserva sin asumir intención. |
| 96 | `122151376083072582_1948100415854115` | Comentario_Raiz | Yo merengues 🤩😌 | `No_Requiere_Respuesta` | Aprobación, risa, saludo, agradecimiento o reacción breve sin una pregunta dirigida a Universe Sent Me. |
| 97 | `122151376083072582_1799264011071516` | Comentario_Raiz | 🥲😏🫣 | `No_Requiere_Respuesta` | Aprobación, risa, saludo, agradecimiento o reacción breve sin una pregunta dirigida a Universe Sent Me. |
| 98 | `122151376083072582_1481281560424877` | Comentario_Raiz | Gracias 😊 | `No_Requiere_Respuesta` | Aprobación, risa, saludo, agradecimiento o reacción breve sin una pregunta dirigida a Universe Sent Me. |
| 99 | `122151376083072582_1551717326189686` | Comentario_Raiz | Eso es lo más ricolino | `No_Requiere_Respuesta` | Comentario contextual, anecdótico o crítico sin una solicitud inequívoca a Universe Sent Me; se conserva sin asumir intención. |
| 100 | `122151376011072582_1051573194149891` | Comentario_Raiz | Contigo-karol g | `Pendiente_Respuesta` | Es una recomendación musical identificable por título y artista; la respuesta reconoce la canción y la conecta con el tono emocional de la publicación sin inventar una interpretación de la letra. |
| 101 | `122151376011072582_1458569976337294` | Comentario_Raiz | aventurera, Alberto plaza | `Pendiente_Respuesta` | Es una referencia musical identificable por título y artista; la propuesta responde a esa elección concreta y mantiene un remate USM breve, sin fingir que el comentario pidió análisis musical. |

## Integridad y siguiente paso

Se incorporaron 0 filas nuevas al ledger; 101 IDs ya estaban registrados. El ledger permanece anonimizado, append-only y con IDs únicos. No existe ninguna respuesta publicable sin una nueva autorización explícita de Fernando.

## Referencias

Fuentes: [Meta Graph API Comments and Mentions][1] y [Meta Graph API Comment reference][2].

[1]: https://developers.facebook.com/documentation/pages-api/comments-mentions
[2]: https://developers.facebook.com/docs/graph-api/reference/comment/
