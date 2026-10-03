# Estrategia de Monetización: Mercado Libre Afiliados — Growth OS

**Propósito:** Definir el marco operativo para capitalizar la afiliación de Mercado Libre a través de contenido narrativo y la sección recurrente "¿Qué me llegó?".
**Estado:** Active
**Fecha de creación:** 2026-08-05
**Última actualización:** 2026-08-22
**Versión:** 1.8
**Autor:** Manus AI (CGO)
**Documentos relacionados:** `01_02_Content_Backlog.md`, `07_00_Registro_Maestro_Reels.md`, `08_00_Metricas_Baseline_Plataformas.md`, `Operations/Production/2026-08-19_Playbook_Tracking_Afiliados_MercadoLibre.md`, `Operations/Production/12_00_Catalogo_Productos_MercadoLibre.md`, `Operations/Production/2026-08-20_Segunda_Capa_Afiliados_Posts_Ganadores.md`, `Operations/Research/Affiliate_Link_Ledger.csv`, `Operations/Research/Affiliate_Metrics_Snapshots.csv`, `Operations/Research/2026-08-19_Auditoria_Reels_y_Monetizacion.md`

---

## 1. Visión Estratégica
La integración de Mercado Libre no debe ser vista como publicidad tradicional, sino como una **extensión de la narrativa de Universe Sent Me**. Los productos que "llegan" al universo son artefactos que interactúan con nuestros personajes, generando valor de entretenimiento mientras se incentiva la compra.

## 2. El Formato: "¿Qué me llegó?" (Reimagined)
Transformaremos el unboxing tradicional en una pieza de **Story-Commerce** utilizando el pipeline de IA (Flow/Higgsfield).

### Pilares del Formato:
| Personaje | Rol en la Reseña | Tono / Ángulo |
| :--- | :--- | :--- |
| **Wilfred** | El Crítico Sabio | Analiza la utilidad del producto desde una perspectiva filosófica o de supervivencia en el bosque. Humor seco. |
| **Universe** | El Juez Supremo | Un gato con gafas que decide si el producto es "digno" o simplemente una distracción. |
| **Elara** | La Lectora de Energías | Evalúa el producto según su "vibración" o utilidad para rituales modernos/astrología. |
| **Silvio** | El Caos | Uso absurdo o incorrecto del producto para generar humor visual. |

## 3. Embudos de Conversión (Funnels)

### A. Facebook Reels (Canal Principal)
- **Gancho:** El paquete de Mercado Libre apareciendo en un entorno fantástico.
- **CTA:** "Link en el primer comentario" o "Escribe INFO para enviarte el link". La gestión se realizará mediante el flujo de Manus y Meta Graph API cuando los permisos lo permitan.
- **Monetización:** Comisión por venta + Bonos por visualizaciones (si aplica).

### B. Mercado Libre Clips
- **Acción:** Subir las piezas de "¿Qué me llegó?" directamente a la sección de Clips de Mercado Libre.
- **Ventaja:** Tráfico con alta intención de compra y visibilidad nativa en el marketplace.

### C. Instagram Stories / Link en Bio
- Uso de **Colecciones de Mercado Libre** organizadas por personaje (ej: "Los favoritos de Wilfred").

## 4. Operativa de Producción (Pipeline)
1. **Selección de Producto:** Basado en tendencias de búsqueda en Mercado Libre o productos que encajen con el Canon.
2. **Scripting:** Breve (15-30s). El producto debe causar una reacción en el personaje.
3. **Generación IA:** Uso de Flow para la interacción personaje-objeto.
4. **Publicación Cascada:** FB -> IG -> TT -> YT -> ML Clips.

## 5. KPIs y Métricas de Éxito
Se integrarán en el `08_00_Metricas_Baseline_Plataformas.md`:
- **CTR (Click-Through Rate):** Clics en el link de afiliado / Visualizaciones.
- **Conversion Rate:** Ventas realizadas / Clics.
- **AOV (Average Order Value):** Ticket promedio de las recomendaciones.
- **Ingreso por Mil (RPM) Afiliado:** Ingresos totales / (Vistas / 1000).

## 6. Próximos Pasos (Q3 2026)
- [ ] Activar automatización de comentarios en Facebook para links de afiliados.
- [ ] Crear la primera "Lista de Favoritos de Universe" en Mercado Libre.
- [ ] Producir el primer Reel de Wilfred recibiendo un producto de tecnología "humana".

---
## 6. Tracking de atribución y estado operativo

La estrategia conserva dos carriles separados: **monetización nativa de Meta**, todavía no verificada para la página, y **afiliación de Mercado Libre**, que puede probarse mediante links etiquetados. El procedimiento operativo, la nomenclatura de etiquetas y las reglas de conciliación están en `Operations/Production/2026-08-19_Playbook_Tracking_Afiliados_MercadoLibre.md`; los registros se almacenan en `Operations/Research/Affiliate_Link_Ledger.csv`.

El primer piloto recomendado es el Reel de la lámpara de luna de Elara. La primera observación del panel de Mercado Libre, para el periodo 4–18 de agosto, muestra una etiqueta agregada `Links de facebook - universesentme` con 3 clics, 2 unidades vendidas, $322.65 MXN en ventas brutas y $28.84 MXN de comisión estimada. Ambas ventas están `En revisión`, por lo que esta señal es comercialmente positiva pero todavía no es comisión confirmada ni atribución específica al Reel de Elara. El panel reporta además una incidencia de datos para los días 16 y 17 de agosto.

El siguiente paso es mantener etiquetas separadas por publicación y superficie. El Reel de Elara y cualquier comentario aprobado deben usar identificadores distintos. No se considerarán conversiones ni comisiones confirmadas hasta conciliar los reportes de Mercado Libre, respetar la ventana de atribución de 24 horas y distinguir ventas brutas de ventas aprobadas. La evidencia histórica está documentada en `Operations/Research/2026-08-19_MercadoLibre_Facebook_Afiliados_Observacion.md`; el corte manual reciente está en `Affiliate_Metrics_Snapshots.csv`.

Para la ola del 18–30 quedó activo un piloto de **10 oportunidades**, sin modificar el P0 editorial. Cada publicación afiliada tiene un producto, una etiqueta y un link únicos. La identidad se registra en `Affiliate_Link_Ledger.csv` y cada corte de métricas se añade a `Affiliate_Metrics_Snapshots.csv`. Fernando confirmó que los diez productos/links fueron publicados o adjuntados en Facebook; las horas e IDs nativos individuales que no fueron capturados permanecen como deuda de conciliación, no como publicaciones pendientes.

## Segunda capa de monetización

La estrategia tendrá dos carriles afiliados: el piloto planificado de 10 publicaciones y una segunda capa posterior a publicación para posts con rendimiento orgánico superior. La segunda capa no debe adjuntar productos a todos los posts exitosos; debe usar un pequeño grupo de candidatos y conservar al menos un control descriptivo sin producto.

La primera campaña activa es `USM-AFF-FB-WINNERS-202608`. La primera ola quedó activada manualmente en dos publicaciones: `2608029` / Wilfred con `usmwin2608029w0820`, y `CNT-034 / 260539` / Evan+Kiri con `usmwin260539ek0820`. Cada candidato usa producto, link y etiqueta distintos de la capa 1. Los resultados se registrarán en `Affiliate_Metrics_Snapshots.csv` sin mezclarlos con las métricas editoriales de P0/P1. La hora exacta y los IDs nativos individuales permanecen pendientes de conciliación.

---

## 7. Revisión CGO — ajuste para próximos contenidos afiliados

### 7.1 Diagnóstico al 22 de agosto

El carril ya está **activado**, pero aún no está comercialmente validado. Existen diez oportunidades de Capa 1 confirmadas por el operador, un Reel adicional de Universe con producto nativo, dos adjunciones de Capa 2 y una publicación de Universe/Senales con superficies separadas. La activación de links o productos no debe confundirse con conversión.

| Evidencia disponible | Lectura correcta | Límite para decidir |
|---|---|---|
| Etiqueta histórica agregada: 3 clics, 2 unidades en revisión, $322.65 MXN brutos y $28.84 MXN de comisión estimada | Existió una señal comercial histórica de Facebook. | No permite atribuir resultado a un post o producto; no hay comisión confirmada. |
| Corte manual del 20 de agosto: 2 clics visibles, 0 unidades y $0 de ventas/ganancias | El tracking puede registrar interés. | La muestra no permite evaluar personaje, producto, CTA o superficie. |
| AFF-07: un clic granular visible, sin unidades | Es la única actividad granular identificable en el corte. | Un clic no constituye un ganador ni justifica escalar. |
| Cartera activa con horas, IDs o permalinks incompletos | Hay ejecución operativa, pero conciliación desigual. | No se puede comparar de forma limpia timing, asset o superficie. |

> **Decisión CGO:** no ampliar el número de piezas afiliadas todavía. Primero se cierra una medición comparable sobre la cartera activa; después se propone una única nueva prueba comercial con un producto narrativamente necesario.

### 7.2 Cartera y límite de exposición

| Carril | Objetivo | Regla de producto | Estado actual |
|---|---|---|---|
| **Editorial puro** | Aprender hooks, personajes, retención y compartibilidad. Incluye MPM y videoclips/fashion films. | Sin afiliación, producto ni pauta. | Continúa sin restricciones comerciales. |
| **Capa 1 existente** | Medir las oportunidades planificadas y el Reel ya activado. | No añadir un CTA comercial nuevo al mismo contenido. | Conciliación pendiente. |
| **Capa 2 existente** | Comprobar si una adjunción posterior encaja con ganadores orgánicos. | Dos adjunciones con un control sin producto. | Conciliación pendiente. |
| **Nueva producción Story-Commerce** | Crear una historia nacida de un objeto específico. | Un producto, una superficie y una pregunta comercial. | Pausada hasta superar el gate. |

Como protección de audiencia y aprendizaje, una vez que el gate se supere, la salida nueva no excederá **una pieza afiliada por cada cuatro piezas editoriales listas para publicar**. La proporción limita exposición; no predice conversiones.

### 7.3 Gate antes de crear la próxima pieza comercial

No se generará un nuevo link, producto ni concepto comercial hasta completar estas condiciones para las publicaciones activas:

1. Conciliar, donde exista evidencia, `Publication_Local` o `Native_Product_Attached_At`, ID/permalink, producto y superficie real. Una captura y permalink sustituyen al ID técnico si Facebook no lo expone.
2. Añadir los cortes de 24 horas, 48 horas y 7 días de cada etiqueta visible. Si el panel no muestra una etiqueta, el estado es `Not_Visible_No_Inference`, no cero.
3. Mantener separados clics, ventas brutas, ventas aprobadas, unidades, comisión estimada y comisión confirmada.
4. Reunir como mínimo **tres etiquetas comparables con corte visible**, idealmente una de Capa 2, antes de escoger un personaje, producto o CTA para una nueva prueba. Si no se llega a tres, la expansión permanece en pausa.
5. Para Capa 2, conservar snapshot editorial pre y post-adjunción para no atribuir a un producto una variación orgánica sin control.

### 7.4 Política de superficies para contenido nuevo

| Plataforma / superficie | Decisión | Control |
|---|---|---|
| Facebook / `FACEBOOK_NATIVE_PRODUCT` | Es la prioridad comercial cuando la adjunción pueda verse y documentarse. | Etiqueta exclusiva, evidencia de adjunción, permalink y hora. |
| Facebook / comentario aprobado | Solo como alternativa experimental si no hay producto nativo. | Link distinto; no coexistir con producto nativo en el mismo post. |
| Instagram Reel | No crear nuevas piezas con URL escrita en copy o texto si no hay ruta clicable y medible. | El caso histórico Universe/Senales se conserva y se mide aparte; no se corrige retroactivamente. |
| TikTok y YouTube | Mantener en espera hasta verificar superficie funcional y trazable. | Los links reservados no deben tratarse como adjunción nativa. |

### 7.5 Criterio creativo posterior al gate

La siguiente pieza deberá partir de **historia → personaje → producto**. El objeto solo entra si permite gancho visual, reacción de personaje y payoff sin que el video deje de funcionar al retirarlo. Antes de aprobarlo se verifican encaje de personaje, ticket impulsivo, ficha vigente, stock/envío y superficie de compra funcional. El catálogo queda como banco creativo, no como una cola automática de producción.

La próxima revisión debe ser un corte de métricas y producir una de tres decisiones: continuar una superficie, ajustar **una** variable —producto, personaje o CTA— o mantener la pausa. No se modifican `Affiliate_Link_Ledger.csv`, `Affiliate_Metrics_Snapshots.csv` ni el backlog en esta revisión porque no hay nuevo link aprobado, nueva métrica o nueva pieza comercial autorizada.

## Historial de Versiones
| Fecha | Versión | Cambio | Autor |
|---|---|---|---|
| 2026-08-05 | 1.0 | Creación de la estrategia inicial de monetización ML. | Manus AI (CGO) |
| 2026-08-15 | 1.1 | Se elimina la referencia operativa a Make; el flujo vigente queda en Manus + Meta Graph API. | Manus AI (CGO) |
| 2026-08-19 | 1.2 | Se añade tracking por etiquetas nativas de Mercado Libre, ledger de enlaces y piloto de atribución para el Reel de Elara. | Manus AI (CGO) |
| 2026-08-19 | 1.3 | Se define el piloto Facebook 18–30 con cuatro-seis publicaciones, etiquetas por post/producto/superficie y snapshots append-only. | Manus AI (CGO) |
| 2026-08-20 | 1.4 | Se corrige el alcance a 10 oportunidades activas y se separa la activación comercial de la medición pendiente; se registra el Reel `2210896633022235` con producto nativo. | Manus AI (CGO) |
| 2026-08-20 | 1.5 | Se incorpora el snapshot manual: 2 clics, 0 unidades y $0 de comisión en el periodo visible; AFF-07 concentra el único clic granular visible y el Reel queda sin inferencia por etiqueta no visible. | Manus AI (CGO) |
| 2026-08-20 | 1.6 | Se añade la segunda capa de monetización para posts ganadores, con campaña independiente, máximo tres candidatos iniciales y filtro de encaje editorial. | Manus AI (CGO) |
| 2026-08-20 | 1.7 | Se activa manualmente la primera ola de Capa 2 en `2608029` y `CNT-034 / 260539`, con dos productos nativos confirmados y tracking separado. | Manus AI (CGO) |
| 2026-08-22 | 1.8 | Revisión CGO: se pausa la expansión hasta conciliar la cartera activa; se separan carriles editoriales/comerciales y se priorizan superficies clicables y verificables. | Manus AI (CGO) |
