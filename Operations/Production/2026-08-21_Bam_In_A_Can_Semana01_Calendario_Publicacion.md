---
title: "Bam in a Can — Semana 01: calendario de publicación"
purpose: "Coordinar la salida del primer lote de cuatro piezas de Bam in a Can, sus metadatos por plataforma y las ventanas mínimas de medición sin programar publicaciones automáticas."
status: "Active — CAN-001 y CAN-002 medidas; CAN-003 con cascada completa y corte inicial preparado"
created: 2026-08-21
updated: 2026-08-25
version: "1.9"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Production/2026-08-21_Bam_In_A_Can_Semana01_Paquete_Lanzamiento.md"
  - "Operations/Production/2026-08-20_Plan_Lanzamiento_Audiencia_Bam_In_A_Can.md"
  - "Operations/Research/Content_Rewards_Pilot_Ledger.csv"
  - "Operations/Research/Bam_In_A_Can_Distribution_Ledger.csv"
organization: "Operations/Production"
---

# Bam in a Can — Semana 01: calendario de publicación

## Propósito operativo

Este calendario presenta a Bam in a Can como un archivo editorial, no como un lote de videos subido de golpe. La separación de 48 horas permite capturar señales tempranas de cada pieza antes de exponer la siguiente, mientras que la secuencia TikTok → Instagram Reels → YouTube Shorts preserva una ventana de lanzamiento controlada por día. Las horas son una hipótesis de arranque para cuentas sin historial; no deben presentarse como “horas óptimas” hasta reunir datos propios.

## Calendario propuesto

| Orden | Pieza | Fecha | Ventana de carga y audio | TikTok | Instagram Reels | YouTube Shorts | Propósito de la salida |
|---:|---|---|---|---|---|---|---|
| 1 | CAN-001 — *It Was Making Noise From the Inside* | Viernes 21 Ago | 18:00–18:45 CDT: elegir audio nativo de tensión y verificar disclosure | 19:00 CDT | 19:20 CDT | 19:45 CDT | Presentar la lata y establecer el lenguaje del archivo. |
| 2 | CAN-002 — *The Memory Printer* | Domingo 23 Ago | 18:00–18:45 CDT: elegir audio nativo de tecnología nostálgica y verificar recibo vacío | 19:00 CDT | 19:20 CDT | 19:45 CDT | Demostrar la rama de falso comercial. |
| 3 | CAN-003 — *Do Not Insert Coins After Midnight* | Martes 25 Ago | 18:00–18:45 CDT: elegir audio nativo que no tape moneda, espirales ni abolladuras | 19:00 CDT | 19:20 CDT | 19:45 CDT | Ampliar el mundo con una anomalía narrativa de entorno. |
| 4 | CAN-004 — *A Normal Amount of Internet* | Jueves 27 Ago | 18:00–18:45 CDT: preservar hum, clicks y remate de cursor | 19:00 CDT | 19:20 CDT | 19:45 CDT | Cerrar la semana con la pieza más ligera y compartible. |

## Reglas de audio y copy

TikTok e Instagram usarán audio nativo únicamente cuando el primer loop añada tensión y permita oír los SFX clave de la pieza. YouTube Shorts se publica con los SFX originales como control de medición. La frase `Original fiction. AI-made.` y la etiqueta de contenido generado/alterado, cuando la plataforma la ofrezca, son obligatorias en las tres redes. No usar el mismo audio por comodidad: se registra título, creador, volumen y segundo de entrada de cada elección nativa.

## Salida registrada

CAN-001 ya se publicó en TikTok el 21 de agosto de 2026 a las 19:04:20 CDT. El ID canónico es `7676640119222209813` y el audio declarado por Fernando es `Do It` — Infraction Music. También salió en Instagram Reels a las 19:20:00 CDT con shortcode `DcUnEVnsoaV`, el mismo audio al 80 % y el disclosure verificado en el caption público. YouTube Shorts cerró la cascada a las 19:50:00 CDT con ID `iuHT1kN0Uow` y SFX originales sin música nativa. La publicación real queda en el ledger. El disclosure de TikTok y YouTube aún requiere verificación porque no se observó en las vistas públicas recuperadas.

## Activación manual de CAN-002 — domingo 23 de agosto

El corte operativo de CAN-001 no identifica una “hora ganadora” ni prueba que el volumen de audio de Instagram explique su mayor consumo; solo muestra que Instagram acumuló más views y watch time medio en la primera pieza. Por ello, CAN-002 conserva la ventana de arranque y el diseño 2 + 1: publicar la pieza hoy sin esperar más datos, pero sin repetir el 80 % de volumen por inercia.

| Momento CDT | Acción exacta | Criterio de ejecución |
|---|---|---|
| 18:45–18:55 | **Go/no-go manual.** Confirmar el corte final de 10 s, recibo completamente vacío, overlay y disclosure. | Si algún elemento falla, no publicar y mover el bloque completo 24 h. |
| 19:00 | **TikTok.** Subir `CAN-002`; elegir dentro de la app un loop lento, tecnológico y nostálgico, sin letra explicativa. Mantener SFX audibles. | Audio nativo al **10–12 %**, entrando desde 00:00. Activar etiqueta IA si está disponible. |
| 19:20 | **Instagram Reels.** Subir el mismo export; elegir un audio nativo propio de la app con textura analógica/ambiental y sin letra dominante. | Audio nativo al **8–10 %**, entrando desde 00:00. No replicar 80 %: CAN-001 no permite atribuirle su resultado. Activar etiqueta IA si está disponible. |
| 19:50 | **YouTube Shorts.** Subir el mismo export como control. | **Solo SFX originales; sin canción.** Marcar contenido alterado/generado si la interfaz lo solicita. |

### Metadatos bloqueados de CAN-002

| Elemento | Texto / regla |
|---|---|
| Overlay | `FOR PEOPLE WHO MISS A SUMMER THEY NEVER HAD.` de **00:00 a 00:02.5**. |
| Caption exacto | `This product was recalled before anyone could forget it.`<br><br>`Original fiction. AI-made.` |
| Hashtags | `#BamInACan #Weirdcore #FakeCommercial #AIVideo` |
| Estructura visual | Impresora retro color hueso, recibo sin texto ni código visible, indicador ámbar, papel que avanza y se curva; corte seco al final. No añadir CTA ni explicación. |
| Registro T0 | Tras cada publicación, guardar ID/permalink, hora real, audio, creador, volumen y segundo de entrada. Calcular T+3 h/T+24 h/T+72 h/T+7 d desde cada T0 real. |

### Registro real — CAN-002 TikTok

| Campo | Dato confirmado |
|---|---|
| Estado | Publicado. |
| T0 canónico | 23 Ago 2026, 18:59:43 CDT; recuperado del ID canónico. |
| ID / permalink | `7677381101991644437` · `https://www.tiktok.com/@bam_in_a_can/video/7677381101991644437` |
| Audio, copy y disclosure | Pendientes de confirmación o verificación pública; no se infieren. |
| T+3 h | 23 Ago, 21:59:43 CDT |
| T+24 h | 24 Ago, 18:59:43 CDT |
| T+72 h | 26 Ago, 18:59:43 CDT |
| T+7 d | 30 Ago, 18:59:43 CDT |

### Registro real — CAN-002 Instagram Reels

| Campo | Dato confirmado |
|---|---|
| Estado | Publicado. |
| T0 público | 23 Ago 2026, 19:20:37 CDT; recuperado del atributo `datetime` visible en el permalink. |
| Shortcode / permalink | `DcZv1l4sjhz` · `https://www.instagram.com/reel/DcZv1l4sjhz/` |
| Copy y disclosure | Verificados públicamente: copy exacto, `Original fiction. AI-made.` y los cuatro hashtags aprobados. |
| Audio | `she share post (for blog)`; creador y volumen no informados. |
| T+3 h | 23 Ago, 22:20:37 CDT |
| T+24 h | 24 Ago, 19:20:37 CDT |
| T+72 h | 26 Ago, 19:20:37 CDT |
| T+7 d | 30 Ago, 19:20:37 CDT |

La siguiente acción de la cascada es YouTube Shorts. Su T0 se registrará por separado; no se reutilizan los T0 de TikTok ni Instagram.

### Registro real — CAN-002 YouTube Shorts

| Campo | Dato confirmado |
|---|---|
| Estado | Publicado; cascada CAN-002 completa. |
| T0 público | 23 Ago 2026, 19:57:00 CDT; recuperado de `uploadDate` y `publishDate` públicos (`17:57:00 -07:00`). |
| ID / permalink | `-P8er9X9ggw` · `https://youtube.com/shorts/-P8er9X9ggw` |
| Audio | SFX originales sin música nativa; control confirmado por Fernando. |
| Disclosure | El título público muestra `AI-made`; el disclosure completo y la etiqueta de IA siguen pendientes de confirmación. |
| T+3 h | 23 Ago, 22:57:00 CDT |
| T+24 h | 24 Ago, 19:57:00 CDT |
| T+72 h | 26 Ago, 19:57:00 CDT |
| T+7 d | 30 Ago, 19:57:00 CDT |

Con este registro, CAN-002 conserva el diseño 2 + 1: TikTok e Instagram con audio nativo compartido y YouTube con SFX originales. Las tres plataformas se miden con su propio T0.

### Control programado — CAN-002 T+72

Se programó un único control consolidado para el **miércoles 26 de agosto de 2026 a las 20:10 CDT**. Esta hora se sitúa después de las tres ventanas T+72 de CAN-002: TikTok 18:59:43, Instagram Reels 19:20:37 y YouTube Shorts 19:57:00 CDT. La programación solo consulta, documenta y reporta; **no publica, edita ni responde contenido**.

El corte usará TikTok mediante la cuenta orgánica de Bam en Windsor.ai, Instagram por shortcode `DcZv1l4sjhz` sin rangos de fecha y bloques de hasta cuatro fields, e intentará YouTube por Windsor sin registrar una ausencia como cero. Si no existe una fila de YouTube, conservará la indexación pendiente y utilizará únicamente evidencia de Studio que Fernando haya compartido con timestamp o edad disponible. El snapshot y el ledger se actualizarán con la hora, fuente, frescura y límites de comparabilidad reales.

## Registro parcial — CAN-003

CAN-003 completó su cascada el 25 de agosto. Los identificadores confirmados son TikTok `7678142841209589012`, Instagram Reels `DcfDsCIMrpx` y YouTube Shorts `ZKm8Xb817A8`. Cada plataforma conserva su propio T0; las horas no se infieren a partir de la secuencia de publicación.

| Plataforma | Estado y metadatos confirmados | Ventanas disponibles |
|---|---|---|
| TikTok | Publicado; ID canónico confirmado. Audio, volumen, etiqueta IA y T0 todavía pendientes de confirmación de Fernando. | Se fijarán cuando exista T0 verificable. |
| Instagram Reels | Publicado; shortcode confirmado. Audio `Order now` — Portizmusic. El copy, la pregunta diegética, el disclosure y los hashtags están verificados públicamente. Volumen, etiqueta IA y T0 aún pendientes. | Se fijarán cuando exista T0 verificable. |
| YouTube Shorts | Publicado; ID `ZKm8Xb817A8`. T0 público **25 Ago, 20:54:05 CDT**, recuperado de `datePublished` (`18:54:05 -07:00`). SFX sin música confirmado por Fernando; etiqueta AI visible en la página pública. | T+3: **25 Ago, 23:54:05 CDT**; T+24: **26 Ago, 20:54:05 CDT**; T+72: **28 Ago, 20:54:05 CDT**; T+7 d: **1 Sep, 20:54:05 CDT**. |

El primer corte multicanal se realiza después de la ventana T+3 de YouTube. Para TikTok e Instagram se etiquetará como snapshot posterior a T0 hasta recuperar sus horas reales; no se los presentará como T+3 exacto.

## Go/no-go por cada día

La hora de publicación no autoriza una salida automática. A las 18:45 CDT, Fernando verifica el export correcto, caption, disclosure y selección de audio. Si falta alguno, la pieza se pospone al siguiente día disponible y todo el calendario se mueve 24 horas, manteniendo siempre la separación mínima de 36 horas entre piezas.

| Momento | Control | Registro requerido |
|---|---|---|
| T0 | ID nativo, permalink, copy exacto, audio y plataforma | Registro maestro de Bam / ledger de distribución. |
| T+3 h | Reproducciones, likes, comentarios, shares, guardados y visitas al perfil cuando existan | Snapshot inicial. |
| T+24 h | Métricas por plataforma y señales cualitativas | Snapshot de día uno. |
| T+72 h | Métricas actualizadas, retención cuando esté disponible y lectura comparativa preliminar | Snapshot de tres días. |
| T+7 d | Cierre de pieza y actualización de aprendizaje | Growth OS; no declarar ganador por una sola pieza. |

## Dependencias antes de iniciar CAN-001

La propuesta asume que los cuatro clips finales ya están aprobados. Antes de publicar cada CAN, seleccionar manualmente los audios nativos de TikTok e Instagram y preparar los tres uploads con el copy correcto. El ledger `Operations/Research/Bam_In_A_Can_Distribution_Ledger.csv` ya contiene los doce renglones planificados; en T0 solo se completan sus campos de publicación real. Este documento no programa publicaciones automáticas, no vincula cuentas ni publica contenido. El único control de medición descrito arriba queda programado como revisión documental y no modifica permisos de las plataformas.
