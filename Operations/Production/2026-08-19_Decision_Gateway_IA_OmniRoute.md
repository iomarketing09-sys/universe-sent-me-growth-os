# Decisión de arquitectura: evaluación de OmniRoute como gateway de IA

**Propósito:** Determinar si Universe Sent Me puede usar OmniRoute para capacidades de IA dentro del dashboard social o de futuros flujos internos, preservando seguridad de credenciales, privacidad de datos, trazabilidad analítica y separación entre inferencia de IA y actualización de métricas.

**Estado:** Review

**Fecha de creación:** 2026-08-19

**Última actualización:** 2026-08-19

**Versión:** 1.0

**Autor:** Manus AI

**Documentos relacionados:** `2026-08-19_Actualizacion_Asistida_Dashboard_Social.md`, `../../GrowthOS/08_00_Metricas_Baseline_Plataformas.md`, `../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md`, `../../GrowthOS/00_01_Changelog_GrowthOS.md`.

---

## Resumen de la decisión

**Sí, OmniRoute puede usarse en Universe Sent Me**, pero no debe instalarse como una dependencia del frontend actual ni llamarse directamente desde el navegador. OmniRoute es un gateway de IA autoalojable, de licencia MIT y compatible con una superficie de API tipo OpenAI; centraliza proveedores y admite selección/fallback de modelos. [1] [2]

El dashboard social actual es una interfaz React estática que calcula visualizaciones desde un dataset versionado y no contiene llamadas a modelos de IA. Por tanto, integrar OmniRoute sin una necesidad concreta solo añadirá infraestructura, superficie de ataque y mantenimiento. La integración queda **condicionada a un caso de uso explícito, acotado y verificable**; por ejemplo, redactar una lectura estratégica basada exclusivamente en un corte de métricas ya normalizado.

> OmniRoute es un componente opcional de **inferencia**, no una fuente de datos ni un reemplazo del procedimiento de actualización asistida del dashboard.

## Compatibilidad con el proyecto actual

| Aspecto | Situación actual | Implicación de OmniRoute | Decisión |
|---|---|---|---|
| Dashboard | Frontend React estático; los cálculos y filtros viven en cliente. | No hay un lugar seguro para guardar secretos ni realizar llamadas de servidor a servidor. | No conectar el navegador directamente al gateway. |
| Credenciales | Las claves de proveedores y de OmniRoute son sensibles. | Una clave enviada al navegador puede ser extraída y reutilizada por terceros. | Guardarlas solo en un servicio backend o gateway controlado. |
| Datos de métricas | La evidencia se conserva con fuente, ventana, normalización y versión. | Una IA puede resumir la evidencia, pero no debe modificarla ni convertirse en fuente analítica canónica. | Mantener GitHub y los artefactos normalizados como fuente de verdad. |
| Actualización Windsor | El flujo vigente es asistido, bajo solicitud y sin proceso permanente. | OmniRoute no aporta valor a la extracción, deduplicación ni cálculo de métricas deterministas. | No incorporarlo al pipeline de extracción de datos. |
| Infraestructura | OmniRoute opera como servicio persistente con su propia base SQLite, credenciales y dashboard administrativo. | Requiere un entorno separado del hosting estático actual. [3] [6] | Aislarlo en un servicio dedicado si se aprueba. |

## Arquitectura permitida

La arquitectura segura para una futura función de IA es la siguiente:

```text
Dashboard web → endpoint privado del backend de Universe Sent Me → OmniRoute → proveedor de modelo
                              ↓
                    dataset normalizado y versionado
```

El navegador solo debe enviar una solicitud de producto mínima al backend de Universe Sent Me. El backend valida el usuario, selecciona la evidencia permitida, elimina campos no necesarios, aplica límites y llama a OmniRoute usando una clave mantenida fuera del cliente. El resultado debe etiquetarse como **análisis asistido por IA**, incluir las fuentes del corte y no escribir de vuelta en los datos canónicos sin revisión humana.

La ruta inversa —navegador → OmniRoute— queda descartada. Aunque OmniRoute documenta controles CORS, la API de inferencia está protegida mediante claves Bearer o `x-api-key`; una aplicación cliente no puede mantener tales secretos. [4]

## Capacidades que sí podrían justificarlo

| Caso de uso propuesto | Valor potencial | Guardrails necesarios | Estado |
|---|---|---|---|
| Lectura narrativa de un corte ya normalizado | Convertir métricas, hipótesis y límites de comparabilidad en un borrador de insight para revisión. | Usar solo artefactos aprobados; mostrar fuentes y ventana; impedir que la IA altere el baseline. | Candidato prioritario. |
| Clasificación asistida de contenidos | Sugerir personaje, formato o tema para filas nuevas antes de su validación. | Resultado como propuesta; revisión humana; conservar el input y la decisión final. | Candidato secundario. |
| Generación de copys o variantes | Acelerar borradores creativos del estudio. | Mantener aprobación editorial y reglas de voz de personajes fuera del gateway. | Fuera del alcance del dashboard actual. |
| Extracción de Windsor, normalización o cálculo de retorno | Ningún beneficio material; son pasos deterministas y con requisitos de trazabilidad. | No aplicable. | No usar OmniRoute. |

## Opciones de implementación

No se selecciona una ruta de forma automática. La elección depende de si el estudio quiere solamente un piloto de análisis asistido o una capa de IA multi-proveedor administrada a largo plazo.

| Enfoque | Qué habilita | Tradeoffs | Coste | Complejidad de preparación |
|---|---|---|---|---|
| Backend del dashboard con un proveedor directo | Un piloto estrecho, por ejemplo una lectura estratégica con un único modelo. | Menos flexibilidad y sin fallback multi-proveedor, pero menor superficie operativa. | Variable según el proveedor; no requiere alojar un gateway adicional. | Media. |
| OmniRoute autoalojado y un backend del dashboard como cliente | Un endpoint compatible con OpenAI, routing/fallback entre proveedores y control central de claves. [1] [2] | Requiere servicio separado, actualizaciones, backups, observabilidad y una política de proveedores. | Software MIT; infraestructura y consumo de proveedores son aparte. [1] | Alta. |
| Uso local de OmniRoute para herramientas creativas internas | Beneficio individual para IDEs y pruebas, sin exponer un endpoint de producción. | La máquina debe estar disponible y no integra una función compartida en el dashboard. | Bajo o nulo para la infraestructura local; depende de los proveedores usados. | Baja. |

## Requisitos de operación y seguridad si se aprueba OmniRoute

La guía de despliegue del proyecto recomienda una VM con al menos 1 vCPU, 1 GB de RAM, Docker y almacenamiento persistente; el mismo documento describe SQLite y un volumen de datos para la aplicación. [3] El servicio debe quedar separado del dashboard estático. No se debe intentar empaquetarlo dentro de la aplicación React ni depender de un runtime efímero para conservar sus credenciales, configuración y base de datos.

| Control | Requisito operativo |
|---|---|
| Aislamiento | Exponer únicamente el endpoint de inferencia que requiera el backend. Mantener la administración, rutas locales y herramientas que ejecutan procesos fuera del acceso público. [5] |
| Secretos | Usar valores únicos para `JWT_SECRET`, `API_KEY_SECRET`, contraseña inicial, secreto del bridge y cifrado de almacenamiento cuando corresponda. Nunca versionar `.env` con secretos. [3] [6] |
| Navegador y CORS | Permitir solo el dominio exacto que corresponda, nunca usar CORS abierto en producción y no inyectar cabeceras CORS duplicadas desde un proxy. [4] |
| Privacidad | Configurar retención de logs; para tráfico sensible usar una clave con la opción de no registrar solicitudes cuando aplique. La documentación indica que las acciones administrativas y cambios de proveedores se auditan por separado. [7] |
| Cadena de suministro | Fijar una versión evaluada o digest de imagen, revisar SBOM/CVE en cada actualización y tratar todo cambio de versión como cambio operativo. El repositorio declara controles de procedencia, SBOM y escaneo de vulnerabilidades, pero esos controles no sustituyen la revisión del operador. [8] |
| Datos enviados | No enviar tokens, credenciales de redes sociales, archivos crudos innecesarios ni datos personales. Construir un payload mínimo desde el dataset normalizado y documentar la ventana de datos utilizada. |
| Gobernanza | Restringir proveedores aprobados, presupuesto, modelos permitidos, límites de solicitud y responsables de cambios antes de habilitarlo para un flujo compartido. |

## Límites que permanecen vigentes

El procedimiento `2026-08-19_Actualizacion_Asistida_Dashboard_Social.md` se mantiene **sin cambios**. Su afirmación de que el refresco de métricas no requiere un servicio permanente sigue siendo correcta: OmniRoute no es necesario para pedir cortes a Windsor, normalizar datos, calcular métricas ni versionar evidencia.

Si se adopta una función de IA, debe actualizarse ese procedimiento para añadir una etapa posterior y opcional de “análisis asistido”, sin cambiar las etapas de extracción, normalización, control, retorno, interfaz y versionado. También requerirá actualizar `GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md` para declarar que las respuestas de IA son derivados revisables, no evidencia maestra.

## Próximo punto de decisión

Antes de implementar, Fernando debe definir el primer caso de uso: **lectura estratégica de datos, clasificación de contenido o generación creativa**. Con esa decisión se podrá elegir entre un piloto con proveedor directo, OmniRoute autoalojado como gateway compartido o uso local para herramientas internas. No se deben instalar paquetes, activar un servicio ni mover credenciales hasta entonces.

## Referencias

[1]: [OmniRoute — repositorio oficial y licencia MIT](https://github.com/diegosouzapw/OmniRoute)

[2]: [OmniRoute — guía oficial de inicio rápido](https://raw.githubusercontent.com/diegosouzapw/OmniRoute/release/v3.8.50/docs/getting-started/QUICK-START.md)

[3]: [OmniRoute — guía oficial de despliegue en VM](https://raw.githubusercontent.com/diegosouzapw/OmniRoute/release/v3.8.50/docs/ops/VM_DEPLOYMENT_GUIDE.md)

[4]: [OmniRoute — configuración CORS y seguridad](https://raw.githubusercontent.com/diegosouzapw/OmniRoute/release/v3.8.50/docs/security/CORS.md)

[5]: [OmniRoute — niveles de protección de rutas](https://raw.githubusercontent.com/diegosouzapw/OmniRoute/release/v3.8.50/docs/security/ROUTE_GUARD_TIERS.md)

[6]: [OmniRoute — referencia de variables de entorno](https://raw.githubusercontent.com/diegosouzapw/OmniRoute/release/v3.8.50/docs/reference/ENVIRONMENT.md)

[7]: [OmniRoute — cumplimiento y auditoría](https://raw.githubusercontent.com/diegosouzapw/OmniRoute/release/v3.8.50/docs/security/COMPLIANCE.md)

[8]: [OmniRoute — controles de cadena de suministro](https://raw.githubusercontent.com/diegosouzapw/OmniRoute/release/v3.8.50/docs/security/SUPPLY_CHAIN.md)
