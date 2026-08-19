# Auditoría de assets de Google Drive para Reels

**Propósito:** Registrar la evidencia de producción disponible en `My Drive/Universe sent me/USM/Reels` y su asociación verificable con publicaciones históricas, sin tratar los archivos ausentes del celular como datos inexistentes.

**Estado:** Active

**Fecha de creación:** 2026-08-19

**Última actualización:** 2026-08-19

**Versión:** 1.0

**Autor:** Manus AI

**Documentos relacionados:** `2026-08-19_Inventario_Assets_Drive_Reels.json`, `2026-08-19_Historial_Reels_Consolidado.json`, `2026-08-19_Relaciones_Reels_Alta_Evidencia.json`, `../../GrowthOS/07_00_Registro_Maestro_Reels.md`, `../../GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md`.

---

## Alcance

La auditoría examinó la carpeta `My Drive/Universe sent me/USM/Reels` (`1kWkZSbWvMGe0fwXu93UTh1iK6aVfE70a`) y subcarpetas de producción identificables. Se observaron 28 videos directos y paquetes de proyecto para `Mi ascenso a la locura`, `08 Agosto`, `CNT-015`, `Elara y Evan`, `Fantasma (Backrooms)` y `No eran papeles`.

| Resultado | Cantidad | Interpretación |
|---|---:|---|
| Registros de video corto publicados | 39 | Inventario multicanal del corte vigente. |
| Publicaciones con asset fuente de Drive asociado | 15 | La asociación queda explícita dentro del historial consolidado. |
| Cascadas multicanal confirmadas | 12 | Un asset no crea una cascada por sí solo; requiere IDs, copy o evidencia de publicación compatible. |
| Piezas aún sin cascada verificable | 11 | Pueden tener asset conocido o estar solo en el celular; permanecen separadas. |

## Asociaciones relevantes

Los paquetes de Drive respaldan directamente la producción de `Mi ascenso a la locura`, `Conversaciones atrancadas`, `Fantasma Backrooms`, `CNT-015 / Instante suspendido`, `Elara y Evan` y `No eran papeles`. También se registró evidencia fuerte para el Reel de Fantasma caminando con gatos y el Short de YouTube sobre una conversación vieja que muestra “Escribiendo…”.

> **Regla de interpretación:** un nombre de archivo o una carpeta de producción sirve como evidencia de asset fuente. No autoriza por sí mismo a declarar una republicación ni a combinar métricas de plataformas distintas.

## Límites y siguiente control

Los Reels que Fernando conserva solo en su celular permanecen fuera del inventario actual. Cuando se incorporen, se debe registrar como mínimo `Drive_Asset_ID` o nombre de archivo, `Concept_ID`, fecha de creación y los `Platform_Content_ID` asociados. El inventario estructurado contiene los IDs de Drive y la evidencia por concepto.
