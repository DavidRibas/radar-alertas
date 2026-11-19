"""
Generador de Vídeo 9:16 de Alto Impacto con la Guía de Estilo Stitch (BMad)
Localización: Barcelona (Eixample)
Resolución: 1080x1920 (TikTok, Reels, Shorts)
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
ASSETS_DIR = BASE_DIR / "assets"
TEMPLATES_DIR = ASSETS_DIR / "templates"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BCN_BG_PATH = TEMPLATES_DIR / "barcelona_aerea.jpg"
AUDIO_BEAT_PATH = OUTPUT_DIR / "pro_tension_beat.wav"
VOZ_TTS = "es-ES-AlvaroNeural"

# Guion periodístico, directo y de alta retención
GUION_COMPLETO = (
    "Fijaos en lo que acaba de publicar el BOE hace unas horas en Barcelona. "
    "Un piso en pleno Eixample que sale a subasta por tan solo cincuenta y cuatro mil euros. "
    "Su tasación oficial supera los trescientos diez mil euros, y en Idealista los pisos similares en la misma manzana no bajan de trescientos cuarenta mil. "
    "¿Dónde está el truco? Hemos auditado el expediente: cero euros de cargas. "
    "Por el artículo 674 de la Ley de Enjuiciamiento Civil, todas las deudas anteriores quedan canceladas por el juzgado. "
    "He preparado la Guía Práctica Oficial en PDF donde explico paso a paso cómo participar sin riesgo. "
    "Descárgatela gratis en el enlace de mi perfil."
)


def obtener_ffmpeg() -> str:
    ruta = shutil.which("ffmpeg")
    if ruta:
        return ruta
    winget = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WinGet" / "Packages" / "Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe" / "ffmpeg-9.0.2-full_build" / "bin" / "ffmpeg.exe"
    if winget.exists():
        return str(winget)
    return "ffmpeg"


def get_base64_bg():
    with open(BCN_BG_PATH, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{b64}"


def build_scene_html(scene_idx: int) -> str:
    bg_uri = get_base64_bg()
    
    # CSS común
    common_css = f"""
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
        padding: 85px 54px 105px;
    }}
    .bg-drone {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url('{bg_uri}');
        background-size: cover;
        background-position: center;
        opacity: 0.74;
        filter: saturate(1.2) contrast(1.15) brightness(0.85);
        z-index: 0;
    }}
    .bg-overlay {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle at 50% 25%, rgba(37, 99, 235, 0.16) 0%, transparent 65%),
                    linear-gradient(180deg, rgba(6, 9, 19, 0.42) 0%, rgba(6, 9, 19, 0.82) 100%);
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
    .hud-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 14px 28px;
        background: rgba(15, 23, 42, 0.85);
        border: 1.5px solid rgba(255, 255, 255, 0.2);
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
        font-family: 'Space Grotesk', 'Syne', sans-serif;
        font-size: 54px;
        font-weight: 900;
        line-height: 1.12;
        letter-spacing: -1.5px;
        color: #ffffff;
        text-shadow: 0 4px 24px rgba(0, 0, 0, 0.95);
    }}
    """

    if scene_idx == 1:
        # ESCENA 1: EL GANCHO (Drone + Oportunidad Barcelona)
        body_content = """
        <div class="hud-header">
            <div class="hud-live"><div class="pulse-dot"></div> RADAR JUDICIAL BOE</div>
            <div class="hud-gps">📍 41.3879° N, 2.1699° E</div>
        </div>

        <div class="hero-title">
            <div class="hero-eyebrow">BARCELONA • DISTRITO EIXAMPLE</div>
            <div class="hero-headline">Piso de 85 m² en Barcelona que sale a Subasta por 54.000 €</div>
        </div>

        <div style="background: linear-gradient(135deg, rgba(6, 78, 59, 0.88) 0%, rgba(15, 23, 42, 0.92) 100%); border: 2.5px solid #10b981; box-shadow: 0 20px 60px rgba(0,0,0,0.7), 0 0 40px rgba(16,185,129,0.35); backdrop-filter: blur(28px); border-radius: 32px; padding: 42px 42px; display: flex; flex-direction: column; gap: 16px; margin-top: 20px;">
            <div style="background: #10b981; color: #064e3b; padding: 8px 22px; border-radius: 999px; font-weight: 800; font-size: 20px; width: fit-content; box-shadow: 0 0 16px rgba(16,185,129,0.5);">SUBASTA ACTIVA EN EL BOE</div>
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 120px; font-weight: 900; color: #00ff88; line-height: 1; letter-spacing: -3px; text-shadow: 0 0 35px rgba(0,255,136,0.6);">54.000 €</div>
            <div style="display: flex; gap: 14px; align-items: center;">
                <div style="background: rgba(16, 185, 129, 0.25); border: 1.5px solid #10b981; padding: 8px 20px; border-radius: 12px; font-size: 24px; font-weight: 800; color: #ffffff;">AHORRO: -84%</div>
                <div style="font-size: 24px; font-weight: 700; color: #a7f3d0;">Margen: +286.000 €</div>
            </div>
        </div>

        <div style="background: rgba(0,0,0,0.85); border: 2px solid #fbbf24; box-shadow: 0 0 30px rgba(251, 191, 36, 0.35); border-radius: 24px; padding: 26px; text-align: center; margin-top: auto;">
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 34px; font-weight: 800; color: #fbbf24; letter-spacing: -0.5px;">"¿CÓMO ES POSIBLE ESTE PRECIO EN EL EIXAMPLE?"</div>
        </div>
        """

    elif scene_idx == 2:
        # ESCENA 2: COMPARATIVA BRUTAL (Idealista vs BOE)
        body_content = """
        <div class="hud-header">
            <div class="hud-live"><div class="pulse-dot"></div> COMPARATIVA DE MERCADO</div>
            <div class="hud-gps">📍 C/ Consell de Cent, BCN</div>
        </div>

        <div class="hero-title">
            <div class="hero-eyebrow">CRUCE CON PORTALES INMOBILIARIOS</div>
            <div class="hero-headline">Misma calle. Mismo metraje. Dos realidades.</div>
        </div>

        <!-- Card Idealista -->
        <div style="background: rgba(20, 15, 25, 0.82); border: 2px solid rgba(239, 68, 68, 0.6); box-shadow: 0 16px 36px rgba(0,0,0,0.6); backdrop-filter: blur(24px); border-radius: 26px; padding: 30px 38px; display: flex; flex-direction: column; gap: 10px;">
            <div style="background: rgba(239,68,68,0.25); border: 1px solid rgba(239,68,68,0.5); padding: 6px 18px; border-radius: 999px; font-size: 18px; font-weight: 700; color: #fca5a5; width: fit-content;">MERCADO LIBRE (IDEALISTA / FOTOCASA)</div>
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 78px; font-weight: 800; color: #ef4444; position: relative; width: fit-content; letter-spacing: -2px;">
                340.000 €
                <div style="position: absolute; left: -10px; top: 50%; width: calc(100% + 20px); height: 7px; background: #ef4444; transform: rotate(-6deg); border-radius: 4px; box-shadow: 0 0 14px rgba(239,68,68,0.85);"></div>
            </div>
            <div style="font-size: 19px; color: #cbd5e1; font-weight: 500;">Precio medio publicado en el barrio + 5% honorarios de agencia</div>
        </div>

        <!-- Card BOE -->
        <div style="background: linear-gradient(135deg, rgba(6, 78, 59, 0.9) 0%, rgba(15, 23, 42, 0.94) 100%); border: 2.5px solid #10b981; box-shadow: 0 20px 50px rgba(0,0,0,0.7), 0 0 40px rgba(16,185,129,0.35); backdrop-filter: blur(24px); border-radius: 28px; padding: 32px 38px; display: flex; flex-direction: column; gap: 12px;">
            <div style="background: #10b981; color: #064e3b; padding: 6px 18px; border-radius: 999px; font-weight: 800; font-size: 19px; width: fit-content;">SUBASTA JUDICIAL BOE</div>
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 96px; font-weight: 900; color: #00ff88; line-height: 1; letter-spacing: -3px; text-shadow: 0 0 35px rgba(0,255,136,0.6);">54.000 €</div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 4px;">
                <div style="background: rgba(16, 185, 129, 0.3); border: 1.5px solid #10b981; padding: 8px 18px; border-radius: 10px; font-size: 22px; font-weight: 800; color: #ffffff;">AHORRO: -84%</div>
                <div style="font-size: 22px; font-weight: 700; color: #a7f3d0;">Margen: +286.000 €</div>
            </div>
        </div>
        """

    elif scene_idx == 3:
        # ESCENA 3: SEGURIDAD JURÍDICA Y AUDITORÍA (Cero cargas)
        body_content = """
        <div class="hud-header">
            <div class="hud-live"><div class="pulse-dot"></div> AUDITORÍA JUDICIAL</div>
            <div class="hud-gps">Expediente Oficial Verificado</div>
        </div>

        <div class="hero-title">
            <div class="hero-eyebrow">AUDITORÍA DE RIESGOS Y CARGAS</div>
            <div class="hero-headline">¿Te comes las deudas del anterior dueño? Rotundamente NO.</div>
        </div>

        <!-- Card Cero Cargas Legal -->
        <div style="background: rgba(2, 132, 199, 0.22); border: 2px solid rgba(56, 189, 248, 0.55); box-shadow: 0 16px 40px rgba(0,0,0,0.65); backdrop-filter: blur(24px); border-radius: 26px; padding: 32px 36px; display: flex; align-items: center; gap: 24px;">
            <div style="width: 72px; height: 72px; background: rgba(56, 189, 248, 0.25); border: 1.5px solid rgba(56, 189, 248, 0.5); border-radius: 20px; display: flex; align-items: center; justify-content: center; color: #38bdf8; flex-shrink: 0;">
                <svg width="42" height="42" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                    <path d="M9 12l2 2 4-4"/>
                </svg>
            </div>
            <div style="display: flex; flex-direction: column; gap: 6px;">
                <div style="font-size: 26px; font-weight: 900; color: #ffffff;">CARGAS HIPOTECARIAS: 0,00 €</div>
                <div style="font-size: 19px; color: #bae6fd; font-weight: 600;">Canceladas por Mandamiento Judicial (Art. 674 LEC)</div>
            </div>
        </div>

        <!-- Ficha de Registro y Posesión -->
        <div style="background: rgba(15, 23, 42, 0.88); border: 1.5px solid rgba(255, 255, 255, 0.15); backdrop-filter: blur(20px); border-radius: 24px; padding: 26px 32px; display: flex; flex-direction: column; gap: 14px;">
            <div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px;">
                <span style="font-size: 20px; color: #94a3b8; font-weight: 600;">Situación Posesoria:</span>
                <span style="font-size: 20px; color: #4ade80; font-weight: 800;">✓ Inmueble Vacío (Sin Ocupantes)</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="font-size: 20px; color: #94a3b8; font-weight: 600;">Fianza Judicial (5%):</span>
                <span style="font-size: 20px; color: #38bdf8; font-weight: 800;">100% Retornable si no ganas</span>
            </div>
        </div>

        <!-- Caja de Margen Oro -->
        <div style="background: rgba(0,0,0,0.92); border: 2.5px solid #fbbf24; box-shadow: 0 0 35px rgba(251, 191, 36, 0.4); border-radius: 24px; padding: 26px; text-align: center; margin-top: auto;">
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 36px; font-weight: 900; color: #fbbf24; letter-spacing: -0.5px;">“HABLAMOS DE 286.000 € DE MARGEN LIMPIO”</div>
        </div>
        """

    elif scene_idx == 4:
        # ESCENA 4: CALL TO ACTION (Descarga Guía PDF y Canal)
        body_content = """
        <div class="hud-header">
            <div class="hud-live"><div class="pulse-dot"></div> GUÍA PRÁCTICA OFICIAL</div>
            <div class="hud-gps">100% Gratuita en PDF</div>
        </div>

        <div class="hero-title">
            <div class="hero-eyebrow">¿CÓMO PARTICIPAR PASO A PASO?</div>
            <div class="hero-headline">Aprende a pujar sin riesgo y detectar chollos antes que nadie.</div>
        </div>

        <!-- Checklist Guía -->
        <div style="background: rgba(15, 23, 42, 0.88); border: 1.5px solid rgba(56, 189, 248, 0.4); backdrop-filter: blur(24px); border-radius: 28px; padding: 32px 36px; display: flex; flex-direction: column; gap: 18px;">
            <div style="display: flex; align-items: center; gap: 16px;">
                <div style="font-size: 26px; color: #22c55e;">✔</div>
                <div style="font-size: 22px; font-weight: 700; color: #f8fafc;">Cómo funciona la fianza del 5% que devuelve el juzgado</div>
            </div>
            <div style="display: flex; align-items: center; gap: 16px;">
                <div style="font-size: 26px; color: #22c55e;">✔</div>
                <div style="font-size: 22px; font-weight: 700; color: #f8fafc;">Artículo 674 LEC: qué deudas quedan anuladas por Ley</div>
            </div>
            <div style="display: flex; align-items: center; gap: 16px;">
                <div style="font-size: 26px; color: #22c55e;">✔</div>
                <div style="font-size: 22px; font-weight: 700; color: #f8fafc;">Alertas en directo de subastas filtradas por IA</div>
            </div>
        </div>

        <!-- Botón Gran CTA Azul Cobalto -->
        <div style="background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); border: 2px solid rgba(147, 197, 253, 0.6); box-shadow: 0 20px 50px rgba(37, 99, 235, 0.6); border-radius: 30px; padding: 32px 42px; display: flex; align-items: center; justify-content: space-between; margin-top: auto;">
            <div style="display: flex; flex-direction: column; gap: 6px;">
                <div style="font-size: 30px; font-weight: 900; color: #ffffff; letter-spacing: -0.5px;">Descarga la Guía en PDF (0 €)</div>
                <div style="font-size: 20px; color: rgba(255, 255, 255, 0.9); font-weight: 600;">Enlace directo en la biografía del perfil</div>
            </div>
            <div style="width: 64px; height: 64px; background: rgba(255, 255, 255, 0.25); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 30px;">➔</div>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&family=Space+Grotesk:wght@700;800;900&display=swap" rel="stylesheet">
    <style>
        {common_css}
    </style>
</head>
<body>
    <div class="bg-drone"></div>
    <div class="bg-overlay"></div>
    <div class="content">
        {body_content}
    </div>
</body>
</html>"""


async def render_escenas():
    """Genera las 4 escenas visuales en PNG a 1080x1920 con Playwright."""
    print("🎨 Renderizando 4 escenas con Playwright (Fondo Barcelona + Glassmorphism Stitch)...")
    rutas = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1920})
        
        for i in range(1, 5):
            html = build_scene_html(i)
            await page.set_content(html, wait_until="networkidle")
            out_img = OUTPUT_DIR / f"stitch_bcn_e{i}.png"
            await page.screenshot(path=str(out_img))
            rutas.append(out_img)
            print(f"  ✓ Escena {i} generada: {out_img.name}")
            
        await browser.close()
    return rutas


async def generar_locucion(ruta_audio: Path) -> float:
    """Genera locución neural con edge_tts y devuelve la duración exacta."""
    print("🎙️ Generando locución ultra-humana con edge_tts...")
    tts = edge_tts.Communicate(text=GUION_COMPLETO, voice=VOZ_TTS, rate="+6%")
    await tts.save(str(ruta_audio))
    
    # Calcular duración
    ffmpeg_bin = obtener_ffmpeg()
    cmd = [ffmpeg_bin, "-i", str(ruta_audio), "-f", "null", "-"]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    duracion = 25.0
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            partes = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = partes.split(":")
            duracion = float(h) * 3600 + float(m) * 60 + float(s)
            break
    print(f"  ✓ Duración de locución: {duracion:.2f} segundos")
    return duracion


def ensamblar_video_final(escenas: list, duracion_total: float, ruta_audio: Path, ruta_salida: Path):
    """
    Ensambla las escenas con zoom dinámico Ken Burns, funde el beat de fondo al 15%
    y genera el MP4 final a 1080x1920 30fps listo para TikTok / Reels.
    """
    ffmpeg_bin = obtener_ffmpeg()
    dur_escena = duracion_total / 4.0
    print(f"🎬 Ensamblando vídeo ({dur_escena:.2f}s por escena, total {duracion_total:.2f}s)...")
    
    clips = []
    for i, escena in enumerate(escenas, 1):
        clip_path = OUTPUT_DIR / f"stitch_clip_{i}.mp4"
        # Zoom sutil para dar movimiento cinematográfico a cada diapositiva
        # zoom de 1.0 a 1.05
        frames = int(dur_escena * 30)
        vf_zoom = f"scale=1080:1920,zoompan=z='min(zoom+0.0004,1.06)':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30"
        
        cmd = [
            ffmpeg_bin, "-y",
            "-loop", "1", "-t", f"{dur_escena:.2f}",
            "-i", str(escena),
            "-vf", vf_zoom,
            "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
            "-an", str(clip_path)
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        clips.append(clip_path)

    # Archivo de concatenación
    concat_txt = OUTPUT_DIR / "concat_stitch.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for c in clips:
            f.write(f"file '{c.name}'\n")

    video_raw = OUTPUT_DIR / "stitch_video_raw.mp4"
    cmd_concat = [
        ffmpeg_bin, "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        str(video_raw)
    ]
    subprocess.run(cmd_concat, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    # Mezcla de Audio: Voz 100% + Música de tensión al 14%
    if AUDIO_BEAT_PATH.exists():
        cmd_final = [
            ffmpeg_bin, "-y",
            "-i", str(video_raw),
            "-i", str(ruta_audio),
            "-stream_loop", "-1", "-i", str(AUDIO_BEAT_PATH),
            "-filter_complex",
            f"[1:a]volume=1.0[v];[2:a]volume=0.14[m];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]",
            "-map", "0:v", "-map", "[a]",
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            "-t", f"{duracion_total:.2f}",
            str(ruta_salida)
        ]
    else:
        cmd_final = [
            ffmpeg_bin, "-y",
            "-i", str(video_raw),
            "-i", str(ruta_audio),
            "-map", "0:v", "-map", "1:a",
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            "-t", f"{duracion_total:.2f}",
            str(ruta_salida)
        ]

    subprocess.run(cmd_final, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    print(f"🎉 VÍDEO FINAL GENERADO: {ruta_salida}")


async def main():
    ruta_audio = OUTPUT_DIR / "stitch_bcn_locucion.mp3"
    ruta_video_final = OUTPUT_DIR / "VIDEO_BARCELONA_STITCH_FINAL.mp4"
    
    # 1. Renderizar diapositivas
    escenas = await render_escenas()
    
    # 2. Generar locución de voz
    duracion = await generar_locucion(ruta_audio)
    
    # 3. Ensamblar vídeo con zoom cinematográfico y música
    ensamblar_video_final(escenas, duracion, ruta_audio, ruta_video_final)


if __name__ == "__main__":
    asyncio.run(main())
