"""
Generador de la Guía Oficial Gratuita en PDF (Lead Magnet Sector Motor):
'Cómo Comprar Coches, Furgonetas y Motos en Subastas Judiciales del BOE desde 500 €'
Diseño visual editorial elegante en A4 (1240 x 1754 px) usando Pillow.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ASSETS_DIR = BASE_DIR / "assets"
ASSETS_DIR.mkdir(exist_ok=True)
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

A4_ANCHO = 1240
A4_ALTO = 1754

def get_font(name: str, size: int):
    """Carga una fuente TrueType del sistema o fallback estándar."""
    try:
        return ImageFont.truetype(name, size)
    except Exception:
        return ImageFont.load_default()

def draw_header_bar(draw: ImageDraw.Draw, page_num: int, total_pages: int = 3):
    """Barra superior elegante de cabecera."""
    draw.rectangle([0, 0, A4_ANCHO, 80], fill=(15, 23, 42))
    draw.text((60, 28), "RADARALERTAS • GUÍA MOTOR & VEHÍCULOS EMBARGADOS", font=get_font("arialbd.ttf", 22), fill=(147, 197, 253))
    draw.text((A4_ANCHO - 160, 28), f"Pág. {page_num}/{total_pages}", font=get_font("arial.ttf", 20), fill=(148, 163, 184))

def draw_footer_bar(draw: ImageDraw.Draw):
    """Pie de página institucional."""
    draw.rectangle([0, A4_ALTO - 70, A4_ANCHO, A4_ALTO], fill=(15, 23, 42))
    draw.text((60, A4_ALTO - 45), "© 2026 RadarAlertas — Monitorización Oficial del BOE y DGT", font=get_font("arial.ttf", 18), fill=(148, 163, 184))
    draw.text((A4_ANCHO - 340, A4_ALTO - 45), "t.me/RadarAletasSubastas_bot", font=get_font("arialbd.ttf", 18), fill=(59, 130, 246))

def crear_pagina_1_portada() -> Image.Image:
    """Página 1: Portada de alto impacto visual para motor."""
    img = Image.new("RGB", (A4_ANCHO, A4_ALTO), (11, 19, 43))
    draw = ImageDraw.Draw(img)

    for y in range(A4_ALTO):
        r = int(11 + (25 - 11) * (y / A4_ALTO))
        g = int(19 + (30 - 19) * (y / A4_ALTO))
        b = int(43 + (55 - 43) * (y / A4_ALTO))
        draw.line([(0, y), (A4_ANCHO, y)], fill=(r, g, b))

    # Badge superior
    badge = [100, 150, 1140, 220]
    draw.rounded_rectangle(badge, radius=16, fill=(30, 58, 138), outline=(96, 165, 250), width=2)
    draw.text((620, 185), "MANUAL PRÁCTICO OFICIAL • EDICIÓN ESPECIAL MOTOR 2026", font=get_font("arialbd.ttf", 24), fill=(191, 219, 254), anchor="mm")

    # Título Principal
    draw.text((620, 340), "CÓMO COMPRAR COCHES", font=get_font("arialbd.ttf", 52), fill=(241, 245, 249), anchor="mm")
    draw.text((620, 420), "Y VEHÍCULOS EN EL BOE", font=get_font("arialbd.ttf", 60), fill=(250, 204, 21), anchor="mm")
    draw.text((620, 500), "DESDE 500 € SIN RIESGO", font=get_font("arialbd.ttf", 54), fill=(241, 245, 249), anchor="mm")

    # Caja de subtítulo
    sub_box = [130, 580, 1110, 720]
    draw.rounded_rectangle(sub_box, radius=20, fill=(15, 23, 42), outline=(59, 130, 246), width=3)
    sub_text = (
        "El método paso a paso para acceder a turismos, SUV, furgonetas\n"
        "y motocicletas embargadas por juzgados y Seguridad Social,\n"
        "con hasta un 70% de ahorro real y 100% libre de deudas anteriores."
    )
    draw.text((620, 650), sub_text, font=get_font("arial.ttf", 26), fill=(226, 232, 240), anchor="mm", align="center")

    # 4 Bloques destacados
    puntos = [
        ("🚗 OPORTUNIDADES REALES", "Vehículos procedentes de embargos bancarios y ejecuciones judiciales con precios de salida muy inferiores a Coches.net o AutoScout24."),
        ("🛡️ CANCELACIÓN DE CARGAS", "El Decreto de Adjudicación (Art. 674 LEC) ordena a Tráfico levantar embargos y precintos sin que asumas la deuda del titular anterior."),
        ("💰 DEPÓSITO 100% REEMBOLSABLE", "El 5% de fianza exigido por el BOE se te devuelve de forma íntegra e inmediata en tu cuenta si otro postor supera tu oferta."),
        ("⚡ PUJA 100% TELEMÁTICA", "Todo el proceso se realiza desde tu ordenador o móvil con Certificado Digital o Cl@ve PIN, sin desplazarte a juzgados.")
    ]

    y_pos = 780
    for tit, desc in puntos:
        box = [100, y_pos, 1140, y_pos + 170]
        draw.rounded_rectangle(box, radius=16, fill=(15, 23, 42), outline=(51, 65, 85), width=2)
        draw.text((140, y_pos + 30), tit, font=get_font("arialbd.ttf", 24), fill=(250, 204, 21))
        # wrap desc
        palabras = desc.split(" ")
        linea1, linea2 = "", ""
        for p in palabras:
            if len(linea1) + len(p) < 70:
                linea1 += p + " "
            else:
                linea2 += p + " "
        draw.text((140, y_pos + 75), linea1.strip(), font=get_font("arial.ttf", 21), fill=(226, 232, 240))
        if linea2:
            draw.text((140, y_pos + 110), linea2.strip(), font=get_font("arial.ttf", 21), fill=(226, 232, 240))
        y_pos += 195

    draw_footer_bar(draw)
    return img

def crear_pagina_2_auditoria() -> Image.Image:
    """Página 2: Los 4 pasos obligatorios antes de pujar."""
    img = Image.new("RGB", (A4_ANCHO, A4_ALTO), (248, 250, 252))
    draw = ImageDraw.Draw(img)
    draw_header_bar(draw, 2, 3)

    draw.text((60, 110), "LOS 4 PASOS OBLIGATORIOS PARA AUDITAR UN COCHE", font=get_font("arialbd.ttf", 34), fill=(15, 23, 42))
    draw.text((60, 160), "Sigue este protocolo para pujar con máxima rentabilidad y cero sorpresas.", font=get_font("arial.ttf", 22), fill=(71, 85, 105))

    pasos = [
        ("PASO 1", "Comprobar la Ficha del BOE y Situación del Vehículo",
         "Revisa si el edicto indica que el vehículo dispone de llaves y documentación técnica (Ficha ITV y Permiso de Circulación). Si no constan, deberás solicitar duplicado en Tráfico tras adjudicártelo (coste aprox. 60 €)."),

        ("PASO 2", "Pedir el Informe Completo de la DGT (8,67 €)",
         "Con la matrícula publicada en la subasta, solicita el informe telemático en la Sede de la DGT. Verifica si existe alguna 'Reserva de Dominio' (financiación bancaria activa) o 'Leasing'. Las reservas de dominio NO se cancelan con el embargo ordinario."),

        ("PASO 3", "Inspección Presencial en el Depósito Judicial",
         "La ley te asiste para acudir al depósito municipal o campa donde custodia el vehículo la Comisión Judicial. Comprueba visualmente el estado de la chapa, neumáticos, lunas e interior antes de formular tu postura."),

        ("PASO 4", "Calcular tu Límite Máximo de Puja",
         "Regla de oro de RadarAlertas: Puja máxima = (Valor de mercado en Coches.net - 30%) - 600 € (grúa, batería, puesta a punto e ITP autonómico del 4% al 8%). Si la subasta supera esa cifra, retírate y espera al siguiente lote.")
    ]

    y_p = 220
    for num, tit, desc in pasos:
        caja = [60, y_p, 1180, y_p + 250]
        draw.rounded_rectangle(caja, radius=16, fill=(255, 255, 255), outline=(203, 213, 225), width=2)

        badge = [85, y_p + 25, 210, y_p + 65]
        draw.rounded_rectangle(badge, radius=8, fill=(239, 246, 255), outline=(59, 130, 246), width=1)
        draw.text((147, y_p + 45), num, font=get_font("arialbd.ttf", 18), fill=(30, 64, 175), anchor="mm")

        draw.text((230, y_p + 35), tit, font=get_font("arialbd.ttf", 24), fill=(15, 23, 42))

        palabras = desc.split(" ")
        lineas = []
        cur = ""
        for p in palabras:
            if len(cur) + len(p) < 85:
                cur += p + " "
            else:
                lineas.append(cur.strip())
                cur = p + " "
        if cur:
            lineas.append(cur.strip())

        ly = y_p + 85
        for l in lineas:
            draw.text((85, ly), l, font=get_font("arial.ttf", 20), fill=(51, 65, 85))
            ly += 32

        y_p += 280

    # Cuadro de alerta legal
    alerta_box = [60, 1370, 1180, 1630]
    draw.rounded_rectangle(alerta_box, radius=16, fill=(254, 243, 199), outline=(245, 158, 11), width=2)
    draw.text((100, 1400), "⚠️ ARTÍCULO 674 LEC: TU ESCUDO LEGAL", font=get_font("arialbd.ttf", 24), fill=(146, 64, 14))
    alerta_desc = (
        "El Letrado de la Administración de Justicia expedirá un 'Mandamiento de Cancelación de Cargas'\n"
        "dirigido al Registro de Bienes Muebles y a la Jefatura Provincial de Tráfico.\n"
        "Tráfico cancelará el precinto judicial y pondrá el vehículo a tu nombre limpio de la deuda del ejecutado."
    )
    draw.text((100, 1450), alerta_desc, font=get_font("arial.ttf", 21), fill=(120, 53, 15))

    draw_footer_bar(draw)
    return img

def crear_pagina_3_estrategia() -> Image.Image:
    """Página 3: Estrategia de puja y llamada a la acción hacia el canal VIP."""
    img = Image.new("RGB", (A4_ANCHO, A4_ALTO), (15, 23, 42))
    draw = ImageDraw.Draw(img)
    draw_header_bar(draw, 3, 3)

    draw.text((620, 140), "ESTRATEGIA GANADORA Y ALERTAS DIARIAS", font=get_font("arialbd.ttf", 36), fill=(255, 255, 255), anchor="mm")
    draw.text((620, 190), "¿Cómo estar seguro de no perderte ninguna ganga en tu provincia?", font=get_font("arial.ttf", 22), fill=(148, 163, 184), anchor="mm")

    # 3 Consejos de puja
    consejos = [
        ("⏱️ NO PUJES EL PRIMER DÍA", "Las subastas en el BOE duran 20 días. Pujar al inicio solo atrae la atención de otros curiosos y encarece el lote. Guarda la fecha en tu Google Calendar y revisa en las últimas 4 horas."),
        ("📉 OFERTAS POR DEBAJO DEL 50%", "En subastas de muebles (vehículos), si la mejor puja es igual o superior al 50% del valor de tasación oficial (o cubre la deuda ejecutada), el juzgado aprueba el remate automáticamente (Art. 677 LEC)."),
        ("⚡ AUTOMATIZA TU DETECCIÓN", "Revisar el BOE a mano cada día es agotador. Se publican decenas de vehículos en toda España. Nuestro bot rastrea de madrugada cada lote y te envía solo los coches verificados.")
    ]

    y_pos = 250
    for tit, desc in consejos:
        caja = [100, y_pos, 1140, y_pos + 190]
        draw.rounded_rectangle(caja, radius=16, fill=(30, 41, 59), outline=(51, 65, 85), width=2)
        draw.text((140, y_pos + 30), tit, font=get_font("arialbd.ttf", 24), fill=(250, 204, 21))
        palabras = desc.split(" ")
        lineas = []
        cur = ""
        for p in palabras:
            if len(cur) + len(p) < 75:
                cur += p + " "
            else:
                lineas.append(cur.strip())
                cur = p + " "
        if cur:
            lineas.append(cur.strip())
        ly = y_pos + 75
        for l in lineas:
            draw.text((140, ly), l, font=get_font("arial.ttf", 20), fill=(226, 232, 240))
            ly += 30
        y_pos += 220

    # Tarjeta de Oferta VIP
    vip_card = [100, 960, 1140, 1560]
    draw.rounded_rectangle(vip_card, radius=20, fill=(30, 58, 138), outline=(96, 165, 250), width=3)

    draw.text((620, 1020), "🚀 ÚNETE AL CANAL VIP DE VEHÍCULOS RADARALERTAS", font=get_font("arialbd.ttf", 30), fill=(255, 255, 255), anchor="mm")
    draw.text((620, 1070), "Recibe alertas instantáneas en Telegram filtradas con oportunidad demostrable:", font=get_font("arial.ttf", 22), fill=(191, 219, 254), anchor="mm")

    features = [
        "✔ Matrícula, marca, modelo, año y kilometraje registrado.",
        "✔ Enlace directo a Google Maps con ubicación de la campa de depósito.",
        "✔ Comparador en 1 clic de cotización real en Coches.net.",
        "✔ Recordatorio 1 clic en Google Calendar con alarma 2h antes del cierre.",
        "✔ Expediente judicial directo para pujar sin intermediarios."
    ]

    fy = 1120
    for f in features:
        draw.text((160, fy), f, font=get_font("arialbd.ttf", 21), fill=(255, 255, 255))
        fy += 45

    # Botón CTA
    btn = [160, 1370, 1080, 1460]
    draw.rounded_rectangle(btn, radius=20, fill=(37, 99, 235), outline=(147, 197, 253), width=2)
    draw.text((620, 1415), "👉 ACTIVAR CANAL VEHÍCULOS (DESDE 2,99 €/MES)", font=get_font("arialbd.ttf", 26), fill=(255, 255, 255), anchor="mm")

    draw.text((620, 1505), "O desbloquea los 5 canales (Pisos, Coches, Ayudas, Licitaciones, Empleo) por solo 4,99 € / mes", font=get_font("arialbd.ttf", 20), fill=(250, 204, 21), anchor="mm")

    draw_footer_bar(draw)
    return img

def compilar_guia_coches_pdf(ruta_destino: Path) -> Path:
    """Compila las 3 páginas de la guía de vehículos en un único archivo PDF."""
    print("🚗 Compilando páginas de la Guía Oficial de Coches Embargados...")
    p1 = crear_pagina_1_portada()
    p2 = crear_pagina_2_auditoria()
    p3 = crear_pagina_3_estrategia()

    p1.save(
        ruta_destino,
        "PDF",
        resolution=150.0,
        save_all=True,
        append_images=[p2, p3],
        quality=95
    )
    print(f"✅ ¡Guía de Coches Embargados generada en: {ruta_destino} ({ruta_destino.stat().st_size / 1024:.1f} KB)")
    return ruta_destino

if __name__ == "__main__":
    out_pdf = ASSETS_DIR / "Guia_Coches_Embargados_RadarAlertas.pdf"
    compilar_guia_coches_pdf(out_pdf)
