# Monetization Lite

Capa de Growth OS para separar **señales de rendimiento**, **estimaciones** y
**dinero realmente pagado**. No es contabilidad, facturación ni cobranza.

## Problema que resuelve

Un post con muchas interacciones no es ingreso. Un estimado de Meta tampoco es
un payout. Sin separar esas capas se duplican cifras y se toman decisiones de
contenido sobre una señal que nunca llegó a cobrarse.

## Tres capas

| Capa | Qué guarda | Fuente | ¿Es ingreso? |
|---|---|---|---|
| `MonetizationSignal` | Observación diaria por publicación: reacciones, comentarios, shares y bonus proxy | JSON de Meta o importación | No |
| `MonetizationPeriod` | Estimado o aprobado por programa y periodo | Manual o reporte de plataforma | No |
| `Payout` | Bruto, fee y neto realmente pagado | Manual o comprobante | Sí, solo si `status=paid` |

## Regla de reconocimiento

- `estimated_net`: suma de periodos `estimated`.
- `approved_unpaid_net`: aprobado menos payouts ya confirmados del mismo periodo.
- `paid_net`: suma de payouts `paid`.
- `recognized_net`: **solo `paid_net`**.
- `pipeline_net`: `estimated_net + approved_unpaid_net`.

Nunca se suman estimado, aprobado y pagado como si fueran tres ingresos.

## Agente y orquestación

`MonetizationAgent` vive en
`modules/intelligence/agents/monetization_agent/` y opera en modo
**read-only**. Lee el ledger, resume el umbral, importa señales locales y cruza
la evidencia de app, API de página y publicaciones. No cambia estados, no
registra payouts y no escribe en Meta.

El CGO lo expone como la capacidad `monetization_report` y también muestra un
resumen dentro de `daily_pipeline`. Las acciones `approved`, `paid` y el alta de
un payout requieren confirmación humana.

```bash
# Resumen del agente
python3 -m modules.intelligence.agents.monetization_agent.agent universe

# Reporte completo con evidencia y conciliación
python3 -m modules.intelligence.agents.monetization_agent.agent universe \
  --since 2026-10-01 --until 2026-10-31 --full

# Capacidad CGO
python3 -m modules.cgo --mode monetization_report --tenant universe --json
```

## Umbral de payout

El umbral se configura por tenant y es independiente del ingreso reconocido:

```json
{
  "monetization": {
    "payout_threshold": {
      "amount": 25.0,
      "currency": "USD",
      "program": "meta_content_monetization",
      "platform": "Facebook"
    }
  }
}
```

El reporte calcula:

- `current_balance`: estimado + aprobado sin pagar del mismo programa,
  plataforma y moneda.
- `remaining`: cuánto falta para alcanzar el umbral.
- `reached`: si el saldo ya alcanzó el mínimo.

Los payouts `paid` quedan fuera del saldo porque ya fueron liberados. Alcanzar
el umbral no crea ingreso reconocido; solo indica que el saldo está listo para
que la plataforma lo libere.

## Ledger por tenant

Rutas locales, ignoradas por git porque contienen datos financieros:

```text
tenants/<tenant>/data/monetization/signals.csv
tenants/<tenant>/data/monetization/periods.csv
tenants/<tenant>/data/monetization/payouts.csv
```

Todo es idempotente:

- `signals.csv`: una fila por `tenant + platform + program + signal_date + publication_id`.
- `periods.csv`: una fila por `tenant + platform + program + period_start + period_end`.
- `payouts.csv`: ID determinista por tenant, programa, periodo y fecha de pago;
  corregir montos actualiza la misma fila, no crea otra.

## CLI

```bash
# Importar los JSON históricos de Universe
python3 tools/monetization_report.py import-signals --tenant universe

# Refrescar el agregado diario de cuenta (no genera posts falsos)
python3 tools/monetization_report.py import-account-log --tenant universe \
  --input tenants/universe/metrics/meta_monetization_log.csv

# Reporte
python3 tools/monetization_report.py report --tenant universe
python3 tools/monetization_report.py report --tenant universe --granularity weekly --json
python3 tools/monetization_report.py report --tenant universe --since 2026-10-01 --until 2026-10-31

# Estimado y aprobado
python3 tools/monetization_report.py add-period --tenant universe \
  --platform Facebook --program meta_content_monetization \
  --period-start 2026-10-01 --period-end 2026-10-31 \
  --estimated-net 25 --status estimated

# Payout confirmado
python3 tools/monetization_report.py add-payout --tenant universe \
  --platform Facebook --program meta_content_monetization \
  --period-start 2026-10-01 --period-end 2026-10-31 \
  --paid-at 2026-11-15 --gross 25 --fee 1.75 --net 23.25
```

## Sincronización automática

```bash
# Captura evidencia de Meta, importa señales y genera el resumen
python3 scripts/run_monetization_sync.py --all --json

# Sin red y sin escribir: solo valida el estado local
python3 scripts/run_monetization_sync.py --all --dry-run --json
```

El timer propuesto vive en `scripts/growth-os-monetization.timer` y su servicio
en `scripts/growth-os-monetization.service`. No se instalan solos. El sync
automático nunca aprueba un periodo ni registra un payout; esas acciones siguen
siendo manuales y requieren statement o confirmación de Meta.

El servicio instalado ejecuta `--all --fetch-signals`: además del agregado de
cuenta, refresca las señales por publicación. La importación es idempotente, así
que repetir la captura del mismo día no duplica filas.

Credenciales: el extractor usa `META_ACCESS_TOKEN` del entorno o del `.env` de
la raíz y lo canjea por un Page Access Token. `PAGE_ACCESS_TOKEN` sigue siendo
válido si ya está configurado. Sin token, el sync falla en vez de reportar un
falso éxito.

Antes de instalar el timer, valida el flujo completo sin red:

```bash
python3 scripts/run_monetization_sync.py --all --dry-run --json
python3 -m modules.cgo --mode daily_pipeline --tenant universe --json
```

`daily_pipeline` incluye una acción `monetization` con el pipeline y lo que
falta para el umbral; no escribe ni cambia estados. Para activar la ejecución
diaria en un host systemd:

```bash
sudo cp scripts/growth-os-monetization.service /etc/systemd/system/
sudo cp scripts/growth-os-monetization.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now growth-os-monetization.timer
systemctl list-timers growth-os-monetization.timer
```

El servicio usa rutas absolutas y el usuario definidos en
`scripts/growth-os-monetization.service`; ajústalos si el repo vive en otra
ruta o corre con otro usuario.

## Reporte

Incluye:

- Señales: filas, posts únicos, rango, antigüedad y bonus incremental.
- Dinero: estimado, aprobado sin pagar, pipeline, pagado y reconocido.
- Desglose por serie, personaje, horario y día.
- Top y bottom de publicaciones.
- Calidad de datos: señales sin contexto, periodos pagados sin payout, payouts
  con `net != gross - fee`, antigüedad de la última señal.

## Incrementos, no acumulados

Los JSON de Meta son snapshots móviles: el mismo post aparece varios días con
conteos acumulados. El reporte calcula el **incremento** entre observaciones.
Así no se suma el mismo bonus varias veces.

La primera observación de un post se marca como `initial` porque incluye lo
acumulado desde la publicación. Los reportes semanales y mensuales agrupan esos
incrementos por fecha de observación.

## Señales de cuenta

El log `meta_monetization_log.csv` trae un agregado diario de toda la cuenta.
No es un snapshot acumulado por publicación y no debe contarse como post ni
como ingreso. `import-account-log` lo guarda con `publication_id=__account__`,
filtra el `Business_ID` configurado en el tenant y colapsa capturas repetidas
de la misma fecha conservando la última. El reporte muestra esas señales en el
bloque `Cuenta`, separadas de `unique_posts`, series y top posts.

## Estimados de contenido vs. payout

Los exports de "Ingresos aproximados por monetización de contenido" sirven
para validar tendencia y atribución por publicación, pero no sustituyen un
statement. Un payout confirmado se registra con su referencia, periodo, bruto,
fee y neto; solo ese neto entra en `recognized_net`. Si el statement no
desglosa fee, se documenta esa limitación en `notes` y no se inventa un cargo.

## Fuera de alcance

- Facturación, CFDI, conciliación bancaria, P&L y cobros automáticos.
- Convertir monedas: el reporte advierte que pueden coexistir monedas distintas.
- Atribución causal de ingresos a un post: las señales son un proxy.
