# Piloto de bajo consumo de OmniRoute

**Propósito:** Definir un procedimiento reproducible para probar OmniRoute en una computadora de baja potencia, ejecutando únicamente el gateway local y enviando las solicitudes a un proveedor cloud con API oficial, sin descargar ni ejecutar modelos localmente.

**Estado:** Review

**Fecha de creación:** 2026-08-18

**Última actualización:** 2026-08-19

**Versión:** 1.3

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

## Paso 10: alojar OmniRoute fuera de la computadora

### Decisión rápida

| Plataforma | ¿Es gratuita? | Persistencia de OmniRoute | Veredicto para este piloto |
|---|---|---|---|
| Render Free | Sí, con límites | No: el filesystem es efímero y se pierde la SQLite al reiniciar, redeployar o suspender; el servicio se suspende tras 15 minutos sin tráfico. [13] [14] | **Solo demo temporal**, no recomendada para conservar providers y configuración. |
| Railway | Trial de 5 USD por hasta 30 días; después, plan Free con 1 USD/mes de crédito | Sí mediante volumen en `/app/data`, pero los volúmenes de cuentas trial se eliminan 30 días después de expirar los créditos. [15] [16] | **Mejor para una prueba de 30 días**, no gratis permanente. |
| Oracle Cloud Always Free | Sí, mientras se mantengan las condiciones de Always Free | Sí, mediante el disco de la VM; exige administrar Linux, Docker, firewall, dominio y backups. [20] | **Mejor alternativa gratuita persistente**, pero requiere más trabajo técnico y puede sufrir falta de capacidad o reclamación por inactividad. |

Para tu caso, la recomendación es **Railway si quieres probarlo rápidamente durante el trial** y **Oracle Cloud Always Free si necesitas dejarlo funcionando sin pagar mensualmente**. Render Free es el camino más sencillo visualmente, pero su pérdida de SQLite hace que OmniRoute olvide la configuración de providers después de un reinicio o suspensión. Además, la instancia gratuita de Render ofrece 512 MB de RAM y 0,1 CPU, mientras que la guía de OmniRoute recomienda como mínimo una VM de 1 GB para un despliegue persistente. [14] [18]

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

### Opción C: Oracle Cloud Always Free para persistencia gratuita

Oracle ofrece una VM Always Free con recursos persistentes durante la vida de la cuenta: hasta 2 OCPU y 12 GB de memoria total en Ampere A1, o hasta dos VMs AMD de 1 GB, además de 200 GB de almacenamiento de bloques en la región principal. Oracle puede reclamar instancias inactivas y la creación puede fallar temporalmente por falta de capacidad. [20]

### 1. Crear la cuenta y controlar el coste

1. Abre [Oracle Cloud Free](https://www.oracle.com/cloud/free/) y completa el registro. La cuenta puede solicitar verificación de identidad o método de pago según el país; eso no convierte automáticamente los recursos etiquetados como **Always Free Eligible** en recursos de pago.
2. Identifica la **home region** de la tenancy. Las VMs Always Free deben crearse allí. Si la consola muestra `out of host capacity`, no cambies inmediatamente a una forma de pago: prueba otro availability domain de la misma región o espera a que haya capacidad. [20]
3. Crea, si la consola lo permite, un compartment llamado `omniroute-free` y utiliza únicamente recursos que muestren la etiqueta **Always Free Eligible**. No crees Load Balancer, NAT Gateway, bases de datos de pago, discos fuera de la home region ni IPs o servicios adicionales sin revisar el coste.
4. No actives Pay As You Go solo para resolver `out of host capacity`. Oracle indica que los recursos Always Free siguen sin cargo después de una actualización, pero cualquier recurso que exceda los límites gratuitos sí puede generar cargos. Las cuotas de compartment ayudan a limitar el consumo. [20]

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

Oracle es la mejor opción gratuita persistente si aceptas administrar un servidor Linux. Es gratuito solo dentro de los recursos Always Free y no elimina los deberes de seguridad, backup, actualización ni supervisión. Railway sigue siendo más sencillo para un trial, pero no es gratuito permanente.

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
