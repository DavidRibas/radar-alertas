"""
Generador de Vídeo de Alto Impacto con Presentación del Ecosistema RadarAlertas
Estructura:
1. Caso Real Barcelona (0s - 22s): Oportunidad de subasta, comparativa de mercado y auditoría legal.
2. Pitch de Plataforma RadarAlertas (22s - Final): Demostración de cómo la tecnología escanea BOE, Catastro, DGT y Subvenciones.
3. Llamada a la acción al Canal Gratuito de Telegram y Guía PDF.
Resolución: 1080x1920 (9:16) en HD Crystal Clear (FFmpeg 6 Mbps).
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
FRAMES_DIR = OUTPUT_DIR / "frames_promo"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FRAMES_DIR.mkdir(parents=True, exist_ok=True)

BCN_BG = TEMPLATES_DIR / "barcelona_aerea.jpg"
AUDIO_BEAT = OUTPUT_DIR / "pro_tension_beat.wav"

GUION_COMPLETO = (
    "Fijaos en lo que acaba de publicar el BOE en Barcelona. "
    "Un piso de ochenta y cinco metros en pleno Eixample, con tres habitaciones y ascensor, por solo cincuenta y cuatro mil euros. "
    "En Idealista, los pisos idénticos en esta misma calle no bajan de trescientos cuarenta mil euros. "
    "Son más de doscientos ochenta y seis mil euros de margen limpio, y el expediente está completamente libre de cargas por el artículo seiscientos setenta y cuatro de la Ley de Enjuiciamiento Civil. "
    "Pero esto no lo encontramos por suerte. RadarAlertas monitoriza el BOE cada madrugada, cruza los datos con Catastro y te avisa a tu Telegram de las mejores subastas de pisos, coches embargados y ayudas del Estado antes de que salgan al mercado. "
    "Entra al enlace de mi biografía, únete gratis al canal y descárgate la Guía Oficial en PDF para empezar hoy mismo."
)

with open(BCN_BG, "rb") as f:
    bg_b64 = base64.b64encode(f.read()).decode("utf-8")
bg_uri = f"data:image/jpeg;base64,{bg_b64}"


def build_property_html(
    price_boe: str = "54.000 €",
    discount: str = "-84%",
    strike_width: str = "calc(100% + 16px)",
    clean_margin: str = "+286.000 €",
    margin_quote: str = "“HABLAMOS DE 286.000 € DE MARGEN LIMPIO”",
    glow_boe: bool = False,
    glow_market: bool = False,
    glow_legal: bool = False,
) -> str:
    boe_style = "box-shadow: 0 20px 60px rgba(0, 0, 0, 0.75), 0 0 50px rgba(16, 185, 129, 0.65); transform: scale(1.02); border-color: #00ff88;" if glow_boe else "box-shadow: 0 16px 40px rgba(0, 0, 0, 0.65);"
    market_style = "box-shadow: 0 20px 50px rgba(0, 0, 0, 0.75), 0 0 45px rgba(239, 68, 68, 0.65); transform: scale(1.02); border-color: #ef4444;" if glow_market else "box-shadow: 0 14px 35px rgba(0, 0, 0, 0.6);"
    legal_style = "box-shadow: 0 20px 50px rgba(0, 0, 0, 0.75), 0 0 45px rgba(56, 189, 248, 0.65); transform: scale(1.02); border-color: #38bdf8;" if glow_legal else "box-shadow: 0 12px 30px rgba(0, 0, 0, 0.55);"

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
            opacity: 0.72; filter: saturate(1.22) contrast(1.15) brightness(0.85); z-index: 0;
        }}
        .bg-overlay {{
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: radial-gradient(circle at 50% 25%, rgba(37, 99, 235, 0.16) 0%, transparent 65%),
                        linear-gradient(180deg, rgba(6, 9, 19, 0.42) 0%, rgba(6, 9, 19, 0.82) 100%);
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
        .hero-headline {{ font-family: 'Space Grotesk', sans-serif; font-size: 52px; font-weight: 900; line-height: 1.1; letter-spacing: -1.5px; color: #ffffff; }}
        .specs-row {{ display: flex; gap: 8px; flex-wrap: wrap; margin-top: 4px; }}
        .spec-pill {{ background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255, 255, 255, 0.2); padding: 6px 14px; border-radius: 8px; font-size: 18px; font-weight: 700; color: #e2e8f0; }}

        .card-market {{ background: rgba(20, 15, 25, 0.82); border: 1.5px solid rgba(239, 68, 68, 0.5); backdrop-filter: blur(20px); border-radius: 24px; padding: 24px 32px; display: flex; flex-direction: column; gap: 8px; {market_style} }}
        .badge-market {{ display: inline-flex; align-items: center; background: rgba(239, 68, 68, 0.2); border: 1px solid rgba(239, 68, 68, 0.5); padding: 5px 14px; border-radius: 999px; font-size: 17px; font-weight: 700; color: #fca5a5; width: fit-content; }}
        .price-market-box {{ position: relative; width: fit-content; }}
        .price-market {{ font-family: 'Space Grotesk', sans-serif; font-size: 68px; font-weight: 800; color: #ef4444; letter-spacing: -2px; }}
        .strikethrough-line {{ position: absolute; left: -8px; top: 50%; height: 6px; background: #ef4444; transform: rotate(-6deg); border-radius: 3px; box-shadow: 0 0 14px rgba(239, 68, 68, 0.95); width: {strike_width}; }}
        .market-sub {{ font-size: 18px; color: #cbd5e1; font-weight: 500; }}

        .card-boe {{ background: linear-gradient(135deg, rgba(6, 78, 59, 0.88) 0%, rgba(15, 23, 42, 0.92) 100%); border: 2px solid rgba(16, 185, 129, 0.9); backdrop-filter: blur(24px); border-radius: 28px; padding: 28px 36px; display: flex; flex-direction: column; gap: 12px; {boe_style} }}
        .badge-boe {{ display: inline-flex; align-items: center; background: #10b981; box-shadow: 0 0 16px rgba(16, 185, 129, 0.5); padding: 7px 20px; border-radius: 999px; font-size: 19px; font-weight: 800; color: #064e3b; width: fit-content; }}
        .price-boe {{ font-family: 'Space Grotesk', sans-serif; font-size: 104px; font-weight: 900; color: #00ff88; line-height: 1; letter-spacing: -3px; text-shadow: 0 0 35px rgba(0, 255, 136, 0.65); }}
        .boe-row {{ display: flex; align-items: center; justify-content: space-between; }}
        .discount-pill {{ background: rgba(16, 185, 129, 0.25); border: 1.5px solid #10b981; padding: 7px 18px; border-radius: 10px; font-size: 22px; font-weight: 800; color: #ffffff; }}
        .boe-margin {{ font-size: 22px; font-weight: 700; color: #a7f3d0; }}

        .card-legal {{ background: rgba(2, 132, 199, 0.22); border: 1.5px solid rgba(56, 189, 248, 0.5); backdrop-filter: blur(20px); border-radius: 22px; padding: 18px 26px; display: flex; flex-direction: column; gap: 10px; {legal_style} }}
        .legal-top {{ display: flex; align-items: center; gap: 16px; }}
        .legal-icon {{ width: 48px; height: 48px; background: rgba(56, 189, 248, 0.2); border: 1px solid rgba(56, 189, 248, 0.4); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #38bdf8; flex-shrink: 0; }}
        .legal-title {{ font-size: 22px; font-weight: 800; color: #ffffff; }}
        .legal-sub {{ font-size: 16px; color: #bae6fd; font-weight: 600; }}
        .legal-audit-pills {{ display: flex; justify-content: space-between; border-top: 1px solid rgba(255, 255, 255, 0.12); padding-top: 8px; font-size: 16px; }}
        .audit-item {{ color: #cbd5e1; font-weight: 600; }}
        .audit-val {{ color: #4ade80; font-weight: 700; }}

        .margin-hook {{ background: rgba(0, 0, 0, 0.9); border: 2px solid rgba(245, 158, 11, 0.9); box-shadow: 0 0 35px rgba(245, 158, 11, 0.35); border-radius: 20px; padding: 18px 24px; text-align: center; }}
        .margin-quote {{ font-family: 'Space Grotesk', sans-serif; font-size: 34px; font-weight: 800; color: #fbbf24; letter-spacing: -0.5px; text-transform: uppercase; }}

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
            <div class="hud-live"><div class="pulse-dot"></div> RADAR JUDICIAL BOE</div>
            <div class="hud-gps">📍 41.3879° N, 2.1699° E</div>
        </div>
        <div class="hero-block">
            <div class="hero-eyebrow">BARCELONA • DISTRITO EIXAMPLE</div>
            <div class="hero-headline">Piso de 85 m² en Barcelona con -84% de Ahorro</div>
            <div class="specs-row">
                <div class="spec-pill">📐 85 m² Construidos</div>
                <div class="spec-pill">🛏️ 3 Dormitorios</div>
                <div class="spec-pill">🏢 Planta 4ª Exterior</div>
                <div class="spec-pill">🛗 Ascensor</div>
                <div class="spec-pill">⚖️ Juzgado 1ª Instancia nº 14</div>
            </div>
        </div>
        <div class="card-market">
            <div class="badge-market">MERCADO LIBRE (IDEALISTA / FOTOCASA)</div>
            <div class="price-market-box">
                <div class="price-market">340.000 €</div>
                <div class="strikethrough-line"></div>
            </div>
            <div class="market-sub">Precio medio en C/ Consell de Cent con 5% honorarios de agencia</div>
        </div>
        <div class="card-boe">
            <div class="badge-boe">SUBASTA JUDICIAL BOE</div>
            <div class="price-boe">{price_boe}</div>
            <div class="boe-row">
                <div class="discount-pill">AHORRO: {discount}</div>
                <div class="boe-margin">Margen bruto: {clean_margin}</div>
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
                    <div class="legal-title">CARGAS HIPOTECARIAS: 0,00 €</div>
                    <div class="legal-sub">Canceladas mediante Mandamiento Judicial (Art. 674 LEC)</div>
                </div>
            </div>
            <div class="legal-audit-pills">
                <div class="audit-item">Posesión: <span class="audit-val">Inmueble Vacío (Sin Okupas)</span></div>
                <div class="audit-item">Fianza 5%: <span class="audit-val">Retornable por Juzgado</span></div>
            </div>
        </div>
        <div class="margin-hook">
            <div class="margin-quote">{margin_quote}</div>
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


def build_platform_showcase_html(glow_cta: bool = False) -> str:
    """Pantalla final de presentación corporativa de la plataforma RadarAlertas."""
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

        /* HUD Superior */
        .hud-header {{
            display: flex; justify-content: space-between; align-items: center;
            padding: 14px 28px; background: rgba(15, 23, 42, 0.92); border: 1.5px solid rgba(56, 189, 248, 0.4);
            backdrop-filter: blur(20px); border-radius: 999px; box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        }}
        .hud-brand {{ display: flex; align-items: center; gap: 12px; font-size: 21px; font-weight: 900; color: #38bdf8; letter-spacing: 1.5px; text-transform: uppercase; }}
        .pulse-dot {{ width: 14px; height: 14px; background: #38bdf8; border-radius: 50%; box-shadow: 0 0 18px #38bdf8; }}
        .hud-status {{ font-size: 18px; font-weight: 700; color: #a7f3d0; }}

        /* Gran Titular de Plataforma */
        .platform-hero {{
            display: flex; flex-direction: column; gap: 12px; text-align: center;
            margin-top: 10px;
        }}
        .platform-badge {{
            display: inline-flex; align-items: center; justify-content: center;
            align-self: center; background: rgba(56, 189, 248, 0.18); border: 1.5px solid rgba(56, 189, 248, 0.4);
            padding: 8px 24px; border-radius: 999px; font-size: 19px; font-weight: 800; color: #38bdf8;
            letter-spacing: 1.5px; text-transform: uppercase;
        }}
        .platform-title {{
            font-family: 'Space Grotesk', sans-serif; font-size: 58px; font-weight: 900;
            line-height: 1.1; letter-spacing: -2px; color: #ffffff;
            text-shadow: 0 4px 28px rgba(0,0,0,0.9);
        }}
        .platform-desc {{
            font-size: 22px; color: #cbd5e1; font-weight: 500; max-width: 900px;
            margin: 0 auto; line-height: 1.4;
        }}

        /* Rejilla de los 4 Canales del Bot */
        .features-grid {{
            display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 10px 0;
        }}
        .feat-card {{
            background: rgba(15, 23, 42, 0.88); border: 1.5px solid rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(24px); border-radius: 24px; padding: 26px 24px;
            display: flex; flex-direction: column; gap: 10px; box-shadow: 0 14px 35px rgba(0,0,0,0.6);
        }}
        .feat-icon-row {{
            display: flex; align-items: center; justify-content: space-between;
        }}
        .feat-icon {{
            font-size: 38px;
        }}
        .feat-tag {{
            font-size: 14px; font-weight: 800; padding: 4px 10px; border-radius: 6px;
            text-transform: uppercase; letter-spacing: 0.5px;
        }}
        .tag-boe {{ background: rgba(16, 185, 129, 0.2); color: #4ade80; border: 1px solid rgba(16, 185, 129, 0.5); }}
        .tag-dgt {{ background: rgba(56, 189, 248, 0.2); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.5); }}
        .tag-ayudas {{ background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.5); }}
        .tag-licit {{ background: rgba(168, 85, 247, 0.2); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.5); }}

        .feat-title {{
            font-size: 23px; font-weight: 800; color: #ffffff;
        }}
        .feat-text {{
            font-size: 17px; color: #94a3b8; line-height: 1.35; font-weight: 500;
        }}

        /* Tarjeta de Garantía y Confianza */
        .trust-banner {{
            background: linear-gradient(135deg, rgba(6, 78, 59, 0.85) 0%, rgba(15, 23, 42, 0.90) 100%);
            border: 2px solid #10b981; border-radius: 22px; padding: 22px 30px;
            display: flex; align-items: center; justify-content: space-between;
            box-shadow: 0 0 30px rgba(16, 185, 129, 0.3);
        }}
        .trust-left {{
            display: flex; align-items: center; gap: 16px;
        }}
        .trust-icon {{
            font-size: 32px;
        }}
        .trust-title {{
            font-size: 22px; font-weight: 900; color: #ffffff;
        }}
        .trust-sub {{
            font-size: 17px; color: #a7f3d0; font-weight: 600;
        }}
        .trust-badge-pill {{
            background: #10b981; color: #064e3b; font-weight: 900; font-size: 18px;
            padding: 8px 18px; border-radius: 999px;
        }}

        /* Gran Botón CTA */
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
        <!-- HUD Superior -->
        <div class="hud-header">
            <div class="hud-brand"><div class="pulse-dot"></div> RADARALERTAS.ES</div>
            <div class="hud-status">● Monitorizando Boletines Oficiales</div>
        </div>

        <!-- Titular Principal -->
        <div class="platform-hero">
            <div class="platform-badge">TECNOLOGÍA DE MONITORIZACIÓN PÚBLICA</div>
            <div class="platform-title">El Radar que escanea el Estado por ti 24/7</div>
            <div class="platform-desc">Auditamos cada madrugada el BOE, Catastro y los registros oficiales para avisarte directamente a Telegram antes de que salgan al mercado.</div>
        </div>

        <!-- Los 4 Canales del Bot -->
        <div class="features-grid">
            <div class="feat-card">
                <div class="feat-icon-row">
                    <span class="feat-icon">🏠</span>
                    <span class="feat-tag tag-boe">BOE JUDICIAL</span>
                </div>
                <div class="feat-title">Subastas Inmuebles</div>
                <div class="feat-text">Pisos y chalets con hasta un 70% de ahorro frente a portales.</div>
            </div>

            <div class="feat-card">
                <div class="feat-icon-row">
                    <span class="feat-icon">🚗</span>
                    <span class="feat-tag tag-dgt">DGT / HACIENDA</span>
                </div>
                <div class="feat-title">Coches Embargados</div>
                <div class="feat-text">Vehículos con tasación oficial y comprobación de cargas 0€.</div>
            </div>

            <div class="feat-card">
                <div class="feat-icon-row">
                    <span class="feat-icon">💶</span>
                    <span class="feat-tag tag-ayudas">BDNS / FONDOS</span>
                </div>
                <div class="feat-title">Ayudas y Subvenciones</div>
                <div class="feat-text">Fondos a fondo perdido para autónomos, pymes y familias.</div>
            </div>

            <div class="feat-card">
                <div class="feat-icon-row">
                    <span class="feat-icon">📋</span>
                    <span class="feat-tag tag-licit">ESTADO</span>
                </div>
                <div class="feat-title">Licitaciones y Empleo</div>
                <div class="feat-text">Contratos públicos menores y convocatorias oficiales activas.</div>
            </div>
        </div>

        <!-- Banner de Confianza -->
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

        <!-- Gran Botón de Conversión CTA -->
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


# Definición secuencial de fotogramas para el vídeo completo
ESCENAS_VIDEO = [
    # PARTE 1: PISO BARCELONA (0s - 22s)
    # Contador ascendente
    {"type": "prop", "dur": 0.25, "price": "14.000 €", "disc": "-22%", "strike": "0%", "margin": "+0 €", "quote": "“BUSCANDO EN EL BOE...”", "glow_boe": True},
    {"type": "prop", "dur": 0.25, "price": "29.000 €", "disc": "-45%", "strike": "0%", "margin": "+0 €", "quote": "“CALCULANDO AHORRO...”", "glow_boe": True},
    {"type": "prop", "dur": 0.25, "price": "43.000 €", "disc": "-67%", "strike": "0%", "margin": "+0 €", "quote": "“COMPARANDO MERCADO...”", "glow_boe": True},
    {"type": "prop", "dur": 0.35, "price": "54.000 €", "disc": "-84%", "strike": "0%", "margin": "+0 €", "quote": "“¡OPORTUNIDAD DETECTADA!”", "glow_boe": True},
    {"type": "prop", "dur": 2.50, "price": "54.000 €", "disc": "-84%", "strike": "0%", "margin": "+0 €", "quote": "“PISO EN EL EIXAMPLE POR 54.000 €”", "glow_boe": True},
    # Tachado de Idealista
    {"type": "prop", "dur": 0.25, "price": "54.000 €", "disc": "-84%", "strike": "35%", "margin": "+0 €", "quote": "“MERCADO LIBRE: 340.000 €”", "glow_market": True},
    {"type": "prop", "dur": 0.25, "price": "54.000 €", "disc": "-84%", "strike": "75%", "margin": "+0 €", "quote": "“MERCADO LIBRE: 340.000 €”", "glow_market": True},
    {"type": "prop", "dur": 3.00, "price": "54.000 €", "disc": "-84%", "strike": "calc(100% + 16px)", "margin": "+0 €", "quote": "“MISMA CALLE: 340.000 € EN PORTALES”", "glow_market": True},
    # Margen Limpio dinámico
    {"type": "prop", "dur": 0.30, "price": "54.000 €", "disc": "-84%", "strike": "calc(100% + 16px)", "margin": "+95.000 €", "quote": "“CALCULANDO MARGEN LIMPIO...”"},
    {"type": "prop", "dur": 0.30, "price": "54.000 €", "disc": "-84%", "strike": "calc(100% + 16px)", "margin": "+195.000 €", "quote": "“CALCULANDO MARGEN LIMPIO...”"},
    {"type": "prop", "dur": 0.30, "price": "54.000 €", "disc": "-84%", "strike": "calc(100% + 16px)", "margin": "+286.000 €", "quote": "“HABLAMOS DE 286.000 € DE MARGEN LIMPIO”"},
    {"type": "prop", "dur": 3.50, "price": "54.000 €", "disc": "-84%", "strike": "calc(100% + 16px)", "margin": "+286.000 €", "quote": "“HABLAMOS DE 286.000 € DE MARGEN LIMPIO”"},
    # Seguridad jurídica Art. 674 LEC
    {"type": "prop", "dur": 6.50, "price": "54.000 €", "disc": "-84%", "strike": "calc(100% + 16px)", "margin": "+286.000 €", "quote": "“HABLAMOS DE 286.000 € DE MARGEN LIMPIO”", "glow_legal": True},

    # PARTE 2: PRESENTACIÓN DE LA PLATAFORMA RADARALERTAS (22s - Final)
    {"type": "platform", "dur": 7.00, "glow_cta": False},
    {"type": "platform", "dur": 6.50, "glow_cta": True},
]


async def render_all_frames():
    print("🎨 Renderizando fotogramas PNG de alta fidelidad (1080x1920)...")
    frame_files = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1920})
        
        for i, step in enumerate(ESCENAS_VIDEO, 1):
            if step["type"] == "prop":
                html = build_property_html(
                    price_boe=step.get("price", "54.000 €"),
                    discount=step.get("disc", "-84%"),
                    strike_width=step.get("strike", "calc(100% + 16px)"),
                    clean_margin=step.get("margin", "+286.000 €"),
                    margin_quote=step.get("quote", "“HABLAMOS DE 286.000 € DE MARGEN LIMPIO”"),
                    glow_boe=step.get("glow_boe", False),
                    glow_market=step.get("glow_market", False),
                    glow_legal=step.get("glow_legal", False),
                )
            else:
                html = build_platform_showcase_html(glow_cta=step.get("glow_cta", False))
                
            await page.set_content(html, wait_until="networkidle")
            out_png = FRAMES_DIR / f"frame_p_{i:02d}.png"
            await page.screenshot(path=str(out_png))
            frame_files.append((out_png, step["dur"]))
            print(f"  ✓ Frame {i:02d} [{step['type'].upper()}] generado ({step['dur']}s)")
            
        await browser.close()
    return frame_files


async def main():
    print("🎙️ 1. Generando locución completa (Caso Barcelona + Pitch RadarAlertas)...")
    ruta_audio = OUTPUT_DIR / "bcn_promo_audio.mp3"
    tts = edge_tts.Communicate(text=GUION_COMPLETO, voice="es-ES-AlvaroNeural", rate="+6%")
    await tts.save(str(ruta_audio))

    cmd_dur = ["ffmpeg", "-i", str(ruta_audio), "-f", "null", "-"]
    res = subprocess.run(cmd_dur, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    duracion_real = 36.0
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            partes = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = partes.split(":")
            duracion_real = float(h) * 3600 + float(m) * 60 + float(s)
            break
    print(f"  ✓ Duración audio real: {duracion_real:.2f} s")

    # Factor de sincronización
    duracion_base = sum(s["dur"] for s in ESCENAS_VIDEO)
    factor = duracion_real / duracion_base

    # Renderizar fotogramas
    frames = await render_all_frames()

    print("🎬 2. Ensamblando vídeo dinámico en alta fidelidad (6 Mbps)...")
    clips = []
    for i, (f_path, dur) in enumerate(frames, 1):
        dur_adj = dur * factor
        clip_path = FRAMES_DIR / f"cp_{i:02d}.mp4"
        cmd = [
            "ffmpeg", "-y", "-loop", "1", "-t", f"{dur_adj:.3f}",
            "-i", str(f_path),
            "-c:v", "libx264", "-b:v", "6000k", "-preset", "veryfast", "-pix_fmt", "yuv420p",
            "-an", str(clip_path)
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        clips.append(clip_path)

    concat_file = FRAMES_DIR / "concat_p.txt"
    with open(concat_file, "w") as f:
        for c in clips:
            f.write(f"file '{c.name}'\n")

    raw_video = OUTPUT_DIR / "promo_raw.mp4"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file), "-c", "copy", str(raw_video)], check=True)

    ruta_final = OUTPUT_DIR / "VIDEO_BARCELONA_Y_RADARALERTAS_PROMO.mp4"
    print("🎵 3. Mezclando locución y banda sonora...")
    if AUDIO_BEAT.exists():
        cmd_final = [
            "ffmpeg", "-y",
            "-i", str(raw_video),
            "-i", str(ruta_audio),
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
        cmd_final = ["ffmpeg", "-y", "-i", str(raw_video), "-i", str(ruta_audio), "-c:v", "copy", "-c:a", "aac", "-t", f"{duracion_real:.2f}", str(ruta_final)]

    subprocess.run(cmd_final, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    print(f"🎉 VÍDEO COMPLETO CON PUBLICIDAD GENERADO: {ruta_final}")


if __name__ == "__main__":
    asyncio.run(main())
