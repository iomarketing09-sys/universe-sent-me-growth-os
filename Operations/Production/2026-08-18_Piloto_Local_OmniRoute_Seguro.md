# Piloto local seguro de OmniRoute

**Propósito:** Definir un procedimiento reproducible para probar OmniRoute en una máquina local con modelos gratuitos, priorizando una ruta local mediante Ollama y evitando exponer credenciales, datos del estudio o el panel administrativo a Internet.

**Estado:** Review

**Fecha de creación:** 2026-08-18

**Última actualización:** 2026-08-18

**Versión:** 1.0

**Autor:** Manus AI

**Organización:** `Operations/Production`

**Documentos relacionados:** [`2026-08-19_Decision_Gateway_IA_OmniRoute.md`](2026-08-19_Decision_Gateway_IA_OmniRoute.md), [`2026-08-19_Actualizacion_Asistida_Dashboard_Social.md`](2026-08-19_Actualizacion_Asistida_Dashboard_Social.md), [`../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md`](../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md).

---

## Decisión de seguridad

Para el primer piloto, la opción más segura no es un proveedor cloud gratuito, sino un **modelo descargado y ejecutado localmente**. OmniRoute registra a Ollama como proveedor `ollama-local`, con base URL OpenAI-compatible `http://localhost:11434/v1` y sin API key de proveedor; Ollama documenta que su API local está disponible en `http://localhost:11434/api` y que ofrece compatibilidad parcial con `/v1/chat/completions`. [1] [2] [3]

Esto reduce el riesgo de que los prompts del piloto lleguen a un tercero, aunque no elimina todos los riesgos: el equipo local conserva los prompts, OmniRoute conserva configuración y logs, y los pesos de los modelos se descargan desde Internet durante la instalación. La ruta local tampoco garantiza una calidad determinada; se debe medir cada modelo con una muestra revisada.

Los proveedores cloud gratuitos quedan como **segunda etapa y solo para datos sintéticos o públicamente compartibles**. Por ejemplo, los términos de los servicios no pagados de Gemini indican que Google puede utilizar entradas y respuestas para mejorar y desarrollar productos, y que revisores humanos pueden leerlas; además, prohíben enviar información sensible, confidencial o personal a esos servicios. [4] Por este motivo, Gemini gratuito no debe recibir datos internos de Universe Sent Me durante este piloto.

Tampoco se recomienda empezar con Kiro, OpenCode Free, proveedores web-cookie, agregadores o endpoints no-auth de procedencia incierta. La propia documentación de OmniRoute marca Kiro y OpenCode Free con advertencia `avoid` en su catálogo de términos, y señala que `NOAUTH` solo describe la ausencia de una credencial, no la privacidad, disponibilidad o autorización para usar un proxy. [5] [6]

> **Orden recomendado:** primero Ollama local; después, si hace falta comparar calidad, un proveedor cloud documentado con una clave separada y prompts sintéticos; nunca comenzar con `model: auto` si existen proveedores no aprobados conectados.

## Matriz de proveedores para el piloto

| Nivel | Proveedor o ruta | Datos que pueden enviarse | Motivo | Estado |
|---|---|---|---|---|
| 1 | `ollama-local` con un modelo local | Prompts de prueba y, después de revisión, datos internos no sensibles | La inferencia ocurre en el equipo local; no requiere una credencial cloud. | **Recomendado** |
| 2 | Gemini API con cuota gratuita | Solo prompts sintéticos o públicos; nunca secretos, datos personales ni información confidencial | API documentada y fácil de comparar, pero la política de servicios no pagados permite uso para mejora y revisión humana. [4] | **Opcional, con cautela** |
| 3 | Groq API con cuota gratuita | Solo prompts sintéticos o públicos, después de revisar cuota y términos vigentes | API documentada y apta para integraciones, pero siguen aplicando términos del modelo y límites del plan. [7] | **Opcional, con cautela** |
| Evitar en la primera etapa | Kiro, OpenCode Free, Pollinations, proveedores web-cookie y agregadores | Ningún dato del proyecto | El modelo de autenticación, los términos de proxy o la procedencia del endpoint requieren una revisión adicional. [5] [6] | **No conectar** |

La etiqueta **“más seguro” es relativa**. No constituye una certificación legal, de privacidad ni de calidad del proveedor. Antes de mover el piloto a un flujo compartido, se deben revisar de nuevo los términos, la política de datos, los límites y la disponibilidad de cada servicio.

## Requisitos previos

El paquete de OmniRoute `v3.8.50` declara Node.js `>=22.22.2 <23` o `>=24.0.0 <27`. La guía rápida ofrece instalación mediante npm, Docker o código fuente; para un piloto local reversible se utilizará npm con la versión fijada, sin abrir puertos públicos. [8] [9]

También se requiere Ollama instalado desde su [sitio oficial](https://ollama.com/download). Ollama funciona en macOS, Windows y Linux; después de instalarlo, su API local usa por defecto el puerto `11434`. [1] [2]

Antes de comenzar, comprobar en una terminal:

```bash
node --version
npm --version
ollama --version
```

Si Node.js es inferior a `22.22.2`, actualizarlo antes de instalar OmniRoute. No se debe forzar la instalación ignorando la restricción de engine del paquete.

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

## Paso 2: descargar un modelo local de tamaño razonable

Como primera prueba de texto, utilizar un modelo pequeño que el equipo pueda ejecutar sin saturarse. Por ejemplo:

```bash
ollama pull llama3.2:3b
ollama list
```

La biblioteca oficial de Ollama también incluye familias como `qwen3`, `gemma4`, `qwen3-vl` y `gemma3`; elegir una variante pequeña que el equipo pueda cargar y consultar con fluidez. Para una prueba visual, la compatibilidad depende de la versión del modelo y del flujo de imagen, por lo que primero se debe validar texto con `llama3.2:3b` o un modelo equivalente. [10]

Comprobar que Ollama está respondiendo localmente:

```bash
curl http://127.0.0.1:11434/api/tags
```

Si la respuesta indica que el servicio no está disponible, iniciar Ollama desde su aplicación de escritorio. En Linux, iniciar el servicio con el mecanismo recomendado por la instalación o ejecutar `ollama serve` en una terminal separada. No cambiar Ollama a `0.0.0.0` durante este piloto.

## Paso 3: instalar OmniRoute con versión fijada

Instalar exactamente la versión revisada en este runbook:

```bash
npm install --global omniroute@3.8.50
omniroute --version
```

La salida debe indicar `3.8.50`. Fijar la versión evita que una instalación posterior cambie silenciosamente el comportamiento del piloto. Si se necesita evaluar otra versión, debe registrarse como un nuevo experimento y no sustituir esta instalación sin documentarlo.

## Paso 4: crear las variables de entorno locales

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
```

Las variables cumplen cuatro funciones del piloto. Los secretos protegen el dashboard y las claves almacenadas; `DATA_DIR` mantiene persistente la SQLite; `OMNIROUTE_SERVER_HOST=127.0.0.1` y `CORS_ALLOWED_ORIGINS` mantienen el acceso local; y la desactivación de sincronización Arena y de comprobaciones periódicas evita tráfico auxiliar no necesario mientras se prueba. La referencia de entorno de OmniRoute documenta estos valores y la retención predeterminada de siete días para los logs de llamadas. [9]

No subir `.env` a GitHub, Drive, el inventario de Universe Sent Me ni ninguna herramienta de IA. Añadirlo a un `.gitignore` local:

```bash
printf '%s\n' '.env' 'data/' '*.log' >> .gitignore
```

## Paso 5: iniciar OmniRoute solo en localhost

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

## Paso 6: proteger el dashboard y crear una clave de cliente

1. Abrir `http://127.0.0.1:20128`.
2. Iniciar sesión con la contraseña inicial guardada en el Paso 4.
3. Cambiar inmediatamente esa contraseña desde la sección de seguridad del dashboard.
4. Crear una única API key para el piloto desde **API Keys** o **API Manager**.
5. Guardar la clave en un gestor de contraseñas. La guía de OmniRoute indica que la clave se muestra una sola vez y que es la credencial para que las herramientas llamen a OmniRoute, no la credencial del proveedor ascendente. [8]
6. No activar `ALLOW_API_KEY_REVEAL`, no reutilizar la clave en otra aplicación y no pegarla en una conversación, captura de pantalla o repositorio.

Si el dashboard permite seleccionar scopes, otorgar únicamente el permiso de ejecución de completions que necesite el cliente de prueba. No conceder permisos de administración, escritura de providers, combos o configuración a una herramienta creativa.

## Paso 7: conectar únicamente Ollama local

En el dashboard:

1. Ir a **Providers** → **Add Provider**.
2. Buscar **Ollama**. En la referencia de OmniRoute aparece como `ollama-local`, alias `ollama`.
3. Configurar la base URL OpenAI-compatible como `http://localhost:11434/v1`.
4. Dejar vacía la API key del proveedor si la interfaz lo permite. Ollama no requiere autenticación para el acceso local; OmniRoute sí debe seguir exigiendo la API key propia en su endpoint porque `REQUIRE_API_KEY=true`. [2] [9]
5. Ejecutar **Test Connection**.
6. Confirmar que el catálogo muestre exactamente el modelo que ya aparece en `ollama list`, por ejemplo `llama3.2:3b`.
7. No conectar todavía Kiro, OpenCode Free, Pollinations, proveedores web-cookie, OpenRouter, AgentRouter ni cualquier provider que no haya sido aprobado para este piloto.

El provider ID exacto y el model ID deben tomarse de la respuesta de `GET /v1/models` o del dashboard; no se deben adivinar prefijos. La referencia oficial confirma la base URL y el ID del provider, pero el catálogo visible puede cambiar entre versiones. [6]

## Paso 8: verificar la API de OmniRoute

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

La respuesta debe incluir `choices[0].message.content`. En el dashboard, revisar **Monitoring/Logs** y confirmar que el proveedor elegido sea `ollama-local` y que no exista fallback a un proveedor remoto. OmniRoute documenta que los logs permiten revisar qué información se envió y qué provider atendió la solicitud. [8]

También se puede probar directamente Ollama para separar un problema del modelo de un problema del gateway:

```bash
curl http://127.0.0.1:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2:3b",
    "messages": [{"role":"user","content":"Responde únicamente: OK local"}],
    "max_tokens": 16
  }'
```

## Paso 9: probar el caso de Universe Sent Me sin datos reales

Durante la primera sesión, utilizar únicamente prompts sintéticos. No pegar capturas privadas, datos de Windsor, tokens de Meta, nombres de seguidores, comentarios reales, IDs de publicaciones ni documentos internos.

Una batería mínima puede contener cinco prompts: una variante de copy breve, una clasificación de formato, una lectura narrativa de números inventados, una traducción y una petición de ideas para una escena de Universe. Para cada prueba registrar fecha, versión de OmniRoute, modelo local, tiempo aproximado, resultado y observaciones en un archivo de evaluación dentro de `Operations/Research/`; no registrar secretos ni datos personales.

El piloto debe comparar al menos dos modelos locales solo si el equipo puede ejecutarlos sin degradación importante. La calidad debe juzgarse con criterios definidos por el estudio —fidelidad al prompt, claridad, tono, repetición y latencia— y no únicamente por una respuesta llamativa.

## Paso 10: añadir un proveedor cloud solo como comparación opcional

Si el modelo local no alcanza la calidad necesaria, añadir **un solo proveedor cloud** y mantenerlo separado del flujo local. Para Gemini, crear una clave independiente en Google AI Studio y usar únicamente prompts sintéticos o públicos. Los términos actuales de los servicios no pagados permiten uso de entradas y respuestas para mejorar productos y revisión humana; por tanto, no utilizar el proveedor gratuito con contenido confidencial de Universe Sent Me. [4]

Después de conectar el proveedor cloud, no utilizar `model: "auto"` para esta comparación. Seleccionar explícitamente el model ID del provider cloud desde `GET /v1/models` y revisar los logs después de cada solicitud. Al terminar, desconectar la credencial y borrar la conexión si el proveedor no seguirá aprobado.

La misma regla aplica a Groq: sus términos permiten integrar las APIs en aplicaciones y describen controles para inputs y outputs, pero siguen aplicando las condiciones del servicio, los términos de los modelos y los límites del plan gratuito. [7] No considerar esta ruta privada por el solo hecho de usar una API key.

## Paso 11: criterios de aceptación y cierre

El piloto local se considera correctamente configurado cuando se cumplen todos estos criterios:

| Control | Resultado requerido |
|---|---|
| Red | OmniRoute y Ollama escuchan solo en `127.0.0.1` o `localhost`. |
| Autenticación | El dashboard tiene contraseña cambiada y `/v1` rechaza solicitudes sin API key. |
| Proveedores | Solo `ollama-local` está conectado durante la primera fase. |
| Datos | Todas las pruebas iniciales usan prompts sintéticos o públicos. |
| Trazabilidad | Se registran versión, modelo, fecha, latencia aproximada y resultado revisado. |
| Fallback | No se usa `auto` mientras existan proveedores no aprobados. |
| Secretos | `.env`, API key y contraseña no aparecen en Git, capturas, logs compartidos ni documentos. |
| Reversibilidad | Se conoce la ubicación de `DATA_DIR` y se puede detener OmniRoute sin afectar el dashboard social. |

Para cerrar el piloto, detener OmniRoute con `Ctrl+C`, revisar y conservar solo los artefactos de evaluación necesarios, revocar o eliminar la API key del gateway, desconectar providers cloud si se probaron y mantener Ollama local únicamente si se continuará evaluando. Para liberar espacio, listar y borrar modelos con `ollama rm MODEL_NAME` después de confirmar que no se necesitan.

## Solución de problemas

| Síntoma | Diagnóstico y corrección |
|---|---|
| `npm install` rechaza la versión de Node | Actualizar a Node `>=22.22.2 <23` o `>=24.0.0 <27`; no ignorar la restricción del paquete. [9] |
| OmniRoute no inicia | Revisar que `.env` esté en `omniroute-pilot`, que los cuatro secretos no estén vacíos y que el puerto 20128 esté libre. |
| Ollama no responde | Iniciar la aplicación Ollama o `ollama serve`; comprobar `curl http://127.0.0.1:11434/api/tags`. |
| El modelo no aparece en OmniRoute | Ejecutar `ollama list`, descargarlo con `ollama pull` y volver a probar la conexión del provider. |
| OmniRoute devuelve `401` | Incluir `Authorization: Bearer PILOT_KEY`; la API key de OmniRoute es distinta de la API key del provider. [8] |
| Aparece un provider remoto en los logs | Detener la prueba, desconectar el provider no aprobado y reemplazar `auto` por el model ID local explícito. |
| La respuesta tarda demasiado | Usar un modelo local más pequeño, reducir `max_tokens` y comprobar memoria/CPU; no ampliar el contexto sin medirlo. |

## Cambios requeridos en documentos relacionados

Este runbook concreta la opción de **piloto local** aprobada en [`2026-08-19_Decision_Gateway_IA_OmniRoute.md`](2026-08-19_Decision_Gateway_IA_OmniRoute.md). No modifica el procedimiento de extracción y normalización del dashboard, porque OmniRoute sigue fuera del pipeline canónico de métricas.

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
