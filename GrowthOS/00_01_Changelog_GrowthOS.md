# Changelog — Growth OS

**Propósito:** Registro centralizado de hitos, integraciones, cambios estratégicos y actualizaciones de arquitectura. Este documento permite a los agentes (Manus, Claude, etc.) sincronizar contexto rápidamente sin re-leer todo el repositorio.
**Estado:** Active
**Fecha de creación:** 2026-08-05
**Última actualización:** 2026-08-24
**Versión:** 3.76
**Autor:** Manus AI (CGO); entradas [1.1.1], [1.2.4]-[1.2.8], [1.2.10] añadidas por Claude; [1.2.9], [1.2.11], [1.2.12], [1.2.13], [1.2.14], [1.2.15], [1.2.16] añadidas por Manus
**Documentos relacionados:** `00_Índice.md`, `Operations/Research/2026-08-24_Growth_Connectivity_Audit_Evidence.json`, `Operations/Research/2026-08-22_Auditoria_Ejecutiva_GrowthOS_Estado_y_Prioridades.md`, `09_00_Estandar_Documentacion_Interna.md`, `Studio_Governance.md`, `Operations/Production/2026-08-24_Backlog_Tecnico_Staging_Firma_Bordados.md`, `Operations/Production/2026-08-24_Curacion_Activos_Web_Firma_Bordados.md`, `Operations/Research/2026-08-15_Community_Engagement_Log.md`, `Operations/Research/2026-08-15_Auditoria_Comentarios_Facebook.md`, `Operations/Research/2026-08-24_Facebook_Editorial_Review_After_Batch14.md`, `Operations/Research/2026-08-24_Facebook_Comment_Publication_After_Batch14.json`, `Operations/Research/2026-08-24_Facebook_Comment_Publication_Record_After_Batch14.json`, `Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Approved_Publication.json`, `Operations/Research/2026-08-24_Facebook_Comment_Review_After_Approved_Publication.json`, `Operations/Research/2026-08-24_Facebook_Editorial_Review_After_Approved_Publication.json`, `Operations/Research/2026-08-24_Facebook_Editorial_Review_After_Approved_Publication.md`, `Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Approved_Publication_Review.json`, `Operations/Research/2026-08-24_Facebook_Direct_Page_Mention_Context_After_Batch14.json`, `Operations/Automation/audit_facebook_comments_after_approved_publication.py`, `Operations/Automation/fetch_direct_page_mention_after_batch14.py`, `Operations/Automation/record_facebook_after_approved_publication_review.py`, `Operations/Research/2026-08-24_Facebook_Comment_Publication_After_Approved_Publication_Review.json`, `Operations/Research/2026-08-24_Facebook_Comment_Publication_Record_After_Approved_Publication_Review.json`, `Operations/Research/2026-08-24_Facebook_Comment_Publication_Record_After_Approved_Publication_Review.md`, `Operations/Automation/publish_facebook_after_approved_publication_review.py`, `Operations/Automation/record_facebook_publication_after_approved_publication_review.py`

- **[3.75.00] — 2026-08-24 (Manus): Auditoría general de conectividad y operación del Growth OS.** GitHub `main` quedó confirmado como fuente oficial sincronizada y los validadores internos de reconciliación, ventanas/video y comunidad devolvieron `PASS`. Facebook presenta operación real con 107 filas en el `Publication_Log`, 62 programadas, 39 publicadas y 448 comentarios únicos en el ledger comunitario; sin embargo, el sistema sigue en nivel 3/5 porque `Interacciones_24h` y `Interacciones_72h` permanecen vacías, `Metrics_Snapshot_Log.csv` no existe y el diseño E0/E24/E72 continúa en `Review`. La auditoría de configuración encontró la Custom API de Meta deshabilitada, Instagram habilitado pero sin `activeAccountUid`, Meta Ads Manager no conectado, Google Calendar sin scopes suficientes, ningún schedule recurrente activo y una hoja `USM Growth OS` en Drive desactualizada al 8 de agosto. La evidencia sanitizada queda en `Operations/Research/2026-08-24_Growth_Connectivity_Audit_Evidence.json`; la decisión es mantener Facebook estable y cerrar primero conectividad mínima, snapshots temporales y coherencia de fuentes antes de ampliar variables. No se publicaron piezas, no se modificaron campañas ni se activaron automatizaciones durante la auditoría.

- **[3.76.00] — 2026-08-24 (Manus): Primer corte visible de Facebook para Maeve Hook-First y corrección de taxonomía.** Meta Business Suite confirmó que el Reel abierto corresponde a `CON-2026-08-24-CraveYou-MaeveFeathers-HOOK-FIRST-V1`, no al Case_ID `MPM-002` de Fantasma y tres gatos. A las 18:03:38 `America/Matamoros` registró 757 visualizaciones, 636 espectadores, 19 interacciones, 43 min 18 s de reproducción total, 4 s de media, 35 vistas de 15 s, 16 reacciones, 3 comentarios, 0 shares y 0 guardados. La caída principal aparece cerca de 0:02; el corte es L3 actual pero no prueba finalización, replay ni un resultado causal frente a MPM-001. La carpeta operativa de Maeve conserva el nombre histórico `MPM.002`, que no debe trasladarse a la taxonomía de la celda Motion + POV/Meme.

- **[3.75.00] — 2026-08-24 (Manus): Revisión transversal de Reels y gates actualizados de MPM-002.** Se separaron cuatro carriles no comparables: MPM-001 (Motion + POV/Meme), `Remote Control` (videoclip musical), `Universe/Senales` (meme con afiliación nativa) y `Maeve Hook-First` (videoclip breve). MPM-001 en Facebook aporta una señal de optimización de hook —411 visualizaciones, 113 vistas de 3 s, 34 de 15 s y caída principal cerca de 0:03—, no un veredicto de familia. MPM-002 se conserva `Reference_Ready_Quota_Wait`: requiere reconciliación operativa de MPM-001, primer snapshot de Maeve, cuota disponible y gate humano; después puede generarse como segundo caso observacional Facebook-first, sin afiliación, pauta ni reuse histórico. No se publicaron ni programaron piezas.

- **[3.74.00] — 2026-08-24 (Manus): Indicadores de retención para el loop de Maeve/Crave You.** Se priorizaron `Retention_3s_Rate`, llegada al punto medio, `Completion_Rate` o vistas del último tramo, continuidad en la unión del loop, `Average_Watch_Time / Duration_Seconds` y `Replay_Rate`, en ese orden. Los plays, reach y tiempo total se conservan como contexto de distribución/consumo, no como sustitutos de retención. Para un loop de 13–14 segundos, la métrica de 15 segundos no se tratará automáticamente como finalización; los acumulados lifetime no se convertirán en snapshots 24/72h. Facebook e Instagram se medirán por separado y el resultado quedará en L1/L2 si faltan curvas o campos nativos.

- **[3.73.00] — 2026-08-24 (Manus): Calendario de seguimiento de métricas para Maeve/Crave You.** Se definió el primer corte operativo para el 2026-08-24 a las 22:00 `America/Matamoros`, con seguimiento diario a la misma hora para Facebook e Instagram por separado. Los cierres de 24 horas —Facebook 2026-08-24 17:36:57— y 72 horas —Facebook 2026-08-26 17:36:57— quedan como opcionales y solo se escribirán si existe baseline y captura temporal válida; los acumulados lifetime no se convierten en ventanas artificiales. El cierre de siete días queda para el 2026-08-30 a las 22:00. No se creó una automatización ni se modificó ninguna publicación.

- **[3.72.00] — 2026-08-24 (Manus): Publicación verificada de las cinco respuestas autorizadas del nuevo corte de Facebook.** Fernando autorizó explícitamente las cinco propuestas; Meta Graph API v26.0 publicó y verificó 5/5 respuestas, con cuatro parents directos y una réplica anidada validada mediante el parent inmediato real devuelto por Meta. El preflight no encontró duplicados ni conflictos de Página; no hubo errores de API ni publicaciones fuera de autorización. El ledger conserva 448 filas únicas, actualiza las cinco con `Respuesta_Estado=Respondido`, `Aprobacion_Estado=Aprobada`, `Respuesta_Meta_ID`, `Respuesta_Fecha`, texto exacto, fuente y timestamp; la cola queda con `Pendiente_Respuesta=0`. Evidencia: `2026-08-24_Facebook_Comment_Publication_After_Approved_Publication_Review.json`, `2026-08-24_Facebook_Comment_Publication_Record_After_Approved_Publication_Review.json` y `2026-08-24_Facebook_Pending_Queue_After_Approved_Publication_Review.json`.

- **[3.71.00] — 2026-08-24 (Manus): Nuevo corte de comentarios posterior a la publicación aprobada y corrección del cursor operativo.** Se corrigió el auditor para usar el cierre real de las 24 respuestas aprobadas (`2026-08-24T17:13:46+00:00`) en lugar del cursor histórico de Batch 14. Meta Graph API v26.0 revisó en modo solo lectura las 20 publicaciones propias más recientes y encontró 95 comentarios nuevos sin respuesta directa: 69 en el reel de Maeve, 23 en el meme de la frase `larga vida a esas mujeres que aprietan desde adentro` y uno en cada una de tres publicaciones adicionales. Los 95 fueron clasificados y registrados en el ledger, que pasó a 448 filas únicas; 5 quedaron como propuestas `Pendiente_Respuesta` + `Pendiente_Fernando` y 90 como `No_Requiere_Respuesta`. Se contextualizó la única mención directa nueva a Universe Sent Me y se conservó sin acción la referencia musical aislada `Coco valiente` por falta de artista o contexto. No se publicaron respuestas ni hubo errores de API. Evidencia: `2026-08-24_Facebook_Comment_Review_After_Approved_Publication.json`, `2026-08-24_Facebook_Editorial_Review_After_Approved_Publication.md/.json` y `2026-08-24_Facebook_Pending_Queue_After_Approved_Publication_Review.json`.

- **[3.70.00] — 2026-08-24 (Manus): Corrección de activo fallido en la galería del staging de Firma Bordados.** La tarjeta «Detalle de bordado» mostró un marcador de generación fallida, por lo que las dos referencias externas se retiraron. La corrección `b634f47` fue revisada vía Pull Request, pasó CI en `staging` y `main` y quedó publicada por el merge `eaf89df`. La galería usa ahora tres activos locales comprobados: bordado en prenda, detalle de bordado y variedad de prendas. Las solicitudes estáticas a los tres recursos devolvieron HTTP 200 y el HTML público no contiene el marcador de error. La revisión visual manual queda pendiente exclusivamente en el navegador Quick-seedless del usuario; no se debe usar un navegador remoto de otra computadora. Wix, DNS, nameservers y `firmabordados.com` no cambiaron.

- **[3.69.00] — 2026-08-24 (Manus): Galería de procesos y guía prudente de prendas validadas en el staging de Firma Bordados.** La revisión de activos autorizados encontró fotografías útiles de bordado que incluían marcas de clientes, por lo que se preservaron únicamente como referencia interna. La página recibió una galería de bordado/serigrafía con una fotografía autorizada y dos visuales exclusivas sin marcas de terceros; no se afirma que representen un pedido, inventario o certificación concreta. Se añadió la frase «explorar opciones de prenda según las necesidades de presentación» en vez de declarar materiales o calidades no confirmadas. La rama `content/work-gallery-refinement` (`8a01b15`) pasó Pull Request y CI a `staging`; el merge `d15ef60` se promovió a `main`, servido como staging público. Se verificaron contenido, CTA, catálogos, contacto, noindex, robots y headers. Wix, DNS, nameservers y `firmabordados.com` no cambiaron.

- **[3.68.00] — 2026-08-24 (Manus): Actualización comercial y visual validada en el staging de Firma Bordados.** Se registró e integró únicamente el mínimo confirmado de serigrafía de 12 piezas y la nota de tiempos variables según cantidad, requerimiento y carga de trabajo; materiales siguen pendientes y no se añadieron plazos, precios, telas ni certificaciones. La rama `content/commercial-visual-update` (`f6a754a`) pasó Pull Request y CI hacia `staging`; el merge `1d24703` se promovió a `main`, que Pages sirve como staging público. La página incorpora una visual exclusiva de prendas sin marcas de terceros y una adaptación fiel de la fachada autorizada, con assets WebP optimizados. Se comprobó visualmente la versión publicada y se conservaron noindex, robots, headers, catálogos, CTA WhatsApp y datos de contacto. Wix, DNS, nameservers y `firmabordados.com` no cambiaron.

- **[3.67.00] — 2026-08-24 (Manus): Publicación verificada de las 24 respuestas aprobadas del corte posterior al Batch 14.** Fernando aprobó explícitamente las 24 propuestas; Meta Graph API v26.0 publicó y verificó 24/24 respuestas, con 23 parents directos y una réplica anidada validada mediante el parent inmediato real devuelto por Meta. El preflight no encontró duplicados ni conflictos de Página; no hubo errores de API ni publicaciones fuera de autorización. El ledger conserva 353 filas y actualiza las 24 con `Respuesta_Estado=Respondido`, `Aprobacion_Estado=Aprobada`, `Respuesta_Meta_ID`, `Respuesta_Fecha`, texto exacto, fuente y timestamp. La cola posterior quedó en cero pendientes publicables. Evidencia: `2026-08-24_Facebook_Comment_Publication_After_Batch14.json`, `2026-08-24_Facebook_Comment_Publication_Record_After_Batch14.json`, `2026-08-24_Facebook_Editorial_Review_After_Batch14.md` y `2026-08-24_Facebook_Pending_Queue_After_Approved_Publication.json`.

- **[3.66.00] — 2026-08-24 (Manus): Nuevo corte de comentarios de Facebook posterior al Batch 14.** Meta Graph API v26.0 revisó en modo solo lectura las 20 publicaciones propias más recientes y encontró 83 comentarios nuevos sin respuesta desde el cursor `2026-08-24T04:14:14+00:00`. Se registraron 24 propuestas específicas como `Pendiente_Respuesta` + `Pendiente_Fernando` y 59 casos como `No_Requiere_Respuesta`; no se realizaron publicaciones ni hubo errores de API. El ledger pasó a 353 filas y conserva `Privacidad=Anonimizado`; la cola requiere aprobación explícita de Fernando antes de cualquier escritura. Evidencia: `2026-08-24_Facebook_Comment_Review_After_Batch14.json`, `2026-08-24_Facebook_Comment_Context_After_Batch14.json`, `2026-08-24_Facebook_Editorial_Review_After_Batch14.md` y `2026-08-24_Facebook_Pending_Queue_After_Review.json`.

- **[3.65.00] — 2026-08-24 (Manus): Paquete P1 de mantenimiento cerrado en el staging Cloudflare de Firma Bordados.** Se integró CI en GitHub para Pull Requests y pushes a `staging`/`main`, con instalación bloqueada, TypeScript y build Vite; tras corregir la inicialización de pnpm, las ejecuciones de ambas ramas terminaron correctamente. Los commits `f49a344` y `beaaa8d` retiraron providers inactivos y las dependencias `next-themes`/`sonner`, hicieron segura en español la pantalla de recuperación, priorizaron el hero y difirieron imágenes no críticas. El bundle principal disminuyó de ≈562 kB a 451.78 kB sin comprimir y de ≈163 kB a 127.12 kB gzip. Se promovió a `main`, que Pages sirve como staging, y se verificaron noindex, robots y headers P0. La protección formal de `main` permanece pendiente de decisión porque altera la colaboración. Wix, DNS, nameservers y `firmabordados.com` no cambiaron.

- **[3.64.00] — 2026-08-24 (Manus): Paquete P0 de accesibilidad/protección validado en el staging Cloudflare de Firma Bordados.** Se habilitó zoom, foco visible, enlace de salto y reducción de movimiento; se añadieron meta noindex y headers estáticos de protección. El commit `b3754d0` se validó con TypeScript/Vite y se promovió a `main`, rama que Pages sirve como staging público. La configuración inicial conservó `main` pese a un intento de definir `staging`; se documentó el flujo ramas de trabajo/staging → revisión → promoción a main. Se verificaron meta, robots, headers, hero y teclado en móvil. Wix, DNS, nameservers y dominio no cambiaron.

- **[3.63.00] — 2026-08-24 (Manus): Backlog técnico de bajo riesgo para Firma Bordados.** Se auditó el staging Cloudflare y se priorizaron mejoras sin depender de materiales, tiempos o mínimos: paquete P0 de accesibilidad/protección de staging, carga diferida de imágenes, limpieza de runtime, CI y protección de ramas. Quedan bloqueados analytics, backend de formularios, precios, SEO estructurado definitivo y dominio hasta confirmación/consentimiento correspondiente. No se modificó el sitio durante la auditoría.

- **[3.62.00] — 2026-08-24 (Manus): Staging Cloudflare Pages desplegado para Firma Bordados.** Se creó el repositorio privado temporal `iomarketing09-sys/firma-bordados-site`, se limitó la app Cloudflare Workers and Pages a ese único repositorio y se desplegó `https://firma-bordados-staging.pages.dev` desde la rama `staging`. El build usa `pnpm exec vite build`, publica `dist/public` y fija Node 22.16.0. Se verificaron hero, CTA WhatsApp, capacidades, catálogos, contacto y PDFs. Wix, DNS, nameservers y `firmabordados.com` no cambiaron; el corte sigue bloqueado por aprobación/transferencia u operación administrada.

- **[3.61.00] — 2026-08-24 (Manus): Excepción temporal de propiedad Io Marketing para el staging de Firma Bordados.** Fernando autorizó que el repositorio privado y el primer Pages staging se creen bajo las cuentas actuales de Io Marketing. La excepción no modifica la propiedad del dominio ni autoriza DNS, Wix, facturación o cancelación. Antes de cualquier corte, será obligatorio transferir repo/proyecto al cliente o documentar la operación administrada y la entrega. Los activos y datos del cliente permanecen separados de Universe Sent Me y OmniRoute.

- **[3.60.00] — 2026-08-24 (Manus): WhatsApp como CTA principal y guía exacta Cloudflare Pages para Firma Bordados.** Se convirtió WhatsApp en el llamado principal del hero, conservando catálogos como acción secundaria y el correo/formulario en contacto. Se documentaron los pasos de cuenta Cloudflare y GitHub propiedad del cliente, repositorio privado, acceso restringido de la app Cloudflare Workers & Pages, ramas, build React/Vite y salida `dist/public`. No se creó cuenta, repositorio ni proyecto Pages; no se modificó Wix, DNS o el dominio público.

- **[3.59.00] — 2026-08-24 (Manus): WhatsApp confirmado en el staging de Firma Bordados.** Se añadió el canal `+52 878 788 0735` con un mensaje inicial de consulta y se mantuvo el correo `firmabordados@yahoo.com` y el formulario `mailto:` ya existente. La legibilidad se verificó en móvil; no se envió ningún mensaje. Materiales, tiempos de entrega y mínimos de pedido siguen pendientes de confirmación del cliente y no se inventaron.

- **[3.58.00] — 2026-08-24 (Manus): Catálogos y servicios confirmados integrados al staging de Firma Bordados.** Fernando validó BigBang 2019, M&O 2016 y Soul & Blues 2025 como catálogos vigentes. Se cargaron sus copias autorizadas en el staging, se corrigieron tamaños visibles a 13.6 MB, 3.8 MB y 8.0 MB, y se verificó respuesta HTTP correcta. Se incorporaron digitalización, bordado, serigrafía, playeras, camisas, uniformes industriales y línea médica; parches y gorras se excluyen con una nota discreta. Los PDFs deberán migrarse al repositorio/almacenamiento del cliente para Cloudflare. Wix, DNS y dominio no cambiaron.

- **[3.57.00] — 2026-08-24 (Manus): Inventario autorizado de catálogos Drive para Firma Bordados.** Se revisaron tres PDFs compartidos por Fernando: BigBang (61 páginas, 13.6 MB), M&O (52 páginas, 3.8 MB) y Soul & Blues 2025 (23 páginas, 8.0 MB). Se detectaron metadatos de tamaño desactualizados en dos tarjetas y ediciones declaradas 2019/2016 que requieren confirmación de vigencia del cliente antes de sustituir enlaces Wix. No se modificó el staging, Cloudflare, Wix, DNS ni contenido de servicios.

- **[3.56.00] — 2026-08-23 (Manus): Cloudflare Pages y movimiento ligero confirmados para Firma Bordados.** Se confirmó Cloudflare Pages como ruta de hosting de menor coste/mantenimiento frente a WordPress y se aplicó al staging la puntada SVG de entrada, revelados breves, microinteracciones de catálogos/CTA y sistema de fichas con reglas de bordado. El movimiento respeta `prefers-reduced-motion`; no se añadieron loops, video automático, parallax, partículas ni carruseles. Wix, DNS, catálogos, formulario y datos del cliente no cambiaron. WordPress permanece solo como alternativa documentada.

- **[3.55.00] — 2026-08-23 (Manus): Ruta WordPress.com para staging de Firma Bordados.** Fernando aclaró que evalúa WordPress como plataforma de hosting en lugar de Cloudflare Pages. Se documentó la ruta WordPress.com bajo cuenta del cliente: sitio temporal `*.wordpress.com`, activos/PDFs propios, revisión sin DNS y conexión futura del dominio Wix mediante registros DNS solo después de aprobación escrita. WordPress.com Personal cabe en el presupuesto de referencia; el staging nativo Business/Commerce no. No se creó cuenta, contrató plan, modificó Wix/DNS ni se mezcló infraestructura con Universe Sent Me.

- **[3.54.00] — 2026-08-23 (Manus): Guía de staging Cloudflare Pages para Firma Bordados.** Se documentó una prueba reversible del sitio React/Vite en una URL `*.pages.dev`, con rama `staging`, repositorio y cuenta propiedad del cliente, salida `dist/public`, reemplazo previo de rutas de activos Manus/Wix y checklist de verificación. La guía no autoriza cambio de DNS, cancelación Wix, formulario con backend ni integración con OmniRoute. WordPress queda descartado para el alcance actual y solo se reconsidera ante edición frecuente autónoma, blog, autores o CMS. Los presupuestos, credenciales, datos y hosting permanecen separados de Universe Sent Me.

- **[3.53.00] — 2026-08-23 (Manus): Diseño de asistencia de métricas y respuestas con OmniRoute.** Se definieron dos carriles `Draft`: lectura narrativa de cortes métricos ya normalizados y propuestas comunitarias a partir de contexto anonimizado. Meta/Windsor y los scripts versionados siguen siendo la fuente de métricas; los ledgers, cálculo, deduplicación, moderación y publicación no se delegan a IA. Las respuestas de comunidad requieren clasificación de riesgo, aprobación explícita de Fernando, preflight anti-duplicado y verificación posterior. Solo se considera una futura preparación programada de colas; un bot que publica autónomamente queda prohibido. No se consultó, escribió ni publicó contenido durante este diseño.

- **[3.52.00] — 2026-08-23 (Manus): Protocolo de OmniRoute para borradores del Growth OS.** Se formalizó OmniRoute como asistente local de ideación, borradores, revisión de coherencia y síntesis cualitativa, usando el Combo `usm-groq-gemini-priority` con Groq principal y Gemini fallback. Se prohíbe enviar secretos, PII, comentarios reales sin anonimizar, Windsor crudo, métricas canónicas no agregadas, documentos privados e IDs de publicación. Ninguna salida puede escribir en inventarios, ledgers, HypothesisBank, calendario, canon o cuentas sociales sin revisión humana; cada salida queda `Draft` hasta la aprobación correspondiente. No se generó, programó ni publicó contenido.
- **[3.65.00] — 2026-08-24 (Manus): Conciliación completa del registro histórico de comentarios respondidos en Facebook.** Se revisaron las 166 filas `Respondido` del ledger contra los registros de publicación disponibles y Meta Graph API v26.0 en modo GET. Las 166 tienen registro administrativo completo; 163 fueron verificadas actualmente por Meta y 3 objetos históricos devuelven HTTP 400. Se corrigieron dos textos de respuesta y un `Comentario_ID` con alias histórico. El ledger queda en 270 filas y 270 IDs únicos, con validación PASS; no se realizaron nuevas escrituras ni reintentos. Evidencia: `2026-08-24_Facebook_Complete_Responded_Registry.json`, `2026-08-24_Facebook_Complete_Responded_Registry.md`, `2026-08-24_Facebook_All_Responded_Comments_Meta_Verification.json` y `2026-08-24_Facebook_Complete_Responded_Registration_Repair.json`.

- **[3.51.00] — 2026-08-24 (Manus): Publicación verificada del Batch 14 de Facebook.** Fernando aprobó las 13 propuestas del Batch 14. Meta Graph API v26.0 confirmó las 13 respuestas con autoría de la Página, texto exacto, `is_hidden=false` y parent válido: 12 con parent directo y 1 réplica anidada con semántica de parent inmediato. Ocho ya estaban creadas antes de la recuperación, una se recuperó tras la validación parcial y cuatro se publicaron durante la recuperación; no se duplicó ningún POST. El ledger quedó en 270 filas y 270 IDs únicos; validación PASS. La cola posterior al Batch 14 contiene 0 pendientes publicables. Evidencia: `2026-08-24_Facebook_Comment_Publication_Batch_14.json`, su registro, el índice Markdown y `2026-08-24_Facebook_Pending_Queue_After_Batch14.json`.

- **[3.50.00] — 2026-08-24 (Manus): Batch 14 de revisión y propuestas de engagement en Facebook.** Meta Graph API v26.0 revisó 20 publicaciones propias, 198 comentarios raíz y 246 IDs de comentarios/réplicas. El escaneo encontró 106 unidades actuales sin respuesta directa, pero 69 ya estaban clasificadas históricamente. Se revisaron 37 unidades nuevas o `Sin_Revisar`: 13 quedaron como propuestas específicas y 24 como `No_Requiere_Respuesta`. El único comentario posterior al cursor del Batch 13 fue una réplica usuario-a-usuario y no se propuso intervenir. No hubo errores de API ni publicaciones en esa fase. Evidencia: `2026-08-24_Facebook_Comment_Review_Batch_14.json`, `2026-08-24_Facebook_Batch14_Engagement_Proposals.md` y el inventario reconciliado.

- **[3.49.00] — 2026-08-24 (Manus): Batch 13 y cierre de la cola autorizada de Facebook.** Fernando autorizó diez respuestas y excluyó explícitamente la réplica de L Roberto y el comentario musical inaccesible sin texto recuperable. Meta Graph API v26.0 publicó y verificó 10/10; una réplica anidada fue validada con la semántica normal de Meta que devuelve el `parent.id` de la raíz del hilo. El ledger queda sincronizado y validado con 255 filas y 255 IDs únicos. La cola posterior al Batch 13 contiene 0 pendientes publicables y conserva 2 casos excluidos: uno marcado `No_Requiere_Respuesta` por decisión editorial y otro `Archivado` por bloqueo de API. No se publicaron respuestas fuera de las 10 autorizadas. Evidencia: `2026-08-24_Facebook_Comment_Publication_Batch_13.json`, su registro, y `2026-08-24_Facebook_Pending_Queue_After_Batch13.md`.

- **[3.48.00] — 2026-08-24 (Manus): Batch 12 y auditoría actual de pendientes.** Fernando aprobó cinco casos reclasificados del post ☁️✨🤔: “Eimen” como “Amén”, “Yo” como identificación, “My Dad” y dos cadenas de emojis interpretables. Meta Graph API v26.0 publicó y verificó 5/5. La auditoría posterior de la cola encontró 12 registros pendientes con propuesta: 11 accesibles y 1 comentario musical inaccesible; ninguno tenía respuesta exacta u otra respuesta de la Página. La cola se compone de 8 raíces del meme, 2 réplicas sujetas a criterio y 1 raíz contextual. El ledger mantiene 255 filas y 255 IDs únicos; validación PASS. No se publicaron respuestas fuera de las cinco autorizadas.

- **[3.47.00] — 2026-08-24 (Manus): Corrección del detalle del Batch 11 y reclasificación editorial.** Se verificó que el Batch 11 contiene 28 respuestas, 28 publicaciones y 28 verificaciones; se creó un índice Markdown completo para evitar recortes de visualización. Fernando corrigió cinco casos: “Eimen” significa “Amén”, “Yo” expresa identificación con el meme, “My Dad” merece revisión y las dos cadenas de emojis contienen señales interpretables. Esos cinco pasan a `Pendiente_Respuesta` con propuestas USM; cuatro casos permanecen como `No_Requiere_Respuesta`. No se publicó nada adicional. El ledger mantiene 255 filas y 255 IDs únicos; validación PASS.

- **[3.46.00] — 2026-08-24 (Manus): Batch 11 y publicación de 28 respuestas del post ☁️✨🤔.** Fernando autorizó las 28 propuestas específicas preparadas tras la auditoría correcta del post `1036844829507460_122151375549072582`. Meta Graph API v26.0 publicó y verificó 28/28, con preconsulta anti-duplicado y comprobación de autoría, padre, texto exacto y `is_hidden=false`. Los 9 casos clasificados como baja señal, nombres, emojis, vacíos o puntuación no se publicaron y quedan para revisión editorial separada. El ledger conserva 255 filas y 255 IDs únicos; validación PASS. No se publicaron respuestas fuera de las 28 autorizadas.

- **[3.45.00] — 2026-08-24 (Manus): Batch 10 y auditoría completa del post ☁️✨🤔.** Fernando autorizó las 25 respuestas ya propuestas para el post `1036844829507460_122151375549072582`. Meta Graph API v26.0 publicó y verificó 25/25, con autoría de Página, padres correctos, textos exactos e `is_hidden=false`. La auditoría posterior del post correcto encontró 68 raíces, 90 IDs incluyendo réplicas, 31 raíces respondidas y 37 raíces sin respuesta. Se prepararon 28 propuestas específicas con personalidad USM y 9 casos sin acción; no se publicaron esas nuevas propuestas. Se corrigió un corte intermedio que había apuntado al post del meme y quedó marcado como superseded. La cola general se redujo a 9 propuestas activas del meme y 1 caso bloqueado por Meta. El ledger conserva 255 filas y 255 IDs únicos; validación PASS.

- **[3.44.00] — 2026-08-24 (Manus): Batch 09 y revisión de la cola restante de Facebook.** Fernando aprobó cinco respuestas musicales. Meta Graph API v26.0 publicó y verificó cuatro; el comentario “El día que volviste a la tierra - Carlos Sadness” quedó bloqueado porque su objeto ya no era accesible (`HTTP 400`, código 100), sin forzar la escritura. La cola restante quedó reconciliada en 34 propuestas activas, 1 caso aprobado bloqueado y 1 réplica excluida por ser conversación usuario-a-usuario; además, un corte posterior encontró una réplica usuario-a-usuario clasificada como `No_Requiere_Respuesta`. El ledger conserva 255 filas y 255 IDs únicos; validación PASS. No se publicaron respuestas fuera de las cuatro verificadas del Batch 09.

- **[3.43.00] — 2026-08-24 (Manus): Batch 08 y reconciliación completa de la cola de Facebook.** Fernando aprobó dos respuestas del corte amplio y Meta Graph API v26.0 confirmó ambas publicaciones: “Ahí está: no era el producto, era la atención. 😂🔋” y “Jajaja, ahí ya se necesita un plan de salida. 😂🙈”, con autoría de Página, padres correctos, textos exactos e `is_hidden=false`. El seguimiento revisó nuevamente las 20 publicaciones y encontró 5 comentarios nuevos; la reconciliación dejó visibles 41 propuestas pendientes, incluidas 5 recomendaciones musicales raíz que antes quedaban fuera del resumen de novedades. No se publicaron respuestas adicionales durante la reconciliación. El ledger conserva 254 filas y 254 IDs únicos; validación PASS. Evidencia: Batch 08, seguimiento de 72 horas y `Facebook_Pending_Queue_Reconciliation`.

- **[3.42.00] — 2026-08-24 (Manus): Auditoría amplia de comentarios de Facebook en ventana móvil de 72 horas.** La revisión exclusiva mediante Meta Graph API v26.0 cubrió las 20 publicaciones propias más recientes, 189 comentarios raíz y 228 IDs de comentarios/réplicas. Detectó 161 unidades sin respuesta actualmente, 159 dentro de la ventana de 72 horas, 23 hallazgos nuevos y 2 candidatos con propuesta específica; 21 quedaron sin acción por falta de contexto, réplicas, etiquetas, conversaciones o baja señal. No hubo errores de API ni publicaciones. El ledger pasó a 249 filas y 249 IDs únicos, con validación PASS. La evidencia queda en `2026-08-24_Facebook_Comment_Review_Broad_72h.json`, `2026-08-24_Facebook_Broad_72h_Reply_Proposals.md/.json` y su registro.

- **[3.41.00] — 2026-08-24 (Manus): Publicación verificada del Batch 07 de siete respuestas aprobadas.** Fernando autorizó publicar las siete respuestas pendientes del informe ampliado, incluida la respuesta específica al comentario sobre “Te Quiero Puta!” de Rammstein y la versión corregida de “Yo sé pero de nada me sirve si ni novio tengo 😒”. Meta Graph API v26.0 confirmó siete publicaciones, cada una con autoría de Universe Sent Me, `parent.id` correcto, texto exacto e `is_hidden=false`. El ledger conserva 226 filas y 226 IDs únicos; la validación quedó en PASS. No se publicó ninguna respuesta fuera de las siete autorizadas. La evidencia está en `2026-08-24_Facebook_Comment_Publication_Batch_07.json` y su registro de sincronización.

- **[3.40.00] — 2026-08-24 (Manus): Refinamiento editorial de respuestas comunitarias.** Fernando sustituyó la propuesta “El universo también entiende esa queja de soltera. 😂” por “Jajaja, el universo también contempla ese pequeño detalle. 😂”, evitando un matiz condescendiente. También confirmó que el comentario musical “Te quiero p..t4 de rammstein habla de un amor hacia una dama que tiene muchos pretendientes muy buena” se refiere a “Te Quiero Puta!” de Rammstein, del álbum *Rosenrot*; la respuesta pendiente ahora devuelve esa interpretación concreta: “Sí, esa lectura de una mujer con tantos pretendientes le pone otra capa a la canción. 👀 Rammstein no deja precisamente las cosas en la superficie.” Se consolidó en GrowthOS la regla de que los remates deben demostrar lectura del comentario y tener criterio propio; no se publicó ninguna respuesta adicional.

- **[3.39.00]** — 2026-08-24 (Manus): Auditoría ampliada de comentarios de Facebook y corrección de fuente visual.** La revisión exclusiva mediante Meta Graph API v26.0 cubrió las 20 publicaciones propias más recientes, 179 comentarios raíz y 215 IDs de comentarios/réplicas; detectó 16 comentarios nuevos sin respuesta directa, añadió 16 filas idempotentes al ledger y no tuvo errores de API. El post `1036844829507460_122151376083072582` se revisó completo: 48 raíces, 31 sin respuesta directa y 42 unidades sin respuesta al incluir réplicas. Se prepararon siete propuestas nuevas, pero no se publicó ninguna. Fernando confirmó que la frase real dentro de la imagen es “larga vida a esas mujeres que aprietan desde adentro”; el caption externo sigue siendo `😏🙈😂 #UniverseUSM #MemesUSM #UniverseSentMe`. Las descripciones anteriores del meme como un gato gris en un salón o corredor palaciego quedan invalidadas y no deben reutilizarse.

- **[3.38.00] — 2026-08-24 (Manus): Batch 06 de tres respuestas aprobadas y verificadas.** Fernando autorizó exactamente tres respuestas para el post `1036844829507460_122151376083072582`. Meta Graph API v26.0 publicó y verificó las tres con autoría `Universe Sent Me`, `parent.id` correcto, texto exacto e `is_hidden=false`. Los IDs de respuesta son `122151376083072582_2270174113755963`, `122151376083072582_1060242273589535` y `122151376083072582_1862911838260493`. El ledger pasó a 210 filas antes del Delta 08 y luego a 226 filas; validación PASS. No se publicaron otras propuestas.

- **[3.37.00] — 2026-08-24 (Manus): Corrección de una verificación visual no fiable.** La afirmación anterior de que el post no tenía frase explicativa ni texto sexual dentro de la imagen queda invalidada por la confirmación autoritativa de Fernando. La referencia válida es la frase visible “larga vida a esas mujeres que aprietan desde adentro”, separada del caption externo `😏🙈😂 #UniverseUSM #MemesUSM #UniverseSentMe`.

- **[3.36.00] — 2026-08-24 (Manus): Entrada histórica corregida.** La descripción previa del meme como un gato gris sentado en un corredor o salón palaciego no es una fuente visual fiable. Esa lectura queda supersedida por la frase confirmada por Fernando: “larga vida a esas mujeres que aprietan desde adentro”.

- **[3.35.00] — 2026-08-24 (Manus): Identificación consolidada del post para propuestas de baja señal.** Se añadió el copy `😏🙈😂 #UniverseUSM #MemesUSM #UniverseSentMe`, el Page Post ID `1036844829507460_122151376083072582` y el enlace de referencia junto a las propuestas opcionales, tanto en Markdown como en JSON.

- **[3.34.00] — 2026-08-24 (Manus): Publicación verificada de nueve respuestas y preparación de propuestas seguras adicionales.** Fernando aprobó las nueve respuestas del hilo `1036844829507460_122151376083072582`; Meta Graph API v26.0 confirmó las nueve publicaciones con autoría `Universe Sent Me`, `parent.id` correcto, texto exacto e `is_hidden=false`. También se prepararon dos propuestas prudentes para lenguaje sexual explícito y nueve respuestas opcionales para baja señal; ninguna de esas 11 nuevas propuestas fue publicada. El ledger comunitario conserva 210 filas y 210 IDs únicos, con validación PASS. La evidencia queda en `2026-08-24_Facebook_Comment_Publication_Batch_05.json`, `2026-08-24_Facebook_Safety_LowSignal_Proposals.json` y la auditoría comunitaria v4.1.

- **[3.33.00] — 2026-08-24 (Manus): Auditoría de hilo enlazado y publicación verificada de dos respuestas de Facebook.** Meta Graph API v26.0 resolvió el enlace de Fernando al Page Post `1036844829507460_122151376083072582`, revisó 40 comentarios raíz, 46 IDs incluyendo réplicas y 41 unidades sin respuesta directa. Se prepararon nueve propuestas específicas y se excluyeron 32 unidades por falta de contexto, baja señal, menciones, conversación entre usuarios o lenguaje sexual explícito. Fernando aprobó dos propuestas previas; se publicaron y verificaron con autoría de Universe Sent Me, `parent.id` correcto, texto exacto e `is_hidden=false`, con respuestas `122151376539072582_1017908597886964` y `122151376083072582_2857677777946548`. El ledger comunitario quedó en 210 filas y 210 IDs únicos, con validación PASS. No se publicaron las nueve propuestas nuevas.

- **[3.32.00] — 2026-08-24 (Manus): Revisión incremental de comentarios nuevos de Facebook y preparación de dos respuestas.** Meta Graph API v26.0 revisó las 20 publicaciones propias más recientes después del corte `2026-08-23T23:49:53+0000` y detectó tres comentarios nuevos sin respuesta directa. Dos recibieron propuestas contextuales y quedaron `Pendiente_Fernando`; un comentario vacío quedó `No_Requiere_Respuesta`. El ledger comunitario pasó a 195 filas y 195 IDs únicos, con validación PASS. No se publicó ninguna respuesta ni se ejecutó escritura sobre Facebook. La evidencia queda en `2026-08-23_Facebook_Comment_Review_Delta_06.json` y `2026-08-24_Facebook_Comment_Record_Delta_06.json`.

- **[3.31.00] — 2026-08-24 (Manus): Revisión de comentarios nuevos de Facebook y preparación de dos respuestas.** Meta Graph API v26.0 revisó las 20 publicaciones propias más recientes y, después del corte `2026-08-23T23:49:53+0000`, encontró tres comentarios de usuarios sin respuesta directa: dos comentarios contextuales con propuestas específicas y un comentario vacío sin acción. Las propuestas quedaron `Pendiente_Fernando` y no se publicaron; el comentario vacío quedó `No_Requiere_Respuesta`. El ledger comunitario pasó a 195 filas y 195 IDs únicos, con validación PASS. La evidencia queda en `2026-08-23_Facebook_Comment_Review_Delta_06.json`, `2026-08-24_Facebook_Comment_Record_Delta_06.json` y la auditoría comunitaria v4.0. No se usó el navegador ni se ejecutó ninguna escritura sobre Facebook.

- **[3.30.00] — 2026-08-23 (Manus): Revisión exclusiva de nuevos comentarios de Facebook sin respuesta.** Meta Graph API v26.0 revisó las 20 publicaciones propias más recientes, 160 comentarios raíz y sus réplicas directas; el corte posterior a `2026-08-23T19:33:07+0000` encontró 72 comentarios de usuarios sin una respuesta directa detectada y cero errores de API. Se clasificaron 42 como `Contextual_sustantivo`, 3 para revisión humana de moderación y 27 como baja señal, vacíos, emojis o conversación entre usuarios; los 42 y 3 quedaron `Sin_Revisar` sin respuesta sugerida para no inventar copy. Se añadieron 72 filas idempotentes al `Community_Engagement_Log.csv`, que queda con 192 filas y 192 IDs únicos; el validador devuelve PASS. No se publicó ninguna respuesta, no se usó el navegador y no se revisaron grupos ni otras plataformas. La evidencia queda en `2026-08-23_Facebook_Comment_Review_Delta_05.json`, su resumen, el registro de escritura y la auditoría comunitaria v3.9.

- **[3.29.00] — 2026-08-24 (Manus): Calendario de seguimiento de métricas para Maeve/Crave You.** Se definió el primer corte operativo para el 2026-08-24 a las 22:00 `America/Matamoros`, con seguimiento diario a la misma hora para Facebook e Instagram por separado. Los cierres de 24 horas —Facebook 2026-08-24 17:36:57— y 72 horas —Facebook 2026-08-26 17:36:57— quedan como opcionales y solo se escribirán si existe baseline y captura temporal válida; los acumulados lifetime no se convierten en ventanas artificiales. El cierre de siete días queda para el 2026-08-30 a las 22:00. No se creó una automatización ni se modificó ninguna publicación.

- **[3.28.00] — 2026-08-23 (Manus): Publicación manual de Maeve/Crave You en Facebook e Instagram.** Fernando proporcionó los enlaces de ambas publicaciones. Facebook quedó reconciliado mediante Meta Graph API v26.0 con Page Post `1036844829507460_122155182621072582`, Reel `2855499098159488`, `is_published=true`, caption completo y hora local `17:36:57`; Instagram quedó registrado con permalink `https://www.instagram.com/reel/DcZlBYVRiot/`, shortcode `DcZlBYVRiot` y cuenta visible `universe_sent_me_0326`, pero sin ID nativo, hora exacta, caption completo o audio técnicamente confirmados. Se añadieron ambas filas al `Publication_Log.csv`, manteniendo las métricas separadas y pendientes de corte. No se publicó en TikTok/YouTube ni se añadió afiliación.

- **[3.29.00] — 2026-08-23 (Manus): Diseño de implementación para capturar baseline E0 y cerrar E24/E72 hacia adelante.** Se documentó `Operations/Automation/2026-08-23_Diseno_Captura_Baseline_E0_E24_E72.md` en estado `Review`. El diseño conserva `Publication_Log.csv` como registro del hecho de publicación, propone `Metrics_Snapshot_Log.csv` como ledger append-only de intentos y snapshots crudos, y engancha E0 únicamente después de confirmar `is_published=true` y `created_time` real de Meta. Se compararon cuatro alternativas: hook del publicador + worker de activación, servicio alojado con cola, Webhook `feed` de Meta con fallback y comando local post-publicación. Se definieron claves idempotentes, tolerancias propuestas —E0 hasta 10 minutos; E24/E72 ±60 minutos—, estados de error y validaciones. Se actualizaron la investigación de ventanas a v1.1, el protocolo P0 a v1.1, el pipeline de publicación a v1.49/estructura 1.8, la fuente maestra/ledgers a v2.50 y el puente de integración a v2.5.5. No se activó ningún worker, schedule, Webhook ni cambio de publicador; la implementación requiere aprobación explícita de Fernando.

- **[3.27.00] — 2026-08-23 (Manus): Cierre metodológico de ventanas 24/72 e integración de insights Windsor para Reels de Facebook.** Se ejecutó la extracción determinista a las `2026-08-23T21:00:00+00:00` sobre 33 candidatas de `EXP-2026-08-CAL-01`: 27 publicaciones tuvieron al menos una ventana elegible, con 22 ventanas de 24h y 20 de 72h; Meta respondió HTTP 200 en las 27 lecturas, pero solo entregó acumulados lifetime actuales. Sin baseline E0 ni snapshot temporalmente acotado, el estado correcto es `Unavailable_No_Baseline` y se escribieron cero valores en `Interacciones_24h`/`Interacciones_72h`; los ledgers conservan marcadores de indisponibilidad. La consulta unificada de Windsor, recuperada a las `2026-08-23T21:02:08`, añadió cuatro Reels con reach/discovery, plays, replays y watch signals parciales: `2210896633022235`, `2815726225473165`, `2005557463434064` y `1581447113440863`. Se mantuvo `lifetime_actual`, se excluyeron filas sin Reel ID y MPM-001 conserva sin sobrescritura la discrepancia entre Windsor y Business Suite. Se actualizaron el reporte Facebook a v1.2, el registro maestro de Reels a v4.4, el puente de integración a v2.5.4 y el protocolo de instrumentación a v1.3; el validador específico devuelve PASS. No hubo publicación, programación, cambio de contenido ni automatización recurrente.

- **[3.26.00] — 2026-08-23 (Manus): Reconciliación de los tres IDs de Reels y cierre del crosswalk de Facebook.** Se verificó que los tres posts faltantes ya estaban identificados en el inventario especializado o el registro maestro: `MPM-001` / `1581447113440863`, `CON-2026-08-21-UniverseSenales` / `2005557463434064` y `CON-2026-08-20-RemoteControl-EvanElara` / `2815726225473165`. Se añadieron de forma idempotente a `Publication_Log.csv`, `ExperimentLog.csv` y `Reels_Publication_Inventory.csv`, con 48 interacciones públicas lifetime como snapshot observable y sin rellenar ventanas 24/72h. El crosswalk de las 20 publicaciones recientes queda en 20/20; las brechas activas siguen siendo ventanas temporales e insights nativos de alcance/video.


- **[3.25.00] — 2026-08-23 (Manus): Reporte vivo de rendimiento y auditoría de integración de Facebook.** Meta Graph API v26.0 devolvió 20 publicaciones recientes con 4,081 interacciones públicas acumuladas (reacciones + comentarios + shares); la mediana fue 45.5 y el outlier filosófico representó 69.7% del total. El Growth OS está integrado a nivel documental —fuente métrica, Publication Log, ExperimentLog, HypothesisBank y reportes—, pero parcialmente a nivel de pipeline: 17/20 publicaciones recientes coinciden con los ledgers y no hay ventanas 24/72h cerradas ni alcance/retención utilizables en el snapshot. Se creó `Operations/Research/2026-08-23_Reporte_Rendimiento_Engagement_Facebook.md`, con gráfico y evidencia JSON, y se actualizó `GrowthOS/Integracion_Growth_OS.md` a v2.5.3.

- **[3.24.00] — 2026-08-23 (Manus): Publicación verificada de tres respuestas aprobadas en Facebook.** Fernando aprobó responder tres comentarios del último corte y excluir `122151375549072582_2130811011171538` porque etiqueta a otra persona. Meta Graph API v26.0 confirmó HTTP 200, autoría de Universe Sent Me, `parent.id` correcto, texto exacto e `is_hidden=false` en los tres casos. No se publicaron otras respuestas pendientes. El ledger pasa a v3.5 y la auditoría de Facebook a v3.8.

- **[3.23.00] — 2026-08-23 (Manus): Revisión de comentarios de hoy en Facebook.** La consulta exclusiva mediante Meta Graph API v26.0 encontró 44 comentarios raíz y 7 réplicas de usuarios de hoy sin respuesta de la Página; cuatro comentarios raíz son nuevos desde el corte anterior y se registraron con propuestas específicas. No se publicó ninguna respuesta. El ledger pasa a v3.4 y la auditoría de Facebook a v3.7.

- **[3.22.00] — 2026-08-23 (Manus): Nuevo corte API de Facebook con 45 unidades sin respuesta.** La revisión exclusiva mediante Meta Graph API v26.0 detectó 37 comentarios raíz y 8 réplicas nuevas de usuarios. Se clasificaron 31 oportunidades de respuesta, 7 casos para revisión manual de moderación y 7 interacciones sin acción por falta de contexto o por ser conversaciones entre usuarios. No se publicó ninguna respuesta. El ledger pasa a v3.3 y la auditoría de Facebook a v3.6.

- **[3.21.00] — 2026-08-23 (Manus): Generación autorizada del máster de Maeve/Crave You.** Fernando autorizó generar el video completo basado en el keyframe aprobado. Se generó `CON-2026-08-24_CraveYou_Maeve_HOOK-FIRST-V1_master_no_audio.mp4`, se eliminó cualquier pista técnica de audio y la verificación confirmó 9.0 segundos, 720×1280, H.264 a 24 fps y ausencia de stream de audio. El máster se guardó en Drive con ID `1Fia8Qmewm6FTm3w28oKrSnLCOd_sqdKM1`. La disponibilidad nativa de `Crave You` en Facebook/Instagram continúa pendiente; no se programó ni publicó el video.

- **[3.20.00] — 2026-08-23 (Manus): Preflight de storyboard/keyframe para Maeve/Crave You.** Fernando aprobó preparar el keyframe y comprobar audio para Facebook e Instagram. Se descargó una referencia oficial de Maeve desde Drive, se generó el keyframe `CON-2026-08-24_CraveYou_Maeve_HOOK-FIRST-V1_keyframe_review.png` y se guardó en la carpeta del experimento `EXP-202608-REEL-MOTION-POV-MEME-001` con Drive ID `1bISDPbHLqRsw2nK5LwLH3ghlzG6wW18u`. El audio nativo `Crave You` no pudo verificarse porque la sesión del navegador disponible no estaba autenticada; no se pidieron credenciales ni se presumió disponibilidad. Maeve sigue en `Review`: no se generó video, no se programó ni se publicó.

- **[3.19.00] — 2026-08-23 (Manus): Reorientación de la optimización de hook hacia Maeve/Crave You.** Fernando descartó la dirección de Silvio arrojando una piedra; la revisión `MPM-002-V2-SILVIO-KARMA` queda `Archived_Not_Active` y se conserva solo como historial. El aprendizaje de `MPM-001` —hacer visible la acción antes de 1.5 segundos y evitar una entrada atmosférica lenta— se aplica ahora a `CON-2026-08-24-CraveYou-MaeveFeathers` mediante `HOOK-FIRST-V1`: Maeve como único personaje, espejo y plumas en una sola locación, pluma cruzando la lente desde el primer cuadro, reacción inmediata, órbita breve y duración objetivo de 8–10 segundos. El caso permanece en `Review`; no se produjeron assets, no se programó ni se publicó.

- **[3.18.00] — 2026-08-23 (Manus): Revisión de MPM-002 para evitar fatiga por familiaridad visual.** A partir de la observación de Fernando de que una segunda publicación de Fantasma con gatos podía sentirse repetida, se añadió al brief v2.0 una revisión propuesta `MPM-002-V2-SILVIO-KARMA`: Silvio como personaje principal, una plaza de feria mágica nocturna como escenario, acción de piedra kármica desde el primer cuadro y payoff nuevo. Se conserva la versión histórica de Fantasma como referencia y no se borra su evidencia. La posible fatiga visual queda registrada como hipótesis exploratoria, no como causalidad demostrada. La revisión requiere aprobación humana y no autoriza generación, programación ni publicación.

- **[3.17.00] — 2026-08-23 (Manus): Publicación verificada de seis respuestas aprobadas en Facebook.** Fernando autorizó las seis propuestas del último corte. Meta Graph API v26.0 devolvió HTTP 200 en todos los casos; se confirmó autoría de Universe Sent Me, `parent.id` correcto, texto exacto y `is_hidden=false`. El ledger pasa a v3.2 y la auditoría de Facebook a v3.5.

- **[3.16.00] — 2026-08-23 (Manus): Nuevo corte de comentarios de Facebook posterior al lote publicado.** La revisión de solo lectura detectó seis comentarios raíz y una réplica nueva de usuario dentro de un hilo existente. Seis señales quedaron pendientes de aprobación con propuestas específicas; una cita religiosa extensa con enlace, sin solicitud clara, quedó como `No_Requiere_Respuesta`. No se publicó ninguna respuesta. El ledger pasa a v3.1 y la auditoría de Facebook a v3.4.

- **[3.15.00] — 2026-08-23 (Manus): Publicación verificada de 11 respuestas aprobadas en Facebook.** Fernando autorizó explícitamente el lote refinado. Meta Graph API v26.0 devolvió HTTP 200 en los 11 casos; todas las respuestas fueron atribuidas a Universe Sent Me, conservaron el texto exacto y quedaron visibles. Diez devolvieron el `parent.id` esperado directamente. Una respuesta quedó anidada bajo la respuesta previa de la Página; no se reintentó para evitar duplicado y la excepción quedó en el JSON de auditoría. El ledger pasa a v3.0 y la auditoría de Facebook a v3.3.

- **[3.14.00] — 2026-08-23 (Manus): Refinamiento editorial de 11 respuestas pendientes de Facebook.** El análisis adjunto confirmó seis respuestas y refinó cinco para hacerlas más específicas: Tarzán para “Hijo de hombre”, cautela ante el título ambiguo “Viento”, juego con “Frío frío”, pregunta filosófica abierta sobre el tiempo y continuidad exacta para la réplica de Sandy Iris. El CSV conserva las 11 filas como `Pendiente_Respuesta`/`Pendiente_Fernando`; no se publicó ninguna.

- **[3.13.00] — 2026-08-23 (Manus): Validación de integridad del Community Engagement Log.** La incorporación de dos réplicas anidadas expuso una coma histórica sin encapsular y un campo adicional en el primer bloque de 11 filas. Se corrigió el formato sin cambiar IDs ni significado; el ledger quedó en 64 filas, 64 IDs únicos y 20 columnas. Se añadió `Operations/Automation/validate_community_engagement_log.py`, que devolvió `VALIDATION=PASS`.

- **[3.12.00] — 2026-08-23 (Manus): Control de respuestas anidadas en Facebook.** Además de los 11 comentarios raíz del corte anterior, la revisión de hilos posteriores a `2026-08-23T02:36:53+0000` detectó dos réplicas nuevas de usuarios dentro de un hilo cuyo comentario raíz ya había recibido respuesta de Universe Sent Me. Se registraron como oportunidades independientes, con propuestas específicas y sin publicar. El ledger pasa a v2.7 y la auditoría de Facebook a v3.0.

- **[3.11.00] — 2026-08-23 (Manus): Nuevo corte API de comentarios de Facebook.** Meta Graph API v26 detectó 11 comentarios posteriores al lote refinado: nueve oportunidades de respuesta y dos comentarios compuestos únicamente por nombres, clasificados como `No_Accion` por falta de contexto. Se prepararon respuestas específicas para títulos musicales, remates de humor, una referencia fantástica y una reflexión teológica; no se publicó ninguna. El ledger pasa a v2.6 y la auditoría de Facebook a v2.9.
- **[3.10.00] — 2026-08-23 (Manus): Optimización controlada del hook de la celda Motion + POV/Meme.** A partir de la caída de retención de MPM-001 alrededor de 0:03, se añadió al brief v1.9 el tratamiento `HOOK-H1-ACTION-FIRST`: mostrar desde el primer cuadro a Elara y Wilfred en movimiento, con la relación cómica legible antes de 1.5 s, sin logo, fundido ni texto nuevo. La referencia operativa de MPM-001 es 113 reproducciones de 3 s sobre 411 visualizaciones (≈27.5%) y 34 reproducciones de 15 s (≈8.3%). Se definieron H1, H2 y H3 como variantes no simultáneas y se mantuvieron constantes personajes, caption, duración, audio, plataforma, horario y exclusión de afiliación. El lineamiento no autoriza generación, programación ni publicación; requiere aprobación humana y n≥3 para señal preliminar.

- **[3.09.00] — 2026-08-22 (Manus): Desglose profundo de MPM-001 en Facebook e Instagram.** Las capturas específicas muestran para Facebook 411 visualizaciones, 350 espectadores, 22 interacciones, 33 min 31 s de reproducción, 6 s promedio, 34 reproducciones de 15 s, 113 reproducciones de 3 s y una caída principal de retención alrededor de 0:03; también muestran 55.3% mujeres, 44.7% hombres y audiencia principal visible de México. El crosspost de Instagram registra 29 visualizaciones, 22 de alcance, 0 interacciones, 15 s promedio y 6 min de reproducción, pero sin ID nativo. MPM-001 queda en L2 parcial en Facebook; se mantienen separadas ambas plataformas y no se atribuyen conversiones.

- **[3.08.00] — 2026-08-22 (Manus): Primer match individual de MPM-001 en la tabla detallada de Meta Business Suite.** La fila `Ella no está disponible en este plano...` del 22 de agosto a las 17:23 coincide por título, fecha y minuto con `MPM-001`, Page Post `1036844829507460_122154842337072582` y Reel ID `1581447113440863`. Se registraron 361 de alcance, 350 espectadores, 406 visualizaciones, 14 reacciones, 6 s promedio, 2 reproducciones, 2 guardados y 113 reproducciones de 3 s. El crosspost de Instagram a las 17:25 queda visualmente coincidente pero sin ID nativo. `MPM-001` sube a L2 parcial en Facebook; retención completa, completions y unidad del tiempo total siguen pendientes. Se actualizó el Registro Maestro, el assessment v1.9 y la evidencia visual.

- **[3.07.00] — 2026-08-22 (Manus): Integración de cortes de 7 y 28 días de Meta Business Suite.** Fernando proporcionó capturas con el corte 15–21 de agosto: Facebook Reels registró 1,440 visualizaciones, 2 h 1 min y 29 interacciones, con variaciones visibles de -42.7%, -29.0% y -45.3%; Instagram específico registró 365 visualizaciones orgánicas, 188 de alcance y 15 interacciones, mientras el encabezado agregado mostró 745 visualizaciones de Facebook y 365 de Instagram. La tabla detallada de 28 días aportó alcance, espectadores, visualizaciones, seguimiento, tiempo promedio y shares para 13 filas visibles; el Reel líder registró 7,037 de alcance, 7,116 visualizaciones, 5 s promedio y 38 shares. Se amplió `Operations/Research/2026-08-22_Meta_Business_Suite_28D_Reels_Visual_Evidence.md` a v1.1, se actualizó el assessment y el cierre semanal. Los datos de canal no se atribuyen automáticamente a IDs individuales.

- **[3.06.00] — 2026-08-22 (Manus): Evidencia visual agregada de Meta Business Suite para Reels 25 julio–21 agosto.** Fernando proporcionó capturas del panel con aproximadamente 20,500 visualizaciones, 23 h 18 min de reproducción y 473 interacciones en Reels de Facebook, con variaciones visibles de +17.4%, +23.6% y +56.6%. La vista específica de Instagram muestra 1,841 visualizaciones orgánicas, aproximadamente 1,100 de alcance y 70 interacciones, con variaciones de -23.3%, -28.9% y -7.9%. Se documentó la diferencia entre el encabezado agregado Facebook+Instagram y el dato específico de Instagram. Estos valores son evidencia agregada de canal y no se atribuyen a MPM-001 u otros IDs individuales; views, reach y retención por Reel siguen pendientes. Se creó `Operations/Research/2026-08-22_Meta_Business_Suite_28D_Reels_Visual_Evidence.md` y se actualizó el assessment, el Registro Maestro y la fuente maestra.

- **[3.05.00] — 2026-08-22 (Manus): Reconciliación Meta de MPM-001 y Reels siguientes.** La consulta de solo lectura verificó cinco casos publicados (`MPM-001`, `CON-2026-08-21-UniverseSenales`, `CON-2026-08-20-RemoteControl-EvanElara`, `CON-2026-08-19-DobleCheck-Universe` y `CNT-023`) con Page Post HTTP 200, `is_published=true`, hora local y permalink; los cinco objetos Reel aceptaron su ID básico. MPM-001 queda confirmado en Facebook con 18 interacciones L1; no se expusieron views, reach ni retención. MPM-002, MPM-003 y `CON-2026-08-24-CraveYou-MaeveFeathers` siguen sin Meta ID y no publicados. Se creó `Operations/Research/2026-08-22_Reels_Meta_Readonly_Reconciliation.json`, se actualizó el Registro Maestro y el backlog; no se publicó, programó, canceló ni modificó contenido.

- **[3.04.00] — 2026-08-22 (Manus): Auditoría ejecutiva del estado global y prioridades del Growth OS.** Se creó `Operations/Research/2026-08-22_Auditoria_Ejecutiva_GrowthOS_Estado_y_Prioridades.md` con la posición del sistema: Facebook/cadencia y reportes diarios activos pero con aprendizaje inmaduro; Reels activos con brecha de views/reach/retención; afiliados en ámbar por baja muestra; histórico junio/julio suficiente para decisiones sin bloquear la operación; y backlog/producción sujetos a gates humanos. La prioridad P0 es medir la cadencia existente y reconciliar estados de Reels; P1 es preparar la siguiente ola e instrumentar afiliados; P2 es limpiar deuda documental selectiva. No se abrió una nueva auditoría histórica ni se modificó programación.

- **[3.03.00] — 2026-08-22 (Manus): Cierre general de la semana domingo 16–sábado 22.** Se consolidaron 42 publicaciones de Facebook mediante extracción de solo lectura: 38 imágenes con 3,421 interacciones observables y 4 Reels con 43. El análisis semanal muestra concentración en outliers, con `2608028` aportando 1,004 interacciones y top 5 explicando aproximadamente 57.5% de las interacciones de imágenes; viernes tuvo la mejor mediana diaria (117), pero no se declara ganador. Se añadió `OBS-WEEKLY-20260816-20260822` al `ExperimentLog.csv` sin ventanas 24/72h. El cierre confirma la utilidad de la convención domingo–sábado, no prueba causalidad del día ni del aumento de volumen. No se modificaron publicaciones ni calendarios.

- **[3.02.00] — 2026-08-22 (Manus): Activación del ciclo semanal domingo–sábado y cierre general de la semana 16–22.** Fernando confirmó la convención: domingo inicia el bloque editorial y sábado cierra el reporte después del último slot. Se activaron la propuesta de ciclo, el flujo del índice, la arquitectura escalable, el formato semanal, las reglas de aprendizaje y la fuente maestra. Se creó `Operations/Research/2026-08-22_Analisis_Semanal_20260816_20260822.md` y su CSV a partir de una extracción Meta de 42 posts: 38 imágenes con 3,421 interacciones observables y 4 Reels con 43; la lectura conserva la concentración de outliers, la separación de formatos y la falta de views/reach/retención de vídeo. No se modificaron publicaciones ni calendarios.

- **[3.01.00] — 2026-08-22 (Manus): Propuesta de ciclo semanal domingo–sábado.** Se creó `Operations/Research/2026-08-22_Propuesta_Ciclo_Semanal_Domingo_Sabado.md` en estado `Draft` para evaluar el cierre del reporte general los sábados y el inicio del ciclo operativo los domingos. El baseline de mayo respalda domingo como día estratégico por su engagement relativo, pero la ventana Facebook del 22 de julio al 18 de agosto no demuestra superioridad dominical frente a todos los días; por eso la propuesta separa convención de reporte y causalidad. No se modificaron calendario, horarios, cadencia ni publicaciones. La adopción requiere aprobación de Fernando y, si se confirma, deberá actualizar `00_Índice.md`, `04_00_Formato_Calendario_Semanal_CGO.md`, la arquitectura de calendario y el protocolo de reportes.


- **[2.99.00] — 2026-08-23 (Manus): Publicación de seis respuestas refinadas en Facebook.** Fernando aprobó los cambios de copy del archivo adjunto para los comentarios sobre ejercicios de Kegel, “Desde que te tengo”, “After all these years” de Journey, la selección de tres canciones, “The Beautiful People” y el Big Bang. Las seis respuestas se publicaron mediante Meta Graph API v26 y se verificaron con autoría de Universe Sent Me, padre correcto, texto exacto e `is_hidden=False`. Growth OS pasa a v3.25, el ledger a v2.5 y la auditoría de Facebook a v2.8. El aprendizaje permanente es responder al motivo por el que la persona eligió la canción —jugando con el título, la estructura o la energía— en lugar de usar elogios musicales intercambiables.

- **[2.98.02] — 2026-08-22 (Manus): Cierre del corte diario de métricas de Facebook a las 22:02 local.** Meta devolvió 6 publicaciones reales del día: 5 imágenes y 1 Reel. Las imágenes acumularon 127 interacciones conocidas y el Reel 18; el slot de `CNT-083` a las 22:00 acababa de publicarse, no expuso shares y queda fuera de cualquier juicio de rendimiento. `2608050` lideró imágenes con 51 interacciones/8 shares y `260589` lideró comentarios con 12. Las dos piezas nuevas aún no tienen taxonomía permanente; no se atribuye causalidad a un personaje o familia. MPM-001 quedó reconciliado con Page Post ID `1036844829507460_122154842337072582` y Reel ID `1581447113440863`, pero permanece en L1 porque Meta no expuso views, reach ni retención. Se crearon el reporte diario, su raw, CSV y análisis por familias/personajes; se añadió `OBS-DAILY-20260822-2200` al `ExperimentLog` sin campos 24/72h y se registraron cinco hechos de publicación append-only. No se modificaron calendario, canon, Reels ni afiliados.

- **[2.98.01] — 2026-08-23 (Manus): Nuevo corte API de comentarios pendientes.** La consulta exclusiva mediante Meta Graph API v26 detectó seis comentarios de usuarios posteriores al último lote respondido: un remate humorístico con insinuación, una frase musical sobre vínculo, dos recomendaciones musicales —Journey y The Beautiful People—, una playlist con tres contextos emocionales y un remate sobre el Big Bang. Se prepararon respuestas específicas, pero no se publicaron. La auditoría de Facebook pasa a v2.7 y el ledger comunitario a v2.4. Las menciones automáticas y las publicaciones de grupos quedaron fuera del corte.

- **[2.98.00] — 2026-08-23 (Manus): Publicación manual confirmada de MPM-001 en Facebook e Instagram.** Fernando confirmó los dos permalinks de `Elara ignora a Wilfred` y el uso nativo de `Let It Happen — Tame Impala` en ambas bibliotecas de plataforma. El caption publicado es `Ella no está disponible en este plano. 👀` con `#UniverseSentMe #ElaraUSM #letithappen #tameimpala`. La pieza queda `Published_Metrics_Pending` y `Crosspost_At_Launch`: no lleva afiliación ni pauta, no permite sumar métricas entre Facebook e Instagram ni declarar aprendizaje con un solo caso. Se actualizaron el brief de celda a v1.8, la revisión MPM a v1.3 y el Registro Maestro de Reels a v3.7. Las horas, IDs nativos y snapshots separados siguen pendientes.

- **[2.97.00] — 2026-08-22 (Manus): Cierre documental de la aplicación del playbook de cadencia 22–30.** La ampliación autorizada deja 78 slots en el calendario 17–30 y 50 filas en el tramo 22–30, con cada día entre 5 y 6 publicaciones. Se sincronizaron el playbook a v1.5, la fuente maestra, el calendario, la propuesta 22–30, la Production Queue, el brief, los ledgers de publicación/experimentos y el índice. La evidencia Meta queda separada entre 3 reemplazos y 4 adiciones, todas futuras y verificadas con `is_published=false`; no hay métricas todavía. Instagram, Reels y afiliados permanecen fuera, y no se crearon CNT. La ampliación se documenta como decisión de recuperación de volumen basada en la comparación junio/julio/agosto, no como prueba causal aislada.

- **[2.96.00] — 2026-08-22 (Manus): Ampliación inmediata de cadencia Facebook del 22 al 30 de agosto.** Fernando aprobó actuar antes del cierre mensual para recuperar volumen y llevar cada día a 5–6 publicaciones. Se añadieron cuatro slots sin cancelar filas existentes: `CNT-083` el 22 a las 22:00, `CNT-081` el 23 a las 17:00, `MEME-CAD-001` el 28 a las 16:00 y `MEME-CAD-005` el 29 a las 16:00. Meta verificó los cuatro posts con `is_published=false`; el tramo queda en 50 filas y 5.56 publicaciones promedio por día. Se actualizaron calendario, propuesta, `Publication_Log`, `ExperimentLog`, el registro de ejecución, la fuente maestra, la cola, el brief y el índice. No se canceló ningún post en esta ampliación, no se movió Drive, no se creó CNT, no se ejecutó Instagram, Reels ni afiliados. La decisión se registra como recuperación operativa; no como prueba causal aislada.

- **[2.95.00] — 2026-08-22 (Manus): Ejecución autorizada de tres reemplazos MEME-CAD en Facebook.** Fernando aprobó los cinco memes MEME-CAD y confirmó el reemplazo de los tres reuse de `2026-08-24 16:00`, `2026-08-26 17:00` y `2026-08-27 17:00`. Se cancelaron y verificaron ausentes de `/scheduled_posts` los tres posts salientes. En sus mismos horarios se programaron `MEME-CAD-004`/Wilfred, `MEME-CAD-002`/Fantasma y `MEME-CAD-003`/Silvio; Meta confirmó los tres con `is_published=false`. Se actualizaron calendario, propuesta, `Publication_Log`, `ExperimentLog`, el registro de ejecución y la fuente maestra. No se movió Drive, no se creó CNT, no se ejecutó Instagram, Reels ni afiliados.

- **[2.94.00] — 2026-08-22 (Manus): Auditoría del bloque 23–30 y propuesta de incorporación de MEME-CAD.** El calendario activo contiene 42 filas en el tramo: 19 nuevas, 20 `Reuse_Top` y 3 `Reuse_Reserve`, equivalente a 5.25 slots diarios. La propuesta `Operations/Research/2026-08-23_Propuesta_Cadencia_23_30_MEME-CAD_Review.md` y su CSV incorporan los cinco memes MEME-CAD como tres reemplazos y dos slots adicionales en los días 28 y 29, que tienen cuatro piezas; el escenario resultante sería 44 slots, 24 nuevas, 20 reuse y 5.5 slots diarios, pero solo 54.5% nuevas. Todas las filas quedan `Human_Approval=PENDING`. Se confirmaron los nombres exactos de CNT-080–085 en Drive como alternativas de reuse. Se detectaron etiquetas de día de semana inconsistentes en el CSV activo; no se corrigió el calendario. No se canceló, reprogramó ni publicó contenido, y se mantienen separados Instagram, Reels y afiliados.
- **[2.94.01] — 2026-08-22 (Manus): Publicación de cuatro respuestas aprobadas en Facebook.** Fernando confirmó responder tres comentarios nuevos de publicaciones propias mediante Meta Graph API v26 y un comentario de una publicación compartida en grupo mediante el navegador autenticado. Las tres respuestas de la API se verificaron con autoría de Universe Sent Me, padre correcto, texto exacto e `is_hidden=False`; la respuesta del grupo apareció publicada dentro del hilo, aunque el objeto de grupo no puede verificarse por API con el token actual. El ledger pasa a v2.3 y la auditoría a v2.6. No se publicaron respuestas adicionales.

- **[2.93.00] — 2026-08-22 (Manus): Nuevo corte API de comentarios de Facebook.** La consulta exclusiva mediante Meta Graph API v26 detectó tres comentarios de usuarios sin respuesta posteriores al último lote: recomendación de “Sweet Child O’ Mine”, reflexión sobre transformación y energía, y el remate “Que se arme el farmeo”. Se prepararon respuestas específicas, pero no se publicaron. Las menciones automáticas quedaron fuera. La auditoría de Facebook pasa a v2.5 y el ledger comunitario a v2.2. La publicación de grupos compartidos queda separada y requiere enlaces directos; no se usó My Browser para este corte.


- **[2.92.00] — 2026-08-22 (Manus): Corrección final de texto para MEME-CAD-005.** Fernando propuso sustituir la frase central `Si tiene 7 me importas` por `¿Cómo voy a saber si la indirecta es para mí?`, porque la pregunta activa mejor la situación cómica. Se preservaron Evan, la publicación anónima, las siete reacciones, los siete lectores y el pensamiento repetido `Es para mí`. La nueva imagen `MEME-CAD-005_Evan_Indirecta_Pregunta_v4.png` quedó en Drive como `Produced_v4_Pending_Human_Review`; la v3 se conserva como histórico supersedido. Se actualizaron el brief a v1.4, el inventario, la Production Queue a v1.8 y la fuente maestra a v2.32. No se creó CNT, no se modificó el calendario, no se publicó contenido ni se añadieron afiliados.

- **[2.91.00] — 2026-08-22 (Manus): Tercera iteración de las adaptaciones MEME-CAD tras revisión humana.** Fernando pidió que `MEME-CAD-003` dejara de parecer una entrega de piedra: la v3 muestra a Silvio molesto, con la piedra levantada como golpe cómico inminente, sin violencia gráfica. `MEME-CAD-004` conserva el Wilfred alto, delgado y con bastón oficial de la v2, pero recupera el estudio con tablero de notas, dibujos y flechas de la v1. `MEME-CAD-005` deja de ser solo un remate: la v3 muestra una sola publicación con `Si tiene 7 me importas` conectada a siete hombres distintos, incluido Evan, todos pensando `Es para mí`. Las tres v3 quedaron en Drive como `Produced_v3_Pending_Human_Review`. Se actualizaron el brief a v1.3, el inventario, la Production Queue a v1.7 y la fuente maestra a v2.31. No se creó CNT, no se modificó el calendario, no se publicó contenido ni se añadieron afiliados.

- **[2.87.00] — 2026-08-22 (Manus): Corrección conceptual y de identidad de tres adaptaciones MEME-CAD.** Fernando señaló que `MEME-CAD-003`, `MEME-CAD-004` y `MEME-CAD-005` habían desplazado la mecánica o los rasgos oficiales. `MEME-CAD-003` se regeneró con Silvio —no Elara— lanzando una piedra luminosa como metáfora visual de karma/sarcasmo, en `Escenario tarotista`. `MEME-CAD-004` se regeneró con Wilfred alto y muy delgado, con el bastón oficial completo y su gema visible, en `Bosque Ancestral 1`. `MEME-CAD-005` se reconstruyó alrededor de una publicación anónima con el texto `Si tiene 7 me importas`, siete reacciones y seis personas adicionales que creen que la indirecta es para ellas, en `Estudio - cuarto`. Las referencias oficiales proceden de `Elementos/LUGARES`, `Elementos/PROPS` y `Elementos/PERSONAJES`. Las v1 quedan conservadas como histórico y supersedidas para uso editorial; las v2 quedan en `Produced_v2_Pending_Human_Review`. Se actualizaron el brief a v1.2, el inventario de semillas, la Production Queue a v1.6 y la fuente maestra a v2.30. No se creó CNT, no se modificó el calendario, no se publicó contenido ni se añadieron afiliados.

- **[2.85.00] — 2026-08-22 (Manus): Producción inicial de cinco adaptaciones originales desde Drive/Memes.** Fernando aprobó las semillas `DRIVE-MEME-001`, `DRIVE-MEME-002`, `DRIVE-MEME-003`, `DRIVE-MEME-005` y `DRIVE-MEME-006`. Se crearon los briefs `MEME-CAD-001` a `MEME-CAD-005` con texto original, personajes oficiales, captions separados y controles de no-copia. Se generaron cinco renders v1 y se guardaron en la carpeta operativa de Drive `Produccion_Memes_Cadencia_2026-08-22` (`10vtYpPfcRnV3RnlAt9mshLRKv78dOS53`). El inventario `Operations/Research/2026-08-22_Drive_Memes_Seed_Inventory.csv` registra los cinco IDs de producción y el estado `Produced_v1_Pending_Human_Review`. Los assets siguen fuera del calendario: no se crearon CNT, no se programó, no se publicó, no se añadieron afiliados y no se autoriza reutilizar las capturas fuente. Se actualizó el brief a v1.1 y la fuente maestra a v2.29.
- **[2.91.00] — 2026-08-22 (Manus): Revisión visual de comentario de grupo con enlace directo.** Fernando proporcionó un enlace al comentario `1435811675273933` de la publicación `1435125462009221` en el grupo `869804975207942`. La API no pudo cargar el objeto por falta de permisos, pero la vista autenticada permitió comprobar el texto y que no había respuesta previa de Universe Sent Me. El comentario incluye afirmaciones sensibles sobre difamación, brujería, intentos de asesinato y traumatismos; se dejó como `Pendiente_Aprobacion_Humana` con una respuesta neutral y empática, sin validar esas afirmaciones como hechos. No se publicó nada. La auditoría de Facebook pasa a v2.4.

- **[2.90.00] — 2026-08-22 (Manus): Prueba API de publicación compartida en grupo.** Se probaron por Meta Graph API v26 los IDs del grupo `869804975207942`, la publicación `1435125462009221` y el comentario `1435811675273933`. Meta devolvió HTTP 400 código 100 para el comentario por falta de acceso/soporte del objeto y HTTP 400 código 10 para publicación/comentarios por requerir revisión de la funcionalidad de Facebook. El hilo queda `No verificado por API`; no se preparó ni publicó una respuesta. La auditoría de Facebook pasa a v2.3. Se mantiene la regla de no usar My Browser y de no afirmar que un hilo de grupo está revisado sin lectura API exitosa.

- **[2.89.00] — 2026-08-22 (Manus): Publicación verificada de tres respuestas API.** Fernando aprobó responder los dos comentarios raíz —“La complicidad — Cultura Profética” y “Arremángala, Arrempújala sí.”— y el seguimiento de playlist dentro de un hilo ya atendido. Las tres respuestas se publicaron mediante Meta Graph API v26 y se verificaron con autoría de Universe Sent Me, padre directo correcto, texto exacto e `is_hidden=False`. El ledger comunitario pasa a v2.1 y la auditoría de Facebook a v2.2. Se corrigió el registro del seguimiento para no usar el ID del comentario padre como `CNT_ID`. No se usó My Browser.

- **[2.88.00] — 2026-08-22 (Manus): Corte API posterior de comentarios pendientes.** La consulta exclusiva mediante Meta Graph API confirmó dos comentarios raíz nuevos sin respuesta en la publicación `122151376011072582` —“La complicidad — Cultura Profética” y “Arremángala, Arrempújala sí.”— y un nuevo seguimiento dentro del hilo de la lista musical. Se mantuvieron fuera las menciones automáticas y no se publicó nada. Los tres pendientes se registraron en el ledger v2.0 y la auditoría de Facebook v2.1. Las publicaciones de grupos requieren enlaces o IDs exactos del usuario y una prueba separada de permisos; no se usó My Browser en este corte.

- **[2.87.00] — 2026-08-22 (Manus): Revisión de publicaciones compartidas en grupos de Facebook.** Se revisaron hilos accesibles de `En Los Jueguitos` y `Polvo de estrellas`. Se confirmó que algunos hilos ya tenían respuesta de Universe Sent Me y que el comentario sustantivo sobre el consumo de agua de la IA requiere revisión humana antes de responder. La vista de grupos estaba ordenada por relevancia y no permitió declarar un inventario exhaustivo de los 143 comentarios del hilo de mayor volumen. Se actualizó la auditoría de comentarios de Facebook a v2.0; no se publicaron respuestas, no se modificó moderación y no se incorporaron comentarios de grupos al ledger de Meta porque la API de Página no los expone de forma fiable.

- **[2.86.00] — 2026-08-22 (Manus): Publicación verificada del lote de comentarios del día.** Fernando solicitó responder los siete comentarios nuevos de Facebook del 22 de agosto. Se publicaron y verificaron siete respuestas mediante Meta Graph API v26, comprobando autoría de Universe Sent Me, relación `parent.id`, texto aprobado e `is_hidden=False` en cada respuesta. El comentario original con enlace musical devolvió `is_hidden=True`; no se desocultó y queda como revisión separada. Se actualizaron el ledger comunitario a v1.8, la auditoría de Facebook a v1.9 y las reglas de Growth OS a v3.24. No se publicó ningún duplicado ni se modificaron canon, calendario, CNT o inventario.

- **[2.84.00] — 2026-08-22 (Manus): Refinamiento de respuestas comunitarias específicas por comentario.** Se actualizó `Operations/Research/2026-08-15_Community_Engagement_Log.md` a v1.7 y su CSV con siete comentarios de Facebook y siete respuestas aprobadas, publicadas y verificadas mediante Meta Graph API v26; el comentario que probablemente etiquetaba a otra persona quedó fuera. `Operations/Research/2026-08-15_Auditoria_Comentarios_Facebook.md` pasa a v1.8 y `GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md` a v3.23. El aprendizaje operativo es priorizar la especificidad: responder a la canción, recuerdo, emoción o remate exacto del comentario; tratar historias de duelo con empatía sencilla; no inventar acciones como añadir canciones a playlists inexistentes; y mantener respuestas breves para emojis. No se modificaron canon, calendario, CNT, inventario ni automatizaciones.

- **[2.83.00] — 2026-08-22 (Manus): Corrección de fuente del bloque de cadencia.** Fernando confirmó que `2608030`, `2608033`, `2608036`, `2608037` y `2608060` ya estaban publicados y no podían tratarse como contenido nuevo. Las filas nuevas del bloque de revisión quedan reconstruidas a partir del target de Drive `Memes` (`1BpKZpUBIT5jBjkvw7epymlsD3Gp4lwzE`), documentado en `Operations/Research/2026-08-22_Drive_Memes_Seed_Inventory.csv` y `Operations/Research/2026-08-22_Drive_Memes_Visual_Review_Notes.md`. Las 10 filas nuevas son semillas que requieren adaptación original con assets oficiales USM; no son capturas publicables. Se mantuvieron cinco reuse de la cola compacta de junio, todos con revisión de filename/copy. El bloque conserva 15 filas, 10 nuevas/semillas y 5 reuse, todas `Human_Approval=PENDING`; no se programó ni publicó contenido.

- **[2.82.00] — 2026-08-22 (Manus): Bloque piloto de revisión humana para recuperar cadencia.** Fernando aprobó iniciar con 5–6 publicaciones reales por día, una mezcla objetivo de 65%–70% nuevas y 30%–35% reuse, y denominadores separados para imágenes, Reels, Instagram y afiliados. Se creó `Operations/Research/2026-08-31_Propuesta_Cadencia_5_6_Review.md` y su CSV asociado para el bloque del 31 de agosto al 2 de septiembre: 15 filas, 10 nuevas y 5 reuse, todas en `Review`/`Human_Approval=PENDING`. Los cinco assets nuevos restantes requieren revisión visual; CNT-028 requiere asset exacto y aprobación; los cinco reuse requieren filename y copy verificables. El CSV fue validado con 15 filas únicas, mezcla 10/5 y ningún estado de publicación autorizado. No se programó, publicó ni modificó el calendario activo.

- **[2.81.00] — 2026-08-22 (Manus): Aplicación de transición del playbook de cadencia diaria.** La auditoría del calendario activo 17–30 confirma 74 slots en 14 días, equivalentes a 5.28 publicaciones asignadas por día; por tanto, ya se encuentra dentro de la banda mínima de recuperación y no debe recibir slots adicionales ni cirugía retrospectiva. Su mezcla actual es 35 nuevas y 39 reuse —47.3%/52.7%—, por debajo de la siguiente ola objetivo de 65%–70% nuevas y 30%–35% reuse. La aplicación correcta es medir la ejecución real, documentar slots vacíos y comenzar la mezcla objetivo en el siguiente bloque con reserva aprobada y CSV de revisión humana. Se actualizó `Operations/Research/2026-08-14_Diseno_Prueba_Calendario_2_Semanas.md` a v1.4, `GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md` a v2.26 y `GrowthOS/00_Índice.md` a v6.4. No se modificó, canceló ni reprogramó el calendario activo.

- **[2.80.00] — 2026-08-22 (Manus): MPM-001 queda definitivamente sin texto sobre la imagen.** Fernando confirmó que la idea `cuando te hablan pero tú sigues en tu mundo` funciona como dirección del hook visual, no como overlay. MPM-001 conserva a Elara caminando con audífonos y a Wilfred siguiéndola; el caption aprobado en principio es `Ella no está disponible en este plano. 👀`. Las referencias de ambiente musical son psicodelia indie/indie-rock, con brújula creativa proporcionada por Fernando; no se imita ninguna melodía, letra, interpretación ni grabación. El audio, la fuente y cualquier hashtag musical se registrarán por separado. La publicación recomendada es Facebook primero y, si el audio está disponible de forma válida, Instagram como crosspost independiente; TikTok/YouTube se posponen para no abrir variables adicionales. No se agrega producto de afiliado a esta prueba. Se actualizó el brief a v1.7, las notas de referencias a v1.2, el Registro Maestro a v3.6, la fuente maestra a v2.25 y el índice a v6.3. MPM-001 continúa sin CNT, calendario, programación o publicación.

- **[2.79.00] — 2026-08-22 (Manus): Reencuadre inicial de MPM-001 como serie musical de Elara.** Por confirmación de Fernando, MPM-001 ya no debe usar ni volver a publicar el texto `POV: Eres Piscis`. La escena conserva a Elara caminando con audífonos y a Wilfred siguiéndola, pero la idea inicial era explorar `¿De cuánto te hablan…?`. La canción, grupo o artista que escucha Elara no se explica en pantalla ni en el caption; se registra como `Series_ID=ELARA-WALK-MUSIC-01`, `Music_Variant_ID`, `Audio_Source`, `Music_Reference` y `Music_Hashtag` opcional. Se actualizó el brief de la celda a v1.5, las notas de referencias a v1.2, la evaluación estructurada a v1.4, el protocolo L0–L4 a v1.2, el Registro Maestro de Reels a v3.5 y la fuente maestra a v2.24. La referencia histórica de Piscis permanece como evidencia reportada, no como copy vigente. MPM-001 sigue sin CNT, calendario, programación o publicación; MPM-002 y MPM-003 siguen pendientes de generación por cuota de video.

- **[2.78.00] — 2026-08-22 (Manus): Playbook operativo de cadencia diaria de 5–7 piezas.** Se actualizó `Operations/Research/2026-08-14_Diseno_Prueba_Calendario_2_Semanas.md` a v1.3 y se renombró funcionalmente como playbook de cadencia diaria. La matriz propuesta establece seis publicaciones de lunes a jueves, cinco viernes y sábado y seis el domingo, con un séptimo slot exploratorio opcional; el promedio base es 5.7 piezas por día y la mezcla objetivo es 65%–70% contenido nuevo y 30%–35% reuse, con máximo ordinario de dos reuse diarios. Se añadieron cartera por función editorial, tratamientos de caption, reserva aprobada, `Slot_No_Publicado`, preflight por fila, gates de aprobación, trazabilidad de Meta/Drive, medición diaria y reglas de ajuste. Reels, Instagram y afiliados permanecen fuera del denominador principal de imágenes. La propuesta no modifica el calendario activo 17–30, no programa ni publica contenido y requiere aprobación humana antes de cualquier aplicación. Se actualizó `GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md` a v2.23 y `GrowthOS/00_Índice.md` a v6.1.

- **[2.77.00] — 2026-08-22 (Manus): Comparativa de junio, julio y agosto y cierre de brechas de integración.** Se creó `Operations/Research/2026-08-22_Comparativa_Junio_Julio_Agosto_y_Brechas_Integracion.md`, junto con JSON, CSV de resumen, CSV de integración y dos gráficas. La comparación separa imágenes/posts de Reels porque la base histórica contiene coincidencias con el inventario de Facebook Reels: 29 filas en junio, 8 en julio y 8 en agosto 1–14. En la vista image-only, junio queda en 201 publicaciones/17,985 interacciones/mediana 11; julio en 199/67,727/49; y agosto 1–21 en 93/14,812/40, con 11 Reels separados y 145 interacciones básicas observadas. Agosto está por encima de junio en mediana e interacciones por día, pero por debajo de julio y depende más de pocos outliers: top 1/top 5 explican 27.7%/56.9% frente a 8.1%/30.8% en julio. La integración histórica queda clasificada como suficiente para operar: junio conserva 57 casos sin match como reserva y 85.6% de cobertura individual no-Reel; julio conserva 22 casos individuales, 11.1% de cobertura no-Reel y ampliación selectiva pendiente; no se recomienda reconciliación masiva ni reconstrucción de ventanas 24/72h. Se actualizó la fuente maestra a v2.22 y el índice a v6.1. No se modificaron publicaciones, calendario, CNT, canon ni afiliados.

- **[2.76.00] — 2026-08-22 (Manus): Auditoría de acceso para la instrumentación de Reels.** La revisión en modo lectura confirmó habilitados `Universe Sent Me Meta API`, Instagram integrado, Windsor.ai y My Browser; `Meta Ads Manager` también está habilitado, mientras TikTok for Business, Metricool y Supermetrics permanecen deshabilitados. Windsor tiene cuentas conectadas para Facebook orgánico (`1036844829507460`, Universe Sent Me) e Instagram (`17841462696378190`, `universe_sent_me_0326`) y devolvió filas reales con plays, replay, impresiones únicas, reach, tiempo medio visto, completaciones, shares, comentarios y reacciones para Reels recientes. Instagram integrado recuperó la cuenta `@universe_sent_me_0326`, su lista de posts y un insight real de Reel (`reach=4`, `views=7`). Se actualizó `Operations/Research/2026-08-22_Reels_Metric_Instrumentation_Protocol.md` a v1.1: Windsor pasa a ser fuente preferida de enriquecimiento L2/L3, sin convertir campos ausentes en ceros; la respuesta técnica con `id=null` queda excluida; y el reporte diario sigue siendo la fuente principal. No se publicaron, modificaron ni programaron contenidos; no se actualizó calendario, CNT, canon, afiliados ni el registro maestro estructural.

- **[2.75.00] — 2026-08-22 (Manus): Protocolo de instrumentación para HB-REEL-MOTION-POV-MEME-01.** La falta de views, reach y retención en Meta no cancela la celda ni permite escribir ceros. Se creó `Operations/Research/2026-08-22_Reels_Metric_Instrumentation_Protocol.md` con niveles `L0_Identidad`, `L1_Engagement_Observable`, `L2_Discovery`, `L3_Video_Retention` y `L4_Comparable_Cell`. El reporte diario es la base operativa; 24/72 horas quedan como cierre contractual opcional. Cada Reel nuevo debe conservar Page Post ID, Reel ID, permalink, hora real, hash del export, duración, fuente de métricas, tipo de ventana y estado de video. MPM-001, MPM-002 y MPM-003 se medirán primero en L1 y subirán a L2/L3 solo si Meta Business Suite o un conector validado entrega las métricas. Se actualizó el brief de la celda a v1.5 y `Reels_Confirmed_Metric_Assessment.json` a v1.3. No se modificaron calendario, CNT, canon, afiliados ni publicaciones.

- **[2.74.00] — 2026-08-21 (Manus): Desglose diario por familias, personajes, shares y comentarios.** Se creó `Operations/Research/2026-08-21_Analisis_Corte_Diario_Familias_Personajes.md`, junto con JSON y CSV. El corte de 12 publicaciones se clasificó de forma primaria y no canónica: `Relatable_Social` n=3 con 156 interacciones/52 shares; `Difusión_Minimal` n=3 con 148/33; `Ácido_Interpersonal` n=2 con 64/16; y familias de observación única para `Personaje_Marcador`, `Conversación_Relacional`, `Sequential_visual_reaction` y `Character_POV_reveal`. Universe aparece en seis piezas con 256 interacciones/67 shares, pero la señal también atraviesa Ganso y una pieza sin personaje identificado; no se atribuye causalidad al personaje. TAX-02 queda reforzada direccionalmente; HUM-06 queda compatible pero no universal; HUM-02 permanece exploratoria; `HB-REEL-MOTION-POV-MEME-01` no es evaluable por falta de views/reach/retención de video. La observación `OBS-DAILY-20260821-2200` del `ExperimentLog` fue ampliada con estos hallazgos. No se modificaron canon, calendario, publicación ni afiliados.

- **[2.73.00] — 2026-08-21 (Manus): Reportes diarios adoptados como fuente principal de aprendizaje.** Fernando aclaró que no estamos operando con ventanas exactas de 24 horas y que la información estratégica debe salir de los análisis diarios. Se actualizó `GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md` a v2.19, `GrowthOS/01_00_Arquitectura_Calendario_Escalable.md`, `GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md` y `GrowthOS/00_Índice.md`. El `ExperimentLog.csv` ahora contiene la observación `OBS-DAILY-20260821-2200` con `Corte_Diario`, 12 publicaciones, 495 interacciones observables y 132 shares. La ventana diaria permite aprender de rankings, formatos, personajes, horarios, shares, comentarios, captions y Reels usando acumulados observables etiquetados como `Corte_Observado`; no se presentan como delta diario. Las ventanas 24/72 horas quedan solo como capa opcional para cierres contractuales de celdas comparables. Afiliados permanece separado.

- **[2.72.00] — 2026-08-21 (Manus): Corte diario de métricas editoriales a las 22:00 local.** Se consultó Meta Graph API v26 con token de Página derivado de `/me/accounts` y se recuperaron 12 publicaciones reales entre el 20 de agosto a las 00:00 y el 21 de agosto a las 22:03 en `America/Matamoros`: 10 imágenes/posts y 2 Reels. Las imágenes acumularon 475 interacciones básicas y los Reels 20; el total editorial fue 495 interacciones. Los líderes fueron los assets `2607794` con 79, `2608038` con 78, `260635` con 63 y `2607838` con 57. Meta no expuso views, reach, retención ni tiempo medio de los Reels en esta extracción, por lo que no se concluye inferioridad del video. Afiliados se mantuvo en capa separada; el último snapshot disponible fue `MANUAL-20260820-7D-AFF07`, sin ventas visibles. Se creó `Operations/Research/2026-08-21_Corte_Diario_Metricas_2200.md`, su JSON estructurado, CSV operativo y copia raw. No se actualizó `ExperimentLog` porque este corte contiene acumulados lifetime, no snapshots exactos de 24/72 horas. No se modificó calendario ni se publicó contenido.

- **[2.71.00] — 2026-08-22 (Manus): Regla de almacenamiento operativo en Drive.** Fernando indicó que todas las imágenes y videos generados deben guardarse en sus carpetas correspondientes de My Drive. Para la celda `EXP-202608-REEL-MOTION-POV-MEME-001` se creó `My Drive/Universe sent me/USM/Reels/08 Agosto/EXP-202608-REEL-MOTION-POV-MEME-001` con ID `1NAyNNUnkNF5QGO7oYDgpw4b5poEPTuhX`. Se cargaron y verificaron las tres referencias oficiales `MPM-001_primary_reference_official_style_v2.png`, `MPM-002_primary_reference_official_style_v2.png`, `MPM-003_primary_reference_official_style_v2.png` y el video `MPM-001_motion_pov_v1.mp4`. El mapeo permanente quedó documentado en `Operations/Production/Generated_Reels/Motion_POV_Meme_001/reference_review_notes.md` v1.2 y en el brief v1.4. GitHub continúa siendo la fuente documental oficial; Drive conserva los binarios operativos. MPM-002 y MPM-003 siguen pendientes por límite diario de video. No se publicó ni se modificó el calendario.

- **[2.70.00] — 2026-08-22 (Manus): Corrección visual contra los elementos oficiales de My Drive.** Fernando indicó que las primeras referencias no coincidían con el estilo de animación ni con los personajes guardados en `My Drive/Universe sent me/USM/Elementos`. Se consultó la carpeta oficial `Elementos` y se descargaron las fuentes de verdad `Elara.jpeg`, `Wilfred.png`, `Fantasma_Reference_Sheet.jpeg`, `Universe_Reference_Sheet.jpeg` y `Bosque Ancestral 1.jpeg` desde `PERSONAJES` y `LUGARES`. Se rechazó y movió a `Rejected_References/` el primer set. Se regeneraron `MPM-001_primary_reference_official_style_v2.png`, `MPM-002_primary_reference_official_style_v2.png` y `MPM-003_primary_reference_official_style_v2.png` con linework oscuro, sombreado gráfico, proporciones 2D y diseños oficiales. La revisión confirma a Elara con sombrero café y cinta morada, cardigan, audífonos y cabello claro; a Wilfred como gnome de sombrero rojo, barba blanca y túnica verde; a Fantasma con sábana blanca, lentes redondos dorados, manos y botas; y a Universe como gato blanco con gafas grandes doradas ornamentadas. Se actualizó el brief a v1.3 y `reference_review_notes.md` a v1.1. No se ha generado video, creado CNT, modificado calendario ni publicado.

- **[2.69.00] — 2026-08-22 (Manus): Referencias primarias generadas y revisadas para Motion + POV/Meme.** Con la aprobación de Fernando, se generaron `MPM-001_primary_reference.png`, `MPM-002_primary_reference.png` y `MPM-003_primary_reference.png` en `Operations/Production/Generated_Reels/Motion_POV_Meme_001/`. MPM-001 cumple identidad de Elara/Wilfred, audífonos, bosque y ausencia de Evan; MPM-002 presenta a Fantasma y tres gatos en un invernadero nuevo, sin copiar el Reel histórico; MPM-003 fue refinado a `MPM-003_primary_reference_v2.png` porque la primera versión no mostraba las dos gafas redondas de Universe con suficiente claridad. El registro `reference_review_notes.md` conserva la revisión. El siguiente gate es aprobar visualmente las referencias y autorizar la generación de los tres clips; no se ha generado video, creado CNT, modificado calendario ni publicado.

- **[2.68.00] — 2026-08-22 (Manus): Paquete técnico de generación para la celda Motion + POV/Meme.** Tras la aprobación de Fernando de los tres conceptos y captions, se amplió `Operations/Production/2026-08-22_Brief_Celda_Reels_Motion_POV_Meme_001.md` a v1.1. El paquete fija los controles comunes —Facebook primario, 7–10 segundos, hook antes de 0.8 s, movimiento físico legible, comprensión sin audio, `Caption_Treatment=caption_minimo`, `Caption_Function=reforzar_remate`, sin afiliación— y añade prompts detallados para MPM-001 Elara/Wilfred Piscis, MPM-002 Fantasma/gatos y MPM-003 Universe/portal. El caso Piscis queda definido como Elara con audífonos ignorando a Wilfred detrás; el asset `Elara y Evan en el Bosque.mp4` no se usa y permanece pendiente de reasignación al Reel reciente de campamento. Los tres puntajes pasan la rúbrica: 9.00, 9.20 y 9.50/10. El siguiente gate es autorización para generar las referencias primarias; no se ha generado imagen/video, creado CNT, modificado calendario ni publicado.

- **[2.67.00] — 2026-08-22 (Manus): Corrección de identidad del caso Piscis y diseño de la celda Motion + POV/Meme.** Fernando confirmó que el Reel de Piscis muestra a Elara caminando con audífonos mientras Wilfred la sigue detrás y le habla sin que ella lo escuche; no participa Evan. También aclaró que `Elara y Evan en el Bosque.mp4` pertenece a otro Reel más reciente de Elara y Evan juntos en el bosque/campamento. Se retiró esa asociación del concepto `CON-2026-08-09-Elara_Evan_Estrellas` y el asset quedó en `Pending_reassignment_after_human_correction`; el concepto cross-platform conserva sus IDs y copy. Se creó `Operations/Production/2026-08-22_Brief_Celda_Reels_Motion_POV_Meme_001.md` en `Review` con tres casos controlados: Elara/Wilfred Piscis, Fantasma con gatos y Universe con hábito digital. Los tres comparten `EXP-202608-REEL-MOTION-POV-MEME-001` y `HB-REEL-MOTION-POV-MEME-01`, con n≥3 para señal preliminar y n=5 para decisión operativa. Se actualizaron el historial v2.2, inventario de assets v1.6, inventario de publicaciones, auditoría v1.14, evaluación estructurada v1.2, registro maestro v3.4 y fuente maestra v2.18. No se generó video, no se creó CNT, no se modificó calendario y no se publicó nada. Los tres casos requieren aprobación humana.

- **[2.66.00] — 2026-08-22 (Manus): Corrección estratégica de la prioridad de Reels.** Fernando reportó que los Reels tipo podcast/radio no estaban llamando la atención, mientras que el Reel de Elara caminando en el bosque con Wilfred siguiéndola y texto `POV: Eres Piscis`, y `Fantasma caminando con gatos` —meme animado con movimiento visible y texto conservado— tuvieron mayor impacto. La evidencia documentada de Fantasma incluye snapshots históricos separados de 6,640 y 6,878 views; no se promedian. La prioridad cambia a la celda candidata `HB-REEL-MOTION-POV-MEME-01`, con mínimo n=3 para señal y n=5 para decisión operativa. `Dialogue_radio` queda como observación secundaria y el brief `Operations/Production/2026-08-22_Brief_Reel_Dialogue_Radio_003.md` pasa a `Archived`; no se genera, programa ni publica esa pieza. Se actualizaron `GrowthOS/07_00_Registro_Maestro_Reels.md` v3.3, `GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md` v2.17, `Operations/Research/2026-08-19_Auditoria_Reels_y_Monetizacion.md` v1.13 y `Operations/Research/2026-08-22_Reels_Confirmed_Metric_Assessment.json` v1.1. El Reel de Piscis queda pendiente de ID nativo y reconciliación de asset; no se confunde con `Elara y Evan en el Bosque.mp4`.

- **[2.65.00] — 2026-08-22 (Manus): Brief Draft para el tercer Reel Dialogue_radio.** Se creó `Operations/Production/2026-08-22_Brief_Reel_Dialogue_Radio_003.md` con la propuesta `Afirmación → mala interpretación → corrección seca → reacción`, protagonizada por Elara y Wilfred. El brief mantiene separados `Caption_Treatment`, `Caption_Function`, subtítulos, audio, duración, watermark, reuse y afiliación. Propone `HB-REEL-DIALOGUE-01` como hipótesis provisional, pero no la registra como aprendizaje validado. No autoriza generación, CNT, programación ni publicación; cualquier acción operativa requiere aprobación humana separada.

- **[2.64.00] — 2026-08-22 (Manus): Clasificación operativa de los seis Reels con asset confirmado.** Se creó `Operations/Research/2026-08-22_Reels_Confirmed_Classification.csv` y su evaluación `Operations/Research/2026-08-22_Reels_Confirmed_Metric_Assessment.json`. Los seis casos se agruparon en `Character_loop_meme`, `Sequential_visual_reaction`, `Dialogue_radio` y `Character_POV_reveal`. `Dialogue_radio` cuenta con dos assets fuente distintos y 9/10 interacciones en snapshots actuales de Meta; es la primera candidata para crear un tercer caso, pero todavía no es un veredicto. `Character_loop_meme` reutiliza el mismo asset de Fantasma y no debe tratarse como dos casos independientes. `Sequential_visual_reaction` y `Character_POV_reveal` son observaciones aisladas. Los seis registros carecen de views/reach en el corte actual y mezclan métricas lifetime con snapshot actual; no se actualizó `ExperimentLog` ni se declaró una familia ganadora.

- **[2.63.00] — 2026-08-22 (Manus): Revisión visual del lote TIER2A e integración de dos matches exactos.** Se revisaron diez Reels Tier 2 y sus candidatos principales de Drive. `2159954351459805` coincide exactamente con `Wilfred_and_Elara_cosmic_radio_202606272110.mp4`; `1339119487723234` coincide exactamente con `Elara_and_Wilfred_dialogue_anima…_202606271715.mp4`. Las comparaciones confirmaron la misma cabina de radio, ventana cósmica, consola, iluminación y composición de personajes; los Reels agregan diálogo, audio o texto de publicación. Los otros ocho quedaron como `No_Match_In_TIER2A_Primary`, sin exclusión global del inventario. La cola pendiente fue regenerada para excluir estos matches y queda en 48 casos. El historial queda en v2.1, el registro maestro en v3.0, la auditoría en v1.11, la fuente maestra en v2.14 y la cobertura en v1.5; hay seis matches exactos Drive↔Meta.

- **[2.62.00] — 2026-08-21 (Manus): Revisión visual del bloque NEXT10 e integración de un cuarto match exacto.** Se revisaron los diez candidatos Tier 1 siguientes a la cola TOP5. El Reel `1518053389684402` coincide exactamente con `Fantasma_tranquilo_con_viento_202605241629.mp4` — mismo Fantasma con lentes, cerca, bosque azul/morado, composición y movimiento — y fue integrado al historial sin crear CNT. Los nueve restantes quedaron sin match dentro de su candidato primario. La comparación directa descartó `Wilfred realista haciendo una posion.mp4` como fuente del Reel `1906363553379974`: comparten personaje/estilo, pero no escena ni secuencia. También se descartó `Universe sent me - 022.png` como fuente del Reel `991640670312120`: comparten atmósfera de catedral, pero no composición ni texto. El historial queda en v2.0, el registro maestro en v2.9, la auditoría en v1.10, la fuente maestra en v2.13 y la cobertura en v1.4; hay cuatro matches exactos y 50 casos históricos aún pendientes de asset.

- **[2.61.00] — 2026-08-21 (Manus): Priorización y revisión visual del lote pendiente de assets.** Se corrigieron los estados de los tres matches exactos para excluirlos de la cola pendiente. Se creó `Operations/Research/2026-08-22_Reels_Pending_Asset_Reconciliation_Queue.csv` con 51 casos pendientes, ordenados por interacción y divididos en Tier 1 (15) y Tier 2 (36). El rastreo recursivo de Drive encontró 202 archivos de imagen/video. Se generó el triage `2026-08-22_Reels_Pending_Drive_Triage.csv` y se revisaron visualmente los cinco Reels pendientes con mayor interacción — 25 candidatos de Drive en total — sin match dentro del lote TOP5: arroyo/raíces, carretera nocturna con luna, cielo con `DESAPENDEJATE`, cielo con frase social y fondo circular de colores. Los cinco permanecen pendientes globales; `No_Match_In_Reviewed_Set` no significa exclusión total de Drive. Se actualizan historial v1.9, registro maestro v2.8, auditoría v1.9, fuente maestra v2.12 y cobertura v1.3. No se asignaron CNT, Concept_ID ni hipótesis.

- **[2.60.00] — 2026-08-21 (Manus): Integración completa de candidatos históricos de video de Meta.** Las 54 publicaciones con attachment `video` recuperadas del feed de Meta para mayo/junio quedaron representadas en el historial estructurado y en la lista CSV como identidad de publicación: 23 de mayo y 31 de junio. Los registros nuevos no reciben `Concept_ID`, CNT, asset de Drive, crosspost o hipótesis por inferencia; conservan `Asset_Match_Status=Pending_Drive_or_local_asset_match`. Los tres matches visuales exactos ya confirmados permanecen vinculados a sus assets de Drive y el caso de Wilfred continúa pendiente después de controles negativos. El inventario histórico asciende a 102 registros por plataforma — Facebook 73, Instagram 16, TikTok 7 y YouTube 6 — y los documentos quedan actualizados: historial v1.7, registro maestro v2.7, auditoría v1.8, fuente maestra v2.11 y cobertura v1.2. No se actualizaron `ExperimentLog` ni se declararon aprendizajes comparables; las métricas siguen separadas por plataforma y ventana.

- **[2.59.00] — 2026-08-21 (Manus): Extensión histórica de Reels a mayo y junio.** Meta devolvió 438 publicaciones de Página entre mayo y junio y 54 candidatos con attachment de video — 23 de mayo y 31 de junio. La carpeta raíz de Reels en Drive contenía cinco videos creados antes de julio; la revisión visual directa confirmó tres matches exactos: `Fantasma_tranquilo_con_viento_202605241629.mp4` → Reel `1877535942934184`; el asset set de los dos clips `Man_*_20260613` → Reel `2417378928740605`; y `Pato_villano_mirando_cámara_POV_EresAries.mp4` → Reel `1049041731412120`. `Wilfred realista haciendo una posion.mp4` queda `Pending_Visual_Review` después de dos controles negativos. El historial pasa a 51 registros por plataforma — Facebook 22, Instagram 16, TikTok 7 y YouTube 6 — y se crea `Operations/Research/2026-08-21_Reels_Drive_Meta_Crossmatch_Review.csv`. Se actualizan el registro maestro v2.6, la auditoría v1.7, la fuente maestra v2.10 y los resúmenes de cobertura. Los matches se integran como identidad histórica, no como experimentos comparables ni como veredictos de rendimiento.

- **[2.58.00] — 2026-08-21 (Manus): Auditoría del inventario y operación de Reels.** Se reconstruyó y sincronizó la lista histórica de video corto: 48 registros por plataforma — Facebook 19, Instagram 16, TikTok 7 y YouTube 6 — correspondientes a 21 conceptos y 17 grupos cross-platform. Se añadieron al historial los Reels recientes `Doble Check → Universe` (`2210896633022235`), `Remote Control` (`2815726225473165`) y `Universe viéndote Farmear Aura` (`2005557463434064`). El Reel de Farmear Aura fue verificado como publicado el 21 de agosto, mientras que la consulta de 47 posts programados devolvió únicamente imágenes y ningún Reel/video pendiente. Maeve permanece como dirección de producción `Crave You — Maeve entre todas las miradas` en `REVIEW`, sin export ni ID nativo confirmado. Se creó `Operations/Research/2026-08-21_Reels_Publication_Inventory.csv`, se actualizaron `GrowthOS/07_00_Registro_Maestro_Reels.md` v2.6, `Operations/Research/2026-08-19_Auditoria_Reels_y_Monetizacion.md` v1.6 y `GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md` v2.9. Las métricas de Reels siguen separadas de imágenes, afiliados y P0; no se cerró ningún veredicto ni se inventaron snapshots.

- **[2.57.00] — 2026-08-21 (Manus): Se documenta el puente de aprendizaje Facebook → Reels.** Los experimentos comparables de imágenes alimentarán Reels únicamente como `Design_Input`/hipótesis editorial, nunca como métricas o veredictos de video. Se definieron tres traducciones futuras: `FUT-TRANS-003` hacia transformación real → Universe, `FUT-MICRO-005/006` hacia microhistoria audiovisual y `FUT-ACID-003` hacia diálogo ácido breve. Cada Reel requiere `Concept_ID`, `Experiment_ID`, `Hypothesis_ID`, `hook_0_3s`, duración, estructura narrativa, tratamiento/función de caption, IDs nativos y snapshots 24/72h. Las plataformas permanecen separadas, la afiliación conserva su ledger propio y la reutilización de memes respeta la antigüedad mínima de 30 días. No se programó una nueva ola de Reels ni se actualizaron métricas de video. Documento: `Operations/Research/2026-08-19_Auditoria_Reels_y_Monetizacion.md`.

- **[2.56.00] — 2026-08-21 (Manus): Tres experimentos comparables programados y verificados en Facebook.** Bajo autorización explícita de Fernando, se cancelaron y verificaron como eliminadas las tres programaciones anteriores. Después se cargaron los PNG v3 y se crearon tres posts futuros con `is_published=false` y `scheduled_publish_time` confirmado: `FUT-MICRO-006/HB-007` → `2026-08-24 10:00`, Post `1036844829507460_122154023721072582`, Photo `122154023691072582`; `FUT-MICRO-005/HB-006` → `2026-08-24 13:30`, Post `1036844829507460_122154023781072582`, Photo `122154023757072582`; `FUT-ACID-003/HB-009` → `2026-08-27 16:00`, Post `1036844829507460_122154023841072582`, Photo `122154023817072582`. `Publication_Log` y el staging fueron actualizados; no se agregaron métricas 24/72h. Instagram, CNT, reuse y afiliados permanecen excluidos.

- **[2.55.00] — 2026-08-21 (Manus): Reemplazos de calendario aprobados y aplicados al CSV maestro.** Fernando aprobó los tres cambios: `2026-08-24 10:00` → `FUT-MICRO-006/HB-007`, `2026-08-24 13:30` → `FUT-MICRO-005/HB-006` y `2026-08-27 16:00` → `FUT-ACID-003/HB-009`. Las tres filas fueron actualizadas con `Aprobado_Sustitucion_Pendiente_Meta`; el staging registra `Meta_Action=Not_Executed`, `CNT_Status=Not_Created`, `Affiliate_Attachment=No` e Instagram separado. El siguiente gate es confirmar captions finales y solicitar autorización explícita para cancelar las tres programaciones existentes y programar/publicar en Facebook. No se modificó `Publication_Log`, `ExperimentLog`, CNT, reuse, afiliados, Instagram ni Meta.

- **[2.54.00] — 2026-08-21 (Manus): Propuesta de sustitución de slots para los tres experimentos comparables.** Se creó `Operations/Research/2026-08-21_Propuesta_Calendario_Experimentos_Comparables.md` usando el calendario 17–30 como base, sin crear programación paralela. La propuesta sugiere sustituir `2026-08-24 13:30` por `FUT-MICRO-005`, `2026-08-24 10:00` por `FUT-MICRO-006` y `2026-08-27 16:00` por `FUT-ACID-003`. Estado `Review`: requiere aprobación humana de los tres reemplazos antes de modificar el calendario, programar en Meta o publicar. No se modificó calendario, `Publication_Log`, `ExperimentLog`, CNT, reuse, afiliados ni Instagram.

- **[2.53.00] — 2026-08-21 (Manus): Selección humana de las tres variantes v3.** Fernando seleccionó `FUT-MICRO-005`, `FUT-MICRO-006` y `FUT-ACID-003` v3 como las versiones elegidas para la prueba, reemplazando a las v2 en el registro de variantes. Los originales y v2 se conservan como historial; no se actualiza `ExperimentLog` porque todavía no hay calendario ni publicación. `Calendar_Status=Not_Scheduled`, `CNT_Status=Not_Created` y `Publication_Status=Not_Published` permanecen activos. No se modificó reuse, afiliados ni plataformas sociales.

- **[2.52.00] — 2026-08-21 (Manus): Tercera iteración aprobada con tríptico oficial de Evan.** Fernando aprobó regenerar `FUT-MICRO-005`, `FUT-MICRO-006` y `FUT-ACID-003` usando `Operations/Production/Character_References/Evan/Evan_full_body_triptych_20260730.jpeg` como referencia principal. Las v3 conservan texto y composición experimental, y mejoran cabello despeinado, cejas marcadas, rostro cansado, expresión ensimismada y hoodie café/taupe. Resultado preliminar: `Pass_visual_v3_preliminar` para los tres. Ledger: `Operations/Production/2026-08-21_Comparable_Identity_V3_Proposals.csv`; prompts: `Operations/Production/2026-08-21_Prompts_Assets_Comparables_v3.md`. Quedan pendientes de selección humana entre original, v2 y v3; no se modificó calendario, CNT, reuse, afiliados, `ExperimentLog` ni publicación.

- **[2.51.00] — 2026-08-21 (Manus): Revisión de referencia ampliada de Evan.** Fernando añadió referencias directas de Evan (`Operations/Production/Character_References/Evan/2608062_Kiri_Evan.jpg` y `Operations/Production/Character_References/Evan/2608052_Evan.jpg`). La comparación confirma que sus anclas incluyen cabello oscuro despeinado, rostro juvenil/cansado, cejas marcadas, paleta marrón/taupe, actitud ensimismada y suéter café. Las tres variantes v2 preservan vestuario y composición, pero alcanzan únicamente `Identity_Partial`: Evan aparece más joven y expresivo que en la referencia. Las tres pasan a `Proposal_Review_Identity_Partial`; no reemplazan los originales. Si se busca fidelidad alta, se recomienda una tercera iteración con la referencia ampliada. No se modificó calendario, CNT, reuse, afiliados, `ExperimentLog` ni publicación.

- **[2.50.00] — 2026-08-21 (Manus): Segunda propuesta de identidad para tres assets comparables.** A solicitud de Fernando, se generaron variantes v2 de `FUT-MICRO-005` y `FUT-MICRO-006` con Elara y Evan, preservando el sombrero puntiagudo de Elara, el cabello claro, el suéter café de Evan, la composición de tres paneles y el texto original. `FUT-ACID-003` v2 usa Universe con sus lentes redondos y Evan con su suéter café, preservando el diálogo y el remate. Las tres variantes pasan `Pass_visual_propuesta_v2` y quedan como `Proposal_Not_Selected`; no reemplazan los originales automáticamente. Registro: `Operations/Production/2026-08-21_Comparable_Identity_V2_Proposals.csv`; control: `Operations/Production/2026-08-21_Control_Visual_Assets_Comparables.md`. No se modificó calendario, CNT, reuse, afiliados, `ExperimentLog` ni publicación.

- **[2.49.00] — 2026-08-21 (Manus): Generación y control visual preliminar de los cuatro assets comparables.** Se generó un PNG nuevo para cada brief en `Operations/Production/Generated_Comparable_Assets/`. `FUT-MICRO-005`, `FUT-MICRO-006` y `FUT-ACID-003` pasaron control visual preliminar; `FUT-TRANS-003` pasó con identidad consistente tras comparar el mismo gato y gafas con la referencia compartida. Ledger: `Operations/Production/2026-08-21_Generated_Comparable_Assets.csv`; control: `Operations/Production/2026-08-21_Control_Visual_Assets_Comparables.md`; prompts: `Operations/Production/2026-08-21_Prompts_Assets_Comparables.md`. No se modificó calendario, CNT, reuse, afiliados, `ExperimentLog` ni publicación. Requiere decisión humana posterior para cualquier uso operativo.

- **[2.48.00] — 2026-08-21 (Manus): Aprobación humana para generar los cuatro assets comparables.** Fernando aprobó `FUT-MICRO-005`, `FUT-MICRO-006`, `FUT-TRANS-003` y `FUT-ACID-003` para `Approved_Generation_Only` el 2026-08-21. La matriz queda validada `4/4` por `Operations/Production/validate_generation_authorization_matrix.py`; `Calendar_Change=No`, `CNT_Creation=No`, `Publication=No` y `Affiliate_Attachment=No`. La autorización permite producir un asset nuevo por brief y ejecutar control visual posterior, pero no autoriza calendario, reuse, afiliados, CNT ni publicación. Scripts: `Operations/Production/approve_generation_briefs.py` y `Operations/Production/validate_generation_authorization_matrix.py`. Assets todavía no generados.

- **[2.47.00] — 2026-08-21 (Manus): Paquete de revisión humana para autorización exclusiva de generación.** Se creó `Operations/Research/2026-08-21_Autorizacion_Generacion_Briefs_Comparables.csv` con cuatro solicitudes `Approve_Generation_Only`, una por brief, todas en `Decision=Pending` y `Generation_Authorization=Pending_Human_Approval`. Los bloqueos `Calendar_Change=No`, `CNT_Creation=No`, `Publication=No` y `Affiliate_Attachment=No` quedaron validados por `Operations/Production/validate_generation_authorization_matrix.py` con `4/4 PASS`. El paquete narrativo actualizado es `Operations/Research/2026-08-21_Paquete_Revision_Humana_Briefs_Comparables.md`. No se generaron assets, no se modificó el calendario y no se actualizó `ExperimentLog`.

- **[2.46.00] — 2026-08-21 (Manus): Registro formal de hipótesis comparables en el HypothesisBank.** Se sustituyeron los IDs provisionales `H-COMP-*` por `HB-006` (`FUT-MICRO-005`), `HB-007` (`FUT-MICRO-006`), `HB-008` (`FUT-TRANS-003`) y `HB-009` (`FUT-ACID-003`) en `GrowthOS/Integracion_Growth_OS.md` y en la matriz `Operations/Research/2026-08-21_Briefs_Comparables_Revision_Humana.csv`. La validación cruzada queda en `4/4 PASS` y `0` colisiones directas. La simulación de solapamientos se mantiene vigente: no combinar celdas con familias Wave 1 y conservar hora/caption como covariables. El registro formal no autoriza generación, calendario, CNT ni publicación; `ExperimentLog` permanece sin nuevas observaciones porque no hay assets ni outcomes.

- **[2.45.00] — 2026-08-21 (Manus): Simulación de impacto de solapamientos semánticos.** La simulación usó outcomes históricos de las celdas comparables y escenarios de doble asignación. Una familia Wave 1 de `n=3` pasaría artificialmente a `n=4` (`+33.33%` de denominador) y el caso duplicado representaría `25.00%` de la muestra contaminada. Bajo escenario máximo, la media simulada se mueve hasta `+11.72%` en interacciones y `+12.50%` en shares para `TRANS-UNIVERSE`; en `ACID-DIALOGUE`, hasta `+2.21%` y `+6.53%`. La mediana no cambió en los escenarios modelados, pero no se declara inmune con muestras pequeñas. Regla operativa: mantener cada brief en su `Cell_ID`, no combinarlo con FAM-02/FAM-03/FAM-04/FAM-05 y tratar hora/caption como covariables compartidas. Reporte: `Operations/Research/2026-08-21_Simulacion_Impacto_Solapamientos_Comparables.md`; datos: `Operations/Research/2026-08-21_Simulacion_Impacto_Solapamientos_Comparables.csv`. No se generaron assets ni se autorizó calendario o publicación.

- **[2.44.00] — 2026-08-21 (Manus): Validación cruzada de hipótesis comparables contra experimentos previos.** Se cruzaron los cuatro briefs contra `ExperimentLog`, la matriz `Wave_1_Signal_Experiment_Design.csv` y el `HypothesisBank` documentado. Resultado: `0` colisiones directas de `Experiment_ID` o `Hypothesis_ID`; los cuatro quedan en `PASS_WITH_WARNINGS` porque `H-COMP-*` aún no está registrado en el `HypothesisBank` local y no cumple la convención formal `HB-###`. Se documentaron solapamientos controlables: `FUT-ACID-003` con FAM-04, `FUT-TRANS-003` con FAM-05/HB-002 y las microhistorias con FAM-02/FAM-03. No se deben combinar denominadores automáticamente. Reporte: `Operations/Research/2026-08-21_Validacion_Cruzada_Hipotesis_Briefs_Comparables.md`; validador: `Operations/Production/validate_comparable_hypothesis_conflicts.py`. No se generaron assets, no se actualizó `ExperimentLog` y no se autorizó calendario ni publicación.

- **[2.43.00] — 2026-08-21 (Manus): Metadatos obligatorios de briefs comparables completados como propuesta.** Se añadieron a `Operations/Research/2026-08-21_Briefs_Comparables_Revision_Humana.csv` los campos `Experiment_ID`, `Hypothesis_ID`, `Caption_Function`, `Humor_Function`, `Hora_Test`, `Hora_Test_TZ`, `Theme_Confound`, `Reuse_Status`, `Metadata_Status`, `Generation_Authorization` y `Metadata_Notes`. Los cuatro briefs comparten `EXP-2026-08-COMP-GAPS-01`, tienen hipótesis individuales `H-COMP-*`, horas propuestas en `America/Matamoros`, `Reuse_Status=New_Asset_Proposed`, `Metadata_Status=Complete_Proposed_Not_Authorized` y `Generation_Authorization=Pending_Human_Approval`. `Caption_Treatment` permanece separado de `Caption_Function`. No se actualizó `ExperimentLog`, no se generaron assets y no se autorizó calendario, publicación ni CNT. Scripts: `Operations/Production/populate_comparable_brief_metadata.py` y `Operations/Production/run_comparable_briefs_preflight.py`.

- **[2.42.00] — 2026-08-21 (Manus): Preflight técnico de briefs comparables completado.** El ejecutor `Operations/Production/run_comparable_briefs_preflight.py` validó `4/4` especificaciones en `PASS` para `FUT-MICRO-005`, `FUT-MICRO-006`, `FUT-TRANS-003` y `FUT-ACID-003`. El resultado `preflight_specification_pass` no equivale a `generation_approved`: no existen assets generados, siguen pendientes los metadatos `Experiment_ID`, `Hypothesis_ID`, `Caption_Function`, `Hora_Test` y demás campos previos a generación, y la promoción permanece bloqueada hasta una aprobación humana separada. Reporte: `Operations/Production/2026-08-21_Preflight_Briefs_Comparables.md`.

- **[2.41.00] — 2026-08-21 (Manus): Aprobación de cuatro briefs para preflight y estado de celdas comparables.** Fernando aprobó `FUT-MICRO-005`, `FUT-MICRO-006`, `FUT-TRANS-003` y `FUT-ACID-003` con `Status=Approved_for_Preflight` y `Requested_Decision=Approve_Preflight_Only`. La aprobación no autoriza generación final, calendario, publicación ni CNT. Estado actual: `MICRO-STRICT-3P n=1` y requiere dos piezas nuevas de tres paneles; `TRANS-UNIVERSE n=2` y requiere una transformación de Universe con gafas preservadas; `ACID-DIALOGUE n=2` y requiere un diálogo ácido nuevo; `MICRO-SEQ-2P`, observacional y autodesprecio/antihéroe están en `n=3` preliminar y requieren dos casos adicionales para `n=5`. Documento actualizado: `Operations/Production/2026-08-21_Diseno_Casos_Comparables_Brechas.md`.

- **[2.40.00] — 2026-08-21 (Manus): Implicaciones estratégicas de captions y siguiente paso analítico.** La revisión histórica de captions queda cerrada: no se abrirá otra ronda de clasificación de junio. El siguiente paso es obtener la decisión humana sobre `FUT-MICRO-005`, `FUT-MICRO-006`, `FUT-TRANS-003` y `FUT-ACID-003`; si se aprueban, pasarán a preflight, no directamente a publicación. Se añade la regla de separar `Caption_Treatment` de `Caption_Function`, distinguir pregunta retórica de conversación real, usar controles visuales comparables, rotar horarios y elegir métricas primarias por hipótesis. No se actualiza el ExperimentLog con las etiquetas históricas.

- **[2.39.00] — 2026-08-21 (Manus): Cierre manual de los 13 captions pendientes e impacto de reclasificaciones.** Se completó la revisión manual de los 17 casos aprobados. El corte final queda en 8 `caption_minimo`, 2 `caption_conversacional`, 6 `caption_refuerzo` y 1 `historical_unavailable`; 12 confianzas altas y 5 medias. Se reclasificaron cuatro casos conversacionales a refuerzo y se confirmaron mínimos/conversacionales según el contexto visual; no se modificó el ExperimentLog. El cambio de Ganso mueve 14 interacciones, 2 shares y 3 comentarios de `caption_refuerzo` a `caption_minimo`; Universe conserva `caption_refuerzo`. El total permanece en 300 interacciones, 53 shares y 13 comentarios. Documentos: `Operations/Research/2026-08-21_Junio_Caption_Reclassification_Impact.md` y `Operations/Research/2026-08-21_Junio_Approved_Character_Caption_Manual_Findings.md`.

- **[2.38.00] — 2026-08-21 (Manus): Revisión manual parcial de captions históricos.** Se revisaron cuatro de los 17 captions ambiguos. El caso Ganso `1036844829507460_122134608507072582` se reclasificó de `caption_refuerzo` a `caption_minimo` porque repite el texto visual y añade hashtags. Universe `1036844829507460_122130196011072582` y Wilfred `1036844829507460_122130309663072582` conservan `caption_refuerzo` con confianza media; Fantasma `1036844829507460_122125895013072582` queda como `historical_unavailable` porque Meta no devolvió mensaje. El corte queda en 8 mínimos, 6 conversacionales, 2 de refuerzo y 1 no disponible; 13 permanecen pendientes. No se actualiza el ExperimentLog ni se declara causalidad. Documento de hallazgos: `Operations/Research/2026-08-21_Junio_Approved_Character_Caption_Manual_Findings.md`.

- **[2.37.00] — 2026-08-21 (Manus): Auditoría histórica de captions de los 17 casos aprobados.** Meta devolvió el texto exacto para 16 de los 17 casos; uno usa fallback de la cola. La propuesta rule-based distribuye los casos en 7 `caption_minimo`, 6 `caption_conversacional`, 3 `caption_refuerzo` y 1 `historical_unavailable`. Los tres casos de `caption_refuerzo` y el caso sin mensaje quedan como prioridad de revisión manual. Todos permanecen con `manual_review_status=Pending_Manual_Caption_Review`; no se actualiza el ExperimentLog ni se atribuye efecto causal. Documentos: `Operations/Research/2026-08-21_Junio_Approved_Character_Caption_Audit.csv` y `Operations/Research/2026-08-21_Junio_Approved_Character_Caption_Analysis.md`.

- **[2.36.00] — 2026-08-21 (Manus): Paquete de revisión humana de cuatro briefs comparables.** Se prepararon `FUT-MICRO-005`, `FUT-MICRO-006`, `FUT-TRANS-003` y `FUT-ACID-003` con hipótesis, estructura visual, tratamiento de caption, confusores, criterios de inclusión/exclusión, preflight y salvaguardas. Todos quedan como `Pending_Fernando_Review`. Se añadió el paquete `Operations/Research/2026-08-21_Paquete_Revision_Humana_Briefs_Comparables.md` y la matriz `Operations/Research/2026-08-21_Briefs_Comparables_Revision_Humana.csv`. La aprobación de un brief solo autoriza desarrollo/preflight; no autoriza generar assets, modificar calendario, publicar ni crear CNT.

- **[2.35.00] — 2026-08-21 (Manus): Corte cuantitativo de personajes y resolución del candidato de cuatro paneles.** Los 17 casos aprobados suman 300 interacciones, 53 shares y 13 comentarios; el caso Universe `1036844829507460_122130196011072582` concentra 54.7% de las interacciones y 79.2% de los shares del subconjunto. Sin ese outlier, la mediana baja a 8 interacciones y 0.5 shares. No se infiere efecto causal ni ranking de personajes. El candidato `1036844829507460_122127951885072582` queda con `validation_status=Excluded_3P_Retain_4P_Candidate`: cuatro paneles confirmados, fuera de `MICRO-STRICT-3P`, retenido solo para una futura `MICRO-SEQ-4P` que no se abrirá sin tres casos comparables y definición aprobada. Documentos: `Operations/Research/2026-08-21_Junio_57_Approved_Character_Analysis.md`, `Operations/Research/2026-08-21_Junio_57_Approved_Character_Analysis.json` y `Operations/Production/2026-08-21_Diseno_Casos_Comparables_Brechas.md`. No se modifican CNT, canon, calendario ni publicaciones.

- **[2.34.00] — 2026-08-21 (Manus): Aprobación de los 17 casos de personaje y validación del candidato de microhistoria.** Fernando aprobó incorporar 17 casos visuales de junio a la capa de análisis selectivo, con alcance limitado a presencia visual, rol narrativo, potencial de etiquetado y relación con celdas. No se autorizaron CNT, canon, reuse, calendario ni publicación. El candidato `1036844829507460_122127951885072582` fue validado como microhistoria de cuatro paneles con turnos, continuidad y remate, pero queda fuera de `MICRO-STRICT-3P` porque esa celda exige exactamente tres paneles. Se conserva como `Pending_Cell_Validation` para una eventual subcelda `MICRO-SEQ-4P`, que no se abrirá sin al menos tres casos comparables y una definición aprobada. Documentos: `Operations/Research/2026-08-21_Junio_57_Unmatched_Visual_Findings.md`, `Operations/Research/2026-08-21_Junio_57_Unmatched_Character_Utility.csv` y `Operations/Production/2026-08-21_Diseno_Casos_Comparables_Brechas.md`.

- **[2.33.00] — 2026-08-21 (Manus): Revisión visual de los 57 posts de junio sin match y diseño de celdas comparables pendientes.** La cola de 57 casos se clasificó como 36 controles de formato, 19 candidatos visuales de personaje, un candidato de microhistoria estricta (`1036844829507460_122127951885072582`) y un caso sin `full_picture`. Se seleccionaron 17 casos de personaje para análisis sin crear CNT; dos quedaron como reserva. Los gatos con gafas, gnomos, Ganso, Fantasma, Silvio y el roster mixto se mantienen como hipótesis visuales, nunca como canon automático. Se diseñaron `FUT-MICRO-005`, `FUT-MICRO-006`, `FUT-TRANS-003` y `FUT-ACID-003` para completar las celdas que siguen bajo `n=3`; son briefs condicionales sin aprobación de publicación. Documentos: `Operations/Research/2026-08-21_Junio_57_Unmatched_Visual_Findings.md`, `Operations/Research/2026-08-21_Junio_57_Unmatched_Character_Utility.csv` y `Operations/Production/2026-08-21_Diseno_Casos_Comparables_Brechas.md`. No se modifican calendario, CNT, canon ni métricas operativas de agosto.

- **[2.32.00] — 2026-08-21 (Manus): Ampliación histórica individual de julio y cierre selectivo de reservas de junio.** El lote 01 de julio seleccionó la unión de los 12 posts con más shares y los 12 con más comentarios, excluyendo los seis top ya integrados. De 17 candidatos, 16 obtuvieron match visual Meta→Drive y se integraron al ledger individual sin crear CNT; julio queda con 22 publicaciones individuales de 207 y un caso borderline fuera. La taxonomía visual revisada confirma que `Universe - Existencial` no equivale automáticamente a personaje Universe. Meta devolvió 284 comentarios de las 16 filas nuevas; se conserva la evidencia, pero no se analizarán manualmente todos los hilos. El cruce horario queda como control descriptivo, no como causalidad. La subcelda de microhistoria de dos paneles llega a `n=3` y autodesprecio/antihéroe llega a `n=3` con sensibilidad; transformación de Universe queda en `n=2`, diálogo ácido en `n=2` y microhistoria estricta de tres paneles en `n=1`. En junio se revisaron los tres primeros `Needs_Asset_Match`: solo `122129404893072582` coincidió con `Asset_Ref=260746`; la cola abierta baja de 58 a 57 y se congela. Documentos: `Operations/Research/2026-08-21_Julio_Expansion_Lote01_Analysis.md`, `Operations/Research/2026-08-21_Julio_Expansion_Lote01_Visual_Findings.md`, `Operations/Research/2026-08-21_Julio_Expansion_Lote01_Comments_Analysis.md`, `Operations/Research/2026-08-21_Expansion_Celdas_Comparables_Post_Julio_Lote01.json`, `Operations/Research/2026-08-21_Junio_Priority_Queue_Visual_Findings.md` y `Operations/Research/2026-08-17_Reporte_Final_Recopilacion_Junio.md` v1.3. No se modifican calendario, CNT, canon ni métricas operativas de agosto.

- **[2.31.00] — 2026-08-21 (Manus): Auditoría de cobertura histórica de junio y julio.** La base comparable queda cerrada a nivel agregado: 230 publicaciones de junio y 207 de julio. Junio mantiene 172 relaciones publicación→asset confirmadas, con 17 registros sin `Asset_Ref` utilizable y 58 casos sin match como reserva; no se reabre la reconciliación masiva. Julio mantiene solo seis publicaciones reconciliadas individualmente de 207, por lo que la ampliación de mayor valor es un lote pequeño ordenado por shares, comentarios y potencial para completar celdas comparables. Las celdas siguen en microhistoria estricta `n=1`, transformación `n=2`, observacional `n=3` preliminar, diálogo ácido `n=2` y autodesprecio/antihéroe `n=2`; los captions históricos no permiten atribución causal suficiente. Se actualizó `Operations/Research/2026-08-20_Sintesis_Historica_Crecimiento_Junio_Julio.md` a v1.1. No se modifican calendario, CNT, canon ni métricas operativas de agosto.

- **[2.30.00] — 2026-08-18 (Manus): Cierre de la creación de etiquetas granulares del piloto afiliado.** Se completaron las diez etiquetas, una por oportunidad/publicación, para AFF-01–AFF-10: `usmfb2606440818`, `usmfb2605600819`, `usmfb2606590820`, `usmfb2606350821`, `usmfb2605100822`, `usmfb2605180824`, `usmfb2605400826`, `usmfb2605900828`, `usmfb7410829` y `usmfb2605280830`. AFF-01 conserva el único link afiliado generado hasta ahora (`https://meli.la/2zCoRix`); los otros nueve links, la selección final de productos y la adjunción nativa en Facebook siguen pendientes. No se publicó ni modificó ninguna publicación. Documentos: `Operations/Research/Affiliate_Pilot_Assignments.csv`, `Operations/Research/Affiliate_Link_Ledger.csv` y `Operations/Research/2026-08-19_Candidatas_Afiliacion_Facebook_18_30_Observacion.md`.

- **[2.29.00] — 2026-08-18 (Manus): Verificación del generador real de links afiliados y primera prueba granular.** Se confirmó en la Central de Afiliados que la URL normal del producto debe pasar por el generador para producir el link afiliado final; las URLs normales no se registran como links afiliados. Mercado Libre exige etiquetas en minúsculas y números. Se crearon `usmfb2606440818`, `usmfb2605600819` y `usmfb2606590820`. Para AFF-01 se generó `https://meli.la/2zCoRix` con `usmfb2606440818`; quedó registrado como `Link_Generated_Product_Pending_Attachment`, sin publicar ni adjuntar en Facebook. Documento: `Operations/Production/2026-08-19_Playbook_Tracking_Afiliados_MercadoLibre.md`; ledger: `Operations/Research/Affiliate_Link_Ledger.csv`.

- **[2.28.00] — 2026-08-19 (Manus): Redistribución temporal de 10 oportunidades afiliadas.** La propuesta se reconcilia contra el calendario maestro 17–30 y distribuye oportunidades desde el 18 hasta el 30 de agosto, comenzando el día 18 y dejando libres los días 23, 25 y 27 como referencias sin afiliación. No se generaron URLs, no se adjuntaron productos y no se modificaron publicaciones. Documento: `Operations/Production/2026-08-19_Piloto_Afiliados_Facebook_18_30_Agosto.md`; registro: `Operations/Research/Affiliate_Pilot_Assignments.csv`.

- **[2.27.00] — 2026-08-19 (Manus): Diseño del piloto de afiliación Facebook 18–30.** Se recomienda probar cuatro-seis publicaciones sin modificar el calendario P0, con un producto, link y etiqueta únicos por publicación. Se crea `Affiliate_Metrics_Snapshots.csv` como ledger append-only para preservar cada corte de métricas. Se actualiza el playbook y la estrategia de Mercado Libre a las versiones 1.1 y 1.3.

- **[2.26.00] — 2026-08-19 (Manus): Cierre de atribución histórica de afiliados de Facebook.** Se conserva la señal agregada `Links de facebook - universesentme` como evidencia de monetización del método: 3 clics, 2 unidades vendidas, $322.65 MXN en ventas brutas y $28.84 MXN de comisión estimada. Se cierra como `No determinable por falta de granularidad` la relación entre productos y publicaciones específicas; no se atribuyen las ventas al Reel de Elara. Las futuras publicaciones deben usar etiquetas separadas por producto y post. Documento: `Operations/Research/2026-08-19_MercadoLibre_Facebook_Afiliados_Observacion.md`.

- **[2.25.00] — 2026-08-19 (Manus): Primera señal comercial verificable de afiliación en Facebook.** La Central de Afiliados de Mercado Libre muestra para el periodo 4–18 de agosto la etiqueta agregada `Links de facebook - universesentme`: 3 clics, 2 unidades vendidas, $322.65 MXN en ventas brutas y $28.84 MXN de comisión estimada. Ambas ventas están `En revisión`; el panel reporta una incidencia de datos para los días 16 y 17. La señal confirma actividad comercial de Facebook, pero no atribuye las ventas específicamente al Reel de Elara. Se documenta la observación y se recomienda separar etiquetas por publicación. Documento: `Operations/Research/2026-08-19_MercadoLibre_Facebook_Afiliados_Observacion.md`.

- **[2.24.00] — 2026-08-19 (Manus): Auditoría separada de Reels y monetización.** Se recuperaron 12 Reels/videos de Meta con mediana actual de 19.5 interacciones; julio tuvo mediana 25.5 y agosto 17.0 en la muestra recuperada. Las consultas de Insights solicitadas para vistas y retención devolvieron HTTP 400 por métricas inválidas, por lo que Reels queda subinstrumentado y no se mezcla con P0. La monetización nativa de Facebook queda como `No verificada` porque Content Monetization es invite-only y Business Suite pidió inicio de sesión; la afiliación de Mercado Libre permanece como diseño activo sin clics, conversiones ni comisiones registradas. Documento: `Operations/Research/2026-08-19_Auditoria_Reels_y_Monetizacion.md`.

- **[2.23.00] — 2026-08-19 (Manus): Auditoría integral del Growth OS.** Meta Graph API y la página responden correctamente en modo lectura; la única tarea activa es el primer corte P0 24h en `America/Matamoros`. La ola del 17 de agosto tiene cinco posts confirmados, pero el inventario maestro todavía no contiene los filenames operativos de la programación 17–30. El Publication Log tiene 98 filas, el ExperimentLog 101 y el baseline P0 cinco filas pendientes de ventana. Se detectaron cinco duplicados lógicos en el histórico de junio y 13 rutas de evidencia visual sin seguimiento; se documentan sin crear CNT ni modificar calendario, canon o Instagram. Documento: `Operations/Research/2026-08-19_Auditoria_Integral_Growth_OS.md`.

- **[2.22.00] — 2026-08-19 (Manus): Subgrupos de humor ácido analizados.** La muestra de 13 casos mantiene una mediana de 20 interacciones, pero tres outliers de funciones distintas concentran 92.6% del total. Observacional es la única microseñal repetida por encima del centro (`n=2`, mediana 30 interacciones y 6 shares). Se mantiene como hipótesis abierta; no se modifica calendario, CNT ni canon.

- **[2.21.00] — 2026-08-19 (Manus): Ampliación del humor sexual.** Se revisaron visualmente 20 casos adicionales de alto rendimiento. La muestra sexual quedó en `n=2` explícitos y `n=5` sugerentes. El grupo sugerente mantiene una señal exploratoria, pero está condicionado por un outlier textual de 171 interacciones y 50 shares; no se convierte en regla. No se crean CNT ni se modifica calendario, canon o Instagram.

- **[2.20.00] — 2026-08-19 (Manus): Humor sexual y ácido analizados por separado.** Se revisaron visualmente 16 publicaciones. El humor ácido produjo una señal exploratoria con `n=13`, mediana de 20 interacciones y 4 shares; el humor sexual quedó inconcluso con un caso explícito y uno sugerente. Se corrigieron falsos positivos de caption y se mantuvieron las categorías separadas. No se modifican calendario, CNT ni canon.

- **[2.19.00] — 2026-08-19 (Manus): Siguiente lote de diálogo y transformación revisado.** Se recuperaron y revisaron 15 candidatos adicionales. No apareció una nueva composición secuencial clara ni otra transformación corporal de Universe. Se registró `transformacion_vestuario_personaje_secundario` como hipótesis aislada para Ganso (`n=1`). La ausencia de nuevos ejemplos comparables se conserva como resultado negativo; no se fuerzan celdas ni se modifican calendario, CNT o canon.

- **[2.18.00] — 2026-08-19 (Manus): Ampliación de diálogo y transformación de Universe.** Se recuperaron y codificaron 12 publicaciones históricas con evidencia visual de Meta. La microhistoria secuencial conserva una señal prometedora pero inconclusa; las transformaciones de Universe muestran mediana exploratoria de 85.5 interacciones y 21 shares con gran dispersión. No se agruparon diálogo implícito, escenas relacionales ni controles textuales con la microhistoria. No se modifican calendario, CNT ni canon.

- **[2.17.00] — 2026-08-18 (Manus): Lote A analizado por estructura narrativa.** Se codificaron diez publicaciones históricas en `texto_simple`, `escena_caption_unico`, `duo_globo_texto`, `dialogo_secuencial`, `transformacion_visual` y `composicion_mundo`. La microhistoria y la transformación de Universe son señales prometedoras, pero inconclusas por `n=1`; no se declara ganador de formato. Se recomienda ampliar diálogos, transformaciones y escenas relacionales antes de convertir estas señales en reglas.

- **[2.16.00] — 2026-08-18 (Manus): Cinco casos convertidos en señales comparables del Growth OS.** Se creó la matriz `2026-08-18_Matriz_Aprendizajes_GrowthOS_Cinco_Casos.csv` y se añadieron las señales abiertas `HJ-001`–`HJ-005` a `GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md`. Se definió un filtro de expansión para los 58 casos: solo se analizarán cuando respondan preguntas concretas sobre estructura narrativa, personajes, transformaciones, humor, densidad visual o conversación. Las señales no modifican canon ni calendario.

- **[2.15.00] — 2026-08-18 (Manus): Nuevo alcance para los casos sin match.** Por decisión de Fernando, no se rastreará el origen de estas publicaciones en marzo, abril, mayo u otras carpetas. Los 58 casos se utilizarán únicamente por sus datos observables de Meta y revisión visual: rendimiento, formato, personajes visibles, rol narrativo, tipo de humor, potencial de etiquetado y conversación disponible. Se actualizó la hipótesis y el análisis detallado para retirar el rastreo de origen como requisito.

- **[2.14.00] — 2026-08-18 (Manus): Análisis detallado de cinco casos fundacionales.** Se analizaron `122127916017072582` (hada/Wilfred/tarot), `122134608507072582` (Ganso), `122130196011072582` (Universe muscular), `122129404893072582` (diálogo humano-hada) y `122125544019072582` (Wilfred). El resultado separa observación, hipótesis de origen, aprendizaje Growth OS y límites canónicos. El caso de Wilfred es la continuidad visual más fuerte; Universe muscular y el diálogo de tres paneles son las señales estratégicas de mayor rendimiento. Documento: `Operations/Research/2026-08-18_Analisis_Detallado_Cinco_Casos_Fundacionales_Junio.md`.

- **[2.13.00] — 2026-08-18 (Manus): Reclasificación de los 58 casos sin match como archivo fundacional.** La cola `Needs_Asset_Match` no se tratará como sobrante: conserva Meta IDs, fechas, captions y métricas, y puede representar la etapa creativa previa a la nomenclatura estable de mayo. Se recuperó y revisó visualmente el top 15 por interacciones. Aparecen Universe, Wilfred, Ganso, hadas, tarot, escenarios cósmicos y formatos de fotografía real/texto. La evidencia todavía no demuestra origen en marzo o abril; se requiere cruce visual/hash con carpetas anteriores. Documento: `Operations/Research/2026-08-18_Hipotesis_Archivo_Fundacional_Junio.md`.

- **[2.12.00] — 2026-08-18 (Manus): Junio integrado y programación histórica congelada durante P0.** Se actualizó el reporte de junio: 177 filas individuales y 172 Meta IDs únicos están integrados; quedan como reservas 17 registros sin `Asset_Ref` utilizable y 58 casos sin match. Los CNT `CNT-080`–`CNT-085` permanecen en inventario como candidatos históricos y no se programarán mientras la prueba activa de agosto continúe hasta el 30 de agosto. No se crean más CNT ni se modifica el calendario en esta fase.

- **[2.11.00] — 2026-08-18 (Manus): CNT y cola de reuse de junio aprobados.** Fernando aprobó los seis candidatos. Se crearon `CNT-080`–`CNT-085` para `2607823`, `2607787`, `2607816`, `2607828`, `260740` y `2607837` en `Content_Inventory.csv`, todos como `Reuse_Candidate`. Se generó `Operations/Research/2026-08-18_Cola_Reuse_Junio_Aprobada.csv` con restricciones de distancia, contexto, plataforma y copy. No se programó contenido, no se movieron archivos de Drive y no se modificó el calendario.

- **[2.10.00] — 2026-08-18 (Manus): Revisión visual y conversación del lote prioritario de junio.** Se revisaron 17 assets con match único de Drive. La observación directa confirmó que varios filenames `Universe - Existencial` contienen humanos, Wilfred, Ganso o dúos; no se atribuyeron personajes por filename. Se extrajeron 72 comentarios mediante un lote de lectura con el Page Access Token, sin publicar respuestas. La propuesta actual recomienda seis candidatos para decisión de CNT/reuse (`2607823`, `2607787`, `2607816`, `2607828`, `260740`, `2607837`) y mantiene los demás en investigación. Documento: `Operations/Research/2026-08-18_Propuesta_CNT_Reuse_Junio_Lote_Prioritario.md`.

- **[2.09.00] — 2026-08-18 (Manus): Inicio del lote prioritario de junio por difusión.** Se seleccionaron 25 publicaciones desde las 177 filas individuales de junio, ordenadas por shares, interacciones y comentarios. El lote queda como cola de investigación: primero se revisarán los casos con asset/Meta/Drive confirmados, después se resolverán los candidatos sin match y solo las piezas aprobadas recibirán CNT o pasarán a reuse. Se mantuvieron separadas las métricas lifetime y las ventanas P0 de agosto. Documentos: `Operations/Research/2026-08-18_Junio_Lote_Priorizado_Difusion.md` y `Operations/Research/2026-08-18_Junio_Lote_Priorizado_Difusion_Enriquecido.csv`.

- **[2.08.00] — 2026-08-17 (Manus): Auditoría de pendientes históricos de junio.** Se confirmó que junio cuenta con 177 filas individuales en `Historical_Performance_Individuals.csv`, 196 assets indexados en Drive y 172 relaciones publicación→asset confirmadas. Permanecen como reservas: 17 registros sin `Asset_Ref` utilizable y 58 posts de la cola sin asset match. La taxonomía, comentarios, lectura ampliada de personajes/horarios/formatos y selección de reuse siguen pendientes analíticos/operativos; no se recomienda crear CNT para todos los assets automáticamente. Las ventanas históricas 24/72h no se reconstruirán: se conserva lifetime separado. Documento actualizado: `Operations/Research/2026-08-17_Reporte_Final_Recopilacion_Junio.md`.

- **[2.07.00] — 2026-08-17 (Manus): Auditoría de integración histórica de julio.** Se confirmó que los seis top posts de julio ya están integrados individualmente con Meta ID, métricas lifetime, asset, Drive ID y CNT (`CNT-074`–`CNT-079`). La comparación mensual contiene 207 publicaciones de julio, pero no sustituye la reconciliación individual. El pendiente real es ampliar la muestra individual comenzando por posts con más shares y comentarios, aplicar la taxonomía normalizada y contrastar las hipótesis de etiquetabilidad, humor y horario. Se clasifica como P1 histórico y no bloquea el cierre P0 de agosto. Documento actualizado: `Operations/Research/2026-08-17_Analisis_Julio_Taxonomia_y_Pendientes_Growth_OS.md`.

- **[2.06.00] — 2026-08-17 (Manus): Verificación Meta y baseline de la ola activa.** Se verificó en modo lectura la página Universe Sent Me (`1036844829507460`) y se confirmaron cinco publicaciones reales del 17 de agosto, correspondientes a los slots 10:00, 11:00, 13:30, 16:00 y 17:00. Se creó `Operations/Research/2026-08-17_Verificacion_Meta_Ola_Activa.json` con la evidencia y `Operations/Research/2026-08-17_P0_Baseline_Ola_Activa.csv` con el cruce por fecha/slot local, Asset_Ref y Meta Post ID. Ninguna ventana 24h/72h está vencida en este corte; no se usaron totales lifetime como sustituto.

- **[2.05.00] — 2026-08-17 (Manus): Protocolo P0 de métricas comparables y veredictos.** Se definió `mediana_por_publicación` como métrica principal, con shares y comentarios raíz como métricas secundarias, separando Facebook/Instagram, formatos, nuevo/reuse y ventanas exactas de 24/72 horas. Lifetime histórico y `Corte_Observado` quedan fuera de la métrica contractual. Los veredictos serán `Validada`, `Parcialmente validada`, `No validada`, `Inconclusa` o `Invalidada por diseño`, con mínimo operativo de cinco publicaciones comparables por celda y uplift predefinido. Documento: `Operations/Research/2026-08-17_Protocolo_P0_Metricas_y_Veredictos.md`.

- **[2.04.00] — 2026-08-17 (Manus): Priorización de pendientes posterior al análisis de julio.** La secuencia CGO prioriza: P0, cerrar el ciclo de aprendizaje de la prueba activa con métricas comparables; P1, monitorear la ola Facebook 17–30, ampliar la recopilación individual de julio y consolidar la fuente maestra; P2, actualizar baseline separando canales, revisar la Biblia con Claude usando evidencia clasificada, continuar comentarios con aprobación humana y mantener Instagram controlado. CNT-004 permanece diferido y Make solo como trazabilidad histórica. Documento: `Operations/Research/2026-08-17_Prioridad_Siguientes_Pendientes_Growth_OS.md`.

- **[2.03.00] — 2026-08-17 (Manus): Revisión visual de los seis top posts de julio.** Se revisaron directamente los seis assets confirmados. Solo `2607966` y `728` muestran claramente a Universe; `2607987` muestra a Fantasma; `260504`, `260604` y `729` no aportan evidencia suficiente para asignar personajes canónicos concretos. Se corrigió la taxonomía y se invalidó el uso del filename `Universe - Existencial` como sustituto del personaje visible. El aprendizaje queda formulado como hipótesis: la situación reconocible, la emoción clara y el potencial de compartir/etiquetar parecen ser señales más defendibles que el nombre del personaje. Informe: `Operations/Research/2026-08-17_Analisis_Julio_Taxonomia_y_Pendientes_Growth_OS.md`.

- **[2.02.00] — 2026-08-17 (Manus): Aplicación inicial de la taxonomía a julio y mapa de pendientes.** Se aplicó la taxonomía normalizada a los seis posts top de julio disponibles en `Historical_Performance_Individuals.csv`. El resultado es provisional: la muestra no representa todo julio y no permite declarar superioridad de personaje o canon. La señal de aprendizaje queda formulada como hipótesis: el humor existencial/relatable y el potencial de compartir parecen explicar parte de la difusión, pero deben contrastarse con una muestra más amplia. Se documentaron los pendientes P0/P1/P2: métricas comparables 24/72h y cierre del ciclo de aprendizaje; ampliación histórica de julio; monitoreo de la ola Facebook 17–30; consolidación de fuente maestra; comentarios bajo aprobación humana; revisión de Biblia con Claude; Instagram controlado; CNT-004 diferido. Informe: `Operations/Research/2026-08-17_Analisis_Julio_Taxonomia_y_Pendientes_Growth_OS.md`.

- **[2.01.00] — 2026-08-17 (Manus): Taxonomía editorial basada en evidencia para revisión con Claude.** Se normalizaron `Content_Inventory.csv` y la base histórica de junio con `personaje_principal_normalizado`, `personajes_secundarios_normalizados`, `rol_narrativo`, `tipo_humor_normalizado`, `potencial_etiquetado`, `confianza_taxonomia`, `fuente_taxonomia` y `nota_taxonomia`. Esta capa es analítica y no modifica el canon automáticamente. La evidencia observada —assets, posts, captions, comentarios, shares, horarios y rendimiento— debe mantenerse separada de las hipótesis de aprendizaje y de las decisiones canónicas. Antes de modificar la Biblia, Claude y Manus deben revisar cada supuesto y clasificarlo como `Sustentado por datos`, `Compatible pero no demostrado`, `Contradicho por evidencia` o `Sin evidencia disponible`. Toda modificación canónica requiere aprobación explícita y actualización de los documentos de Canon y de los bridges relacionados. Documentos: `Operations/Research/2026-08-17_Taxonomia_Editorial_Contenido_USM.md`, `GrowthOS/Content_Inventory.csv`, `Operations/Research/2026-08-17_Junio_Analisis_Base.csv` y `Operations/Research/2026-08-17_Reporte_Final_Recopilacion_Junio.md`.

- Se publicó manualmente `260633 - Universe.png` en Instagram con aprobación explícita: container `17976689082089880`, media `17943879225288953`, permalink `https://www.instagram.com/p/DcIQHJJHEp0/`, hora local `2026-08-16 23:08:35`, sin `scheduled_publish_time`. Se actualizaron ambos ledgers, la propuesta Instagram, la recomendación CGO, la fuente maestra y la auditoría; no se tocó Facebook ni Drive y no se creó CNT sin evidencia.
- Fernando eliminó la tarea histórica `USM Instagram 15-16 Agosto`. Se documentó la decisión CGO de no recrearla con polling: si se automatiza una campaña nueva, deberá usar una ejecución exacta por fila, playbook autocontenido, zona `America/Matamoros`, tolerancia máxima de ±2 minutos, `no-op_late`, bloqueo idempotente y ningún uso de `scheduled_publish_time`. La recomendación inmediata sigue siendo publicación manual fila por fila hasta aprobar la campaña concreta.
- El cruce exacto de la primera ola Instagram 17–30 contra `Publication_Log.csv` confirmó 6 coincidencias con Facebook y 0 filas exclusivas de Instagram para scheduler. Fernando confirmó que `260633` fue eliminada manualmente; se actualizó su fila a `Eliminada_Manualmente` y quedó prohibida su republicación. Se prepararon cinco registros manuales para `260560`, `260614`, `260625`, `260613` y `260528`, sujetos a fecha, caption e idempotencia.
- Fernando proporcionó seis identificadores para las duplicaciones Instagram: `1564061365193135`, `1385059653723843`, `1598897621792943`, `2631450910602853`, `1372611618180903` y `1406763488012220`. Se registraron en ambos ledgers como `Programada`, sin afirmar publicación efectiva ni inventar permalink/hora real; la fila histórica eliminada de `260633` permanece separada.
- Se cerró el subpendiente P2 de normalización documental. Se alinearon la fuente maestra, el calendario Instagram, los ledgers, la auditoría, el índice, la recomendación CGO y el changelog; se creó `2026-08-17_Normalizacion_Documental_P2.md`. La deuda residual queda limitada a metadatos históricos y no bloquea la operación; Make continúa únicamente como trazabilidad.
- Se auditó la documentación estadística histórica: mayo cuenta con top posts y ranking de reuse; junio y julio cuentan con agregados completos y dataset comparativo; agosto conserva la baseline y los ledgers operativos. Se propuso integrar estos datos mediante una capa `Historical_Performance_Snapshot` separada de métricas 24/72h, sin mezclar alcance, interacciones, lifetime ni ventanas incompatibles. Informe: `2026-08-17_Integracion_Historicos_Growth_OS.md`.
- Fernando aprobó integrar primero los agregados mensuales. Se construyó `Operations/Research/Historical_Performance_Snapshot.csv` con cinco filas verificables: mayo Facebook como snapshot de top 12 posts, junio y julio Facebook como meses completos, y junio y julio Instagram como meses completos. La baseline y la fuente maestra enlazan la nueva capa; no se modificaron los ledgers operativos.
- Se completó el lote individual histórico 02: `Historical_Performance_Individuals.csv` contiene 28 candidatos Top28 de reuse de mayo y 11 top posts de junio-julio, todos con Meta ID y métricas de fuente. Se enlazó en baseline, fuente maestra e índice; no se crearon CNT automáticos ni se modificaron Publication Log o Experiment Log operativos.
- Se reconciliaron los 39 históricos contra `Content_Inventory.csv` y Drive. En el corte inicial se localizaron 28 assets exactos en `05 Mayo`; posteriormente Fernando autorizó su integración y se crearon `CNT-040`–`CNT-067`, preservando los 11 top posts de junio-julio como pendientes de evidencia de archivo. También se clasificaron lotes adicionales: 95 `Reserve`, 8 `Unmatched_Review`, 205 cruces Meta de mayo, 508 filas comparativas y 133 filas de inventario Drive. Informe vigente: `2026-08-17_Integracion_CNT_Mayo_Reserve_Revision.md`.
- De los 95 `Reserve`, 92 tienen filename exacto en Drive y 3 permanecen sin evidencia exacta: `260571 - Kiri.png`, `260550 - Universe.png` y `260617 - Elara+Kael.png`. Ninguno recibió CNT en este lote; requieren revisión editorial, distancia de 30 días y deduplicación antes de integración.
- Se completó la revisión editorial de metadatos del Reserve: 92 quedaron como `Elegible_con_revision` y 3 como `No_elegible__Evidence_missing`. Los 92 se priorizaron en 12 de Prioridad A, 27 de Prioridad B y 53 de Prioridad C. La clasificación requiere revisión visual final y no crea CNT ni autoriza reuse automáticamente. Informe: `2026-08-17_Revision_Editorial_Reserve_Mayo.md`.
- Se inició el paso a junio. La auditoría confirmó que los cinco top posts de junio ya están integrados en `Historical_Performance_Individuals.csv` con Meta ID y métricas: `El gato: 😧`, `a ver... a ver... 🤨`, `yo Aura Fuerte 😏`, `Me da miedo ser el malo de la historia...` y `🤡`. Se corrigió la fuente: las capturas compartidas con Claude pertenecen a la biblia; la fuente operativa es la carpeta Drive `06 Junio`, con 196 assets y una subcarpeta `Top`, pero sin fecha individual por asset. El siguiente cruce debe reconstruir asset→fecha mediante Meta y evidencia visual, sin asumir que los cinco top posts cubren todo junio.
- El cruce de junio encontró que `06 Junio` contiene 196 imágenes y que `Top` contiene una sola captura. La captura corresponde al post `✨✨✨` del 7 de junio, Meta ID `1036844829507460_122127939543072582`, que no estaba entre los cinco top posts integrados. La comparación visual exacta localizó `Universe - Existencial 260724.png`, Drive ID `1smMni1etHda5lhATT0XGtjE1EcAvIFYw`, y se creó `CNT-068` con confianza alta. La captura y el dataset muestran snapshots métricos diferentes; no se mezclaron. Graph live devolvió error de permisos `pages_read_engagement/Page Public Content Access`, por lo que el resto de los assets sigue pendiente.
- Se propuso crear un índice visual persistente de assets y un reporte incremental para no repetir búsquedas completas en Drive. La propuesta recomienda indexación inicial, actualización por cambios y reporte bajo demanda o cada 48 horas antes que un reporte diario como sesión completa. No se creó scheduler.
- Se construyó el índice visual inicial de `06 Junio`: 196 assets indexados con Drive ID, filename, dimensiones, SHA-256, hash visual y estado de evidencia. `260724` quedó enlazado a `CNT-068`; los otros 195 assets permanecen como `Asset_Indexed` sin fecha de publicación confirmada. OCR no se ejecutó porque Tesseract no está disponible. No se creó automatización.
- Se creó `Historical_Asset_Performance.csv` como primera capa de rendimiento por asset para la biblia. Incluye seis observaciones históricas de junio y un snapshot lifetime separado de la captura Top para `260724`; las métricas no se mezclan y los cinco posts sin asset confirmado quedan pendientes de reconciliación visual.

---

## [1.3.00] — 2026-08-17 (Manus)
### Diagnóstico y solución para ventanas temporales de Meta
- Se consultaron las referencias oficiales v26.0 de Post Insights, Page Insights y Batch Requests.
- Las pruebas reales con la cuenta Universe Sent Me confirmaron que la lectura directa del objeto post devuelve lifetime, Post/Page Insights respondieron `data=[]` para las métricas temporales probadas y `post_impressions` fue inválida en v26.0. La página sí cumple el requisito de tamaño con 4,731 seguidores/likes.
- Se documentó que el lote histórico 15–16 no puede reconstruirse con exactitud a partir de lifetime. La solución propuesta para futuras publicaciones es capturar un baseline al publicar y calcular deltas de contadores a +24h y +72h, con un solo despertar diario y Batch Requests para reducir conexiones.
- Se creó `Operations/Research/2026-08-17_Investigacion_Ventanas_Temporales_Meta.md`, se actualizó el playbook del extractor a v1.2 y se mantuvieron abiertas `HB-003`, `HB-004` y `HB-005`.
- Se añadió una propuesta de dos carriles: `Ventana_Estricta_24h/72h` para métricas contractuales y `Corte_Observado` para rescatar el lote 15–16 con reacciones, comentarios, shares y edad real del post, sin escribir esos datos en los campos estrictos.
- Se ejecutó una revisión de lectura agrupada sobre las 9 publicaciones del lote: 370 reacciones, 23 comentarios y 109 shares, para 502 interacciones observadas. Se recuperaron 23 comentarios y se generó `Operations/Research/2026-08-17_Reporte_Corte_Observado_15_16.md`; no se modificaron `Publication_Log.csv`, `ExperimentLog.csv`, `Interacciones_24h` ni `Interacciones_72h`.
- Se creó la propuesta `Operations/Research/2026-08-17_Calendario_Instagram_17_30_Propuesto.md` con seis assets existentes para una primera ola selectiva. La cola no es una programación automática: cada fila requiere aprobación explícita, URL pública exacta y ejecución inmediata con `media → FINISHED → media_publish`.
- Se auditó localmente el primer lote de 10 filas del calendario 17–30: 8 quedaron como candidatas con evidencia de asset, 2 requieren evidencia adicional y se crearon 0 CNT. La auditoría de la cola Instagram confirmó 8 filas `FB + IG selectivo`, 1 `FB + IG prioritario`, 2 `IG prioritario` y 1 `IG secundario`; no se llamó a Meta ni se publicaron filas nuevas.

---

## [1.2.99] — 2026-08-17 (Manus)
### Revisión P0 de métricas 24/72h
- El extractor oficial evaluó nueve publicaciones de Facebook del lote 15–16 en un solo lote; cuatro (`CNT-031`–`CNT-034`) ya tenían ventana 24h elegible y cinco aún no.
- Meta respondió HTTP 200, pero devolvió únicamente totales lifetime. Se conservaron como evidencia, no se escribieron en `Interacciones_24h` ni `Interacciones_72h` y no se cerraron `HB-003`, `HB-004` ni `HB-005`.
- Resultado: `4/9` ventanas 24h elegibles, `0/4` snapshots exactos, `0` escrituras métricas. Instagram no fue tocado y no se publicó contenido.
- Se actualizaron la baseline v1.4, la auditoría v1.9, el índice v5.9 y la evidencia `Operations/Research/2026-08-17_Metricas_24_72_Extraccion_02.json`.

---

## [1.2.98] — 2026-08-17 (Manus)
### Publicación de respuesta aprobada en comentario comunitario
- Fernando aprobó la respuesta `Eso ya no fue una relación, fue una temporada completa de drama con trámites incluidos. Ojalá la estabilidad te encuentre antes que la próxima cita. 😅` para el comentario `3290357934484526`.
- Meta aceptó el POST con HTTP 200 y devolvió el ID real `122148874563072582_1613678620282915`. La verificación GET posterior devolvió HTTP 403 `Missing Permissions`; no se reintentó.
- El ledger comunitario pasó a 5 respuestas publicadas y la evidencia `2026-08-17_Comentario_3290357934484526_Revision.json` quedó actualizada con el resultado real.

---

## [1.2.97] — 2026-08-17 (Manus)
### Revisión puntual de comentario personal en publicación de Silvio
- La revisión del Post ID `1036844829507460_122148874371072582` devolvió diez comentarios; nueve ya estaban registrados y uno nuevo (`3290357934484526`) fue clasificado como `Historia_Personal`.
- El comentario combina humor autobiográfico con referencias a conflicto relacional, problemas legales y malestar emocional. Se preparó una respuesta empática con humor ligero, sin discutir hechos ni ofrecer consejo legal o médico.
- La respuesta queda `Pendiente_Fernando`; no se escribió en Meta. Se actualizó el ledger comunitario a 18 comentarios y se creó `Operations/Research/2026-08-17_Comentario_3290357934484526_Revision.json`.

---

## [1.2.96] — 2026-08-17 (Manus)
### Segundo delta incremental P2 de comunidad
- Se consultó únicamente el intervalo posterior a `2026-08-16T23:41:56.744815Z`; Meta devolvió 1 publicación y 2 comentarios nuevos.
- Se registraron 1 comentario vacío y 1 mención automática `@seguidores`. No hubo comentarios cualitativos nuevos, respuestas requeridas ni escrituras en Meta.
- El ledger comunitario pasa a 17 comentarios reales y la siguiente consulta debe iniciar después de `2026-08-17T01:48:41Z`.
- Se actualizaron `Community_Engagement_Log.md`, `Community_Engagement_Log.csv`, la auditoría, la fuente maestra, el índice y la evidencia `Operations/Research/2026-08-17_P2_Comunidad_Delta_02.json`.

---

## [1.2.95] — 2026-08-17 (Manus)
### Republicación autorizada de 2608036 y 2608060 en Instagram
- Fernando confirmó explícitamente que `2608036` y `2608060` podían republicarse aunque sus intentos anteriores hubieran sido eliminados manualmente. No se generaron imágenes nuevas; se reutilizaron los assets existentes.
- Meta confirmó `FINISHED → media_publish` para ambas filas. `2608036` quedó publicado con media `17891183814416135` y permalink https://www.instagram.com/p/DcHxuuWllRk/; `2608060` quedó publicado con media `17909839698449207` y permalink https://www.instagram.com/p/DcHxv5SlorV/.
- No se usó `scheduled_publish_time`, no se tocó Facebook, Drive ni el scheduler permanente. `2608030` no se duplicó y `260583` continúa prohibida.
- Se actualizaron el playbook v1.8, el calendario 15–16, `Publication_Log.csv`, `ExperimentLog.csv`, la auditoría general, el índice y la evidencia `Operations/Research/2026-08-17_Instagram_Republicacion_2608036_2608060.json`.

---

## [1.2.94] — 2026-08-16 (Manus)
### Preflight de Instagram 2608060 detenido por idempotencia
- Fernando aprobó la prueba única para `2608060 - Kael+Maeve - gustos salvajones.jpeg` en Instagram únicamente, usando la URL pública y el caption exactos del playbook.
- La validación encontró que la fila ya tenía `IG_Media_ID=17922210816414183` y `Estado_Publicacion=Eliminada_Manualmente`. Conforme al playbook, la ejecución se detuvo antes de crear el contenedor.
- No se llamó a `media`, no se verificó `FINISHED`, no se ejecutó `media_publish`, no se usó `scheduled_publish_time`, no se reintentó y no se modificó Facebook, Drive ni el scheduler.
- El resultado quedó documentado en `Operations/Research/2026-08-16_Instagram_2608060_Prueba_Resultado.json`; el playbook pasó a v1.7 y la auditoría/índice fueron sincronizados.

---

## [1.2.93] — 2026-08-16 (Manus)
### Primer lote P2 de comunidad y preparación de baseline
- La consulta incremental de comentarios se ejecutó desde el cursor `2026-08-16T01:45:00Z` y devolvió 3 publicaciones propias con 6 comentarios nuevos.
- Se añadieron 6 filas al `Community_Engagement_Log.csv`: 4 comentarios vacíos y 2 menciones automáticas `@seguidores`. No hubo comentarios cualitativos nuevos, respuestas pendientes ni escrituras en Meta. La evidencia está en `Operations/Research/2026-08-16_P2_Comunidad_Delta_01.json`.
- El control de preparación de baseline aisló 12 observaciones del lote 15–16: 9 de Facebook y 3 de Instagram. Las 9 filas activas de Facebook tienen 0/9 snapshots 24h y 0/9 snapshots 72h; no se actualizaron cifras ni veredictos.
- Se actualizaron el Community Engagement Log, la fuente maestra, la baseline, la auditoría general, la deuda documental P2 y el índice. El siguiente P2 operativo es una nueva ventana incremental de comunidad; la baseline espera el cierre P0 de métricas.

---

## [1.2.92] — 2026-08-16 (Manus)
### CNT-004 diferido y transición a pendientes P2
- Fernando decidió dejar `CNT-004 — La Búsqueda del Frasco Olvidado` fuera del desarrollo por ahora.
- El inventario conserva intactos los campos históricos `estado` y `bloqueado_canon`, mantiene `Estado_Canon=Revision`, `Canon_Review_Required` y `Motivo_Revision_Normalizado=Canon_Contradiccion_Sustantiva`, y cambia únicamente el estado operativo a `Deferred_Operational` y el de producción a `Diferido`.
- Se actualizaron el bridge, backlog, cola de producción, cola de aprobación, fuente maestra, auditoría general, índice y deuda documental P2. CNT-004 no se marca como resuelto en canon y no forma parte del lote activo.
- El trabajo operativo continúa con los P2 de comunidad, baseline común y normalización documental; las menciones históricas a Make permanecen solo como trazabilidad.

---

## [1.2.91] — 2026-08-16 (Manus)
### Movimiento y verificación de los 46 assets del calendario 17–30
- Fernando autorizó y se ejecutó el movimiento de los 11 reuse restantes del manifiesto hacia `08 Agosto` mediante Google Drive `PATCH` con `addParents` y `removeParents`, sin crear copias.
- La consulta posterior a Drive encontró los **46/46 Drive IDs** del manifiesto dentro de `08 Agosto` y **0/46** restantes en las carpetas de origen. El CSV y el JSON del manifiesto quedaron en `MOVED_MANUALLY_VERIFIED`, conservando `MOVE_ONLY` y `copy_allowed=NO`.
- El calendario operativo 17–30 quedó actualizado: el archivado Drive ya no es pendiente. Permanecen como siguientes controles la publicación real de Facebook y la extracción de métricas 24/72h.
- No se modificó Instagram, no se publicaron posts adicionales y no se alteró Facebook durante este movimiento.

---

## [1.2.90] — 2026-08-16 (Manus)
### Auditoría general del Growth OS — estado real del control plane
- Facebook 17–30 quedó confirmado como **74/74 posts programados** por Meta; la consulta live devolvió 76 posts programados en total, incluidos 2 previos. Los 74 siguen `is_published=false`, por lo que aún no generan métricas de publicación real.
- Drive contiene 35 de los 46 archivos del manifiesto en `08 Agosto`; 11 reuse todavía no aparecen en la carpeta destino. No se ejecutaron movimientos durante la auditoría.
- `Publication_Log.csv` y `ExperimentLog.csv` registraron dos hechos adicionales de Instagram (`2608036` y `2608060`) como `Eliminada_Manualmente` / `Excluida_del_aprendizaje`, porque Meta confirmó su publicación inmediata y Fernando eliminó posteriormente ambas. No se contarán como publicaciones activas ni se republicarán automáticamente.
- La tarea histórica de Instagram quedó temporalmente transformada en una ejecución única de `2608060` a las 19:00, con `runAsNewTask=false`, sin repetición y con expiración posterior; el resultado definirá si se prepara una campaña nueva, no una reactivación permanente.
- El ciclo de aprendizaje sigue siendo el principal bloqueo: las columnas 24/72h del `ExperimentLog` están vacías, el schedule de revisión cada 48 horas está documentado como activo y `HB-003`, `HB-004` y `HB-005` permanecen abiertos.
- La fuente maestra sigue incompleta frente al calendario: `Content_Inventory.csv` tiene 39 filas, mientras el calendario 17–30 contiene 71 referencias `260####` distintas; la reconciliación debe hacerse sin inventar relaciones CNT.
- `CNT-004` continúa como única contradicción narrativa sustantiva; Silvio/Payaso está resuelto. El ledger comunitario contiene 9 comentarios y 4 respuestas publicadas, pero aún falta revisar deltas y cobertura.
- Informe actualizado: `Operations/Research/2026-08-15_Auditoria_General_Growth_OS.md` v1.6.

---

## [1.2.89] — 2026-08-16 (Manus)
### Pausa definitiva del scheduler histórico de Instagram 15–16
- La tarea `USM Instagram 15-16 Agosto` estaba activa con `runAsNewTask=true`, cron de múltiples despertares y expiración `2026-08-17T04:30:00Z`; sus ejecuciones abrían nuevas ventanas y se detenían con prerrequisitos incorrectos.
- Se verificó que `Operations/Production/instagram_15_16_scheduler_playbook.md` y `run_instagram_15_16_scheduler.py` sí existen y están versionados. El conector `Universe Sent Me Meta API` también aparece habilitado en la configuración actual; no se modificó el conector.
- La tarea fue pausada con `manus-config schedule update --enabled=false`. El playbook quedó actualizado a v1.6 y declara aprobación manual fila por fila; no se debe reactivar esta tarea histórica.
- No se publicaron posts, no se crearon contenedores ni media nuevos, no se modificó Facebook, no se movió Drive y `260583` continúa excluida por `ELIMINADA_MANUALMENTE`.

---

## [1.2.88] — 2026-08-16 (Manus)
### Programación Facebook 17–30 de agosto
- Se programaron **74 posts de Facebook** mediante Meta Graph API v26.0 usando el flujo oficial de foto temporal (`/{page_id}/photos`, `published=false`, `temporary=true`) seguido de post en `/{page_id}/feed` con `attached_media`, `published=false`, `scheduled_publish_time` y `unpublished_content_type=SCHEDULED`.
- Meta devolvió **74 Page Post IDs**, **74 Photo IDs** y **74 verificaciones exitosas** con `is_published=false`; no hubo errores finales y `260583` no apareció en el lote.
- `Publication_Log.csv` recibió 74 filas respaldadas por IDs y permalinks reales; `ExperimentLog.csv` recibió 74 observaciones operativas sin métricas inventadas ni relaciones CNT creadas sin evidencia.
- El calendario maestro y el ledger de asignación pasaron a `Programado`; el manifiesto de 46 archivos pasó a `LISTO_PARA_MOVIMIENTO_MANUAL`. No se movió ni copió ningún archivo en Drive.
- Instagram no se tocó. El extractor de métricas fue ampliado para reconocer `OBS-FB-17_30-*` cuando las publicaciones pasen de programadas a publicadas y existan ventanas 24/72h elegibles.
- Informe permanente: `Operations/Research/2026-08-16_Programacion_Facebook_17_30_Agosto.md`.

---

## [1.2.87] — 2026-08-16 (Manus)
### Integración aprobada de los 11 reuse en el calendario de agosto
- Fernando aprobó la propuesta de completar los 11 slots faltantes con 8 reuse de `06 Junio/Top` y 3 reuse Reserve de la raíz disponible de `05 Mayo`.
- El calendario maestro y el ledger de asignación quedaron actualizados a 74 slots completos: 35 `Nueva`, 36 `Reuse_Top` y 3 `Reuse_Reserve`; no quedan filas `PENDIENTE_GENERAR`.
- Los ocho assets nuevos afectados por la redistribución conservaron su identidad y fueron reubicados en el ledger y el manifiesto, sin inventar relaciones CNT↔260.
- El manifiesto CSV y JSON quedaron sincronizados con 46 archivos, `MOVE_ONLY`, `copy_allowed=NO` y `MANUAL_MOVE_AFTER_FB_PROGRAMMING`. Los archivos permanecen en sus carpetas de origen hasta confirmar la programación de Facebook; no se movió ni copió ningún archivo.
- Instagram queda explícitamente pendiente y no se modificó su scheduler ni se prepararon publicaciones.

---

## [1.2.86] — 2026-08-16 (Manus)
### Propuesta de cierre de los 11 slots restantes
- Se verificaron en Drive los ocho archivos de `06 Junio/Top`: `260646`, `260735`, `260733`, `2607794`, `2607838`, `260757`, `2607825` y `2607792`.
- Se verificaron en la raíz disponible de `05 Mayo` tres candidatos adicionales: `260571`, `260550` y `260617`. Sus fechas históricas individuales permanecen desconocidas, por lo que se clasifican como `Reuse_Reserve`, no como `Reuse_Top`.
- Se creó el anexo `Operations/Research/2026-08-16_Propuesta_Completado_11_Reuse_Junio_Mayo.csv` y se actualizó la propuesta ajustada. La alternativa completa los 11 slots, conserva los 35 assets nuevos aprobados y requiere mover ocho assets nuevos a otros slots.
- La alternativa produce 39 reuse y 35 nuevos. Con 39 reuse en 74 slots no es posible mantener cero pares consecutivos —el máximo alternado es 37—; el diseño revisado reduce el resultado a cinco pares y deja el trade-off explícito. El calendario operativo maestro no se modificó ni se aprobó automáticamente.

---

## [1.2.85] — 2026-08-16 (Manus)
### Aprobación final del lote operativo de agosto
- Fernando aprobó `260661` y `2607831`, cerrando la aprobación visual de los 35 assets nuevos asignados al calendario del 17–30 de agosto.
- Se actualizaron la clasificación visual, la asignación de slots, el calendario operativo, el inventario especializado y el informe de revisión; los 11 slots `PENDIENTE_GENERAR` permanecen sin inventar contenido.
- La validación final pasó: 35 filas nuevas asignadas, 35 captions con secuencias de emojis, 35 filas en el manifiesto, 28 reuse sin pares consecutivos y 11 placeholders.
- El movimiento de los 35 archivos a `08 Agosto` continúa siendo manual por Fernando y de tipo `MOVE_ONLY`; no se crearán copias ni se programará contenido automáticamente desde este cierre documental.

---

## [1.2.62] — 2026-08-15 (Manus)
### Reconciliado
- **Publicaciones Facebook 15–16 de agosto:** se crearon `CNT-031`–`CNT-039` para los nueve assets que no tenían una fila CNT previa. Cada relación se sustentó con filename exacto de Drive, caption/personajes del calendario aprobado, Meta Post ID y permalink confirmado por Graph API.
- `Publication_Log.csv` ahora enlaza las nueve publicaciones de Facebook con sus CNT, conserva la prueba de Instagram de `260583` como eliminada manualmente y registra la publicación manual real de `2608030` como `PUB-IG-15_16-01`/`CNT-031`.
- `ExperimentLog.csv` enlaza las nueve observaciones de Facebook y añade la observación operativa de Instagram. Las métricas de 24/72 horas siguen pendientes y no se estimaron.
### Documentado
- Se creó `Operations/Research/2026-08-15_Reconciliacion_Publicaciones_15_16_CNT.md` y se actualizaron `14_00_Fuente_Maestra_y_Ledgers.md` y `00_Índice.md`.
- El inventario pasó de 30 a 39 IDs únicos sin borrar campos históricos ni aprobar estados de canon.
### Nota operativa
- `260583` no debe republicarse. La publicación de Instagram `2608030` fue manual y no demuestra programación futura nativa ni ejecución automática del scheduler.

---

## [1.2.63] — 2026-08-15 (Manus)
### Decisión CGO
- **Métricas cada 48 horas:** se adopta una revisión agrupada cada dos días para reducir consultas repetidas y leer solo las filas del `Publication_Log` que ya alcanzaron sus ventanas de 24 o 72 horas.
- La cadencia no autoriza a sustituir un snapshot exacto de 24 horas por un total acumulado de lifetime. Si Meta no permite reconstruir retrospectivamente la ventana, se registra la limitación y no se inventa el valor.
### Estado vigente del Growth OS
- La reconciliación Facebook 15–16 y la fuente maestra están cerradas; el pendiente P0 es completar métricas/veredictos de `HB-003`, `HB-004` y `HB-005` y actualizar la baseline.
- Siguen como P0 completar métricas/veredictos de `HB-003`, `HB-004` y `HB-005` y actualizar la baseline. Silvio/Payaso ya no es un P0: la alerta fue un caché desincronizado y el bridge quedó corregido. Como P1 quedan CNT-004 por sus contradicciones narrativas sustantivas, producir/aprobar las 46 piezas nuevas del calendario 17–30, revisar los 28 reuse y retirar referencias activas a Make. Como P2 queda crear el ledger ligero de comentarios y registrar cobertura de respuestas.
- Se actualizó `Operations/Research/2026-08-15_Auditoria_General_Growth_OS.md` a la versión 1.3, `GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md` a la versión 1.3 y `GrowthOS/Integracion_Growth_OS.md` a la versión 2.4.

---

## [1.2.64] — 2026-08-15 (Manus)
### Métricas y scheduler
- Se ejecutó la primera extracción agrupada de métricas para las nueve publicaciones Facebook del experimento `EXP-2026-08-CAL-01`. Las nueve filas fueron evaluadas; `eligible_count=0`, no se escribió ninguna métrica 24/72 horas y no se modificaron veredictos. La evidencia quedó en `Operations/Research/2026-08-15_Metricas_24_72_Extraccion_01.json`.
- `Publication_Log.csv` y `ExperimentLog.csv` registraron la revisión no elegible sin inventar snapshots ni totales acumulados.
- El scheduler de Instagram quedó pausado y limpiado: se retiró `intervalSeconds`, se conservó el cron aprobado y se dejó únicamente `Universe Sent Me Meta API` adjunto. No se publicó contenido durante la operación.
- Se actualizó `Operations/Research/2026-08-15_Auditoria_General_Growth_OS.md` a la versión 1.2 y `Operations/Research/2026-08-15_Reconciliacion_Publicaciones_15_16_CNT.md` a la versión 1.3.

---

## [1.2.65] — 2026-08-15 (Manus)
### Corrección de canon y clasificación de inventario
- Se verificó localmente que `Canon_Contradictions_Report.md` marca la contradicción Silvio/Payaso como `RESUELTO` el 2026-08-03, con nombre y diseño corregido registrados bajo el commit canónico `8e9fe9a`. El bridge estaba congelado en `939752c`; se actualizó a v2.4. El repositorio canónico remoto no fue accesible desde esta sesión, por lo que la próxima sincronización debe comprobar su HEAD real.
- Se reclasificaron las 22 filas que compartían `estado_canon_normalizado=Canon_Review_Required` mediante `Motivo_Revision_Normalizado`, preservando `estado`, `bloqueado_canon` y `Estado_Canon=Revision`. Solo `CNT-004` conserva `Canon_Review_Required`; 21 filas ahora distinguen reconciliación, aprobación administrativa, restricción no bloqueante, canon resuelto o identidad reconciliada sin conflicto evidente.
- Se actualizó `Operations/Research/2026-08-15_Reclasificacion_Canon_vs_Reconciliacion.json`, `Operations/Research/2026-08-15_Reconciliacion_Publicaciones_15_16_CNT.md` a v1.4, `GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md` a v1.3, `GrowthOS/00_Índice.md` a v3.3 y la auditoría general a v1.3.

---

## [1.2.66] — 2026-08-15 (Manus)
### Cierre de sincronización y clasificación
- Se marcó `Operations/Research/2026-08-15_Reconciliacion_Lote_01_Preview.md` como `Superseded`; su conteo original de 13 `Canon_Review_Required` se conserva solo como snapshot histórico.
- Se confirmó que el campo histórico `bloqueado_canon` de `CNT-009` conserva una advertencia antigua sobre Silvio, mientras `Motivo_Revision_Normalizado=Canon_Resuelto_Reconciliacion_Pendiente` y el bridge actualizado registran la resolución canónica de `8e9fe9a`.
- No se aprobó canon nuevo. `Estado_Canon=Revision` se conserva donde correspondía y la única contradicción canónica sustantiva vigente en el inventario es `CNT-004`.

---

## [1.2.67] — 2026-08-15 (Manus)
### Resincronización del bridge con el canon administrado por Claude
- `GrowthOS/Integracion_Growth_OS.md` pasó a v2.5 y se resincronizó contra la rama `main` del repositorio canónico con HEAD `1daaad5342c278909b78076a54d8b220fa51e023`, según la ficha consultada por Claude el `2026-08-15T22:56:57Z` mediante clonación directa.
- Se incorporaron los cambios verificables posteriores a `939752c`: Universe blanco/crema y registro sarcástico limitado por Anti-tono; Kiri y su varita; Kael y Maeve como pareja canonizada; ambigüedad Evan/Kiri/Elara abierta; y las propuestas no canónicas La Hoguera y La Ciudad.
- Se incorporó la tabla de contradicciones de `La Búsqueda del Frasco Olvidado` como contenido de Growth OS evaluado contra reglas canónicas, no como contenido del repositorio de canon. Capítulos 8 y 10 y la duplicación de rol de Elara siguen activos; Capítulo 7 requiere relectura directa; Silvio está resuelto.
- Se documentó que `universe-sent-me-1` es administrado por Claude: Manus no lo modifica ni convierte contenido de Growth OS en canon. La próxima sincronización requiere una nueva ficha de HEAD.
- Se actualizó `GrowthOS/00_Índice.md` a v3.4 y `Operations/Research/2026-08-15_Auditoria_General_Growth_OS.md` a v1.4.

---

## [1.2.68] — 2026-08-15 (Manus)
### IDs, métricas y limpieza de documentación operativa
- Se corrigió la descripción del primer extractor: la extracción se ejecutó el `2026-08-15 16:59:37` en `America/Matamoros`, evaluó las nueve publicaciones de `EXP-2026-08-CAL-01`, encontró 0 ventanas 24/72 elegibles, escribió 0 métricas y no modificó veredictos.
- La tabla de IDs de `GrowthOS/Integracion_Growth_OS.md` ya incluye `@char_USM_kael` (alias visual: Chico de los Pantalones) y `@char_USM_maeve` (alias visual: Chica del Suéter) como canon cerrado desde `a994354`; la relación narrativa con Universe permanece abierta.
- `GrowthOS/10_00_Kit_de_Hashtags_USM.md` fue corregido a v1.1: `#MaeveUSM` corresponde a Maeve (Chica del Suéter) y `#KaelUSM` corresponde a Kael (Chico de los Pantalones).
- Se retiraron referencias operativas nominales a Make de README, governance, arquitectura de calendario, Approval Queue, sistema de memes, formato semanal, monetización, pipeline y bridge. La guía archivada, changelog, auditorías históricas y blueprints conservan menciones solo como trazabilidad.
- Se actualizó la auditoría general para marcar esta limpieza como cerrada/controlada y documentar el resultado real de la extracción. El índice pasa a v3.5.

---

## [1.2.71] — 2026-08-15 (Manus)
### Primer lote real de community engagement
- Se extrajeron y validaron 9 comentarios de la publicación de Silvio `1036844829507460_122148874371072582` mediante Meta Graph API v26. El lote tiene 9 `Comentario_ID` únicos, permanece anonimizado y no inventa ninguna relación `CNT-####`.
- El ledger registra 3 respuestas sugeridas en `Pendiente_Fernando`, 1 comentario escalado para revisión individual y 5 interacciones sin respuesta requerida. Ninguna respuesta se ha publicado.
- Se corrigió la alineación CSV de un insight con coma, se ejecutó `validate_community_target_lot.py` y el resultado fue `validation=ok`.
- Se actualizaron `Operations/Research/2026-08-15_Community_Engagement_Log.csv`, su ficha Markdown, `GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md`, `GrowthOS/00_Índice.md`, la auditoría general, la auditoría de comentarios y la deuda documental P2.
- Próximo paso controlado: Fernando debe aprobar o rechazar las tres respuestas propuestas y revisar individualmente el comentario escalado antes de cualquier escritura en Meta.

---

## [1.2.72] — 2026-08-15 (Manus)
### Revisión editorial del comentario 4
- Fernando revisó el comentario `122148874563072582_4457431547856510` y determinó que funciona como ampliación humorística del meme hacia ambos géneros; “ridículos” se refiere al tipo de conducta descrita y no constituye un ataque personal contra quien comentó.
- El ledger reclasificó el registro de `Riesgo_Moderacion`/`Escalado` a `Contextual_Sustantivo`/`Pendiente_Respuesta`, con `Moderacion_Estado=No_Accion` y prioridad `Media`.
- Se propuso la respuesta: “Silvio concluye: no es cosa de hombres o mujeres; es competencia mundial de ridículos.” La respuesta conserva el humor ácido sin atacar a la autora y queda pendiente de aprobación junto con las otras tres.
- Se actualizaron el CSV y la ficha del Community Engagement Log, la auditoría general, la auditoría de comentarios, el índice y la deuda documental P2. No se publicó ninguna respuesta.

---

## [1.2.73] — 2026-08-16 (Manus)
### Publicación de respuestas comunitarias aprobadas
- Fernando aprobó las cuatro respuestas del primer lote del post de Silvio y actualizó las respuestas 2 y 3 a: “Silvio no busca tendencias. Bastante tiene con terminar esa frase” y “Wilfred lleva años diciendo eso. Nadie le hace caso.”
- La publicación mediante Meta Graph API v26 usó el Page Access Token derivado para `Universe Sent Me`; Meta respondió HTTP 200 en las cuatro operaciones y devolvió estos `Respuesta_Meta_ID`: `122148874563072582_27890320530627412`, `122148874563072582_1085071464477450`, `122148874563072582_1591809705981593` y `122148874563072582_1358728859707799`.
- `Community_Engagement_Log.csv` añadió el campo `Respuesta_Meta_ID` y actualizó las cuatro filas a `Respuesta_Estado=Respondido`, `Aprobacion_Estado=Aprobada`, con timestamp `2026-08-16T01:45:00.480282+00:00`.
- La prueba valida el flujo de aprobación humana y escritura controlada; no habilita respuestas automáticas ni crea un bot.
- Se sincronizaron la ficha del ledger, la fuente maestra, las auditorías, el índice y la deuda documental P2. Ninguna relación `CNT-####` fue inventada.

---

## [1.2.74] — 2026-08-16 (Manus)
### Optimización de cadencia de métricas
- La revisión diaria de métricas quedó sustituida por una revisión agrupada cada 48 horas para reducir despertares y consultas repetidas.
- La hora recomendada para `EXP-2026-08-CAL-01` es **22:15 de America/Matamoros**, comenzando el `2026-08-16`; a esa hora ya maduró el último slot del día anterior y el lote puede procesar todas las filas vencidas de una sola vez.
- Se confirma que **un solo despertar por ejecución es suficiente** para las nueve publicaciones: el extractor recorre las filas vencidas, consulta solo los Meta Post IDs elegibles y no requiere un despertar por publicación.
- La tarea de métricas no apareció entre los schedules visibles de esta sesión; solo se observó `USM Instagram 15-16 Agosto`, pausado. No se modificó ese scheduler para evitar alterar una tarea distinta.
- Se actualizaron `GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md` a v1.7 y `Operations/Research/2026-08-08_Ciclo_Diario_Metricas_24h.md` a v1.1 (Superseded).

---

## [1.2.75] — 2026-08-16 (Manus)
### Separación de la tarea de métricas
- Fernando decidió crear una tarea independiente para la revisión de métricas, en lugar de reutilizar la sesión que contiene el scheduler pausado de Instagram.
- La nueva tarea deberá ejecutarse cada 48 horas a las 22:15 de `America/Matamoros`, comenzando el 2026-08-16, con un solo despertar por ejecución y procesamiento agrupado de todas las filas vencidas.
- La tarea `USM Instagram 15-16 Agosto` no fue modificada. La creación del nuevo schedule requiere abrir una tarea independiente, porque esta sesión ya tiene un schedule asociado y el CLI no expone aquí una credencial para crear otra tarea programáticamente.
- Se actualizó `Operations/Research/2026-08-08_Ciclo_Diario_Metricas_24h.md` para registrar la decisión.

---

## [1.2.76] — 2026-08-16 (Manus)
### Estado de programación de métricas
- Se intentó crear la tarea independiente `USM Growth OS - Revisión de Métricas cada 48h` para `EXP-2026-08-CAL-01`, con primer disparo el 2026-08-16 a las 22:15 de `America/Matamoros`, repetición cada 48 horas y un solo despertar por ejecución.
- El servicio de programación devolvió `permission_denied: 403 Forbidden`; la tarea no quedó creada ni activa. No se modificó el scheduler pausado de Instagram, no se publicó contenido y no se alteraron `Publication_Log.csv` ni `ExperimentLog.csv`.
- La ruta exacta `/home/ubuntu/extract_metrics_24_72.py` no estaba disponible en ese entorno. La activación quedó bloqueada hasta restaurar el extractor exacto y habilitar la creación del schedule.
- Se actualizó `Operations/Research/2026-08-08_Ciclo_Diario_Metricas_24h.md` a v1.2 con el estado, las restricciones y las acciones pendientes.

---

## [1.2.77] — 2026-08-16 (Manus)
### Reintento de creación del scheduler de métricas
- Tras la solicitud explícita de Fernando, se reintentó crear `USM Growth OS - Revisión de Métricas cada 48h` como tarea independiente, recalculando el intervalo hasta el primer disparo de las 22:15 en `America/Matamoros` (`77190` segundos al momento del intento).
- El servicio volvió a responder `permission_denied: 403 Forbidden`; la tarea no quedó creada, no existe un schedule activo y no se ejecutó ninguna revisión de métricas.
- La verificación confirmó que `/home/ubuntu/extract_metrics_24_72.py` estaba ausente en el entorno de la sesión. No se creó un sustituto en ese intento ni se modificaron `Publication_Log.csv`, `ExperimentLog.csv`, Instagram o el scheduler de Instagram.
- Se actualizó `Operations/Research/2026-08-08_Ciclo_Diario_Metricas_24h.md` a v1.3.

---

## [1.2.79] — 2026-08-16 (Manus)
### Schedule de revisión de métricas materializado
- Se creó y verificó como activo `USM Growth OS - Revisión de Métricas cada 48h`, con task UID `egAl6a7WZExBrDPd8tIY1B`, expresión `0 15 22 */2 * *` y zona horaria `America/Matamoros`.
- El schedule usa únicamente `Universe Sent Me Meta API` para consultas de lectura; no hereda Instagram, no publica contenido, no modifica Instagram y no altera el scheduler de Instagram.
- La tarea ejecuta `/home/ubuntu/extract_metrics_24_72.py` en un solo despertar por lote, procesa únicamente filas vencidas de `EXP-2026-08-CAL-01` en Facebook, actualiza los dos ledgers autorizados y registra evidencia JSON.
- Se validó la copia operativa contra `Operations/Production/extract_metrics_24_72.py`. La prueba seca encontró 9 candidatos y 9 ventanas 24h elegibles, sin llamadas de red ni cambios en ledgers.
- Se actualizaron `Operations/Production/extract_metrics_24_72_playbook.md` a v1.1 y `Operations/Research/2026-08-08_Ciclo_Diario_Metricas_24h.md` a v1.4.

---

## [1.2.78] — 2026-08-16 (Manus)
### Extractor de métricas recreado y validado
- Se recreó `Operations/Production/extract_metrics_24_72.py` y se dejó una copia operativa en `/home/ubuntu/extract_metrics_24_72.py` para la tarea independiente.
- El extractor procesa en un solo despertar todas las filas vencidas de `EXP-2026-08-CAL-01`, calcula ventanas con `America/Matamoros`, deriva el Page Access Token de la Página correcta y nunca publica ni modifica Instagram.
- La idempotencia usa `Publicacion_ID` y marcadores `METRICS-RUN:<run_id>`; si Graph API solo devuelve totales lifetime, registra `24h_snapshot_unavailable`/`72h_snapshot_unavailable` y no escribe esos totales en campos de ventana.
- La validación seca determinista encontró 9 candidatos y 9 ventanas de 24 horas elegibles, escribió 0 métricas y 0 ledgers, y confirmó `single_wakeup_batch=true`, `instagram_touched=false` y `content_published=false`. Las pruebas unitarias de cálculo e idempotencia también pasaron.
- Se creó `Operations/Production/extract_metrics_24_72_playbook.md` y se actualizó el índice y la fuente maestra. La programación sigue bloqueada externamente por `permission_denied: 403 Forbidden`; no se intentó modificar Instagram.

---

---

## [1.2.79] — 2026-08-16 (Manus)
### Revisión de pendientes después de activar métricas
- `Operations/Research/2026-08-15_Auditoria_General_Growth_OS.md` pasó a v1.5 y refleja que la tarea independiente de métricas está activa con `egAl6a7WZExBrDPd8tIY1B`, cron `0 15 22 */2 * *`, zona `America/Matamoros` y un solo despertar.
- El P0 ya no es crear el schedule: queda esperar la primera ejecución válida, verificar la evidencia, actualizar `Publication_Log.csv` y `ExperimentLog.csv`, cerrar `HB-003`/`HB-004`/`HB-005` y actualizar la baseline.
- Se mantienen como P1: prueba `nothing_due` antes de reactivar Instagram, revisión de `CNT-004`, normalización completa de estados y preparación/aprobación del calendario 17–30. La comunidad queda en P2 para medir cobertura y tiempo de respuesta en nuevos deltas.

---

## [1.2.80] — 2026-08-16 (Manus)
### Revisión del calendario experimental 17–30
- Se auditó la propuesta de 74 slots contra el inventario de 38 assets nuevos y el `Publication_Log.csv`.
- Se confirmó que 5 assets de los 38 ya fueron publicados en 15–16 (`2608030`, `2608033`, `2608036`, `2608037` y `2608060`); quedan 33 nuevos no registrados como publicados para revisión visual, no aprobación automática.
- Se detectaron cinco pares de reuse consecutivos. Se preparó una propuesta Draft que conserva 46 nuevas y 28 reuse, mantiene `260528` el domingo 30 a las 22:00 y reubica cinco reuse sin tocar el calendario anterior.
- Drive confirmó que `260508 - Universe.jpg` y `Universe - Existencial 260508.png` son dos archivos distintos con checksums y contenidos visuales diferentes; ambos deben conservar filename completo para evitar ambigüedad.
- Se crearon `Operations/Research/2026-08-16_Revision_Calendario_17_30.md` y `Operations/Research/2026-08-16_Propuesta_Ajuste_Calendario_17_30_Agosto.md/.csv`. La propuesta queda pendiente de aprobación de Fernando; no se generaron imágenes, no se movieron assets y no se programó contenido.

---

## [1.2.84] — 2026-08-16 (Manus)
### Corrección del conteo Drive y captions de emojis
- Fernando señaló que la carpeta raíz contiene 35 imágenes, no 33. La conciliación directa de Drive confirmó 41 hijos: 6 carpetas mensuales y 35 imágenes.
- Los dos extras no registrados inicialmente son `260661` (Wilfred: memes prohibidos) y `2607831` (Kiri: pollo asado en el cine). Ambos se integraron al inventario especializado, clasificación, asignación y manifiesto, y Fernando aprobó su inclusión en el calendario.
- La versión operativa ahora contiene 35 assets nuevos asignados, 11 placeholders y 28 reuse. Los 35 nuevos usan captions de secuencias de múltiples emojis más hashtags del kit USM; los reuse conservan sus captions previos.
- Fernando moverá manualmente los archivos; el manifiesto de 35 assets es de referencia `MOVE_ONLY`, con `copy_allowed=NO`, y no se ejecutará ningún movimiento desde esta sesión.

---

## [1.2.83] — 2026-08-16 (Manus)
### Calendario operativo y manifiesto de movimiento
- Fernando aprobó las 33 asignaciones visuales: 18 candidatos generales y 15 candidatos con control editorial.
- Se generó `2026-08-16_Calendario_Operativo_17_30_Agosto.csv/.md` con captions mínimos del kit USM, 28 reuse aprobados y 13 slots `PENDIENTE_GENERAR`.
- Se verificaron los 33 Drive IDs y todos permanecen en `Humor existencial` (`1b0FRf8BFg2fIUoIf5CeMeiQb3uDduWcZ`). El destino correcto es `08 Agosto` (`11nuEUoU2Or8uc0oxXLu7-k6LChk8zQNf`).
- Se generó el manifiesto `MOVE_ONLY` con 33 filas; no permite copias y queda `READY_FOR_USER_CONFIRMATION`. No se movieron archivos ni se programó contenido.

---

## [1.2.82] — 2026-08-16 (Manus)
### Revisión visual de los 33 memes nuevos
- Se descargaron localmente los 33 assets aún no registrados como publicados y se revisaron visualmente por lotes; no se movió ni copió ningún archivo dentro de Drive.
- Se generaron `2026-08-16_Clasificacion_Visual_33_Memes_Nuevos.csv` y `2026-08-16_Asignacion_Visual_Calendario_17_30_Agosto.csv`.
- Resultado validado: 28 candidatos asignados a slots `Nueva`, 5 piezas retenidas por aprobación editorial (`2608047`, `2608051`, `2608053`, `2608059`, `2608062`) y 18 slots todavía `PENDIENTE_GENERAR`.
- Las piezas sensibles se mantienen fuera de la programación automática: contienen sexualidad explícita, doble sentido fuerte o una representación romántica coercitiva. No se descartan sin decisión de Fernando.
- Se creó `2026-08-16_Revision_Visual_Asignacion_33_Memes_Nuevos.md`; la propuesta queda en estado `Review` y no autoriza generación, movimiento, programación ni publicación.

---

## [1.2.81] — 2026-08-16 (Manus)
### Aprobación parcial del calendario 17–30
- Fernando aprobó los cinco movimientos de reuse documentados en `2026-08-16_Propuesta_Ajuste_Calendario_17_30_Agosto.md`.
- La propuesta conserva estado `Review`: los 46 slots nuevos siguen como `PENDIENTE_GENERAR` y los 33 assets nuevos disponibles aún requieren revisión visual/editorial.
- Se actualizó el índice y la auditoría del calendario. No se movieron assets de Drive, no se generaron imágenes y no se programó contenido.

---

## [1.2.70] — 2026-08-15 (Manus)
### Pendientes P2: comunidad, baseline y deuda documental
- Se creó `Operations/Research/2026-08-15_Community_Engagement_Log.csv` con encabezados y cero filas intencionalmente; no se inventó un backfill de los 67 comentarios históricos.
- Se creó `Operations/Research/2026-08-15_Community_Engagement_Log.md` con taxonomía, privacidad, ventanas de revisión y reglas de aprobación humana.
- `GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md` pasó a v1.4 e incorporó el Community Engagement Log como ledger cualitativo complementario.
- `GrowthOS/08_00_Metricas_Baseline_Plataformas.md` pasó a v1.2 y documenta el esquema de comparación Facebook/Instagram; no se alteraron cifras históricas ni se escribieron métricas prematuras del lote 15–16.
- `Operations/Research/2026-08-15_Deuda_Documental_P2.md` clasifica documentos activos, históricos, superseded y pendientes de metadatos; las referencias restantes a Make quedan como trazabilidad.
- Se actualizaron el sistema de dos capas, la auditoría de comentarios, la auditoría general y el índice maestro.

---

## [1.2.69] — 2026-08-15 (Manus)
### Corrección de alias canónicos de Maeve y Kael
- Se corrigió la correspondencia confirmada por Fernando: **Chica del Suéter = Maeve** y **Chico de los Pantalones = Kael**.
- `GrowthOS/Integracion_Growth_OS.md` pasó a v2.5.1 y eliminó las dos filas estructurales duplicadas; Maeve y Kael conservan sus IDs canónicos y ahora incluyen sus alias visuales/editoriales.
- `GrowthOS/10_00_Kit_de_Hashtags_USM.md` quedó alineado con `#MaeveUSM` y `#KaelUSM`.
- `Content_Inventory.csv` actualizó CNT-013 y CNT-014 a `@char_USM_maeve` y `@char_USM_kael`, preservando los campos históricos de estado y bloqueo.
- `GrowthOS/Canon_Contradictions_Report.md` dejó registrado que ambos nombres quedaron formalizados en `a994354`.
- El índice pasa a v3.6.

---

## [1.2.17] — 2026-08-14 (Manus)
### Añadido
- **Custom API de Meta para Universe Sent Me:** se creó y activó el conector `Universe Sent Me Meta API` con almacenamiento seguro del Page Access Token como `META_PAGE_ACCESS_TOKEN`. La verificación `GET /me?fields=id,name` respondió HTTP 200 e identificó la página como `Fernando Gdlr` (ID `2920605591459033`). El token no se documenta ni se sube al repositorio.
### Nota
- La integración permite consultar identidad, publicaciones e insights, y preparar operaciones de publicación; cualquier escritura debe ejecutarse solo después de una solicitud explícita y confirmación previa de Fernando.
- Se actualizó `13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md` y la entrada correspondiente en `00_Índice.md`.

---

## [1.2.18] — 2026-08-14 (Manus)
### Añadido
- **Diagnóstico de permisos Meta:** el token efectivo devuelve `pages_manage_engagement`, `pages_read_engagement` y la tarea `MODERATE` para la página Universe Sent Me; se verificó lectura de comentarios de Facebook con HTTP 200 usando el Page Access Token derivado desde el token de usuario.
- La cuenta profesional de Instagram `17841462696378190` está vinculada a la página `1036844829507460`, pero el permiso `instagram_manage_comments` no está concedido. Por ello, la respuesta automatizada a comentarios de Instagram queda bloqueada hasta solicitar y reautorizar ese permiso.
- Se registraron los permisos efectivos y las cuentas vinculadas en `13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md`.

---

---

## [1.2.47] — 2026-08-15 (Manus)
### Auditoría de comentarios de Facebook
- Se creó `Operations/Research/2026-08-15_Auditoria_Comentarios_Facebook.md` con la verificación directa de permisos y la propuesta CGO de escucha, respuesta humana guiada y aprendizaje editorial.
- `/me/permissions` respondió HTTP 200; el token tiene `pages_manage_engagement`, `pages_read_engagement` y la Página devuelve `MODERATE`/`CREATE_CONTENT`.
- La lectura de `/{post_id}/comments` respondió HTTP 200. En 20 publicaciones recientes se observaron 67 comentarios acumulados, 16 publicaciones con comentarios, mediana de 2 y máximo de 14.
- La escritura de respuestas, ocultamientos o eliminaciones no se probó; queda pendiente una prueba controlada con confirmación explícita de Fernando.
- El mismo chequeo mostró que `instagram_manage_comments` ahora está concedido, por lo que se corrige el diagnóstico anterior de permiso ausente. La moderación de Instagram sigue separada y no se automatiza todavía.

---

## [1.2.48] — 2026-08-15 (Manus)
### Análisis cualitativo de comentarios de Facebook
- Se recuperó el texto anonimizado de los 67 comentarios de las 20 publicaciones recientes y se actualizó `Operations/Research/2026-08-15_Auditoria_Comentarios_Facebook.md` a la versión 1.1.
- La muestra contiene 14 comentarios de distribución de la página, 15 vacíos, 13 etiquetas sociales, 9 acuerdos o risas breves, 6 reacciones de emojis, 7 comentarios contextuales y 3 críticos o de riesgo.
- “¿Qué quieres desayunar?” fue la publicación más conversacional con 14 comentarios; “Tus únicas amigas son estas” concentró 11; el meme de Silvio concentró 8 y también los riesgos de tono más claros.
- La comunidad dejó señales de auto-revelación sobre soledad, sinceridad, afecto y extrañar a alguien. Se recomienda medir comentarios cualitativos por separado de menciones automáticas y emojis.
- Se recomendó revisar el mismo día y entre 24–48 horas después, mantener respuestas humanas guiadas y probar un estímulo conversacional por día como máximo durante el calendario experimental.

---

## [1.2.49] — 2026-08-15 (Manus)
### Comunidad y respuestas creativas
- Fernando confirmó que las respuestas tardías todavía generan agradecimiento explícito —“por eso amamos la página”— y que una mejora de velocidad puede fortalecer una relación que ya existe.
- Se actualizó `Operations/Research/2026-08-15_Auditoria_Comentarios_Facebook.md` a la versión 1.2 para incorporar una estrategia de assets de respuesta: memes juguetones, reacciones de personajes, llamadas de atención cariñosas y cierres visuales.
- Los comentarios negativos se tratarán individualmente. Un comentario oscuro o de estrés no se penaliza automáticamente; se observarán patrones de acoso, amenazas, discriminación, spam o escalamiento antes de ocultar, eliminar o bloquear.
- `GrowthOS/12_00_Sistema_Dos_Capas_Contenido_Canon.md` dejó de considerar pendiente la evidencia de comunidad: el agradecimiento por el tono de respuesta se reconoce como señal cualitativa de pertenencia. Queda pendiente formalizar el registro mensual y la biblioteca de assets.

---

## [1.2.50] — 2026-08-15 (Manus)
### Primer lote de memes de respuesta USM
- Se creó `Operations/Research/2026-08-15_Propuesta_Memes_Respuesta_USM.md` con cinco adaptaciones de referencias externas al lenguaje visual y narrativo de Universe Sent Me.
- Se generaron cinco assets verticales 4:5 con Silvio, Wilfred, Elara, Universe y Fantasma, usando referencias temporales de personajes y escenarios de `My Drive/Universe sent me/USM/Elementos`.
- La estructura de los memes conserva el ritmo y la función de las referencias, pero reemplaza identidades externas, evita la referencia estigmatizante a esquizofrenia y convierte el frasco en “paciencia cósmica”.
- Los assets quedan en estado `Review`; no se crearon copias permanentes en Drive ni se publicaron automáticamente. El traslado a producción queda pendiente de aprobación de Fernando.

---

## [1.2.51] — 2026-08-15 (Manus)
### Regeneración visual Nano Banana de memes de respuesta
- Fernando indicó que la primera versión se sentía demasiado como plantilla de meme y pidió conservar exactamente los textos de las referencias, pero con el lenguaje de animación fantástica de Universe Sent Me.
- Se regeneraron las cinco piezas con Nano Banana Pro, usando como referencia las versiones anteriores, personajes canónicos y escenarios de `My Drive/Universe sent me/USM/Elementos`.
- La nueva dirección usa fondos narrativos detallados, profundidad ambiental, iluminación cinematográfica y cintas de texto integradas al mundo. La pieza “QUE NO SOMOS ADIVINOS” quedó identificada como la favorita provisional.
- La pieza 2 conserva deliberadamente el texto original `PASTILLAS ESQUIZOFRENIA` por solicitud de fidelidad; queda marcada como texto sensible para revisión antes de producción.
- Se actualizó `Operations/Research/2026-08-15_Propuesta_Memes_Respuesta_USM.md` a la versión 2.0. Las cinco piezas quedan en estado `Review`, sin publicación ni copias permanentes en Drive.

---

## [1.2.52] — 2026-08-15 (Manus)
### Assets cuadrados para seguidores activos
- Se añadieron tres propuestas de respuesta para seguidores que comentan con frecuencia: Universe agradece su presencia, Wilfred los reconoce y Silvio celebra que comenten.
- Los tres assets fueron generados con Nano Banana Pro en formato 1:1, con fondos mínimos, gradientes mágicos y foco principal en personaje, expresión y frase.
- Se actualizó `Operations/Research/2026-08-15_Propuesta_Memes_Respuesta_USM.md` a la versión 2.1 y se incorporó el lote al registro canónico de comunidad.
- Los assets quedan en estado `Review`; son respuestas individuales y no publicaciones del calendario regular.

---

## [1.2.61] — 2026-08-15 (Manus)
### Primer lote de unificación de la fuente maestra
- `Content_Inventory.csv` conserva 30 filas, 30 IDs únicos y todos los campos históricos.
- Se añadieron los campos canónicos derivados `Asset_Ref`, `Asset_Filename`, `Drive_ID`, `Estado_Canon`, `Estado_Produccion`, `Estado_Publicacion` y `Ultima_Sincronizacion`.
- El lote enlaza 2 piezas con publicación Meta (`CNT-002` y `CNT-023`) y deja 28 piezas sin publicación confirmada; no se confirmó ningún `260####` sin evidencia.
- Quedan pendientes de integración: mapear las 9 órdenes del calendario 15–16 a `ID_Pieza`, completar métricas 24/72 horas, enlazar el ExperimentLog con publicaciones, resolver revisiones de canon y convertir calendarios/colas en vistas verificables.
- La migración conserva reversibilidad: los estados históricos no se eliminan ni se sustituyen automáticamente.

---

## [1.2.60] — 2026-08-15 (Manus)
### Resolución de CNT-029 y CNT-030
- Se verificó la ficha de producción v2.1 de CNT-029: reel “Pausa para ver qué piensa de ti”, banco de 9 cuadros, hook de pausa y estado `Draft_Pending_Approval`.
- Se verificó la ficha v2.0 de CNT-030: audio y concepto de montaje dependiente de CNT-029, también `Draft_Pending_Approval`; no es una publicación independiente.
- La búsqueda acotada de Meta del 14–17 de agosto no encontró un caption o permalink coincidente para CNT-029/CNT-030. No se añadieron filas ficticias al `Publication_Log`.
- Se conservaron los nombres de assets documentados y se registraron las dependencias `CNT-029 ↔ CNT-030` en el inventario maestro.
- Las cuatro excepciones del lote 1 quedan resueltas a nivel de registro; CNT-029/CNT-030 solo requieren aprobación y publicación futura para completar su trazabilidad de ejecución.

---

## [1.2.59] — 2026-08-15 (Manus)
### Publicación confirmada de CNT-023 — Elara / Lámpara de Luna
- Fernando proporcionó el permalink `https://www.facebook.com/reel/1067337609170026` y la verificación visual confirmó el Reel de Elara con la caja de Mercado Libre.
- Meta Graph API resolvió el Reel como Page Post ID `1036844829507460_122147352825072582`, creado el 2026-08-09 a las 01:19:54 UTC, con caption de “¿Qué me llegó?”, CTA `LUNA` y hashtags `#UniverseSentMe #QueMeLlegoUSM #UniverseUSM #ElaraUSM`.
- `CNT-023` pasó a `Published` en `Content_Inventory.csv` y se añadió `PUB-FB-2026-08-08-CNT023` a `Publication_Log.csv`.
- Se conservó la resolución como conjunto de 7 assets de Drive; no se inventó un `260####` individual.
- Se actualizaron el preview de reconciliación, la fuente maestra y el índice.

---

## [1.2.58] — 2026-08-15 (Manus)
### Cierre de CNT-023 como conjunto de assets
- Se verificó nuevamente la carpeta Drive `Elara - Lampara de luna` mediante `gws`: contiene 7 archivos hijos, cuatro videos/imagenes de entrega y apertura de paquete y tres renders de secuencia.
- `CNT-023` mantiene el estado `Resolved_Asset_Set`, conserva los siete nombres en `asset_set`, el `drive_reference_id` de la carpeta y la relación `registro_relacionado=CNT-002`.
- No se asignó un `260####` individual porque el episodio 2 de “¿Qué me llegó?” es un conjunto de producción y no una publicación histórica separada. No se añadió ninguna fila ficticia a `Publication_Log`.
- Se actualizó el preview de reconciliación y `GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md`; la validación conserva 30 filas y 30 IDs únicos.

---

## [1.2.57] — 2026-08-15 (Manus)
### Cierre de CNT-002 mediante Meta Graph API
- Se identificó el post real de CNT-002 mediante Graph API: `1036844829507460_122143141185072582`, publicado el 2026-07-30 a las 14:16:47 UTC, con permalink `https://www.facebook.com/reel/911880681976378/`.
- El reel dura 17.39 segundos y su secuencia coincide con los videos de producción de Drive `Wilfred_holding_plush_toy_202607300618.mp4`, `Wilfred_holding_plush_unimpressed_202607300634.mp4` y `Cat_carrying_box_to_Wilfred_202607300636.mp4`.
- Se rechazó definitivamente la asociación con `260509`, cuyo archivo es `Universe - Existencial 260509.png`.
- `CNT-002` quedó como `Resolved_Production_Set`; se añadió la publicación histórica a `Publication_Log.csv` y se registró el permalink, fecha, Meta ID y conjunto de producción en `Content_Inventory.csv`.
- La excepción queda cerrada sin inventar un render final `260####` que no existe como archivo localizado.

---

## [1.2.56] — 2026-08-15 (Manus)
### Resolución de excepciones del inventario
- `CNT-002 → 260509` fue rechazado como `Rejected_Mismatch`: el post de Meta del 30 de julio corresponde a Wilfred/MercadoLibre/plush, mientras 260509 es un asset de Universe existencial.
- `CNT-023` fue resuelto como `Resolved_Asset_Set`: su episodio 2 de “¿Qué me llegó?” se conecta a la carpeta Drive `Elara - Lampara de luna`, con 7 videos de producción, sin forzar un único `260####`.
- `CNT-029` y `CNT-030` fueron incorporados desde sus documentos de producción y enlazados entre sí; CNT-030 es el registro dependiente de audio/montaje de CNT-029, no una publicación independiente.
- `Content_Inventory.csv` pasó de 28 a 30 registros, manteniendo las columnas históricas y sin inventar ningún asset 260 confirmado. El único pendiente operativo es localizar el asset exacto de CNT-002.
- Se actualizaron el preview de reconciliación, `GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md` y `GrowthOS/00_Índice.md`.

---

## [1.2.55] — 2026-08-15 (Manus)
### Normalización y reconciliación de inventario — lote 1
- Se auditaron las 28 filas actuales de `GrowthOS/Content_Inventory.csv` y se conservaron intactas las columnas históricas `estado` y `bloqueado_canon`.
- Se añadieron estados normalizados y campos de reconciliación reversibles. La distribución operativa quedó en 17 `Idea`, 3 `Production_Pending`, 3 `Draft_Pending_Approval`, 2 `Pending_Approval`, 2 `Reuse_Candidate` y 1 `Blocked_Operational`.
- La búsqueda encontró dos relaciones históricas candidatas, pero ninguna confirmada: `CNT-002 → 260509` tiene conflicto de título; `CNT-023 → 260801` no tiene archivo exacto en Drive y solo aparecen referencias `2608010–2608019`.
- `CNT-029` y `CNT-030` aparecen en el historial del repositorio pero faltan en el inventario actual. No se crearon filas automáticamente.
- Se añadió el preview `Operations/Research/2026-08-15_Reconciliacion_Lote_01_Preview.md` y se actualizó `GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md` y `GrowthOS/00_Índice.md`.

---

## [1.2.54] — 2026-08-15 (Manus)
### Primer ExperimentLog y fuente maestra unificada
- Se creó `Operations/Research/2026-08-15_ExperimentLog.csv` con seis observaciones históricas de junio–agosto y nueve publicaciones de Facebook del 15–16 de agosto pendientes de métricas 24/72 horas.
- Se creó `Operations/Research/2026-08-15_Publication_Log.csv` con una fila por publicación/plataforma: 9 órdenes de Facebook y 1 prueba de Instagram eliminada manualmente.
- Se creó `GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md`, estableciendo `Content_Inventory.csv` como fuente de identidad, los dos CSV como ledgers append-only y los calendarios/colas como vistas.
- Se actualizó `Integracion_Growth_OS.md`, `01_00_Arquitectura_Calendario_Escalable.md`, `13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md` y `00_Índice.md` para compartir la nueva trazabilidad y consultar solo deltas, reduciendo lecturas y llamadas repetidas.
- Las métricas 24/72 horas de las nueve publicaciones quedan pendientes hasta que transcurran las ventanas válidas; no se estiman ni se inventan resultados.

---

## [1.2.53] — 2026-08-15 (Manus)
### Auditoría general de integración del Growth OS
- Se creó `Operations/Research/2026-08-15_Auditoria_General_Growth_OS.md` como nueva línea base de auditoría, comparando la arquitectura documentada con el estado live de Meta Graph API, conectores, scheduler, calendarios, inventarios, comunidad y ciclo de aprendizaje.
- Se verificó que Facebook está operativamente integrado: Meta devolvió 9 publicaciones programadas, coincidentes con el calendario 15–16 de agosto, y los assets fueron archivados sin copias.
- Se verificó que Instagram está técnicamente accesible, pero que su programación nativa no está disponible y que el estado live del scheduler conserva una discrepancia entre cron, intervalo de 900 segundos, modo de ejecución y conectores adjuntos.
- Se identificaron como brechas principales el `ExperimentLog` vacío, la baseline de métricas atrasada, la fragmentación de inventarios/calendarios, el caché de canon atrasado con conflicto Silvio/Payaso y las referencias históricas a Make en documentos operativos.
- `GrowthOS/00_Índice.md` fue actualizado a la versión 3.0; la auditoría del 14 de agosto queda marcada como `Superseded` por este reporte.

---

## [1.2.46] — 2026-08-15 (Manus)
### Optimización y primera verificación del scheduler Instagram 15–16
- Se corrigió la preparación inicial de assets para que `gws drive files get` descargue a nombres temporales seguros dentro de su directorio de trabajo.
- Las cinco imágenes aprobadas para Instagram se alojaron una sola vez en URLs temporales y se guardaron en `/home/ubuntu/instagram_15_16_public_urls.json`.
- `run_instagram_15_16_scheduler.py` dejó de descargar desde Drive y ejecutar `manus-upload-file` en cada despertar; ahora reutiliza exclusivamente el manifiesto de URLs, conserva la ventana de 8 minutos, la idempotencia, la exclusión de `260583` y la protección de Facebook.
- La tarea `USM Instagram 15-16 Agosto` quedó activa con 16 despertares candidatos, `runAsNewTask=true`, zona `America/Matamoros` y expiración `2026-08-17T04:30:00Z`.
- Se ejecutó el runner a las 00:16:21 en `America/Mexico_City` y devolvió `nothing_due`; no había ningún slot dentro de la ventana válida de ocho minutos, por lo que no se realizaron llamadas `media`, verificación ni `media_publish`.
- No se generaron IDs de contenedor, IDs de media ni errores de Meta. Facebook no fue modificado y `scheduled_publish_time` no fue utilizado.
- Se confirmó la exclusión de `260583 - Universe.png` por `ELIMINADA_MANUALMENTE`; no se requiere actualizar CSV ni estado local porque no hubo filas procesadas.

---

## [1.2.45] — 2026-08-15 (Manus)
### Scheduler por horarios exactos
- Se sustituyó la revisión periódica por una expresión cron limitada a los grupos horarios candidatos del 15–16: `0 0,30 11,14,17,20 15,16 8 *` en la zona del scheduler `America/Matamoros`, equivalente a los slots de `America/Mexico_City` por la diferencia horaria vigente.
- El runner filtra internamente la hora local exacta y solo publica dentro de una ventana de 8 minutos posteriores al slot; no recupera publicaciones atrasadas.
- La matriz cubre los cinco slots de Instagram aprobados: 15/08 10:00 y 13:30; 16/08 10:00, 16:00 y 19:00 de Ciudad de México.
- Se mantiene la exclusión de `260583`, la idempotencia, el límite de fechas y la protección de Facebook.

---

## [1.2.44] — 2026-08-15 (Manus)
### Optimización de frecuencia del scheduler Instagram
- La revisión se redujo de cada 5 minutos a cada 15 minutos para evitar ejecuciones innecesarias mientras se conserva un margen operativo razonable para este calendario de nueve slots.
- La tarea continúa activa, con expiración `2026-08-17T04:30:00Z`, y mantiene el filtro de fechas, la idempotencia y la exclusión de `260583`.

---

## [1.2.43] — 2026-08-15 (Manus)
### Scheduler temporal Instagram 15–16
- Se configuró una tarea recurrente autónoma `USM Instagram 15-16 Agosto`, con intervalo de 15 minutos y expiración `2026-08-17T04:30:00Z`.
- El ejecutor procesa únicamente filas `Facebook; Instagram selectivo` del calendario del 15–16, respetando `America/Mexico_City` y usando el flujo `media` → verificación → `media_publish`.
- `260583` quedó marcado `ELIMINADA_MANUALMENTE` después de que Fernando borrara la prueba; el runner no lo republicará.
- El scheduler no modifica Facebook, no usa `scheduled_publish_time` y conserva estados/errores para mantener idempotencia.
- Se añadieron `Operations/Production/run_instagram_15_16_scheduler.py` y `Operations/Production/instagram_15_16_scheduler_playbook.md`.

---

## [1.2.42] — 2026-08-15 (Manus)
### Prueba de programación futura Instagram
- Se probó mediante Graph API directa la primera publicación aprobada para Instagram: `2608030 - Universe - Que fibra tomas pa cagarla tanto.jpeg`.
- Se solicitó `scheduled_publish_time=1786982400`, correspondiente al 2026-08-17 a las 10:00 de Ciudad de México, en `POST /17841462696378190/media`.
- Meta respondió HTTP 400, código 3: `User must be on whitelist`.
- No se llamó a `media_publish`, no se creó un `IG_CONTAINER_ID` y no se publicó la imagen. El resultado demuestra que la publicación inmediata funciona, pero la ruta de programación futura probada no está habilitada para esta app/cuenta.
- La operación futura queda pendiente de un scheduler externo autorizado que ejecute `media_publish` en el momento del calendario, o de habilitar formalmente la capacidad de scheduling de Meta.

---

## [1.2.41] — 2026-08-15 (Manus)
### Prueba controlada Instagram
- Se publicó mediante Graph API directa el asset aprobado `260583 - Universe.png` en `@universe_sent_me_0326`.
- Creación de contenedor: `17976335523089880`; estado `FINISHED`.
- Publicación verificada: `18105410684129991`; permalink `https://www.instagram.com/p/DcDHxq5AMHh/`.
- La prueba demuestra que los permisos, la vinculación de la Página y el PPA permiten publicar en Instagram. El scheduler futuro queda como pendiente independiente: la API ejecutó publicación inmediata, no programación futura.
- El calendario del 15–16 fue actualizado con `IG_Container_ID`, `IG_Media_ID`, permalink y estado `PUBLICADA_PRUEBA` para esta fila.

---

## [1.2.40] — 2026-08-15 (Manus)
### Auditoría Instagram API
- Se auditó Instagram directamente mediante Meta Graph API v26.0, no mediante el conector MCP.
- La cuenta `@universe_sent_me_0326` (`17841462696378190`) está vinculada a la Página correcta (`1036844829507460`), responde HTTP 200 y devuelve media reciente.
- Los permisos `instagram_basic`, `instagram_content_publish` y `pages_read_engagement` están concedidos; la Página devuelve tareas `CREATE_CONTENT` y `MANAGE`.
- La cuota de publicación consultada es `0/100` contenedores en la ventana de 24 horas.
- El conector MCP desconectado no representa un fallo de Graph API. Instagram no quedó programado el 15–16 porque nunca se creó un contenedor ni se llamó a `media_publish`.
- Se añadió el informe permanente `Operations/Research/2026-08-15_Auditoria_API_Instagram.md` con el flujo correcto, el posible requisito PPA y el checklist para una primera prueba controlada.

---

## [1.2.39] — 2026-08-15 (Manus)
### Añadido y confirmado
- Se creó y validó la skill `usm-calendar-scheduler`, con el flujo simplificado para validar calendarios aprobados, derivar correctamente el Page Access Token, programar Facebook, verificar IDs, mover originales en Drive sin copias y registrar el resultado.
- La skill incluye una referencia técnica sobre la diferencia entre User ID y Page ID, el flujo `/photos` + `/feed` y el tratamiento separado de Instagram.
- Se confirmó que las publicaciones del 15–16 de agosto quedaron programadas únicamente en Facebook. Instagram no quedó programado: el conector estaba desconectado y no existe un registro de publicación o programación de Instagram para esas piezas.

---

## [1.2.38] — 2026-08-15 (Manus)
### Ejecutado y corregido
- Se auditó el token renovado: `pages_manage_posts` está concedido y la Página Universe Sent Me devuelve tareas `CREATE_CONTENT`, `MANAGE` y `MODERATE`.
- Se corrigió el diagnóstico inicial: `2920605591459033` es el ID del usuario `Fernando Gdlr`; la Página real es `1036844829507460`, derivada mediante `/me/accounts`. El error anterior sobre `publish_actions` fue causado por usar el ID de usuario en la ruta de Página.
- Se programaron **9 publicaciones de Facebook** para el 15–16 de agosto mediante carga temporal de foto y Page Feed programado. Meta devolvió `is_published=false` y se registraron los IDs en `Operations/Research/2026-08-15_Calendario_15_16_Agosto.csv`.
- Se movieron los **9 archivos originales** utilizados a `Humor existencial/08 Agosto` mediante cambio de carpeta, sin crear copias. La ubicación fue verificada por ID de Drive.
- Instagram no se ejecutó en esta operación; permanece como distribución selectiva pendiente de una orden específica de publicación/programación.

---

## [1.2.37] — 2026-08-15 (Manus)
### Corregido
- Se reemplazaron los hashtags provisionales del calendario `Operations/Research/2026-08-15_Calendario_15_16_Agosto.csv` y su versión Markdown por etiquetas del roster oficial de `GrowthOS/10_00_Kit_de_Hashtags_USM.md`.
- Se validó que no quedaran hashtags inventados ni nombres de personajes fuera del kit; Kael no recibe hashtag propio porque su identificador canónico aún no está confirmado.

---

## [1.2.36] — 2026-08-15 (Manus)
### Añadido
- Se registraron **38 imágenes nuevas** encontradas directamente en la raíz de `Humor existencial`; las carpetas mensuales quedaron excluidas por representar archivo histórico.
- Se creó `Operations/Research/2026-08-15_Inventario_Memes_Nuevos_Drive.md` y su CSV con referencias, personajes, enlaces y estado `Nuevo_Pendiente_Revision`.
- Se creó `Operations/Research/2026-08-15_Calendario_15_16_Agosto.md` y su CSV con **9 publicaciones pendientes de aprobación**: 5 nuevas y 4 reuse aprobados manualmente.
- La propuesta conserva el sábado en cuatro slots y el domingo como día estelar de cinco slots. No se generaron órdenes de publicación.

---

## [1.2.35] — 2026-08-14 (Manus)
### Cambiado
- La prueba `EXP-2026-08-CAL-01` se amplió de 68 a **74 slots**.
- De lunes a jueves se añadió la publicación de las **19:00**; viernes adopta el patrón de sábado con 10:00, 11:00, 13:30 y 19:00.
- El domingo conserva sus cinco horarios —10:00, 13:30, 16:00, 19:00 y 22:00— y queda formalmente definido como **día estelar**.
- La mezcla se actualizó a **46 piezas nuevas y 28 reuse**, aproximadamente 62%/38%. La frecuencia adicional se cubre con contenido nuevo, no con reuse extra.

---

## [1.2.34] — 2026-08-14 (Manus)
### Añadido
- Se creó `Operations/Research/2026-08-14_Propuesta_Calendario_17_30_Agosto_con_Copys.md` y su CSV ampliado con caption, variante de copy y decisión de Instagram para los 74 slots.
- Se creó `Operations/Research/2026-08-14_Recomendacion_Instagram_CGO.md`: la recomendación es cross-post selectivo, no duplicación masiva. Primera tanda sugerida: `260560`, `260625` y `260528`; `260539` y `humor4.16` quedan como pruebas orgánicas posteriores y de mayor riesgo de distribución.
- La cuenta de Instagram sigue con el conector no conectado; no se publicó ningún asset durante esta tarea.

---

## [1.2.33] — 2026-08-14 (Manus)
### Cambiado
- `260528 - Universe.png` se movió al domingo 30 de agosto a las 22:00.
- Se separaron los reuse consecutivos de los días 27 y 28 de agosto sin cambiar la mezcla 28/40.
- La revisión histórica de 508 publicaciones confirma una señal fuerte a favor de probar copys mínimos —uno o dos emojis—, pero también se registraron frases cortas y variantes conversacionales. La evidencia queda documentada en `Operations/Research/2026-08-14_Analisis_Copys_Rendimiento.md`.

---

## [1.2.32] — 2026-08-14 (Manus)
### Corregido
- Se corrigió la propuesta de calendario experimental después de detectar que se habían incluido 36 reuse en lugar de los 28 definidos por la proporción aprobada.
- La versión vigente conserva exactamente **28 reuse y 40 espacios para memes nuevos** en 68 slots.
- Los ocho assets aprobados manualmente quedan en la Reuse Queue como reserva y no se usan en esta primera prueba.

---

## [1.2.31] — 2026-08-14 (Manus)
### Añadido
- **Propuesta de calendario experimental 17–30 de agosto:** se creó `Operations/Research/2026-08-14_Propuesta_Calendario_17_30_Agosto.md` y su CSV operativo.
- La propuesta contiene 68 slots: 28 reuse del ranking principal y 40 espacios vacíos para memes nuevos que Fernando debe generar. Los ocho assets aprobados manualmente quedan como reserva.
- Se excluyeron los memes del Día de la Madre y se revisaron los slots para no colocar piezas de contexto romántico, nocturno o sexualizado como contenido de buenos días.
- El borrador no modifica el calendario histórico ni publica/mueve assets de Drive. La propuesta conserva la mezcla protocolaria 40/28; no modifica la proporción experimental aprobada.

---

## [1.2.30] — 2026-08-14 (Manus)
### Añadido
- **Archivado mensual de memes:** `My Drive/Universe sent me/USM/Humor existencial` queda definido como entrada operativa de memes nuevos. Después de confirmar una publicación real mediante el `ID_Meta`, el archivo se mueve a `Humor existencial/[Mes]` conservando su nombre y referencia.
- Los archivos programados pero no publicados permanecen en la raíz. Las carpetas mensuales representan historial organizado, mientras que las fechas y métricas oficiales siguen viniendo de Meta.
- La regla quedó documentada en `GrowthOS/01_03_Reuse_Queue.md` y `GrowthOS/13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md`.

---

## [1.2.29] — 2026-08-14 (Manus)
### Cambiado
- Fernando aprobó las ocho piezas sin match visual confirmado para integrarlas a la reutilización.
- El doble sentido y la sexualización quedan definidos como atributos editoriales válidos, no como motivos automáticos de descarte.
- Los cambios de personaje solo se propondrán por contradicción de canon o coherencia del personaje; no se eliminará el contexto sexualizado por defecto.
- La clasificación `Approved_User_Context` queda registrada en `Operations/Research/2026-08-14_Reuse_Mayo_Unmatched_Review.csv`.

---

## [1.2.28] — 2026-08-14 (Manus)
### Añadido
- **Cruce histórico de reuse mayo:** se extrajeron 205 publicaciones de Facebook de mayo y se cruzaron sus adjuntos con los 131 assets de imagen de la raíz de `05 Mayo`.
- Se confirmaron 123 assets únicos con historial visual y se generó `Operations/Research/2026-08-14_Reuse_Mayo_Ranking.csv` para seleccionar las 28 piezas reuse de la prueba.
- Se conservaron ocho assets sin match visual confirmado como `Sin_Historial_Visual_Confirmado`, no como piezas de bajo rendimiento.
- La Reuse Queue ahora enlaza el cruce bruto y el ranking individual.

---

## [1.2.27] — 2026-08-14 (Manus)
### Cambiado
- **Drive como fuente operativa de reuse:** Fernando reorganizó `05 Mayo` para separar la raíz de 133 assets candidatos de `Reutilizado Agosto` (21 imágenes) y `Reutilizado Juilo (menos de 30 dias)` (7 imágenes).
- La raíz de mayo se considera disponible bajo la confirmación operativa de que esas piezas no fueron publicadas en los últimos 30 días. La fecha individual de publicación original de mayo queda registrada como desconocida y no se inventará.
- La prueba de dos semanas puede seleccionar sus 28 reuse top principalmente desde la raíz de mayo; junio se usará selectivamente para introducir frescura.

---

## [1.2.26] — 2026-08-14 (Manus)
### Corregido
- **Corrección de inventario reuse mayo:** Fernando confirmó que `260516`, `260523`, `260574`, `260595`, `260596`, `260602`, `260610` y `260624` ya fueron publicados, incluso algunos el mismo día de la revisión. Estas piezas quedan excluidas de la prueba actual.
- Se corrigió el informe `Operations/Research/2026-08-14_Revision_Reuse_Mayo_Junio.md`: la muestra visual se considera evidencia de estilo, no disponibilidad; el inventario físico de Drive ya no se presenta como reserva elegible.
- El catálogo CSV ahora distingue `Published_Confirmed_User`, `Unverified` y `Pending_Historical_Check`.

---

## [1.2.25] — 2026-08-14 (Manus)
### Añadido
- **Revisión de reuse mayo-junio:** se creó `Operations/Research/2026-08-14_Revision_Reuse_Mayo_Junio.md` y su catálogo de datos. Se identificaron 167 imágenes en la carpeta `05 Mayo` y 197 en `06 Junio`, incluyendo una subcarpeta `Top` con 8 piezas curadas.
- Se recomienda pasar parcialmente a junio para aprovechar el conjunto `Top` y piezas más recientes, mientras se conserva mayo como reserva secundaria filtrada por rendimiento y saturación.
- Mayo no cubre por sí solo la necesidad de 28 piezas reuse top para la prueba de dos semanas con un nivel de confianza alto; la combinación de las 12 prioridades de mayo y los 8 top de junio ofrece una base inicial de 20 candidatos.
- No se eliminó ni modificó ningún archivo en Drive; la recomendación de descarte es únicamente para la exclusión temporal de la prueba.

---

## [1.2.24] — 2026-08-14 (Manus)
### Cambiado
- **Prueba de calendario actualizada por decisión de Fernando:** lunes a viernes mantiene 10:00, 11:00, 13:30, 16:00 y 17:00; sábado elimina 16:00 y mueve 17:00 a 19:00; domingo mueve 11:00 a 16:00 y conserva 19:00 y 22:00 como franjas nocturnas.
- **Mezcla experimental actualizada:** dos piezas reuse por cada tres piezas nuevas en días de cinco slots. El sábado, con cuatro slots, se asignan dos nuevas y dos reuse. El total de la prueba queda en 68 publicaciones: 40 nuevas y 28 reuse top.
- El calendario operativo `05_03_Calendario_10_16_Agosto.md` todavía no fue modificado; solo se actualizó el protocolo de prueba.

---

## [1.2.23] — 2026-08-14 (Manus)
### Añadido
- **Diseño de prueba de calendario de dos semanas:** se creó `Operations/Research/2026-08-14_Diseno_Prueba_Calendario_2_Semanas.md` para probar frecuencia, tipo de contenido y franjas horarias sin alterar aún el calendario vigente.
- La matriz base propone cinco publicaciones de Facebook por día: 10:00, 11:00, 13:30, 16:00 y 17:00 de lunes a sábado; los domingos cambia a 10:00, 11:00, 13:30, 19:00 y 22:00 para probar la hipótesis de tráfico nocturno dominical.
- La mezcla experimental propuesta es 80% contenido nuevo y 20% `Reuse_Top`, con Reels y carruseles fuera del cálculo principal.
- La producción documentada todavía no garantiza 56 piezas nuevas para 14 días; el protocolo incluye una variante de cuatro publicaciones diarias si Fernando no confirma capacidad suficiente.
- El calendario `05_03_Calendario_10_16_Agosto.md` no fue modificado.

---

## [1.2.22] — 2026-08-14 (Manus)
### Añadido
- **Comparativo junio–julio–agosto:** se creó `Operations/Research/2026-08-14_Comparativo_Desempeno_Junio_Julio_Agosto.md` y el snapshot de 508 publicaciones extraídas mediante Graph API.
- El análisis de los primeros 14 días muestra 9.50 publicaciones/día en junio, 6.71 en julio y 4.57 en agosto. Agosto cae frente a julio en interacciones totales por día y mediana por publicación, pero permanece por encima de junio por publicación.
- Se registraron `HB-004` sobre saturación de reuse y `HB-005` sobre superficie de descubrimiento/frecuencia. Ambas quedan `En prueba`; no se modificó el calendario.
- La teoría de que los huecos de publicación reducen oportunidades de descubrimiento es plausible, pero todavía no se prueba el mecanismo algorítmico ni la contribución incremental de cada post.

---

## [1.2.21] — 2026-08-14 (Manus)
### Añadido
- **Ciclo de aprendizaje de horarios:** se creó `Operations/Research/2026-08-14_Ciclo_Aprendizaje_Horarios.md` y su snapshot `2026-08-14_Ciclo_Aprendizaje_Horarios_Datos.csv` para reconstruir la razón del cambio de horarios del 10–16 de agosto.
- Se registró `HB-003` en `Integracion_Growth_OS.md`: la ampliación de franjas puede mejorar la interacción típica, pero queda `En prueba` porque el cambio de horarios ocurrió junto con cambios de contenido, personajes, días y proporción de reuse.
- La comparación inicial de Facebook, en zona horaria `America/Mexico_City`, muestra mediana de 26 interacciones en 33 publicaciones del 4–9 de agosto frente a 37 en 17 publicaciones del 10–14 de agosto. La señal es preliminar y no cierra causalidad.
- El calendario `05_03_Calendario_10_16_Agosto.md` no fue modificado.

---

## [1.2.20] — 2026-08-14 (Manus)
### Cambiado
- **Make retirado de la estrategia operativa:** la guía `02_00_Guia_Automatizacion_Make.md` pasa a `Archived`. La arquitectura, el documento puente, el índice, la cola de reuse y la cola de producción fueron actualizados para que Manus gestione la validación, programación, publicación y aprendizaje mediante Graph API de Meta.
- **Graph API validada con token temporal:** el token de usuario respondió HTTP 200 para identidad y permisos; Manus derivó en memoria el Page Access Token de Universe Sent Me y verificó identidad de Página, feed, publicaciones programadas, identidad de Instagram `@universe_sent_me_0326` y lectura de media, todos con HTTP 200.
- No se ejecutaron operaciones de escritura. La primera publicación real queda pendiente de una prueba explícita con un asset aprobado. Los tokens temporales deben renovarse cuando expiren.

---

## [1.2.19] — 2026-08-14 (Manus)
### Añadido
- **Auditoría del Growth OS:** se creó `Operations/Research/2026-08-14_Auditoria_Growth_OS.md` para evaluar la programación modificada, el estado de Make e Instagram, la trazabilidad hacia el pipeline CSV y el ciclo de aprendizaje post-publicación.
- Dictamen provisional: el sistema funciona parcialmente, pero no está validado de extremo a extremo. Make responde a nivel de identidad; Instagram está seleccionado como `@universe_sent_me_0326` pero el conector aparece no conectado; no se verificaron escenarios individuales ni ejecuciones; el `ExperimentLog` continúa vacío.
- Se documentaron inconsistencias de versión y slots en `05_03_Calendario_10_16_Agosto.md`, además de la falta de exportación CSV y correspondencia entre IDs `CNT-####` y códigos `260####`.
### Nota
- El calendario no fue modificado durante la auditoría. La revisión y corrección del calendario queda separada para una sesión posterior, después de validar integraciones y trazabilidad de publicación.

---

## [1.2.10] — 2026-08-12 (Claude)
### Añadido
- **`13_00_Pipeline_Publicacion_Local_y_Estandar_CSV.md`.** Fernando confirmó nuevos permisos de Meta API aprobados (`pages_manage_posts`, `instagram_content_publish`, `pages_read_engagement`, `read_audience_network_insights`, entre otros) que habilitan publicación automatizada real, no solo lectura. Reveló además que ya tiene un pipeline propio funcional (script en PyCharm, usando Gemini, publicando vía Meta Graph API) que consume un spreadsheet de 8 columnas (`Fecha_Programada`, `Hora`, `Marca`, `Categoria`, `Archivo`, `Ruta_Completa`, `Caption`, `Estado`) — Facebook integrado y en uso real; Instagram pendiente de integrar, sin columna de plataforma todavía. El pipeline es **multi-marca** (ejemplos vistos de otro proyecto de Fernando, "Quirelli"/"Flexi", no de USM). `Archivo` (solo filename) y `Ruta_Completa` (ruta local absoluta en Drive sincronizado) son columnas separadas.
### Nota
- Documento deja explícito que, de ahora en más, cualquier calendario "listo para publicar" debe ser exportable a esta estructura de 8 columnas, no solo entregarse como tabla markdown de planeación — y que los nombres de archivo usados en cualquier calendario deben coincidir exactamente con los nombres reales en la carpeta local de Fernando.
- Quedan 5 puntos pendientes de definición explícitos en la sección 4 del documento (valor de `Marca` para USM, valores de `Estado`, mapeo de `Categoria` para contenido de memes/reels vs. e-commerce, manejo multi-plataforma, validación pre-publicación) — no se resolvieron en esta sesión, solo se registró lo confirmado.

---

## [1.2.11] — 2026-08-14 (Manus)
### Añadido
- **CNT-027 — Meme Fantasma "Ghosting eterno":** propuesta derivada de la revisión de la carpeta de Google Drive "Universe Sent Me > Ideas > Memes" (solicitada por Fernando). De las ~19 semillas de referencia se identificaron 4 patrones (espera eterna resignada, autodesprecio con punchline seco, ternura interactiva, agotamiento social); la propuesta combina los dos primeros con el Fantasma y un giro moderno (mensajes sin leer/ghosting). Copy: "Hace 400 años que no me contestan un mensaje. Ahora le dicen ghosting. Yo solo lo llamaba martes." Score **9.10/10 PASS** verificado por `scripts/score_proposal.py`. Slot sugerido 4:00–5:00 PM, base visual del asset 2K existente del proyecto. Canon-safe: el arco del Fantasma no se resuelve.

---

## [1.2.15] — 2026-08-14 (Manus)
### Añadido
- **CNT-030 — Música del reel CNT-029:** pista original de IA generada para el reel de los sueños de Universe (92 BPM, Do mayor, instrumental; corte de 20 s con fade y arco tierno→cómico→remate que replica la estructura del reel). Se documentó además el benchmark de audios en tendencia de agosto-2026 (Sweetly de jkl — 26K posts, apto business — como referencia principal; alternativas In & Out, Sometimes, Summer Vibes; August de Taylor Swift descartado por cuenta business). Hipótesis experimental registrada: trending da +alcance inicial; audio propio da libertad editorial y cero riesgo de copyright. Assets en archivos compartidos: `14_Musica_Reel_suenos_pista_original.mp3` y `15_Musica_Reel_suenos_corte_20s.mp3`.

---

## [1.2.16] — 2026-08-14 (Manus)
### Cambiado
- **CNT-030 v2.0 — corrección de concepto del reel:** Fernando aclaró la dirección real: el reel es un **scroll ultra rápido (~0.5–1 s por cuadro) con gancho de pausa** (el texto de cada sueño no alcanza a leerse y eso obliga a pausar el video), con audio de **rock con actitud estilo Måneskin**, no un montaje tierno lento. CNT-030 se reescribió completo (montaje, referencias de audio: versiones trending de Måneskin en la app, Bed On Fire — G Flip, Beat It, She Wolf — Shakira; registro de que no se genera audio por IA sin petición explícita; la pista v1.0 pasa a fallback). El guion de CNT-029 se reemplazó (sección 3b conserva el guion v1.0 como histórico). Lección de proceso: validar el concepto de montaje (ritmo + gancho + rol del audio) con Fernando antes de producir audio/montaje.

---

## [1.2.14] — 2026-08-14 (Manus)
### Añadido
- **CNT-029 — Reel "Pausa para ver qué piensa de ti":** a solicitud de Fernando, se generaron 5 imágenes para completar su reel de 6 cuadros (su imagen base + las 5 generadas), con composición idéntica —Universe en la nube con globo de pensamiento sobre el cielo pastel— donde solo cambia el sueño dentro del globo: falda (base de Fernando), piernas, pecho, cena romántica, lluvia con cacao y atardecer con lentes oscuros (cierre cómico). La frase del reel va como superposición de video, no incrustada en las imágenes. Rasgos de Universe respetados (gafas steampunk, asset 3) y estilo de animación idéntico al de la base. La figura femenina es genérica (Capa 1, sin vínculo canon fijado); si se la identifique con un personaje nombrado requiere validación explícita dado que Maeve/Kael aún no tienen asset oficial. Assets: `06_Reel_...` a `10_Reel_...` en archivos compartidos del proyecto.

---

## [1.2.13] — 2026-08-14 (Manus)
### Cambiado
- **CNT-028 v2.0 — corrección de identidad visual:** Fernando rechazó la v1 del banco de memes adaptados por alterar los rasgos físicos y el estilo de animación de los personajes. Se regeneraron las 5 imágenes usando exclusivamente los assets oficiales del proyecto como referencia: Fantasma (sábana blanca con gafas oscuras, asset 8), Universe (gato blanco con gafas steampunk doradas con engranajes, asset 3), Silvio (pelo morado, nariz roja, golilla, sonrisa cómplice + ceja levantada, asset 7) y Wilfred (asset 4). M2 (Kael+Maeve) se mantiene como diseño pendiente de validación: estos personajes no tienen asset oficial en el proyecto. Consecuencia de sistema: **regla dura nº 5 añadida al `03_00`** — identidad física y estilo de animación no negociables; para personajes sin asset oficial, validación explícita de Fernando antes de publicar. CNT028 sube a v2.0 y `03_00` a v2.2.

---

## [1.2.12] — 2026-08-14 (Manus)
### Añadido
- **CNT-028 — Banco de 5 memes adaptados de Drive (modo "adaptado") (v1.0):** a solicitud de Fernando, se seleccionaron 5 memes con frase en español de la carpeta Drive Ideas-Memes y se recrearon con personajes y escenarios USM: M1 Fantasma "¿Qué vendrá primero mi boda o Jesús?", M2 Kael+Maeve "Tu soltera y yo soltero... (Que nadie nos soporta)", M3 Silvio "Mira, te llama tu mamá, corre", M4 Wilfred "Y que estabas haciendo que no respondías / Yo:... Ver más", M5 Universe "Lo bueno del amor es que / si eres un buen observador / lo verás en todos lados". Reglas aplicadas: frase original intacta palabra por palabra (verificada), marca "UniverseSentMe" discreta en imagen, y **modo adaptado** formalizado en `03_00` como segundo modo de producción junto al modo estándar (frase en copy). Se descartaron 3 referencias de Drive: WhatsApp con insultos (tonalidad incompatible con "ácido ≠ insulto"), axolotl con vulgaridad y autoría ajena identificada (riesgo de reporte/crédito), y memes sin frase en español. Registro de descarte documentado en CNT028 para trazabilidad.

---

## [1.2.9] — 2026-08-12 (Manus)
### Añadido
- **CNT-026 — Banco de memes fin de semana 16–17 de agosto:** 5 propuestas (Fantasma "El que más aguanta el grupo" 9.15, Pareja Kael+Maeve 9.05, Universe "Señales del fin de semana" 8.95, Wilfred "Fin de semana no es descanso" 8.75, Fantasma minimalista 🫥 8.60), todas con score ≥ 8.5 verificado por `scripts/score_proposal.py`. Registradas en `../Operations/Production/CNT026_Memes_FinDeSemana_16_17_Ago.md`. Nota: el ID original CNT-025 ya estaba asignado a los Experimentos Growth OS (tests A/B), por lo que este banco tomó el siguiente ID libre. Explota las hipótesis H11 (minimalismo = shares), H13 (ácido = shares desproporcionados) y H14 (pareja = shares etiquetables) del ciclo diario del 8 de agosto. Tras las promociones de canon de junio ([1.2.8]), el changelog del banco registra a "Kael+Maeve" como pareja — se actualizará la pieza M3 de CNT-026 para usar `#KaelUSM` en lugar de `#ChicoDeLosPantalonesUSM` (actualización pendiente, ver documento CNT026).

---

## [1.2.8] — 2026-08-10 (Claude)
### Añadido
- **Segunda ronda de promociones meme→canon**, a partir de análisis visual de junio 2026 (screenshots de Meta Business Suite provistos por Fernando, no solo datos de Windsor.ai):
  1. **Universe (ampliación):** el registro sarcástico ya promovido ([1.2.7]) se confirma también en formato cinemático/composición elaborada, no solo minimalista. Evidencia: "yo Aura Fuerte" con 110,510 visualizaciones — el pico más alto registrado en todo el análisis de junio. Commit `universe-sent-me-1@b52ea42`.
  2. **Kael y Maeve:** primera creación formal de canon para ambos (nombres ya aprobados por Fernando en sesiones previas, sin ficha hasta ahora). Ubicados en Segundo Círculo — máscara todavía en formación, evidenciado por su contenido de fricción cotidiana resuelta en humor/ternura, no una dinámica ya consolidada. Se confirma también su relación de pareja establecida (novios), con evidencia de rendimiento fuerte y repetido en junio 2026. Commit `universe-sent-me-1@a994354`.
- Log de promociones (`12_00...`, sección 4.5) actualizado con las 3 entradas nuevas; versión del documento subida a 1.3.
### Nota
- Esta ronda usó una fuente de evidencia distinta a la primera: capturas reales de Meta Business Suite (visualizaciones, interacción, % seguidores vs. no seguidores, edad/sexo de audiencia) en vez de solo datos agregados de Windsor.ai — mucho más rica para detectar patrones por personaje específico, ya que incluye la imagen real de cada post.
- Confirma con fuerza estadística la tesis de Fernando sobre las dos capas: todas las piezas de alto rendimiento de este lote tienen % de seguidores entre 0.2% y 3.3% — este contenido opera casi enteramente sobre la órbita de no-seguidores vía algoritmo, no sobre fidelización.

---

## [1.2.7] — 2026-08-10 (Claude)
### Añadido
- **Primera promoción real meme→canon** bajo el sistema de dos capas (`12_00_Sistema_Dos_Capas_Contenido_Canon.md`, sección 4). Personaje: Universe. Patrón: registro sarcástico/cortante en formato meme corto, detectado en 3+ piezas de junio-agosto 2026 con rendimiento consistentemente alto (imágenes de junio revisadas visualmente por Fernando en esta sesión, más el post "😒" de agosto ya documentado en el reporte mensual junio-julio).
- Claude alertó el patrón (mecanismo de la sección 4.2); Fernando confirmó la promoción y especificó que es un registro adicional, no un reemplazo del Universe observador/curioso ya cerrado en canon, y que debía vivir como nota dentro de la ficha ya existente, no como documento nuevo.
- Cambio aplicado en el repo `universe-sent-me-1`: `02 Personajes/Primer Círculo/Universe/03 Reglas de diseño.md`, v1.3→v1.4, commit `e8b6f22`. Nueva sección "Registro sarcástico (formato meme)", anclada explícitamente al Anti-tono ya cerrado (autoafirmación despreocupada, nunca desprecio a otros — "se ríe con, no de").
### Nota
- Durante la revisión de junio, Fernando compartió también contenido publicado en un grupo externo de Facebook ("Polvo de estrellas") con nivel de explicitud mayor al de la página propia — se documentó por separado en la sección 8 del mismo sistema de dos capas (ver [1.2.6.1] más abajo si aplica, o revisar historial de commits de esa fecha), sin mezclarse con esta promoción de canon.

---

## [1.2.6] — 2026-08-10 (Claude)
### Añadido
- **Sistema de Dos Capas:** `12_00_Sistema_Dos_Capas_Contenido_Canon.md`. Formaliza dirección estratégica de Fernando: separa la capa de memes/reels (libre, orientada a algoritmo y audiencia amplia no-seguidora) de la capa de canon (Biblia, decisiones permanentes). Margen amplio confirmado para todos los personajes sin distinción de círculo — los memes son proceso de descubrimiento tanto para elenco nuevo como establecido. Define 3 límites duros que aplican incluso en capa libre (identidad física fija, vínculos que comprometan narrativa futura, Gramática Emocional Invisible). Formaliza mecanismo de promoción deliberada meme→canon: Claude alerta cuando un patrón cruza umbral (3+ piezas/30 días con rendimiento consistente), Fernando decide, nunca automático.
### Nota
- Documenta explícitamente que `Canon_Contradictions_Report.md` aplica solo a narrativa seria (historias/episodios), nunca a memes sueltos — 3 de sus 5 contradicciones históricas resultaron ser falta de registro formal de nombres (Silvio/Maeve/Kiri), no errores de contenido, evidencia que motivó esta separación.
- Sección 5 deja abierto un futuro registro cualitativo de insights de comunidad (comentarios con historias personales/puntos de vista) — pendiente de primer uso real, sin ejemplo generado en esta sesión.

---

## [1.2.5] — 2026-08-10 (Claude)
### Añadido
- **Calendario 10-16 agosto:** `05_03_Calendario_10_16_Agosto.md`. Cambio de estrategia por instrucción de Fernando: reduce proporción de reuse a máximo 1 pieza/día (solo "top" ya validados por datos), prioriza 14 piezas nuevas de personajes del elenco extendido (Maeve, Kael, Silvio, Evan, Kiri, Elara, Universe). Horarios elegidos por análisis de mediana horaria/diaria sobre 99 posts reales (Windsor.ai, julio), no por suposición. Reels diarios quedan como TBD — Fernando define contenido día a día.
### Nota
- Fernando indicó que varias de las 14 piezas nuevas no pasaron revisión formal de canon y pidió posponer esa revisión a sesión dedicada — documentado explícitamente en el nuevo calendario, sección 8 (pendientes). También mencionó estar considerando invertir el flujo canon→contenido (que los datos de rendimiento de memes informen la Biblia); queda registrado como dirección en discusión, no como cambio de proceso implementado.
- `05_02_Calendario_04_09_Agosto.md` marcado como Superseded en el índice (semana ya cerrada).

---

## [1.2.4] — 2026-08-08 (Claude)
### Añadido
- **Reporte mensual Junio-Julio 2026:** `../Operations/Research/2026-08-08_Reporte_Mensual_Junio_Julio_2026.md`. Cierra el vacío de datos entre el reporte de mayo (`mayo_2026_top_posts_metaBS.md`) y el análisis de 28 días de agosto (`agosto_2026_analisis_28_dias.md`). 61 días cubiertos vía Windsor.ai (`facebook_organic`), métrica de reacciones+comentarios+shares (misma metodología que el ciclo diario de agosto, ya que alcance/impresiones está deprecado). Julio creció +269% en interacciones totales vs. junio. Confirma con datos propios tres posts ya listados por alcance en `08_00_Metricas_Baseline_Plataformas.md` (21 jul, 28 jul, 24 jul), subiendo la confianza del patrón minimalista de "hipótesis reciente" a "tendencia de 3 meses".

---

## [1.2.3] — 2026-08-08
### Añadido
- **Ciclo diario de métricas 24h (Manus CGO, rutina programada):** primer ciclo automatizado registrado en `../Operations/Research/2026-08-08_Ciclo_Diario_Metricas_24h.md`. 6 posts FB en 24h (128 interacciones, 23 shares). Post top: Fantasma minimalista 👻 (42 reacciones, 11 shares). Hipótesis nuevas H11-H14 registradas en el Sheet "USM Growth OS".
### Corregido
- **Limitación de API:** las métricas de alcance/impresiones (`post_impressions`, `page_impressions`, etc.) están deprecadas en Graph API v21.0 para la página; el ciclo usa conteos de objeto (`reactions.summary`, `comments.summary`, `shares`) como workaround validado y propone `shares/interacciones ≥ 0.25` como proxy provisional de viralidad.
- **Instagram:** la vinculación del conector se cambió de @firmabordados a @universe_sent_me_0326; el conector aún reporta "not connected" y requiere re-autorización en la interfaz de Manus.
---

## [1.2.4] — 2026-08-09
### Añadido
- **CNT-026 — Banco de memes fin de semana 16–17 de agosto:** 5 propuestas (Fantasma "El que más aguanta el grupo" 9.15, Pareja Maeve 9.05, Universe "Señales del fin de semana" 8.95, Wilfred "Fin de semana no es descanso" 8.75, Fantasma minimalista 🫥 8.60), todas con score ≥ 8.5 verificado por `scripts/score_proposal.py`. Registradas en `../Operations/Production/CNT026_Memes_FinDeSemana_16_17_Ago.md`. El ID original CNT-025 ya estaba asignado a los Experimentos Growth OS (tests A/B), por lo que este banco tomó el siguiente ID libre. Explota las hipótesis H11 (minimalismo = shares), H13 (ácido = shares desproporcionados) y H14 (pareja = shares etiquetables) del ciclo diario del 8 de agosto.

---

## [1.2.2] — 2026-08-07
### Corregido
- **Reestructuración del Catálogo de Productos:** `12_00_Catalogo_Productos_MercadoLibre.md` pasa a versión 2.0 con enfoque "Historia → Personaje → Producto" en lugar de "Personaje → Producto". Se eliminaron productos genéricos (audífonos, organizadores, cámara WiFi) que no conectan con la identidad de la página. Se reemplazaron las tiras LED RGB de Silvio por productos de caos visual (máquina de humo, bola disco, máscara LED, máquina de burbujas). Se agregaron pools de productos por personaje (Wilfred, Elara, Universe, Fantasma, Kiri, Silvio).

---

## [1.2.1] — 2026-08-06
### Corregido
- **Actualización de Tendencias:** El catálogo de productos (`12_00_Catalogo_Productos_MercadoLibre.md`) se basaba en datos de tendencias de enero 2026. Se ha actualizado la referencia para reflejar las tendencias actuales de Q3 2026 (agosto), validando que la mayoría de los productos seleccionados (como el Proyector LED Galaxia) siguen siendo virales y pertinentes para la temporada.

---

## [1.2.0] — 2026-08-05
### Añadido
- **Integración de Monetización:** Creación de la estrategia de Mercado Libre Afiliados (`11_00_Estrategia_Monetizacion_MercadoLibre.md`).
- **Sección Story-Commerce:** Activación del formato "¿Qué me llegó?" en el Content Backlog (`CNT-023`).
- **KPIs de Afiliados:** Incorporación de métricas de conversión y clics en `08_00_Metricas_Baseline_Plataformas.md`.
- **Este Changelog:** Creación de `00_01_Changelog_GrowthOS.md` para gestión de contexto.

### Actualizado
- **Calendario Editorial:** Añadido calendario oficial 4-9 de agosto validado por Fernando.
- **Reportes de Análisis:** Actualización de reportes de agosto con datos de Top Memes y métricas de Facebook.

---

## [1.1.1] — Corrección y contexto de canon faltante (Claude, 2026-08-05)

### Corregido
- Fecha real de desbloqueo de Silvio y Kiri: **2026-08-03**, no 08-04. Ver commits `f7bebca` y `8e9fe9a` en el repositorio de canon (`universe-sent-me-1`).

### Añadido — hitos de canon no reflejados antes en este changelog
Este changelog vive en Growth OS, pero varios de los hitos de esta semana ocurrieron en el repositorio de canon (`universe-sent-me-1`), donde Manus tiene solo lectura. Se registran aquí para que ningún agente tenga que adivinarlos:

- **Silvio (El Payaso):** su primer reference sheet usaba el arquetipo del "payaso triste" clásico (lágrimas pintadas, mueca de tristeza), lo cual contradecía la regla de diseño ya cerrada. Fernando aprobó un diseño corregido (sonrisa cómplice, ceja levantada) — **ese es el único diseño válido para producción.** Corolario visual documentado en `02 Personajes/Primer Círculo/Payaso/03 Reglas de diseño.md` (canon, commit `8e9fe9a`).
- **Kiri (El Hada):** además del nombre, se confirmó una varita como objeto personal (canon, `00 Resumen.md` de Hada, commit `990a69c`). Su función narrativa todavía no se ha desarrollado.
- **Dos lugares nuevos, ambos en estado PROPUESTA (no CANON todavía):**
  - `La Hoguera.md` — punto de encuentro cercano a la ciudad, de escala íntima a grupal, posible entrada al Bosque.
  - `La Ciudad.md` — ficha deliberadamente incompleta. Confirmado: dirección visual (arquitectura arena/terracota) y una criatura gigante en el cielo, sin historia todavía, vista con naturalidad, sin interacción de ningún personaje — es una restricción narrativa activa, no un vacío a llenar.
- **Maeve (Chica del Suéter):** su diseño está confirmado y aprobado (carpeta Drive revisada), pero **todavía no tiene commit formal en el repo de canon** — a diferencia de Kiri y Silvio, que ya están cerrados. Tratar como "aprobado por Fernando, pendiente de registro en Biblia" hasta nuevo aviso.

---

## [1.1.0] — 2026-08-04
### Añadido
- **Kit de Hashtags USM:** Creación de `10_00_Kit_de_Hashtags_USM.md` para estandarizar etiquetas.
- **Desbloqueo de Personajes:** Desbloqueo operativo de Silvio y Kiri tras validación de canon.

### Corregido
- **Corrección de Identidad:** Ajuste de tags Maeve/MaeveUSM y LoresUSM para consistencia con publicaciones previas.

---

## [1.0.0] — 2026-08-03
### Añadido
- **Estándar de Documentación:** Formalización de `09_00_Estandar_Documentacion_Interna.md`.
- **Métricas Baseline:** Integración de datos reales de Windsor.ai para FB e IG.
- **Arquitectura CGO v3.0:** Implementación de la máquina de estados de contenido y colas de producción.

### Corregido
- **Ajuste de Canon:** Corrección masiva (6 archivos) sobre la "inmovilidad" del Fantasma; aclarado como bloqueo emocional, no físico.

---

## [0.9.0] — 2026-08-01 a 2026-08-02
### Añadido
- **Registro Maestro de Reels:** Creación de `07_00_Registro_Maestro_Reels.md`.
- **Auditoría Higgsfield:** Documentación para la candidatura al Filmmaker Grant.
- **Blueprint de Producción:** Storyboard y guion para el Showreel de USM.

---

## Guía para Agentes (Instrucción de Lectura)
Al iniciar una nueva sesión o tarea, los agentes deben:
1. Leer `00_01_Changelog_GrowthOS.md` para identificar cambios desde su última interacción.
2. Verificar el `00_Índice.md` para ubicar nuevos documentos mencionados en el changelog.
3. No proponer cambios que contradigan hitos marcados como "Active" o "Canon" en este registro.
4. Recordar que este changelog vive en Growth OS, pero puede registrar hitos ocurridos en el repositorio de canon (`universe-sent-me-1`) cuando afectan la producción — Manus tiene acceso de solo lectura ahí y debe confiar en lo que Claude/Fernando documenten aquí sobre ese repositorio, sin asumir que un silencio significa que no hubo cambios.

- **[2.11.01] — 2026-08-18 (Manus): Revisión independiente de atención comunitaria 15–18 agosto.** Se consultaron en modo lectura las publicaciones recientes y sus comentarios anidados mediante el token de página derivado de Meta. Se confirmó que Fernando ya respondió comentarios de "Mmmm, pensé que era otra cosa", "No sólo te enamoras de personas", "Mi elfa hermosa", el hilo sexualizado y el hilo de "Jesús". La bandeja pendiente se reduce a tres propuestas: `122151374157072582_2093067344913171`, `122151374157072582_1577015310481547` y `122151373833072582_1715141313071482`. No se publicaron respuestas ni se modificó Facebook. Auditoría actualizada a v1.6.

- **[2.11.02] — 2026-08-18 (Manus): Respuestas comunitarias aprobadas y regla de estilo refinada.** Fernando aprobó tres respuestas para los comentarios `122151374217072582_2093067344913171`, `122151374217072582_1577015310481547` y `122151373833072582_1715141313071482`: “Y nosotros aquí fingiendo que no nos dimos cuenta. 🤭”, “Lo sospechábamos, pero gracias por confirmar. 😌” y “Eso no es chisme, es investigación de campo… con excelente memoria. 🔥”. Quedaron registradas como aprobadas y pendientes de publicación; no se escribió en Meta. Se añadió la regla de que los personajes son condimento, no requisito, en respuestas comunitarias.

- **[2.11.03] — 2026-08-18 (Manus): Publicación verificada de tres respuestas comunitarias.** Tras confirmación explícita de Fernando, Meta aceptó las respuestas para `122151374217072582_2093067344913171`, `122151374217072582_1577015310481547` y `122151373833072582_1715141313071482`. IDs devueltos: `122151374217072582_2435856813608994`, `122151374217072582_1830912011221593` y `122151373833072582_1625579462232436`. El ledger pasa las tres filas a `Respondido`; no hubo otras acciones de moderación.

- **[2.11.04] — 2026-08-18 (Manus): Revisión comunitaria de hoy.** La nueva publicación de las 21:00 UTC no tenía comentarios. Se detectó un único comentario cualitativo no registrado previamente (`122151374217072582_1811120803575478`) en el post `122151374217072582`: crítica interpretativa ambigua, sin amenaza ni insulto directo. Se registró como `Pendiente_Fernando`, sin moderación automática ni respuesta publicada. No se detectaron casos de abuso, amenaza u ocultamiento.

- **[2.11.05] — 2026-08-18 (Manus): Respuesta seleccionada para abrir contexto narrativo.** Fernando eligió la propuesta “Momento… ¿cómo que soundtrack, villanos y santos? 👀 Necesitamos el episodio anterior.” para el comentario `122151374217072582_1811120803575478`. La respuesta queda pendiente de aprobación final/publicación; el aprendizaje es usar comentarios con drama implícito como puertas de entrada a una segunda ronda de conversación.

- **[2.11.06] — 2026-08-18 (Manus): Publicación de respuesta de contexto y revisión posterior.** Se publicó y verificó la respuesta “Momento… ¿cómo que soundtrack, villanos y santos? 👀 Necesitamos el episodio anterior.” para `122151374217072582_1811120803575478`; Meta devolvió `122151374217072582_1786534689428464` a las 22:56:57 UTC. El autor original todavía no había respondido. La revisión posterior encontró únicamente un comentario vacío (`122151374367072582_1377072351216209`), clasificado como `No_Requiere_Respuesta`; no hubo casos de moderación.

- **[2.11.07] — 2026-08-18 (Manus): Segunda revisión del hilo del chisme.** El autor original no respondió a la invitación de contexto. Se detectaron dos comentarios nuevos de baja prioridad —“ya casi llegas, confía 👁️‍🗨️🫩” y “x2”— y un comentario vacío; todos quedaron como `No_Requiere_Respuesta`. No hubo nuevos casos de moderación.

- **[2.11.08] — 2026-08-18 (Manus): Publicación verificada de respuesta de apoyo.** Se publicó “Ya casi, ya casi… no me desconcentres. 😭👀🫩” en el comentario `122151374289072582_1362274622770602`; Meta devolvió `122151374289072582_1753493165792345` a las 23:17:38 UTC. El ledger pasa la interacción a `Respondido`; no hubo otras acciones de moderación.

- **[2.11.09] — 2026-08-19 (Manus): Cierre provisional del ciclo P0.** Se confirmó que el alcance oficial es el lote de cinco publicaciones del 17 de agosto, no el lote operativo de nueve publicaciones del 15–16. La consulta directa de Meta observó 578 reacciones, 10 comentarios, 197 compartidos y 785 interacciones acumuladas. `2608028` concentró 636/785 interacciones observadas. El veredicto queda `Cerrada_con_limitacion`: aprendizaje editorial utilizable, pero sin snapshots exactos 24/72h porque Meta entregó acumulados lifetime. Se añadió `P0-CLOSE-2026-08-19` al ExperimentLog.

- **[2.11.10] — 2026-08-19 (Manus): Análisis detallado de 2608028.** El asset concentró 636/785 interacciones observadas (81.0%), 462/578 reacciones (79.9%) y 172/197 compartidos (87.3%). La ventaja se concentra en reacciones y compartidos, no en volumen de comentarios. El análisis visual identifica personaje reconocible, atractivo fantástico, secuencia de tres momentos, frase universal y caption mínimo. Se recomienda replicar la estructura como hipótesis en 2–3 piezas de la siguiente ola, mantener controles diversos y no convertir el resultado en regla de horario o canon editorial.

- **[2.11.11] — 2026-08-20 (Manus): Revisión de comentarios sin responder.** En el corte 19–20 de agosto se detectaron dos comentarios pendientes en la publicación `122151374823072582`: “Estás alrevesado” y “Ay por Dios es al revés”. Ambos parecen señalar que el asset está invertido; se deben revisar como un solo hilo antes de responder. Las reacciones con emojis no requieren intervención y los comentarios con respuesta de la página no se marcaron como pendientes.

- **[2.11.12] — 2026-08-20 (Manus): Corrección de clasificación del remate visual.** Fernando aclaró que “Estás alrevesado” y “Ay por Dios es al revés” son dos intervenciones independientes sobre el remate visual, no un único hilo ni una acusación necesariamente dirigida al asset completo. La bandeja y la auditoría quedan corregidas; se prepararán respuestas separadas.

- **[2.11.13] — 2026-08-20 (Manus): Aprobación de una sola respuesta sobre el remate visual.** Fernando aprobó únicamente “Sí… pero ya que lo hicimos al revés, vamos a fingir que era parte del concepto. 😂👀” para `122151374823072582_899916076126399`. El segundo comentario (`122151374823072582_2572609183253364`) queda sin respuesta; ninguna publicación se ha realizado.

- **[2.11.14] — 2026-08-20 (Manus): Publicación verificada de dos respuestas sobre el remate visual.** Se publicaron “Sí… pero ya que lo hicimos al revés, vamos a fingir que era parte del concepto. 😂👀” (`122151374823072582_904578688978118`) y “¡Exacto! El remate venía con giro incluido. 😂🫠” (`122151374823072582_942838658075352`). Meta verificó ambas a las 01:47:28 y 01:47:33 UTC; el ledger pasa ambas filas a `Respondido`.

- **[2.11.15] — 2026-08-20 (Manus): Actualización de pendientes estadísticos.** La auditoría integral queda corregida: P0 ya tiene cierre provisional basado en 785 interacciones observadas, con limitación por ausencia de snapshots exactos 24/72h. El siguiente análisis estadístico prioritario es la cohorte separada de nueve publicaciones del 15–16 (`CNT-031`–`CNT-039`); no se debe mezclar con P0 ni convertir el outlier `2608028` en regla general.

- **[2.11.16] — 2026-08-20 (Manus): Análisis de cohorte 15–16 y comparación robusta con P0.** Las nueve publicaciones registraron 747 interacciones observadas, media 83 y mediana 56. Las franjas de 19:00 y 10:00 fueron las más fuertes en esta cohorte, pero con muestras pequeñas. `CNT-034 / 260539 - Evan+Kiri.png` lideró con 227 interacciones. P0 promedió 157 por post por efecto de `2608028`; sin ese outlier, las otras cuatro piezas promediaron 37.25. La recomendación es priorizar pruebas en 19:00 y 10:00, conservar controles y no inferir causalidad de horario sin más observaciones.

- **[2.11.17] — 2026-08-20 (Manus): Comparación CNT-034/CNT-038 y corte de ola 17–30.** En la misma franja de 19:00, CNT-034 obtuvo 227 interacciones frente a 37 de CNT-038, 6.14 veces más; las diferencias visuales priorizadas son estructura de dos paneles, reacción facial visible, fantasía romántica universal y mayor compartibilidad frente a una escena única y un remate sexual más nicho. El corte real 17–30, excluyendo P0, contiene 14 publicaciones hasta el 19 de agosto, 731 interacciones observadas y un nuevo outlier `2608029` con 335 interacciones.

- **[2.11.18] — 2026-08-20 (Manus): Corrección de formato en corte 17–30.** El corte detectó 14 publicaciones no-P0, pero solo 13 devolvieron métricas de imagen interpretables; un reel devolvió ceros en los campos consultados y queda pendiente de métricas específicas de video. Los 731 acumulados corresponden únicamente a las 13 publicaciones con datos interpretables.

- **[2.11.19] — 2026-08-20 (Manus): Desglose del outlier 2608029.** La pieza de Wilfred obtuvo 335 interacciones, 231 reacciones, 4 comentarios y 100 compartidos; concentró 45.8% de las interacciones y 58.8% de los compartidos de la cohorte no-P0. Frente a las otras 12 piezas, multiplicó por 10.15 la media. Las hipótesis priorizadas son gancho coloquial con aclaración inesperada, fantasía cotidiana deseable, personaje reconocible, escenario rico y remate fácil de compartir; no se convierte el horario de las 19:00 en regla causal.

- **[2.11.20] — 2026-08-20 (Manus): Lineamientos prácticos de copy para P1.** Se actualizó `06_00_Reglas_Aprendizaje_Tendencias.md` a v3.8 con estructuras de copy derivadas de CNT-034 y 2608029, tratamientos `caption_minimo`, `caption_refuerzo` y `caption_conversacional`, reglas de emojis/hashtags, control de calidad y campos de instrumentación para validar compartibilidad sin canonizar un horario o formato por outliers.

- **[2.11.21] — 2026-08-20 (Manus): Mapa de pendientes fuera de comunidad.** Activos: continuar cortes estadísticos de la ola 17–30 con métricas específicas de video para el reel pendiente; preparar la siguiente ola P1 aplicando los lineamientos de copy y la instrumentación antes de publicar; completar después la reconciliación de inventario/filename y la consolidación de duplicados históricos. Pausados: scheduler automático de Instagram, piloto de afiliados de Mercado Libre y desarrollo de CNT-004.

- **[2.11.22] — 2026-08-20 (Manus): Corrección de estado de monetización afiliada.** La línea de pendientes `[2.11.21]` contenía un estado obsoleto: Mercado Libre **no está pausado**. El piloto está activo con diez links afiliados granulares; Fernando confirmó que los diez productos/links fueron publicados o adjuntados en Facebook. Se actualizaron `Operations/Research/Affiliate_Link_Ledger.csv`, `Operations/Research/Affiliate_Pilot_Assignments.csv`, `Operations/Production/2026-08-19_Playbook_Tracking_Afiliados_MercadoLibre.md` y `Operations/Research/2026-08-19_Auditoria_Reels_y_Monetizacion.md`. Las horas e IDs nativos individuales que no fueron capturados siguen pendientes de conciliación, sin revertir el estado operativo.

- **[2.11.23] — 2026-08-20 (Manus): Revisión de Reels de la sesión.** El Reel `2210896633022235` / `CON-2026-08-19-DobleCheck-Universe` quedó documentado como cascada completa en Instagram, Facebook, TikTok y YouTube Shorts. Fernando confirmó que hoy se incorporó un producto nativo de Mercado Libre: producto `MLMU3833350067`, link `https://meli.la/1AQ2upG`, etiqueta `usmfb20260819p01`. Reels sigue activo; sus métricas de video y afiliación deben extraerse en carriles separados y no mezclarse con P0.

- **[2.11.24] — 2026-08-20 (Manus): Corte de métricas del Reel `2210896633022235`.** La consulta correcta se hizo sobre el feed de publicaciones de la página, porque el ID del Reel aparece en el permalink y el objeto de publicación usa `1036844829507460_122153090559072582`. En el corte de las 05:07 UTC Meta devolvió 1 reacción, 0 comentarios y `shares` no expuesto; no se usó el endpoint de Insights que había fallado para las métricas de video. El resultado queda separado de P0 en `Operations/Research/2026-08-20_Meta_Reel_2210896633022235_Metrics.json`.

- **[2.11.25] — 2026-08-20 (Manus): Intento de snapshot afiliado.** No fue posible leer la Central de Afiliados porque la sesión disponible siguió mostrando el inicio de sesión del navegador aislado, aunque My Browser figura habilitado. No se introdujeron credenciales ni se modificó contenido. El corte por etiqueta queda pendiente de una conexión My Browser efectiva o de datos visibles proporcionados por Fernando.

- **[2.11.26] — 2026-08-20 (Manus): Snapshot manual de Mercado Libre confirmado.** Fernando confirmó mediante capturas que el periodo `Últimos 7 días`, actualizado a las 20:51, muestra 2 clics, 0 compradores, 0 órdenes, 0 unidades, $0 de ventas y $0 de comisión. La pestaña `Fecha` atribuye los 2 clics al 18 de agosto. En `Etiquetas de seguimiento`, `Links de facebook - universesentme` registra 1 clic y `usmfb2605400826` —AFF-07 / publicación 260540— registra 1 clic; ambos tienen 0 unidades y 0% de conversión. La etiqueta `usmfb20260819p01` del Reel no aparece en la tabla visible; se clasifica como `Not_Visible_No_Inference`, no como cero clics. Se actualizaron `Affiliate_Metrics_Snapshots.csv`, la auditoría y la estrategia de monetización.

- **[2.11.27] — 2026-08-20 (Manus): Diseño Draft de segunda capa de afiliación para posts ganadores.** Se propone un carril separado `USM-AFF-FB-WINNERS-202608` para revisar publicaciones con rendimiento orgánico superior aunque no pertenezcan a las 10 oportunidades de la Capa 1. Candidatos iniciales de revisión: `2608028` (636 interacciones), `2608029` (335) y `CNT-034 / 260539` (227). La primera ola tendrá como máximo tres candidatos, dos adjunciones aprobadas y un control descriptivo sin producto. Cada candidato requiere encaje editorial, link, etiqueta, fila de ledger y aprobación humana propios. No se asignaron productos ni se adjuntó contenido; la especificación queda en `Operations/Production/2026-08-20_Segunda_Capa_Afiliados_Posts_Ganadores.md` con estado Draft.

- **[2.11.28] — 2026-08-20 (Manus): Primera propuesta concreta de Capa 2.** Tras la aprobación de las reglas generales, se propone adjuntar como máximo dos productos: lámpara de camping para `2608029` / Wilfred y tiras LED suaves para `CNT-034 / 260539` / Evan+Kiri. `2608028` / Universe se conserva como control sin producto en la primera ola por ser el outlier P0 y para no contaminar su referencia editorial. Los productos todavía requieren verificación en Mercado Libre, precio objetivo y aprobación específica; no se generaron links ni se modificó contenido. El Draft pasó a v1.1 en `Operations/Production/2026-08-20_Segunda_Capa_Afiliados_Posts_Ganadores.md`.

- **[2.11.29] — 2026-08-20 (Manus): Candidatos públicos de producto para Capa 2.** Con la selección aprobada, se verificó públicamente una lámpara LED recargable solar para camping con power bank, `MLMU3878057684`, con precio visible de $200.25 MXN para `2608029` / Wilfred; y una tira LED USB de luz cálida para decoración 3000K, `MLM2087253521`, para `CNT-034 / 260539` / Evan+Kiri. Son candidatos públicos, no links afiliados. Falta verificar vendedor, disponibilidad y precio en la sesión de Fernando, generar dos etiquetas/URLs `meli.la` exclusivas y obtener la aprobación final antes de adjuntar.

- **[2.11.30] — 2026-08-20 (Manus): Refinamiento comercial de Capa 2.** La lámpara solar `MLMU3878057684` queda en reserva por envío internacional y solo cinco ventas visibles. La búsqueda de más vendidos encontró como reemplazo prioritario la `MLMU474178210` —Lámpara Táctica Recargable Xhp360 Campismo— con precio visible de $255 MXN, calificación 4.8 y más de 10 mil vendidos; falta verificar envío nacional y stock en la sesión de Fernando. Para `CNT-034 / 260539`, Fernando proporcionó la tira LED neón flexible de 5 m `MLM-3088935338`; precio, vendedor, stock y ventas quedan pendientes de verificación manual. No se generaron links ni se adjuntaron productos.

- **[2.11.31] — 2026-08-20 (Manus): Identificadores operativos de Capa 2 preparados.** Con ambos productos confirmados como disponibles, se prepararon `ML-FB-WIN-2608029-XHP360` con etiqueta `usmwin2608029w0820` para Wilfred y `ML-FB-WIN-CNT034-LEDNEON` con etiqueta `usmwin260539ek0820` para Evan+Kiri. Las etiquetas son exclusivas, no reutilizan AFF-01–AFF-10 ni el Reel, y permanecen en `Draft/Not_Generated` hasta que Fernando genere las URLs afiliadas desde su sesión.

- **[2.11.32] — 2026-08-20 (Manus): Links de Capa 2 generados.** Fernando proporcionó `https://meli.la/1bpVmJQ` con etiqueta `usmwin2608029w0820` para `2608029` / Wilfred / Xhp360, y `https://meli.la/11cbTYc` con etiqueta `usmwin260539ek0820` para `CNT-034 / 260539` / Evan+Kiri / tira LED neón. Ambos quedaron en `Affiliate_Link_Ledger.csv` como `Link_Generated_Not_Attached`; no se adjuntaron a Facebook. Falta aprobación final de la adjunción por registro.

- **[2.11.33] — 2026-08-20 (Manus): Primera ola de Capa 2 activada manualmente.** Fernando confirmó que adjuntó la lámpara Xhp360 (`https://meli.la/1bpVmJQ`, etiqueta `usmwin2608029w0820`) a `2608029` / Wilfred, y las tiras LED neón (`https://meli.la/11cbTYc`, etiqueta `usmwin260539ek0820`) a `CNT-034 / 260539` / Evan+Kiri. `Affiliate_Link_Ledger.csv` fue reconciliado a `Native_Product_Attached_User_Confirmed`; no se modificó el contenido editorial. Horas exactas e IDs nativos individuales permanecen pendientes.

- **[2.11.34] — 2026-08-20 (Manus): Revisión de mención externa y comentario de comunidad.** Se documentó una publicación externa de Skocaj Soledad que menciona a Universe Sent Me tras cuatro semanas consecutivas en su lista de participación. Se clasificó como señal de pertenencia de alta prioridad comunitaria y baja urgencia de moderación. También se revisó el hilo “Aura débil / Aura fuerte” y se preparó una respuesta pendiente de aprobación para el comentario “Falto farmar aura para que nos quede claro”. No se publicaron respuestas ni se modificó Facebook.

- **[2.11.35] — 2026-08-20 (Manus): Respuesta aprobada publicada y tercer comentario identificado.** Se publicó y verificó la respuesta `“Eso ya no es aura débil… eso es falta de actualización espiritual. 😂✨”` al comentario `122151374823072582_1041411612075968`; Meta devolvió `122151374823072582_1792383575281432`. El comentario omitido del mismo hilo es `“La tribu de los migajeros 🤷🏻‍♀️”` (`122151374823072582_1114814910869463`), para el cual queda propuesta `“La tribu se reconoce entre sí. 😂🤷🏻‍♀️”`, pendiente de aprobación. La respuesta al post externo de reconocimiento comunitario sigue sin publicarse porque requiere interacción desde el perfil/página con acceso al post de un tercero.

- **[2.11.36] — 2026-08-20 (Manus): Tercer comentario respondido y hilo cerrado.** Fernando aprobó la respuesta `“La tribu se reconoce entre sí. 😂🤷🏻‍♀️”` al comentario `122151374823072582_1114814910869463`. Meta confirmó HTTP 200 y devolvió `122151374823072582_1415067117189886`. El hilo propio queda atendido; la única acción comunitaria pendiente es que Fernando publique manualmente la respuesta de reconocimiento en el post externo de Skocaj Soledad.

- **[2.11.37] — 2026-08-20 (Manus): Mapa ejecutivo de pendientes actualizado.** Se actualizó `Operations/Research/2026-08-17_Prioridad_Siguientes_Pendientes_Growth_OS.md` a v1.1. El estado real distingue como activos los cortes de la cohorte Facebook 17–30, los snapshots afiliados de AFF-01–AFF-10/Reel/Capa 2, la instrumentación de video del Reel y la reconciliación de la fuente maestra. P0 queda cerrado provisionalmente con limitación; Cohorte 15–16, copy guidelines, movimiento Drive y la primera ola Capa 2 quedan fuera de pendientes inmediatos. Se mantienen diferidos el scheduler histórico de Instagram, CNT-004 y Make como arquitectura activa.

- **[2.11.38] — 2026-08-20 (Manus): Fuente maestra y histórico de junio normalizados.** Se creó `Operations/Research/2026-08-20_Source_Alias_Table.csv` con 98 filas del Publication Log: 52 coincidencias únicas de alta confianza, 46 filas en revisión/sin match y 3 sin clave numérica extraíble. No se crearon CNT ni se convirtió un filename en aprobación canónica. También se creó `Operations/Research/2026-08-20_Historical_Performance_Individuals_Consolidated.csv`, que conserva 211 filas fuente y ofrece 206 publicaciones lógicas tras consolidar cinco grupos duplicados de Meta ID con métricas consistentes. La fuente maestra y la auditoría integral fueron sincronizadas; la deuda restante es resolver los 46 aliases en revisión y enlazar o exceptuar los cinco assets P0.

- **[2.11.39] — 2026-08-20 (Manus): Asociación P0 y clasificación de aliases 17–30.** Los cinco assets P0 fueron auditados: `260633 → CNT-062` y `260642 → CNT-064` quedaron asociados con alta confianza; `2608028`, `2608034- Elara` y `2608027.jpeg` permanecen como excepciones con Meta ID y evidencia visual local, sin CNT creado. En la programación 17–30 se revisaron 81 filas y 43 quedaron en Review: 33 tienen identidad de asset verificada por archivo local pero carecen de fila de inventario, y 10 requieren evidencia adicional. No se modificó `Content_Inventory.csv` automáticamente.

- **[2.11.40] — 2026-08-20 (Manus): Staging de aliases y evidencia ampliada.** Se creó `Operations/Research/2026-08-20_Inventory_Alias_Staging_17_30.csv` con 33 assets visualmente verificados, conservando rutas y SHA-256 sin crear CNT ni modificar `Content_Inventory.csv`. Los diez casos inicialmente sin evidencia en la carpeta principal fueron buscados en rutas locales adicionales: `260508` tiene dos variantes con candidatos `CNT-042`/`CNT-043`, y los otros ocho tienen archivo local pero no fila de inventario. Las opciones y riesgos quedaron en `Operations/Research/2026-08-20_10_Cases_Resolution_Options.csv`.

- **[2.11.41] — 2026-08-20 (Manus): Resolución de 260508 y aprobación no-CNT.** Se validaron `ALIAS-0036 → CNT-042` y `ALIAS-0047 → CNT-043` por filename exacto, asset ref y hash local; ambos pasan a alta confianza sin crear CNT. Las ocho identidades restantes con archivo local se prepararon en `Operations/Research/2026-08-20_NonCNT_Inventory_Alias_Approval.csv` como `Pending_Admin_Approval`, con `CNT_Creation_Allowed=No` y `Canon_Impact=None`.

- **[2.11.42] — 2026-08-20 (Manus): Aprobación administrativa no-CNT.** Fernando aprobó las ocho filas de `2026-08-20_NonCNT_Inventory_Alias_Approval.csv`. El estado pasa a `Approved_Admin`; se mantienen `CNT_Creation_Allowed=No` y `Canon_Impact=None`. No se modificó `Content_Inventory.csv` ni el canon.

- **[2.11.43] — 2026-08-20 (Manus): Impacto de aliases sobre junio cuantificado.** La actualización no cambia Meta IDs ni métricas históricas. Los dos aliases resueltos de `260508` son publicaciones de mayo y sus 17 interacciones quedan atribuidas con precisión a `CNT-042` (9) y `CNT-043` (8), sin alterar la suma mensual. Para junio se establece el uso obligatorio de la vista consolidada: 172 publicaciones lógicas y 17,334 interacciones; las 177 filas fuente contienen cinco duplicados. La capa staging, las ocho aprobaciones no-CNT y las excepciones P0 quedan fuera de los agregados de junio. Documento: `Operations/Research/2026-08-20_Alias_Impact_June.md`; vista maestra actualizada a v2.8.

- **[2.11.44] — 2026-08-20 (Manus): Pendientes de junio reclasificados.** La consolidación de los cinco Meta IDs duplicados quedó cerrada: los agregados deben usar 172 publicaciones lógicas y 17,334 interacciones, preservando las 177 filas fuente para auditoría. Junio ya no tiene un pendiente de métricas ni de doble conteo. Permanece únicamente una cola opcional de 160 publicaciones lógicas sin CNT/inventory match y cinco registros sin `Asset_Ref` utilizable; esa cola no bloquea los agregados y solo debe abrirse si existe una pregunta concreta de atribución, taxonomía o reuse. El mapa de pendientes pasa a v1.2.

- **[2.11.45] — 2026-08-20 (Manus): Estado de julio sincronizado.** El agregado mensual de Facebook permanece integrado para 207 publicaciones, mientras que la reconciliación individual verificable cubre seis top posts (`CNT-074`–`CNT-079`) con Meta ID, asset, Drive y métricas lifetime. La revisión visual y taxonómica de esos seis casos quedó completada: no sustenta atribuir el rendimiento a un personaje por filename. El pendiente real es ampliar la muestra individual solo si existe una pregunta concreta de rendimiento; las ventanas 24/72 horas históricas no son reconstruibles y no deben mezclarse con P0 de agosto. Documento actualizado: `Operations/Research/2026-08-17_Analisis_Julio_Taxonomia_y_Pendientes_Growth_OS.md` v1.2.

- **[2.11.46] — 2026-08-20 (Manus): Paquete de revisión de taxonomía y humor preparado para Claude.** Se consolidaron las hipótesis actuales sobre revisión visual, personajes, estructuras secuenciales, transformaciones, humor ácido, humor sexual sugerente/explícito y captions minimalistas. La clasificación provisional separa `Sustentada por datos`, `Compatible pero no demostrada`, `Inconclusa`, `No validada` y `Señal editorial`; no se modifican la Biblia, el canon, el calendario ni la cola automática de reuse. Se solicita revisión de Claude antes de elevar cualquier hipótesis a regla narrativa. Documento: `Operations/Research/2026-08-20_Revision_Claude_Hipotesis_Taxonomia_Humor.md`.

- **[2.11.47] — 2026-08-20 (Manus): Revisión de Claude integrada al Growth OS.** Se archivó la respuesta completa en `Operations/Research/2026-08-20_Respuesta_Claude_Hipotesis_Taxonomia_Humor.md` y se actualizó el expediente a v1.1. Claude confirmó `TAX-01` como regla permanente de proceso: la revisión visual prevalece sobre filenames genéricos; `TAX-02` puede orientar briefs de situación reconocible, remate claro y compartibilidad; las microhistorias, transformaciones, humor observacional, doble sentido sexual y captions mínimos permanecen como celdas experimentales. `HUM-01` quedó clasificada como **Contradicha por evidencia** cuando se interpreta el humor ácido como categoría amplia. Para futuras transformaciones de Universe se agregan los campos `preserva_gafas_universe` y `preserva_marcadores_identidad`; cualquier `No` requiere revisión canónica antes de interpretar rendimiento. No se modifican Biblia, canon, calendario, inventario protegido ni reuse automático.

- **[2.11.48] — 2026-08-20 (Manus): Propuesta de expansión de celdas comparables.** Se creó la cola `2026-08-20_Expansion_Celdas_Comparables_Candidatos.csv` y la propuesta `2026-08-20_Propuesta_Expansion_Celdas_Comparables.md` para microhistorias secuenciales, transformaciones visuales, humor observacional, diálogo ácido y autodesprecio/antihéroe. La cobertura actual es insuficiente para todas las celdas: transformación tiene 2 casos comparables; observacional y autodesprecio tienen 2; microhistoria tiene 1; diálogo ácido tiene 1. Se fijan umbrales de `n=3` para señal preliminar y `n=5` para veredicto operativo. `caption_minimo`, `caption_refuerzo` y `caption_conversacional` quedan como variable separada. La propuesta permanece en Review y no autoriza publicación, CNT, calendario ni reuse.

- **[2.11.49] — 2026-08-20 (Manus): Corte visual 01 de celdas comparables.** Se promovió `2607787`/Meta ID `1036844829507460_122132365443072582` a diálogo ácido comparable y `2607816`/Meta ID `1036844829507460_122133575895072582` a humor observacional comparable. Se excluyeron Silvio `2607797` y la escena de ansiedad `2607795` de autodesprecio/antihéroe. `2607828`/Meta ID `1036844829507460_122134169481072582` quedó como candidato de autopercepción absurda/antihéroe, conservando la discrepancia con `asset_ref=2607833` en la vista histórica. La cobertura queda en `n=3` observacional, `n=2` diálogo ácido, `n=2` autodesprecio/antihéroe, `n=2` transformación y `n=1` microhistoria. Hallazgos: `Operations/Research/2026-08-20_Expansion_Visual_Findings_01.md`; propuesta actualizada en `Operations/Research/2026-08-20_Propuesta_Expansion_Celdas_Comparables.md`.

- **[2.11.50] — 2026-08-20 (Manus): Ronda 2 de celdas comparables.** Se incorporaron `260731` y `260775` como dos casos comparables de la subcelda `Microhistoria secuencial — dos paneles`, con mediana descriptiva de 361.5 interacciones y 39.5 shares. No se mezclan con la celda estricta de tres paneles, que permanece en `n=1`. El caso `122134608507072582`/Ganso vestido quedó como candidato de transformación de vestuario secundario, no como evidencia de transformación de Universe. `260766` se excluyó por dualidad simultánea y `260728` por ser un panel único. Los captions de la ronda 2 permanecen como `historical_unavailable`; no se estima efecto de caption. Documentos: `Operations/Research/2026-08-20_Expansion_Round2_Analysis.md`, `Operations/Research/2026-08-20_Expansion_Round2_Candidatos.csv` y `Operations/Research/2026-08-20_Expansion_Round2_Visual_Findings.md`.

- **[2.11.51] — 2026-08-20 (Manus): Síntesis histórica junio–julio para orientar agosto.** Se creó `Operations/Research/2026-08-20_Sintesis_Historica_Crecimiento_Junio_Julio.md` y su cálculo reproducible `Operations/Research/2026-08-20_Comparativo_Crecimiento_Junio_Julio.json`. La base homogénea muestra que julio superó a junio en mediana de interacciones por publicación (43 vs. 10) y shares (7 vs. 1), aunque publicó aproximadamente 10% menos piezas. El copy mínimo mejoró con fuerza en julio, pero también mejoraron los posts no mínimos; por ello se documentan como biblioteca de pruebas `Difusión_Minimal`, `Relatable_Social`, `Conversación_Relacional`, `Ácido_Interpersonal` y `Personaje_Marcador`, no como reglas universales. Se recomienda explorar 18:00–22:00 como corredor principal y 14:00–16:00 como control secundario, sin modificar automáticamente el calendario ni el canon.

- **[2.11.52] — 2026-08-20 (Manus): Plan de experimentos de agosto basado en cinco familias.** Se creó `Operations/Production/2026-08-20_Plan_Experimentos_Agosto_5_Familias.md` con las familias `Difusión_Minimal`, `Relatable_Social`, `Conversación_Relacional`, `Ácido_Interpersonal` y `Personaje_Marcador`. La primera ola propuesta (`Wave_1_Signal`) contiene 15 filas, tres por familia, rotando `caption_minimo`, `caption_refuerzo` y `caption_conversacional`. La matriz `2026-08-20_Wave1_Signal_Experiment_Design.csv` permanece en Draft/Review con assets, fechas y aprobaciones en TBD/Pending; no autoriza publicaciones, cambios de calendario, P0, reuse ni afiliados.

- **[2.11.53] — 2026-08-20 (Manus): Integración del plan experimental sobre el calendario 17–30.** La auditoría encontró 74 slots: 35 nuevos, 36 `Reuse_Top` y 3 `Reuse_Reserve`. Se decidió no crear una programación paralela ni mover horarios. La primera ola se implementa como overlay reversible en `Operations/Research/2026-08-20_Overlay_Wave1_Calendario_17_30.csv`, con 15 slots nuevos provisionales, tres por familia y treatments separados. Los 39 slots de reuse y el baseline P0 quedan fuera. El overlay está en Review y requiere aprobación humana antes de cambiar captions, asignar treatments definitivos o modificar cualquier registro de programación.

- **[2.11.54] — 2026-08-20 (Manus): Revisión visual del overlay Wave 1.** Se revisaron los 15 slots futuros del overlay sobre la programación 17–30. La matriz quedó con 9 casos `Eligible`, 4 `Candidate_Review` y 2 `Hold`. `2608053` quedó en hold por coerción romántica y arma de juguete; `2608059` quedó en hold por doble sentido sexual dominante. Se corrigieron clasificaciones de `2608035`, `2608049`, `2608045`, `2608065` y `2608055` para no forzar conversación o humor ácido donde la imagen muestra estrés, monólogo, romance u observación existencial. El validador `2026-08-20_Overlay_Wave1_Review_Summary.json` devuelve `validation=PASS`. No se modificó el calendario ni se publicó contenido.

- **[2.11.55] — 2026-08-20 (Manus): Fernando aprueba excluir los dos holds de Wave 1.** `2608053` y `2608059` pasan a `Approval_Status=Approved_Excluded`; permanecen documentados y no se eliminan del histórico ni del calendario. El subconjunto operativo de nueve casos elegibles se generó en `Operations/Research/2026-08-20_Wave1_Eligible_Operational_Subset.csv`. Los nueve candidatos y los cuatro `Candidate_Review` mantienen `Approval_Status=Pending`; no hay autorización de publicación, cambio de caption ni modificación de calendario. El validador continúa en `validation=PASS`.

- **[2.11.56] — 2026-08-20 (Manus): Visualización de treatments de caption en los 9 candidatos elegibles.** La distribución es 3 `caption_minimo`, 4 `caption_refuerzo` y 2 `caption_conversacional`. `Relatable_Social` concentra cuatro casos; `Difusión_Minimal`, `Conversación_Relacional` y `Ácido_Interpersonal` solo tienen un caso cada una. Se generó `Operations/Research/2026-08-20_Wave1_Caption_Treatment_Distribution.png` y se documentó que los veredictos deben calcularse por familia, no solo sobre el agregado de nueve posts.

- **[2.11.57] — 2026-08-20 (Manus): Corte observado actual de la cohorte Facebook 17–30.** Se refrescó Meta Graph API v26 y se reconciliaron 19 publicaciones de imagen no-P0 con estado `Publicado`, Meta IDs y permalinks en `Operations/Research/2026-08-15_Publication_Log.csv`. El agregado editorial registra 1,095 interacciones observadas: 811 reacciones, 44 comentarios y 240 shares; mediana 35 y media 57.6. Frente al corte homogéneo anterior de 13 imágenes y 731 interacciones, se incorporan 6 imágenes y 364 interacciones; las nuevas promedian 60.7, pero la mediana global baja de 38 a 35. Los 2 Reels se conservan separados y no se mezclan con imágenes, P0 ni afiliados. Meta no entregó ventanas exactas 24/72h; los datos son lifetime observados. El recordatorio anterior era de una ejecución única y permanece pausado/expirado; el corte se ejecutó manualmente sin crear una tarea recurrente. Evidencia: `Operations/Research/2026-08-20_Cohorte_17_30_Meta_Raw_Current.json`, `Operations/Research/2026-08-20_Cohorte_17_30_Current_Cut.json` y `Operations/Research/2026-08-20_Cohorte_17_30_Current_Cut.md`.

- **[2.11.58] — 2026-08-20 (Manus): Outlier de Wilfred traducido a hipótesis de replicación controlada.** El post `2608029` registra 339 interacciones y 100 shares en el corte actual: 31.0% de las interacciones y 41.7% de los shares de las 19 imágenes no-P0. La señal dominante es difusión por identificación, no conversación extensa. Se descompuso el patrón en `gancho coloquial`, `reencuadre inesperado`, `situación deseable`, `estado emocional legible`, `foco visual único` y `personaje visualmente confirmado`. Se creó `Operations/Research/2026-08-20_Analisis_Wilfred_Outlier_Replicacion_5_Familias.md`, el análisis reproducible `Operations/Research/2026-08-20_Wilfred_Outlier_Replication_Analysis.json`, la evidencia de comentarios y el registro visual comparativo. El stack se probará en las cinco familias mediante `Wilfred_Stack_Fidelity`, sin canonizar a Wilfred, la hora 19:00, el fondo fantástico o el caption mínimo. No se modificaron publicaciones, calendario, canon ni inventario protegido.
