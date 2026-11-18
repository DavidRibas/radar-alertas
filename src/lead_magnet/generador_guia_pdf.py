"""
Generador de la Guía Oficial Gratuita en PDF (Lead Magnet de Alta Conversión):
'Cómo Participar en Subastas Judiciales y Embargos del BOE sin Riesgo'
Diseño visual editorial elegante en A4 (1240 x 1754 px) usando Pillow.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ASSETS_DIR = BASE_DIR / "assets"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

A4_ANCHO = 1240
A4_ALTO = 1754

def draw_header_bar(draw: ImageDraw.Draw, page_num: int, total_pages: int = 4):
    """Barra superior elegante de cabecera."""
    draw.rectangle([0, 0, A4_ANCHO, 80], fill=(15, 23, 42))
    draw.text((60, 28), "RADARALERTAS • GUÍA OFICIAL EXCLUSIVA", font=ImageFont.truetype("arialbd.ttf", 22), fill=(147, 197, 253))
    draw.text((A4_ANCHO - 160, 28), f"Pág. {page_num}/{total_pages}", font=ImageFont.truetype("arial.ttf", 20), fill=(148, 163, 184))

def draw_footer_bar(draw: ImageDraw.Draw):
    """Pie de página institucional."""
    draw.rectangle([0, A4_ALTO - 70, A4_ANCHO, A4_ALTO], fill=(15, 23, 42))
    draw.text((60, A4_ALTO - 45), "© 2026 RadarAlertas — Monitorización Oficial del BOE y BDNS", font=ImageFont.truetype("arial.ttf", 18), fill=(148, 163, 184))
    draw.text((A4_ANCHO - 340, A4_ALTO - 45), "t.me/RadarAletasSubastas_bot", font=ImageFont.truetype("arialbd.ttf", 18), fill=(59, 130, 246))

def crear_pagina_1_portada() -> Image.Image:
    """Página 1: Portada de alto impacto."""
    img = Image.new("RGB", (A4_ANCHO, A4_ALTO), (11, 19, 43))
    draw = ImageDraw.Draw(img)

    # Fondo degradado sutil
    for y in range(A4_ALTO):
        r = int(11 + (28 - 11) * (y / A4_ALTO))
        g = int(19 + (37 - 19) * (y / A4_ALTO))
        b = int(43 + (65 - 43) * (y / A4_ALTO))
        draw.line([(0, y), (A4_ANCHO, y)], fill=(r, g, b))

    # Badge superior
    badge = [100, 160, 1140, 230]
    draw.rounded_rectangle(badge, radius=16, fill=(30, 58, 138), outline=(96, 165, 250), width=2)
    draw.text((620, 195), "MANUAL PRÁCTICO OFICIAL • EDICIÓN 2026", font=ImageFont.truetype("arialbd.ttf", 24), fill=(191, 219, 254), anchor="mm")

    # Título Principal
    draw.text((620, 360), "CÓMO PARTICIPAR EN", font=ImageFont.truetype("arialbd.ttf", 44), fill=(241, 245, 249), anchor="mm")
    draw.text((620, 440), "SUBASTAS JUDICIALES", font=ImageFont.truetype("arialbd.ttf", 64), fill=(250, 204, 21), anchor="mm")
    draw.text((620, 520), "Y EMBARGOS DEL BOE", font=ImageFont.truetype("arialbd.ttf", 64), fill=(250, 204, 21), anchor="mm")
    draw.text((620, 600), "SIN CORRER RIESGOS", font=ImageFont.truetype("arialbd.ttf", 44), fill=(241, 245, 249), anchor="mm")

    # Caja de subtítulo
    sub_box = [140, 670, 1100, 810]
    draw.rounded_rectangle(sub_box, radius=20, fill=(15, 23, 42, 220), outline=(59, 130, 246), width=3)
    sub_text = (
        "El método paso a paso para acceder a pisos, chalets y vehículos\n"
        "con hasta un 70% de descuento respecto a valor de mercado,\n"
        "auditando cargas y pujando de forma 100% legal y telemática."
    )
    draw.text((620, 740), sub_text, font=ImageFont.truetype("arial.ttf", 26), fill=(226, 232, 240), anchor="mm", align="center")

    # 4 Tarjetas de Puntos Clave
    puntos = [
        ("🏛️ El Portal de Subastas del BOE", "Cómo registrarte gratis con tu DNI electrónico y recuperar el depósito del 5%."),
        ("⚖️ La Auditoría de Cargas (Art. 674 LEC)", "Aprende qué deudas se cancelan por ley y cuáles te correspondería pagar."),
        ("🚗 Subastas de Coches y Vehículos", "El secreto para pujar por turismos y SUVs desde 500 € con visita previa."),
        ("📱 La Clave: La Detección Temprana", "Cómo encontrar oportunidades antes de que se llenen de pujadores profesionales.")
    ]

    y_pos = 870
    for tit, desc in puntos:
        card = [120, y_pos, 1120, y_pos + 120]
        draw.rounded_rectangle(card, radius=18, fill=(20, 30, 55), outline=(51, 65, 85), width=2)
        draw.text((150, y_pos + 25), tit, font=ImageFont.truetype("arialbd.ttf", 26), fill=(147, 197, 253))
        draw.text((150, y_pos + 68), desc, font=ImageFont.truetype("arial.ttf", 21), fill=(203, 213, 225))
        y_pos += 145

    # Badge de autor
    draw.text((620, 1530), "DOCUMENTO ELABORADO POR EL EQUIPO DE ANÁLISIS DE RADARALERTAS", font=ImageFont.truetype("arialbd.ttf", 20), fill=(148, 163, 184), anchor="mm")
    draw.text((620, 1570), "Distribución gratuita para suscriptores y nuevos miembros", font=ImageFont.truetype("arial.ttf", 18), fill=(100, 116, 139), anchor="mm")

    draw_footer_bar(draw)
    return img

def crear_pagina_2_portal_boe() -> Image.Image:
    """Página 2: El Portal del BOE y el Depósito del 5%."""
    img = Image.new("RGB", (A4_ANCHO, A4_ALTO), (248, 250, 252))
    draw = ImageDraw.Draw(img)
    draw_header_bar(draw, 2)

    # Título de sección
    draw.text((80, 120), "CAPÍTULO 1: CÓMO FUNCIONA EL PORTAL DEL BOE", font=ImageFont.truetype("arialbd.ttf", 34), fill=(15, 23, 42))
    draw.text((80, 170), "Todo lo que necesitas saber antes de poner un solo euro", font=ImageFont.truetype("arial.ttf", 24), fill=(100, 116, 139))
    draw.line([(80, 215), (A4_ANCHO - 80, 215)], fill=(226, 232, 240), width=3)

    bloques = [
        (
            "1. ¿Dónde se celebran las subastas legales en España?",
            "El único portal legal y oficial del Estado es subastas.boe.es, gestionado directamente por la Agencia Estatal Boletín Oficial del Estado. "
            "Cualquier otra web que te cobre comisiones de intermediación por pujar NO es la plataforma judicial. "
            "En el portal del BOE la participación es pública y universal para cualquier ciudadano mayor de edad con DNIe o certificado digital."
        ),
        (
            "2. El Depósito de Garantía del 5% (Totalmente seguro)",
            "Para poder emitir una puja en cualquier bien (inmueble o coche), la ley exige consignar el 5% del valor de tasación del bien. "
            "¿Qué ocurre con este dinero?\n"
            "• Si ganas la subasta: El 5% se descuenta automáticamente del precio final a pagar.\n"
            "• Si alguien puja más que tú y NO ganas: El Estado te devuelve el 10% íntegro a tu cuenta corriente en un plazo habitual de 24 a 72 horas.\n"
            "• Reserva de postura: Si quedas segundo, puedes marcar la casilla para que te lo retengan solo si el ganador no paga y el lote pasa a ti."
        ),
        (
            "3. Duración de la subasta y prórroga automática",
            "Las subastas judiciales tienen una duración estándar de 20 días naturales desde su publicación oficial. "
            "¡Cuidado con la regla del último minuto! Si se produce una puja en los últimos minutos antes del cierre, el sistema prorroga el reloj automáticamente hasta 24 horas para dar oportunidad de contraofertar. "
            "Por eso, los inversores veteranos calculan su 'puja máxima racional' y nunca se dejan llevar por la emoción."
        )
    ]

    y = 250
    for tit, cuerpo in bloques:
        card = [80, y, A4_ANCHO - 80, y + 360]
        draw.rounded_rectangle(card, radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=2)

        # Barra lateral azul
        draw.rounded_rectangle([80, y, 92, y + 360], radius=4, fill=(37, 99, 235))

        draw.text((120, y + 25), tit, font=ImageFont.truetype("arialbd.ttf", 25), fill=(30, 58, 138))

        # Texto con wrapping manual
        lines = []
        words = cuerpo.split()
        curr_line = ""
        for w in words:
            if "\n" in w:
                partes = w.split("\n")
                curr_line += partes[0]
                lines.append(curr_line)
                curr_line = partes[1] + " "
            elif len(curr_line + w) < 78:
                curr_line += w + " "
            else:
                lines.append(curr_line)
                curr_line = w + " "
        if curr_line:
            lines.append(curr_line)

        y_text = y + 75
        for l in lines:
            color = (30, 41, 59) if not l.strip().startswith("•") else (21, 128, 61)
            draw.text((120, y_text), l.strip(), font=ImageFont.truetype("arial.ttf", 20), fill=color)
            y_text += 32

        y += 400

    # Cuadro de advertencia
    alerta_box = [80, 1480, A4_ANCHO - 80, 1630]
    draw.rounded_rectangle(alerta_box, radius=14, fill=(254, 242, 242), outline=(239, 68, 68), width=2)
    draw.text((120, 1505), "⚠️ REGLA DE ORO RADARALERTAS:", font=ImageFont.truetype("arialbd.ttf", 22), fill=(185, 28, 28))
    draw.text((120, 1545), "Nunca pujes por un bien sin haber revisado previamente el Dictamen de Cargas.", font=ImageFont.truetype("arialbd.ttf", 20), fill=(127, 29, 29))
    draw.text((120, 1580), "En el siguiente capítulo te explicamos exactamente cómo hacerlo en 2 minutos.", font=ImageFont.truetype("arial.ttf", 19), fill=(153, 27, 27))

    draw_footer_bar(draw)
    return img

def crear_pagina_3_cargas_y_coches() -> Image.Image:
    """Página 3: El Secreto de las Cargas y Subastas de Coches."""
    img = Image.new("RGB", (A4_ANCHO, A4_ALTO), (248, 250, 252))
    draw = ImageDraw.Draw(img)
    draw_header_bar(draw, 3)

    draw.text((80, 120), "CAPÍTULO 2: AUDITORÍA DE CARGAS Y VEHÍCULOS", font=ImageFont.truetype("arialbd.ttf", 34), fill=(15, 23, 42))
    draw.text((80, 170), "La diferencia entre conseguir un chollo o comprar una deuda", font=ImageFont.truetype("arial.ttf", 24), fill=(100, 116, 139))
    draw.line([(80, 215), (A4_ANCHO - 80, 215)], fill=(226, 232, 240), width=3)

    # Comparativa de Cargas
    box_cargas = [80, 250, A4_ANCHO - 80, 770]
    draw.rounded_rectangle(box_cargas, radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=2)
    draw.text((120, 280), "⚖️ El Secreto del Artículo 674 de la Ley de Enjuiciamiento Civil", font=ImageFont.truetype("arialbd.ttf", 25), fill=(30, 58, 138))

    texto_art = (
        "El mayor miedo de quien no conoce el sistema es: '¿Y si el piso tiene deudas y me las quedo yo?'\n"
        "La ley española es muy clara y divide las deudas en dos tipos según la fecha en que se registraron:"
    )
    draw.text((120, 330), texto_art, font=ImageFont.truetype("arial.ttf", 20), fill=(51, 65, 85))

    # Caja Verde: Cargas Posteriores
    verde_box = [120, 420, A4_ANCHO - 120, 560]
    draw.rounded_rectangle(verde_box, radius=12, fill=(240, 253, 244), outline=(34, 197, 94), width=2)
    draw.text((145, 435), "✅ CARGAS POSTERIORES (SE CANCELAN POR MANDAMIENTO JUDICIAL)", font=ImageFont.truetype("arialbd.ttf", 20), fill=(21, 128, 61))
    draw.text((145, 470), "Son las hipotecas o embargos inscritos DESPUÉS del que ejecuta la subasta.", font=ImageFont.truetype("arial.ttf", 19), fill=(22, 101, 52))
    draw.text((145, 505), "El Letrado de la Administración de Justicia ordena su borrado total en el Registro de la Propiedad. Cero euros a pagar.", font=ImageFont.truetype("arial.ttf", 19), fill=(22, 101, 52))

    # Caja Roja: Cargas Anteriores
    roja_box = [120, 580, A4_ANCHO - 120, 720]
    draw.rounded_rectangle(roja_box, radius=12, fill=(254, 242, 242), outline=(239, 68, 68), width=2)
    draw.text((145, 595), "❌ CARGAS ANTERIORES O PREFERENTES (SUBSISTEN Y LAS ASUMES TÚ)", font=ImageFont.truetype("arialbd.ttf", 20), fill=(185, 28, 28))
    draw.text((145, 630), "Son deudas inscritas ANTES de la que provoca la subasta (ej: una primera hipoteca impagada).", font=ImageFont.truetype("arial.ttf", 19), fill=(127, 29, 29))
    draw.text((145, 665), "En RadarAlertas auditamos el expediente oficial para alertarte solo de oportunidades limpias.", font=ImageFont.truetype("arialbd.ttf", 19), fill=(127, 29, 29))

    # Sección de Coches y Vehículos
    box_veh = [80, 810, A4_ANCHO - 80, 1600]
    draw.rounded_rectangle(box_veh, radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=2)
    draw.text((120, 840), "🚗 CÓMO PUJAR POR COCHES Y VEHÍCULOS EMBARGADOS", font=ImageFont.truetype("arialbd.ttf", 25), fill=(30, 58, 138))

    pasos_coche = [
        ("1. ¿Dónde están los coches?", "La mayoría se encuentran custodiados en los depósitos judiciales o municipales de cada ayuntamiento. En la ficha oficial del BOE consta el lugar exacto."),
        ("2. Derecho de Inspección Mecánica", "La ley te da derecho a acudir al depósito previa cita para inspeccionar el estado exterior, neumáticos y comprobar si dispone de llaves y documentación."),
        ("3. El número de bastidor (VIN)", "Con el número de bastidor puedes pedir un informe completo en la DGT por menos de 9 € y comprobar si tiene multas de tráfico pendientes o precintos."),
        ("4. Retirada con grúa y nueva documentación", "Una vez adjudicado el vehículo, el juzgado te entrega el Decreto de Adjudicación. Con él acudes a Tráfico y te emiten la ficha técnica y permiso de circulación a tu nombre sin pagar deudas anteriores.")
    ]

    y_v = 900
    for tit, desc in pasos_coche:
        draw.text((120, y_v), tit, font=ImageFont.truetype("arialbd.ttf", 22), fill=(15, 23, 42))
        draw.text((120, y_v + 35), desc, font=ImageFont.truetype("arial.ttf", 19), fill=(71, 85, 105))
        y_v += 95

    # Badge final
    sello_coches = [120, 1360, A4_ANCHO - 120, 1540]
    draw.rounded_rectangle(sello_coches, radius=12, fill=(239, 246, 255), outline=(59, 130, 246), width=2)
    draw.text((145, 1390), "💡 DATO CLAVE PARA VEHÍCULOS:", font=ImageFont.truetype("arialbd.ttf", 22), fill=(30, 58, 138))
    draw.text((145, 1435), "Muchos coches de gama alta (Mercedes, BMW, Audi) salen a subasta municipal con salidas", font=ImageFont.truetype("arial.ttf", 19), fill=(30, 58, 138))
    draw.text((145, 1475), "inferiores a 1.000 € por falta de postores locales. Quien tiene la alerta, se lleva el chollo.", font=ImageFont.truetype("arialbd.ttf", 19), fill=(29, 78, 216))

    draw_footer_bar(draw)
    return img

def crear_pagina_4_estrategia_y_vip() -> Image.Image:
    """Página 4: La Estrategia y Acceso a los Canales VIP."""
    img = Image.new("RGB", (A4_ANCHO, A4_ALTO), (11, 19, 43))
    draw = ImageDraw.Draw(img)

    for y in range(A4_ALTO):
        r = int(11 + (25 - 11) * (y / A4_ALTO))
        g = int(19 + (35 - 19) * (y / A4_ALTO))
        b = int(43 + (55 - 43) * (y / A4_ALTO))
        draw.line([(0, y), (A4_ANCHO, y)], fill=(r, g, b))

    draw_header_bar(draw, 4)

    draw.text((620, 140), "LA VENTAJA COMPETITIVA DEFINITIVA", font=ImageFont.truetype("arialbd.ttf", 36), fill=(241, 245, 249), anchor="mm")
    draw.text((620, 190), "Por qué el 90% de los chollos se los llevan quienes reciben alertas en tiempo real", font=ImageFont.truetype("arial.ttf", 22), fill=(147, 197, 253), anchor="mm")

    # Caja central
    card = [100, 260, 1140, 720]
    draw.rounded_rectangle(card, radius=24, fill=(15, 23, 42), outline=(59, 130, 246), width=3)

    draw.text((140, 300), "🚨 El problema de buscar manualmente en el BOE:", font=ImageFont.truetype("arialbd.ttf", 26), fill=(239, 68, 68))
    draw.text((140, 350), "Cada día se publican cientos de páginas en el Boletín Oficial del Estado.", font=ImageFont.truetype("arial.ttf", 22), fill=(226, 232, 240))
    draw.text((140, 395), "Revisar una por una las referencias catastrales, notas de cargas y registros es", font=ImageFont.truetype("arial.ttf", 22), fill=(226, 232, 240))
    draw.text((140, 440), "un trabajo de 4 horas diarias que casi nadie puede permitirse.", font=ImageFont.truetype("arial.ttf", 22), fill=(226, 232, 240))

    draw.text((140, 520), "⚡ La solución RadarAlertas:", font=ImageFont.truetype("arialbd.ttf", 26), fill=(34, 197, 94))
    draw.text((140, 570), "Nuestros algoritmos analizan las bases de datos oficiales 3 veces al día,", font=ImageFont.truetype("arial.ttf", 22), fill=(226, 232, 240))
    draw.text((140, 615), "filtran únicamente los expedientes limpios con más del 50% de ahorro real", font=ImageFont.truetype("arial.ttf", 22), fill=(226, 232, 240))
    draw.text((140, 660), "y te los envían directamente a tu Telegram con el enlace para pujar en 1 clic.", font=ImageFont.truetype("arial.ttf", 22), fill=(226, 232, 240))

    # Oferta Canales VIP
    vip_box = [100, 770, 1140, 1460]
    draw.rounded_rectangle(vip_box, radius=28, fill=(20, 30, 55), outline=(234, 179, 8), width=4)

    draw.text((620, 830), "⭐ ACCEDE A NUESTROS 5 CANALES VIP PRIVADOS", font=ImageFont.truetype("arialbd.ttf", 32), fill=(250, 204, 21), anchor="mm")

    canales = [
        ("🏠 Canal Subastas Inmobiliarias", "Pisos, casas y locales al -50% y sin cargas preferentes."),
        ("🚗 Canal Vehículos y Embargos", "Turismos, SUVs, furgonetas y motos oficiales desde 500 €."),
        ("💰 Canal Ayudas y Subvenciones", "Dinero a fondo perdido (BDNS) con convocatorias directas."),
        ("📑 Canal Licitaciones Públicas", "Contratos menores de obras y servicios abiertos a pymes y autónomos."),
        ("💼 Canal Empleo y Oposiciones", "Plazas fijas urgentes del BOE con sueldos de +2.000 €/mes.")
    ]

    y_c = 900
    for tit, sub in canales:
        draw.text((150, y_c), tit, font=ImageFont.truetype("arialbd.ttf", 24), fill=(255, 255, 255))
        draw.text((150, y_c + 38), sub, font=ImageFont.truetype("arial.ttf", 20), fill=(147, 197, 253))
        y_c += 85

    # Botón de CTA
    btn = [160, 1340, 1080, 1430]
    draw.rounded_rectangle(btn, radius=20, fill=(37, 99, 235), outline=(96, 165, 250), width=2)
    draw.text((620, 1385), "👉 ABRE EL BOT DE TELEGRAM: @RadarAletasSubastas_bot", font=ImageFont.truetype("arialbd.ttf", 28), fill=(255, 255, 255), anchor="mm")

    draw.text((620, 1530), "Pack Total VIP: Los 5 Canales por solo 4,99 € / mes (Cancela cuando quieras)", font=ImageFont.truetype("arialbd.ttf", 22), fill=(251, 191, 36), anchor="mm")

    draw_footer_bar(draw)
    return img

def compilar_guia_pdf(ruta_destino: Path) -> Path:
    """Genera todas las páginas y las guarda en un único archivo PDF optimizado."""
    print("📄 Generando páginas de la Guía Oficial RadarAlertas...")
    p1 = crear_pagina_1_portada()
    p2 = crear_pagina_2_portal_boe()
    p3 = crear_pagina_3_cargas_y_coches()
    p4 = crear_pagina_4_estrategia_y_vip()

    p1.save(
        ruta_destino,
        "PDF",
        resolution=150.0,
        save_all=True,
        append_images=[p2, p3, p4],
        quality=95
    )
    print(f"✅ ¡Guía PDF Oficial generada con éxito en: {ruta_destino} ({ruta_destino.stat().st_size / 1024:.1f} KB)")
    return ruta_destino

if __name__ == "__main__":
    out_pdf = OUTPUT_DIR / "Guia_Subastas_Judiciales_RadarAlertas.pdf"
    compilar_guia_pdf(out_pdf)
