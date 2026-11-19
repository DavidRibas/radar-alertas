import asyncio
import base64
from pathlib import Path
from playwright.async_api import async_playwright

BASE_DIR = Path("C:/Ideas/radar-alertas")
OUTPUT_DIR = BASE_DIR / "output"
ASSETS_DIR = BASE_DIR / "assets"
TEMPLATES_DIR = ASSETS_DIR / "templates"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Cargar foto satélite como Base64 para que siempre cargue al 100%
with open(TEMPLATES_DIR / "barrio_pilar_aerea.jpg", "rb") as f:
    sat_b64 = base64.b64encode(f.read()).decode("utf-8")
sat_data_uri = f"data:image/jpeg;base64,{sat_b64}"

HTML_CONTENT = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=Syne:wght@700;800&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Plus Jakarta Sans', sans-serif;
            -webkit-font-smoothing: antialiased;
        }}
        body {{
            width: 1080px;
            height: 1920px;
            background: #060913;
            color: #ffffff;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 70px 50px 90px;
        }}
        /* Fondo con imagen satélite bien visible y viñeta cinematográfica suave */
        .bg-sat {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: url('{sat_data_uri}');
            background-size: cover;
            background-position: center;
            opacity: 0.72;
            filter: saturate(1.1) contrast(1.15) brightness(0.85);
            z-index: 0;
        }}
        .bg-gradient {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at 50% 25%, rgba(37, 99, 235, 0.12) 0%, transparent 65%),
                        linear-gradient(180deg, rgba(6, 9, 19, 0.45) 0%, rgba(6, 9, 19, 0.75) 100%);
            z-index: 1;
        }}

        .content {{
            position: relative;
            z-index: 2;
            display: flex;
            flex-direction: column;
            gap: 26px;
            height: 100%;
        }}

        /* HUD Superior */
        .hud-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 14px 26px;
            background: rgba(15, 23, 42, 0.85);
            border: 1.5px solid rgba(255, 255, 255, 0.18);
            backdrop-filter: blur(24px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
            border-radius: 999px;
        }}
        .hud-live {{
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 20px;
            font-weight: 800;
            color: #ef4444;
            letter-spacing: 1.5px;
            text-transform: uppercase;
        }}
        .pulse-dot {{
            width: 14px;
            height: 14px;
            background: #ef4444;
            border-radius: 50%;
            box-shadow: 0 0 16px #ef4444;
        }}
        .hud-gps {{
            font-size: 19px;
            font-weight: 700;
            color: #cbd5e1;
            letter-spacing: 0.5px;
        }}

        /* Título Principal */
        .hero-title {{
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-top: 6px;
            text-shadow: 0 4px 20px rgba(0, 0, 0, 0.8);
        }}
        .hero-tag {{
            font-size: 22px;
            font-weight: 800;
            color: #38bdf8;
            letter-spacing: 2px;
            text-transform: uppercase;
        }}
        .hero-main {{
            font-family: 'Syne', sans-serif;
            font-size: 56px;
            font-weight: 800;
            line-height: 1.1;
            letter-spacing: -1.5px;
            color: #ffffff;
            text-shadow: 0 4px 24px rgba(0, 0, 0, 0.9);
        }}

        /* Tarjeta 1: Idealista (Mercado Libre) */
        .card-market {{
            background: rgba(20, 15, 25, 0.82);
            border: 2px solid rgba(239, 68, 68, 0.65);
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.65);
            backdrop-filter: blur(28px);
            border-radius: 28px;
            padding: 32px 38px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            position: relative;
            overflow: hidden;
        }}
        .badge-market {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(239, 68, 68, 0.2);
            border: 1px solid rgba(239, 68, 68, 0.5);
            padding: 6px 16px;
            border-radius: 999px;
            font-size: 18px;
            font-weight: 700;
            color: #fca5a5;
            width: fit-content;
        }}
        .price-row-market {{
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .price-market {{
            font-family: 'Syne', sans-serif;
            font-size: 74px;
            font-weight: 800;
            color: #ef4444;
            position: relative;
            letter-spacing: -2px;
        }}
        .price-market::after {{
            content: '';
            position: absolute;
            left: -10px;
            top: 50%;
            width: calc(100% + 20px);
            height: 7px;
            background: #ef4444;
            transform: rotate(-6deg);
            border-radius: 4px;
            box-shadow: 0 0 14px rgba(239, 68, 68, 0.8);
        }}
        .market-meta {{
            font-size: 20px;
            color: #cbd5e1;
            font-weight: 500;
        }}

        /* Tarjeta 2: BOE (El Bombazo) */
        .card-boe {{
            background: linear-gradient(135deg, rgba(6, 78, 59, 0.88) 0%, rgba(15, 23, 42, 0.92) 100%);
            border: 2.5px solid #22c55e;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.75), 0 0 45px rgba(34, 197, 94, 0.35);
            backdrop-filter: blur(32px);
            border-radius: 32px;
            padding: 38px 42px;
            display: flex;
            flex-direction: column;
            gap: 16px;
            position: relative;
        }}
        .badge-boe {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: #22c55e;
            box-shadow: 0 0 18px rgba(34, 197, 94, 0.5);
            padding: 8px 22px;
            border-radius: 999px;
            font-size: 20px;
            font-weight: 800;
            color: #064e3b;
            width: fit-content;
            letter-spacing: 0.5px;
        }}
        .price-boe {{
            font-family: 'Syne', sans-serif;
            font-size: 114px;
            font-weight: 800;
            color: #4ade80;
            line-height: 1;
            letter-spacing: -4px;
            text-shadow: 0 0 40px rgba(74, 222, 128, 0.5);
        }}
        .discount-pill {{
            display: inline-flex;
            align-items: center;
            background: rgba(34, 197, 94, 0.25);
            border: 1.5px solid rgba(34, 197, 94, 0.6);
            padding: 8px 22px;
            border-radius: 14px;
            font-size: 24px;
            font-weight: 800;
            color: #ffffff;
            width: fit-content;
        }}
        .boe-margin {{
            font-size: 24px;
            font-weight: 700;
            color: #a7f3d0;
        }}

        /* Tarjeta 3: Seguridad Jurídica */
        .card-legal {{
            background: rgba(15, 23, 42, 0.85);
            border: 1.5px solid rgba(56, 189, 248, 0.4);
            box-shadow: 0 14px 35px rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(24px);
            border-radius: 24px;
            padding: 22px 30px;
            display: flex;
            align-items: center;
            gap: 20px;
        }}
        .legal-icon {{
            width: 58px;
            height: 58px;
            background: rgba(56, 189, 248, 0.18);
            border: 1px solid rgba(56, 189, 248, 0.35);
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #38bdf8;
            flex-shrink: 0;
        }}
        .legal-texts {{
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}
        .legal-title {{
            font-size: 22px;
            font-weight: 800;
            color: #ffffff;
        }}
        .legal-sub {{
            font-size: 17px;
            color: #94a3b8;
            font-weight: 500;
        }}

        /* Subtítulo dinámico estilo TikTok */
        .subtitle-box {{
            background: rgba(0, 0, 0, 0.9);
            border: 2px solid #facc15;
            box-shadow: 0 0 35px rgba(250, 204, 21, 0.35);
            border-radius: 24px;
            padding: 22px 28px;
            text-align: center;
        }}
        .subtitle-text {{
            font-family: 'Syne', sans-serif;
            font-size: 38px;
            font-weight: 800;
            color: #facc15;
            letter-spacing: -0.5px;
            text-transform: uppercase;
        }}

        /* Botón Inferior CTA */
        .cta-btn {{
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            border: 1.5px solid rgba(147, 197, 253, 0.5);
            box-shadow: 0 16px 45px rgba(37, 99, 235, 0.5);
            border-radius: 28px;
            padding: 28px 38px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .cta-left {{
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}
        .cta-main {{
            font-size: 28px;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: -0.5px;
        }}
        .cta-sub {{
            font-size: 18px;
            color: rgba(255, 255, 255, 0.85);
            font-weight: 600;
        }}
        .cta-arrow {{
            width: 56px;
            height: 56px;
            background: rgba(255, 255, 255, 0.22);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 26px;
        }}
    </style>
</head>
<body>
    <div class="bg-sat"></div>
    <div class="bg-gradient"></div>

    <div class="content">
        <!-- HUD Superior -->
        <div class="hud-header">
            <div class="hud-live">
                <div class="pulse-dot"></div>
                RADAR JUDICIAL BOE
            </div>
            <div class="hud-gps">📍 40.4812° N, 3.7078° W</div>
        </div>

        <!-- Título -->
        <div class="hero-title">
            <div class="hero-tag">CONVOCATORIA ACTIVA HOY</div>
            <div class="hero-main">Piso de 80 m² en Madrid con -84% de Ahorro</div>
        </div>

        <!-- Tarjeta 1: Idealista -->
        <div class="card-market">
            <div class="badge-market">MERCADO LIBRE (IDEALISTA)</div>
            <div class="price-row-market">
                <div class="price-market">270.000 €</div>
            </div>
            <div class="market-meta">Precio medio en el mismo barrio con comisiones de agencia</div>
        </div>

        <!-- Tarjeta 2: Subasta BOE -->
        <div class="card-boe">
            <div class="badge-boe">SUBASTA JUDICIAL BOE</div>
            <div class="price-boe">42.000 €</div>
            <div class="discount-pill">AHORRO: -84% SOBRE TASACIÓN</div>
            <div class="boe-margin">Margen bruto estimado: +228.000 €</div>
        </div>

        <!-- Tarjeta 3: Seguridad Jurídica -->
        <div class="card-legal">
            <div class="legal-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                </svg>
            </div>
            <div class="legal-texts">
                <div class="legal-title">CARGAS HIPOTECARIAS: 0,00 €</div>
                <div class="legal-sub">Canceladas mediante Mandamiento Judicial (Art. 674 LEC)</div>
            </div>
        </div>

        <!-- Subtítulo estilo TikTok -->
        <div class="subtitle-box">
            <div class="subtitle-text">"Hablamos de 228.000 € de margen limpio"</div>
        </div>

        <!-- Botón CTA Inferior -->
        <div class="cta-btn">
            <div class="cta-left">
                <div class="cta-main">Guía Práctica Oficial en PDF (0 €)</div>
                <div class="cta-sub">Descárgala gratis en el enlace del perfil</div>
            </div>
            <div class="cta-arrow">➔</div>
        </div>
    </div>
</body>
</html>
"""

async def generar_imagen():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1920})
        await page.set_content(HTML_CONTENT, wait_until="networkidle")
        out_path = OUTPUT_DIR / "DISENO_MODERNO_2026.png"
        await page.screenshot(path=str(out_path))
        await browser.close()
        print(f"🎉 Imagen generada con fondo satélite visible: {out_path}")

asyncio.run(generar_imagen())

