"""
Generador del Vídeo Tutorial Oficial: ¿Cómo Funciona RadarAlertas? (48s HD Vertical 1080x1920)
Guía visual paso a paso para nuevos usuarios, redes sociales (TikTok/Reels/Shorts), Web y Telegram.
"""
import asyncio
import base64
import os
import sys
import shutil
import subprocess
from pathlib import Path
import edge_tts
from playwright.async_api import async_playwright

BASE_DIR = Path("C:/Ideas/radar-alertas")
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

OUTPUT_DIR = BASE_DIR / "output"
TEMPLATES_DIR = BASE_DIR / "assets" / "templates"
AUDIO_BEAT = OUTPUT_DIR / "pro_tension_beat.wav"
VOICE = "es-ES-AlvaroNeural"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def img_to_b64(path: Path) -> str:
    with open(path, "rb") as f:
        return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode('utf-8')}"

TUTORIAL_SCRIPT = (
    "¿Sabías que cada madrugada el Estado publica cientos de pisos, chalets y coches embargados con hasta un setenta por ciento de descuento? "
    "El problema es que el portal del BOE es caótico y casi nadie sabe cómo buscar. "
    "Por eso creamos RadarAlertas: el radar inteligente que rastrea cada noche el BOE, la DGT y los registros oficiales para filtrar las mejores oportunidades. "
    "Al entrar en nuestro explorador web interactivo puedes filtrar por tu provincia, ver fotos de satélite, referencia catastral y calcular tu margen real. "
    "Nuestra calculadora audita el expediente y te confirma que todas las hipotecas y deudas anteriores quedan canceladas a cero euros por decreto judicial según el artículo seiscientos setenta y cuatro de la Ley de Enjuiciamiento Civil. "
    "Y además, recibes avisos inmediatos en WhatsApp y Telegram antes de que terminen las pujas. "
    "Entra ahora al enlace de mi perfil, pruébalo gratis y descarga la guía oficial en PDF."
)

def build_scene_html(scene_idx: int, bg_uri: str) -> str:
    # 5 Escenas magistrales:
    # Escena 1: El problema del BOE vs Oportunidades ocultas
    # Escena 2: Qué es RadarAlertas (El radar 24/7)
    # Escena 3: Explorador Web y Filtro por Provincia
    # Escena 4: Calculadora Art. 674 LEC y cancelación de deudas a 0€
    # Escena 5: Canales WhatsApp & Telegram + CTA enlace perfil

    if scene_idx == 1:
        badge = "EL SECRETO DEL BOE Y LA DGT"
        title = "Pisos y Coches con hasta un -70% de Descuento"
        sub = "¿Por qué casi nadie aprovecha las subastas judiciales del Estado?"
        content_block = """
        <div class="problem-card">
            <div class="problem-header">
                <span class="warning-icon">⚠️</span>
                <div>
                    <div class="problem-title">El Problema del Portal Oficial</div>
                    <div class="problem-sub">Expedientes judiciales complejos en PDF que ocultan los verdaderos chollos</div>
                </div>
            </div>
            <div class="stats-row">
                <div class="stat-pill"><span class="stat-num">+450</span><span class="stat-lbl">Subastas / Día</span></div>
                <div class="stat-pill"><span class="stat-num">-70%</span><span class="stat-lbl">Ahorro Medio</span></div>
                <div class="stat-pill"><span class="stat-num">5%</span><span class="stat-lbl">Fianza Legal</span></div>
            </div>
        </div>
        """
    elif scene_idx == 2:
        badge = "TECNOLOGÍA RADARALERTAS"
        title = "Auditamos Cada Noche 5 Fuentes Oficiales"
        sub = "Filtramos miles de registros para dejar solo las operaciones con margen limpio"
        content_block = """
        <div class="grid-4">
            <div class="card-mini"><span class="c-ico">🏠</span><div class="c-tit">Inmuebles BOE</div><div class="c-desc">Pisos y chalets al -50% con Catastro</div></div>
            <div class="card-mini"><span class="c-ico">🚗</span><div class="c-tit">Vehículos DGT</div><div class="c-desc">Coches desde 500 € con precintos 0 €</div></div>
            <div class="card-mini"><span class="c-ico">💰</span><div class="c-tit">Ayudas BDNS</div><div class="c-desc">Subvenciones a fondo perdido pymes</div></div>
            <div class="card-mini"><span class="c-ico">📑</span><div class="c-tit">Licitaciones</div><div class="c-desc">Contratos menores del Estado</div></div>
        </div>
        """
    elif scene_idx == 3:
        badge = "PASO 1: EXPLORADOR WEB INTERACTIVO"
        title = "Filtra por tu Provincia y Encuentra Chollos"
        sub = "Buscador en tiempo real con datos de Catastro, Street View y tasación oficial"
        content_block = """
        <div class="browser-mockup">
            <div class="mockup-bar">
                <div class="dots"><span class="d-red"></span><span class="d-yel"></span><span class="d-gre"></span></div>
                <div class="mockup-url">radar-alertas-delta.vercel.app</div>
            </div>
            <div class="mockup-body">
                <div class="filter-chips">
                    <span class="chip active">📍 Toda España</span>
                    <span class="chip">📍 Madrid</span>
                    <span class="chip">📍 Barcelona</span>
                    <span class="chip">📍 Valencia</span>
                </div>
                <div class="deal-preview">
                    <div class="deal-top">
                        <span class="deal-tag">🚗 EMBARGO DGT</span>
                        <span class="deal-disc">-89% DESCUENTO</span>
                    </div>
                    <div class="deal-name">SUV Mazda CX-5 (Año 2021)</div>
                    <div class="deal-prices">
                        <div class="p-col"><span class="p-lbl">MERCADO</span><span class="p-old">18.424 €</span></div>
                        <div class="p-col"><span class="p-lbl">SUBASTA BOE</span><span class="p-new">1.842 €</span></div>
                    </div>
                </div>
            </div>
        </div>
        """
    elif scene_idx == 4:
        badge = "PASO 2: SEGURIDAD ART. 674 LEC"
        title = "Calculadora Oficial de Cargas e Impuestos"
        sub = "Cero sorpresas: las deudas e hipotecas previas quedan canceladas por Decreto"
        content_block = """
        <div class="legal-card">
            <div class="legal-badge-row">
                <span class="legal-shield">🛡️</span>
                <div class="legal-tit">DICTAMEN ART. 674 LEY ENJUICIAMIENTO CIVIL</div>
            </div>
            <div class="legal-items">
                <div class="l-item"><span class="check-ico">✅</span><span><strong>Cargas Anteriores:</strong> 0,00 € Canceladas por Juez</span></div>
                <div class="l-item"><span class="check-ico">✅</span><span><strong>Fianza del 5%:</strong> Reembolsable al 100% si no ganas</span></div>
                <div class="l-item"><span class="check-ico">✅</span><span><strong>Simulador ITP:</strong> Cálculo de aranceles y margen neto</span></div>
            </div>
            <div class="profit-highlight">
                <span>MARGEN LIMPIO ESTIMADO:</span>
                <span class="profit-val">+16.580 €</span>
            </div>
        </div>
        """
    else:
        badge = "PASO 3: ALERTAS INMEDIATAS EN TU MÓVIL"
        title = "Recibe Avisos Antes de que Cierren las Pujas"
        sub = "Acceso instantáneo en WhatsApp y Telegram + Explorador Web y Guía PDF"
        content_block = """
        <div class="channels-card">
            <div class="chan-row whatsapp">
                <span class="chan-ico">💬</span>
                <div>
                    <div class="chan-tit">Canal Oficial de WhatsApp</div>
                    <div class="chan-sub">Alertas públicas directas a tu chat</div>
                </div>
                <span class="chan-badge">ACTIVO</span>
            </div>
            <div class="chan-row telegram">
                <span class="chan-ico">🤖</span>
                <div>
                    <div class="chan-tit">Bot Interactivo de Telegram</div>
                    <div class="chan-sub">Filtro personal por categorías y expediente</div>
                </div>
                <span class="chan-badge">24/7</span>
            </div>
        </div>
        <div class="final-cta-btn">
            <div class="cta-txt-col">
                <div class="cta-head">Entra a la Web + Guía en PDF Gratis</div>
                <div class="cta-bot">Enlace oficial en mi perfil de redes</div>
            </div>
            <div class="cta-cir">➔</div>
        </div>
        """

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
            justify-content: space-between; padding: 75px 50px 90px;
        }}
        .bg-drone {{
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-image: url('{bg_uri}'); background-size: cover; background-position: center;
            opacity: 0.60; filter: saturate(1.2) contrast(1.1) brightness(0.65); z-index: 0;
        }}
        .bg-overlay {{
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: radial-gradient(circle at 50% 20%, rgba(37, 99, 235, 0.28) 0%, transparent 70%),
                        linear-gradient(180deg, rgba(6, 9, 19, 0.55) 0%, rgba(6, 9, 19, 0.92) 100%);
            z-index: 1;
        }}
        .content {{
            position: relative; z-index: 2; display: flex; flex-direction: column;
            gap: 24px; height: 100%; justify-content: space-between;
        }}
        .hud-header {{
            display: flex; justify-content: space-between; align-items: center;
            padding: 14px 28px; background: rgba(15, 23, 42, 0.92); border: 1.5px solid rgba(56, 189, 248, 0.4);
            backdrop-filter: blur(20px); border-radius: 999px; box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        }}
        .hud-brand {{ display: flex; align-items: center; gap: 12px; font-size: 21px; font-weight: 900; color: #38bdf8; letter-spacing: 1.5px; text-transform: uppercase; }}
        .pulse-dot {{ width: 14px; height: 14px; background: #38bdf8; border-radius: 50%; box-shadow: 0 0 18px #38bdf8; }}
        .hud-status {{ font-size: 18px; font-weight: 700; color: #a7f3d0; }}

        .hero-block {{ display: flex; flex-direction: column; gap: 12px; text-align: center; }}
        .badge-pill {{
            display: inline-flex; align-items: center; justify-content: center; align-self: center;
            background: rgba(56, 189, 248, 0.18); border: 1.5px solid rgba(56, 189, 248, 0.5);
            padding: 8px 24px; border-radius: 999px; font-size: 18px; font-weight: 800; color: #38bdf8;
            letter-spacing: 1.5px; text-transform: uppercase;
        }}
        .main-title {{
            font-family: 'Space Grotesk', sans-serif; font-size: 54px; font-weight: 900;
            line-height: 1.1; letter-spacing: -2px; color: #ffffff; text-shadow: 0 4px 28px rgba(0,0,0,0.9);
        }}
        .main-sub {{ font-size: 22px; color: #cbd5e1; font-weight: 500; max-width: 920px; margin: 0 auto; line-height: 1.4; }}

        /* Estilos Escena 1 */
        .problem-card {{ background: rgba(15, 23, 42, 0.90); border: 2px solid #ef4444; border-radius: 28px; padding: 32px; display: flex; flex-direction: column; gap: 24px; }}
        .problem-header {{ display: flex; align-items: center; gap: 18px; }}
        .warning-icon {{ font-size: 46px; }}
        .problem-title {{ font-size: 26px; font-weight: 900; color: #f87171; }}
        .problem-sub {{ font-size: 19px; color: #cbd5e1; }}
        .stats-row {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; }}
        .stat-pill {{ background: rgba(30, 41, 59, 0.9); border: 1.5px solid rgba(255, 255, 255, 0.15); border-radius: 18px; padding: 20px; text-align: center; }}
        .stat-num {{ font-size: 38px; font-weight: 900; color: #38bdf8; font-family: 'Space Grotesk', sans-serif; display: block; }}
        .stat-lbl {{ font-size: 15px; color: #94a3b8; font-weight: 700; text-transform: uppercase; }}

        /* Estilos Escena 2 */
        .grid-4 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }}
        .card-mini {{ background: rgba(15, 23, 42, 0.92); border: 1.5px solid rgba(255, 255, 255, 0.18); border-radius: 24px; padding: 26px; display: flex; flex-direction: column; gap: 10px; }}
        .c-ico {{ font-size: 42px; }}
        .c-tit {{ font-size: 24px; font-weight: 800; color: #ffffff; }}
        .c-desc {{ font-size: 17px; color: #94a3b8; line-height: 1.35; }}

        /* Estilos Escena 3 */
        .browser-mockup {{ background: rgba(15, 23, 42, 0.94); border: 2px solid #38bdf8; border-radius: 28px; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,0.8); }}
        .mockup-bar {{ background: #0f172a; padding: 16px 24px; display: flex; align-items: center; gap: 16px; border-bottom: 1px solid rgba(255, 255, 255, 0.1); }}
        .dots {{ display: flex; gap: 8px; }}
        .dots span {{ width: 14px; height: 14px; border-radius: 50%; display: inline-block; }}
        .d-red {{ background: #ef4444; }} .d-yel {{ background: #f59e0b; }} .d-gre {{ background: #10b981; }}
        .mockup-url {{ background: rgba(30, 41, 59, 0.8); padding: 8px 20px; border-radius: 999px; font-size: 16px; color: #94a3b8; font-family: monospace; flex: 1; text-align: center; }}
        .mockup-body {{ padding: 28px; display: flex; flex-direction: column; gap: 20px; }}
        .filter-chips {{ display: flex; gap: 12px; flex-wrap: wrap; }}
        .chip {{ background: rgba(30, 41, 59, 0.8); border: 1.5px solid rgba(255, 255, 255, 0.15); padding: 10px 18px; border-radius: 999px; font-size: 16px; font-weight: 700; color: #cbd5e1; }}
        .chip.active {{ background: #2563eb; border-color: #60a5fa; color: #ffffff; }}
        .deal-preview {{ background: rgba(30, 41, 59, 0.7); border: 1.5px solid rgba(56, 189, 248, 0.4); border-radius: 20px; padding: 22px; display: flex; flex-direction: column; gap: 12px; }}
        .deal-top {{ display: flex; justify-content: space-between; align-items: center; }}
        .deal-tag {{ font-size: 14px; font-weight: 800; color: #38bdf8; }}
        .deal-disc {{ background: #10b981; color: #064e3b; font-size: 14px; font-weight: 900; padding: 4px 10px; border-radius: 6px; }}
        .deal-name {{ font-size: 24px; font-weight: 900; color: #ffffff; }}
        .deal-prices {{ display: flex; justify-content: space-between; background: rgba(15, 23, 42, 0.8); padding: 14px 20px; border-radius: 14px; }}
        .p-col {{ display: flex; flex-direction: column; }}
        .p-lbl {{ font-size: 12px; font-weight: 800; color: #94a3b8; }}
        .p-old {{ font-size: 22px; font-weight: 800; color: #94a3b8; text-decoration: line-through; }}
        .p-new {{ font-size: 26px; font-weight: 900; color: #4ade80; }}

        /* Estilos Escena 4 */
        .legal-card {{ background: linear-gradient(135deg, rgba(6, 78, 59, 0.88) 0%, rgba(15, 23, 42, 0.94) 100%); border: 2.5px solid #10b981; border-radius: 28px; padding: 32px; display: flex; flex-direction: column; gap: 20px; box-shadow: 0 0 50px rgba(16, 185, 129, 0.35); }}
        .legal-badge-row {{ display: flex; align-items: center; gap: 16px; }}
        .legal-shield {{ font-size: 44px; }}
        .legal-tit {{ font-size: 21px; font-weight: 900; color: #a7f3d0; letter-spacing: 0.5px; }}
        .legal-items {{ display: flex; flex-direction: column; gap: 14px; font-size: 20px; color: #e2e8f0; }}
        .l-item {{ display: flex; align-items: center; gap: 14px; }}
        .check-ico {{ font-size: 24px; }}
        .profit-highlight {{ background: rgba(15, 23, 42, 0.85); border: 2px dashed #10b981; border-radius: 18px; padding: 18px 24px; display: flex; justify-content: space-between; align-items: center; font-size: 20px; font-weight: 800; color: #ffffff; }}
        .profit-val {{ font-size: 34px; font-weight: 900; color: #4ade80; font-family: 'Space Grotesk', sans-serif; }}

        /* Estilos Escena 5 */
        .channels-card {{ display: flex; flex-direction: column; gap: 16px; }}
        .chan-row {{ background: rgba(15, 23, 42, 0.92); border: 1.5px solid rgba(255, 255, 255, 0.15); border-radius: 22px; padding: 22px 28px; display: flex; align-items: center; justify-content: space-between; }}
        .chan-row.whatsapp {{ border-color: rgba(37, 211, 102, 0.6); box-shadow: 0 0 25px rgba(37, 211, 102, 0.2); }}
        .chan-row.telegram {{ border-color: rgba(56, 189, 248, 0.6); box-shadow: 0 0 25px rgba(56, 189, 248, 0.2); }}
        .chan-ico {{ font-size: 40px; margin-right: 18px; }}
        .chan-tit {{ font-size: 22px; font-weight: 900; color: #ffffff; }}
        .chan-sub {{ font-size: 16px; color: #94a3b8; }}
        .chan-badge {{ background: #22c55e; color: #052e16; font-size: 15px; font-weight: 900; padding: 6px 14px; border-radius: 999px; }}

        .final-cta-btn {{
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            border: 2px solid #ffffff; border-radius: 26px; padding: 26px 34px;
            display: flex; align-items: center; justify-content: space-between;
            box-shadow: 0 20px 60px rgba(37, 99, 235, 0.95), 0 0 45px rgba(59, 130, 246, 0.8);
            transform: scale(1.02);
        }}
        .cta-txt-col {{ display: flex; flex-direction: column; gap: 4px; }}
        .cta-head {{ font-size: 26px; font-weight: 900; color: #ffffff; }}
        .cta-bot {{ font-size: 18px; color: rgba(255, 255, 255, 0.9); font-weight: 600; }}
        .cta-cir {{ width: 52px; height: 52px; background: rgba(255, 255, 255, 0.25); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 26px; }}
    </style>
</head>
<body>
    <div class="bg-drone"></div>
    <div class="bg-overlay"></div>
    <div class="content">
        <div class="hud-header">
            <div class="hud-brand"><div class="pulse-dot"></div> RADARALERTAS.ES</div>
            <div class="hud-status">● CÓMO FUNCIONA EL SISTEMA</div>
        </div>
        <div class="hero-block">
            <div class="badge-pill">{badge}</div>
            <div class="main-title">{title}</div>
            <div class="main-sub">{sub}</div>
        </div>
        {content_block}
        <div class="hud-header" style="justify-content: center; background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.1);">
            <div style="font-size: 16px; color: #94a3b8; font-weight: 600;">📡 Plataforma de Monitorización Pública 24/7 • Libre de Cargas</div>
        </div>
    </div>
</body>
</html>"""

async def renderizar_video_tutorial():
    print("\n🎬 ==================================================")
    print("🎥 GENERANDO VÍDEO TUTORIAL: CÓMO FUNCIONA RADARALERTAS")
    print("🎬 ==================================================")

    # 1. Locución neural
    audio_path = OUTPUT_DIR / "tutorial_radaralertas_audio.mp3"
    print("🎙️ 1. Generando locución neural...")
    tts = edge_tts.Communicate(text=TUTORIAL_SCRIPT, voice=VOICE, rate="+6%")
    await tts.save(str(audio_path))

    cmd_dur = ["ffmpeg", "-i", str(audio_path), "-f", "null", "-"]
    res = subprocess.run(cmd_dur, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    duracion_real = 45.0
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            partes = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = partes.split(":")
            duracion_real = float(h) * 3600 + float(m) * 60 + float(s)
            break
    print(f"  ✓ Locución lista: {duracion_real:.2f} s")

    # 2. Definición de escenas y tiempos proporcionales
    scenes = [
        {"idx": 1, "dur": 6.5, "bg": TEMPLATES_DIR / "fachada_edificio.jpg"},
        {"idx": 2, "dur": 8.5, "bg": TEMPLATES_DIR / "barcelona_aerea.jpg"},
        {"idx": 3, "dur": 11.0, "bg": TEMPLATES_DIR / "satelite_tierra.jpg"},
        {"idx": 4, "dur": 11.0, "bg": TEMPLATES_DIR / "barrio_pilar_aerea.jpg"},
        {"idx": 5, "dur": 9.0, "bg": TEMPLATES_DIR / "barcelona_aerea.jpg"},
    ]
    duracion_base = sum(s["dur"] for s in scenes)
    factor = duracion_real / duracion_base

    frames_sub_dir = OUTPUT_DIR / "frames_tutorial"
    frames_sub_dir.mkdir(parents=True, exist_ok=True)

    print("🖼️ 2. Renderizando fotogramas con Playwright...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1080, "height": 1920})
        frame_files = []

        for s in scenes:
            bg_uri = img_to_b64(s["bg"])
            html = build_scene_html(s["idx"], bg_uri)
            await page.set_content(html, wait_until="networkidle")
            frame_png = frames_sub_dir / f"scene_{s['idx']}.png"
            await page.screenshot(path=str(frame_png))
            frame_files.append((frame_png, s["dur"]))
            print(f"  ✓ Escena {s['idx']} capturada")

        await browser.close()

    print("✂️ 3. Ensamblando clips de vídeo...")
    clips = []
    for i, (f_path, dur) in enumerate(frame_files, 1):
        dur_adj = dur * factor
        clip_mp4 = frames_sub_dir / f"clip_{i:02d}.mp4"
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

    ruta_salida_final = OUTPUT_DIR / "VIDEO_TUTORIAL_COMO_FUNCIONA_RADARALERTAS.mp4"
    ruta_en_semana = BASE_DIR / "output" / "semana_actual" / "00_TUTORIAL_COMO_FUNCIONA_RADARALERTAS.mp4"

    print("🎵 4. Mezclando voz y música de tensión...")
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
            str(ruta_salida_final)
        ]
    else:
        cmd_final = ["ffmpeg", "-y", "-i", str(raw_mp4), "-i", str(audio_path), "-c:v", "copy", "-c:a", "aac", "-t", f"{duracion_real:.2f}", str(ruta_salida_final)]

    subprocess.run(cmd_final, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    shutil.copyfile(ruta_salida_final, ruta_en_semana)

    # También copiar a docs/assets/ para que esté disponible en la Web Vercel
    docs_video_dir = BASE_DIR / "docs" / "assets"
    docs_video_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ruta_salida_final, docs_video_dir / "tutorial_radaralertas.mp4")

    print(f"\n🎉 ¡VÍDEO TUTORIAL COMPLETADO!")
    print(f"  📁 Salida principal: {ruta_salida_final}")
    print(f"  📁 En semana_actual: {ruta_en_semana}")
    print(f"  📁 En docs/assets: {docs_video_dir / 'tutorial_radaralertas.mp4'}")

if __name__ == "__main__":
    asyncio.run(renderizar_video_tutorial())
