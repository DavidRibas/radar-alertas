"""
Motor de Vídeo Animado en Tiempo Real (Playwright + CSS3 Keyframes + JS Counters)
Implementa la especificación BMad con movimiento completo:
1. Fondo Dron Barcelona en movimiento continuo cinemático (Pan & Zoom CSS).
2. Contador numérico ascendente del precio BOE (0 € -> 54.000 €).
3. Animación de tachado dinámico en el precio de Idealista (340.000 €).
4. Contador de margen limpio animado (+286.000 €).
5. Punto de radar parpadeante en vivo.
6. Pulso y resplandor en la cláusula legal (Art. 674 LEC) y el botón CTA.
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
REC_DIR = OUTPUT_DIR / "rec_animado"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REC_DIR.mkdir(parents=True, exist_ok=True)

BCN_BG = TEMPLATES_DIR / "barcelona_aerea.jpg"
AUDIO_BEAT = OUTPUT_DIR / "pro_tension_beat.wav"

GUION = (
    "Fijaos en lo que acaba de publicar el BOE en Barcelona. "
    "Un piso de ochenta y cinco metros en pleno Eixample, tres habitaciones y ascensor, por tan solo cincuenta y cuatro mil euros. "
    "En Idealista, los pisos idénticos en esta calle no bajan de trescientos cuarenta mil euros. "
    "Calculad el beneficio: son más de doscientos ochenta y seis mil euros de margen limpio. "
    "¿Y las cargas? Cero euros de deuda previa. Por el artículo seiscientos setenta y cuatro de la LEC, quedan anuladas por el juzgado. "
    "Descárgate la Guía Oficial en PDF gratis en el enlace de mi perfil para aprender a pujar sin riesgo."
)

with open(BCN_BG, "rb") as f:
    bg_b64 = base64.b64encode(f.read()).decode("utf-8")
bg_uri = f"data:image/jpeg;base64,{bg_b64}"


def build_animated_html() -> str:
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Space+Grotesk:wght@700;800;900&display=swap" rel="stylesheet">
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
            padding: 68px 46px 82px;
        }}

        /* 1. MOVIMIENTO DE DRON CINEMÁTICO CONTINUO */
        @keyframes dronePan {{
            0% {{
                transform: scale(1.0) translate(0, 0);
            }}
            50% {{
                transform: scale(1.12) translate(-30px, -20px);
            }}
            100% {{
                transform: scale(1.0) translate(0, 0);
            }}
        }}

        .bg-drone {{
            position: absolute;
            top: -5%;
            left: -5%;
            width: 110%;
            height: 110%;
            background-image: url('{bg_uri}');
            background-size: cover;
            background-position: center;
            opacity: 0.74;
            filter: saturate(1.25) contrast(1.18) brightness(0.85);
            z-index: 0;
            animation: dronePan 30s ease-in-out infinite;
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
            gap: 18px;
            height: 100%;
            justify-content: space-between;
        }}

        /* HUD Superior */
        .hud-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 14px 26px;
            background: rgba(15, 23, 42, 0.9);
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

        /* 2. PULSO RADAR */
        @keyframes pulseGlow {{
            0%, 100% {{ transform: scale(1); box-shadow: 0 0 14px #ef4444; }}
            50% {{ transform: scale(1.3); box-shadow: 0 0 28px #ef4444, 0 0 40px #ef4444; }}
        }}
        .pulse-dot {{
            width: 14px;
            height: 14px;
            background: #ef4444;
            border-radius: 50%;
            animation: pulseGlow 1.2s infinite ease-in-out;
        }}
        .hud-gps {{
            font-size: 19px;
            font-weight: 700;
            color: #38bdf8;
            letter-spacing: 0.5px;
        }}

        /* Cabecera & Specs */
        .hero-block {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        .hero-eyebrow {{
            font-size: 21px;
            font-weight: 800;
            color: #38bdf8;
            letter-spacing: 2px;
            text-transform: uppercase;
        }}
        .hero-headline {{
            font-family: 'Space Grotesk', sans-serif;
            font-size: 52px;
            font-weight: 900;
            line-height: 1.1;
            letter-spacing: -1.5px;
            color: #ffffff;
            text-shadow: 0 4px 24px rgba(0, 0, 0, 0.95);
        }}
        .specs-row {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-top: 4px;
        }}
        .spec-pill {{
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 6px 14px;
            border-radius: 8px;
            font-size: 18px;
            font-weight: 700;
            color: #e2e8f0;
        }}

        /* Card 1: Mercado Libre */
        .card-market {{
            background: rgba(20, 15, 25, 0.82);
            border: 1.5px solid rgba(239, 68, 68, 0.5);
            backdrop-filter: blur(20px);
            border-radius: 24px;
            padding: 24px 32px;
            display: flex;
            flex-direction: column;
            gap: 8px;
            box-shadow: 0 14px 35px rgba(0, 0, 0, 0.6);
        }}
        .badge-market {{
            display: inline-flex;
            align-items: center;
            background: rgba(239, 68, 68, 0.2);
            border: 1px solid rgba(239, 68, 68, 0.5);
            padding: 5px 14px;
            border-radius: 999px;
            font-size: 17px;
            font-weight: 700;
            color: #fca5a5;
            width: fit-content;
        }}
        .price-market-box {{
            position: relative;
            width: fit-content;
        }}
        .price-market {{
            font-family: 'Space Grotesk', sans-serif;
            font-size: 68px;
            font-weight: 800;
            color: #ef4444;
            letter-spacing: -2px;
        }}
        
        /* 3. LÍNEA DE TACHADO ANIMADA */
        .strikethrough-line {{
            position: absolute;
            left: -8px;
            top: 50%;
            height: 6px;
            background: #ef4444;
            transform: rotate(-6deg);
            border-radius: 3px;
            box-shadow: 0 0 14px rgba(239, 68, 68, 0.95);
            width: 0%;
            transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .market-sub {{
            font-size: 18px;
            color: #cbd5e1;
            font-weight: 500;
        }}

        /* Card 2: Subasta BOE Hero */
        .card-boe {{
            background: linear-gradient(135deg, rgba(6, 78, 59, 0.88) 0%, rgba(15, 23, 42, 0.92) 100%);
            border: 2px solid rgba(16, 185, 129, 0.9);
            backdrop-filter: blur(24px);
            border-radius: 28px;
            padding: 28px 36px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.75), 0 0 35px rgba(16, 185, 129, 0.35);
        }}
        .badge-boe {{
            display: inline-flex;
            align-items: center;
            background: #10b981;
            box-shadow: 0 0 16px rgba(16, 185, 129, 0.5);
            padding: 7px 20px;
            border-radius: 999px;
            font-size: 19px;
            font-weight: 800;
            color: #064e3b;
            width: fit-content;
        }}
        .price-boe {{
            font-family: 'Space Grotesk', sans-serif;
            font-size: 104px;
            font-weight: 900;
            color: #00ff88;
            line-height: 1;
            letter-spacing: -3px;
            text-shadow: 0 0 35px rgba(0, 255, 136, 0.65);
        }}
        .boe-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .discount-pill {{
            background: rgba(16, 185, 129, 0.25);
            border: 1.5px solid #10b981;
            padding: 7px 18px;
            border-radius: 10px;
            font-size: 22px;
            font-weight: 800;
            color: #ffffff;
        }}
        .boe-margin {{
            font-size: 22px;
            font-weight: 700;
            color: #a7f3d0;
        }}

        /* Card 3: Seguridad Jurídica */
        .card-legal {{
            background: rgba(2, 132, 199, 0.22);
            border: 1.5px solid rgba(56, 189, 248, 0.5);
            backdrop-filter: blur(20px);
            border-radius: 22px;
            padding: 18px 26px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.55);
        }}
        .legal-top {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}
        .legal-icon {{
            width: 48px;
            height: 48px;
            background: rgba(56, 189, 248, 0.2);
            border: 1px solid rgba(56, 189, 248, 0.4);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #38bdf8;
            flex-shrink: 0;
        }}
        .legal-title {{
            font-size: 22px;
            font-weight: 800;
            color: #ffffff;
        }}
        .legal-sub {{
            font-size: 16px;
            color: #bae6fd;
            font-weight: 600;
        }}
        .legal-audit-pills {{
            display: flex;
            justify-content: space-between;
            border-top: 1px solid rgba(255, 255, 255, 0.12);
            padding-top: 8px;
            font-size: 16px;
        }}
        .audit-item {{
            color: #cbd5e1;
            font-weight: 600;
        }}
        .audit-val {{
            color: #4ade80;
            font-weight: 700;
        }}

        /* 4. CAJA DE MARGEN LIMPIO ANIMADA */
        @keyframes goldGlow {{
            0%, 100% {{ box-shadow: 0 0 25px rgba(245, 158, 11, 0.35); }}
            50% {{ box-shadow: 0 0 45px rgba(245, 158, 11, 0.7); }}
        }}
        .margin-hook {{
            background: rgba(0, 0, 0, 0.9);
            border: 2px solid rgba(245, 158, 11, 0.9);
            border-radius: 20px;
            padding: 18px 24px;
            text-align: center;
            animation: goldGlow 2.5s infinite ease-in-out;
        }}
        .margin-quote {{
            font-family: 'Space Grotesk', sans-serif;
            font-size: 34px;
            font-weight: 800;
            color: #fbbf24;
            letter-spacing: -0.5px;
            text-transform: uppercase;
        }}

        /* 5. BOTÓN CTA PULSANTE */
        @keyframes ctaPulse {{
            0%, 100% {{ transform: scale(1); box-shadow: 0 16px 45px rgba(37, 99, 235, 0.55); }}
            50% {{ transform: scale(1.02); box-shadow: 0 20px 60px rgba(37, 99, 235, 0.85); }}
        }}
        .cta-btn {{
            background: #2563eb;
            border: 1.5px solid rgba(147, 197, 253, 0.5);
            border-radius: 24px;
            padding: 24px 32px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            animation: ctaPulse 2s infinite ease-in-out;
        }}
        .cta-left {{
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}
        .cta-main {{
            font-size: 26px;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: -0.5px;
        }}
        .cta-sub {{
            font-size: 17px;
            color: rgba(255, 255, 255, 0.9);
            font-weight: 600;
        }}
        .cta-arrow {{
            width: 50px;
            height: 50px;
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
        <!-- HUD Superior -->
        <div class="hud-header">
            <div class="hud-live">
                <div class="pulse-dot"></div>
                RADAR JUDICIAL BOE
            </div>
            <div class="hud-gps">📍 41.3879° N, 2.1699° E</div>
        </div>

        <!-- Headline & Specs -->
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

        <!-- Card 1: Mercado Libre -->
        <div class="card-market">
            <div class="badge-market">MERCADO LIBRE (IDEALISTA / FOTOCASA)</div>
            <div class="price-market-box">
                <div class="price-market">340.000 €</div>
                <div id="strike-line" class="strikethrough-line"></div>
            </div>
            <div class="market-sub">Precio medio en C/ Consell de Cent con 5% honorarios de agencia</div>
        </div>

        <!-- Card 2: Subasta BOE Hero -->
        <div class="card-boe">
            <div class="badge-boe">SUBASTA JUDICIAL BOE</div>
            <div id="price-boe" class="price-boe">0 €</div>
            <div class="boe-row">
                <div id="badge-discount" class="discount-pill">AHORRO: -0%</div>
                <div id="boe-margin" class="boe-margin">Margen bruto: +0 €</div>
            </div>
        </div>

        <!-- Card 3: Seguridad Jurídica y Cero Cargas -->
        <div class="card-legal">
            <div class="legal-top">
                <div class="legal-icon">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                        <path d="M9 12l2 2 4-4"/>
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

        <!-- Card 4: Gancho de Margen Dinámico -->
        <div class="margin-hook">
            <div id="margin-quote" class="margin-quote">“CALCULANDO MARGEN LIMPIO...”</div>
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

    <!-- SCRIPT DE ANIMACIONES DINÁMICAS SINCRONIZADAS -->
    <script>
        function animarContador(elementoId, inicio, fin, duracionMs, sufijo = '', prefijo = '') {{
            const obj = document.getElementById(elementoId);
            const tiempoInicio = performance.now();
            function update(ahora) {{
                const transcurrido = ahora - tiempoInicio;
                const progreso = Math.min(transcurrido / duracionMs, 1);
                // Curva easeOutExpo
                const factor = progreso === 1 ? 1 : 1 - Math.pow(2, -10 * progreso);
                const valorActual = Math.floor(inicio + (fin - inicio) * factor);
                obj.innerText = prefijo + valorActual.toLocaleString('es-ES') + sufijo;
                if (progreso < 1) {{
                    requestAnimationFrame(update);
                }}
            }}
            requestAnimationFrame(update);
        }}

        // SECUENCIA DE TIEMPOS
        // 1. Segundo 1.5: Sube el precio del BOE de 0 a 54.000 €
        setTimeout(() => {{
            animarContador('price-boe', 0, 54000, 1600, ' €');
            animarContador('badge-discount', 0, 84, 1600, '%', 'AHORRO: -');
        }}, 1200);

        // 2. Segundo 4.5: Se tacha dinámicamente el precio de Idealista (340.000 €)
        setTimeout(() => {{
            document.getElementById('strike-line').style.width = 'calc(100% + 16px)';
        }}, 4500);

        // 3. Segundo 7.0: Se calcula y sube el margen limpio de 0 a +286.000 €
        setTimeout(() => {{
            animarContador('boe-margin', 0, 286000, 1800, ' €', 'Margen bruto: +');
            setTimeout(() => {{
                document.getElementById('margin-quote').innerText = '“HABLAMOS DE 286.000 € DE MARGEN LIMPIO”';
            }}, 1200);
        }}, 7000);
    </script>
</body>
</html>"""


async def main():
    print("🎙️ 1. Generando locución optimizada...")
    ruta_audio = OUTPUT_DIR / "bcn_animado_locucion.mp3"
    tts = edge_tts.Communicate(text=GUION, voice="es-ES-AlvaroNeural", rate="+6%")
    await tts.save(str(ruta_audio))

    # Calcular duración
    cmd_dur = ["ffmpeg", "-i", str(ruta_audio), "-f", "null", "-"]
    res = subprocess.run(cmd_dur, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    duracion = 28.0
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            partes = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = partes.split(":")
            duracion = float(h) * 3600 + float(m) * 60 + float(s)
            break
    print(f"  ✓ Duración audio: {duracion:.2f} s")

    print("🎬 2. Grabando animación en tiempo real con Playwright Chromium (1080x1920)...")
    html_code = build_animated_html()
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            record_video_dir=str(REC_DIR),
            record_video_size={"width": 1080, "height": 1920}
        )
        page = await context.new_page()
        await page.set_content(html_code, wait_until="networkidle")
        
        # Esperar la duración exacta del audio + 1s de margen
        tiempo_espera = duracion + 1.2
        print(f"  ▶ Grabando {tiempo_espera:.2f} segundos de animación pura...")
        await asyncio.sleep(tiempo_espera)
        
        raw_video_path = await page.video.path()
        await page.close()
        await context.close()
        await browser.close()

    print(f"  ✓ Archivo capturado por Chromium: {raw_video_path}")

    # 3. Mezclar con audio y música en FFmpeg
    ruta_final = OUTPUT_DIR / "VIDEO_BARCELONA_CON_MOVIMIENTO.mp4"
    print("🎵 3. Mezclando locución, música de tensión y vídeo capturado a 1080x1920...")
    
    if AUDIO_BEAT.exists():
        cmd_final = [
            "ffmpeg", "-y",
            "-i", str(raw_video_path),
            "-i", str(ruta_audio),
            "-stream_loop", "-1", "-i", str(AUDIO_BEAT),
            "-filter_complex",
            "[1:a]volume=1.0[v];[2:a]volume=0.14[m];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]",
            "-map", "0:v", "-map", "[a]",
            "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-t", f"{duracion:.2f}",
            str(ruta_final)
        ]
    else:
        cmd_final = [
            "ffmpeg", "-y",
            "-i", str(raw_video_path),
            "-i", str(ruta_audio),
            "-map", "0:v", "-map", "1:a",
            "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-t", f"{duracion:.2f}",
            str(ruta_final)
        ]

    subprocess.run(cmd_final, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    print(f"🎉 VÍDEO CON MOVIMIENTO TOTAL COMPLETADO: {ruta_final}")


if __name__ == "__main__":
    asyncio.run(main())
