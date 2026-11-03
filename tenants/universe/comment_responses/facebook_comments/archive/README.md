# Archivo de comentarios

Este directorio conserva material histórico. Nada de aquí se publica ni se lee
por el worker de comentarios.

## Estructura

- `closed_batches/`: lotes de publicación ya cerrados. Se guardan solo para
  auditoría; no son fuente de verdad.
- `legacy_backups/`: versiones anteriores de scripts y responders, movidas
  desde la carpeta activa para evitar que se confundan con el flujo vigente.

## Regla

La única cola publicable es `../aprobaciones.json`. Los lotes nuevos que
requieran publicación deben llamarse `aprobaciones_publish_*.json` y declarar
`kind: publish_batch`; el worker ignora cualquier otro archivo.

Archivado el 2026-11-02 durante la consolidación del edificio de
Comunicaciones. No se eliminó ningún archivo.
