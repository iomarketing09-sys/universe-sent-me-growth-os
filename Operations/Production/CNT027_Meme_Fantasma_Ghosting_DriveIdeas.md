# CNT-027 — Meme Fantasma: "Ghosting eterno" (propuesta desde Drive Ideas-Memes)

| Campo | Valor |
| :--- | :--- |
| **Propósito** | Propuesta de meme del Fantasma generada a partir del patrón de las semillas de ideas guardadas en Google Drive (carpeta "Universe Sent Me > Ideas > Memes"), para aprobación y publicación en Facebook/Instagram |
| **Estado** | Draft (pendiente de aprobación de Fernando) |
| **Fecha de creación** | 2026-08-14 |
| **Última actualización** | 2026-08-14 |
| **Versión** | 1.0 |
| **Autor** | Manus AI (CGO) |
| **ID** | CNT-027 |
| **Documentos relacionados** | `GrowthOS/03_00_Sistema_Generacion_Memes.md`, `GrowthOS/05_03_Calendario_10_16_Agosto.md`, `GrowthOS/12_00_Sistema_Dos_Capas_Contenido_Canon.md`, `GrowthOS/00_01_Changelog_GrowthOS.md` (entrada [1.2.10]), `Operations/Production/CNT026_Memes_FinDeSemana_16_17_Ago.md`, `Operations/Research/2026-08-12_Revision_Cambios_GrowthOS_Claude_Fernando.md` |

## 1. Origen de la propuesta

El usuario pidió revisar la carpeta de Google Drive **"Universe sent me > Ideas > Memes"** (ID Ideas: `1Aav6tyHJPwpUPHox7Dh3upttKhkuC0Kj`; Memes: shortcut a `1BpKZpUBIT5jBjkvw7epymlsD3Gp4lwzE`, con subcarpetas **Dump** y **Nuevos**; ~19 archivos mayormente capturas de referencia externa). De la revisión se extrajeron cuatro patrones recurrentes en las semillas:

| Patrón identificado | Ejemplo en Drive | Territorio emocional |
| :--- | :--- | :--- |
| Espera eterna resignada con elemento mañanero | Perro en bata con café: "¿Qué vendrá primero mi boda o Jesús?" | Anhelo por algo que no llega + resignación divertida |
| Autodesprecio compartido con punchline seco | Texto plano: "Tu soltera y yo soltero... (Que nadie nos soporta)" | Pareja/amistad que se ríe de sí misma |
| Ternura interactiva | Kawaii "pause to see what he thinks about you" | Cariño + mecánica de "pausa el video" |
| Agotamiento social cotidiano | Conejo en junta: "when I've already used all my fake laughs and the person keeps talking" | Sobreexigencia emocional + trabajo/oficina |

La propuesta **combina los dos primeros patrones** (espera eterna + punchline de resignación) con el **personaje Fantasma** y un **giro moderno de mensajería**, la combinación con mayor evidencia de viralidad del Growth OS (ver sección 3).

## 2. Propuesta

**Base visual:** asset existente `8 - Fantasma_levitating_above_woods_2K_202608060333.jpeg` (Fantasma levitando sobre el bosque, 2K, del proyecto). Foto estática, sin texto incrustado.

**Copy:**

> Hace 400 años que no me contestan un mensaje. Ahora le dicen ghosting. Yo solo lo llamaba martes.
>
> #FantasmaUSM #MemesUSM #UniverseSentMe

**Slot sugerido:** 4:00–5:00 PM (horario validado en baselines; mejor hora por volumen según `05_03`). Día: preferente fin de semana o el próximo slot 4 PM disponible; si se publica el sábado 16, el calendario 05_03 marca "contenido nuevo" ese día.

## 3. Scoring (rúbrica oficial, ejecutado con `scripts/score_proposal.py`)

| Criterio | Puntaje | Peso | Justificación |
| :--- | :--- | :--- | :--- |
| relatable | 9 | 30% | Cualquier seguidor ha mandado mensajes que nadie responde; el "visto" es universal |
| humor_or_emotion | 9 | 25% | Resignación absurda + punchline seco, el motor del post Fantasma de 173.9K |
| share_hook | 9 | 15% | Invita a etiquetar al amigo que tarda en contestar y compartir en historias |
| modern_twist | 9 | 10% | Ghosting de WhatsApp integrado en la espera eterna, paralelo al Universe astral (3.31% ER) |
| character_voice | 9 | 10% | El Fantasma ES la espera eterna y el arco no resuelto; voz consistente con canon |
| slot_fits | 10 | 5% | 4:00–5:00 PM es el mejor horario del calendario |
| format_ok | OK | 3% | Foto estática 2K + frase en copy (nunca Reel de texto) |
| canon_safe | OK | 2% | Sin moralización; el arco no se resuelve, la máscara no cae, la espera sigue invisible |

**SCORE: 9.10/10 — PASS (mínimo 8.5)**.

**Benchmark esperado:** alcance estimado 60K–174K (rango del post top de Fantasma), ER esperado ~2.1–3.3% (entre el ER del post Fantasma de julio y el techo del periodo). Compartidos: objetivo ≥ 0.5% del alcance.

## 4. Reglas duras verificadas

La propuesta cumple el formato foto estática + copy (prohibido Reel de texto), usa solo hashtags del roster oficial (`#FantasmaUSM`, `#MemesUSM`, raíz `#UniverseSentMe`), no moraliza ni diagnostica, y —punto clave— **no resuelve el arco del Fantasma**: el chiste refuerza su estado eterno sin mostrar cambio visible, conforme al Sistema de Dos Capas (Capa 1: memes sueltos no requieren promoción de canon). No se fija ningún vínculo nuevo.

## 5. Pendientes y notas

Si Fernando aprueba, se produce la imagen (o se reutiliza el asset 2K existente) y se publica en el slot; luego se registra el resultado en el ExperimentLog para actualizar las métricas del Fantasma. Nota operativa: aplicar regla de 30 días si se contempla reutilizar esta imagen en un futuro "meme to reel".
