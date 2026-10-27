# 00 — Estado de la campaña

| Campo | Valor |
|---|---|
| Campaña | Prueba Meta Ads — Flexi OI26 |
| Slug | `2026-10_flexi_ads_500mxn` |
| Estado | **G1 APROBADO — G2 pendiente de aprobación (propuesta v7 generada)** |
| Creada | 2026-10-16 |
| Objetivo Meta | Mensajes a WhatsApp (Click-to-WhatsApp) |
| Objetivo de negocio | Generar conversaciones con intención y aprender qué ángulo funciona |
| Canal | WhatsApp (propuesto; Linktree descartado para esta prueba) |
| Presupuesto | **500 MXN totales**, tipo lifetime |
| Duración | **7 días** (~71.43 MXN/día) |
| Cuenta publicitaria | **de Flexi — aún no visible para el token** |
| Página / Instagram | Zapateria Flexi Piedras Negras / `@zapateriaflexipn` |

## Decisiones tomadas

- [x] Presupuesto **total** de 500 MXN (no semanal).
- [x] Duración de **7 días**.
- [x] Solo los 5 modelos con asset (`142801`, `142901`, `143001`, `143201`, `306703`) + material de marca.
- [x] **Claims rechazados por el cliente** (respuesta "No"): 2×1, MSI, envío gratis >$1,200 y 15 % cumpleaños.
      No se usan en copy, anuncios ni respuestas.
- [x] Sin autorización de gasto (G3) no se publica.
- [x] **G1 aprobado (2026-10-16)** con una condición: segmentación **solo Piedras Negras, sin radio**.
- [ ] Obtener el `act_...` de Flexi y darlo de alta con permiso de administrar campañas.

## Bloqueos

| Bloqueo | Dueño | Estado |
|---|---|---|
| La cuenta publicitaria de Flexi no aparece en el token (solo hay 3 personales) | Cliente / Fernando | **Abierto** |
| Acceso del usuario a la cuenta, página e IG de Flexi | Cliente | **Abierto** |
| Atribución conversación→anuncio (el Worker no guarda `referral`) | CGO | Abierto (no bloquea lanzar) |

## Notas de acceso (verificado 2026-10-16)

- El token tiene `ads_management` y `ads_read`.
- `GET /me/adaccounts` devuelve 3 cuentas: `act_178259139027039` (cerrada),
  `act_692733670912914` (saldo pendiente) y `act_431501342532392` (**activa, personal**).
- `GET /1940942776222567/owned_ad_accounts` solo devuelve las dos cuentas personales anteriores;
  `client_ad_accounts` está vacío. **No hay cuenta de Flexi compartida todavía.**
- Para lanzar hace falta: `act_...` de Flexi, usuario con "Administrar campañas", página e IG
  vinculados y método de pago activo en MXN.

## Gates

| Gate | Qué se aprueba | Aprobó | Fecha |
|---|---|---|---|
| G0 | Cuenta, pago, página/IG, medición | | |
| G1 | Brief y presupuesto | Fernando | 2026-10-16 |
| G2 | Creativos y voz | | |
| G3 | Autorización de gasto | | |
| G4 | Lectura a 72 h | | |

## Bitácora

| Fecha | Cambio | Autor |
|---|---|---|
| 2026-10-16 | Se crea la carpeta y se registran las decisiones aprobadas; sin brief ni creativos todavía | CGO |
| 2026-10-16 | Cliente rechaza los 4 claims; se fija duración en 7 días; se confirma que la cuenta de Flexi aún no está accesible | CGO |
| 2026-10-16 | Se llenan `01_brief.md` y `02_audiencia.md` para revisión de Gate 1 | CGO |
| 2026-10-16 | **G1 aprobado** con geo limitada a Piedras Negras (sin radio); cuenta publicitaria queda pendiente de revisión del cliente | CGO |
| 2026-10-16 | **Agente Meta Ads reparado** (changelog 6.15.00): plan, creativos, compliance y dry-run funcionando; G2 puede ejecutarse con el agente | CGO |
| 2026-10-17 | Copywriter Agent genera propuesta v1 (4 variantes); G2 pendiente | CGO |
| 2026-10-17 | Copywriter Agent genera propuesta v2 (4 variantes); G2 pendiente | CGO |
| 2026-10-17 | Copywriter Agent genera propuesta v3 (4 variantes); G2 pendiente | CGO |
| 2026-10-17 | Copywriter Agent genera propuesta v4 (4 variantes); G2 pendiente | CGO |
| 2026-10-17 | Copywriter Agent genera propuesta v5 (4 variantes); G2 pendiente | CGO |
| 2026-10-17 | Copywriter Agent genera propuesta v6 (4 variantes); G2 pendiente | CGO |
| 2026-10-17 | Copywriter Agent genera propuesta v7 (4 variantes); G2 pendiente | CGO |
