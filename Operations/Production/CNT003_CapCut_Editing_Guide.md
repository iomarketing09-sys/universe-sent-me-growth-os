# CNT-003 Trailer 001 — Guía de Edición en CapCut

**Propósito:** Instrucciones paso a paso para ensamblar el trailer de Universe Sent Me en CapCut, incluyendo timeline, transiciones, BGM, color grading y exportación.
**Estado:** Draft
**Fecha de creación:** 2026-08-06
**Última actualización:** 2026-08-06
**Versión:** 1.0
**Autor:** Manus AI (CGO)
**Documentos relacionados:** `CNT003_Trailer001_Clip_Plan.md`, `CNT003_Trailer001_Video_Prompts.md`, `Showreel_Storyboard_Blueprint.md`

---

## Configuración Inicial del Proyecto

| Ajuste | Valor |
| :--- | :--- |
| **Proyecto nuevo** | CapCut → New Project |
| **Aspect ratio** | 9:16 (vertical) |
| **Resolución** | 1080 x 1920 (2K si los clips lo permiten) |
| **Frame rate** | 30fps |
| **Formato de clips importados** | Los 10-11 clips generados en Flow |
| **BGM** | Archivo de música épica orquestal (buscar en biblioteca CapCut o importar propio) |

---

## BGM: Música Épica en CapCut

**Opción A — Biblioteca de CapCut:**
1. Toca **Audio** → **Sounds** → busca:
   - "epic cinematic"
   - "orchestral cinematic"
   - "fantasy epic"
   - "cinematic trailer music"
2. Filtra por duración: busca una pieza de 45-60 segundos que tenga construcción (empieza suave, sube al clímax).
3. Recomendación: busca tracks con la etiqueta "Epic" en la categoría Cinematic.

**Opción B — Importar audio propio:**
- Si generaste la BGM en otra herramienta (Suno, Udio, etc.), impórtala como archivo MP3/WAV.
- Arrastra el archivo a la timeline en la pista de audio.

**Estructura esperada de la música:**
- `00:00-00:14` — Inicio suave (piano/strings,sparse)
- `00:14-00:25` — Construcción gradual
- `00:25-00:30` — Dip/pausa breve (Silvio)
- `00:30-00:35` — Tensión oscura (Fantasma)
- `00:35-00:40` — Crescendo explosivo (Portal)
- `00:40-00:45` — Pico máximo (Bosque Cósmico)
- `00:45-00:48` — Resolución (Outro)

---

## Step-by-Step: Ensamblaje del Timeline

### Paso 1: Importar todos los clips

1. Abre CapCut → **New Project**
2. Importa los 10-11 clips generados en Flow (en orden numérico)
3. Arrastra todos a la timeline en este orden:

| Orden | Clip | Imagen Referencia | Duración Sugerida |
| :--- | :--- | :--- | :--- |
| 1 | Mar de Nubes | Img 1 | 5.0s |
| 2 | Wilfred en bosque cósmico | Img 4 | 5.0s |
| 3 | Universe (gato) | Img 3 | 4.0s |
| 4 | Elara (fuego) | Img 5 | 4.0s |
| 5 | Kiri (hada) | Img 6 | 4.0s |
| 6 | Silvio (payaso) | Img 7 | 3.0s |
| 7 | Fantasma + gatos | Img 8 | 5.0s |
| 8 | Portal Cósmico | Img 9 | 4.0s |
| 9 | Bosque Cósmico | Img 10 | 5.0s |
| 10 | Outro | Img 11 | 4.0s |

**Total: ~43 segundos**

### Paso 2: Ajustar duraciones de cada clip

1. Toca cada clip en la timeline.
2. Arrastra los bordes del clip para ajustar la duración exacta.
3. **Tip:** Si un clip de Flow es más largo de lo necesario (ej: Flow generó 8s pero solo necesitas 5s), recórtalo manteniendo la mejor parte del movimiento.

### Paso 3: Transiciones entre clips

El principio de este trailer es **cortes secos** (no transiciones suaves), para mantener ritmo cinematográfico. Las únicas excepciones:

| Entre Clip | Tipo de Transición | Notas |
| :--- | :--- | :--- |
| Clip 1→2 (Mar de Nubes → Wilfred) | **Corte seco** | Cambio de mundo a personaje, impacto directo |
| Clip 2→3 (Wilfred → Universe) | **Corte seco** | Personaje a personaje |
| Clip 3→4 (Universe → Elara) | **Corte seco** | Personaje a personaje |
| Clip 4→5 (Elara → Kiri) | **Corte seco** | Personaje a personaje |
| Clip 5→6 (Kiri → Silvio) | **Corte seco** | Cambio de tono (de etéreo a absurdo) |
| Clip 6→7 (Silvio → Fantasma) | **Corte seco** | Cambio de tono (de absurdo a misterioso) |
| Clip 7→8 (Fantasma → Portal) | **Corte seco + flash blanco** | El portal explota — usar el flash natural del clip |
| Clip 8→9 (Portal → Bosque Cósmico) | **Disolver corto (0.3-0.5s)** | Única transición suave, conecta el clímax |
| Clip 9→10 (Bosque Cósmico → Outro) | **Fade to black (0.5s)** | Cierre cinematográfico |

**Cómo aplicar en CapCut:**
- Para cortes secos: simplemente coloca los clips uno al lado del otro sin solapamiento.
- Para fade to black: toca el clip → **Animation** → **Out** → selecciona "Fade" → ajusta duración a 0.5s.
- Para disolver: toca la unión entre dos clips → **Transition** → selecciona "Dissolve" → 0.3-0.5s.

### Paso 4: BGM en la timeline

1. Toca **Audio** en la barra inferior → **Sounds** o **Import** (si tienes tu propio archivo).
2. Arrastra la música épica a la pista de audio debajo de los clips.
3. Alinea el inicio de la música con el inicio del primer clip.
4. Si la música es más larga que el video, córtala al final del clip 10.
5. Si la música es más corta, extiéndela o busca una más larga.

**Ajuste fino de BGM por sección:**

| Sección | Clips | Volumen BGM | Notas |
| :--- | :--- | :--- | :--- |
| Introducción | 1-2 | 60-70% | Inicio suave, la música entra gradualmente |
| Personajes | 3-6 | 70-80% | Música sostiene, no domina |
| Silvio (dip) | 6 | 50% | Baja el volumen aquí para la pausa absurda |
| Fantasma | 7 | 65% | Música más oscura/tensa |
| Clímax (Portal) | 8 | 90-100% | Música al máximo, sincroniza con la explosión |
| Bosque Cósmico | 9 | 100% | Pico máximo de la música |
| Outro | 10 | 40-50% (fade out) | Música baja y se desvanece |

**Cómo ajustar volumen por sección en CapCut:**
1. Toca la pista de audio en la timeline.
2. Toca la sección que quieres ajustar.
3. Toca **Volume** y ajusta el valor.
4. Para fade in/out: toca **Fade in** / **Fade out** en la sección de audio.

### Paso 5: Color Grading (opcional pero recomendado)

Para mantener consistencia visual entre todos los clips:

1. Selecciona el primer clip en la timeline.
2. Toca **Filter** o **Adjust** → selecciona un filtro base.
3. Filtro recomendado: **"B&W"** al 0% (neutral), o busca filtros como:
   - "Film" → subtle
   - "Vivid" → si quieres más saturación
   - "Cinema" → tono cinematográfico
4. Ajusta ligeramente:
   - **Contrast:** +5 a +10 (para más impacto)
   - **Saturation:** +5 a +10 (para mantener colores vivos)
   - **Highlights:** -5 a -10 (para no quemar las luces)
   - **Shadows:** +5 (para mantener detalle en zonas oscuras)
5. **Importante:** Aplica los mismos ajustes a TODOS los clips para mantener consistencia.

**Cómo aplicar a todos los clips:**
1. Ajusta el primer clip como quieres.
2. Toca **Adjust** → **Save Preset** → dale un nombre (ej: "USM Trailer").
3. Selecciona los demás clips → **Adjust** → **Apply Preset** → "USM Trailer".

### Paso 6: Ajuste de velocidad (opcional)

Si algún clip se siente muy rápido o muy lento:
1. Toca el clip → **Speed**.
2. Ajusta: 0.8x para ralentizar ligeramente, 1.2x para acelerar.
3. **Tip:** El clip del Portal (8) puede ir a 1.1x para más impacto explosivo.
4. **Tip:** El clip del Outro (10) puede ir a 0.9x para más calma.

### Paso 7: Audio original de los clips

Los clips de Flow generan su propio audio (ambientación, viento, fuego, etc.). Esto es BUENO — úsalo.

1. Verifica que cada clip tenga su audio original activo.
2. El volumen del audio original debe estar entre **10-30%** (por debajo de la BGM).
3. La BGM debe estar entre **60-100%** (dominante).
4. Esto crea una mezcla donde la música es el elemento principal pero la ambientación del mundo se escucha sutilmente.

### Paso 8: Exportación

1. Toca **Export** (esquina superior derecha).
2. Configuración de exportación:

| Ajuste | Valor |
| :--- | :--- |
| **Resolution** | 1080p (o 2K si lo soporta) |
| **Frame rate** | 30fps |
| **Quality** | High / Best |
| **Format** | MP4 |
| **Bitrate** | Auto o High |

3. Toca **Export** y espera.

---

## Timeline Visual (referencia rápida)

```
0s    5s    10s   14s   18s   22s   25s   30s   34s   39s   43s
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
|Mar  |Wilfr|Univ |Elara|Kiri |Silv |Fant |Port |Bosq |Outro|
|Nubes|ed   |erse |     |     |io   |asma |al   |Cósm |     |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
BGM:  suave→construye→dip→tensión→EXPLOTA→PICO→fade out
Vol:  60%  70%  70%  75%  75%  50%  65%  95%  100% 40%
Cortes: SECO SECO SECO SECO SECO SECO SECO DISSOLVE FADE
```

---

## Checklist Final

- [ ] Todos los clips importados en orden correcto
- [ ] Duraciones ajustadas (total ~43s)
- [ ] BGM colocada y alineada con el inicio
- [ ] Volumen de BGM ajustado por sección (dip en Silvio, pico en Portal/Bosque)
- [ ] Fade out en el último clip
- [ ] Transición dissolve entre Portal y Bosque Cósmico
- [ ] Audio original de clips al 10-30%
- [ ] Color grading consistente aplicado a todos los clips
- [ ] Exportado en 1080p, 30fps, MP4
- [ ] Revisado en pantalla completa antes de publicar
