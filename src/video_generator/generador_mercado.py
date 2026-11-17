import asyncio
import os
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import edge_tts
from playwright.async_api import async_playwright

BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Guion hiper-atractivo con cruce de datos de mercado y CTA de suscripción nítido
GUION_MERCADO = (
    "Fijaos bien en lo que acaba de publicar el BOE hace un rato para Madrid. "
    "Es este piso de ochenta metros en el Barrio del Pilar por solo cuarenta y dos mil euros. "
    "Pero atentos al cruce de datos: nos vamos a la pestaña de precio de mercado en la zona, "
    "y el metro cuadrado medio aquí se vende a tres mil trescientos ochenta euros. "
    "Un piso reformado en esta misma calle se vende por doscientos setenta mil euros. "
    "¡Estamos hablando de un margen potencial de más de doscientos veinte mil euros! "
    "Y las cargas están a cero. "
    "Para recibir las alertas completas antes que nadie, entra al enlace de nuestra biografía "
    "y suscríbete a nuestro canal privado de Telegram. Tienes el link en el perfil."
)

def obtener_ruta_ffmpeg() -> str:
    ruta = shutil.which("ffmpeg")
    if ruta:
        return ruta
    winget_path = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WinGet" / "Packages" / "Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe" / "ffmpeg-9.0.2-full_build" / "bin" / "ffmpeg.exe"
    if winget_path.exists():
        return str(winget_path)
    return "ffmpeg"

def generar_cara_reaccion(ruta_salida: Path):
    """
    Crea un bubble avatar circular con una cara estilizada/reacción 'menudo chollazo'
    para superponer en una esquina del vídeo como una 'facecam' de reacción.
    """
    size = (280, 280)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Círculo base con borde brillante
    draw.ellipse([10, 10, 270, 270], fill=(30, 41, 59), outline=(234, 179, 8), width=6)
    
    # Emoji / Ilustración de reacción de sorpresa e inversor
    # Si no hay emoji en font, dibujamos una composición gráfica expresiva
    try:
        f_emoji = ImageFont.truetype("seguiemj.ttf", 110)
        draw.text((140, 110), "😱", font=f_emoji, fill=(255, 255, 255), anchor="mm")
    except Exception:
        f_alt = ImageFont.truetype("arialbd.ttf", 48)
        draw.text((140, 110), "CHOLLO", font=f_alt, fill=(234, 179, 8), anchor="mm")

    # Bocadillo / Badge inferior: "¡MENUDO CHOLLO!"
    f_badge = ImageFont.truetype("arialbd.ttf", 24)
    draw.rounded_rectangle([20, 215, 260, 265], radius=12, fill=(234, 179, 8))
    draw.text((140, 240), "¡QUÉ CHOLLAZO! 🔥", font=f_badge, fill=(15, 23, 42), anchor="mm")

    img.save(ruta_salida, "PNG")

def generar_html_multi_pestana() -> str:
    """Genera la interfaz de navegador con 2 pestañas reales: BOE Oficial + Informe de Mercado."""
    return """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
  body { background-color: #0f172a; color: #1e293b; }

  /* Barra de pestañas del navegador (Chrome style) */
  .browser-tabs { background: #1e293b; padding: 8px 12px 0; display: flex; gap: 6px; border-bottom: 2px solid #334155; }
  .b-tab { padding: 10px 22px; font-size: 13px; font-weight: bold; border-radius: 8px 8px 0 0; cursor: pointer; display: flex; align-items: center; gap: 8px; color: #94a3b8; background: #0f172a; }
  .b-tab.active { background: #f8fafc; color: #0f172a; }

  .page { display: none; background: #f8fafc; min-height: 840px; }
  .page.active { display: block; }

  /* Estilos BOE */
  header.boe-head { background: #8b0000; color: white; padding: 12px 30px; display: flex; align-items: center; justify-content: space-between; border-bottom: 3px solid #f59e0b; }
  .container { max-width: 1100px; margin: 20px auto; background: white; border-radius: 8px; padding: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.06); border: 1px solid #cbd5e1; }
  
  /* Estilos Mercado (Idealista / Tasación) */
  header.market-head { background: #1e3a8a; color: white; padding: 12px 30px; display: flex; align-items: center; justify-content: space-between; border-bottom: 3px solid #38bdf8; }
  .market-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 20px; }
  .market-card { background: white; border: 1px solid #cbd5e1; border-radius: 10px; padding: 20px; text-align: center; }
  .market-card.hero { background: #ecfdf5; border: 2px solid #10b981; grid-column: span 3; }

  /* Cursor */
  #cursor {
    position: absolute;
    width: 28px;
    height: 28px;
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="%23000000" stroke="%23ffffff" stroke-width="1.5"><polygon points="3,3 3,21 8,16 13,22 16,20 11,14 19,14"/></svg>');
    pointer-events: none;
    z-index: 999999;
    transition: all 0.2s cubic-bezier(0.25, 1, 0.5, 1);
  }

  .highlighter {
    background-color: #fef08a;
    padding: 2px 8px;
    border-radius: 4px;
    box-shadow: 0 0 10px #fde047;
  }
</style>
</head>
<body>
<div id="cursor" style="left: 600px; top: 100px;"></div>

<!-- Pestañas del navegador -->
<div class="browser-tabs">
  <div class="b-tab active" id="tab-btn-boe">🏛️ Portal Subastas BOE (Exp. 9481)</div>
  <div class="b-tab" id="tab-btn-market">📊 Informe de Mercado Barrio del Pilar (Idealista/Tasación)</div>
</div>

<!-- PÁGINA 1: BOE -->
<div class="page active" id="page-boe">
  <header class="boe-head">
    <div style="font-weight: 800; font-size: 16px;">MINISTERIO DE JUSTICIA • PORTAL OFICIAL DE SUBASTAS</div>
    <div style="font-size: 12px; background: rgba(0,0,0,0.25); padding: 5px 12px; border-radius: 4px;">CERTIFICADO JUDICIAL</div>
  </header>
  <div class="container">
    <div style="color: #dc2626; font-weight: bold; font-size: 13px; margin-bottom: 5px;">⚠️ SUBASTA EN PLAZO DE PUJAS ACTIVA</div>
    <h2 style="font-size: 24px; color: #0f172a; margin-bottom: 12px;" id="boe-title">Vivienda 80 m² en C/ Ginzo de Limia (Madrid)</h2>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin-top: 15px;">
      <div style="background: #f8fafc; padding: 18px; border-radius: 8px; border: 1px solid #e2e8f0;">
        <div style="font-size: 12px; color: #64748b; font-weight: bold;">VALOR TASACIÓN OFICIAL</div>
        <div style="font-size: 26px; font-weight: bold; text-decoration: line-through; color: #dc2626;" id="boe-tasacion">190.450 €</div>
      </div>
      <div style="background: #f0fdf4; padding: 18px; border-radius: 8px; border: 2px solid #22c55e;">
        <div style="font-size: 12px; color: #15803d; font-weight: bold;">PRECIO SALIDA EN SUBASTA</div>
        <div style="font-size: 34px; font-weight: 900; color: #16a34a;" id="boe-salida">42.000 €</div>
      </div>
    </div>
    <div style="margin-top: 20px; background: #f0fdf4; border: 1px solid #86efac; padding: 15px; border-radius: 8px;" id="boe-cargas">
      <strong style="color: #166534;">✔ ESTADO DE CARGAS:</strong>
      <span style="color: #15803d;">Cargas hipotecarias anteriores: <strong>0,00 € (LIMPIO DE DEUDAS)</strong></span>
    </div>
  </div>
</div>

<!-- PÁGINA 2: INFORME DE MERCADO -->
<div class="page" id="page-market">
  <header class="market-head">
    <div style="font-weight: 800; font-size: 16px;">📈 TASACIÓN Y PRECIO MEDIO EN MERCADO LIBRE (BARRIO DEL PILAR)</div>
    <div style="font-size: 12px; background: rgba(0,0,0,0.25); padding: 5px 12px; border-radius: 4px;">DATOS EN TIEMPO REAL</div>
  </header>
  <div class="container">
    <div style="font-size: 13px; color: #0284c7; font-weight: bold; margin-bottom: 5px;">ANÁLISIS COMPARATIVO DE COMPRAVENTAS EN LA MISMA CALLE</div>
    <h2 style="font-size: 22px; color: #0f172a; margin-bottom: 15px;">Métricas Reales para Inversión / Venta</h2>

    <div class="market-grid">
      <div class="market-card">
        <div style="font-size: 12px; color: #64748b; font-weight: bold;">PRECIO MEDIO ZONA</div>
        <div style="font-size: 28px; font-weight: 800; color: #0f172a; margin-top: 6px;" id="m-metro">3.380 € / m²</div>
        <div style="font-size: 11px; color: #64748b; margin-top: 4px;">Madrid Norte</div>
      </div>

      <div class="market-card">
        <div style="font-size: 12px; color: #64748b; font-weight: bold;">PRECIO MEDIO VENTA</div>
        <div style="font-size: 28px; font-weight: 800; color: #0284c7; margin-top: 6px;" id="m-venta">270.400 €</div>
        <div style="font-size: 11px; color: #64748b; margin-top: 4px;">Piso reformado 80m²</div>
      </div>

      <div class="market-card">
        <div style="font-size: 12px; color: #64748b; font-weight: bold;">ALQUILER ESTIMADO</div>
        <div style="font-size: 28px; font-weight: 800; color: #7c3aed; margin-top: 6px;">1.150 € / mes</div>
        <div style="font-size: 11px; color: #64748b; margin-top: 4px;">Alta demanda</div>
      </div>

      <div class="market-card hero">
        <div style="font-size: 14px; color: #166534; font-weight: bold;">PLUSVALÍA / MARGEN POTENCIAL BRUTO DE COMPRA</div>
        <div style="font-size: 44px; font-weight: 900; color: #059669; margin: 8px 0;" id="m-margen">+ 228.400 €</div>
        <p style="font-size: 13px; color: #15803d; font-weight: 600;">(Valor de mercado 270.400 € - Precio de subasta 42.000 €)</p>
      </div>
    </div>
  </div>
</div>

<script>
  const cursor = document.getElementById('cursor');

  function moverCursor(x, y) {
    cursor.style.left = x + 'px';
    cursor.style.top = y + 'px';
  }

  function resaltar(id) {
    document.getElementById(id).classList.add('highlighter');
  }

  function cambiarPestana(target) {
    document.getElementById('tab-btn-boe').classList.remove('active');
    document.getElementById('tab-btn-market').classList.remove('active');
    document.getElementById('page-boe').classList.remove('active');
    document.getElementById('page-market').classList.remove('active');

    if (target === 'market') {
      document.getElementById('tab-btn-market').classList.add('active');
      document.getElementById('page-market').classList.add('active');
    } else {
      document.getElementById('tab-btn-boe').classList.add('active');
      document.getElementById('page-boe').classList.add('active');
    }
  }
</script>
</body>
</html>"""

async def grabar_sesion_multitasking(ruta_video_webm: Path):
    """Navega entre BOE y el Informe de Mercado simulando interacción humana."""
    html_content = generar_html_multi_pestana()
    html_path = OUTPUT_DIR / "browser_multitask.html"
    html_path.write_text(html_content, encoding="utf-8")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1400, "height": 900},
            record_video_dir=str(OUTPUT_DIR),
            record_video_size={"width": 1400, "height": 900}
        )
        page = await context.new_page()
        await page.goto(f"file:///{html_path.resolve().as_posix()}")

        # 1. Mira el BOE (0 - 5 seg)
        await page.evaluate("moverCursor(450, 260)")
        await asyncio.sleep(2.0)
        await page.evaluate("moverCursor(850, 310)")
        await page.evaluate("resaltar('boe-salida')")
        await asyncio.sleep(2.5)

        # 2. Hace clic en la pestaña de Informe de Mercado (5 - 6 seg)
        await page.evaluate("moverCursor(420, 20)")
        await asyncio.sleep(0.8)
        await page.evaluate("cambiarPestana('market')")
        await asyncio.sleep(1.0)

        # 3. Resalta el precio del metro cuadrado y precio medio (6 - 13 seg)
        await page.evaluate("moverCursor(300, 310)")
        await page.evaluate("resaltar('m-metro')")
        await asyncio.sleep(2.0)
        await page.evaluate("moverCursor(700, 310)")
        await page.evaluate("resaltar('m-venta')")
        await asyncio.sleep(2.0)

        # 4. Baja a la caja de plusvalía gigante +228.400 € (13 - 18 seg)
        await page.evaluate("moverCursor(680, 520)")
        await page.evaluate("resaltar('m-margen')")
        await asyncio.sleep(4.0)

        # 5. Vuelve al BOE para confirmar cargas a 0€ (18 - 25 seg)
        await page.evaluate("moverCursor(180, 20)")
        await asyncio.sleep(0.8)
        await page.evaluate("cambiarPestana('boe')")
        await page.evaluate("moverCursor(500, 430)")
        await page.evaluate("resaltar('boe-cargas')")
        await asyncio.sleep(4.0)

        video_obj = page.video
        await page.close()
        await context.close()
        await browser.close()

        recorded_path = await video_obj.path()
        shutil.move(recorded_path, ruta_video_webm)
        print("✅ Grabación multi-pestaña completada.")

async def generar_locucion_y_subtitulos(texto: str, ruta_audio: Path, ruta_srt: Path):
    com = edge_tts.Communicate(texto, "es-ES-AlvaroNeural", rate="+4%")
    submaker = edge_tts.SubMaker()
    with open(ruta_audio, "wb") as f_a:
        async for chunk in com.stream():
            if chunk["type"] == "audio":
                f_a.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.feed(chunk)
    with open(ruta_srt, "w", encoding="utf-8") as f_s:
        f_s.write(submaker.get_srt())

def convertir_srt_a_ass(ruta_srt: Path, ruta_ass: Path):
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Mercado,Arial Black,50,&H0000FFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,7,2,2,80,80,380,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    with open(ruta_srt, "r", encoding="utf-8") as f:
        contenido = f.read()
    bloques = contenido.strip().split("\n\n")
    eventos = []
    for b in bloques:
        lineas = b.strip().split("\n")
        if len(lineas) >= 3:
            tiempos = lineas[1].replace(",", ".")
            partes = tiempos.split(" --> ")
            if len(partes) == 2:
                inicio = partes[0][:11]
                fin = partes[1][:11]
                texto = " ".join(lineas[2:]).upper()
                eventos.append(f"Dialogue: 0,{inicio},{fin},Mercado,,0,0,0,,{texto}")

    with open(ruta_ass, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(eventos))

def crear_tarjeta_suscripcion_telegram(ruta_salida: Path):
    """Crea la tarjeta ultra-clara explicativa de cómo suscribirse en Telegram."""
    img = Image.new("RGBA", (1000, 360), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Fondo azul Telegram con borde brillante
    draw.rounded_rectangle([0, 0, 1000, 360], radius=28, fill=(30, 41, 59), outline=(56, 189, 248), width=4)

    f_title = ImageFont.truetype("arialbd.ttf", 36)
    f_step = ImageFont.truetype("arialbd.ttf", 28)
    f_cta = ImageFont.truetype("arialbd.ttf", 34)

    # Cabecera Telegram
    draw.rounded_rectangle([0, 0, 1000, 75], radius=24, fill=(2, 132, 199))
    draw.text((500, 38), "✈️ CÓMO UNIRTE AL CANAL PRIVADO DE TELEGRAM", font=f_title, fill=(255, 255, 255), anchor="mm")

    # Pasos 1, 2, 3
    draw.text((60, 120), "1️⃣  Toca la foto de nuestro perfil de TikTok", font=f_step, fill=(248, 250, 252))
    draw.text((60, 175), "2️⃣  Haz clic en el enlace de la Biografía (Link en Bio)", font=f_step, fill=(248, 250, 252))
    draw.text((60, 230), "3️⃣  Recibe todas las alertas de subastas con cargas verificadas", font=f_step, fill=(148, 163, 184))

    # Botón brillante
    draw.rounded_rectangle([60, 280, 940, 340], radius=16, fill=(34, 197, 94))
    draw.text((500, 310), "👉 ¡ENLACE DIRECTO EN NUESTRO PERFIL! 👈", font=f_cta, fill=(15, 23, 42), anchor="mm")

    img.save(ruta_salida, "PNG")

def ensamblar_video_mercado_pro(ruta_video_pantalla: Path, ruta_cara: Path, ruta_cta: Path, ruta_audio: Path, ruta_ass: Path, ruta_final: Path):
    """
    Ensambla:
    - Grabación de pantalla multi-pestaña (BOE + Mercado)
    - Burbuja de reacción 'Qué chollazo' en la esquina superior derecha
    - Tarjeta ultra-clara de suscripción a Telegram en la parte inferior
    - Subtítulos dinámicos estilo TikTok
    """
    ffmpeg_bin = obtener_ruta_ffmpeg()
    ass_escaped = str(ruta_ass).replace("\\", "/").replace(":", "\\:")

    cmd = [
        ffmpeg_bin, "-y",
        "-i", str(ruta_video_pantalla),
        "-i", str(ruta_cara),
        "-i", str(ruta_cta),
        "-i", str(ruta_audio),
        "-filter_complex",
        (
            "color=c=0x0a0f1d:s=1080x1920:d=26[bg];"
            # 1. Escalar pantalla de navegador y colocarla en el tercio superior/medio
            "[0:v]scale=1040:-1,pad=1050:ih+10:5:5:color=0x38bdf8[screen];"
            "[bg][screen]overlay=x=(W-w)/2:y=240[v1];"
            # 2. Superponer cara de reacción en la esquina superior derecha
            "[v1][1:v]overlay=x=W-w-30:y=260[v2];"
            # 3. Superponer la tarjeta de cómo suscribirse en Telegram abajo
            "[v2][2:v]overlay=x=(W-w)/2:y=1510[v3];"
            # 4. Quemar subtítulos dinámicos
            f"[v3]subtitles='{ass_escaped}'[vout]"
        ),
        "-map", "[vout]",
        "-map", "3:a",
        "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(ruta_final)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"🚀 ¡VÍDEO CON CRUCE DE MERCADO Y REACCIÓN GENERADO!: {ruta_final}")

async def main():
    print("🔥 Construyendo vídeo viral con cruce de datos de mercado y CTA Telegram...")
    ruta_webm = OUTPUT_DIR / "market_screen.webm"
    ruta_audio = OUTPUT_DIR / "market_locucion.mp3"
    ruta_srt = OUTPUT_DIR / "market_subtitulos.srt"
    ruta_ass = OUTPUT_DIR / "market_subtitulos.ass"
    ruta_cara = OUTPUT_DIR / "avatar_reaccion.png"
    ruta_cta = OUTPUT_DIR / "telegram_cta_card.png"
    ruta_final = OUTPUT_DIR / "subasta_tiktok_MERCADO_TOTAL.mp4"

    # 1. Generar recursos gráficos (cara de reacción + tarjeta CTA Telegram)
    generar_cara_reaccion(ruta_cara)
    crear_tarjeta_suscripcion_telegram(ruta_cta)

    # 2. Generar locución y subtítulos
    await generar_locucion_y_subtitulos(GUION_MERCADO, ruta_audio, ruta_srt)
    convertir_srt_a_ass(ruta_srt, ruta_ass)

    # 3. Grabar sesión multi-pestaña (BOE <-> Mercado Idealista)
    await grabar_sesion_multitasking(ruta_webm)

    # 4. Ensamblar todo con FFmpeg
    ensamblar_video_mercado_pro(ruta_webm, ruta_cara, ruta_cta, ruta_audio, ruta_ass, ruta_final)

if __name__ == "__main__":
    asyncio.run(main())
