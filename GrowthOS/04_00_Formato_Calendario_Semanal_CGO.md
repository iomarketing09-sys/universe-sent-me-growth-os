# Formato del Calendario Semanal (Propuesta CGO)

**Propósito:** Establecer la estructura de distribución semanal de contenido en las plataformas de Universe Sent Me, optimizando el mix entre reutilización de memes, reels, nuevo contenido y lore.
**Estado:** Active (Propuesta)
**Fecha de creación:** 2026-08-01
**Última actualización:** 2026-08-01
**Versión:** 1.0
**Autor:** Manus AI (CGO)
**Documentos relacionados:** `01_00_Arquitectura_Calendario_Escalable.md`, `01_01_Calendario_Semanal.md`, `01_03_Reuse_Queue.md`

---

## 1. Estrategia de Distribución Semanal (El Mix Ideal)

Como CGO, propongo una estructura semanal diseñada para maximizar el engagement, minimizar la fatiga de producción y mantener el ecosistema narrativo coherente. La semana consta de **12 a 15 piezas de contenido** distribuidas entre las 4 plataformas principales.

### 1.1 Cuotas de Formatos (Top of Funnel / Middle of Funnel)

Para mantener la salud de la audiencia y el algoritmo, dividimos el contenido en cuatro pilares:

| Pilar de Contenido | Cuota Semanal | Formatos Principales | Función en el Embudo |
| :--- | :--- | :--- | :--- |
| **Memes Reutilizados (Evergreen)** | 5 - 6 piezas | Fotos / Carruseles | **Viralidad y Retención.** Aprovechar el archivo de mayo (ej. Tarot, frases de Wilfred). Costo cero. |
| **Memes Nuevos (Proposals)** | 3 - 4 piezas | Fotos / Historias | **Frecuencia y Relatabilidad.** Adaptar las propuestas diarias de Drive al canon. Costo muy bajo. |
| **Reels / Video** | 2 - 3 piezas | Reels (9s - 30s) | **Alcance y Conversión.** Tests A/B, secciones recurrentes (afiliación), y activación de personajes. |
| **Lore / Narrativa Profunda** | 1 - 2 piezas | Carruseles / Reels largos | **Profundidad de Marca.** Historias serializadas, Cosmogonía, o activaciones especiales (ej. Fantasma). |

### 1.2 Distribución por Plataforma

No todo debe publicarse en todas partes. La estrategia se ajusta al comportamiento de cada plataforma:

*   **Instagram:** El hub central. Aquí se publica el 100% del mix (Reels, Fotos, Carruseles, Historias diarias). Es el motor principal de marca.
*   **TikTok / YouTube Shorts:** Enfocado casi exclusivamente en **Reels (video)**. El alcance aquí es más frío (nueva audiencia), por lo que el contenido debe ser visualmente impactante o muy relatable.
*   **Facebook:** El motor de viralidad masiva. Aquí brilla el contenido de **Fotos y Carruseles** (como el Tarot, que históricamente tiene millones de vistas). Los Reels se comparten, pero el foco es el formato estático.

---

## 2. Propuesta de Plantilla Semanal (Template W02+)

A continuación, presento cómo se vería una semana estándar (`Semana W02` a `W04`) aplicando las reglas del Growth OS (Regla de 30 días para reutilización, Regla de Equilibrio de personajes, y Bloqueo de Canon).

### Lunes: Apertura de Marca (Evergreen)
*   **Contenido:** Foto / Carrusel
*   **Personaje:** Universe (El Anfitrión)
*   **Acción:** Reutilización de Tarot o Frase de Universo.
*   **Plataformas:** Instagram, Facebook.

### Martes: El Gancho Visual (Reels)
*   **Contenido:** Reel (~9s - 15s)
*   **Personaje:** Wilfred o Elara
*   **Acción:** Reel nuevo o reutilizado de meme viral. Activación de formato recurrente.
*   **Plataformas:** Instagram, TikTok, YouTube Shorts.

### Miércoles: Frecuencia y Relatabilidad (Memes Nuevos)
*   **Contenido:** Foto / Meme Adaptado
*   **Personaje:** Rotativo (Payaso, Ganso, Universe)
*   **Acción:** Publicación de un meme nuevo aprobado de la carpeta `Generated_By_Gemini`.
*   **Plataformas:** Instagram, Facebook.

### Jueves: Narrativa o Profundidad (Lore)
*   **Contenido:** Carrusel o Reel largo
*   **Personaje:** Fantasma, Elara, o Narrativa
*   **Acción:** Activación de Cosmogonía, Principios Filosóficos, o el instante suspendido del Fantasma.
*   **Plataformas:** Instagram, Facebook.

### Viernes: El Gancho Visual (Reels / Tendencia)
*   **Contenido:** Reel (~15s - 30s)
*   **Personaje:** Universe o Wilfred
*   **Acción:** Reel de tendencia, test A/B de tono, o sección recurrente.
*   **Plataformas:** Instagram, TikTok, YouTube Shorts.

### Sábado: Frecuencia y Relatabilidad (Memes Nuevos)
*   **Contenido:** Foto / Meme Adaptado
*   **Personaje:** Rotativo (Elara, Kiri)
*   **Acción:** Segunda publicación de un meme nuevo de la semana.
*   **Plataformas:** Instagram, Facebook.

### Domingo: Cierre y Comunidad (Reutilización / Historias)
*   **Contenido:** Carrusel / Historias (Stories)
*   **Personaje:** Variable
*   **Acción:** Recopilación semanal, meme reutilizado exitoso de la semana anterior (si cumple 30 días), o interacción de comunidad.
*   **Plataformas:** Instagram (Stories), Facebook.

---

## 3. Reglas de Operación CGO para el Calendario

Para que este formato funcione a escala, se deben aplicar estas reglas al llenar el calendario:

1.  **Regla de Costo Cero (Prioridad 1):** El lunes, miércoles, sábado y domingo deben llenarse primero con **Memes Reutilizados** de la `Reuse Queue`. Solo si no hay memes disponibles se genera contenido nuevo.
2.  **Regla de la Carpeta Drive (Prioridad 2):** Los slots de "Memes Nuevos" (Martes y Viernes en la propuesta) deben llenarse exclusivamente con las piezas generadas por Manus/Gemini en la carpeta `Generated_By_Gemini`.
3.  **Regla de Aprobación de Fernando (Prioridad 3):** Los Reels y el Lore (Lunes/Jueves/Viernes) requieren aprobación explícita de Fernando. No se publican hasta que el estado sea `Aprobado`.
4.  **Regla de Canon:** Nunca se asignará un personaje a un formato que contradiga sus reglas de diseño (ej. El Fantasma nunca en un Reel dinámico, Wilfred nunca moralizando).

---

**Nota de CGO:** Esta estructura está lista para ser convertida en un flujo automatizado de Make que, cada domingo a las 23:00, genere el borrador de la siguiente semana filtrando automáticamente la `Reuse Queue` y el `Content Backlog` basado en estas cuotas.
