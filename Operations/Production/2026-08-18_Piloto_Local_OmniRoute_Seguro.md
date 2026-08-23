# Piloto de bajo consumo de OmniRoute

**Propósito:** Definir un procedimiento reproducible para probar OmniRoute en una computadora de baja potencia, ejecutando únicamente el gateway local y enviando las solicitudes a un proveedor cloud con API oficial, sin descargar ni ejecutar modelos localmente.

**Estado:** Review

**Fecha de creación:** 2026-08-18

**Última actualización:** 2026-08-23

**Versión:** 2.8

**Autor:** Manus AI

**Organización:** `Operations/Production`

**Documentos relacionados:** [`2026-08-19_Decision_Gateway_IA_OmniRoute.md`](2026-08-19_Decision_Gateway_IA_OmniRoute.md), [`2026-08-19_Actualizacion_Asistida_Dashboard_Social.md`](2026-08-19_Actualizacion_Asistida_Dashboard_Social.md), [`../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md`](../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md).

---

## Decisión de seguridad y hardware

Dado que la computadora no es potente, el piloto debe ser **cloud-first**: OmniRoute se ejecuta localmente solo como gateway y no se descargan ni ejecutan modelos mediante Ollama. Esta opción consume mucho menos almacenamiento, memoria y CPU que la inferencia local. El equipo seguirá conservando el dashboard, la configuración y los logs de OmniRoute, mientras que el prompt viajará al proveedor cloud seleccionado.

La ruta principal será un proveedor con API oficial y clave propia, preferentemente Groq para el primer experimento de texto. Sus términos describen que no accede, usa, almacena o retiene inputs y outputs salvo cuando sea necesario para prestar el servicio, operar de forma fiable o cumplir obligaciones, y que no puede usar inputs u outputs para entrenamiento o fine-tuning salvo autorización expresa; siguen aplicando los términos de cada modelo y del servicio. [7]

Gemini queda como alternativa para comparar calidad o capacidades multimodales, pero su modalidad gratuita indica que el contenido puede utilizarse para mejorar productos y que revisores humanos pueden procesar inputs y outputs. Por tanto, Gemini gratuito solo debe recibir prompts sintéticos o públicamente compartibles, nunca información interna, secretos, datos personales o documentos privados de Universe Sent Me. [4]

Si incluso el gateway de OmniRoute resulta pesado o lento, la alternativa correcta es probar el proveedor cloud directamente desde su Playground o API, sin OmniRoute. OmniRoute aporta valor cuando se necesita un endpoint OpenAI-compatible, trazabilidad y cambio controlado entre providers; no es obligatorio añadirlo si la máquina no puede mantenerlo estable.

No se recomienda empezar con Kiro, OpenCode Free, proveedores web-cookie, agregadores o endpoints no-auth de procedencia incierta. La documentación de OmniRoute marca Kiro y OpenCode Free con advertencia `avoid`, y señala que `NOAUTH` solo describe la ausencia de una credencial, no la privacidad, disponibilidad o autorización para usar un proxy. [5] [6]

> **Orden recomendado para tu equipo:** Groq cloud con datos sintéticos → Gemini cloud solo si hace falta comparar → Ollama local únicamente si más adelante se confirma que el hardware lo soporta. No comenzar con `model: auto` si existen providers no aprobados conectados.

## Matriz de proveedores para el piloto

| Nivel | Proveedor o ruta | Datos que pueden enviarse | Motivo | Estado |
|---|---|---|---|---|
| 1 | Groq API con cuota del plan gratuito | Prompts sintéticos o públicamente compartibles; no secretos ni datos personales | API oficial, rápida y documentada; sus términos describen controles sobre inputs y outputs, pero se deben revisar los términos del modelo y los límites vigentes. [7] [11] | **Recomendado** |
| 2 | Gemini API con cuota gratuita | Solo prompts sintéticos o públicos; nunca información confidencial | API oficial y útil para comparar, pero la modalidad gratuita permite uso para mejora y revisión humana. [4] [12] | **Opcional, con cautela** |
| 3 | Ollama local, solo si el equipo lo soporta | Prompts que deban permanecer en el equipo | Mayor privacidad de inferencia, pero requiere descargar pesos y usar memoria, CPU o GPU local. [1] [2] [3] | **Posponer** |
| Evitar en la primera etapa | Kiro, OpenCode Free, Pollinations, proveedores web-cookie y agregadores | Ningún dato del proyecto | El modelo de autenticación, los términos de proxy o la procedencia del endpoint requieren una revisión adicional. [5] [6] | **No conectar** |

La etiqueta **“más seguro” es relativa**. No constituye una certificación legal, de privacidad ni de calidad. Antes de mover el piloto a un flujo compartido, se deben revisar de nuevo los términos, la política de datos, los límites y la disponibilidad de cada servicio. La cuota gratuita puede cambiar o desaparecer, por lo que ningún model ID debe fijarse sin comprobar el catálogo vigente del provider.

## Requisitos previos

El paquete de OmniRoute `v3.8.50` declara Node.js `>=22.22.2 <23` o `>=24.0.0 <27`. La guía rápida ofrece instalación mediante npm, Docker o código fuente; para un piloto reversible se utilizará npm con la versión fijada, sin abrir puertos públicos. [8] [9]

No se requiere Ollama para esta variante. Solo se instalará si en una etapa posterior se decide evaluar inferencia local y se confirma que el equipo puede sostenerla.

Antes de comenzar, comprobar en una terminal:

```bash
node --version
npm --version
```

Si Node.js es inferior a `22.22.2`, actualizarlo antes de instalar OmniRoute. No se debe forzar la instalación ignorando la restricción de engine del paquete. Si el equipo tiene poca memoria o tarda demasiado en iniciar Node/Next, saltar OmniRoute y usar directamente el Playground o API del provider cloud.

## Paso 1: crear un directorio aislado

En macOS o Linux, crear un directorio exclusivo para el piloto:

```bash
mkdir -p "$HOME/omniroute-pilot/data"
cd "$HOME/omniroute-pilot"
```

En Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME\omniroute-pilot\data" | Out-Null
Set-Location "$HOME\omniroute-pilot"
```

No reutilizar el directorio de una instalación de producción ni copiar el `.env` de otro servicio. El piloto debe tener su propia base de datos, contraseña, claves y carpeta de datos.

## Paso 2: instalar OmniRoute con versión fijada

Instalar exactamente la versión revisada en este runbook:

```bash
npm install --global omniroute@3.8.50
omniroute --version
```

La salida debe indicar `3.8.50`. Fijar la versión evita que una instalación posterior cambie silenciosamente el comportamiento del piloto. Si se necesita evaluar otra versión, debe registrarse como un nuevo experimento y no sustituir esta instalación sin documentarlo.

## Paso 3: crear las variables de entorno locales

En macOS o Linux, generar secretos únicos y crear `.env`:

```bash
cd "$HOME/omniroute-pilot"
JWT_SECRET_VALUE="$(openssl rand -base64 48)"
API_KEY_SECRET_VALUE="$(openssl rand -hex 32)"
STORAGE_KEY_VALUE="$(openssl rand -hex 32)"
INITIAL_PASSWORD_VALUE="$(openssl rand -hex 24)"

cat > .env <<EOF
JWT_SECRET=$JWT_SECRET_VALUE
API_KEY_SECRET=$API_KEY_SECRET_VALUE
INITIAL_PASSWORD=$INITIAL_PASSWORD_VALUE
STORAGE_ENCRYPTION_KEY=$STORAGE_KEY_VALUE
STORAGE_ENCRYPTION_KEY_VERSION=v1
DATA_DIR=$HOME/omniroute-pilot/data
PORT=20128
NODE_ENV=production
OMNIROUTE_SERVER_HOST=127.0.0.1
AUTH_COOKIE_SECURE=false
REQUIRE_API_KEY=true
CORS_ALLOWED_ORIGINS=http://localhost:20128
CORS_ALLOW_ALL=false
CALL_LOG_RETENTION_DAYS=7
APP_LOG_RETENTION_DAYS=7
ARENA_ELO_SYNC_ENABLED=false
OMNIROUTE_DISABLE_CREDENTIAL_HEALTH_CHECK=true
OMNIROUTE_MEMORY_MB=512
EOF

chmod 600 .env
printf '%s\n' "Save the initial password in your password manager: $INITIAL_PASSWORD_VALUE"
```

En Windows PowerShell, crear el archivo con un editor de texto y sustituir los cuatro secretos por valores aleatorios generados en un gestor de contraseñas o con una herramienta criptográficamente segura. El archivo debe contener como mínimo:

```dotenv
JWT_SECRET=<secreto-largo-y-unico>
API_KEY_SECRET=<secreto-hexadecimal-unico>
INITIAL_PASSWORD=<contraseña-inicial-unica>
STORAGE_ENCRYPTION_KEY=<clave-hexadecimal-unica>
STORAGE_ENCRYPTION_KEY_VERSION=v1
DATA_DIR=C:\Users\TU_USUARIO\omniroute-pilot\data
PORT=20128
NODE_ENV=production
OMNIROUTE_SERVER_HOST=127.0.0.1
AUTH_COOKIE_SECURE=false
REQUIRE_API_KEY=true
CORS_ALLOWED_ORIGINS=http://localhost:20128
CORS_ALLOW_ALL=false
CALL_LOG_RETENTION_DAYS=7
APP_LOG_RETENTION_DAYS=7
ARENA_ELO_SYNC_ENABLED=false
OMNIROUTE_DISABLE_CREDENTIAL_HEALTH_CHECK=true
OMNIROUTE_MEMORY_MB=512
```

Las variables cumplen cuatro funciones del piloto. Los secretos protegen el dashboard y las claves almacenadas; `DATA_DIR` mantiene persistente la SQLite; `OMNIROUTE_SERVER_HOST=127.0.0.1` y `CORS_ALLOWED_ORIGINS` mantienen el acceso local; y la desactivación de sincronización Arena y de comprobaciones periódicas evita tráfico auxiliar no necesario mientras se prueba. La referencia de entorno de OmniRoute documenta estos valores y la retención predeterminada de siete días para los logs de llamadas. [9]

No subir `.env` a GitHub, Drive, el inventario de Universe Sent Me ni ninguna herramienta de IA. Añadirlo a un `.gitignore` local:

```bash
printf '%s\n' '.env' 'data/' '*.log' >> .gitignore
```

## Paso 4: iniciar OmniRoute solo en localhost

Desde el directorio del piloto:

```bash
cd "$HOME/omniroute-pilot"
omniroute
```

La guía rápida documenta que OmniRoute inicia el dashboard en `http://localhost:20128`. Abrir esa dirección únicamente en la máquina local. No utilizar una IP LAN, túnel, dominio público, Cloudflare Tunnel ni port forwarding durante este piloto. [8]

Comprobar desde otra terminal:

```bash
curl -I http://127.0.0.1:20128
```

También se puede comprobar el socket de escucha:

```bash
ss -lntp | grep 20128
```

El resultado esperado debe mostrar `127.0.0.1:20128` o `localhost:20128`, no `0.0.0.0:20128`. En Windows, utilizar `Get-NetTCPConnection -LocalPort 20128` y confirmar que la dirección local sea `127.0.0.1`.

## Paso 5: proteger el dashboard y crear una clave de cliente

1. Abrir `http://127.0.0.1:20128`.
2. Iniciar sesión con la contraseña inicial guardada en el Paso 3.
3. Cambiar inmediatamente esa contraseña desde la sección de seguridad del dashboard.
4. Crear una única API key para el piloto desde **API Keys** o **API Manager**.
5. Guardar la clave en un gestor de contraseñas. La guía de OmniRoute indica que la clave se muestra una sola vez y que es la credencial para que las herramientas llamen a OmniRoute, no la credencial del proveedor ascendente. [8]
6. No activar `ALLOW_API_KEY_REVEAL`, no reutilizar la clave en otra aplicación y no pegarla en una conversación, captura de pantalla o repositorio.

Si el dashboard permite seleccionar scopes, otorgar únicamente el permiso de ejecución de completions que necesite el cliente de prueba. No conceder permisos de administración, escritura de providers, combos o configuración a una herramienta creativa.

## Paso 6: conectar un único provider cloud oficial

Para la primera prueba, utilizar Groq:

1. Crear una cuenta en [GroqCloud](https://console.groq.com/) y una API key exclusiva para el piloto.
2. En el dashboard de OmniRoute, ir a **Providers** → **Add Provider**.
3. Seleccionar **Groq** y configurar la base URL oficial `https://api.groq.com/openai/v1`.
4. Pegar la API key únicamente en el campo del provider y guardarla; no introducirla en el frontend, en GitHub ni en un prompt.
5. Ejecutar **Test Connection**.
6. Consultar el catálogo del provider y elegir un model ID que aparezca disponible para tu plan gratuito. No fijar nombres antiguos de memoria: Groq publica el catálogo y el endpoint `/v1/models` para obtener los IDs activos. [11]
7. No conectar todavía Kiro, OpenCode Free, Pollinations, proveedores web-cookie, OpenRouter, AgentRouter ni cualquier provider que no haya sido aprobado para este piloto.

El model ID exacto debe tomarse de la respuesta de `GET /v1/models` del gateway o del dashboard. Mientras haya un solo provider conectado, se reduce el riesgo de fallback inesperado; aun así, utilizar un model ID explícito y no `auto`. Si Groq no ofrece cuota gratuita para el model ID elegido, no habilitar facturación automáticamente: probar otro modelo del catálogo, cambiar a Gemini con datos sintéticos o usar el Playground del provider.

## Paso 7: verificar la API de OmniRoute

Sustituir `PILOT_KEY` por la clave creada en el Paso 6 y consultar los modelos:

```bash
curl http://127.0.0.1:20128/v1/models \
  -H "Authorization: Bearer PILOT_KEY"
```

Copiar uno de los `id` locales que aparecen en esa respuesta y usarlo en la prueba siguiente:

```bash
curl http://127.0.0.1:20128/v1/chat/completions \
  -H "Authorization: Bearer PILOT_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID_LOCAL",
    "messages": [
      {
        "role": "user",
        "content": "Escribe tres variantes breves y aptas para todo público de un mensaje sobre una pausa en el bosque. No uses nombres de personajes ni datos del proyecto."
      }
    ],
    "temperature": 0.7,
    "max_tokens": 180
  }'
```

La respuesta debe incluir `choices[0].message.content`. En el dashboard, revisar **Monitoring/Logs** y confirmar que el provider elegido sea únicamente el provider cloud aprobado. OmniRoute documenta que los logs permiten revisar qué información se envió y qué provider atendió la solicitud. [8]

Para reducir consumo y cuota durante la prueba, utilizar `max_tokens` bajo, prompts cortos y no más de una solicitud simultánea. Groq documenta límites por RPM, RPD, TPM y TPD; los valores exactos deben verificarse en el panel de la cuenta. [11]

## Resultado de validación inicial — 2026-08-23

La primera solicitud real del piloto completó correctamente el recorrido local hacia Groq. OmniRoute reportó la siguiente evidencia técnica:

| Campo | Resultado |
|---|---|
| Versión de OmniRoute | `3.8.49` |
| Provider | `groq` |
| Model ID solicitado | `groq/openai/gpt-oss-20b` |
| Model ID normalizado en la respuesta | `openai/gpt-oss-20b` |
| Decisión de routing | `provider=groq` |
| Latencia reportada | `1214 ms` |
| Tokens de entrada | `99` |
| Tokens de salida | `80` |
| Cache hit | `false` |
| Costo reportado por OmniRoute | `0.0000000000` |
| Finalización SSE | `data: [DONE]` |

Este resultado confirma que el iMac ejecuta el gateway local y que Groq procesa la inferencia remota. El costo cero es el valor reportado por OmniRoute para esa respuesta; no constituye una garantía de permanencia de la cuota gratuita ni sustituye la revisión del panel y los límites de Groq. La API key de Groq no debe registrarse en el repositorio ni en los artefactos de evaluación. Fuente del resultado: salida de terminal proporcionada por Fernando el 2026-08-23.

El criterio de aceptación de esta etapa queda cumplido: **gateway local operativo, provider oficial de Groq, modelo remoto, respuesta SSE completa y sin inferencia local**. La siguiente etapa es evaluar cinco prompts sintéticos y revisar consumo/errores en el dashboard antes de usar cualquier dato del proyecto.

## Paso 8: probar el caso de Universe Sent Me sin datos reales

Durante la primera sesión, utilizar únicamente prompts sintéticos. No pegar capturas privadas, datos de Windsor, tokens de Meta, nombres de seguidores, comentarios reales, IDs de publicaciones ni documentos internos.

Una batería mínima puede contener cinco prompts: una variante de copy breve, una clasificación de formato, una lectura narrativa de números inventados, una traducción y una petición de ideas para una escena de Universe. Para cada prueba registrar fecha, versión de OmniRoute, provider, model ID, tiempo aproximado, resultado y observaciones en un archivo de evaluación dentro de `Operations/Research/`; no registrar secretos ni datos personales.

### Resultado de la batería sintética — 2026-08-23

La batería se ejecutó desde el iMac con `stream: false`, provider explícito `groq`, model ID `groq/openai/gpt-oss-20b` y sin datos privados. La respuesta normalizó el modelo a `openai/gpt-oss-20b` en los headers de OmniRoute. La Prueba 1 fue técnicamente exitosa pero se truncó por `max_tokens: 120`; la Prueba 3 se repitió y quedó aprobada al usar `reasoning_effort: low`.

| Prueba | Tipo de prompt sintético | HTTP | Finalización | Latencia | Tokens entrada/salida | Resultado |
|---:|---|---:|---|---:|---:|---|
| 1 | Tres frases creativas | 200 | `length` | 514 ms | 106 / 120 | Routing correcto; contenido truncado por límite bajo. |
| 2 | Clasificación en JSON | 200 | `stop` | 948 ms | 146 / 264 | Completada correctamente. |
| 3 | Cálculo de tasas inventadas | 200 | `stop` | 735 ms | 188 / 394 | Completada correctamente con razonamiento bajo; cálculos verificados. |
| 4 | Traducción breve | 200 | `stop` | 335 ms | 117 / 24 | Completada correctamente. |
| 5 | Microescena de cuatro pasos | 200 | `stop` | 500 ms | 134 / 182 | Completada correctamente. |

En las cinco pruebas, los headers indicaron `strategy=single`, `provider=groq`, model ID normalizado `openai/gpt-oss-20b` y versión OmniRoute `3.8.49`. En las solicitudes donde se extrajo el header, OmniRoute reportó `x-omniroute-response-cost: 0.0000000000`; este dato es un cálculo del gateway para esas respuestas y no debe interpretarse como garantía de cuota gratuita futura de Groq.

### Verificación visual de Monitoring/Logs

La captura del panel proporcionada el 2026-08-23 muestra cinco filas visibles, todas con estado `200` y origen `UPSTREAM`. Tres filas son `connection-test` sin tokens —`152 ms`, `209 ms` y `233 ms`— y dos filas son solicitudes `OPENAI-CHAT` a `groq/openai/gpt-oss-20b`: una con `134` tokens de entrada y `182` de salida, `368` TPS y `494 ms`; otra con `117` tokens de entrada y `24` de salida, `72.9` TPS y `329 ms`. El provider aparece como `GROQ` en las cinco filas y la cuenta se muestra enmascarada como `Unive***`.

La captura no contiene una columna de costo legible y no demuestra por sí sola que esas cinco filas sean exactamente las cinco pruebas funcionales; combina dos chats con tres comprobaciones de conexión. La evidencia principal de las cinco pruebas es la salida de terminal, mientras que el panel confirma que no hubo errores HTTP, que el provider fue Groq y que el routing ocurrió aguas arriba. No se documentan identificadores completos de API key, aunque el panel mostraba uno truncado.

### Wrapper diario seguro

El script [`omniroute-daily-wrapper.sh`](omniroute-daily-wrapper.sh) permite usar el gateway desde la Terminal sin guardar la API key. Solicita la clave en modo silencioso, crea un payload temporal, utiliza el model ID explícito `groq/openai/gpt-oss-20b`, envía `reasoning_effort: low` y `stream: false`, muestra la respuesta y elimina el payload, los headers y la variable de entorno al terminar. El wrapper no publica contenido ni escribe en los ledgers del Growth OS.

En el iMac, después de copiar el script a una ubicación local, aplicar permisos restrictivos y ejecutarlo:

```bash
chmod 700 ~/omniroute-daily-wrapper.sh
~/omniroute-daily-wrapper.sh
```

El modo normal acepta un prompt de una sola línea. Para pegar un prompt largo o estructurado en varias líneas, usar el modo multilinea y escribir `FIN` sola en una línea cuando se haya terminado. Esto evita que las líneas del prompt se interpreten como comandos de la Terminal:

```bash
~/omniroute-daily-wrapper.sh --multiline
```

Después de iniciar ese modo, pegar el prompt completo, escribir:

```text
FIN
```

y pulsar Enter. Solo entonces el wrapper solicitará la API key de forma silenciosa.

### Validación del wrapper — 2026-08-23

El wrapper se ejecutó desde el iMac con un prompt sintético y completó la solicitud sin error: HTTP `200`, respuesta no vacía, `finish_reason: stop`, provider `groq`, model ID normalizado `openai/gpt-oss-20b`, `strategy=single`, latencia `2093 ms`, `89` tokens de entrada y `44` de salida. El header indicó `x-omniroute-cache-hit: false`, versión `3.8.49` y costo reportado por OmniRoute de `0.0000000000`. La clave no se incorporó al comando, al prompt ni al repositorio; el wrapper la recibe mediante entrada silenciosa y ejecuta limpieza al terminar.

Esta prueba confirma la ruta operativa diaria: **Terminal → wrapper → OmniRoute local en `127.0.0.1` → Groq → respuesta**. La latencia de `2093 ms` es mayor que algunas pruebas anteriores, pero no representa un fallo; puede variar según la solicitud, el razonamiento del modelo y la red. La cifra de costo es la reportada por el gateway para esa respuesta y no garantiza que la cuota de Groq permanezca gratuita.

### Validación editorial inicial — 2026-08-23

Con el wrapper ya corregido, se ejecutó un prompt de una sola línea para generar un borrador editorial sintético sobre un gato ficticio con gafas que descubre una puerta luminosa entre libros. La salida cumplió la estructura solicitada: etiqueta `Draft sujeto a revisión humana`, gancho, tres momentos visuales, descripción y llamada a la acción. No inventó métricas, fechas, resultados ni datos de audiencia.

| Control editorial | Resultado |
|---|---|
| Prompt completo recibido | Sí; la API key se solicitó después del prompt |
| Respuesta | HTTP `200`, no vacía |
| Terminación | `finish_reason: stop` |
| Routing | `strategy=single`, provider `groq`, modelo `openai/gpt-oss-20b` |
| Latencia | `866 ms` |
| Tokens | `147` de entrada / `294` de salida |
| Cache | `false` |
| Estado de contenido | Borrador; no publicado |

La respuesta agregó emojis, hashtags y una llamada a la acción de estilo genérico. Esto no es un error técnico, pero demuestra que el prompt debe especificar si el estudio quiere un tono sobrio, sin emojis, sin hashtags o con una voz de personaje concreta. Antes de guardar un borrador dentro de Growth OS, revisar canon, voz, duración, claridad visual y llamada a la acción. La prueba valida la generación asistida, no el rendimiento de la pieza ni la conveniencia de publicarla. Los resultados permanecen como derivados revisables y no deben incorporarse a `Publication_Log.csv`, `ExperimentLog.csv` ni a un baseline hasta que exista aprobación editorial y publicación real.

El prompt debe ser sintético o anonimizado. Para una tarea que requiera más salida, puede aumentarse temporalmente el límite sin guardar configuración permanente:

```bash
OMNIROUTE_MAX_TOKENS=600 ~/omniroute-daily-wrapper.sh
```

No establecer la API key en `.bashrc`, `.profile`, Git, archivos de texto, historial de comandos ni servicios automáticos. El wrapper es una herramienta manual y reversible; no debe utilizarse todavía para publicación automática, actualización de métricas o envío de datos crudos de Windsor. Si el contenedor está detenido, primero iniciarlo con `sudo docker start omniroute`; si está activo, no recrearlo solo para usar el wrapper.

El piloto puede comparar un segundo model ID cloud solo si el provider lo ofrece dentro de la cuota gratuita. La calidad debe juzgarse con criterios definidos por el estudio —fidelidad al prompt, claridad, tono, repetición y latencia— y no únicamente por una respuesta llamativa. Si OmniRoute ralentiza demasiado el equipo, continuar la comparación directamente en el Playground del provider y registrar que el gateway fue omitido por limitación de hardware.

## Paso 9: añadir Gemini solo como comparación opcional

Si se necesita una segunda opinión, añadir **un solo provider adicional** y mantenerlo separado de Groq. Para Gemini, crear una clave independiente en Google AI Studio y usar únicamente prompts sintéticos o públicos. La documentación de precios indica que el nivel gratuito tiene tokens sin costo, pero también marca que el contenido se utiliza para mejorar productos; por tanto, no utilizar el provider gratuito con contenido confidencial de Universe Sent Me. [4] [12]

Después de conectar Gemini, no utilizar `model: "auto"` para esta comparación. Seleccionar explícitamente el model ID que aparezca disponible en el catálogo, revisar los logs después de cada solicitud y desconectar la credencial al terminar. Si el equipo se vuelve lento, detener OmniRoute antes de continuar y usar directamente el Playground de Gemini.

### Validación de Google AI Studio — 2026-08-23

El primer model ID probado, `gemini/gemini-2.5-flash`, devolvió HTTP `404` con el mensaje del provider de que `models/gemini-2.5-flash` ya no está disponible para usuarios nuevos. No se debe volver a usar ese ID; el catálogo vigente del dashboard tiene prioridad sobre la memoria o ejemplos antiguos.

Se probó después el model ID visible `gemini/gemini-3.5-flash` con un prompt sintético. La respuesta fue completa y terminó correctamente:

| Campo | Resultado |
|---|---|
| HTTP | `200` |
| Provider | `gemini` |
| Model ID normalizado | `gemini-3.5-flash` |
| Decisión | `strategy=single; provider=gemini` |
| Latencia | `5359 ms` |
| Finalización | `stop` |
| Tokens según `usage` del cuerpo | `39` de entrada / `623` de salida |
| Tokens según headers OmniRoute | `39` de entrada / `34` de salida |
| Cache | `false` |
| Costo reportado por OmniRoute | `0.0000000000` |

La discrepancia entre `usage.completion_tokens=623` y `x-omniroute-tokens-out=34` queda registrada como una observación de medición específica de esta ruta; no debe resolverse inventando un valor ni mezclando ambas cifras. Para auditoría se conservará el cuerpo de la respuesta junto con los headers cuando se haga una comparación formal.

Esta ejecución valida Google AI Studio como segundo provider directo, pero no valida todavía que el fallback del Combo se active. El Combo `usm-groq-gemini-priority` sí quedó creado con Groq primero y Google AI Studio después; su prueba realizada hasta este punto confirmó únicamente la ruta primaria de Groq. No se debe afirmar que el failover está probado hasta observar una solicitud atendida por `gemini` después de un fallo controlado de Groq.

### Validación de failover del Combo — 2026-08-23

Se realizó una prueba controlada con el Combo `usm-groq-gemini-priority`: Groq se desactivó temporalmente desde el dashboard, se envió una sola solicitud sintética y Groq se reactivó inmediatamente después. OmniRoute transfirió la solicitud al segundo destino:

| Campo | Resultado |
|---|---|
| Combo | `usm-groq-gemini-priority` |
| Estrategia | `priority` |
| Provider seleccionado | `gemini` |
| Modelo seleccionado | `gemini-3.5-flash` |
| HTTP | `200` |
| Finalización | `stop` |
| Latencia | `3714 ms` |
| Tokens según `usage` del cuerpo | `11` de entrada / `250` de salida |
| Tokens según headers OmniRoute | `11` de entrada / `17` de salida |
| Cache | `false` |
| Costo reportado por OmniRoute | `0.0000000000` |
| Groq después de la prueba | Reactivado |

La evidencia confirma el failover del Combo, no solo la disponibilidad directa de Gemini. La diferencia entre los contadores de tokens del cuerpo y de los headers vuelve a aparecer en la ruta Gemini y queda registrada sin reconciliar artificialmente. La solicitud utilizó un prompt sintético; no se enviaron datos privados, tokens, métricas reales ni documentos internos.

Groq debe tratarse como una ruta cloud controlada, no como una ruta privada local. Aunque sus términos describen restricciones sobre el uso de inputs y outputs, el prompt sale del equipo y se aplican también los términos de cada model provider. [7]

## Siguiente etapa: integración en aplicación o API de producción

La instalación actual en el iMac es válida para desarrollo y staging, pero no puede ser el endpoint de producción: OmniRoute escucha únicamente en `127.0.0.1`, depende de que el iMac esté encendido y no es accesible desde una aplicación alojada en Internet. La aplicación tampoco debe llamar al dashboard ni al puerto local directamente desde el navegador.

La arquitectura objetivo para un primer caso editorial es:

```text
Frontend React o cliente autorizado
        ↓ HTTPS + sesión/autorización
Backend privado de Universe Sent Me
        ↓ payload mínimo + API key de ejecución
OmniRoute privado en un host persistente
        ↓ model = usm-groq-gemini-priority
Groq principal → Gemini fallback
        ↓ respuesta derivada
Backend → borrador no publicado
```

| Enfoque | Tradeoffs | Coste | Complejidad de configuración |
|---|---|---|---|
| Provider directo desde el backend, sin OmniRoute | Es la alternativa ligera y reduce componentes, pero no conserva el Combo ni el failover multi-provider. | Coste y cuota del provider elegido; no se garantiza gratuidad permanente. | Baja |
| OmniRoute en un host persistente con Docker y HTTPS | Conserva `usm-groq-gemini-priority`, logs y failover; exige volumen persistente, TLS, firewall, backups y mantenimiento. | Hosting potencialmente facturable más uso de providers; no asumir que Oracle, Google, Railway o Render serán gratuitos a largo plazo. | Media-alta |
| Mantener OmniRoute en el iMac | Costo adicional mínimo y útil para staging local, pero no funciona como servicio público ni cuando el equipo está apagado. | Sin hosting adicional; requiere mantener el iMac encendido para cada prueba. | Baja para staging; no válida para producción |

El siguiente paso de implementación debe ser un endpoint backend mínimo, por ejemplo `POST /api/ai/draft`, y no una llamada desde React a OmniRoute. El backend debe aceptar solo un propósito editorial permitido, limitar el tamaño del prompt, eliminar o rechazar secretos y datos personales, usar la API key de OmniRoute con permisos de ejecución, invocar el Combo por su nombre exacto, registrar request ID, provider, modelo, latencia, estado y costo reportado, y devolver el resultado marcado como `Draft`. No debe publicar contenido ni escribir en `Publication_Log.csv`, `ExperimentLog.csv`, el baseline ni la fuente maestra.

Antes de exponer ese endpoint se requiere un entorno de staging separado, una URL HTTPS privada o protegida, autenticación del cliente, rate limiting, límites de longitud, timeout, manejo de `429`/`5xx`, sanitización de respuestas y observabilidad. El primer despliegue debe usar prompts sintéticos; después se puede evaluar texto público o anonimizado. La clave de Management Access debe permanecer desactivada y no debe reutilizarse la API key de un provider.

La decisión pendiente es elegir entre el provider directo ligero y un host persistente para OmniRoute. Si el objetivo de producción exige conservar el Combo, el siguiente trabajo concreto es inventariar la aplicación actual —stack, hosting y backend disponible— y diseñar el contrato de `POST /api/ai/draft`; no se debe abrir el puerto del iMac a Internet ni crear un túnel improvisado.

## Paso 10: alojar OmniRoute fuera de la computadora

### Decisión rápida

| Plataforma | ¿Es gratuita? | Persistencia de OmniRoute | Veredicto para este piloto |
|---|---|---|---|
| Render Free | Sí, con límites | No: el filesystem es efímero y se pierde la SQLite al reiniciar, redeployar o suspender; el servicio se suspende tras 15 minutos sin tráfico. [13] [14] | **Solo demo temporal**, no recomendada para conservar providers y configuración. |
| Railway | Trial de 5 USD por hasta 30 días; después, plan Free con 1 USD/mes de crédito | Sí mediante volumen en `/app/data`, pero los volúmenes de cuentas trial se eliminan 30 días después de expirar los créditos. [15] [16] | **Mejor para una prueba de 30 días**, no gratis permanente. |
| Oracle Cloud Always Free | Sí, mientras se mantengan las condiciones de Always Free | Sí, mediante el disco de la VM; exige administrar Linux, Docker, firewall, dominio y backups. [20] | **Mejor alternativa gratuita persistente**, pero requiere más trabajo técnico y puede sufrir falta de capacidad o reclamación por inactividad. |
| Google Cloud e2-micro | Sí, dentro de límites y regiones elegibles | Sí, con 30 GB-mes de disco estándar; una IPv4 externa puede generar un cargo separado. [23] [28] | **Alternativa persistente**, con control estricto de red y facturación; no se puede garantizar costo cero absoluto si se necesita salida a Internet. |

Para tu caso, la recomendación es **Oracle Cloud A1/E2 Micro si aparece capacidad**, **Google Cloud e2-micro si aceptas controlar una posible tarifa de IPv4 externa**, Railway para una prueba temporal y Render solo para una demo descartable. Render Free es el camino más sencillo visualmente, pero su pérdida de SQLite hace que OmniRoute olvide la configuración de providers después de un reinicio o suspensión. Además, la instancia gratuita de Render ofrece 512 MB de RAM y 0,1 CPU, mientras que la guía de OmniRoute recomienda como mínimo una VM de 1 GB para un despliegue persistente. [14] [18]

### Configuración común de secretos

No subas un archivo `.env` al repositorio. En Render, Railway u Oracle, introduce cada variable desde el panel de variables/secretos o crea el archivo directamente en la VM con permisos restringidos. Genera valores distintos para cada instalación:

```dotenv
JWT_SECRET=<openssl-rand-hex-32>
INITIAL_PASSWORD=<contraseña-larga-y-unica>
API_KEY_SECRET=<openssl-rand-hex-32>
STORAGE_ENCRYPTION_KEY=<openssl-rand-hex-32>
STORAGE_ENCRYPTION_KEY_VERSION=v1
MACHINE_ID_SALT=<openssl-rand-hex-32>
OMNIROUTE_WS_BRIDGE_SECRET=<openssl-rand-hex-32>
NODE_ENV=production
DATA_DIR=/app/data
AUTH_COOKIE_SECURE=true
REQUIRE_API_KEY=true
CORS_ALLOW_ALL=false
CALL_LOG_RETENTION_DAYS=7
APP_LOG_RETENTION_DAYS=7
ARENA_ELO_SYNC_ENABLED=false
OMNIROUTE_DISABLE_CREDENTIAL_HEALTH_CHECK=true
OMNIROUTE_DISABLE_BACKGROUND_SERVICES=1
OMNIROUTE_MEMORY_MB=512
```

`OMNIROUTE_WS_BRIDGE_SECRET` es requerido por la guía de despliegue para producción. No actives servicios web-cookie, MCP, Redis, Qdrant, Bifrost ni perfiles CLI en un free tier; solo necesitas el runtime base y un provider cloud oficial. [18]

### Opción A: Railway para una prueba rápida

1. Crea una cuenta en Railway. Si la verificación de GitHub no se completa, el trial puede tener restricciones de red; la documentación de Railway distingue entre trial completo y trial limitado. [15]
2. Crea un proyecto y despliega la imagen pública de OmniRoute. Usa una referencia por digest cuando la plataforma lo permita: `docker.io/diegosouzapw/omniroute@sha256:2bf79cf167478bf283c633ffef2e1e26ba746882e7267fab9320c09df56e8b57`. Este digest corresponde a la imagen `latest` consultada el 19 de agosto de 2026; compruébalo nuevamente antes de usarlo porque las imágenes pueden cambiar. [19]
3. Añade las variables del bloque anterior. Configura `PORT=20128`, `DASHBOARD_PORT=20128`, `API_PORT=20128`, `OMNIROUTE_SERVER_HOST=0.0.0.0` y `BASE_URL=http://127.0.0.1:20128`.
4. Añade `NEXT_PUBLIC_BASE_URL=https://TU_DOMINIO.up.railway.app` después de generar el dominio público. Railway proporciona dominios `*.railway.app` y TLS automático. [17]
5. Crea un volumen conectado al servicio y móntalo exactamente en `/app/data`. OmniRoute guarda allí su SQLite y la configuración cifrada. Railway documenta que un volumen montado en `/app/data` conserva los datos escritos por la aplicación y que los volúmenes se montan al iniciar el contenedor. [16]
6. Añade `RAILWAY_RUN_UID=0` solo si el contenedor no puede escribir en el volumen. Railway advierte que los volúmenes se montan como root y que las imágenes con usuario no root pueden necesitar esta variable; usarla implica aceptar que el proceso principal se ejecute como root durante el piloto. [16]
7. En **Settings → Networking → Public Networking**, genera el dominio. No abras puertos TCP adicionales ni publiques Redis, el puerto administrativo alternativo o servicios auxiliares. [17]
8. Abre `https://TU_DOMINIO.up.railway.app`, cambia la contraseña inicial y crea una API key de OmniRoute.
9. Conecta únicamente Groq con su API key oficial. Selecciona un model ID que aparezca disponible en el catálogo de tu cuenta, no `auto`. La clave de Groq debe guardarse en la configuración cifrada de OmniRoute sobre `/app/data`, no en un prompt ni en el código cliente.
10. Prueba `https://TU_DOMINIO.up.railway.app/v1/models` y luego una solicitud pequeña a `/v1/chat/completions`. Si el trial termina, exporta o elimina los datos antes de que Railway elimine el volumen; no guardes allí la fuente maestra ni datasets permanentes.

**Importante:** Railway no es completamente gratuito a largo plazo. Después de 30 días o de consumir 5 USD, el trial vuelve al plan Free con 1 USD de crédito mensual; el crédito no se acumula y los volúmenes de cuentas trial se eliminan 30 días después de expirar los créditos. [15]

### Opción B: Render Free para una demo descartable

Render puede desplegar una imagen Docker preconstruida y expone el servicio con HTTPS. En **New → Web Service → Existing Image**, utiliza `docker.io/diegosouzapw/omniroute:latest` o un digest verificado; Render exige que el servicio escuche en `0.0.0.0` y recomienda usar la variable `PORT`. [13] [14]

Configura como mínimo:

```dotenv
PORT=10000
DASHBOARD_PORT=10000
API_PORT=10000
OMNIROUTE_SERVER_HOST=0.0.0.0
NEXT_PUBLIC_BASE_URL=https://TU_SERVICIO.onrender.com
BASE_URL=http://127.0.0.1:10000
DATA_DIR=/app/data
AUTH_COOKIE_SECURE=true
REQUIRE_API_KEY=true
OMNIROUTE_MEMORY_MB=384
OMNIROUTE_DISABLE_BACKGROUND_SERVICES=1
OMNIROUTE_DISABLE_CREDENTIAL_HEALTH_CHECK=true
```

Después de cada suspensión o reinicio, debes asumir que la SQLite y las credenciales almacenadas desaparecerán. Render confirma que los servicios Free no pueden usar discos persistentes y que las bases SQLite locales se pierden; su Postgres Free también tiene una vigencia limitada de 30 días. [13] Por eso Render Free no debe ser la opción principal para OmniRoute. Úsalo solo para comprobar que el contenedor arranca, abrir el dashboard temporalmente y probar un provider sin datos privados.

### Opción C: Google Cloud e2-micro como alternativa persistente

Google Cloud ofrece una VM e2-micro no interrumpible por mes dentro del nivel gratuito en una de estas regiones de Estados Unidos: `us-west1` (Oregón), `us-central1` (Iowa) o `us-east1` (Carolina del Sur). También incluye hasta 30 GB-mes de disco persistente estándar y 1 GB mensual de salida desde Norteamérica, dentro de los límites publicados. [23]

**Advertencia de costo:** no existe una forma honesta de garantizar costo cero absoluto si la VM necesita una ruta normal de salida a Internet. Google cobra las direcciones IPv4 externas estáticas o efímeras por separado; el precio publicado es de US$0.005 por hora. [28] Una VM sin IPv4 externa puede administrarse mediante IAP, pero para descargar Docker y llamar a Groq necesitaría salida a Internet mediante Cloud NAT u otro proxy, que tampoco debe asumirse como gratuito. [29]

Para el piloto, la opción práctica es usar una **IPv4 externa efímera**, nunca una IP estática, y asumir que podría aparecer un cargo pequeño. Si costo cero estricto es un requisito no negociable, no despliegues OmniRoute en Google Cloud: usa Oracle Always Free cuando A1/E2 Micro tenga capacidad o ejecuta Groq directamente desde el iMac.

#### Diferenciar Google AI Pro del crédito de Google Cloud

Google AI Pro/Google One es una suscripción de almacenamiento y funciones Gemini. En México, la página pública de Google One muestra 5 TB y un beneficio separado de créditos mensuales de Google Cloud del Google Developer Program; el precio y la elegibilidad que aparecen en la cuenta del usuario pueden variar por promoción. Ese plan **no convierte el almacenamiento de Drive/Fotos/Gmail en almacenamiento de una VM** y no debe confundirse con el saldo de Billing de Google Cloud. [30]

El crédito que aparece como `Trial credit for GenAI App Builder` con un saldo aproximado de MX$17,178.46 es otra promoción. En la cuenta utilizada para este piloto, la información de Billing confirma que está estrictamente limitado a servicios de GenAI App Builder/Vertex AI Agent Builder, APIs de Vertex AI y SKUs de IA generativa directamente asociados. Su fecha de vencimiento confirmada es el **14 de marzo de 2027**. **Compute Engine y los servicios de infraestructura de propósito general están excluidos y se facturan a tarifas estándar.** Por tanto, este crédito no puede financiar la VM e2-micro de OmniRoute. La cobertura visible en la cuenta del usuario y el desglose de SKU tienen prioridad sobre cualquier suposición basada en el nombre de la promoción. Fuente permanente del proyecto: aclaración de Billing proporcionada por Fernando el 2026-08-23.

Antes de crear la VM, confirma por escrito en la consola:

| Comprobación | Resultado que autoriza continuar |
|---|---|
| Crédito | Tiene saldo disponible y vence el **14 de marzo de 2027** según la cuenta del piloto. |
| Servicios elegibles | La promoción menciona explícitamente **Compute Engine** o la simulación de costo muestra el SKU como cubierto. El crédito actual de GenAI App Builder **no cumple** este criterio. |
| Proyecto | La VM se creará en el proyecto vinculado a la cuenta de facturación que contiene el crédito. |
| Costos no cubiertos | IPv4 externa, salida de red, disco, snapshots y otros SKU están identificados; no se asume que el crédito cubra todo. |

El crédito actual de GenAI App Builder, válido hasta el **14 de marzo de 2027**, no es elegible para Compute Engine, por lo que no debe usarse para la VM. Mantén la opción Oracle Always Free, intenta la forma E2/A1 cuando exista capacidad o ejecuta Groq directamente desde el iMac. Google Cloud solo queda aprobado si se utiliza su e2-micro Free Tier o una promoción distinta que indique explícitamente cobertura de Compute Engine; cualquier uso posterior o SKU excluido puede facturarse.

#### Crear el proyecto y controlar el costo

1. Crea un proyecto de Google Cloud con un nombre como `omniroute-free` o utiliza un proyecto vacío existente. No mezcles otros servicios.
2. Vincula una cuenta de facturación únicamente porque Google Cloud la requiere para Compute Engine; esto no elimina la necesidad de controlar los SKU.
3. En **Billing → Budgets & alerts**, crea un presupuesto de referencia muy bajo, por ejemplo US$1, con alertas al 50%, 90% y 100%. Las alertas **no detienen automáticamente** los recursos ni la facturación, por lo que son un aviso y no un límite técnico. [27]
4. En **Billing → Reports/Cost table**, filtra por el proyecto y revisa Compute Engine, Persistent Disk, External IP y Network Egress después de crear la VM.

#### Crear la VM e2-micro

En **Compute Engine → VM instances → Create instance**, usa estos valores:

| Campo | Valor recomendado |
|---|---|
| Name | `omniroute-free` |
| Region | `us-west1`, `us-central1` o `us-east1` |
| Zone | Una zona dentro de la región elegida, por ejemplo `us-central1-a` |
| Machine type | **E2 → e2-micro**; no `e2-small`, `e2-medium` ni tipo personalizado |
| Provisioning model | **Standard/no interrumpible**, no Spot |
| Boot disk | Ubuntu LTS x86_64/AMD64, **20 GB**, `pd-standard` |
| External IPv4 | Efímera, solo si se acepta el posible cargo; nunca reservar una IP estática |
| Firewall | No marcar “Allow HTTP” ni “Allow HTTPS” durante el piloto |
| GPUs | Ninguna |
| Additional disks/snapshots | Ninguno |

La consola debe indicar que la VM `e2-micro` y el disco estándar están dentro de las condiciones del nivel gratuito. No crees más de una e2-micro y mantén el disco total del proyecto por debajo de 30 GB. No añadas Cloud NAT, Load Balancer, GPU, discos SSD, snapshots automáticos ni IP reservada.

Para una VM sin IPv4 externa, IAP TCP forwarding permite el acceso SSH a la IP interna mediante un túnel HTTPS, pero requiere autenticación, IAM y una regla de firewall desde `35.235.240.0/20`. [29] Esa variante es apropiada para administrar una VM sin publicarla, pero no resuelve por sí sola la salida del contenedor hacia Docker Hub o Groq; por eso no es la ruta inicial recomendada para este piloto.

#### Preparar la VM de 1 GB

Conéctate por SSH y crea swap antes de instalar OmniRoute:

```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
sudo sysctl vm.swappiness=10
free -h
```

Instala Docker siguiendo el bloque oficial de este runbook y configura `OMNIROUTE_MEMORY_MB=384` o `512`, `OMNIROUTE_DISABLE_BACKGROUND_SERVICES=1`, un solo provider cloud y solicitudes pequeñas. Mantén el contenedor enlazado a `127.0.0.1:20128`; no marques los checkboxes de HTTP/HTTPS ni expongas el dashboard directamente durante el piloto.

Si necesitas abrir el dashboard desde el iMac sin publicar el puerto, utiliza un túnel SSH local después de configurar el acceso:

```bash
ssh -i ~/.ssh/omniroute_oracle -N \
  -L 20128:127.0.0.1:20128 usuario@IP_O_HOST_DE_GOOGLE
```

En Google Cloud, la ruta IAP equivalente es `gcloud compute ssh ... --tunnel-through-iap`, con un reenvío `-L`; la documentación oficial muestra los permisos y la regla de firewall necesarios. [29]

#### Validación de costo antes de usar OmniRoute

Antes de instalar el provider cloud, verifica en la consola:

| Control | Resultado requerido |
|---|---|
| Máquina | `e2-micro`, Standard, una sola instancia |
| Región | `us-west1`, `us-central1` o `us-east1` |
| Disco | `pd-standard`, máximo 30 GB acumulados; se recomienda 20 GB |
| IP | Efímera si es necesaria; no reservada/estática |
| Red | Sin Cloud NAT, Load Balancer, GPU ni firewall HTTP/HTTPS público |
| Salida | Mantener las llamadas a Groq pequeñas para no superar 1 GB/mes |
| Billing | Alertas creadas y Cost table revisada; recordar que las alertas no apagan recursos |

Si aparece cualquier SKU distinto de Compute e2-micro, Persistent Disk Standard o la IP externa que conscientemente aceptaste, detén la VM y corrige el recurso antes de desplegar OmniRoute.

### Opción D: Oracle Cloud Always Free para persistencia gratuita

Oracle ofrece una VM Always Free con recursos persistentes durante la vida de la cuenta: hasta 2 OCPU y 12 GB de memoria total en Ampere A1, o hasta dos VMs AMD de 1 GB, además de 200 GB de almacenamiento de bloques en la región principal. Oracle puede reclamar instancias inactivas y la creación puede fallar temporalmente por falta de capacidad. [20]

### 1. Crear la cuenta y controlar el coste

1. Abre [Oracle Cloud Free](https://www.oracle.com/cloud/free/) y completa el registro. La cuenta puede solicitar verificación de identidad o método de pago según el país; eso no convierte automáticamente los recursos etiquetados como **Always Free Eligible** en recursos de pago. Oracle indica que solo se permite una cuenta Free Trial o Always Free por persona; no crear una segunda cuenta para intentar obtener otra región o sortear la falta de capacidad. [24]
2. Identifica la **home region** de la tenancy. Oracle indica que la home region no se puede cambiar después de crear la cuenta y que las VMs Compute Always Free deben crearse allí. Se pueden suscribir regiones adicionales en algunas cuentas, pero eso no convierte sus recursos Compute en Always Free. [20] [22]
3. En la cuenta actual del piloto, la consola muestra la región `Mexico Northeast (Monterrey)` y solo `AD-1`. Por tanto, no hay otro availability domain disponible para sortear el error de capacidad; la acción correcta es esperar y reintentar A1, no cambiar a E5/E4/Intel Flex. En regiones con varios dominios sí se puede probar otro AD. Oracle indica que E2 Micro puede estar limitado a un solo AD. [20]
4. Crea, si la consola lo permite, un compartment llamado `omniroute-free` y utiliza únicamente recursos que muestren la etiqueta **Always Free Eligible**. No crees Load Balancer, NAT Gateway, bases de datos de pago, discos fuera de la home region ni IPs o servicios adicionales sin revisar el coste.
5. No actives Pay As You Go solo para resolver `out of host capacity`. Oracle indica que los recursos Always Free siguen sin cargo después de una actualización, pero cualquier recurso que exceda los límites gratuitos sí puede generar cargos. Las cuotas de compartment ayudan a limitar el consumo. [20]
6. Si una VM E5/E4/Intel Flex fue creada por error, termina únicamente la instancia y elimina su boot volume vacío; no solicites la eliminación de toda la tenancy. La eliminación de la tenancy borra la cuenta cloud y todos sus recursos de manera irreversible, y la solicitud puede suspenderlos durante el proceso de 30 días. [25]

### 2. Crear la VM Always Free

En **Compute → Instances → Create instance**, configura lo siguiente:

| Campo | Valor recomendado |
|---|---|
| Name | `omniroute-free` |
| Availability domain | Cualquiera disponible en la home region; si A1 no tiene capacidad, esperar o usar AMD Micro para una prueba mínima. |
| Image | Ubuntu 24.04 LTS, marcada como Always Free Eligible. |
| Shape | `VM.Standard.A1.Flex`, 1 OCPU y 6 GB RAM. Esta es la opción preferida para OmniRoute. |
| Boot volume | 50 GB, dentro de los 200 GB Always Free de block volume. |
| Networking | VCN nueva, subnet pública, asignar IPv4 pública. |
| SSH keys | Subir una clave pública Ed25519; no usar contraseña SSH. |

Oracle ofrece hasta 2 OCPU y 12 GB de RAM totales para A1 Always Free, o hasta dos VMs AMD `VM.Standard.E2.1.Micro` de 1 GB. Oracle puede reclamar una VM Always Free si durante siete días cumple simultáneamente sus umbrales de inactividad; no existe garantía de que una VM totalmente abandonada permanezca disponible. [20]

En **Networking → Network Security Groups** o en la security list de la subnet, permite solamente:

| Puerto | Origen | Uso |
|---|---|---|
| 22/TCP | Tu IP pública `/32` si es posible | SSH administrativo |
| 80/TCP | `0.0.0.0/0` | Redirección HTTP a HTTPS o validación del dominio |
| 443/TCP | `0.0.0.0/0` | HTTPS del reverse proxy |

No abras el puerto `20128`, `20129`, `20132`, `6379`, `6333`, `8080` ni ningún puerto auxiliar a Internet.

### 3. Conectarse y preparar Ubuntu

Desde tu computadora, usa la clave privada correspondiente a la pública que subiste:

```bash
chmod 600 ~/.ssh/omniroute_oracle
ssh -i ~/.ssh/omniroute_oracle ubuntu@IP_PUBLICA
```

En la VM:

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y ca-certificates curl gnupg ufw fail2ban openssl jq
```

Instala Docker Engine desde el repositorio oficial:

```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo \"$VERSION_CODENAME\") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo systemctl enable --now docker
```

Configura el firewall del sistema. Primero permite SSH para no bloquear la sesión actual:

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable
sudo systemctl enable --now fail2ban
sudo ufw status verbose
```

### 4. Crear el archivo `.env` con secretos únicos

Crea la carpeta de instalación y un directorio de datos con permisos para el usuario no root del contenedor:

```bash
sudo mkdir -p /opt/omniroute/data /opt/omniroute/backups
sudo chown -R 1000:1000 /opt/omniroute/data
sudo chmod 700 /opt/omniroute /opt/omniroute/data /opt/omniroute/backups
```

Genera el `.env` sin pegar secretos reales en el repositorio. El siguiente comando crea contraseñas hexadecimales seguras para el piloto:

```bash
sudo bash -c 'cat > /opt/omniroute/.env <<EOF
JWT_SECRET=$(openssl rand -hex 32)
INITIAL_PASSWORD=$(openssl rand -hex 18)
API_KEY_SECRET=$(openssl rand -hex 32)
STORAGE_ENCRYPTION_KEY=$(openssl rand -hex 32)
STORAGE_ENCRYPTION_KEY_VERSION=v1
MACHINE_ID_SALT=$(openssl rand -hex 32)
OMNIROUTE_WS_BRIDGE_SECRET=$(openssl rand -hex 32)
NODE_ENV=production
PORT=20128
HOSTNAME=0.0.0.0
DATA_DIR=/app/data
APP_LOG_TO_FILE=true
AUTH_COOKIE_SECURE=true
REQUIRE_API_KEY=true
CORS_ALLOW_ALL=false
BASE_URL=http://127.0.0.1:20128
NEXT_PUBLIC_BASE_URL=https://llms.TU-DOMINIO.com
OMNIROUTE_PUBLIC_BASE_URL=https://llms.TU-DOMINIO.com
CALL_LOG_RETENTION_DAYS=7
APP_LOG_RETENTION_DAYS=7
ARENA_ELO_SYNC_ENABLED=false
OMNIROUTE_DISABLE_BACKGROUND_SERVICES=1
OMNIROUTE_DISABLE_CREDENTIAL_HEALTH_CHECK=true
OMNIROUTE_MEMORY_MB=2048
EOF
chmod 600 /opt/omniroute/.env'
```

Sustituye `llms.TU-DOMINIO.com` por tu dominio real antes de iniciar el contenedor. Guarda el valor de `INITIAL_PASSWORD` en un gestor de contraseñas; puedes consultarlo una sola vez con `sudo grep '^INITIAL_PASSWORD=' /opt/omniroute/.env` y luego limpiar el historial de la terminal. La guía oficial de OmniRoute exige secretos únicos y utiliza `/app/data` para SQLite y configuración cifrada. [18]

No añadas `GROQ_API_KEY` ni `GEMINI_API_KEY` al `.env`: desde OmniRoute v3.8 las credenciales de providers se gestionan desde el dashboard y se almacenan en el sistema cifrado de datos. Añádelas únicamente desde **Providers** después de activar HTTPS. [21]

### 5. Ejecutar OmniRoute con almacenamiento persistente

La imagen pública consultada ofrece manifiestos `linux/amd64` y `linux/arm64`. El digest siguiente corresponde a la imagen `latest` consultada el 19 de agosto de 2026; vuelve a comprobarlo si la etiqueta ha cambiado antes de desplegar. [19]

```bash
IMAGE='docker.io/diegosouzapw/omniroute@sha256:2bf79cf167478bf283c633ffef2e1e26ba746882e7267fab9320c09df56e8b57'
sudo docker pull "$IMAGE"
sudo docker run -d \\
  --name omniroute \\
  --restart unless-stopped \\
  --env-file /opt/omniroute/.env \\
  -p 127.0.0.1:20128:20128 \\
  -v /opt/omniroute/data:/app/data \\
  "$IMAGE"
```

Comprueba el arranque:

```bash
sudo docker ps --filter name=omniroute
sudo docker logs omniroute --tail 50
curl -fsS http://127.0.0.1:20128/health
```

Debes ver el contenedor activo, la base de datos SQLite lista y una respuesta exitosa de `/health`. Si aparece `permission denied` en `/app/data`, vuelve a aplicar `sudo chown -R 1000:1000 /opt/omniroute/data` y reinicia el contenedor.

### 6. Configurar dominio y HTTPS

Para usar el dashboard desde fuera de la VM necesitas un dominio o subdominio real. La ruta recomendada por la guía de OmniRoute es Cloudflare + Nginx:

1. En el DNS de Cloudflare, crea un registro `A` para `llms` apuntando a la IP pública de Oracle y activa el proxy naranja.
2. En Cloudflare, crea un certificado de origen desde **SSL/TLS → Origin Server**. Guarda el certificado en `/etc/nginx/ssl/origin.crt` y la clave privada en `/etc/nginx/ssl/origin.key`, con permisos `600` para la clave.
3. Instala Nginx:

```bash
sudo apt install -y nginx
sudo mkdir -p /etc/nginx/ssl
sudo chmod 700 /etc/nginx/ssl
```

4. Crea `/etc/nginx/sites-available/omniroute` con esta configuración, sustituyendo el dominio:

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name llms.TU-DOMINIO.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name llms.TU-DOMINIO.com;

    ssl_certificate     /etc/nginx/ssl/origin.crt;
    ssl_certificate_key /etc/nginx/ssl/origin.key;
    ssl_protocols TLSv1.2 TLSv1.3;

    location / {
        proxy_pass http://127.0.0.1:20128;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_buffering off;
        proxy_cache off;
        proxy_read_timeout 600s;
        proxy_send_timeout 600s;
    }
}
```

5. Activa la configuración y valida Nginx:

```bash
sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/omniroute /etc/nginx/sites-enabled/omniroute
sudo nginx -t
sudo systemctl enable --now nginx
sudo systemctl reload nginx
```

6. En Cloudflare, utiliza **SSL/TLS → Overview → Full (Strict)** y activa **Always Use HTTPS**. Verifica desde cualquier equipo:

```bash
curl -sSI https://llms.TU-DOMINIO.com/health
```

No configures `NEXT_PUBLIC_BASE_URL` con la IP ni con HTTP: OmniRoute utiliza esa variable como origen canónico para callbacks y enlaces públicos. [18]

Si todavía no tienes dominio, no expongas el dashboard. Puedes administrarlo mediante un túnel SSH temporal desde tu computadora:

```bash
ssh -i ~/.ssh/omniroute_oracle -N \\
  -L 20128:127.0.0.1:20128 ubuntu@IP_PUBLICA
```

En ese caso, abre `http://127.0.0.1:20128` y cambia temporalmente `AUTH_COOKIE_SECURE=false`; ejecuta `sudo docker restart omniroute` para aplicar el cambio. Cuando utilices HTTPS público, vuelve a `AUTH_COOKIE_SECURE=true`, reinicia el contenedor y no vuelvas a usar la cookie por HTTP. El túnel no ejecuta modelos en tu computadora: solo transporta la interfaz y las solicitudes hacia la VM.

### 7. Primer acceso y conexión con Groq

1. Abre `https://llms.TU-DOMINIO.com`.
2. Inicia sesión con `INITIAL_PASSWORD` y cámbiala inmediatamente.
3. En **API Keys/API Manager**, crea una API key exclusiva para el piloto.
4. En **Providers**, agrega Groq con una API key creada específicamente para esta instancia.
5. Selecciona un model ID visible en el catálogo actual de Groq; no utilices `auto` durante la primera prueba.
6. Prueba desde la VM o desde tu computadora:

```bash
curl -fsS https://llms.TU-DOMINIO.com/v1/models \\
  -H 'Authorization: Bearer TU_OMNIROUTE_API_KEY'

curl -fsS https://llms.TU-DOMINIO.com/v1/chat/completions \\
  -H 'Authorization: Bearer TU_OMNIROUTE_API_KEY' \\
  -H 'Content-Type: application/json' \\
  -d '{
    "model": "MODEL_ID_VISIBLE_EN_GROQ",
    "messages": [{"role":"user","content":"Responde únicamente: OK"}],
    "max_tokens": 16
  }'
```

Usa prompts sintéticos o públicos. No envíes tokens de Meta, datos de seguidores, comentarios reales, datasets crudos ni documentos privados a un provider gratuito.

### 8. Backups y actualización

El `.env` y `/opt/omniroute/data` son críticos. Mantén el `.env` en un gestor de contraseñas y respalda solo los datos necesarios de OmniRoute:

```bash
sudo tar -czf /opt/omniroute/backups/omniroute-data-$(date +%F).tgz \\
  -C /opt/omniroute data
sudo chmod 600 /opt/omniroute/backups/*.tgz
```

Descarga periódicamente el backup fuera de la VM:

```bash
scp -i ~/.ssh/omniroute_oracle \\
  ubuntu@IP_PUBLICA:/opt/omniroute/backups/omniroute-data-AAAA-MM-DD.tgz \\
  ./
```

Para actualizar sin perder la configuración:

```bash
IMAGE='docker.io/diegosouzapw/omniroute@sha256:NUEVO_DIGEST_VERIFICADO'
sudo docker pull "$IMAGE"
sudo docker stop omniroute
sudo docker rm omniroute
sudo docker run -d \\
  --name omniroute \\
  --restart unless-stopped \\
  --env-file /opt/omniroute/.env \\
  -p 127.0.0.1:20128:20128 \\
  -v /opt/omniroute/data:/app/data \\
  "$IMAGE"
sudo docker logs omniroute --tail 50
```

No uses `latest` en una actualización de producción sin revisar primero el cambio. Conserva el digest anterior y el backup hasta verificar `/health`, login, providers y `/v1/models`.

### 9. Mantenimiento y diagnóstico

Usa estos comandos mensualmente:

```bash
sudo docker stats --no-stream omniroute
free -m
df -h
sudo ufw status verbose
sudo systemctl status docker nginx fail2ban --no-pager
```

Si Oracle muestra que la VM puede considerarse inactiva, no generes tráfico artificial únicamente para evitar la reclamación. Usa la VM de forma real para el piloto, registra actividad operativa y conserva backups. Oracle puede reclamar una instancia que cumpla sus umbrales de inactividad durante siete días. [20]

Los problemas más comunes son los siguientes:

| Síntoma | Corrección |
|---|---|
| `out of host capacity` al crear A1 | Probar otro availability domain de la home region o esperar; no activar un plan de pago automáticamente. |
| No hay respuesta en `/health` | Revisar `sudo docker logs omniroute`, `sudo docker ps` y que Nginx apunte a `127.0.0.1:20128`. |
| Error 502 en el dominio | Comprobar que el contenedor esté activo, que el certificado y `proxy_pass` sean correctos y que el puerto 20128 no esté abierto directamente. |
| No se puede escribir en SQLite | Aplicar `sudo chown -R 1000:1000 /opt/omniroute/data` y reiniciar el contenedor. |
| Login no funciona detrás del túnel SSH | Usar temporalmente `AUTH_COOKIE_SECURE=false` solo en acceso HTTP local; volver a `true` con HTTPS. |
| Se consume demasiada RAM | Mantener `OMNIROUTE_DISABLE_BACKGROUND_SERVICES=1`, reducir `OMNIROUTE_MEMORY_MB`, limitar solicitudes pesadas y no activar perfiles web/CLI. |

Oracle es la mejor opción gratuita persistente si aceptas administrar un servidor Linux y logras capacidad para A1 o E2 Micro en la home region. Es gratuito solo dentro de los recursos Always Free y no elimina los deberes de seguridad, backup, actualización ni supervisión. Railway sigue siendo más sencillo para un trial, pero no es gratuito permanente. Si Oracle no ofrece ninguna forma gratuita, la alternativa permanente más cercana es Google Cloud Compute Engine e2-micro en `us-west1`, `us-central1` o `us-east1`, con 30 GB-mes de disco estándar y 1 GB de salida mensual desde Norteamérica dentro de los límites del nivel gratuito; requiere configurar otra cuenta de nube y aceptar sus propias condiciones de facturación. [23]

## Paso 11: criterios de aceptación y cierre

El piloto de bajo consumo se considera correctamente configurado cuando se cumplen todos estos criterios:

| Control | Resultado requerido |
|---|---|
| Red | OmniRoute escucha solo en `127.0.0.1` o `localhost`; el provider cloud es el único destino externo aprobado. |
| Autenticación | El dashboard tiene contraseña cambiada y `/v1` rechaza solicitudes sin API key. |
| Consumo | Se ha fijado `OMNIROUTE_MEMORY_MB` según el entorno —`512` en free tiers pequeños o `2048` en la VM Oracle A1 de 6 GB—, se usan prompts cortos y no hay solicitudes simultáneas. |
| Proveedores | Solo Groq está conectado durante la primera fase; Gemini se añade únicamente para una comparación explícita. |
| Datos | Todas las pruebas iniciales usan prompts sintéticos o públicos. |
| Trazabilidad | Se registran versión, provider, model ID, fecha, latencia aproximada y resultado revisado. |
| Fallback | No se usa `auto` mientras existan providers no aprobados. |
| Secretos | `.env`, API key y contraseña no aparecen en Git, capturas, logs compartidos ni documentos. |
| Reversibilidad | Se conoce la ubicación de `DATA_DIR` y se puede detener OmniRoute sin afectar el dashboard social. |

Para cerrar el piloto, detener OmniRoute con `Ctrl+C`, revisar y conservar solo los artefactos de evaluación necesarios, revocar o eliminar la API key del gateway, eliminar las claves de los providers cloud y borrar la carpeta `DATA_DIR` si no se necesita conservar el historial. Si se usa directamente el Playground por limitación de hardware, cerrar la sesión y revocar la clave desde el panel del provider.

## Solución de problemas

| Síntoma | Diagnóstico y corrección |
|---|---|
| `npm install` rechaza la versión de Node | Actualizar a Node `>=22.22.2 <23` o `>=24.0.0 <27`; no ignorar la restricción del paquete. [9] |
| OmniRoute no inicia o ralentiza mucho el equipo | Revisar `.env`, bajar la carga, mantener `OMNIROUTE_MEMORY_MB=512` y cerrar otras aplicaciones. Si sigue lento, usar directamente el Playground o API del provider. |
| El provider no responde | Probar la API oficial del provider directamente, revisar la clave, la URL `https://api.groq.com/openai/v1` y la cuota vigente. |
| El model ID no aparece | Consultar el catálogo actual del provider; no reutilizar nombres antiguos. Groq publica `/v1/models` para los IDs activos. [11] |
| OmniRoute devuelve `401` | Incluir `Authorization: Bearer PILOT_KEY`; la API key de OmniRoute es distinta de la API key del provider. [8] |
| Aparece un provider no aprobado en los logs | Detener la prueba, desconectar el provider y reemplazar `auto` por el model ID explícito del único provider aprobado. |
| La respuesta tarda demasiado o devuelve `429` | Reducir `max_tokens`, espaciar solicitudes y revisar los límites de RPM, RPD, TPM y TPD del plan. [11] |

## Cambios requeridos en documentos relacionados

Este runbook actualiza la opción a un **piloto cloud-first de bajo consumo** dentro de la decisión de OmniRoute. OmniRoute sigue fuera del pipeline canónico de métricas y no debe convertirse en fuente maestra.

Si el piloto se convierte en una función compartida, se deberán actualizar el documento de decisión, [`2026-08-19_Actualizacion_Asistida_Dashboard_Social.md`](2026-08-19_Actualizacion_Asistida_Dashboard_Social.md) y [`../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md`](../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md). La actualización deberá declarar que los prompts y respuestas son derivados revisables, no evidencia maestra, y deberá añadir un registro de modelo, provider, versión, fecha y dataset de entrada.

## Referencias

[1]: [Ollama — Quickstart oficial](https://docs.ollama.com/quickstart)

[2]: [Ollama — API local oficial](https://docs.ollama.com/api/introduction)

[3]: [Ollama — compatibilidad oficial con OpenAI API](https://docs.ollama.com/api/openai-compatibility)

[4]: [Google — Gemini API Additional Terms of Service](https://ai.google.dev/gemini-api/terms)

[5]: [OmniRoute — Free Tiers Guide](https://raw.githubusercontent.com/diegosouzapw/OmniRoute/release/v3.8.50/docs/getting-started/FREE-TIERS-GUIDE.md)

[6]: [OmniRoute — Provider Reference v3.8.50](https://raw.githubusercontent.com/diegosouzapw/OmniRoute/release/v3.8.50/docs/reference/PROVIDER_REFERENCE.md)

[7]: [Groq — Services Agreement](https://console.groq.com/docs/legal/services-agreement)

[8]: [OmniRoute — Quick Start v3.8.50](https://raw.githubusercontent.com/diegosouzapw/OmniRoute/release/v3.8.50/docs/getting-started/QUICK-START.md)

[9]: [OmniRoute — package.json v3.8.50](https://raw.githubusercontent.com/diegosouzapw/OmniRoute/release/v3.8.50/package.json)

[10]: [Ollama — model library](https://ollama.com/library)

[11]: [Groq — Supported Models and Rate Limits](https://console.groq.com/docs/models)

[12]: [Google — Gemini Developer API pricing](https://ai.google.dev/gemini-api/docs/pricing)

[13]: [Render — Deploy for Free](https://render.com/docs/free)

[14]: [Render — Web Services and instance types](https://render.com/docs/web-services)

[15]: [Railway — Free Trial and Free plan](https://docs.railway.com/pricing/free-trial)

[16]: [Railway — Volumes](https://docs.railway.com/volumes)

[17]: [Railway — Public Networking](https://docs.railway.com/networking/public-networking)

[18]: [OmniRoute — VM Deployment Guide](https://raw.githubusercontent.com/diegosouzapw/OmniRoute/release/v3.8.50/docs/ops/VM_DEPLOYMENT_GUIDE.md)

[19]: [Docker Hub — OmniRoute image](https://hub.docker.com/r/diegosouzapw/omniroute)

[20]: [Oracle Cloud — Always Free Resources](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm)

[21]: [OmniRoute — Environment Variables v3.8.50](https://raw.githubusercontent.com/diegosouzapw/OmniRoute/release/v3.8.50/docs/reference/ENVIRONMENT.md)

[22]: [Oracle — Managing Regions](https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/managingregions.htm)

[23]: [Google Cloud — Free Program and Compute Engine e2-micro](https://cloud.google.com/free/docs/free-cloud-features)

[24]: [Oracle Cloud Free Tier — FAQ](https://www.oracle.com/cloud/free/faq/)

[25]: [Oracle — Deleting a Free Tier Tenancy and Cloud Account](https://docs.oracle.com/en-us/iaas/Content/General/Tasks/deleting_tenancy_freetier.htm)

[26]: [Google Cloud — Create and start a Compute Engine instance](https://cloud.google.com/compute/docs/instances/create-start-instance)

[27]: [Google Cloud — Create, edit, or delete budgets and budget alerts](https://cloud.google.com/billing/docs/how-to/budgets)

[28]: [Google Cloud — Network pricing and external IP addresses](https://cloud.google.com/vpc/network-pricing)

[29]: [Google Cloud — Connect to Linux VMs using Identity-Aware Proxy](https://cloud.google.com/compute/docs/connect/ssh-using-iap)

[30]: [Google One — Google AI Plans](https://one.google.com/about/google-ai-plans/)

[31]: [Google Cloud — Google Developer Program Premium GenAI Credit SKU Group](https://cloud.google.com/skus/sku-groups/google-developer-program-premium-genai-credit)
