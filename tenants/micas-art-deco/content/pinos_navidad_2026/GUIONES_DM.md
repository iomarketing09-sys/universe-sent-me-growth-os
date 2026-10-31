# Guiones de DM y WhatsApp — Pinos de Autor 2026

**Regla:** los precios y la política de anticipo se explican aquí, nunca en el copy público. **Tiempo de respuesta objetivo:** menos de 2 horas en horario hábil.

## 1. Primera respuesta

> ¡Hola! Gracias por escribir🎄

> Con gusto te ayudo con tu pino. Para darte una cotización clara necesito 4 datos:

> 1. ¿Qué altura aproximada tiene tu pino? (mediano ~1.90 m, estándar 2.10–2.20 m, grande 2.40 m o más)

> 2. ¿Quieres trabajar con tus adornos o un diseño desde cero?

> 3. ¿Tienes algun color en mente?, o algo personalizado.

> 4. ¿Me compartes una foto del espacio y de tus adornos actuales?

> Con eso te digo qué opción te conviene y qué fechas tengo disponibles.

## 2. Si responde solo una parte

> Con eso ya me hago una idea 🙌 Solo me falta \[dato pendiente\]. En cuanto lo tenga te paso la cotización y las fechas libres.

No insistir más de dos veces. Si no responde en 48 h:

> ¡Hola de nuevo! Te dejo las fechas que tengo libres esta semana por si te sirve retomarlo: \[fechas\]. Sin compromiso.

## 3. Cotización

> Te comparto tu cotización:

> **Servicio:** \[Restyling Estándar / Transformación Total VIP / Comercial\] **Pino:** \[altura y si es del cliente\] **Incluye:** diagnóstico, diseño, montaje y ajuste final. **No incluye:** \[pino / luces nuevas / traslado / desmontaje\], se cotiza aparte si lo necesitas. **Inversión:** $\[precio final\]

> **Para apartar la fecha:** 50% de anticipo. El saldo se cubre el día del montaje. El anticipo aparta el día y no es reembolsable. \[Confirmar política de reagenda antes de enviar.\]

> ¿Te reservo el \[fecha\] a las \[10:00 / 16:00\]?

## 4. Confirmación de apartado

> Listo, tu fecha queda apartada 🎄

> **Fecha:** \[día\] de \[mes\], \[10:00 / 16:00\] **Servicio:** \[paquete\] **Anticipo recibido:** $\[monto\] **Saldo el día del montaje:** $\[monto\]

> Te mando recordatorio 48 horas antes. Cualquier cambio, avísame con la mayor anticipación posible.

## 5. Recordatorio 48 h antes

> ¡Hola! Te recuerdo tu montaje del \[fecha\] a las \[hora\] 🎄

> Para ese día necesito que el pino esté armado y en el lugar donde se va a decorar. Si tienes luces, déjalas a mano.

> ¿Sigue todo en orden?

## 6. Día del montaje

> ¡Hoy es el día! Llego a las \[hora\]. Cuando termine te comparto fotos del resultado y te cobro el saldo de $\[monto\].

## 7. Cierre y testimonio

> Gracias por confiarme tu pino 🎄 Quedó precioso.

> Si te gustó el resultado, ¿me regalas un comentario o una foto para compartir? Con tu permiso, claro.

> Y si alguien de tu familia quiere su montaje, con gusto le doy prioridad de fecha.

## 8. Reactivación de clientas históricas

> ¡Hola \[nombre\]! Soy Mica 🎄

> Este año abrí la agenda de decoración de pinos del 9 de noviembre al 18 de diciembre. Me encantaría volver a trabajar contigo.

> Si quieres, te mando las opciones y las fechas que tengo. ¿Te interesa?

Enviar en tandas de 10–15, personalizadas. No mandar el mismo texto masivo.

## 9. Pinos comerciales

> ¡Hola! Soy Mica, de Mica's Art & Deco.

> Diseño montajes navideños para espacios comerciales en Piedras Negras: clínicas, spas, notarías y boutiques. Trabajo con una estética cuidada, materiales que se ven bien en foto y montaje que resiste el paso diario.

> ¿Te interesa que te pase una propuesta para tu espacio? Puedo ir a verlo sin compromiso.

## 10. Aliados y referidos

> ¡Hola \[nombre\]! Soy Mica 🎄

> Estoy abriendo la agenda de decoración de pinos para noviembre y diciembre. Si en \[floristería / mueblería / inmobiliaria\] tienen clientes que necesiten montaje, me encantaría colaborar.

> Por cada cliente que cierre, te doy \[comisión o contraprestación acordada\]. ¿Te parece si platicamos?

## 11. Objeciones

**“Está caro”**

> Entiendo. El precio incluye diseño, montaje y ajuste; no es solo colgar adornos. Si el presupuesto es el límite, podemos trabajar con tus adornos en Restyling, que baja la inversión sin perder el diseño.

**“Lo voy a pensar”**

> Claro. Solo te comento que trabajo un pino por día y las fechas se van apartando. Si quieres, te guardo \[fecha\] por 24 horas sin compromiso.

**“Yo lo hago”**

> ¡Qué bueno! Si en algún momento quieres que revisemos la composición o te ayude con los detalles finales, aquí estoy.

**“¿Incluye el pino?”**

> El pino lo pones tú. Si no tienes, también te lo puedo cotizar completo con adornos y luces.

## 12. Motivos de pérdida para el tracker

Usar uno de estos en `--lost-reason`:

- `precio`

- `sin\_respuesta`

- `fecha\_no\_disponible`

- `lo\_hace\_por\_su\_cuenta`

- `fuera\_de\_zona`

- `pospuesto`

## 13. Registro en el tracker

```
python3 tools/revenue\_tracker.py add --tenant micas-art-deco \\  
  --client "Nombre o Cliente 1" --product "Restyling Estándar" --quote 2100 \\  
  --status anticipo --collected 1050 --source facebook \\  
  --stage cita --appointment-at 2026-11-17 \\  
  --campaign-id pinos-2026 --conversation-id "\<id del hilo\>" \\  
  --payment-method transferencia
```

