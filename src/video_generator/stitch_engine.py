"""
Motor de Renderizado Stitch (BMad Visual Directive)
Implementa la especificación de diseño 9:16 (1080x1920) para Radar Judicial BOE
usando Playwright Chromium headless.
"""
import asyncio
import base64
from pathlib import Path
from playwright.async_api import async_playwright

BASE_DIR = Path("C:/Ideas/radar-alertas")
OUTPUT_DIR = BASE_DIR / "output"
ASSETS_DIR = BASE_DIR / "assets"
TEMPLATES_DIR = ASSETS_DIR / "templates"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def build_stitch_html(
    headline_text: str = "Piso de 80 m² en Madrid con -84% de Ahorro",
    market_price: str = "270.000 €",
    auction_price: str = "42.000 €",
    discount_percentage: str = "84",
    clean_margin: str = "228.000 €",
    gps_coordinates: str = "40.4812° N, 3.7078° W",
    bg_image_path: Path = TEMPLATES_DIR / "barrio_pilar_aerea.jpg"
) -> str:
    """Genera el código HTML5 con CSS Glassmorphism puro y tokens oficiales de Stitch."""
    
    # Cargar fondo aéreo/dron como Base64
    if Path(bg_image_path).exists():
        with open(bg_image_path, "rb") as f:
            b64_data = base64.b64encode(f.read()).decode("utf-8")
        bg_uri = f"data:image/jpeg;base64,{b64_data}"
    else:
        bg_uri = ""

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&family=Space+Grotesk:wght@700;800&family=Syne:wght@700;800&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', -apple-system, sans-serif;
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
            padding: 80px 52px 100px;
        }}
        /* Capa 0: Fondo Drone / Aéreo con contraste ajustado */
        .bg-drone {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: url('{bg_uri}');
            background-size: cover;
            background-position: center;
            opacity: 0.72;
            filter: saturate(1.15) contrast(1.18) brightness(0.85);
            z-index: 0;
        }}
        .bg-overlay {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at 50% 25%, rgba(37, 99, 235, 0.14) 0%, transparent 65%),
                        linear-gradient(180deg, rgba(6, 9, 19, 0.45) 0%, rgba(6, 9, 19, 0.8) 100%);
            z-index: 1;
        }}

        .content {{
            position: relative;
            z-index: 2;
            display: flex;
            flex-direction: column;
            gap: 24px;
            height: 100%;
        }}

        /* HUD Superior */
        .hud-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 14px 28px;
            background: rgba(15, 23, 42, 0.85);
            border: 1.5px solid rgba(255, 255, 255, 0.18);
            backdrop-filter: blur(20px);
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
            color: #38bdf8;
            letter-spacing: 0.5px;
        }}

        /* Titular */
        .hero-title {{
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-top: 4px;
            text-shadow: 0 4px 20px rgba(0, 0, 0, 0.85);
        }}
        .hero-eyebrow {{
            font-size: 22px;
            font-weight: 800;
            color: #38bdf8;
            letter-spacing: 2px;
            text-transform: uppercase;
        }}
        .hero-headline {{
            font-family: 'Syne', 'Space Grotesk', sans-serif;
            font-size: 54px;
            font-weight: 800;
            line-height: 1.12;
            letter-spacing: -1.5px;
            color: #ffffff;
            text-shadow: 0 4px 24px rgba(0, 0, 0, 0.9);
        }}

        /* Tarjeta 1: Mercado Libre (Idealista) */
        .card-market {{
            background: rgba(20, 15, 25, 0.78);
            border: 1.5px solid rgba(239, 68, 68, 0.45);
            box-shadow: 0 16px 36px rgba(0, 0, 0, 0.65);
            backdrop-filter: blur(20px);
            border-radius: 26px;
            padding: 28px 36px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        .badge-market {{
            display: inline-flex;
            align-items: center;
            background: rgba(239, 68, 68, 0.2);
            border: 1px solid rgba(239, 68, 68, 0.5);
            padding: 6px 16px;
            border-radius: 999px;
            font-size: 18px;
            font-weight: 700;
            color: #fca5a5;
            width: fit-content;
        }}
        .price-market {{
            font-family: 'Space Grotesk', 'Syne', sans-serif;
            font-size: 70px;
            font-weight: 800;
            color: #ef4444;
            position: relative;
            letter-spacing: -2px;
            width: fit-content;
        }}
        .price-market::after {{
            content: '';
            position: absolute;
            left: -8px;
            top: 50%;
            width: calc(100% + 16px);
            height: 6px;
            background: #ef4444;
            transform: rotate(-6deg);
            border-radius: 3px;
            box-shadow: 0 0 12px rgba(239, 68, 68, 0.85);
        }}
        .market-sub {{
            font-size: 19px;
            color: #cbd5e1;
            font-weight: 500;
        }}

        /* Tarjeta 2: Subasta Judicial BOE (Protagonista) */
        .card-boe {{
            background: linear-gradient(135deg, rgba(6, 78, 59, 0.85) 0%, rgba(15, 23, 42, 0.90) 100%);
            border: 2px solid rgba(16, 185, 129, 0.85);
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.75), 0 0 40px rgba(16, 185, 129, 0.3);
            backdrop-filter: blur(24px);
            border-radius: 30px;
            padding: 34px 40px;
            display: flex;
            flex-direction: column;
            gap: 14px;
        }}
        .badge-boe {{
            display: inline-flex;
            align-items: center;
            background: #10b981;
            box-shadow: 0 0 16px rgba(16, 185, 129, 0.5);
            padding: 8px 22px;
            border-radius: 999px;
            font-size: 19px;
            font-weight: 800;
            color: #064e3b;
            width: fit-content;
        }}
        .price-boe {{
            font-family: 'Space Grotesk', 'Syne', sans-serif;
            font-size: 108px;
            font-weight: 900;
            color: #00ff88;
            line-height: 1;
            letter-spacing: -3px;
            text-shadow: 0 0 35px rgba(0, 255, 136, 0.55);
        }}
        .discount-pill {{
            display: inline-flex;
            align-items: center;
            background: rgba(16, 185, 129, 0.25);
            border: 1.5px solid #10b981;
            padding: 8px 20px;
            border-radius: 12px;
            font-size: 23px;
            font-weight: 800;
            color: #ffffff;
            width: fit-content;
        }}
        .boe-margin {{
            font-size: 23px;
            font-weight: 700;
            color: #a7f3d0;
        }}

        /* Tarjeta 3: Seguridad Jurídica */
        .card-legal {{
            background: rgba(2, 132, 199, 0.2);
            border: 1.5px solid rgba(56, 189, 248, 0.45);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.55);
            backdrop-filter: blur(20px);
            border-radius: 22px;
            padding: 20px 28px;
            display: flex;
            align-items: center;
            gap: 18px;
        }}
        .legal-icon {{
            width: 54px;
            height: 54px;
            background: rgba(56, 189, 248, 0.18);
            border: 1px solid rgba(56, 189, 248, 0.4);
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #38bdf8;
            flex-shrink: 0;
        }}
        .legal-texts {{
            display: flex;
            flex-direction: column;
            gap: 3px;
        }}
        .legal-title {{
            font-size: 21px;
            font-weight: 800;
            color: #ffffff;
        }}
        .legal-sub {{
            font-size: 16px;
            color: #94a3b8;
            font-weight: 500;
        }}

        /* Tarjeta 4: Gancho de Margen */
        .margin-hook {{
            background: rgba(0, 0, 0, 0.88);
            border: 2px solid rgba(245, 158, 11, 0.9);
            box-shadow: 0 0 35px rgba(245, 158, 11, 0.35);
            border-radius: 22px;
            padding: 20px 26px;
            text-align: center;
        }}
        .margin-quote {{
            font-family: 'Space Grotesk', 'Syne', sans-serif;
            font-size: 36px;
            font-weight: 800;
            color: #fbbf24;
            letter-spacing: -0.5px;
            text-transform: uppercase;
        }}

        /* Botón Inferior CTA */
        .cta-btn {{
            background: #2563eb;
            border: 1.5px solid rgba(147, 197, 253, 0.5);
            box-shadow: 0 16px 45px rgba(37, 99, 235, 0.55);
            border-radius: 26px;
            padding: 26px 36px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .cta-left {{
            display: flex;
            flex-direction: column;
            gap: 5px;
        }}
        .cta-main {{
            font-size: 26px;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: -0.5px;
        }}
        .cta-sub {{
            font-size: 17px;
            color: rgba(255, 255, 255, 0.88);
            font-weight: 600;
        }}
        .cta-arrow {{
            width: 52px;
            height: 52px;
            background: rgba(255, 255, 255, 0.22);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }}
    </style>
</head>
<body>
    <div class="bg-drone"></div>
    <div class="bg-overlay"></div>

    <div class="content">
        <!-- Status Live & GPS -->
        <div class="hud-header">
            <div class="hud-live">
                <div class="pulse-dot"></div>
                RADAR JUDICIAL BOE
            </div>
            <div class="hud-gps">📍 {gps_coordinates}</div>
        </div>

        <!-- Headline -->
        <div class="hero-title">
            <div class="hero-eyebrow">CONVOCATORIA ACTIVA HOY</div>
            <div class="hero-headline">{headline_text}</div>
        </div>

        <!-- Card 1: Mercado Libre -->
        <div class="card-market">
            <div class="badge-market">MERCADO LIBRE (IDEALISTA)</div>
            <div class="price-market">{market_price}</div>
            <div class="market-sub">Precio medio en el mismo barrio con comisiones de agencia</div>
        </div>

        <!-- Card 2: Subasta BOE Hero -->
        <div class="card-boe">
            <div class="badge-boe">SUBASTA JUDICIAL BOE</div>
            <div class="price-boe">{auction_price}</div>
            <div class="discount-pill">AHORRO: -{discount_percentage}% SOBRE TASACIÓN</div>
            <div class="boe-margin">Margen bruto estimado: +{clean_margin}</div>
        </div>

        <!-- Card 3: Seguridad Jurídica Art. 674 LEC -->
        <div class="card-legal">
            <div class="legal-icon">
                <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                </svg>
            </div>
            <div class="legal-texts">
                <div class="legal-title">CARGAS HIPOTECARIAS: 0,00 €</div>
                <div class="legal-sub">Canceladas mediante Mandamiento Judicial (Art. 674 LEC)</div>
            </div>
        </div>

        <!-- Card 4: Gancho de Margen -->
        <div class="margin-hook">
            <div class="margin-quote">“HABLAMOS DE {clean_margin} DE MARGEN LIMPIO”</div>
        </div>

        <!-- Bottom CTA Button -->
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


async def render_stitch_asset(
    output_filename: str = "STITCH_FRAME_TEST.png",
    **kwargs
) -> Path:
    """Renderiza el activo gráfico 1080x1920 con Playwright."""
    html = build_stitch_html(**kwargs)
    out_path = OUTPUT_DIR / output_filename
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1920})
        await page.set_content(html, wait_until="networkidle")
        await page.screenshot(path=str(out_path))
        await browser.close()

    print(f"✅ Render completado: {out_path}")
    return out_path


if __name__ == "__main__":
    asyncio.run(render_stitch_asset("STITCH_FRAME_TEST.png"))
