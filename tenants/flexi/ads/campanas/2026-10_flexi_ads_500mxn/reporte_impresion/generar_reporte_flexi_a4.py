#!/usr/bin/env python3
from __future__ import annotations

import math
from pathlib import Path

import cairo

OUT_DIR = Path(__file__).resolve().parent
OUT_PDF = OUT_DIR / 'reporte_flexi_campana_A4_impresion.pdf'

A4_W, A4_H = 595.28, 841.89  # points

WHITE = (1.0, 1.0, 1.0)
INK = (0.105, 0.125, 0.16)
MUTED = (0.40, 0.44, 0.49)
ORANGE = (0.84, 0.43, 0.07)
DEEP_ORANGE = (0.60, 0.28, 0.035)
PALE_ORANGE = (0.995, 0.91, 0.77)
PALE_GOLD = (0.985, 0.96, 0.84)
GREEN = (0.12, 0.50, 0.34)
PALE_GREEN = (0.91, 0.97, 0.93)
BLUE = (0.16, 0.38, 0.62)
PALE_BLUE = (0.92, 0.96, 0.99)
BORDER = (0.87, 0.85, 0.79)
GRID = (0.91, 0.90, 0.85)


def hex_rgb(value: str):
    value = value.lstrip('#')
    return tuple(int(value[i:i+2], 16) / 255 for i in (0, 2, 4))


def set_source(c, color):
    c.set_source_rgb(*color)


def rounded_rect(c, x, y, w, h, radius=10):
    r = min(radius, w/2, h/2)
    c.new_sub_path()
    c.arc(x+w-r, y+r, r, -math.pi/2, 0)
    c.arc(x+w-r, y+h-r, r, 0, math.pi/2)
    c.arc(x+r, y+h-r, r, math.pi/2, math.pi)
    c.arc(x+r, y+r, r, math.pi, 3*math.pi/2)
    c.close_path()


def fill_round(c, x, y, w, h, color, radius=10):
    rounded_rect(c, x, y, w, h, radius)
    set_source(c, color)
    c.fill()


def stroke_round(c, x, y, w, h, color, radius=10, width=1):
    rounded_rect(c, x, y, w, h, radius)
    set_source(c, color)
    c.set_line_width(width)
    c.stroke()


def text_width(c, text, size, bold=False):
    c.save()
    c.select_font_face('DejaVu Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size)
    ext = c.text_extents(text)
    c.restore()
    return ext.x_advance


def draw_text(c, x, y, text, size=10, color=INK, bold=False, max_width=None, align='left', line_height=None, max_lines=None):
    face = cairo.ToyFontFace('DejaVu Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    c.select_font_face('DejaVu Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size)
    set_source(c, color)
    words = text.split()
    lines = []
    current = ''
    for word in words:
        candidate = word if not current else current + ' ' + word
        if max_width and text_width(c, candidate, size, bold) > max_width and current:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and text_width(c, lines[-1] + '…', size, bold) > max_width:
            lines[-1] = lines[-1][:-1]
        lines[-1] += '…'
    lh = line_height or size * 1.32
    total_h = len(lines) * lh
    if align == 'center':
        for idx, line in enumerate(lines):
            tw = text_width(c, line, size, bold)
            c.move_to(x - tw/2, y + idx*lh)
            c.show_text(line)
    elif align == 'right':
        for idx, line in enumerate(lines):
            tw = text_width(c, line, size, bold)
            c.move_to(x - tw, y + idx*lh)
            c.show_text(line)
    else:
        for idx, line in enumerate(lines):
            c.move_to(x, y + idx*lh)
            c.show_text(line)
    return total_h


def draw_centered(c, cx, y, text, size=10, color=INK, bold=False, max_width=None):
    return draw_text(c, cx, y, text, size, color, bold, max_width=max_width, align='center')


def planet(c, cx, cy, radius, variant=0):
    # Saturn-like orange planet
    c.save()
    c.arc(cx, cy, radius, 0, 2*math.pi)
    c.set_source_rgb(*PALE_ORANGE)
    c.fill()
    c.set_source_rgb(*ORANGE)
    c.set_line_width(1.4)
    c.stroke()
    # bands
    c.save()
    c.arc(cx, cy, radius, 0, 2*math.pi)
    c.clip()
    for idx, off in enumerate((-0.35, -0.05, 0.28, 0.52)):
        yy = cy + radius * off
        c.set_source_rgb(*(DEEP_ORANGE if idx % 2 == 0 else PALE_GOLD))
        c.set_line_width(max(1.5, radius*0.13))
        c.move_to(cx-radius, yy + radius*0.05)
        c.curve_to(cx-radius*0.25, yy-radius*0.08, cx+radius*0.25, yy+radius*0.08, cx+radius, yy-radius*0.03)
        c.stroke()
    c.restore()
    # ring
    c.set_source_rgba(0.60, 0.28, 0.035, 0.55)
    c.set_line_width(max(1.2, radius*0.11))
    c.save()
    c.translate(cx, cy)
    c.scale(1, 0.28)
    c.arc(0, 0, radius*1.42, math.pi*0.08, math.pi*0.92)
    c.stroke()
    c.restore()
    # moon
    moon_x = cx + radius*1.25
    moon_y = cy - radius*0.95
    c.arc(moon_x, moon_y, radius*0.18, 0, 2*math.pi)
    c.set_source_rgb(*PALE_GOLD)
    c.fill()
    c.set_source_rgb(*DEEP_ORANGE)
    c.set_line_width(0.8)
    c.stroke()
    c.restore()


def icon_spark(c, cx, cy, size, color=ORANGE):
    c.set_source_rgb(*color)
    c.move_to(cx, cy-size)
    c.line_to(cx+size*0.22, cy-size*0.22)
    c.line_to(cx+size, cy)
    c.line_to(cx+size*0.22, cy+size*0.22)
    c.line_to(cx, cy+size)
    c.line_to(cx-size*0.22, cy+size*0.22)
    c.line_to(cx-size, cy)
    c.line_to(cx-size*0.22, cy-size*0.22)
    c.close_path()
    c.fill()


def draw_logo(c, x, y):
    planet(c, x+18, y+18, 13, 0)
    draw_text(c, x+42, y+10, 'iO', 17, INK, True)
    draw_text(c, x+62, y+10, 'Marketing', 17, ORANGE, True)
    draw_text(c, x+42, y+26, 'INTELIGENCIA QUE IMPULSA', 5.5, MUTED, True)


def draw_header(c, page_label, subtitle):
    c.set_source_rgb(*WHITE)
    c.paint()
    # decorative orbit lines
    c.save()
    c.translate(A4_W-45, 42)
    c.scale(1, 0.3)
    c.set_source_rgba(0.84, 0.43, 0.07, 0.16)
    c.set_line_width(7)
    c.arc(0, 0, 30, 0, 2*math.pi)
    c.stroke()
    c.restore()
    draw_logo(c, 38, 26)
    fill_round(c, A4_W-166, 28, 128, 23, WHITE, 11)
    draw_centered(c, A4_W-102, 43, page_label, 8, DEEP_ORANGE, True)
    c.set_source_rgb(*BORDER)
    c.set_line_width(0.8)
    c.move_to(38, 72)
    c.line_to(A4_W-38, 72)
    c.stroke()
    draw_text(c, 38, 90, subtitle, 8, MUTED, False, max_width=A4_W-76)


def draw_footer(c, page_no):
    c.set_source_rgb(*BORDER)
    c.set_line_width(0.8)
    c.move_to(38, 807)
    c.line_to(A4_W-38, 807)
    c.stroke()
    draw_text(c, 38, 822, 'iO Marketing · Datos Meta Ads · corte 25 oct 2026', 7, MUTED)
    draw_text(c, A4_W-38, 822, f'{page_no}/2', 7, MUTED, align='right')


def metric_card(c, x, y, w, h, label, value, unit='', accent=ORANGE, note=None, fill=WHITE):
    fill_round(c, x, y, w, h, fill, 12)
    stroke_round(c, x, y, w, h, BORDER, 12, 0.8)
    c.set_source_rgb(*accent)
    c.rectangle(x, y, 4, h)
    c.fill()
    draw_text(c, x+16, y+22, label.upper(), 7, MUTED, True, max_width=w-26)
    draw_text(c, x+16, y+52, value, 24, INK, True, max_width=w-26)
    if unit:
        vw = text_width(c, value, 24, True)
        draw_text(c, x+18+vw, y+52, unit, 8, MUTED, True)
    if note:
        draw_text(c, x+16, y+h-15, note, 7, MUTED, False, max_width=w-26, max_lines=2)


def section_title(c, x, y, number, title, subtitle=None):
    icon_spark(c, x+6, y-3, 6, ORANGE)
    draw_text(c, x+18, y, title, 13, INK, True)
    if subtitle:
        draw_text(c, x+18, y+15, subtitle, 7.5, MUTED)
    return y + (29 if subtitle else 18)


def progress_bar(c, x, y, w, value, max_value, color, threshold=None, label=None, value_label=None):
    fill_round(c, x, y, w, 8, (0.91,0.90,0.85), 4)
    ratio = 0 if max_value <= 0 else max(0, min(1, value/max_value))
    fill_round(c, x, y, w*ratio, 8, color, 4)
    if threshold is not None:
        tx = x + w*max(0,min(1,threshold/max_value))
        c.set_source_rgb(*DEEP_ORANGE)
        c.set_line_width(1.2)
        c.move_to(tx, y-3)
        c.line_to(tx, y+11)
        c.stroke()
    if label:
        draw_text(c, x, y+21, label, 6.8, MUTED)
    if value_label:
        draw_text(c, x+w, y+21, value_label, 6.8, INK, True, align='right')


def bullet(c, x, y, title, body, width, color=ORANGE, body_size=8):
    c.set_source_rgb(*color)
    c.arc(x+3, y-2.5, 2.8, 0, 2*math.pi)
    c.fill()
    draw_text(c, x+12, y, title, 9, INK, True, max_width=width-12)
    return draw_text(c, x+12, y+14, body, body_size, MUTED, False, max_width=width-12, line_height=body_size*1.35, max_lines=3)


def page_one(c):
    draw_header(c, 'REPORTE DE CAMPAÑA', 'Resultados consolidados · ejecución, audiencia y conversación')
    y = 112
    draw_text(c, 38, y, 'Flexi OI26', 25, INK, True)
    draw_text(c, 38, y+19, 'Campaña de prueba en Meta Ads para generar conversaciones por WhatsApp', 9, MUTED)
    fill_round(c, 412, 106, 145, 44, PALE_GREEN, 12)
    draw_text(c, 426, 123, 'RESULTADO PRINCIPAL', 7, GREEN, True)
    draw_text(c, 426, 141, '79 conversaciones', 13, INK, True)
    c.set_source_rgb(*GREEN)
    c.set_line_width(1.5)
    c.move_to(520, 126); c.line_to(527, 133); c.line_to(542, 113); c.stroke()

    y = 170
    section_title(c, 38, y, '1', 'Inversión y alcance')
    card_y = y + 22
    metric_card(c, 38, card_y, 162, 84, 'Gasto real', '$439.28', 'MXN', ORANGE, '87.9% del presupuesto de $500 MXN')
    metric_card(c, 214, card_y, 162, 84, 'Impresiones', '12,772', '', BLUE, 'Exposiciones del anuncio')
    metric_card(c, 390, card_y, 167, 84, 'Alcance', '6,653', 'personas', GREEN, 'Frecuencia: 1.92')

    y = card_y + 105
    section_title(c, 38, y, '2', 'Tráfico y eficiencia')
    card_y = y + 22
    metric_card(c, 38, card_y, 102, 84, 'Clics', '999', '', BLUE)
    metric_card(c, 153, card_y, 102, 84, 'CTR', '7.82', '%', GREEN, 'Meta ≥ 0.8%')
    metric_card(c, 268, card_y, 102, 84, 'CPC', '$0.44', 'MXN', ORANGE)
    metric_card(c, 383, card_y, 174, 84, 'Conversaciones', '79', '', ORANGE, '$5.56/conversación · meta ≤ $35 MXN')

    y = card_y + 104
    section_title(c, 38, y, '3', 'Cumplimiento de objetivos', 'Comparación de resultados contra la meta de la prueba')
    panel_y = y + 31
    fill_round(c, 38, panel_y, 519, 133, WHITE, 12)
    stroke_round(c, 38, panel_y, 519, 133, BORDER, 12, 0.8)
    progress_bar(c, 58, panel_y+26, 210, 79, 14, GREEN, threshold=14, label='Conversaciones · meta ≥ 14', value_label='79  ·  564%')
    progress_bar(c, 58, panel_y+62, 210, 5.56, 35, GREEN, threshold=35, label='Costo por conversación · meta ≤ $35', value_label='$5.56  ·  óptimo')
    progress_bar(c, 58, panel_y+98, 210, 7.82, 0.8, GREEN, threshold=0.8, label='CTR · meta ≥ 0.8%', value_label='7.82%  ·  978%')
    # right insight
    c.set_source_rgb(*PALE_ORANGE)
    c.rectangle(300, panel_y+16, 1, 101); c.fill()
    planet(c, 331, panel_y+42, 19)
    draw_text(c, 364, panel_y+31, 'LA PRUEBA FUE', 7, DEEP_ORANGE, True)
    draw_text(c, 364, panel_y+48, 'EFECTIVA', 15, INK, True)
    draw_text(c, 364, panel_y+66, 'El tráfico y el costo de conversación superaron ampliamente las metas definidas.', 8, MUTED, max_width=170, line_height=11)
    draw_text(c, 300, panel_y+101, 'Conclusión: el mensaje genera interés y abre conversaciones con un costo unitario bajo.', 8.2, INK, True, max_width=236, line_height=11)

    y = panel_y + 153
    section_title(c, 38, y, '4', 'Qué sabemos y qué falta')
    fill_round(c, 38, y+19, 251, 83, PALE_GREEN, 12)
    stroke_round(c, 38, y+19, 251, 83, (0.72,0.88,0.78), 12, 0.8)
    icon_spark(c, 55, y+39, 5, GREEN)
    draw_text(c, 67, y+42, 'CONFIRMADO', 8, GREEN, True)
    draw_text(c, 55, y+61, '• 79 conversaciones iniciadas', 8, INK)
    draw_text(c, 55, y+75, '• 90 conexiones totales de mensajería', 8, INK)
    draw_text(c, 55, y+89, '• CTR de 7.82%', 8, INK)
    fill_round(c, 306, y+19, 251, 83, PALE_BLUE, 12)
    stroke_round(c, 306, y+19, 251, 83, (0.76,0.87,0.94), 12, 0.8)
    icon_spark(c, 323, y+39, 5, BLUE)
    draw_text(c, 335, y+42, 'PENDIENTE DE MEDIR', 8, BLUE, True)
    draw_text(c, 323, y+61, '• Profundidad: mensajes por conversación', 8, INK)
    draw_text(c, 323, y+75, '• Respuestas salientes de la sucursal', 8, INK)
    draw_text(c, 323, y+89, '• Ventas y visitas atribuidas', 8, INK)
    draw_footer(c, 1)


def page_two(c):
    draw_header(c, 'GUÍA DE INTERPRETACIÓN', 'Qué nos dicen los datos y cómo convertir el aprendizaje en mejores campañas')
    y = 108
    draw_text(c, 38, y, 'De métricas a decisiones', 22, INK, True)
    draw_text(c, 38, y+18, 'La conversación es el resultado principal; las demás métricas ayudan a entender cómo llegó.', 8.5, MUTED)

    y = 148
    section_title(c, 38, y, '1', 'Qué significa cada cifra')
    items = [
        ('Conversaciones', 'Personas que escribieron', 'Personas que escribieron al anuncio. Es el KPI principal: mide cuántas personas iniciaron una conversación.'),
        ('CTR', 'Interés en el anuncio', 'Porcentaje de personas que hizo clic. Un 7.82% indica que el mensaje resonó con la audiencia.'),
        ('CPC', 'Costo de cada clic', 'Cuánto se pagó por cada clic al mensaje o enlace. No equivale al costo de una venta.'),
        ('Alcance y frecuencia', 'Personas y repeticiones', 'Alcance: cuántas personas vieron el anuncio. Frecuencia: cuántas veces promedio lo vieron.'),
        ('Costo por conversación', 'Eficiencia real', 'Gasto dividido entre conversaciones. Indica cuánto costó abrir cada conversación con el anuncio.'),
        ('90 conexiones', 'Volumen total de mensajería', 'Volumen total registrado: 79 conversaciones iniciadas más 11 conexiones de mensajería.'),
    ]
    col1 = [items[0], items[1], items[2]]
    col2 = [items[3], items[4], items[5]]
    for idx, item in enumerate(col1):
        yy = y + 24 + idx*62
        fill_round(c, 38, yy, 251, 58, WHITE, 9)
        stroke_round(c, 38, yy, 251, 58, BORDER, 9, 0.7)
        draw_text(c, 50, yy+14, item[0], 8.3, INK, True)
        draw_text(c, 50, yy+26, item[1].upper(), 6.2, ORANGE, True)
        draw_text(c, 50, yy+38, item[2], 6.4, MUTED, max_width=225, max_lines=2, line_height=8)
    for idx, item in enumerate(col2):
        yy = y + 24 + idx*62
        fill_round(c, 306, yy, 251, 58, WHITE, 9)
        stroke_round(c, 306, yy, 251, 58, BORDER, 9, 0.7)
        draw_text(c, 318, yy+14, item[0], 8.3, INK, True)
        draw_text(c, 318, yy+26, item[1].upper(), 6.2, ORANGE, True)
        draw_text(c, 318, yy+38, item[2], 6.4, MUTED, max_width=225, max_lines=2, line_height=8)

    y = 370
    section_title(c, 38, y, '2', 'Para qué nos sirven estos datos')
    uses = [
        ('Detectar qué mensaje funciona', 'El CTR y el costo por conversación permiten conservar el enfoque que genera interés sin gastar de más.'),
        ('Mejorar la atención en WhatsApp', '79 conversaciones son 79 oportunidades. El tiempo de respuesta y la calidad del seguimiento convierten interés en visitas.'),
        ('Diseñar la siguiente prueba', 'Comparar ángulos, mensajes y públicos con una línea base real, en lugar de escalar con supuestos.'),
    ]
    for idx, (title, body) in enumerate(uses):
        x = 38 + idx*174
        fill_round(c, x, y+20, 163, 76, PALE_ORANGE if idx == 1 else WHITE, 11)
        stroke_round(c, x, y+20, 163, 76, BORDER, 11, 0.7)
        planet(c, x+23, y+37, 9)
        draw_text(c, x+40, y+34, title, 8.1, INK, True, max_width=113, max_lines=2, line_height=9)
        draw_text(c, x+12, y+56, body, 6.6, MUTED, max_width=140, line_height=8.5, max_lines=3)

    y = 484
    section_title(c, 38, y, '3', 'Cómo podemos mejorar la siguiente campaña')
    steps = [
        ('01', 'Separar volumen de calidad', 'Clasificar cada conversación: modelo, talla, precio o visita. Medir cuáles son comerciales.'),
        ('02', 'Activar la profundidad', 'Completar los ecos de WhatsApp para registrar respuestas de sucursal, duración y profundidad.'),
        ('03', 'A/B testear el mensaje', 'Probar Beneficio directo contra Prueba social con el mismo presupuesto y audiencias comparables.'),
        ('04', 'Optimizar la atención', 'Programar atención humana, responder en menos de 15 minutos y usar un guion de tallas y modelos.'),
        ('05', 'Cerrar el ciclo de venta', 'Registrar visita, cotización o compra para conectar el costo de conversación con el resultado comercial.'),
        ('06', 'Escalar con evidencia', 'Repetir el mejor creativo, aumentar el presupuesto gradualmente y mantener un grupo de control.'),
    ]
    for idx, (num, title, body) in enumerate(steps):
        col = idx % 2
        row = idx // 2
        x = 38 + col*260
        yy = y + 20 + row*57
        fill_round(c, x, yy, 250, 51, WHITE, 10)
        stroke_round(c, x, yy, 250, 51, BORDER, 10, 0.7)
        fill_round(c, x+10, yy+11, 34, 34, PALE_ORANGE, 17)
        draw_centered(c, x+27, yy+32, num, 10, DEEP_ORANGE, True)
        draw_text(c, x+54, yy+17, title, 8.1, INK, True, max_width=185)
        draw_text(c, x+54, yy+31, body, 6.5, MUTED, max_width=185, max_lines=2, line_height=8)

    y = 687
    fill_round(c, 38, y, 519, 91, PALE_GOLD, 13)
    stroke_round(c, 38, y, 519, 91, (0.88,0.76,0.49), 13, 0.8)
    planet(c, 72, y+35, 20)
    draw_text(c, 106, y+25, 'RECOMENDACIÓN INMEDIATA', 8, DEEP_ORANGE, True)
    draw_text(c, 106, y+45, 'No escalar todavía a ciegas.', 13, INK, True)
    draw_text(c, 106, y+63, 'La campaña demostró que el mensaje atrae y conversa a bajo costo. El siguiente paso es medir calidad,', 7.6, MUTED, max_width=422, line_height=10)
    draw_text(c, 106, y+74, 'respuesta humana y resultado comercial; después decidir cuánto presupuesto aumentar.', 7.6, MUTED, max_width=422, line_height=10)
    draw_footer(c, 2)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    surface = cairo.PDFSurface(str(OUT_PDF), A4_W, A4_H)
    c = cairo.Context(surface)
    page_one(c)
    c.show_page()
    page_two(c)
    c.show_page()
    surface.finish()
    print(OUT_PDF)

if __name__ == '__main__':
    main()
