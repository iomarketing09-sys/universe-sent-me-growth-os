# Reporte de Contradicciones de Canon

**Mini-historia:** "La Búsqueda del Frasco Olvidado"
**Pipeline:** Meme-to-Reel Pipeline y Mini-Historias Serializadas
**Fecha del reporte:** 2026-07-31
**Estado:** Bloqueado — No publicar hasta corrección

---

## Resumen Ejecutivo

Se han identificado **5 contradicciones de canon** en la mini-historia "La Búsqueda del Frasco Olvidado" que impiden su producción y publicación. Ninguna automatización de publicación puede dispararse hasta que estos capítulos sean reescritos y re-aprobados por Fernando.

---

## Contradicciones Identificadas

### Contradicción #1 — Capítulo 7: Fantasma interviene activamente

| Campo | Valor |
| :--- | :--- |
| **Personaje** | Fantasma (`@char_USM_fantasma`) |
| **Lo que dice el canon (corregido 2026-08-02)** | El Fantasma está emocionalmente congelado en un instante que nunca cerró — esto no es incapacidad física ni prohibición de actuar. Se aferra por una lógica de supervivencia interna (creer que soltar sería dejar de existir), tan válida como el control del Ganso o la sabiduría de Wilfred. La restricción real es que su identidad congelada no puede resolverse ni superarse de forma heroica, dramática y visible dentro de un mismo episodio. |
| **Nota de lectura original (incorrecta)** | La versión anterior de este reporte decía "El Fantasma no puede seguir adelante en absoluto... no puede intervenir activamente en la trama" — eso trataba una condición emocional/identitaria como si fuera una restricción de movilidad física. Esa lectura no está respaldada por el canon real y ya se había propagado a varios documentos de Growth OS (corregidos en el mismo commit que esta nota). |
| **Lo que hace la historia** | El Fantasma interviene activamente para detener el caos y "salvar el día". |
| **Fuente canon** | `02 Personajes/Segundo Círculo/Fantasma/01 Territorio emocional.md`, `03 Reglas de diseño.md` (commit `cf2ac53`) |
| **Tipo de error** | Pendiente de reconfirmar — la actúación física del Fantasma en sí no es el problema. El punto real a verificar es si el capítulo presenta su identidad congelada como resuelta o superada de forma dramática y visible ("salva el día" como resolución heroica de su propio arco), lo cual sí violaría Principio 3 (el cambio es invisible) y el Estándar de Historias (ninguna máscara cae por completo). Claude no tiene el texto completo del Capítulo 7 en este momento — este campo queda abierto hasta relectura directa del capítulo. |
| **Corrección necesaria** | Releer el Capítulo 7 bajo la lectura corregida antes de decidir si reescribirlo. Si el Fantasma solo actúa físicamente sin que eso implique resolver o superar su identidad congelada, no hay contradicción. Si "salva el día" se presenta como una resolución dramática de su arco interno, sí requiere reescritura — pero el motivo sería ese, no una imposibilidad de movimiento. |

---

### Contradicción #2 — Capítulo 10: Universe como orquestador omnisciente

| Campo | Valor |
| :--- | :--- |
| **Personaje** | Universe (`@char_USM_universe`) |
| **Lo que dice el canon** | Universe conoce el mecanismo pero nunca entiende completamente el propósito ni tiene acceso total. No es orquestador de conflictos. |
| **Lo que hace la historia** | Universe revela que "sabía todo el plan desde el inicio", convirtiéndolo en el orquestador de todo el conflicto. |
| **Fuente canon** | `02 Personajes/Primer Círculo/Universe/03 Reglas de diseño.md` (commit `cf2ac53`) |
| **Tipo de error** | Contradicción directa con regla de diseño cerrada |
| **Corrección necesaria** | Reescribir el capítulo 10 para que Universe NO revele omnisciencia. Su rol debe mantener la limitación de conocimiento parcial. |

---

### Contradicción #3 — Capítulo 8: Moralización explícita y CTA didáctico

| Campo | Valor |
| :--- | :--- |
| **Personaje** | Wilfred (`@char_USM_wilfred`) |
| **Lo que dice el canon** | El Estándar de Historias prohíbe que una historia exista para ilustrar una lección. Ningún personaje puede diagnosticar a otro. La lección debe sentirse sin nombrarse. |
| **Lo que hace la historia** | Diálogo de Wilfred con CTA explícito: "¿crees que Universe aprendió la lección?" — moraliza explícitamente. |
| **Fuente canon** | `07 Historias/00 Estándar de Historias.md` (commit `cf2ac53`) |
| **Tipo de error** | Violación del Estándar de Historias (anti-tono moralizante) |
| **Corrección necesaria** | Reescribir el diálogo y el CTA para que la lección se sienta sin nombrarse. Eliminar cualquier frase que diagnostique o moralice. |

---

### Contradicción #4 — Duplicación de rol: Elara como tarotista

| Campo | Valor |
| :--- | :--- |
| **Personaje afectado** | Elara (`@char_USM_elara`) |
| **Lo que dice el canon** | Elara es lectora de cartas mágicas conectada con astrología y naturaleza. Su identidad diferenciada es distinta del rol de tarotista. |
| **Lo que hace la historia** | Asigna a Elara un "consultorio de tarot interactivo" que duplica el rol ya establecido y viral de Universe como tarotista. |
| **Fuente canon** | `02 Personajes/Primer Círculo/Elara/03 Reglas de diseño.md` + identidad visual de Universe (outfit tarotista) |
| **Tipo de error** | Dilución de activo establecido (el tarot es identidad visual viral de Universe) |
| **Corrección necesaria** | Asignar a Elara un ángulo de contenido distinto que no solape con el tarot de Universe. Potenciar su conexión con astrología y naturaleza como diferenciador. |

---

### Contradicción #5 — Nombre "Silvio" — ✅ RESUELTO (2026-08-03)

| Campo | Valor |
| :--- | :--- |
| **Personaje** | Payaso (`@char_USM_payaso`) |
| **Lo que dice el canon** | El personaje del Primer Círculo se llama "Payaso". No existe nombre propio aprobado. |
| **Lo que hace la historia** | Usa el nombre "Silvio" para el Payaso sin confirmación previa. |
| **Fuente canon** | `02 Personajes/Primer Círculo/Payaso/00 Resumen.md` (commit `cf2ac53`) |
| **Tipo de error** | Identificador no aprobado |
| **Resolución de Fernando (2026-08-03)** | Silvio es el nombre confirmado para El Payaso, junto con un diseño corregido (se detectó que el reference sheet original usaba el arquetipo del "payaso triste" clásico, contradiciendo la regla de diseño; el diseño corregido ya fue aprobado y registrado en canon, commit `8e9fe9a`). `#SilvioUSM` queda autorizado. |
| **Estado** | ✅ RESUELTO — Desbloqueado. |

---

## "Maeve" / MaeveUSM — ✅ RESUELTO, no era una contradicción (2026-08-03)

| Campo | Valor |
| :--- | :--- |
| **Personaje involucrado** | "Maeve" |
| **Resolución de Fernando** | Maeve es el nombre confirmado de la Chica del Suéter (carpeta `PERSONAJES/Maeve (la chica del suéter)/` en Drive, ya revisada por Claude). El post del 2026-08-02 con `#MaeveUSM` y `#FantasmaUSM` **no era un error de identidad** — la pieza muestra a Maeve abrazando al Fantasma; ambos hashtags son correctos porque ambos personajes aparecen en la escena. Claude marcó esto como contradicción por error de lectura propia; queda corregido aquí. |
| **Formalización** | Maeve quedó formalizada junto con Kael en el commit canónico `a994354`. Maeve es la Chica del Suéter; Kael es el Chico de los Pantalones. Ambos nombres están cerrados y sus hashtags propios están autorizados. |
| **Estado** | Sin bloqueo. `#MaeveUSM` y `#FantasmaUSM` pueden co-existir en una misma pieza cuando ambos personajes aparecen juntos. |

---

## Contradicción — "Kiri" / KiriUSM y "#LoresUSM" — ✅ RESUELTO (2026-08-03)

| Campo | Valor |
| :--- | :--- |
| **Personaje involucrado** | "Kiri", nombre de El Hada |
| **Resolución de Fernando** | Kiri es el nombre que Fernando le asignó a El Hada. **Confirmado y ya registrado en canon**: `Universe Sent Me - Biblia/02 Personajes/Segundo Círculo/Hada/00 Resumen.md` (commit `f7bebca`, v1.1, 2026-08-03). `#KiriUSM` queda autorizado para uso en Growth OS. |
| **Sobre "#LoresUSM"** | Fue un typo — una "s" de más. No es un elemento de canon; Fernando está implementando un kit de hashtags de marca con firma `USM` (ver `10_00_Kit_de_Hashtags_USM.md`). Corregir a `#LoreUSM` si se usa como categoría temática, o retirar el hashtag si no corresponde a esta pieza. |
| **Estado** | Desbloqueado. |

---

## Estado de Bloqueo

| Ítem | Estado | Acción requerida |
| :--- | :--- | :--- |
| Capítulo 7 | **BLOQUEADO — pendiente relectura** | Motivo original corregido. Releer bajo lectura correcta del Fantasma antes de desbloquear. |
| Capítulo 8 | **BLOQUEADO** | Reescribir — Eliminar moralización explícita |
| Capítulo 10 | **BLOQUEADO** | Reescribir — Universe no puede ser omnisciente |
| Elara / Tarot | **BLOQUEADO** | Reescribir — Asignar ángulo distinto a Elara |
| ~~"Silvio" (Payaso)~~ | **✅ RESUELTO** | Registrado en canon (commit `8e9fe9a`), diseño corregido y aprobado. Desbloqueado. |
| ~~"Maeve" / MaeveUSM~~ | **✅ RESUELTO** | No era contradicción — error de lectura de Claude, corregido. Pendiente solo el commit formal de canon. |
| ~~"Kiri" / KiriUSM~~ | **✅ RESUELTO** | Registrado en canon (commit `f7bebca`). Desbloqueado. |
| ~~"LoresUSM"~~ | **✅ RESUELTO** | Era typo, no elemento de canon. Ver kit de hashtags. |

---

## Regla de Bloqueo Operativo

> Ninguna automatización de publicación (Story Scheduler, Meme-to-Reel Factory, etc.) puede dispararse para esta mini-historia hasta que:
> 1. Las contradicciones de canon sean corregidas por Fernando.
> 2. Fernando o Claude cambien el estado a "Aprobado" en el Calendario Editorial del Growth OS.
> 3. Se pruebe el flujo de aprobación del puente con este caso como primera prueba real.
