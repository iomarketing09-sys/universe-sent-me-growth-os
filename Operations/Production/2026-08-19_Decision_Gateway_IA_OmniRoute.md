# Decisión: uso de OmniRoute como gateway de IA

**Propósito:** Determinar si Universe Sent Me puede utilizar OmniRoute para capacidades de IA dentro del dashboard social, herramientas creativas o futuros flujos internos, preservando la seguridad de credenciales, la privacidad de datos, la trazabilidad analítica y la separación entre inferencia de IA y actualización de métricas.

**Estado:** Review

**Fecha de creación:** 2026-08-19

**Última actualización:** 2026-08-23

**Versión:** 2.7

**Autor:** Manus AI

**Organización:** `Operations/Production`

**Documentos relacionados:** [`2026-08-18_Piloto_Local_OmniRoute_Seguro.md`](2026-08-18_Piloto_Local_OmniRoute_Seguro.md), [`2026-08-19_Actualizacion_Asistida_Dashboard_Social.md`](2026-08-19_Actualizacion_Asistida_Dashboard_Social.md), [`../../GrowthOS/08_00_Metricas_Baseline_Plataformas.md`](../../GrowthOS/08_00_Metricas_Baseline_Plataformas.md), [`../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md`](../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md), [`../../GrowthOS/00_01_Changelog_GrowthOS.md`](../../GrowthOS/00_01_Changelog_GrowthOS.md).

---

## Respuesta corta

**Sí, se puede usar OmniRoute en Universe Sent Me**, pero la recomendación depende del lugar donde se quiera usar:

| Escenario | Recomendación actual | Motivo |
|---|---|---|
| Piloto en una computadora de baja potencia | **Sí, cloud-first** | OmniRoute actúa solo como gateway ligero en `127.0.0.1`; la inferencia ocurre en un provider cloud con API oficial. Si el gateway ralentiza el equipo, se usa directamente el Playground o API del provider. |
| Uso local para probar modelos, redactar borradores o conectar herramientas creativas | **Sí, si el equipo lo soporta** | Puede centralizar providers sin exponer credenciales en el navegador, pero la inferencia local con Ollama se pospone por consumo de RAM, CPU, GPU y almacenamiento. [1] [2] |
| Función compartida del dashboard social | **Sí, pero solo mediante backend y servicio separado** | El frontend actual no debe guardar secretos ni llamar directamente a proveedores o a OmniRoute. |
| Extracción de Windsor, normalización, deduplicación o cálculo de métricas | **No** | Son procesos deterministas que requieren trazabilidad y ya están definidos en el flujo de actualización asistida. |
| Exponer OmniRoute públicamente sin autenticación, límites ni revisión de proveedores | **No** | Amplía la superficie de ataque, puede filtrar datos y puede incumplir los términos de determinados proveedores o niveles gratuitos. [3] [6] |

> **Decisión:** OmniRoute queda aprobado como **gateway local de bajo consumo conectado a un único provider cloud oficial**, siempre que el equipo lo soporte. La inferencia local mediante Ollama queda pospuesta. Si OmniRoute ralentiza la computadora, el piloto debe ejecutarse directamente en el Playground o API del provider. No se instala como dependencia del dashboard ni se activa un servicio de producción hasta que Fernando defina el primer caso de uso y se aprueben los controles operativos.

## Qué es y qué aporta

OmniRoute es un gateway de IA autoalojable, con licencia MIT y una interfaz compatible con el formato OpenAI. La rama `release/v3.8.50` documenta 341 proveedores y 1.202 modelos, además de selección automática, fallback y varias estrategias de routing. El quick start indica que el servicio local utiliza `http://localhost:20128` y expone la API bajo `/v1`. [1] [2]

Esto puede ser útil para Universe Sent Me porque permitiría cambiar de proveedor sin reescribir cada integración, probar modelos distintos con una interfaz uniforme y mantener un punto de control para límites, logs y selección de modelos. Sin embargo, OmniRoute **no es una fuente de datos**, **no sustituye Windsor**, **no valida métricas** y **no convierte una respuesta de IA en evidencia canónica**.

El repositorio también publicita proveedores gratuitos o sin clave. Esa facilidad no debe interpretarse como garantía de disponibilidad, calidad, privacidad o permiso para uso mediante proxy. La propia documentación de OmniRoute mantiene una tabla de advertencias sobre términos de servicio y señala que esas advertencias son informativas, no una autorización legal. [2] [6]

## Compatibilidad con la arquitectura actual

El dashboard social de Universe Sent Me funciona como una interfaz React estática que presenta cálculos y filtros sobre datasets versionados. La actualización de métricas se ejecuta bajo solicitud, conserva fuentes y ventanas de comparabilidad, y mantiene GitHub como fuente oficial de verdad. Ese diseño está documentado en [`2026-08-19_Actualizacion_Asistida_Dashboard_Social.md`](2026-08-19_Actualizacion_Asistida_Dashboard_Social.md) y [`../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md`](../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md).

Por tanto, la arquitectura permitida para una futura función de análisis asistido es:

```text
Dashboard web
    ↓ solicitud mínima
Backend privado de Universe Sent Me
    ↓ payload reducido y validado
OmniRoute privado
    ↓ proveedor seleccionado o fallback
Modelo de IA
    ↓ respuesta etiquetada como derivada
Backend → Dashboard
```

La ruta **navegador → OmniRoute** queda descartada. Las claves de API, los tokens de proveedores y las credenciales administrativas no pueden residir en el código cliente ni viajar a un navegador controlado por terceros. CORS tampoco reemplaza la autenticación: aunque OmniRoute documenta una política de origen cerrada por defecto, el acceso de inferencia sigue dependiendo de Bearer o `x-api-key`, y el gateway debe estar protegido como servicio privado. [3] [5]

## Casos de uso permitidos

| Caso de uso | Valor potencial | Límites y guardrails | Decisión |
|---|---|---|---|
| Lectura narrativa de un corte de métricas ya normalizado | Convertir métricas, hipótesis y límites de comparabilidad en un borrador de insight. | Enviar solo el corte aprobado; conservar ventana y fuentes; etiquetar la respuesta como análisis asistido; impedir escritura automática en los ledgers. | **Candidato prioritario** |
| Clasificación asistida de contenidos | Sugerir personaje, formato, tema o hipótesis para una pieza nueva. | El resultado es una propuesta; requiere revisión humana y debe conservar input, modelo y decisión final. | **Candidato secundario** |
| Generación de copys y variantes creativas | Acelerar borradores para Universe, Wilfred, Elara, Kiri y otros personajes. | La voz, el canon y la aprobación editorial permanecen fuera del gateway; no se publica automáticamente. | **Uso local o backend editorial** |
| Extracción de Windsor | Consultar datos de rendimiento. | OmniRoute no aporta valor frente al conector y añadiría una capa innecesaria. | **No usar** |
| Normalización, deduplicación y cálculo de retorno | Producir métricas reproducibles. | Debe permanecer en scripts y datasets versionados; no delegar reglas deterministas a un modelo. | **No usar** |

## Riesgos y controles obligatorios

| Riesgo | Qué puede ocurrir | Control requerido antes de un uso compartido |
|---|---|---|
| Privacidad | Un prompt enviado al proveedor puede contener datos de métricas, nombres, identificadores o contexto interno. | Construir un payload mínimo; excluir tokens, credenciales sociales, archivos crudos y datos personales; registrar la ventana de datos. |
| Credenciales | Una clave expuesta permite consumir modelos, leer datos o administrar el gateway. | Mantener secretos solo en backend o entorno de servidor; usar valores únicos para `JWT_SECRET`, `API_KEY_SECRET`, contraseña inicial y secreto de bridge; no versionar `.env`. [3] [4] |
| Persistencia | La configuración, credenciales y logs pueden perderse en un runtime efímero. | Ejecutar en una VM o servicio persistente con volumen de datos y copias de seguridad de SQLite. La guía de VM documenta como mínimo 1 vCPU, 1 GB de RAM y 10 GB SSD. [4] |
| Exposición de red | La interfaz administrativa, rutas de gestión o herramientas auxiliares quedan accesibles desde Internet. | Mantener el puerto interno restringido; publicar solo mediante reverse proxy HTTPS; aplicar autenticación, firewall, límites y guardas de rutas. [3] [4] |
| CORS | Una configuración amplia facilita usos no previstos y puede crear errores de proxy. | Usar una lista explícita de orígenes; no activar `CORS_ALLOW_ALL=true` en producción; dejar que OmniRoute gestione los encabezados sin duplicarlos en el proxy. [5] |
| Términos de servicio | Algunos proveedores gratuitos o de prueba restringen proxy, reventa, automatización o uso comercial. | Aprobar proveedores individualmente; conservar una lista permitida; no utilizar la cifra de tokens gratuitos como presupuesto garantizado. [6] |
| Calidad y fallback | Un modelo alternativo puede cambiar el tono, la modalidad o la interpretación del prompt. | Fijar modelos permitidos por caso de uso; registrar proveedor/modelo, latencia, error y coste; revisar muestras antes de adoptar resultados. |
| Cadena de suministro | Una actualización puede cambiar dependencias, rutas o comportamiento operativo. | Fijar una versión evaluada o digest, revisar cambios y vulnerabilidades, hacer backup antes de actualizar y probar en staging. [3] |
| Gobernanza analítica | Una respuesta generada puede confundirse con una métrica o decisión aprobada. | Guardar la salida como derivado revisable; nunca sobrescribir `Content_Inventory.csv`, `Publication_Log.csv`, `ExperimentLog.csv` ni el baseline automáticamente. |

## Opciones de implementación

No se selecciona una implementación definitiva hasta que exista un primer caso de uso aprobado.

| Enfoque | Cuándo usarlo | Ventaja | Coste operativo |
|---|---|---|---|
| Proveedor directo desde un backend | Piloto estrecho con un único modelo y poco tráfico. | Menor superficie operativa y menor número de componentes. | Menos flexibilidad y sin fallback multi-proveedor. |
| OmniRoute local como gateway cloud-first | Piloto personal en una computadora de baja potencia, con un único provider cloud oficial. | Menor consumo que ejecutar modelos locales y endpoint OpenAI-compatible. | Sigue consumiendo RAM/CPU y envía prompts al provider cloud; no es un servicio compartido. |
| Provider directo sin OmniRoute | Equipo demasiado lento para mantener el gateway o piloto con un único modelo. | Menor superficie operativa y menor consumo local. | No ofrece routing, fallback ni trazabilidad centralizada del gateway. |
| OmniRoute autoalojado detrás de backend | Función compartida de análisis o producción editorial. | Endpoint uniforme, routing, fallback y control centralizado. [1] [2] | Requiere VM persistente, backups, observabilidad, control de proveedores y mantenimiento. |

**Recomendación de implementación:** comenzar con **Groq cloud conectado a un gateway OmniRoute local de bajo consumo**, utilizando datos sintéticos o un corte de métricas ya anonimizado. Fijar un único provider y un model ID explícito; no usar `auto` ni conectar providers gratuitos de procedencia incierta. Si el gateway ralentiza el equipo, probar Groq o Gemini directamente desde su Playground/API. Si el piloto demuestra valor, construir un endpoint backend mínimo y desplegar OmniRoute en una VM separada; no incrustarlo dentro del frontend React ni dentro del proceso de extracción de Windsor.

Para evitar cargar la computadora, el hosting externo queda permitido solo bajo estas condiciones: **Railway** sirve para un trial temporal con volumen en `/app/data`, **Render Free** solo para una demo descartable porque pierde la SQLite al suspenderse, y **Oracle Cloud Always Free** es la alternativa gratuita persistente si Fernando acepta administrar una VM, firewall, HTTPS y backups. Sin embargo, en la cuenta actual la región principal es `Mexico Northeast (Monterrey)`, solo se muestra `AD-1` y `VM.Standard.A1.Flex` está temporalmente sin capacidad. La home region no puede cambiarse después de crear la tenancy y suscribir otra región no convierte automáticamente sus VMs en Always Free. [7] [8] Si Oracle no libera capacidad para A1 ni ofrece E2 Micro, Google Cloud e2-micro en una región elegible es la alternativa permanente más cercana, mientras que Railway y Render quedan limitados a pruebas temporales. El procedimiento detallado y sus límites están en [`2026-08-18_Piloto_Local_OmniRoute_Seguro.md`](2026-08-18_Piloto_Local_OmniRoute_Seguro.md), que incluye Oracle, HTTPS, backups y alternativas de hosting.

## Regiones y alternativas cuando Oracle no tiene capacidad

Oracle asigna una **home region** al crear la tenancy y no permite cambiarla posteriormente. Algunas cuentas pueden suscribir regiones adicionales, pero los recursos Compute y Block Volume Always Free deben crearse en la home region; suscribir otra región no convierte una forma de pago en gratuita. En la cuenta del piloto, la consola muestra `Mexico Northeast (Monterrey)` con un único availability domain visible (`AD-1`). Por eso el error `Out of capacity` para A1 no se puede resolver cambiando de AD en esta cuenta. [7] [8]

| Ruta | Permanencia | Condiciones | Decisión |
|---|---|---|---|
| Oracle `VM.Standard.A1.Flex` | Gratuita dentro de límites | Esperar y reintentar en la home region; usar Ubuntu ARM64/AArch64; no cambiar a E5/E4/Intel Flex. | **Primera opción si aparece capacidad** |
| Oracle `VM.Standard.E2.1.Micro` | Gratuita dentro de límites | Crear una VM nueva, no cambiar la E5 existente; usar imagen Ubuntu x86_64/AMD64; aproximadamente 1 GB RAM. | **Plan de contingencia** |
| Google Cloud `e2-micro` | Nivel gratuito mensual; el crédito GenAI App Builder no aplica | Solo `us-west1`, `us-central1` o `us-east1`; 30 GB-mes de disco estándar y 1 GB/mes de salida desde Norteamérica dentro de límites; la IPv4 externa puede tener un SKU separado; requiere facturación y revisión de créditos. | **Alternativa externa persistente con control estricto** |
| Railway | Trial/crédito limitado | Prueba sencilla, pero no es Always Free permanente y el volumen tiene condiciones de expiración. | **Solo prueba** |
| Render Free | Gratuita con límites | Suspensión por inactividad y filesystem efímero; no conserva SQLite/configuración. | **Solo demo descartable** |
| Cuenta Oracle duplicada | No aprobada | Oracle permite una sola cuenta Free Trial o Always Free por persona; no crear cuentas adicionales para cambiar la home region o sortear la capacidad. | **No usar** |

Para el uso manual desde el iMac se aprueba el wrapper [`omniroute-daily-wrapper.sh`](omniroute-daily-wrapper.sh), que solicita la clave de OmniRoute de forma silenciosa, utiliza un model ID Groq explícito, elimina los archivos temporales al terminar y no publica ni escribe en los ledgers. La ruta sigue siendo local y reversible; no se autoriza almacenar credenciales en `.bashrc`, `.profile`, Git o servicios automáticos. El primer caso de uso debe permanecer editorial y revisable, con prompts sintéticos o anonimizados.

La primera ejecución del wrapper quedó validada el 2026-08-23 con un prompt sintético: HTTP `200`, `finish_reason: stop`, provider `groq`, modelo `openai/gpt-oss-20b`, `strategy=single`, `2093 ms`, `89` tokens de entrada y `44` de salida, sin cache hit. Esta prueba confirma la operación diaria del gateway, pero no autoriza todavía la publicación automática ni el envío de datos reales.

El wrapper fue corregido para aceptar prompts extensos en modo multilinea mediante `omniroute-daily-wrapper.sh --multiline`; el usuario pega el contenido y escribe `FIN` en una línea separada antes de introducir la API key. Este control evita que las líneas del prompt se interpreten accidentalmente como comandos de shell.

La primera validación editorial con el wrapper también quedó aprobada: un prompt sintético produjo HTTP `200`, `finish_reason: stop`, `866 ms`, `147` tokens de entrada y `294` de salida, con un borrador estructurado y marcado para revisión humana. La salida no incluyó métricas ni datos de audiencia, aunque añadió emojis, hashtags y una llamada a la acción genérica; por ello, los prompts editoriales deben especificar tono, voz de personaje y formato deseado. La respuesta sigue siendo un derivado no publicado, no una evidencia de rendimiento.

Posteriormente se conectó Google AI Studio como segundo provider. `gemini/gemini-2.5-flash` respondió HTTP `404` porque ya no estaba disponible para usuarios nuevos; el model ID fue descartado. `gemini/gemini-3.5-flash`, visible en el catálogo, respondió correctamente con HTTP `200`, `finish_reason: stop`, `5359 ms` y `strategy=single; provider=gemini`. La diferencia entre los tokens `usage` del cuerpo (`39/623`) y los headers de OmniRoute (`39/34`) queda registrada como observación de medición.

El failover del Combo `usm-groq-gemini-priority` quedó validado mediante una prueba controlada: Groq se desactivó temporalmente, se envió una sola solicitud sintética, OmniRoute seleccionó `gemini/gemini-3.5-flash` con `strategy=priority`, HTTP `200`, `finish_reason: stop` y `3714 ms`, y Groq fue reactivado inmediatamente. La evidencia confirma la transferencia al segundo provider, pero no autoriza todavía publicación automática ni uso de datos privados. La discrepancia de tokens del cuerpo (`11/250`) frente a headers (`11/17`) se conserva como observación separada.

La recomendación actual es no aceptar `VM.Standard.E5.Flex` ni `VM.Standard3.Flex` solo porque tengan capacidad. Debe esperarse A1, intentar E2 Micro como piloto de muy bajo consumo o migrar a Google Cloud e2-micro. En Google Cloud, la ruta más simple requiere una IPv4 externa efímera y puede generar un SKU separado; IAP permite administrar la VM sin IP pública, pero no resuelve por sí solo la salida del contenedor hacia Docker Hub o Groq. El plan Google AI Pro/Google One y el crédito `Trial credit for GenAI App Builder` no deben tratarse como equivalentes: el primero es una suscripción con beneficios y créditos mensuales separados, y el segundo está limitado en la cuenta del piloto a GenAI App Builder/Vertex AI Agent Builder, APIs de Vertex AI y SKUs de IA generativa directamente asociados. El crédito tiene fecha de vencimiento confirmada del **14 de marzo de 2027**. **Compute Engine está excluido de ese crédito y se factura a tarifas estándar.** Compute Engine solo se aprueba mediante el e2-micro Free Tier u otra promoción distinta cuyos términos confirmen explícitamente que el SKU está cubierto. Si el costo cero estricto es no negociable, se debe preferir Oracle Always Free cuando haya capacidad o usar Groq directamente desde el iMac. Si se usa E2 Micro, OmniRoute debe ejecutarse con swap, servicios de fondo desactivados, un único provider cloud y solicitudes pequeñas; si el gateway no cabe con estabilidad, se debe omitir OmniRoute. Si existe una VM flexible creada por error, se debe terminar únicamente esa VM y eliminar su boot volume vacío; no solicitar la eliminación de toda la tenancy salvo que se quiera cerrar permanentemente la cuenta y se hayan revisado todos sus recursos. [12] [13] [14] [15] [16] [17]

## Piloto propuesto

El piloto debe responder una sola pregunta: **¿una lectura asistida por IA mejora la velocidad o la claridad de interpretación de un corte normalizado sin degradar la trazabilidad?**

La validación inicial del gateway local quedó cumplida el 2026-08-23 en el iMac con Xubuntu: OmniRoute `3.8.49` dirigió una solicitud al provider `groq` con el modelo `openai/gpt-oss-20b`, reportó `1214 ms`, `99` tokens de entrada, `80` de salida, decisión `provider=groq` y finalización SSE `data: [DONE]`. OmniRoute reportó costo `0.0000000000` para esa respuesta; este valor es evidencia del gateway, no una garantía de cuota gratuita futura ni una sustitución de la revisión del panel de Groq. Fuente: salida de terminal proporcionada por Fernando el 2026-08-23.

La batería sintética posterior quedó aprobada para el objetivo técnico del piloto: cinco prompts sin datos privados devolvieron HTTP 200 mediante `strategy=single` y `provider=groq`; cuatro terminaron con `finish_reason: stop` y una quedó registrada como truncada por un límite de tokens deliberadamente bajo. La prueba de Monitoring/Logs aportada el mismo día mostró cinco filas visibles sin errores —tres `connection-test` y dos `OPENAI-CHAT`—, todas con estado 200, provider GROQ y cuenta enmascarada. Esta evidencia valida el gateway, pero no convierte las respuestas en evidencia canónica de Growth OS ni autoriza todavía el envío de datos reales.

| Fase | Acción | Criterio de salida |
|---|---|---|
| 1. Preparación | Seleccionar un dataset de prueba sin credenciales ni datos personales. | Payload mínimo documentado y reproducible. |
| 2. Ejecución cloud-first | Instalar OmniRoute localmente solo como gateway; conectar un provider cloud oficial y probar un model ID explícito, sin fallback automático. | Respuesta obtenida sin exponer el gateway a Internet y con el provider registrado. |
| 3. Evaluación | Comparar factualidad, tono, latencia, errores y coste frente a un borrador manual o proveedor directo. Si el gateway pesa demasiado, repetir directamente en el Playground del provider. | Muestra revisada por Fernando; limitaciones registradas. |
| 4. Trazabilidad | Guardar modelo, proveedor, fecha, versión del gateway, prompt estructurado y dataset utilizado. | Artefacto de evaluación en `Operations/Research/`. |
| 5. Decisión | Elegir entre abandonar, mantener uso local o diseñar backend privado. | Decisión explícita y actualización de este documento. |

El piloto no debe publicar contenido, cambiar el canon, editar el inventario, recalcular el baseline ni actualizar automáticamente ninguna cuenta social.

## Relación con documentos existentes

La evaluación actual **no requiere modificar** el procedimiento de actualización del dashboard ni la fuente maestra y los ledgers, porque no se ha aprobado una integración de producción. El procedimiento vigente sigue siendo correcto al afirmar que el refresco de métricas no necesita un servicio permanente y que la evidencia debe conservarse con fuente, fecha, definición y ventana.

Si se aprueba una integración posterior, deberán actualizarse como mínimo estos documentos:

| Documento | Cambio requerido |
|---|---|
| [`2026-08-19_Actualizacion_Asistida_Dashboard_Social.md`](2026-08-19_Actualizacion_Asistida_Dashboard_Social.md) | Añadir una etapa opcional y posterior de análisis asistido, sin alterar extracción, normalización, control, retorno, interfaz ni versionado. |
| [`../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md`](../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md) | Declarar que prompts y respuestas de IA son derivados revisables y no evidencia maestra; definir dónde se registran modelo, proveedor y versión. |
| [`../../GrowthOS/00_01_Changelog_GrowthOS.md`](../../GrowthOS/00_01_Changelog_GrowthOS.md) | Registrar la decisión de implementación, el alcance, la fecha y los documentos afectados. |
| Nuevo runbook en `Operations/Automation/` o `Operations/Production/` | Documentar despliegue, backups, actualización, lista de proveedores permitidos, límites y respuesta a incidentes, solo si se pasa a servicio persistente. |

## Próximo punto de decisión

Antes de instalar paquetes, activar un servicio o mover credenciales, Fernando debe elegir el primer caso de uso: **lectura estratégica de datos, clasificación de contenido o generación creativa**. Con esa elección se decidirá entre Groq/Gemini directo, OmniRoute local como gateway cloud-first o OmniRoute autoalojado detrás de un backend privado.

Hasta entonces, la conclusión operativa es: **sí se puede usar OmniRoute, pero en esta computadora debe probarse únicamente como gateway cloud-first de bajo consumo; si también ralentiza el equipo, se debe omitir el gateway y utilizar directamente el provider cloud**.

## Referencias

[1]: [OmniRoute — repositorio oficial, licencia MIT y capacidades](https://github.com/diegosouzapw/OmniRoute)

[2]: [OmniRoute — Quick Start v3.8.50](https://raw.githubusercontent.com/diegosouzapw/OmniRoute/release/v3.8.50/docs/getting-started/QUICK-START.md)

[3]: [OmniRoute — Security Policy y arquitectura de seguridad](https://raw.githubusercontent.com/diegosouzapw/OmniRoute/release/v3.8.50/SECURITY.md)

[4]: [OmniRoute — guía de despliegue en VM](https://raw.githubusercontent.com/diegosouzapw/OmniRoute/release/v3.8.50/docs/ops/VM_DEPLOYMENT_GUIDE.md)

[5]: [OmniRoute — configuración CORS y seguridad](https://raw.githubusercontent.com/diegosouzapw/OmniRoute/release/v3.8.50/docs/security/CORS.md)

[6]: [OmniRoute — Free Tiers & Free-Token Budget](https://raw.githubusercontent.com/diegosouzapw/OmniRoute/release/v3.8.50/docs/reference/FREE_TIERS.md)

[7]: [Oracle Cloud — Always Free Resources](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm)

[8]: [Oracle — Managing Regions](https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/managingregions.htm)

[9]: [Google Cloud — Free Program and Compute Engine e2-micro](https://cloud.google.com/free/docs/free-cloud-features)

[10]: [Render — Deploy for Free](https://render.com/docs/free)

[11]: [Railway — Pricing and resource limits](https://railway.com/pricing)

[12]: [Oracle Cloud Free Tier — FAQ](https://www.oracle.com/cloud/free/faq/)

[13]: [Oracle — Deleting a Free Tier Tenancy and Cloud Account](https://docs.oracle.com/en-us/iaas/Content/General/Tasks/deleting_tenancy_freetier.htm)

[14]: [Google Cloud — Network pricing and external IP addresses](https://cloud.google.com/vpc/network-pricing)

[15]: [Google Cloud — Connect to Linux VMs using Identity-Aware Proxy](https://cloud.google.com/compute/docs/connect/ssh-using-iap)

[16]: [Google One — Google AI Plans](https://one.google.com/about/google-ai-plans/)

[17]: [Google Cloud — Google Developer Program Premium GenAI Credit SKU Group](https://cloud.google.com/skus/sku-groups/google-developer-program-premium-genai-credit)
