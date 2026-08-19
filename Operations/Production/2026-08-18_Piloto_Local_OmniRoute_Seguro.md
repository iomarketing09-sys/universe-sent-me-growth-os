# Piloto de bajo consumo de OmniRoute

**Propósito:** Definir un procedimiento reproducible para probar OmniRoute en una computadora de baja potencia, ejecutando únicamente el gateway local y enviando las solicitudes a un proveedor cloud con API oficial, sin descargar ni ejecutar modelos localmente.

**Estado:** Review

**Fecha de creación:** 2026-08-18

**Última actualización:** 2026-08-19

**Versión:** 1.1

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

## Paso 8: probar el caso de Universe Sent Me sin datos reales

Durante la primera sesión, utilizar únicamente prompts sintéticos. No pegar capturas privadas, datos de Windsor, tokens de Meta, nombres de seguidores, comentarios reales, IDs de publicaciones ni documentos internos.

Una batería mínima puede contener cinco prompts: una variante de copy breve, una clasificación de formato, una lectura narrativa de números inventados, una traducción y una petición de ideas para una escena de Universe. Para cada prueba registrar fecha, versión de OmniRoute, provider, model ID, tiempo aproximado, resultado y observaciones en un archivo de evaluación dentro de `Operations/Research/`; no registrar secretos ni datos personales.

El piloto puede comparar un segundo model ID cloud solo si el provider lo ofrece dentro de la cuota gratuita. La calidad debe juzgarse con criterios definidos por el estudio —fidelidad al prompt, claridad, tono, repetición y latencia— y no únicamente por una respuesta llamativa. Si OmniRoute ralentiza demasiado el equipo, continuar la comparación directamente en el Playground del provider y registrar que el gateway fue omitido por limitación de hardware.

## Paso 9: añadir Gemini solo como comparación opcional

Si se necesita una segunda opinión, añadir **un solo provider adicional** y mantenerlo separado de Groq. Para Gemini, crear una clave independiente en Google AI Studio y usar únicamente prompts sintéticos o públicos. La documentación de precios indica que el nivel gratuito tiene tokens sin costo, pero también marca que el contenido se utiliza para mejorar productos; por tanto, no utilizar el provider gratuito con contenido confidencial de Universe Sent Me. [4] [12]

Después de conectar Gemini, no utilizar `model: "auto"` para esta comparación. Seleccionar explícitamente el model ID que aparezca disponible en el catálogo, revisar los logs después de cada solicitud y desconectar la credencial al terminar. Si el equipo se vuelve lento, detener OmniRoute antes de continuar y usar directamente el Playground de Gemini.

Groq debe tratarse como una ruta cloud controlada, no como una ruta privada local. Aunque sus términos describen restricciones sobre el uso de inputs y outputs, el prompt sale del equipo y se aplican también los términos de cada model provider. [7]

## Paso 10: criterios de aceptación y cierre

El piloto de bajo consumo se considera correctamente configurado cuando se cumplen todos estos criterios:

| Control | Resultado requerido |
|---|---|
| Red | OmniRoute escucha solo en `127.0.0.1` o `localhost`; el provider cloud es el único destino externo aprobado. |
| Autenticación | El dashboard tiene contraseña cambiada y `/v1` rechaza solicitudes sin API key. |
| Consumo | Se ha fijado `OMNIROUTE_MEMORY_MB=512`, se usan prompts cortos y no hay solicitudes simultáneas. |
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
