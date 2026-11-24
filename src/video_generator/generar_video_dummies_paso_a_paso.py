"""
Generador del Vídeo Tutorial: Cómo Proceder Paso a Paso en una Subasta (Para Dummies)
Formato: 1080x1920 HD Vertical (TikTok, Reels, Shorts y Web)
Explica qué hacer en la vida real una vez que tienes la información de RadarAlertas.
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
OUTPUT_DIR = BASE_DIR / "output"
TEMPLATES_DIR = BASE_DIR / "assets" / "templates"
AUDIO_BEAT = OUTPUT_DIR / "pro_tension_beat.wav"
VOICE = "es-ES-AlvaroNeural"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def img_to_b64(path: Path) -> str:
    if not path.exists():
        # Fallback si no existe la imagen específica
        for f in TEMPLATES_DIR.glob("*.jpg"):
            path = f
            break
    with open(path, "rb") as f:
        return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode('utf-8')}"

TUTORIAL_SCRIPT = (
    "Ya tienes tu alerta de RadarAlertas en la mano. ¿Y ahora qué haces en la vida real? "
    "Paso uno: Entras en subastas punto boe punto es desde tu móvil. Te identificas en dos segundos con tu Cl@ve PIN o Certificado Digital, igual que para la renta. "
    "Paso dos: Para pujar, la ley solo te pide depositar el cinco por ciento de fianza desde tu banco. Si ganas, se descuenta del precio. Si no ganas, el juzgado te devuelve el cien por cien de tu fianza en veinticuatro horas a tu cuenta bancaria. Riesgo cero. "
    "Paso tres: Pones tu puja máxima. La subasta dura veinte días naturales. Si nadie supera tu oferta, ¡el bien es tuyo! "
    "Paso cuatro: El juez te entrega el Decreto de Adjudicación que sustituye a la escritura del notario, ahorrándote más de mil euros. Vas al Registro, lo pones a tu nombre y recoges las llaves. "
    "Todo el procedimiento es telemático y legal. Entra ahora en radaralertas punto com y descarga tu kit de seguridad."
)

def build_scene_html(scene_idx: int, bg_uri: str) -> str:
    if scene_idx == 1:
        badge = "GUÍA PRÁCTICA PARA DUMMIES"
        title = "Tienes la Alerta... ¿Y Ahora Qué Haces?"
        sub = "Cómo proceder en la vida real sin intermediarios ni errores"
        content_block = """
        <div class="problem-card">
            <div class="problem-header">
                <span class="warning-icon">📱</span>
                <div>
                    <div class="problem-title">De la Alerta a las Llaves</div>
                    <div class="problem-sub">El proceso judicial telemático explicado paso a paso en cristiano</div>
                </div>
            </div>
            <div class="stats-row">
                <div class="stat-pill"><span class="stat-num">100%</span><span class="stat-lbl">Online</span></div>
                <div class="stat-pill"><span class="stat-num">5%</span><span class="stat-lbl">Fianza</span></div>
                <div class="stat-pill"><span class="stat-num">24-48h</span><span class="stat-lbl">Devolución</span></div>
            </div>
        </div>
        """
    elif scene_idx == 2:
        badge = "PASO 1 · IDENTIFICACIÓN"
        title = "Entra en subastas.boe.es con Cl@ve"
        sub = "Desde tu móvil o PC sin pisar ningún juzgado"
        content_block = """
        <div class="features-list">
            <div class="feat-item">
                <span class="feat-check">1</span>
                <div><strong>Accede a la Sede Oficial:</strong> Portal único del BOE para toda España.</div>
            </div>
            <div class="feat-item">
                <span class="feat-check">2</span>
                <div><strong>Identifícate con Cl@ve PIN:</strong> La misma que usas para la Renta o la DGT.</div>
            </div>
            <div class="feat-item">
                <span class="feat-check">3</span>
                <div><strong>Localiza el Expediente:</strong> Con el número de referencia que te dio RadarAlertas.</div>
            </div>
        </div>
        """
    elif scene_idx == 3:
        badge = "PASO 2 · FIANZA DEL 5%"
        title = "Depositas la Fianza (Dinero Blindado)"
        sub = "Solo el 5% y recuperable al 100% si no ganas"
        content_block = """
        <div class="calc-card">
            <div class="calc-top">
                <span class="calc-badge">PROTECCIÓN LEGAL ART. 652 LEC</span>
                <div class="calc-title">Ejemplo en Piso de 40.000 €</div>
            </div>
            <div class="calc-row">
                <span>Depósito Obligatorio (5%):</span>
                <strong style="color:#10b981;">2.000 €</strong>
            </div>
            <div class="calc-row">
                <span>Si no ganas la subasta:</span>
                <strong style="color:#38bdf8;">Devolución 100% en 24h</strong>
            </div>
            <div class="calc-disclaimer">🛡️ El dinero se consigna en la cuenta oficial del juzgado, nadie puede tocarlo.</div>
        </div>
        """
    elif scene_idx == 4:
        badge = "PASO 3 Y 4 · PUJA Y ADJUDICACIÓN"
        title = "Pones tu Puja y el Juez te da las Llaves"
        sub = "El Decreto Judicial sustituye a la escritura notarial"
        content_block = """
        <div class="calc-card">
            <div class="calc-top">
                <span class="calc-badge">AHORRO DE NOTARÍA: +1.000 €</span>
                <div class="calc-title">Adjudicación Oficial</div>
            </div>
            <div class="calc-row">
                <span>Duración de la Subasta:</span>
                <strong style="color:#f59e0b;">20 Días Naturales</strong>
            </div>
            <div class="calc-row">
                <span>Cargas y Deudas Anteriores:</span>
                <strong style="color:#10b981;">0,00 € (Canceladas por Ley)</strong>
            </div>
            <div class="calc-disclaimer">🔑 El testimonio judicial te otorga la posesión legal inmediata.</div>
        </div>
        """
    else:  # scene 5
        badge = "RADARALERTAS · PLATAFORMA OFICIAL"
        title = "Empieza Hoy con Muestras Gratis"
        sub = "Todo el catálogo auditado con Kit de Seguridad Anti-Riesgo"
        content_block = """
        <div class="cta-box">
            <div class="cta-headline">Visita Ahora la Plataforma</div>
            <div class="cta-url">radaralertas.com</div>
            <div class="cta-sub">1 Oportunidad Gratis por Categoría • Kit Anti-Riesgo a 2,90 €</div>
            <div class="cta-badge">📲 Enlace Directo en el Perfil</div>
        </div>
        """

    return f"""<!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&family=Space+Grotesk:wght@700;900&display=swap" rel="stylesheet">
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{
                width: 1080px;
                height: 1920px;
                background-color: #060911;
                font-family: 'Inter', sans-serif;
                color: #ffffff;
                position: relative;
                overflow: hidden;
            }}
            .bg-image {{
                position: absolute;
                top: 0; left: 0; width: 100%; height: 100%;
                background-image: url('{bg_uri}');
                background-size: cover;
                background-position: center;
                opacity: 0.28;
                filter: blur(10px) brightness(0.65);
                transform: scale(1.05);
            }}
            .overlay {{
                position: absolute;
                top: 0; left: 0; width: 100%; height: 100%;
                background: radial-gradient(circle at 50% 30%, rgba(30, 58, 138, 0.4) 0%, rgba(6, 9, 17, 0.95) 75%);
            }}
            .container {{
                position: relative;
                z-index: 10;
                width: 100%;
                height: 100%;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                padding: 100px 70px 120px;
            }}
            .top-bar {{
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            .logo-wrap {{
                display: flex;
                align-items: center;
                gap: 14px;
            }}
            .logo-icon {{
                background: linear-gradient(135deg, #0284c7, #38bdf8);
                color: #000;
                width: 54px;
                height: 54px;
                border-radius: 14px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 28px;
                font-weight: 900;
                box-shadow: 0 0 25px rgba(56, 189, 248, 0.6);
            }}
            .logo-text {{
                font-family: 'Space Grotesk', sans-serif;
                font-size: 38px;
                font-weight: 900;
                letter-spacing: -1px;
            }}
            .live-badge {{
                display: flex;
                align-items: center;
                gap: 10px;
                background: rgba(16, 185, 129, 0.15);
                border: 1px solid rgba(16, 185, 129, 0.4);
                color: #34d399;
                padding: 10px 20px;
                border-radius: 999px;
                font-size: 18px;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            .live-dot {{
                width: 12px;
                height: 12px;
                border-radius: 50%;
                background: #10b981;
                box-shadow: 0 0 14px #10b981;
            }}
            .scene-main {{
                display: flex;
                flex-direction: column;
                gap: 30px;
            }}
            .badge-pill {{
                align-self: flex-start;
                background: rgba(56, 189, 248, 0.15);
                border: 1px solid rgba(56, 189, 248, 0.5);
                color: #38bdf8;
                font-size: 20px;
                font-weight: 900;
                padding: 10px 24px;
                border-radius: 12px;
                letter-spacing: 1.5px;
            }}
            .scene-title {{
                font-family: 'Space Grotesk', sans-serif;
                font-size: 64px;
                font-weight: 900;
                line-height: 1.1;
                letter-spacing: -1.5px;
            }}
            .scene-sub {{
                font-size: 28px;
                color: #94a3b8;
                line-height: 1.4;
            }}
            .problem-card, .calc-card, .cta-box {{
                background: rgba(15, 23, 42, 0.85);
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 28px;
                padding: 40px;
                backdrop-filter: blur(20px);
                box-shadow: 0 30px 60px rgba(0, 0, 0, 0.6);
            }}
            .problem-header {{
                display: flex;
                align-items: center;
                gap: 20px;
                margin-bottom: 30px;
            }}
            .warning-icon {{
                font-size: 48px;
            }}
            .problem-title {{
                font-size: 32px;
                font-weight: 800;
            }}
            .problem-sub {{
                font-size: 20px;
                color: #94a3b8;
                margin-top: 4px;
            }}
            .stats-row {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 20px;
            }}
            .stat-pill {{
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 18px;
                padding: 24px 16px;
                text-align: center;
            }}
            .stat-num {{
                display: block;
                font-size: 42px;
                font-weight: 900;
                color: #38bdf8;
                font-family: 'Space Grotesk', sans-serif;
            }}
            .stat-lbl {{
                display: block;
                font-size: 16px;
                color: #94a3b8;
                font-weight: 700;
                margin-top: 6px;
                text-transform: uppercase;
            }}
            .features-list {{
                display: flex;
                flex-direction: column;
                gap: 20px;
            }}
            .feat-item {{
                background: rgba(15, 23, 42, 0.85);
                border: 1.5px solid rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                padding: 26px 30px;
                display: flex;
                align-items: center;
                gap: 20px;
                font-size: 24px;
                line-height: 1.4;
            }}
            .feat-check {{
                background: #10b981;
                color: #000;
                width: 44px;
                height: 44px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 900;
                font-size: 22px;
                flex-shrink: 0;
            }}
            .calc-top {{
                margin-bottom: 24px;
            }}
            .calc-badge {{
                background: rgba(16, 185, 129, 0.15);
                border: 1px solid #10b981;
                color: #34d399;
                font-size: 16px;
                font-weight: 900;
                padding: 6px 16px;
                border-radius: 8px;
                display: inline-block;
                margin-bottom: 12px;
            }}
            .calc-title {{
                font-size: 34px;
                font-weight: 900;
            }}
            .calc-row {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 26px;
                padding: 16px 0;
                border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            }}
            .calc-disclaimer {{
                margin-top: 24px;
                font-size: 19px;
                color: #94a3b8;
                line-height: 1.4;
            }}
            .cta-box {{
                text-align: center;
                padding: 60px 40px;
            }}
            .cta-headline {{
                font-size: 28px;
                font-weight: 800;
                color: #94a3b8;
                text-transform: uppercase;
                letter-spacing: 2px;
            }}
            .cta-url {{
                font-family: 'Space Grotesk', sans-serif;
                font-size: 68px;
                font-weight: 900;
                color: #38bdf8;
                margin: 20px 0;
                letter-spacing: -1.5px;
            }}
            .cta-sub {{
                font-size: 24px;
                color: #ffffff;
                margin-bottom: 30px;
            }}
            .cta-badge {{
                display: inline-block;
                background: linear-gradient(135deg, #059669, #10b981);
                color: #ffffff;
                padding: 18px 40px;
                border-radius: 999px;
                font-size: 24px;
                font-weight: 900;
                box-shadow: 0 10px 30px rgba(16, 185, 129, 0.5);
            }}
            .footer-bar {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                padding-top: 30px;
                font-size: 20px;
                color: #64748b;
            }}
        </style>
    </head>
    <body>
        <div class="bg-image"></div>
        <div class="overlay"></div>
        <div class="container">
            <div class="top-bar">
                <div class="logo-wrap">
                    <div class="logo-icon">⚡</div>
                    <div class="logo-text">RadarAlertas</div>
                </div>
                <div class="live-tag">
                    <div class="live-dot"></div>
                    <span>GUÍA OFICIAL 2026</span>
                </div>
            </div>

            <div class="scene-main">
                <div class="badge-pill">{badge}</div>
                <h1 class="scene-title">{title}</h1>
                <p class="scene-sub">{sub}</p>
                {content_block}
            </div>

            <div class="footer-bar">
                <span>🇪🇸 Boletín Oficial del Estado (BOE) & DGT</span>
                <span>radaralertas.com</span>
            </div>
        </div>
    </body>
    </html>
    """

async def renderizar_video_dummies():
    print("🎬 INICIANDO GENERACIÓN: VÍDEO SUBASTAS PARA DUMMIES (Paso a Paso)")
    
    # 1. Generar audio con Edge TTS
    audio_path = OUTPUT_DIR / "tutorial_dummies_audio.mp3"
    print("🗣️ 1. Generando locución con Edge-TTS (AlvaroNeural)...")
    com = edge_tts.Communicate(TUTORIAL_SCRIPT, VOICE, rate="+6%")
    await com.save(str(audio_path))

    # Obtener duración real con ffprobe / ffmpeg
    cmd_dur = ["ffmpeg", "-i", str(audio_path)]
    res = subprocess.run(cmd_dur, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    duracion_real = 46.0
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            partes = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = partes.split(":")
            duracion_real = float(h) * 3600 + float(m) * 60 + float(s)
            break
    print(f"  ✓ Locución lista: {duracion_real:.2f} s")

    # 2. Definición de escenas
    scenes = [
        {"idx": 1, "dur": 6.5, "bg": TEMPLATES_DIR / "fachada_edificio.jpg"},
        {"idx": 2, "dur": 9.0, "bg": TEMPLATES_DIR / "barcelona_aerea.jpg"},
        {"idx": 3, "dur": 11.5, "bg": TEMPLATES_DIR / "barrio_pilar_aerea.jpg"},
        {"idx": 4, "dur": 11.0, "bg": TEMPLATES_DIR / "satelite_tierra.jpg"},
        {"idx": 5, "dur": 8.0, "bg": TEMPLATES_DIR / "barcelona_aerea.jpg"},
    ]
    duracion_base = sum(s["dur"] for s in scenes)
    factor = duracion_real / duracion_base

    frames_sub_dir = OUTPUT_DIR / "frames_dummies"
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

    ruta_salida_final = OUTPUT_DIR / "VIDEO_TUTORIAL_DUMMIES_COMO_PUJAR_PASO_A_PASO.mp4"
    ruta_en_semana = BASE_DIR / "output" / "semana_actual" / "08_TUTORIAL_DUMMIES_COMO_PUJAR.mp4"
    (BASE_DIR / "output" / "semana_actual").mkdir(parents=True, exist_ok=True)

    print("🎵 4. Mezclando voz y música de fondo...")
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

    # Copiar a docs/assets/ para reproducir en la web
    docs_video_dir = BASE_DIR / "docs" / "assets"
    docs_video_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ruta_salida_final, docs_video_dir / "tutorial_dummies_paso_a_paso.mp4")

    print(f"\n🎉 ¡VÍDEO PARA DUMMIES COMPLETADO!")
    print(f"  📁 Salida principal: {ruta_salida_final}")
    print(f"  📁 En semana_actual: {ruta_en_semana}")
    print(f"  📁 En docs/assets: {docs_video_dir / 'tutorial_dummies_paso_a_paso.mp4'}")

if __name__ == "__main__":
    asyncio.run(renderizar_video_dummies())
