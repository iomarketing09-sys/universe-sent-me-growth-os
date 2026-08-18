# Estrategia de Monetización: Mercado Libre Afiliados — Growth OS

**Propósito:** Definir el marco operativo para capitalizar la afiliación de Mercado Libre a través de contenido narrativo y la sección recurrente "¿Qué me llegó?".
**Estado:** Active
**Fecha de creación:** 2026-08-05
**Última actualización:** 2026-08-19
**Versión:** 1.2
**Autor:** Manus AI (CGO)
**Documentos relacionados:** `01_02_Content_Backlog.md`, `07_00_Registro_Maestro_Reels.md`, `08_00_Metricas_Baseline_Plataformas.md`

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

El siguiente paso es reemplazar la etiqueta agregada por etiquetas separadas para cada nueva superficie de Facebook. El Reel de Elara y cualquier comentario aprobado deben usar identificadores distintos. No se considerarán conversiones ni comisiones confirmadas hasta conciliar los reportes de Mercado Libre, respetar la ventana de atribución de 24 horas y distinguir ventas brutas de ventas aprobadas. La evidencia está documentada en `Operations/Research/2026-08-19_MercadoLibre_Facebook_Afiliados_Observacion.md`.

## Historial de Versiones
| Fecha | Versión | Cambio | Autor |
|---|---|---|---|
| 2026-08-05 | 1.0 | Creación de la estrategia inicial de monetización ML. | Manus AI (CGO) |
| 2026-08-15 | 1.1 | Se elimina la referencia operativa a Make; el flujo vigente queda en Manus + Meta Graph API. | Manus AI (CGO) |
| 2026-08-19 | 1.2 | Se añade tracking por etiquetas nativas de Mercado Libre, ledger de enlaces y piloto de atribución para el Reel de Elara. | Manus AI (CGO) |
