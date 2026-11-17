import asyncio
import os
import shutil
import subprocess
from pathlib import Path
import edge_tts
from playwright.async_api import async_playwright

BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Guion 100% natural, como si un amigo te enseña su pantalla
GUION_POV = (
    "Fijaos bien en lo que acaba de publicar el BOE hace un rato para Madrid. "
    "Es este piso de ochenta metros en el Barrio del Pilar. "
    "Mirad aquí: la tasación oficial es de ciento noventa mil euros, "
    "y el precio de salida en subasta es de tan solo cuarenta y dos mil. "
    "Pero lo más importante de todo, nos vamos a la pestaña de cargas... "
    "y como veis aquí abajo está completamente limpio, cero euros de hipoteca previa. "
    "Os he dejado el enlace oficial y el expediente exacto en nuestro canal de Telegram. "
    "Tenéis el link en la bio."
)

def obtener_ruta_ffmpeg() -> str:
    ruta = shutil.which("ffmpeg")
    if ruta:
        return ruta
    winget_path = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WinGet" / "Packages" / "Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe" / "ffmpeg-9.0.2-full_build" / "bin" / "ffmpeg.exe"
    if winget_path.exists():
        return str(winget_path)
    return "ffmpeg"

def generar_html_dossier_boe() -> str:
    """Crea una réplica exacta y fotorrealista del Portal de Subastas del BOE para grabar en el navegador."""
    return """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
  body { background-color: #f1f5f9; color: #1e293b; }
  
  /* Cabecera oficial BOE */
  header { background: #8b0000; color: white; padding: 12px 40px; display: flex; align-items: center; justify-content: space-between; border-bottom: 4px solid #f59e0b; }
  .logo-title { display: flex; align-items: center; gap: 15px; }
  .escudo { background: #f59e0b; color: #8b0000; font-weight: 900; font-size: 20px; padding: 8px 14px; border-radius: 6px; }
  .boe-header h1 { font-size: 19px; font-weight: 700; letter-spacing: 0.5px; }
  .boe-header p { font-size: 12px; color: #fde68a; }

  /* Contenedor del Expediente */
  .container { max-width: 1100px; margin: 25px auto; background: white; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); overflow: hidden; border: 1px solid #cbd5e1; }
  .alert-bar { background: #fee2e2; border-left: 5px solid #dc2626; color: #991b1b; padding: 12px 20px; font-size: 14px; font-weight: 600; display: flex; justify-content: space-between; }
  
  .expediente-header { padding: 25px 30px 15px; border-bottom: 1px solid #e2e8f0; }
  .exp-num { font-size: 13px; color: #64748b; font-weight: bold; text-transform: uppercase; }
  .exp-title { font-size: 26px; font-weight: 800; color: #0f172a; margin: 6px 0 10px; }
  .badge-ubicacion { display: inline-block; background: #e0f2fe; color: #0369a1; padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: 600; }

  /* Pestañas */
  .tabs { display: flex; background: #f8fafc; border-bottom: 2px solid #e2e8f0; padding: 0 25px; }
  .tab { padding: 14px 20px; font-size: 14px; font-weight: 600; color: #64748b; cursor: pointer; border-bottom: 3px solid transparent; }
  .tab.active { color: #8b0000; border-bottom-color: #8b0000; background: white; }

  /* Contenido */
  .tab-content { padding: 30px; }
  .data-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
  .data-box { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 18px 20px; }
  .data-box.highlight { background: #ecfdf5; border-color: #10b981; }
  .data-label { font-size: 12px; color: #64748b; font-weight: 700; text-transform: uppercase; margin-bottom: 6px; }
  .data-val { font-size: 26px; font-weight: 800; color: #0f172a; }
  .data-val.strikethrough { text-decoration: line-through; color: #dc2626; font-size: 22px; }
  .data-val.green { color: #059669; font-size: 34px; }
  
  .cargas-box { display: none; background: #f0fdf4; border: 2px solid #16a34a; border-radius: 8px; padding: 20px; margin-top: 20px; }
  .cargas-title { color: #166534; font-weight: 800; font-size: 18px; margin-bottom: 8px; }
  .cargas-detail { color: #15803d; font-size: 14px; line-height: 1.5; }

  /* Cursor virtual realista */
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
    background-color: rgba(253, 224, 71, 0.85);
    padding: 2px 8px;
    border-radius: 4px;
    box-shadow: 0 0 8px rgba(253, 224, 71, 0.6);
  }
</style>
</head>
<body>
<div id="cursor" style="left: 600px; top: 100px;"></div>

<header>
  <div class="logo-title">
    <div class="escudo">BOE</div>
    <div class="boe-header">
      <h1>AGENCIA ESTATAL BOLETÍN OFICIAL DEL ESTADO</h1>
      <p>Portal Oficial de Subastas Judiciales y Notariales</p>
    </div>
  </div>
  <div style="font-size: 12px; font-weight: bold; background: rgba(0,0,0,0.2); padding: 6px 14px; border-radius: 4px;">
    CERTIFICADO ELECTRÓNICO ACTIVO
  </div>
</header>

<div class="container">
  <div class="alert-bar">
    <span>⚠️ ESTADO: CONVOCATORIA DE SUBASTA EN PLAZO DE PUJAS</span>
    <span>PUBLICADO HACE 4 HORAS</span>
  </div>

  <div class="expediente-header">
    <div class="exp-num">EXPEDIENTE SUB-JA-2026-9481 • JUZGADO 1ª INSTANCIA DE MADRID</div>
    <div class="exp-title" id="titulo-expediente">Vivienda 80 m² en C/ Ginzo de Limia (Barrio del Pilar, Madrid)</div>
    <span class="badge-ubicacion">📍 Madrid Capital</span>
    <span class="badge-ubicacion" style="background: #fef3c7; color: #b45309;">Vivienda Libre de Arrendatarios</span>
  </div>

  <div class="tabs">
    <div class="tab active" id="tab-general">Información General</div>
    <div class="tab" id="tab-cargas">Cargas y Deudas Registrales</div>
    <div class="tab">Titulaciones y Documentación</div>
  </div>

  <div class="tab-content">
    <div class="data-grid" id="grid-precios">
      <div class="data-box" id="box-tasacion">
        <div class="data-label">Valor de Tasación Oficial (Juzgado)</div>
        <div class="data-val strikethrough" id="val-tasacion">190.450,00 €</div>
        <p style="font-size: 11px; color: #94a3b8; margin-top: 5px;">Precio medio tasado en escritura pública</p>
      </div>

      <div class="data-box highlight" id="box-salida">
        <div class="data-label" style="color: #047857;">Precio de Salida en Subasta</div>
        <div class="data-val green" id="val-salida">42.000,00 €</div>
        <p style="font-size: 11px; color: #059669; margin-top: 5px; font-weight: bold;">Sin puja mínima fijada • Ahorro del 78%</p>
      </div>

      <div class="data-box">
        <div class="data-label">Depósito para participar (5%)</div>
        <div class="data-val" style="font-size: 18px;">2.100,00 € (Retenido en cuenta judicial)</div>
      </div>

      <div class="data-box">
        <div class="data-label">Cierre del plazo de pujas</div>
        <div class="data-val" style="font-size: 18px; color: #dc2626;">En 6 días (18:00 horas)</div>
      </div>
    </div>

    <div class="cargas-box" id="panel-cargas">
      <div class="cargas-title">✔ CERTIFICADO REGISTRAL DE DOMINIO Y CARGAS</div>
      <div class="cargas-detail">
        <strong>Resultado de la consulta judicial:</strong><br>
        • Cargas hipotecarias anteriores o preferentes: <strong>0,00 € (CANCELADAS / SIN CARGAS)</strong>.<br>
        • Situación posesoria: Finca desocupada según mandamiento judicial.<br>
        • El adquirente NO asume deudas de la hipoteca ejecutada.
      </div>
    </div>
  </div>
</div>

<script>
  // Funciones para animar el cursor y resaltar elementos como un usuario humano
  const cursor = document.getElementById('cursor');

  function moverCursor(x, y) {
    cursor.style.left = x + 'px';
    cursor.style.top = y + 'px';
  }

  function resaltarElemento(id) {
    const el = document.getElementById(id);
    el.classList.add('highlighter');
  }

  function abrirPestanaCargas() {
    document.getElementById('tab-general').classList.remove('active');
    document.getElementById('tab-cargas').classList.add('active');
    document.getElementById('panel-cargas').style.display = 'block';
  }
</script>
</body>
</html>"""

async def grabar_sesion_navegador(ruta_video_webm: Path, duracion_seg: float):
    """Abre Chromium con Playwright, carga el BOE simulado, mueve el ratón y graba el vídeo."""
    html_content = generar_html_dossier_boe()
    html_path = OUTPUT_DIR / "boe_page.html"
    html_path.write_text(html_content, encoding="utf-8")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Grabamos a resolución nítida 1920x1080
        context = await browser.new_context(
            viewport={"width": 1400, "height": 900},
            record_video_dir=str(OUTPUT_DIR),
            record_video_size={"width": 1400, "height": 900}
        )
        page = await context.new_page()
        await page.goto(f"file:///{html_path.resolve().as_posix()}")
        
        # Secuencia humana de navegación sincronizada con el guion:
        # 1. Inicia mirando el título del expediente (0 - 3s)
        await page.evaluate("moverCursor(380, 240)")
        await asyncio.sleep(2.5)
        
        # 2. Mueve el cursor a la tasación de 190.000 € y la resalta (3 - 7s)
        await page.evaluate("moverCursor(450, 480)")
        await asyncio.sleep(1.0)
        await page.evaluate("resaltarElemento('val-tasacion')")
        await asyncio.sleep(2.0)
        
        # 3. Mueve el cursor a la salida de 42.000 € y la resalta (7 - 11s)
        await page.evaluate("moverCursor(850, 480)")
        await asyncio.sleep(1.0)
        await page.evaluate("resaltarElemento('val-salida')")
        await asyncio.sleep(2.5)

        # 4. Hace clic en la pestaña de 'Cargas y Deudas' para mostrar 0€ limpio (11 - 17s)
        await page.evaluate("moverCursor(480, 360)")
        await asyncio.sleep(0.8)
        await page.evaluate("abrirPestanaCargas()")
        await page.evaluate("moverCursor(500, 720)")
        await asyncio.sleep(4.0)

        # 5. Cierre
        await asyncio.sleep(2.0)

        # Cerrar página para finalizar la grabación
        video_obj = page.video
        await page.close()
        await context.close()
        await browser.close()

        # Obtener ruta del archivo de vídeo grabado por Playwright
        recorded_path = await video_obj.path()
        shutil.move(recorded_path, ruta_video_webm)
        print(f"✅ Grabación de pantalla del navegador completada: {ruta_video_webm}")

async def generar_locucion_y_subtitulos(texto: str, ruta_audio: Path, ruta_srt: Path):
    """Genera locución cercana y extrae los subtítulos."""
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
    print("✅ Locución natural y marcas de tiempo listas.")

def convertir_srt_a_ass_pov(ruta_srt: Path, ruta_ass: Path):
    """Subtítulos estilo TikTok colocados en el tercio inferior para formato vertical."""
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: POV,Arial Black,52,&H0000FFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,7,2,2,80,80,260,1

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
                eventos.append(f"Dialogue: 0,{inicio},{fin},POV,,0,0,0,,{texto}")

    with open(ruta_ass, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(eventos))

def ensamblar_video_pov(ruta_video_pantalla: Path, ruta_audio: Path, ruta_ass: Path, ruta_final: Path):
    """
    Ensambla el vídeo vertical (1080x1920) mostrando la pantalla del ordenador grabada en el centro/arriba,
    con marco realista de portátil/mesa, subtítulos estilo TikTok y llamada a la acción inferior.
    """
    ffmpeg_bin = obtener_ruta_ffmpeg()
    ass_escaped = str(ruta_ass).replace("\\", "/").replace(":", "\\:")

    # Filtro complejo de FFmpeg:
    # 1. Crea un lienzo vertical 1080x1920 con fondo oscuro degradado (aspecto moderno/setup de trabajo).
    # 2. Escala la captura del navegador (1400x900) para encajarla de forma prominente en el vídeo (1040x668).
    # 3. Le añade un marco con sombra alrededor de la pantalla grabada.
    # 4. Quema los subtítulos dinámicos en la parte inferior.
    cmd = [
        ffmpeg_bin, "-y",
        "-i", str(ruta_video_pantalla),
        "-i", str(ruta_audio),
        "-filter_complex",
        (
            "color=c=0x0b0f19:s=1080x1920:d=22[bg];"
            "[0:v]scale=1040:-1,pad=1050:ih+10:5:5:color=0x334155[screen];"
            "[bg][screen]overlay=x=(W-w)/2:y=240[vbase];"
            f"[vbase]subtitles='{ass_escaped}'[vout]"
        ),
        "-map", "[vout]",
        "-map", "1:a",
        "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(ruta_final)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"🔥 ¡VÍDEO POV CON NAVEGADOR REAL GENERADO!: {ruta_final}")

async def main():
    print("🚀 Iniciando generador formato POV (Grabación real de navegador)...")
    ruta_webm = OUTPUT_DIR / "browser_record.webm"
    ruta_audio = OUTPUT_DIR / "pov_locucion.mp3"
    ruta_srt = OUTPUT_DIR / "pov_subtitulos.srt"
    ruta_ass = OUTPUT_DIR / "pov_subtitulos.ass"
    ruta_final = OUTPUT_DIR / "subasta_tiktok_POV.mp4"

    # Paso 1: Generar voz y subtítulos
    await generar_locucion_y_subtitulos(GUION_POV, ruta_audio, ruta_srt)
    convertir_srt_a_ass_pov(ruta_srt, ruta_ass)

    # Paso 2: Grabar sesión de navegador simulando navegación humana
    await grabar_sesion_navegador(ruta_webm, 20.0)

    # Paso 3: Ensamblar vídeo vertical con pantalla grabada + subtítulos dinámicos
    ensamblar_video_pov(ruta_webm, ruta_audio, ruta_ass, ruta_final)

if __name__ == "__main__":
    asyncio.run(main())
