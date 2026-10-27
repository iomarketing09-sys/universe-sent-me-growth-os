# Integración Canon - Puente entre Repos

## Arquitectura de Repos

| Repo | Rol | Acceso CGO |
|------|-----|------------|
| `universe-sent-me-growth-os` | **Operational workspace** | Read/Write (CGO opera aquí) |
| `universe-sent-me-1` (canon) | **Source of truth** | Read-only (CGO solo lee) |

---

## Flujo de Sincronización

```
canon repo (universe-sent-me-1)
    │
    │ Git sync / PR
    ▼
GrowthOS/Integracion_Growth_OS.md  ← Puente documental
    │
    │ CGO lee y aplica
    ▼
growth-os/ (workspace operacional)
    │
    │ CGO escribe, ejecuta, publica
    ▼
Meta / WhatsApp / GBP / Web
```

---

## Archivos de Puente

### `GrowthOS/Integracion_Growth_OS.md`
- Última sincronización: 2026-08-23, commit `1daaad5`
- Contiene: mapeo de piezas canon ↔ growth-os, reglas de traducción, estado de sync

### `GrowthOS/Content_Inventory.csv`
- **Master identity source** - fuente única de verdad para piezas
- Columnas: ID_Pieza, Titulo, Personaje_Principal, Tipo_Contenido, Estado, etc.

### `GrowthOS/Content_Inventory_CANONICAL.csv`
- Versión canonizada (validada por Claude)
- Solo piezas con `Estado_Canon = CLEAR_VERIFIED`

### `GrowthOS/Canon_Contradictions_Report.md`
- Registro de contradicciones detectadas entre canon y workspace
- Resueltas o pendientes

---

## Reglas de Traducción

| Canon | Growth OS | Notas |
|-------|-----------|-------|
| `CNT-xxxx` | `CNT-xxxx` | IDs preservados |
| `Personaje_Principal` | `Personaje_Principal` | Mismo enum |
| `Estado_Canon` | `Estado_Canon` + `Estado_Canon_Normalizado` | Normalización automática |
| `Asset_Ref_Confirmado` | `Asset_Ref_Confirmado` | Path relativo a `tenants/universe/assets/` |
| `Hipotesis_ID` | `Hipotesis_ID` | Vinculado a `GrowthOS/HIPOTESIS_PLANTILLA.md` |

---

## Sincronización Manual (Actual)

```bash
# 1. Pull canon changes
cd /path/to/universe-sent-me-1
git pull origin main

# 2. Copiar archivos de puente
cp GrowthOS/Content_Inventory.csv /path/to/growth-os/GrowthOS/
cp GrowthOS/Content_Inventory_CANONICAL.csv /path/to/growth-os/GrowthOS/
cp GrowthOS/Integracion_Growth_OS.md /path/to/growth-os/GrowthOS/
cp GrowthOS/Canon_Contradictions_Report.md /path/to/growth-os/GrowthOS/

# 3. CGO valida y aplica
python3 skills/growth-cgo/scripts/verify_setup.py
```

---

## Automatización Futura

- [ ] Git submodule o subtree para canon
- [ ] Webhook canon → growth-os para sync automático
- [ ] Validación continua `canon-validator` en pipeline

---

*Actualizado: 15 Octubre 2026*
