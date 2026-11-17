import asyncio
import os
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import edge_tts

BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = BASE_DIR / "output"
TEMPLATES_DIR = BASE_DIR / "assets" / "templates"
OUTPUT_DIR.mkdir(exist_ok=True)

GUION_VISUAL = (
    "Mira lo que acaba de salir en Madrid. "
    "Nos vamos directos al Barrio del Pilar. "
    "Este piso de ochenta metros sale a subasta judicial por solo cuarenta y dos mil euros. "
    "Pero atentos a las fotos del inmueble y al cruce de datos: "
    "en esta misma calle los pisos reformados se venden por doscientos setenta mil euros. "
    "Estamos hablando de más de doscientos veinte mil euros de margen bruto, "
    "y el expediente está completamente libre de cargas. "
    "Para ver el expediente oficial y recibir las mejores oportunidades de España, "
    "entra al enlace de nuestra biografía y únete a nuestro canal privado de Telegram. "
    "Tienes el link en el perfil."
)

def obtener_ruta_ffmpeg() -> str:
    ruta = shutil.which("ffmpeg")
    if ruta:
        return ruta
    winget_path = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WinGet" / "Packages" / "Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe" / "ffmpeg-9.0.2-full_build" / "bin" / "ffmpeg.exe"
    if winget_path.exists():
        return str(winget_path)
    return "ffmpeg"

def texto_centrado_auto(draw: ImageDraw.ImageDraw, texto: str, rect: list, font_file: str, max_size: int, color: tuple, padding_x: int = 30):
    """
    Ajusta automáticamente el tamaño de fuente para que el texto NUNCA se salga del cuadro
    y quede perfectamente centrado vertical y horizontalmente.
    """
    x1, y1, x2, y2 = rect
    max_w = (x2 - x1) - (padding_x * 2)
    max_h = (y2 - y1) - 10

    size = max_size
    font = ImageFont.truetype(font_file, size)
    bbox = font.getbbox(texto)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    # Reducir tamaño hasta que quepa perfectamente
    while (w > max_w or h > max_h) and size > 16:
        size -= 2
        font = ImageFont.truetype(font_file, size)
        bbox = font.getbbox(texto)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]

    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    draw.text((cx, cy), texto, font=font, fill=color, anchor="mm")

def preparar_escena_1_satelite(ruta_salida: Path):
    """Escena 1 (Google Earth Dive): Satélite con pin perfecto y encajado."""
    ancho, alto = 1080, 1920
    sat_img = Image.open(TEMPLATES_DIR / "satelite_tierra.jpg").convert("RGB")
    sat_img = sat_img.resize((ancho, alto), Image.Resampling.LANCZOS)
    
    overlay = Image.new("RGBA", (ancho, alto), (0, 0, 0, 90))
    sat_img.paste(overlay, (0, 0), overlay)
    draw = ImageDraw.Draw(sat_img)

    # 1. Badge superior
    badge_rect = [120, 200, 960, 290]
    draw.rounded_rectangle(badge_rect, radius=20, fill=(220, 38, 38))
    texto_centrado_auto(draw, "🚨 NUEVA SUBASTA JUDICIAL", badge_rect, "arialbd.ttf", 38, (255, 255, 255))

    # 2. Pin central grande
    pin_rect = [100, 720, 980, 930]
    draw.rounded_rectangle(pin_rect, radius=28, fill=(15, 23, 42), outline=(239, 68, 68), width=5)
    
    # Textos dentro del pin con espacio propio
    r_tit = [120, 740, 960, 830]
    r_sub = [120, 830, 960, 900]
    texto_centrado_auto(draw, "📍 MADRID • BARRIO DEL PILAR", r_tit, "arialbd.ttf", 52, (255, 255, 255))
    texto_centrado_auto(draw, "Aterrizando en la oportunidad del día...", r_sub, "arial.ttf", 36, (248, 113, 113))

    sat_img.save(ruta_salida, quality=95)

def preparar_escena_2_fachada(ruta_salida: Path):
    """Escena 2 (Fachada): Tarjeta limpia sin desbordes."""
    ancho, alto = 1080, 1920
    fac_img = Image.open(TEMPLATES_DIR / "fachada_edificio.jpg").convert("RGB")
    fac_img = fac_img.resize((ancho, alto), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(fac_img)

    # Tarjeta flotante en el tercio medio/inferior
    card_rect = [70, 1050, 1010, 1530]
    draw.rounded_rectangle(card_rect, radius=32, fill=(15, 23, 42), outline=(34, 197, 94), width=4)

    r_h1 = [90, 1080, 990, 1160]
    r_lbl = [90, 1170, 990, 1240]
    r_precio = [90, 1250, 990, 1390]
    r_desc = [300, 1420, 780, 1490]

    texto_centrado_auto(draw, "PISO 80 m² • 3 HABITACIONES", r_h1, "arialbd.ttf", 48, (255, 255, 255))
    texto_centrado_auto(draw, "PRECIO DE SALIDA EN SUBASTA", r_lbl, "arialbd.ttf", 34, (148, 163, 184))
    texto_centrado_auto(draw, "42.000 €", r_precio, "arialbd.ttf", 100, (34, 197, 94))
    
    draw.rounded_rectangle(r_desc, radius=16, fill=(34, 197, 94))
    texto_centrado_auto(draw, "78% DE DESCUENTO", r_desc, "arialbd.ttf", 34, (15, 23, 42))

    fac_img.save(ruta_salida, quality=95)

def preparar_escena_3_interior(ruta_salida: Path):
    """Escena 3 (Interior reformado): Todos los datos encajados milimétricamente."""
    ancho, alto = 1080, 1920
    int_img = Image.open(TEMPLATES_DIR / "interior_piso.jpg").convert("RGB")
    int_img = int_img.resize((ancho, alto), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(int_img)

    card_rect = [60, 900, 1020, 1550]
    draw.rounded_rectangle(card_rect, radius=32, fill=(15, 23, 42), outline=(56, 189, 248), width=3)

    r_lbl1 = [80, 930, 1000, 980]
    r_val1 = [80, 985, 1000, 1055]
    texto_centrado_auto(draw, "VALOR MEDIO REFORMADO EN LA ZONA", r_lbl1, "arialbd.ttf", 32, (148, 163, 184))
    texto_centrado_auto(draw, "270.000 € (3.380 €/m²)", r_val1, "arialbd.ttf", 52, (56, 189, 248))

    # Separador
    draw.line([(120, 1080), (960, 1080)], fill=(51, 65, 85), width=2)

    r_lbl2 = [80, 1100, 1000, 1160]
    r_ganancia = [80, 1170, 1000, 1290]
    texto_centrado_auto(draw, "PLUSVALÍA / MARGEN BRUTO ESTIMADO", r_lbl2, "arialbd.ttf", 34, (187, 247, 208))
    texto_centrado_auto(draw, "+ 228.000 €", r_ganancia, "arialbd.ttf", 86, (34, 197, 94))

    # Badge de cargas
    r_cargas = [120, 1320, 960, 1400]
    draw.rounded_rectangle(r_cargas, radius=16, fill=(22, 101, 52))
    texto_centrado_auto(draw, "✔ CARGAS: 0,00 € (EXPEDIENTE LIMPIO)", r_cargas, "arialbd.ttf", 32, (255, 255, 255))

    # Alquiler
    r_alq = [80, 1430, 1000, 1480]
    r_barrio = [80, 1485, 1000, 1530]
    texto_centrado_auto(draw, "Alquiler estimado: 1.150 € / mes (Alta demanda)", r_alq, "arialbd.ttf", 30, (203, 213, 225))
    texto_centrado_auto(draw, "Zona Barrio del Pilar (Madrid)", r_barrio, "arial.ttf", 28, (148, 163, 184))

    int_img.save(ruta_salida, quality=95)

def preparar_escena_4_telegram(ruta_salida: Path):
    """Escena 4: Pantalla final de Telegram con los 3 pasos que encajan perfectamente sin salirse."""
    ancho, alto = 1080, 1920
    bg = Image.open(TEMPLATES_DIR / "barrio_pilar_aerea.jpg").convert("RGB")
    bg = bg.resize((ancho, alto), Image.Resampling.LANCZOS)
    bg = bg.filter(ImageFilter.GaussianBlur(15))
    draw = ImageDraw.Draw(bg)

    card_rect = [60, 320, 1020, 1560]
    draw.rounded_rectangle(card_rect, radius=36, fill=(15, 23, 42), outline=(56, 189, 248), width=5)

    # Cabecera Telegram
    header_rect = [60, 320, 1020, 480]
    draw.rounded_rectangle(header_rect, radius=32, fill=(2, 132, 199))
    r_th1 = [80, 340, 1000, 420]
    r_th2 = [80, 420, 1000, 470]
    texto_centrado_auto(draw, "✈️ TELEGRAM PRIVADO", r_th1, "arialbd.ttf", 58, (255, 255, 255))
    texto_centrado_auto(draw, "RadarAlertas • Canal Exclusivo", r_th2, "arial.ttf", 34, (224, 242, 254))

    # Subtítulo explicativo
    r_exp1 = [80, 520, 1000, 580]
    r_exp2 = [80, 585, 1000, 640]
    texto_centrado_auto(draw, "ACCEDE AL EXPEDIENTE COMPLETO", r_exp1, "arialbd.ttf", 36, (255, 255, 255))
    texto_centrado_auto(draw, "Enlace judicial directo, fotos y filtro de cargas", r_exp2, "arial.ttf", 30, (148, 163, 184))

    # Los 3 Pasos con tamaño de fuente auto-ajustado para que NUNCA se corten
    pasos = [
        ("1️⃣", "Toca nuestra foto de perfil de TikTok"),
        ("2️⃣", "Haz clic en el enlace de la Biografía (Link en Bio)"),
        ("3️⃣", "Accede al canal y recibe las alertas en tiempo real")
    ]
    y = 700
    for num, txt in pasos:
        box_rect = [100, y, 980, y + 120]
        draw.rounded_rectangle(box_rect, radius=18, fill=(30, 41, 59), outline=(71, 85, 105), width=2)
        
        # Icono número
        r_num = [110, y + 10, 200, y + 110]
        texto_centrado_auto(draw, num, r_num, "arialbd.ttf", 44, (255, 255, 255))
        
        # Texto del paso (perfectamente ajustado dentro del ancho restante)
        r_txt = [200, y + 10, 960, y + 110]
        texto_centrado_auto(draw, txt, r_txt, "arialbd.ttf", 30, (248, 250, 252), padding_x=10)
        y += 150

    # Botón brillante inferior
    btn_rect = [100, 1340, 980, 1480]
    draw.rounded_rectangle(btn_rect, radius=24, fill=(34, 197, 94))
    texto_centrado_auto(draw, "👉 ¡LINK EN EL PERFIL! 👈", btn_rect, "arialbd.ttf", 46, (15, 23, 42))

    bg.save(ruta_salida, quality=95)

async def generar_locucion_y_subtitulos(texto: str, ruta_audio: Path, ruta_srt: Path):
    com = edge_tts.Communicate(texto, "es-ES-AlvaroNeural", rate="+5%")
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
    """
    Subtítulos centrados en la zona segura media-baja (MarginV: 260)
    con tamaño 44 y fondo limpio para que no colisionen con las tarjetas.
    """
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: VisualPro,Arial Black,44,&H0000FFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,7,2,2,60,60,200,1

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
                eventos.append(f"Dialogue: 0,{inicio},{fin},VisualPro,,0,0,0,,{texto}")

    with open(ruta_ass, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(eventos))

def ensamblar_video_cinematico(escenas: list, duraciones: list, ruta_audio: Path, ruta_ass: Path, ruta_final: Path):
    ffmpeg_bin = obtener_ruta_ffmpeg()
    ass_escaped = str(ruta_ass).replace("\\", "/").replace(":", "\\:")

    clips = []
    for idx, (img_path, dur) in enumerate(zip(escenas, duraciones)):
        clip_path = OUTPUT_DIR / f"clip_fit_{idx+1}.mp4"
        cmd_clip = [
            ffmpeg_bin, "-y",
            "-loop", "1", "-i", str(img_path),
            "-t", str(dur),
            "-vf", f"scale=1080:1920,zoompan=z='min(zoom+0.0010,1.10)':d={int(dur*30)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            str(clip_path)
        ]
        subprocess.run(cmd_clip, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        clips.append(clip_path)

    concat_file = OUTPUT_DIR / "concat_fit.txt"
    with open(concat_file, "w", encoding="utf-8") as f:
        for c in clips:
            f.write(f"file '{c.name}'\n")

    video_raw = OUTPUT_DIR / "video_fit_raw.mp4"
    subprocess.run([ffmpeg_bin, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file), "-c", "copy", str(video_raw)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    cmd_final = [
        ffmpeg_bin, "-y",
        "-i", str(video_raw),
        "-i", str(ruta_audio),
        "-filter_complex", f"[0:v]subtitles='{ass_escaped}'[vout]",
        "-map", "[vout]",
        "-map", "1:a",
        "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(ruta_final)
    ]
    subprocess.run(cmd_final, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"🎬 ¡VÍDEO CON ENCAJE TIPOGRÁFICO PERFECTO GENERADO!: {ruta_final}")

async def main():
    print("🔧 Generando escenas con auto-ajuste de márgenes y tipografía...")
    e1 = OUTPUT_DIR / "earth_fit_e1.png"
    e2 = OUTPUT_DIR / "earth_fit_e2.png"
    e3 = OUTPUT_DIR / "earth_fit_e3.png"
    e4 = OUTPUT_DIR / "earth_fit_e4.png"

    preparar_escena_1_satelite(e1)
    preparar_escena_2_fachada(e2)
    preparar_escena_3_interior(e3)
    preparar_escena_4_telegram(e4)

    ruta_audio = OUTPUT_DIR / "visual_fit_locucion.mp3"
    ruta_srt = OUTPUT_DIR / "visual_fit_subtitulos.srt"
    ruta_ass = OUTPUT_DIR / "visual_fit_subtitulos.ass"
    ruta_final = OUTPUT_DIR / "subasta_tiktok_EARTH_PERFECTO.mp4"

    await generar_locucion_y_subtitulos(GUION_VISUAL, ruta_audio, ruta_srt)
    convertir_srt_a_ass(ruta_srt, ruta_ass)

    duraciones = [3.5, 5.0, 6.5, 7.0]
    ensamblar_video_cinematico([e1, e2, e3, e4], duraciones, ruta_audio, ruta_ass, ruta_final)

if __name__ == "__main__":
    asyncio.run(main())
