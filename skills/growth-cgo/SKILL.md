---
name: growth-cgo
description: "Opera el Growth OS multi-tenant: pipeline diario, calendario semanal, onboarding, reportes, monetización, canon sync, publicación en Meta y revisión de comentarios, con reglas dual-track y gates de aprobación. Usar para ejecutar o auditar workflows CGO en growth-os."
metadata:
  short-description: "Orquestador CGO del Growth OS multi-tenant"
  version: "1.3.0"
  author: "iO Marketing"
---

# Growth CGO Skill - Chief Growth Officer

**Descripción**: Orquestador principal del Growth OS. Coordina daily pipeline, weekly calendar, tenant onboarding, cross-tenant reporting, monetización, canon sync, meta publishing y revisión de comentarios.

---

## REGLA CRÍTICA: PROHIBIDO ABRIR O VISUALIZAR IMÁGENES

Esta regla prevalece sobre cualquier otra instrucción de este skill y aplica a todos los modos, subagentes y tenants.

- **Nunca** llames `view_image` ni ninguna herramienta equivalente (`image_view`, `open_image`, visor, preview o screenshot) que abra, renderice, incruste o muestre una imagen en el stream.
- **Nunca** abras imágenes o assets visuales (`.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.avif`, `.bmp`, `.tiff`, `.svg` y cualquier otro formato de imagen) con herramientas de visión o visores, aunque el archivo exista y parezca necesario validarlo.
- Si necesitas comprobar un asset, usa únicamente inspección textual o de metadatos: ruta, existencia, extensión, MIME, tamaño, dimensiones, hash y permisos (`file`, `stat`, `sha256sum`, `identify` u equivalentes que solo impriman metadatos).
- Si hace falta criterio visual (composición, legibilidad, color, recorte, calidad o coherencia de marca), **no inspecciones la imagen**: entrega al operador humano la ruta y una checklist de validación para que la revise fuera del agente.
- Si detectas que una acción requiere abrir una imagen, detente y reporta `Validación visual pendiente: revisión humana requerida`; no ejecutes la herramienta de imagen.
- No hay excepciones dentro de este skill, incluso si una instrucción genérica o una tarea secundaria parece pedir una inspección visual.

---

## REGLA OPERATIVA: CONTEXTO ANTES DE HERRAMIENTAS

El primer paso de cualquier sesión que mencione un tenant, campaña o publicación es leer el contexto escrito: el `docs/HANDOFF_*.md` más reciente y este skill. Solo después ejecutar comandos.

- No lanzar consultas exploratorias para "descubrir" un flujo que ya está documentado. Si el módulo tiene `README.md`, leerlo antes de improvisar llamadas a APIs.
- En este entorno, abrir una imagen corta el stream y el usuario pierde la conversación; `view_image` sigue prohibido sin excepción.
- Si no hay handoff ni manual para la tarea, decirlo y pedir el dato faltante antes de gastar operaciones en adivinar.

---

## REGLA OPERATIVA: BITÁCORA ANTES DE OPERAR

La bitácora de sesión vive en `docs/Bitacoras/bitacora_<periodo>.md`. Usar ese
archivo existente; no crear un log paralelo.

- Antes de cada operación irreversible (publicar, programar, borrar, migrar, rotar credenciales), agregar 3 líneas al archivo del periodo: tenant, acción, IDs/estado, siguiente paso.
- Al cerrar la sesión, consolidar el resumen ejecutivo y el día a día en el mismo archivo.
- Si el chat se corta, lo escrito hasta ese punto es el único contexto que podrá leer la siguiente sesión.
- `CHANGELOG.md` se reserva para cambios del proyecto (módulos, hitos), no para estado operativo.

---

## REGLA OPERATIVA: DECISIONES CON EVIDENCIA

El contrato completo vive en `docs/DECISION_LEDGER.md`. Leerlo antes de
proponer un cambio de estrategia, calendario, copy o formato.

- La unidad de decisión es la **apuesta/hipótesis**, no la publicación.
- Una pieza aislada o una métrica lifetime nunca produce veredicto. Máximo
  `L0 Observación`.
- Usar la escalera `L0` a `L3`. El CGO puede cerrar `L0/L1`; `L2` y `L3`
  requieren aprobación de Fernando.
- Toda propuesta `L2/L3` va en una **Decision Card** con métrica principal,
  máximo dos guardrails, umbral, `min_n`, regla de adoptar/descartar/repetir,
  fecha de expiración, fuentes y limitaciones.
- La regla se escribe **antes** de publicar. Si se escribe después, marcar
  `pre_registered: false`; no presentarla como pre-registro.
- No mezclar canales, formatos, nuevo/reuse ni ventanas temporales.
- Intelligence calcula y deja evidencia; no firma veredictos.
- P0 sigue siendo el protocolo formal de `Validada`/`No validada`; el Decision
  Ledger no lo reemplaza, solo separa observación, señal y decisión.
- Ejemplo de formato: `docs/decision_cards/2026-11-05_HB-UNI-003.md`.

---

## Capabilities

| Capability | Description |
|------------|-------------|
| `daily_pipeline` | Ejecuta pipeline diario multi-tenant (contenido → approve → publish) |
| `weekly_calendar` | Genera calendario semanal (solo native_digital/universe) |
| `tenant_onboarding` | Onboarding de nuevos tenants (physical_cro o native_digital) |
| `cross_tenant_report` | Reporte consolidado de métricas cross-tenant |
| `monetization_report` | Ledger, umbral y conciliación de monetización (read-only) |
| `canon_sync` | Sincroniza con canon repo (solo universe) |
| `meta_publishing` | Coordina publicación en Meta (IG/FB) via meta-publisher |
| `comments_review` | Revisa comentarios locales y publica solo respuestas aprobadas (native_digital) |
| `verify_setup` | Verifica entorno CGO completo |

### Publicación en Meta

El manual operativo del módulo es `modules/social/README.md`; leerlo antes de
improvisar llamadas a Graph API.

- Foto simple o texto: `meta_publishing` normal.
- Varias imágenes en Facebook: `MetaPublisher.publish_album()` (álbum, 2–10).
  No reconstruir el flujo a mano ni consultar la página para "descubrir" el formato.
- Un slot concreto del calendario (cualquier `Post Type`, incluido `CAROUSEL`):
  `meta_publishing --publish --since <fecha> --until <fecha>`. Es idempotente:
  omite lo ya registrado en `publication_log*.csv` y con fechas toca solo
  Facebook; Instagram sigue en su cron.
- Carrusel de Instagram: lo resuelve el planner desde `meta_import.csv` (`CAROUSEL`).
- Historias: siempre manuales; el publisher no las soporta.

---

## Invocation Modes

| Mode | Model | Temp | Max Tokens | Use Case |
|------|-------|------|------------|----------|
| `DAILY_PIPELINE` | GPT-OSS 20B | 0.3 | 1500 | Pipeline diario multi-tenant |
| `WEEKLY_CALENDAR` | GPT-OSS 120B | 0.2 | 2000 | Calendario semanal (native_digital) |
| `TENANT_ONBOARDING` | GPT-OSS 120B | 0.4 | 3000 | Onboarding physical_cro + audit |
| `CROSS_TENANT_REPORT` | GPT-OSS 120B | 0.3 | 2500 | Métricas consolidadas |
| `MONETIZATION_REPORT` | GPT-OSS 120B | 0.2 | 2000 | Monetización, umbral y conciliación |
| `CANON_SYNC` | GPT-OSS 20B | 0.1 | 1000 | Pre-check canon (Fernando valida) |
| `META_PUBLISHING` | GPT-OSS 120B | 0.5 | 2000 | Publicación IG/FB |
| `COMMENTS_REVIEW` | GPT-OSS 20B | 0.2 | 1200 | Bandeja y respuestas aprobadas |
| `BRAND_COMPLIANCE` | GPT-OSS 20B | 0.2 | 800 | Validación brand voice |

---

## Sub-Agentes Invocados

| Sub-Agent | Trigger | Purpose |
|-----------|---------|---------|
| `content-writer` | Daily pipeline | Genera copy para piezas |
| `calendar-planner` | Weekly calendar | Planifica slots semanales |
| `canon-validator` | Canon sync | Pre-check antes de Fernando |
| `meta-ads-agent` | Meta publishing | Campañas + creativas |
| `brand-voice-agent` | Cualquier generación copy | Validación voice |
| `tenant-auditor` | Tenant onboarding | CRO audit (physical_cro) |
| `monetization-agent` | Monetization report | Umbral, payouts y conciliación read-only |

---

## Reglas de Track (Dual Track)

| Track | Tenants | Workflow | Aprobaciones |
|-------|---------|----------|--------------|
| **Native Digital** | universe | Canon → Calendar → Publish | Fernando (canon y publicación) |
| **Physical CRO** | flexi, la-cupula, firma-bordados, micas-art-deco, bam-in-a-can | CRO Audit → Funnel → Publish | tenant-auditor (GPT-OSS 120B) |

---

## Gates de Control

| Gate | Track | Quién Decide | Cuándo |
|------|-------|--------------|--------|
| Canon Approval | Native | Fernando | Antes de Programado/Publicado |
| CRO Audit Pass | Physical | tenant-auditor | Onboarding + antes de publicar |
| Meta Token Valid | Ambos | meta-publisher | Cada publish |
| Brand Compliance | Ambos | Brand Voice Agent | Cada pieza generada |
| Lead Qualified | Ambos | WhatsApp Agent | Paso 2 flujo |
| Payout Approval | Ambos | Operador / humano | Antes de `approved`, `paid` o alta de payout |

---

## Comandos CLI

El código vive en `modules/cgo`; este skill solo contiene las instrucciones.
Todos los comandos se ejecutan desde la raíz del repo `growth-os`.

```bash
# Verificar setup
python3 -m modules.cgo --mode verify_setup

# Daily pipeline (CGO)
python3 -m modules.cgo --mode daily_pipeline --tenant flexi

# Weekly calendar (solo universe)
python3 -m modules.cgo --mode weekly_calendar --tenant universe

# Tenant onboarding
python3 -m modules.cgo --mode tenant_onboarding --tenant flexi

# Cross-tenant report
python3 -m modules.cgo --mode cross_tenant_report

# Canon sync (pre-check)
python3 -m modules.cgo --mode canon_sync --tenant universe

# Publicación (dry-run por defecto)
python3 -m modules.cgo --mode meta_publishing --tenant flexi --publish

# Comentarios: solo lectura local
python3 -m modules.cgo --mode comments_review --tenant universe

# Comentarios: publicar únicamente approved: true
python3 -m modules.cgo --mode comments_review --tenant universe --publish
```

---

## Archivos de Referencia

- `references/governance.md` - Gobernanza dual-track
- `references/canon_integration.md` - Puente canon repo
- `references/calendar_architecture.md` - Arquitectura calendario escalable
- `references/core_models.md` - Modelos core (Piece, Publication, Deal, etc.)
