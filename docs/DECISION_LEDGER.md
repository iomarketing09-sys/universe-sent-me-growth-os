# Decision Ledger — contrato de decisión por apuesta

**Estado:** Activo
**Creado:** 2026-11-05
**Dueño operativo:** CGO
**Aprueba:** Fernando para `L2` y `L3`
**Protocolo formal relacionado:** `Operations/Research/2026-08-17_Protocolo_P0_Metricas_y_Veredictos.md`
**Ledgers relacionados:** `tenants/<tenant>/experiments/hypothesis_bank.csv`, `tenants/<tenant>/experiment_log.csv`, `tenants/<tenant>/metrics/metrics_snapshot_log.csv`

---

## 1. Para qué existe

El protocolo P0 sirve para auditar y cerrar veredictos formales. No sirve como
cadencia diaria de aprendizaje: exige cinco publicaciones comparables, ventanas
exactas y una celda bien definida. En contenido orgánico eso deja demasiadas
observaciones en `Inconclusa`.

El Decision Ledger separa tres cosas que P0 mezcla:

1. **Observación:** lo que pasó en una o dos piezas.
2. **Señal:** un patrón preliminar en una celda pequeña.
3. **Decisión:** un cambio operativo con evidencia suficiente y aprobación.

No reemplaza P0. Lo usa como capa de auditoría y agrega una cadencia operativa
para decidir sin fingir causalidad.

---

## 2. Principios

- **La unidad es la apuesta, no la publicación.** Una apuesta es una hipótesis
  con una métrica principal, un umbral y una fecha de expiración.
- **Pre-registrar antes de publicar.** La regla de decisión se escribe antes de
  ver resultados. Si se escribe después, se marca `pre_registered: false` y no
  cuenta como pre-registro.
- **Una métrica principal y máximo dos guardrails.** Más métricas aumentan
  falsos positivos y paralizan la decisión.
- **Ningún veredicto sale de lifetime ni de una sola pieza.**
- **Ningún lenguaje causal sin control o aleatorización.** Una comparación
  descriptiva no demuestra que el personaje, el copy o la hora causaron el
  resultado.
- **Intelligence calcula; CGO interpreta y propone; Fernando aprueba `L2/L3`.**
- **P0 sigue siendo la fuente de verdad para `Validada` y `No validada`.**

---

## 3. Escalera de evidencia

| Nivel | Mínimo | Qué permite | Quién cierra |
|---|---|---|---|
| `L0 Observación` | 1–2 piezas, o muestra no comparable | Actualizar la hipótesis y el siguiente test. No hay veredicto. | CGO registra |
| `L1 Señal` | 3–4 comparables, o una celda limpia con dirección consistente | Ajustar la siguiente prueba. No cambia estrategia, calendario ni copy de forma permanente. | CGO registra |
| `L2 Decisión operativa` | 5+ comparables, ventana exacta, guardrails limpios y efecto que cumple el umbral pre-registrado | Cambiar calendario, copy, formato o asignación. | CGO redacta Decision Card; Fernando aprueba |
| `L3 Regla` | `L2` replicado en otro ciclo, tenant o cohorte independiente | Convertirlo en default operativo. | Fernando aprueba; canon sigue su propio gate |

### Qué cuenta como "comparable"

Mismo canal, mismo formato, misma condición nuevo/reuse, misma banda horaria,
misma familia de contenido y misma ventana temporal. Si falta una de estas
condiciones, el máximo nivel posible es `L1`.

---

## 4. Decision Card

Cada `L2` o `L3` necesita una tarjeta en
`docs/decision_cards/YYYY-MM-DD_<hypothesis_id>.md`.

| Campo | Obligatorio | Descripción |
|---|---|---|
| `card_id` | Sí | Identificador único de la tarjeta |
| `hypothesis_id` | Sí | Enlace al `hypothesis_bank.csv` |
| `tenant` | Sí | Tenant y plataforma |
| `owner` | Sí | Quién redacta la tarjeta |
| `status` | Sí | `draft`, `approved`, `rejected`, `expired` |
| `created_at` | Sí | Fecha de creación |
| `pre_registered` | Sí | `true` solo si se escribió antes de publicar |
| `decision_question` | Sí | Una pregunta decidible |
| `primary_metric` | Sí | Fórmula exacta y ventana |
| `guardrails` | Sí | Máximo dos |
| `threshold` | Sí | Qué número cambia la decisión |
| `min_n` | Sí | Mínimo de piezas comparables |
| `cell_definition` | Sí | Canal, formato, tipo, horario, familia |
| `decision_rule` | Sí | Adoptar / descartar / repetir |
| `expires_at` | Sí | Cuándo se cierra aunque no haya decisión |
| `data_sources` | Sí | Ledgers y consultas usadas |
| `limitations` | Sí | Qué no permite concluir |
| `evidence_level` | Sí | `L0` a `L3` |
| `recommendation` | Sí | Acción propuesta, no ejecutada |
| `approver` | Para `L2/L3` | Fernando |

### Regla de decisión recomendada

> Si la mediana de `[métrica]` es `>= [umbral de adopción]`, al menos
> `[k/n]` piezas superan `[piso operativo]` y los guardrails pasan, se adopta.
> Si la mediana es `<= [umbral de descarte]` o falla un guardrail, se descarta.
> En cualquier otro caso, se repite con `[n]` piezas comparables más.

Para muestras pequeñas, usar bootstrap o probabilidad de superar el umbral como
apoyo exploratorio. No usar un p-value aislado como única puerta.

---

## 5. Guardrails

Elegir como máximo dos por tarjeta:

- **Marca y canon:** cero bloqueos de canon; ninguna pieza publicada sin
  aprobación.
- **Piso de interacción:** la mediana de interacciones no cae más de 20%
  frente al baseline comparable.
- **Conversación:** no se desploma el volumen de comentarios; los comentarios
  sensibles siguen en revisión humana.
- **Costo y cadencia:** la prueba no rompe la producción ni el calendario.
- **Integridad del dato:** ventana exacta, métrica definida y cero valores
  inventados.

Un guardrail no es una métrica objetivo. Sirve para vetar una decisión, no para
justificarla.

---

## 6. Relación con P0

| P0 | Decision Ledger | Lectura |
|---|---|---|
| `Validada` | `L3` | Regla replicada y aprobada |
| `Parcialmente validada` | `L2` | Decisión operativa, todavía no regla |
| `Inconclusa` | `L0` o `L1` | Falta comparabilidad o muestra |
| `No validada` | `L2` negativa | Solo si la celda era comparable |
| `Invalidada por diseño` | Cualquier nivel | La prueba no respetó la condición |

La equivalencia es orientativa. Una tarjeta puede ser `L2` operativa sin ser un
`Validada` de P0. Para declarar una regla formal siguen aplicando los cinco
comparables y la revisión de P0.

---

## 7. Cadencia operativa

1. **Antes de publicar:** escribir la tarjeta con `pre_registered: true`,
   métrica, umbral, `min_n`, guardrails y fecha de expiración.
2. **Después de E24:** registrar la observación en `experiment_log.csv`. La
   tarjeta no sube de nivel por tener un buen resultado aislado.
3. **Revisión semanal:** el CGO separa `L0/L1` de `L2/L3`. Solo las tarjetas
   `L2/L3` van a Fernando.
4. **Después de la decisión:** actualizar `hypothesis_bank.csv` solo con la
   aprobación correspondiente. La tarjeta queda como evidencia.
5. **Al expirar:** cerrar como `expired` si no se alcanzó `min_n`; no dejar una
   tarjeta abierta indefinidamente.

---

## 8. Qué no hacer

- No llamar "validado" a un post viral.
- No cambiar estrategia desde una sola pieza.
- No escribir una tarjeta después de ver datos y llamarla pre-registrada.
- No mezclar Facebook con Instagram, nuevo con reuse, o formatos distintos.
- No usar lifetime como si fuera E24/E72.
- No permitir que Intelligence escriba veredictos.
- No crear un sistema paralelo: el Decision Ledger es un contrato sobre los
  ledgers existentes.

---

## 9. Ejemplo real

- `docs/decision_cards/2026-11-05_HB-UNI-003.md` — tarjeta retrospectiva sobre
  humor de Universe y share rate. Sirve para probar el formato, no como
  pre-registro.
