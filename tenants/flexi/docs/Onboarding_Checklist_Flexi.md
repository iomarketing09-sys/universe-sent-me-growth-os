# Checklist de Onboarding – Flexi Distribuidor Oficial

**Fecha de inicio objetivo:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
**Responsable Flexi:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
**Responsable Growth OS:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_


## 📦 1. CATÁLOGO Y PRECIOS (Día 1 - Crítico)

> **Para qué:** Diseñar flujo (menú catálogo, respuestas "¿Precio de...?"), crear anuncios, calcular metas reales.

| Ítem | Detalle Requerido | Formato | ✅ Listo |
| - | - | - | - |
| Lista completa de productos | SKU, Nombre, Precio, Tallas disponibles, Colores, Stock actual | CSV / Excel / Google Sheets | ☐ |
| Fotos principales | 1 foto por SKU (fondo blanco preferible), naming: `SKU\_nombre.jpg` | Carpeta Drive / ZIP | ☐ |
| Top 10 best-sellers | SKU + unidades vendidas último mes | Lista simple | ☐ |
| Productos con mayor margen | SKU + margen % (para empujar en chat/ads) | Lista simple | ☐ |
| Productos discontinuados / sin stock | SKU (para no ofrecer en chat) | Lista simple | ☐ |



## 📊 2. HISTORIAL DE VENTAS (Día 1 - Si Tienen)

> **Para qué:** Calcular ticket promedio real, estacionalidad, metas basadas en datos, no suposiciones.

| Ítem | Detalle Requerido | Formato | ✅ Listo |
| - | - | - | - |
| Ventas últimos 6 meses | Fecha, SKU, Producto, Talla, Precio unitario, Cantidad, Total, Canal (IG/FB/WhatsApp/Web/Referido) | CSV / Excel | ☐ |
| Ticket promedio histórico | (Se calcula, pero si ya lo saben: $\_\_\_\_) | Número | ☐ |
| Estacionalidad | Meses fuertes / débiles | Notas | ☐ |
| Clientes recurrentes | % que recompra, frecuencia | % / notas | ☐ |



## 🎁 3. PROMOCIONES VIGENTES (Día 1)

> **Para qué:** Configurar en chat (OmniRoute), copys de anuncios, plantillas WhatsApp.

| Ítem | Detalle Requerido | Formato | ✅ Listo |
| - | - | - | - |
| Promociones activas | Tipo (% off, 2x1, envío gratis, 1ra compra), vigencia, condiciones, código si aplica | Lista | ☐ |
| Descuentos por volumen | "Compra 3 y lleva 1 gratis", "Mayoreo desde 6 pares" | Detalle | ☐ |
| Promos estacionales planificadas | Fechas, tipo, productos aplicables | Calendario | ☐ |



## 🚚 4. LOGÍSTICA Y ENVÍOS (Día 2)

> **Para qué:** Plantillas WhatsApp ("Tu pedido está en camino"), FAQ en chat, gestión de expectativas.

| Ítem | Detalle Requerido | Formato | ✅ Listo |
| - | - | - | - |
| Tiempo de preparación | Horas/días hábiles desde pago confirmado hasta salida | Número | ☐ |
| Paquetería(s) usada(s) | Nombre(s), si tienen cuenta corporativa | Lista | ☐ |
| Costo de envío por zona | CDMX, Área Metro, Foráneo, Gratis desde $X | Tabla / Reglas | ☐ |
| Rastreo | ¿Envían link automático? ¿Manual? ¿Paquetería lo da? | Sí/No + cómo | ☐ |
| Empaque especial | Caja de marca, papel tissue, tarjeta agradecimiento | Sí/No + fotos | ☐ |



## 📋 5. POLÍTICAS COMERCIALES (Día 2)

> **Para qué:** FAQ en chat, reducir fricción en cierre, plantillas WhatsApp.

| Ítem | Detalle Requerido | Formato | ✅ Listo |
| - | - | - | - |
| Cambios y devoluciones | Días permitidos, condiciones (sin usar, etiquetas, empaque original), quién paga envío | Texto | ☐ |
| Garantía | Qué cubre, por cuánto tiempo, proceso | Texto | ☐ |
| Métodos de pago aceptados | Transferencia, link de pago (MercadoPago/Stripe), efectivo en entrega, meses sin intereses | Lista | ☐ |
| Facturación | ¿Facturan? ¿RFC requerido? ¿Proceso? | Sí/No + detalle | ☐ |



## 👥 6. EQUIPO WHATSAPP (Día 2)

> **Para qué:** Configurar derivación en OmniRoute, horarios, métricas de respuesta.

| Ítem | Detalle Requerido | Formato | ✅ Listo |
| - | - | - | - |
| Quién atiende | Nombre, rol, horario (ej: L-V 9-18, S 10-14) | Tabla | ☐ |
| Respaldos | Quién cubre si el titular no está | Nombre | ☐ |
| Tiempo objetivo 1ra respuesta | Meta: \< 5 min / \< 15 min / \< 1 hora | Minutos | ☐ |
| Escalación | ¿A quién derivar si no saben responder? (Gerente, dueño) | Nombre + contacto | ☐ |
| Número WhatsApp Business | El número que se registrará en API (debe recibir SMS/llamada) | Número | ☐ |



## 🔐 7. ACCESOS TÉCNICOS (Admin - Día 1)

> **Nosotros configuramos, tú das permiso de administrador.**

| Acceso | Plataforma | Permiso | ✅ Otorgado |
| - | - | - | - |
| Meta Business Suite | business.facebook.com | **Administrador** | ☐ |
| Instagram | @zapateriaflexipn | **Administrador** | ☐ |
| Facebook Page | Zapateria Flexi Piedras Negras | **Administrador** | ☐ |
| Google Analytics (GA4) | analytics.google.com | **Editor** | ☐ |
| Google Tag Manager | tagmanager.google.com | **Publicar** | ☐ |
| **Número WhatsApp** | (Para verificación Business API) | **Propietario** (recibe SMS/llamada) | ☐ |
| Dominio (opcional) | DNS de `flexi.mx` | **Acceso DNS** (para subdominio `comprar.flexi.mx`) | ☐ |


> **Cómo darnos acceso sin compartir contraseña:**

> - Meta: Business Settings → Usuarios → Agregar → Email nuestro → Admin

> - GA4/GTM: Admin → Gestión de acceso → Agregar usuario → Email nuestro

> - WhatsApp: Solo necesitamos el número; nosotros iniciamos verificación


## 🌐 8. OPCIONAL: DOMINIO PARA PANEL WEB

| Opción | Acción | ✅ Listo |
| - | - | - |
| Subdominio propio | Crear `comprar.flexi.mx` → apuntar a IP que demos | ☐ |
| Usar nuestro dominio | `flexi.growth-os.dashboard` (listo en 1 día) | ☐ |



## ✅ 9. VERIFICACIÓN META BUSINESS (Iniciar Ya)

> **Requerido para:** Plantillas WhatsApp + Anuncios "Clic a WhatsApp".  
**Tiempo:** 1-2 semanas. **Iniciar ya en paralelo al onboarding.**

| Paso | Acción | ✅ Listo |
| - | - | - |
| 1. Entrar a business.facebook.com → Configuración de negocio → Verificación | Iniciar proceso | ☐ |
| 2. Subir documentos: Acta constitutiva, RFC, identificación representante legal | Subir PDFs | ☐ |
| 3. Esperar revisión Meta (1-10 días hábiles) | Monitorear email | ☐ |
| 4. Confirmar permisos `whatsapp\_business\_management` y `whatsapp\_business\_messaging` | Verificar en configuración | ☐ |



## 📅 10. CALENDARIO DE ARRANQUE (Propuesto)

| Semana | Hito | Responsable |
| - | - | - |
| **Semana 0 (Onboarding)** | Entregar todo lo de arriba + accesos | Flexi |
| **Día 1-2** | Kickoff 30 min + verificación accesos | Ambos |
| **Semana 1** | Linktree, WhatsApp API, OmniRoute, Pixel/GA4, Panel MVP, CRM plantilla | Growth OS |
| **Semana 1-2** | Verificación Meta Business (en paralelo) | Flexi |
| **Semana 2** | Plantillas WhatsApp aprobadas, Ads activos, Contenidos, Panel v1.0 | Growth OS |
| **Semana 3** | Capacitación CRM (1h), Métricas 48h en Panel | Ambos |
| **Semana 4** | Panel v1.0 completo, A/B tests, Retargeting | Growth OS |



## 📝 NOTAS ADICIONALES

| Tema | Comentario |
| - | - |
| Fotos/video para contenidos | ¿Equipo interno o necesitan proveedor? |
| Festivos / cierres 2026 | Días sin operación para no programar ads |
| Competencia directa | Nombres / cuentas IG para benchmark |
| Objetivo de ventas mes 3 | Pedidos meta: \_\_\_\_ / Mes (para calcular CAC objetivo) |



## ✅ FIRMA DE CONFORMIDAD

**Flexi (Cliente):**

- Nombre: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

- Cargo: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

- Firma: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

- Fecha: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Growth OS (Proveedor):**

- Nombre: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

- Cargo: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

- Firma: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

- Fecha: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_


> **¿Dudas? ¿Algo no aplica? Marcar y lo ajustamos en kickoff.**

