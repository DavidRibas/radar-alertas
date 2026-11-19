"""
Generador Maestro del Pack de Vídeos Promocionales (Stitch + BMad Style)
Produce los 3 vídeos para los otros servicios de RadarAlertas listos para el envío de las 19:00:
1. VEHÍCULOS EMBARGADOS (Subastas judiciales DGT / Hacienda)
2. AYUDAS Y SUBVENCIONES (BDNS / Fondos Europeos a fondo perdido)
3. LICITACIONES PÚBLICAS (Contratos menores del Estado con cobro garantizado)
"""
import asyncio
import base64
import os
import shutil
import subprocess
from pathlib import Path
import edge_tts
from playwright.async_api import async_playwright

BASE_DIR = Path("C:/Ideas/radar-alertas")
OUTPUT_DIR = BASE_DIR / "output"
TEMPLATES_DIR = BASE_DIR / "assets" / "templates"
AUDIO_BEAT = OUTPUT_DIR / "pro_tension_beat.wav"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

VOICE = "es-ES-AlvaroNeural"


def img_to_b64(path: Path) -> str:
    with open(path, "rb") as f:
        return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode('utf-8')}"


# ==============================================================================
# CONFIGURACIÓN DE LOS 3 SERVICIOS
# ==============================================================================
SERVICES_CONFIG = {
    "vehiculos": {
        "output_filename": "VIDEO_VEHICULOS_PROMO.mp4",
        "bg_img": TEMPLATES_DIR / "vehiculo_coche_oficial.jpg",
        "hud_tag": "SUBASTA JUDICIAL DGT / BOE",
        "hud_meta": "📍 DGT • Madrid / Tráfico",
        "hero_tag": "VEHÍCULOS Y EMBARGOS PÚBLICOS",
        "headline": "BMW Serie 3 Berlina que sale a Subasta por 4.800 €",
        "specs": ["🚘 Año 2021", "⛽ Diésel 190 CV", "⚙️ Automático", "🛣️ 68.000 km", "⚖️ Juzgado 1ª Instancia"],
        "market_label": "MERCADO OCASIÓN (COCHES.NET)",
        "market_price": "24.500 €",
        "market_sub": "Precio medio en concesionario con garantía estándar",
        "boe_label": "PRECIO SALIDA SUBASTA BOE",
        "hero_target_price": "4.800 €",
        "hero_int_price": 4800,
        "discount": "-80%",
        "discount_int": 80,
        "clean_margin": "+19.700 €",
        "margin_int": 19700,
        "margin_quote": "“HABLAMOS DE 19.700 € DE MARGEN LIMPIO”",
        "legal_title": "PREVIO REGISTRO DGT: 0,00 € DE CARGAS",
        "legal_sub": "Cancelación de precintos y multas por Mandamiento Judicial",
        "audit_item1": "Estado: <span style='color:#4ade80;'>Libre de precintos / Llaves y ficha</span>",
        "audit_item2": "Fianza 5%: <span style='color:#38bdf8;'>Retornable si no ganas</span>",
        "guion": (
            "Fijaos en lo que acaba de publicar el portal de subastas del BOE. "
            "Un BMW Serie 3 del año dos mil veintiuno, automático y con sesenta y ocho mil kilómetros, por tan solo cuatro mil ochocientos euros. "
            "En portales de segunda mano como Coches punto net, este mismo coche supera los veinticuatro mil euros. "
            "Estamos hablando de casi veinte mil euros de margen, y el juzgado cancela cualquier multa o precinto anterior por mandamiento judicial. "
            "Pero esto no es casualidad. RadarAlertas escanea el BOE y la DGT cada madrugada para avisarte en Telegram de las mejores subastas de coches, pisos y ayudas antes que nadie. "
            "Entra al enlace de mi biografía, únete gratis al canal y descarga la Guía en PDF."
        )
    },
    "ayudas": {
        "output_filename": "VIDEO_AYUDAS_PROMO.mp4",
        "bg_img": TEMPLATES_DIR / "ayuda_dinero_euros.jpg",
        "hud_tag": "BDNS • FONDOS PÚBLICOS ACTIVOS",
        "hud_meta": "📍 Convocatoria Oficial Abierta",
        "hero_tag": "AYUDAS Y SUBVENCIONES ESTATALES",
        "headline": "Hasta 12.000 € a Fondo Perdido para Autónomos y Pymes",
        "specs": ["💶 Fondos Europeos", "💼 Autónomos y Pymes", "🏛️ BDNS Oficial", "📅 Plazo Abierto Hoy", "✅ Sin Devolución"],
        "market_label": "PRÉSTAMO BANCARIO COMERCIAL",
        "market_price": "12.000 € (+8,5% INTERÉS)",
        "market_sub": "Devolución obligatoria con intereses y comisiones de apertura",
        "boe_label": "SUBVENCIÓN PÚBLICA DIRECTA",
        "hero_target_price": "12.000 € (0 € COSTE)",
        "hero_int_price": 12000,
        "discount": "100% SUBVENCIONADO",
        "discount_int": 100,
        "clean_margin": "+12.000 € NETOS",
        "margin_int": 12000,
        "margin_quote": "“DINERO DIRECTO 100% A FONDO PERDIDO”",
        "legal_title": "RESOLUCIÓN OFICIAL PUBLICADA EN BDNS",
        "legal_sub": "Ingreso directo en cuenta bancaria tras justificación de actividad",
        "audit_item1": "Devolución: <span style='color:#4ade80;'>0,00 € (No reembolsable)</span>",
        "audit_item2": "Concurrencia: <span style='color:#38bdf8;'>Por orden de solicitud</span>",
        "guion": (
            "Atención autónomos y pequeñas empresas, porque el Estado acaba de publicar una nueva partida de ayudas directas. "
            "Hasta doce mil euros a fondo perdido para digitalización, modernización y gastos de negocio. "
            "A diferencia de un crédito bancario con intereses, esta subvención no se devuelve. Son fondos europeos directos a tu cuenta. "
            "¿Cuál es el problema habitual? Que nadie se entera a tiempo y los fondos se agotan. "
            "RadarAlertas monitoriza la Base de Datos Nacional de Subvenciones cada mañana y te avisa a Telegram con los requisitos listos para solicitarla en un clic. "
            "Entra al enlace de mi biografía, únete al canal gratuito y no dejes escapar las ayudas que te corresponden."
        )
    },
    "licitaciones": {
        "output_filename": "VIDEO_LICITACIONES_PROMO.mp4",
        "bg_img": TEMPLATES_DIR / "licitacion_contrato_oficial.jpg",
        "hud_tag": "PLATAFORMA CONTRATACIÓN ESTADO",
        "hud_meta": "📍 Contrato Menor Publicado",
        "hero_tag": "CONTRATOS MENORES DEL ESTADO",
        "headline": "Contrato de 42.000 € para Autónomos y Pymes Locales",
        "specs": ["📋 Contrato Menor", "🏛️ Ayuntamiento / CCAA", "⏱️ Presentación en 7 Días", "💶 Pago por Ley a 30 Días", "🏢 Sin Gran Burocracia"],
        "market_label": "CLIENTE PRIVADO TRADICIONAL",
        "market_price": "RIESGO DE IMPAGO / 90 DÍAS",
        "market_sub": "Pagarés, retrasos en cobro y riesgo de quiebra comercial",
        "boe_label": "CONTRATO MENOR DEL ESTADO",
        "hero_target_price": "42.000 € (GARANTIZADOS)",
        "hero_int_price": 42000,
        "discount": "PAGO ASEGURADO POR LEY",
        "discount_int": 100,
        "clean_margin": "+42.000 € FACTURACIÓN",
        "margin_int": 42000,
        "margin_quote": "“FACTURA AL ESTADO CON COBRO PUNTUAL GARANTIZADO”",
        "legal_title": "ADJUDICACIÓN TRANSPARENTE POR LEY 9/2017",
        "legal_sub": "Cobro directo avalado por la Ley de Contratos del Sector Público",
        "audit_item1": "Solvencia: <span style='color:#4ade80;'>Acreditación básica de oficio</span>",
        "audit_item2": "Plazo cobro: <span style='color:#38bdf8;'>Máximo 30 días garantizados</span>",
        "guion": (
            "¿Tienes una empresa o eres autónomo y buscas clientes que paguen puntual? "
            "El Sector Público acaba de publicar contratos menores de mantenimiento, obras y servicios por importes de hasta cuarenta y dos mil euros. "
            "Sin avales bancarios complejos ni burocracia de grandes licitaciones, y con el cobro legalmente garantizado a treinta días. "
            "En RadarAlertas filtramos cada madrugada la Plataforma de Contratación del Estado y te enviamos a Telegram los contratos menores de tu sector y provincia para que presentes tu oferta antes que nadie. "
            "Entra al enlace de mi biografía y únete gratis a nuestro canal de alertas."
        )
    }
}


def build_service_card_html(cfg: dict, bg_uri: str, step_dict: dict) -> str:
    boe_style = "box-shadow: 0 20px 60px rgba(0, 0, 0, 0.75), 0 0 50px rgba(16, 185, 129, 0.65); transform: scale(1.02); border-color: #00ff88;" if step_dict.get("glow_boe") else "box-shadow: 0 16px 40px rgba(0, 0, 0, 0.65);"
    market_style = "box-shadow: 0 20px 50px rgba(0, 0, 0, 0.75), 0 0 45px rgba(239, 68, 68, 0.65); transform: scale(1.02); border-color: #ef4444;" if step_dict.get("glow_market") else "box-shadow: 0 14px 35px rgba(0, 0, 0, 0.6);"
    legal_style = "box-shadow: 0 20px 50px rgba(0, 0, 0, 0.75), 0 0 45px rgba(56, 189, 248, 0.65); transform: scale(1.02); border-color: #38bdf8;" if step_dict.get("glow_legal") else "box-shadow: 0 12px 30px rgba(0, 0, 0, 0.55);"

    price_val = step_dict.get("price", cfg["hero_target_price"])
    disc_val = step_dict.get("disc", cfg["discount"])
    strike_val = step_dict.get("strike", "calc(100% + 16px)")
    margin_val = step_dict.get("margin", cfg["clean_margin"])
    quote_val = step_dict.get("quote", cfg["margin_quote"])

    specs_pills = "".join(f'<div class="spec-pill">{s}</div>' for s in cfg["specs"])

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Space+Grotesk:wght@700;800;900&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', sans-serif; -webkit-font-smoothing: antialiased; }}
        body {{
            width: 1080px; height: 1920px; background: #060913; color: #ffffff;
            position: relative; overflow: hidden; display: flex; flex-direction: column;
            justify-content: space-between; padding: 68px 46px 82px;
        }}
        .bg-drone {{
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-image: url('{bg_uri}'); background-size: cover; background-position: center;
            opacity: 0.72; filter: saturate(1.2) contrast(1.15) brightness(0.85); z-index: 0;
        }}
        .bg-overlay {{
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: radial-gradient(circle at 50% 25%, rgba(37, 99, 235, 0.16) 0%, transparent 65%),
                        linear-gradient(180deg, rgba(6, 9, 19, 0.42) 0%, rgba(6, 9, 19, 0.85) 100%);
            z-index: 1;
        }}
        .content {{
            position: relative; z-index: 2; display: flex; flex-direction: column;
            gap: 18px; height: 100%; justify-content: space-between;
        }}
        .hud-header {{
            display: flex; justify-content: space-between; align-items: center;
            padding: 14px 26px; background: rgba(15, 23, 42, 0.9); border: 1.5px solid rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(20px); border-radius: 999px;
        }}
        .hud-live {{ display: flex; align-items: center; gap: 12px; font-size: 20px; font-weight: 800; color: #ef4444; letter-spacing: 1.5px; text-transform: uppercase; }}
        .pulse-dot {{ width: 14px; height: 14px; background: #ef4444; border-radius: 50%; box-shadow: 0 0 18px #ef4444; }}
        .hud-gps {{ font-size: 19px; font-weight: 700; color: #38bdf8; letter-spacing: 0.5px; }}

        .hero-block {{ display: flex; flex-direction: column; gap: 8px; }}
        .hero-eyebrow {{ font-size: 21px; font-weight: 800; color: #38bdf8; letter-spacing: 2px; text-transform: uppercase; }}
        .hero-headline {{ font-family: 'Space Grotesk', sans-serif; font-size: 50px; font-weight: 900; line-height: 1.1; letter-spacing: -1.5px; color: #ffffff; }}
        .specs-row {{ display: flex; gap: 8px; flex-wrap: wrap; margin-top: 4px; }}
        .spec-pill {{ background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255, 255, 255, 0.2); padding: 6px 14px; border-radius: 8px; font-size: 18px; font-weight: 700; color: #e2e8f0; }}

        .card-market {{ background: rgba(20, 15, 25, 0.82); border: 1.5px solid rgba(239, 68, 68, 0.5); backdrop-filter: blur(20px); border-radius: 24px; padding: 24px 32px; display: flex; flex-direction: column; gap: 8px; {market_style} }}
        .badge-market {{ display: inline-flex; align-items: center; background: rgba(239, 68, 68, 0.2); border: 1px solid rgba(239, 68, 68, 0.5); padding: 5px 14px; border-radius: 999px; font-size: 17px; font-weight: 700; color: #fca5a5; width: fit-content; }}
        .price-market-box {{ position: relative; width: fit-content; }}
        .price-market {{ font-family: 'Space Grotesk', sans-serif; font-size: 66px; font-weight: 800; color: #ef4444; letter-spacing: -2px; }}
        .strikethrough-line {{ position: absolute; left: -8px; top: 50%; height: 6px; background: #ef4444; transform: rotate(-6deg); border-radius: 3px; box-shadow: 0 0 14px rgba(239, 68, 68, 0.95); width: {strike_val}; }}
        .market-sub {{ font-size: 18px; color: #cbd5e1; font-weight: 500; }}

        .card-boe {{ background: linear-gradient(135deg, rgba(6, 78, 59, 0.88) 0%, rgba(15, 23, 42, 0.92) 100%); border: 2px solid rgba(16, 185, 129, 0.9); backdrop-filter: blur(24px); border-radius: 28px; padding: 28px 36px; display: flex; flex-direction: column; gap: 12px; {boe_style} }}
        .badge-boe {{ display: inline-flex; align-items: center; background: #10b981; box-shadow: 0 0 16px rgba(16, 185, 129, 0.5); padding: 7px 20px; border-radius: 999px; font-size: 19px; font-weight: 800; color: #064e3b; width: fit-content; }}
        .price-boe {{ font-family: 'Space Grotesk', sans-serif; font-size: 96px; font-weight: 900; color: #00ff88; line-height: 1; letter-spacing: -3px; text-shadow: 0 0 35px rgba(0, 255, 136, 0.65); }}
        .boe-row {{ display: flex; align-items: center; justify-content: space-between; }}
        .discount-pill {{ background: rgba(16, 185, 129, 0.25); border: 1.5px solid #10b981; padding: 7px 18px; border-radius: 10px; font-size: 22px; font-weight: 800; color: #ffffff; }}
        .boe-margin {{ font-size: 22px; font-weight: 700; color: #a7f3d0; }}

        .card-legal {{ background: rgba(2, 132, 199, 0.22); border: 1.5px solid rgba(56, 189, 248, 0.5); backdrop-filter: blur(20px); border-radius: 22px; padding: 18px 26px; display: flex; flex-direction: column; gap: 10px; {legal_style} }}
        .legal-top {{ display: flex; align-items: center; gap: 16px; }}
        .legal-icon {{ width: 48px; height: 48px; background: rgba(56, 189, 248, 0.2); border: 1px solid rgba(56, 189, 248, 0.4); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #38bdf8; flex-shrink: 0; }}
        .legal-title {{ font-size: 21px; font-weight: 800; color: #ffffff; }}
        .legal-sub {{ font-size: 16px; color: #bae6fd; font-weight: 600; }}
        .legal-audit-pills {{ display: flex; justify-content: space-between; border-top: 1px solid rgba(255, 255, 255, 0.12); padding-top: 8px; font-size: 16px; }}
        .audit-item {{ color: #cbd5e1; font-weight: 600; }}

        .margin-hook {{ background: rgba(0, 0, 0, 0.9); border: 2px solid rgba(245, 158, 11, 0.9); box-shadow: 0 0 35px rgba(245, 158, 11, 0.35); border-radius: 20px; padding: 18px 24px; text-align: center; }}
        .margin-quote {{ font-family: 'Space Grotesk', sans-serif; font-size: 32px; font-weight: 800; color: #fbbf24; letter-spacing: -0.5px; text-transform: uppercase; }}

        .cta-btn {{ background: #2563eb; border: 1.5px solid rgba(147, 197, 253, 0.5); border-radius: 24px; padding: 24px 32px; display: flex; align-items: center; justify-content: space-between; }}
        .cta-main {{ font-size: 26px; font-weight: 800; color: #ffffff; letter-spacing: -0.5px; }}
        .cta-sub {{ font-size: 17px; color: rgba(255, 255, 255, 0.9); font-weight: 600; }}
        .cta-arrow {{ width: 50px; height: 50px; background: rgba(255, 255, 255, 0.22); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; }}
    </style>
</head>
<body>
    <div class="bg-drone"></div>
    <div class="bg-overlay"></div>
    <div class="content">
        <div class="hud-header">
            <div class="hud-live"><div class="pulse-dot"></div> {cfg["hud_tag"]}</div>
            <div class="hud-gps">{cfg["hud_meta"]}</div>
        </div>
        <div class="hero-block">
            <div class="hero-eyebrow">{cfg["hero_tag"]}</div>
            <div class="hero-headline">{cfg["headline"]}</div>
            <div class="specs-row">{specs_pills}</div>
        </div>
        <div class="card-market">
            <div class="badge-market">{cfg["market_label"]}</div>
            <div class="price-market-box">
                <div class="price-market">{cfg["market_price"]}</div>
                <div class="strikethrough-line"></div>
            </div>
            <div class="market-sub">{cfg["market_sub"]}</div>
        </div>
        <div class="card-boe">
            <div class="badge-boe">{cfg["boe_label"]}</div>
            <div class="price-boe">{price_val}</div>
            <div class="boe-row">
                <div class="discount-pill">AHORRO: {disc_val}</div>
                <div class="boe-margin">Margen bruto: {margin_val}</div>
            </div>
        </div>
        <div class="card-legal">
            <div class="legal-top">
                <div class="legal-icon">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>
                    </svg>
                </div>
                <div>
                    <div class="legal-title">{cfg["legal_title"]}</div>
                    <div class="legal-sub">{cfg["legal_sub"]}</div>
                </div>
            </div>
            <div class="legal-audit-pills">
                <div class="audit-item">{cfg["audit_item1"]}</div>
                <div class="audit-item">{cfg["audit_item2"]}</div>
            </div>
        </div>
        <div class="margin-hook">
            <div class="margin-quote">{quote_val}</div>
        </div>
        <div class="cta-btn">
            <div class="cta-left">
                <div class="cta-main">Guía Práctica Oficial en PDF (0 €)</div>
                <div class="cta-sub">Descárgala gratis en el enlace del perfil</div>
            </div>
            <div class="cta-arrow">➔</div>
        </div>
    </div>
</body>
</html>"""


def build_platform_pitch_html(bg_uri: str, glow_cta: bool = False) -> str:
    cta_style = "box-shadow: 0 20px 60px rgba(37, 99, 235, 0.95), 0 0 50px rgba(59, 130, 246, 0.85); transform: scale(1.02); border: 2px solid #ffffff;" if glow_cta else "box-shadow: 0 16px 45px rgba(37, 99, 235, 0.55);"

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Space+Grotesk:wght@700;800;900&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', sans-serif; -webkit-font-smoothing: antialiased; }}
        body {{
            width: 1080px; height: 1920px; background: #060913; color: #ffffff;
            position: relative; overflow: hidden; display: flex; flex-direction: column;
            justify-content: space-between; padding: 75px 48px 90px;
        }}
        .bg-drone {{
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-image: url('{bg_uri}'); background-size: cover; background-position: center;
            opacity: 0.65; filter: saturate(1.1) contrast(1.1) brightness(0.75); z-index: 0;
        }}
        .bg-overlay {{
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: radial-gradient(circle at 50% 20%, rgba(37, 99, 235, 0.22) 0%, transparent 70%),
                        linear-gradient(180deg, rgba(6, 9, 19, 0.55) 0%, rgba(6, 9, 19, 0.9) 100%);
            z-index: 1;
        }}
        .content {{
            position: relative; z-index: 2; display: flex; flex-direction: column;
            gap: 22px; height: 100%; justify-content: space-between;
        }}
        .hud-header {{
            display: flex; justify-content: space-between; align-items: center;
            padding: 14px 28px; background: rgba(15, 23, 42, 0.92); border: 1.5px solid rgba(56, 189, 248, 0.4);
            backdrop-filter: blur(20px); border-radius: 999px; box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        }}
        .hud-brand {{ display: flex; align-items: center; gap: 12px; font-size: 21px; font-weight: 900; color: #38bdf8; letter-spacing: 1.5px; text-transform: uppercase; }}
        .pulse-dot {{ width: 14px; height: 14px; background: #38bdf8; border-radius: 50%; box-shadow: 0 0 18px #38bdf8; }}
        .hud-status {{ font-size: 18px; font-weight: 700; color: #a7f3d0; }}

        .platform-hero {{ display: flex; flex-direction: column; gap: 12px; text-align: center; margin-top: 10px; }}
        .platform-badge {{
            display: inline-flex; align-items: center; justify-content: center; align-self: center;
            background: rgba(56, 189, 248, 0.18); border: 1.5px solid rgba(56, 189, 248, 0.4);
            padding: 8px 24px; border-radius: 999px; font-size: 19px; font-weight: 800; color: #38bdf8;
            letter-spacing: 1.5px; text-transform: uppercase;
        }}
        .platform-title {{
            font-family: 'Space Grotesk', sans-serif; font-size: 58px; font-weight: 900;
            line-height: 1.1; letter-spacing: -2px; color: #ffffff; text-shadow: 0 4px 28px rgba(0,0,0,0.9);
        }}
        .platform-desc {{
            font-size: 22px; color: #cbd5e1; font-weight: 500; max-width: 900px; margin: 0 auto; line-height: 1.4;
        }}

        .features-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 10px 0; }}
        .feat-card {{
            background: rgba(15, 23, 42, 0.88); border: 1.5px solid rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(24px); border-radius: 24px; padding: 26px 24px;
            display: flex; flex-direction: column; gap: 10px; box-shadow: 0 14px 35px rgba(0,0,0,0.6);
        }}
        .feat-icon-row {{ display: flex; align-items: center; justify-content: space-between; }}
        .feat-icon {{ font-size: 38px; }}
        .feat-tag {{ font-size: 14px; font-weight: 800; padding: 4px 10px; border-radius: 6px; text-transform: uppercase; letter-spacing: 0.5px; }}
        .tag-boe {{ background: rgba(16, 185, 129, 0.2); color: #4ade80; border: 1px solid rgba(16, 185, 129, 0.5); }}
        .tag-dgt {{ background: rgba(56, 189, 248, 0.2); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.5); }}
        .tag-ayudas {{ background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.5); }}
        .tag-licit {{ background: rgba(168, 85, 247, 0.2); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.5); }}
        .feat-title {{ font-size: 23px; font-weight: 800; color: #ffffff; }}
        .feat-text {{ font-size: 17px; color: #94a3b8; line-height: 1.35; font-weight: 500; }}

        .trust-banner {{
            background: linear-gradient(135deg, rgba(6, 78, 59, 0.85) 0%, rgba(15, 23, 42, 0.90) 100%);
            border: 2px solid #10b981; border-radius: 22px; padding: 22px 30px;
            display: flex; align-items: center; justify-content: space-between;
            box-shadow: 0 0 30px rgba(16, 185, 129, 0.3);
        }}
        .trust-left {{ display: flex; align-items: center; gap: 16px; }}
        .trust-icon {{ font-size: 32px; }}
        .trust-title {{ font-size: 22px; font-weight: 900; color: #ffffff; }}
        .trust-sub {{ font-size: 17px; color: #a7f3d0; font-weight: 600; }}
        .trust-badge-pill {{ background: #10b981; color: #064e3b; font-weight: 900; font-size: 18px; padding: 8px 18px; border-radius: 999px; }}

        .cta-btn {{
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            border: 2px solid rgba(147, 197, 253, 0.6); border-radius: 28px;
            padding: 28px 36px; display: flex; align-items: center; justify-content: space-between;
            {cta_style}
        }}
        .cta-left {{ display: flex; flex-direction: column; gap: 5px; }}
        .cta-main {{ font-size: 28px; font-weight: 900; color: #ffffff; letter-spacing: -0.5px; }}
        .cta-sub {{ font-size: 18px; color: rgba(255, 255, 255, 0.92); font-weight: 600; }}
        .cta-arrow {{ width: 56px; height: 56px; background: rgba(255, 255, 255, 0.22); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 26px; }}
    </style>
</head>
<body>
    <div class="bg-drone"></div>
    <div class="bg-overlay"></div>
    <div class="content">
        <div class="hud-header">
            <div class="hud-brand"><div class="pulse-dot"></div> RADARALERTAS.ES</div>
            <div class="hud-status">● Monitorizando Boletines Oficiales</div>
        </div>
        <div class="platform-hero">
            <div class="platform-badge">TECNOLOGÍA DE MONITORIZACIÓN PÚBLICA</div>
            <div class="platform-title">El Radar que escanea el Estado por ti 24/7</div>
            <div class="platform-desc">Auditamos cada madrugada el BOE, Catastro y los registros oficiales para avisarte directamente a Telegram antes de que salgan al mercado.</div>
        </div>
        <div class="features-grid">
            <div class="feat-card">
                <div class="feat-icon-row"><span class="feat-icon">🏠</span><span class="feat-tag tag-boe">BOE JUDICIAL</span></div>
                <div class="feat-title">Subastas Inmuebles</div>
                <div class="feat-text">Pisos y chalets con hasta un 70% de ahorro frente a portales.</div>
            </div>
            <div class="feat-card">
                <div class="feat-icon-row"><span class="feat-icon">🚗</span><span class="feat-tag tag-dgt">DGT / HACIENDA</span></div>
                <div class="feat-title">Coches Embargados</div>
                <div class="feat-text">Vehículos con tasación oficial y comprobación de cargas 0€.</div>
            </div>
            <div class="feat-card">
                <div class="feat-icon-row"><span class="feat-icon">💶</span><span class="feat-tag tag-ayudas">BDNS / FONDOS</span></div>
                <div class="feat-title">Ayudas y Subvenciones</div>
                <div class="feat-text">Fondos a fondo perdido para autónomos, pymes y familias.</div>
            </div>
            <div class="feat-card">
                <div class="feat-icon-row"><span class="feat-icon">📋</span><span class="feat-tag tag-licit">ESTADO</span></div>
                <div class="feat-title">Licitaciones y Empleo</div>
                <div class="feat-text">Contratos públicos menores y convocatorias oficiales activas.</div>
            </div>
        </div>
        <div class="trust-banner">
            <div class="trust-left">
                <span class="trust-icon">⚡</span>
                <div>
                    <div class="trust-title">Alertas en tiempo real a tu Telegram</div>
                    <div class="trust-sub">Canal abierto sin costes ni permanencias</div>
                </div>
            </div>
            <div class="trust-badge-pill">100% GRATIS</div>
        </div>
        <div class="cta-btn">
            <div class="cta-left">
                <div class="cta-main">Únete al Canal Gratis + Guía en PDF</div>
                <div class="cta-sub">Accede directo desde el enlace de mi biografía</div>
            </div>
            <div class="cta-arrow">➔</div>
        </div>
    </div>
</body>
</html>"""


async def procesar_servicio(service_key: str, browser) -> Path:
    cfg = SERVICES_CONFIG[service_key]
    print(f"\n==================================================")
    print(f"🚀 GENERANDO VÍDEO: {service_key.upper()} ({cfg['output_filename']})")
    print(f"==================================================")

    # 1. Locución neural
    print("🎙️ 1. Generando locución...")
    audio_path = OUTPUT_DIR / f"{service_key}_audio.mp3"
    tts = edge_tts.Communicate(text=cfg["guion"], voice=VOICE, rate="+6%")
    await tts.save(str(audio_path))

    cmd_dur = ["ffmpeg", "-i", str(audio_path), "-f", "null", "-"]
    res = subprocess.run(cmd_dur, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    duracion_real = 35.0
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            partes = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = partes.split(":")
            duracion_real = float(h) * 3600 + float(m) * 60 + float(s)
            break
    print(f"  ✓ Duración de locución: {duracion_real:.2f} s")

    # 2. Fotogramas dinámicos específicos para este servicio
    p_step1 = int(cfg["hero_int_price"] * 0.25)
    p_step2 = int(cfg["hero_int_price"] * 0.60)
    p_step3 = int(cfg["hero_int_price"] * 0.85)
    m_step1 = int(cfg["margin_int"] * 0.35)
    m_step2 = int(cfg["margin_int"] * 0.70)

    steps = [
        # PARTE 1: CASO REAL
        {"type": "prop", "dur": 0.25, "price": f"{p_step1:,} €".replace(",", "."), "disc": "-20%", "strike": "0%", "margin": "+0 €", "quote": "“BUSCANDO OPORTUNIDAD...”", "glow_boe": True},
        {"type": "prop", "dur": 0.25, "price": f"{p_step2:,} €".replace(",", "."), "disc": "-45%", "strike": "0%", "margin": "+0 €", "quote": "“ANALIZANDO EXPEDIENTE...”", "glow_boe": True},
        {"type": "prop", "dur": 0.25, "price": f"{p_step3:,} €".replace(",", "."), "disc": "-65%", "strike": "0%", "margin": "+0 €", "quote": "“CRUCE CON MERCADO...”", "glow_boe": True},
        {"type": "prop", "dur": 0.35, "price": cfg["hero_target_price"], "disc": cfg["discount"], "strike": "0%", "margin": "+0 €", "quote": "“¡OPORTUNIDAD DETECTADA!”", "glow_boe": True},
        {"type": "prop", "dur": 2.50, "price": cfg["hero_target_price"], "disc": cfg["discount"], "strike": "0%", "margin": "+0 €", "quote": cfg["margin_quote"], "glow_boe": True},
        
        # Tachado de mercado
        {"type": "prop", "dur": 0.25, "price": cfg["hero_target_price"], "disc": cfg["discount"], "strike": "35%", "margin": "+0 €", "quote": cfg["margin_quote"], "glow_market": True},
        {"type": "prop", "dur": 0.25, "price": cfg["hero_target_price"], "disc": cfg["discount"], "strike": "75%", "margin": "+0 €", "quote": cfg["margin_quote"], "glow_market": True},
        {"type": "prop", "dur": 3.00, "price": cfg["hero_target_price"], "disc": cfg["discount"], "strike": "calc(100% + 16px)", "margin": "+0 €", "quote": cfg["margin_quote"], "glow_market": True},

        # Margen / Beneficio dinámico
        {"type": "prop", "dur": 0.30, "price": cfg["hero_target_price"], "disc": cfg["discount"], "strike": "calc(100% + 16px)", "margin": f"+{m_step1:,} €".replace(",", "."), "quote": "“CALCULANDO RENTABILIDAD...”"},
        {"type": "prop", "dur": 0.30, "price": cfg["hero_target_price"], "disc": cfg["discount"], "strike": "calc(100% + 16px)", "margin": f"+{m_step2:,} €".replace(",", "."), "quote": "“CALCULANDO RENTABILIDAD...”"},
        {"type": "prop", "dur": 0.30, "price": cfg["hero_target_price"], "disc": cfg["discount"], "strike": "calc(100% + 16px)", "margin": cfg["clean_margin"], "quote": cfg["margin_quote"]},
        {"type": "prop", "dur": 3.00, "price": cfg["hero_target_price"], "disc": cfg["discount"], "strike": "calc(100% + 16px)", "margin": cfg["clean_margin"], "quote": cfg["margin_quote"]},

        # Auditoría Legal
        {"type": "prop", "dur": 6.50, "price": cfg["hero_target_price"], "disc": cfg["discount"], "strike": "calc(100% + 16px)", "margin": cfg["clean_margin"], "quote": cfg["margin_quote"], "glow_legal": True},

        # PARTE 2: PITCH RADARALERTAS
        {"type": "platform", "dur": 7.00, "glow_cta": False},
        {"type": "platform", "dur": 6.50, "glow_cta": True},
    ]

    duracion_base = sum(s["dur"] for s in steps)
    factor = duracion_real / duracion_base

    # 3. Renderizar frames PNG con Playwright
    print("🎨 2. Renderizando fotogramas PNG lossless a 1080x1920...")
    frames_sub_dir = OUTPUT_DIR / f"frames_{service_key}"
    frames_sub_dir.mkdir(parents=True, exist_ok=True)
    
    bg_uri_service = img_to_b64(cfg["bg_img"])
    bcn_bg_uri = img_to_b64(TEMPLATES_DIR / "barcelona_aerea.jpg")
    
    page = await browser.new_page(viewport={"width": 1080, "height": 1920})
    frame_files = []

    for idx, s in enumerate(steps, 1):
        if s["type"] == "prop":
            html = build_service_card_html(cfg, bg_uri_service, s)
        else:
            html = build_platform_pitch_html(bcn_bg_uri, glow_cta=s.get("glow_cta", False))
            
        await page.set_content(html, wait_until="networkidle")
        frame_png = frames_sub_dir / f"f_{idx:02d}.png"
        await page.screenshot(path=str(frame_png))
        frame_files.append((frame_png, s["dur"]))
        
    await page.close()

    # 4. Compilar con FFmpeg a 6 Mbps
    print("🎬 3. Ensamblando clips y codificando vídeo...")
    clips = []
    for i, (f_path, dur) in enumerate(frame_files, 1):
        dur_adj = dur * factor
        clip_mp4 = frames_sub_dir / f"c_{i:02d}.mp4"
        cmd = [
            "ffmpeg", "-y", "-loop", "1", "-t", f"{dur_adj:.3f}",
            "-i", str(f_path),
            "-c:v", "libx264", "-b:v", "6000k", "-preset", "veryfast", "-pix_fmt", "yuv420p",
            "-an", str(clip_mp4)
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        clips.append(clip_mp4)

    concat_txt = frames_sub_dir / "concat.txt"
    with open(concat_txt, "w") as f:
        for c in clips:
            f.write(f"file '{c.name}'\n")

    raw_mp4 = frames_sub_dir / "raw.mp4"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c", "copy", str(raw_mp4)], check=True)

    ruta_final = OUTPUT_DIR / cfg["output_filename"]
    print(f"🎵 4. Mezclando locución y música de tensión en {ruta_final.name}...")
    
    if AUDIO_BEAT.exists():
        cmd_final = [
            "ffmpeg", "-y",
            "-i", str(raw_mp4),
            "-i", str(audio_path),
            "-stream_loop", "-1", "-i", str(AUDIO_BEAT),
            "-filter_complex",
            "[1:a]volume=1.0[v];[2:a]volume=0.14[m];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]",
            "-map", "0:v", "-map", "[a]",
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            "-t", f"{duracion_real:.2f}",
            str(ruta_final)
        ]
    else:
        cmd_final = ["ffmpeg", "-y", "-i", str(raw_mp4), "-i", str(audio_path), "-c:v", "copy", "-c:a", "aac", "-t", f"{duracion_real:.2f}", str(ruta_final)]

    subprocess.run(cmd_final, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    print(f"✅ VÍDEO FINAL {service_key.upper()} COMPLETADO: {ruta_final}")
    return ruta_final


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # Procesar los 3 servicios secuencialmente
        for s_key in ["vehiculos", "ayudas", "licitaciones"]:
            await procesar_servicio(s_key, browser)
            
        await browser.close()

    print("\n🎉🎉 PACK COMPLETO DE LOS 3 SERVICIOS LISTO PARA EL ENVÍO DE LAS 19:00 🎉🎉")


if __name__ == "__main__":
    asyncio.run(main())
