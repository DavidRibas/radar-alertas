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

def preparar_escena_1_satelite(ruta_salida: Path):
    """Escena 1 (Google Earth Dive): Foto de satélite con pin de ubicación en Madrid."""
    ancho, alto = 1080, 1920
    # Abrir satélite de la Tierra / España
    sat_img = Image.open(TEMPLATES_DIR / "satelite_tierra.jpg").convert("RGB")
    sat_img = sat_img.resize((ancho, alto), Image.Resampling.LANCZOS)
    
    # Oscurecer ligeramente para contrastar
    overlay = Image.new("RGBA", (ancho, alto), (0, 0, 0, 80))
    sat_img.paste(overlay, (0, 0), overlay)
    draw = ImageDraw.Draw(sat_img)

    f_pin = ImageFont.truetype("arialbd.ttf", 56)
    f_badge = ImageFont.truetype("arialbd.ttf", 36)
    f_sub = ImageFont.truetype("arial.ttf", 40)

    # Pin de ubicación estilo Google Earth
    draw.rounded_rectangle([140, 750, 940, 920], radius=24, fill=(15, 23, 42, 230), outline=(239, 68, 68), width=4)
    draw.text((540, 810), "📍 MADRID • BARRIO DEL PILAR", font=f_pin, fill=(255, 255, 255), anchor="mm")
    draw.text((540, 875), "Aterrizando en la oportunidad del día...", font=f_sub, fill=(248, 113, 113), anchor="mm")

    # Badge superior de Alerta
    draw.rounded_rectangle([180, 200, 900, 290], radius=20, fill=(220, 38, 38))
    draw.text((540, 245), "🚨 NUEVA SUBASTA JUDICIAL", font=f_badge, fill=(255, 255, 255), anchor="mm")

    sat_img.save(ruta_salida, quality=95)

def preparar_escena_2_fachada(ruta_salida: Path):
    """Escena 2 (Fachada del Edificio / Vista aérea real): Cero texto denso, solo la foto y el precio."""
    ancho, alto = 1080, 1920
    # Imagen de la fachada / calle
    fac_img = Image.open(TEMPLATES_DIR / "fachada_edificio.jpg").convert("RGB")
    fac_img = fac_img.resize((ancho, alto), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(fac_img)

    f_title = ImageFont.truetype("arialbd.ttf", 52)
    f_precio = ImageFont.truetype("arialbd.ttf", 94)
    f_sub = ImageFont.truetype("arialbd.ttf", 38)

    # Tarjeta flotante moderna semi-transparente en el tercio inferior
    card = [60, 1150, 1020, 1580]
    draw.rounded_rectangle(card, radius=32, fill=(15, 23, 42), outline=(34, 197, 94), width=4)

    draw.text((540, 1220), "PISO 80 m² • 3 HABITACIONES", font=f_title, fill=(255, 255, 255), anchor="mm")
    draw.text((540, 1290), "PRECIO DE SALIDA EN SUBASTA", font=f_sub, fill=(148, 163, 184), anchor="mm")
    
    # Precio verde gigante
    draw.text((540, 1390), "42.000 €", font=f_precio, fill=(34, 197, 94), anchor="mm")
    
    # Badge ahorro
    draw.rounded_rectangle([320, 1470, 760, 1540], radius=16, fill=(34, 197, 94))
    draw.text((540, 1505), "78% DE DESCUENTO", font=f_sub, fill=(15, 23, 42), anchor="mm")

    fac_img.save(ruta_salida, quality=95)

def preparar_escena_3_interior(ruta_salida: Path):
    """Escena 3 (Interior reformado + Margen de beneficio): El número que hace soñar al inversor."""
    ancho, alto = 1080, 1920
    int_img = Image.open(TEMPLATES_DIR / "interior_piso.jpg").convert("RGB")
    int_img = int_img.resize((ancho, alto), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(int_img)

    f_label = ImageFont.truetype("arialbd.ttf", 36)
    f_val = ImageFont.truetype("arialbd.ttf", 54)
    f_ganancia = ImageFont.truetype("arialbd.ttf", 80)
    f_check = ImageFont.truetype("arialbd.ttf", 34)

    # Tarjeta de Comparativa de Mercado
    card = [60, 950, 1020, 1620]
    draw.rounded_rectangle(card, radius=32, fill=(15, 23, 42), outline=(56, 189, 248), width=3)

    # Línea 1: Precio de mercado
    draw.text((540, 1010), "VALOR MEDIO REFORMADO EN LA ZONA", font=f_label, fill=(148, 163, 184), anchor="mm")
    draw.text((540, 1070), "270.000 € (3.380 €/m²)", font=f_val, fill=(56, 189, 248), anchor="mm")

    # Separador
    draw.line([(140, 1125), (940, 1125)], fill=(51, 65, 85), width=2)

    # Línea 2: El Margen Bruto
    draw.text((540, 1170), "PLUSVALÍA / MARGEN BRUTO ESTIMADO", font=f_label, fill=(187, 247, 208), anchor="mm")
    draw.text((540, 1260), "+ 228.000 €", font=f_ganancia, fill=(34, 197, 94), anchor="mm")

    # Badge de cargas limpias
    draw.rounded_rectangle([180, 1340, 900, 1420], radius=16, fill=(22, 101, 52))
    draw.text((540, 1380), "✔ CARGAS: 0,00 € (EXPEDIENTE LIMPIO)", font=f_check, fill=(255, 255, 255), anchor="mm")

    # Rentabilidad
    draw.text((540, 1490), "Alquiler estimado: 1.150 € / mes (Alta demanda)", font=f_label, fill=(203, 213, 225), anchor="mm")
    draw.text((540, 1550), "Zona Barrio del Pilar (Madrid)", font=f_check, fill=(148, 163, 184), anchor="mm")

    int_img.save(ruta_salida, quality=95)

def preparar_escena_4_telegram(ruta_salida: Path):
    """Escena 4: Pantalla final exclusiva de Telegram. Cero dudas de cómo entrar."""
    ancho, alto = 1080, 1920
    # Fondo con la vista aérea desenfocada
    bg = Image.open(TEMPLATES_DIR / "barrio_pilar_aerea.jpg").convert("RGB")
    bg = bg.resize((ancho, alto), Image.Resampling.LANCZOS)
    bg = bg.filter(ImageFilter.GaussianBlur(15))
    draw = ImageDraw.Draw(bg)

    f_logo = ImageFont.truetype("arialbd.ttf", 64)
    f_sub = ImageFont.truetype("arial.ttf", 38)
    f_step = ImageFont.truetype("arialbd.ttf", 36)
    f_btn = ImageFont.truetype("arialbd.ttf", 46)

    # Tarjeta gigante de Telegram
    card = [70, 350, 1010, 1550]
    draw.rounded_rectangle(card, radius=36, fill=(15, 23, 42), outline=(56, 189, 248), width=5)

    # Cabecera Telegram
    draw.rounded_rectangle([70, 350, 1010, 520], radius=32, fill=(2, 132, 199))
    draw.text((540, 415), "✈️ TELEGRAM PRIVADO", font=f_logo, fill=(255, 255, 255), anchor="mm")
    draw.text((540, 480), "RadarAlertas • Canal Exclusivo", font=f_sub, fill=(224, 242, 254), anchor="mm")

    # Explicación del valor
    draw.text((540, 600), "ACCEDE AL EXPEDIENTE COMPLETO", font=f_step, fill=(255, 255, 255), anchor="mm")
    draw.text((540, 660), "Enlace judicial directo, fotos y filtro de cargas", font=f_sub, fill=(148, 163, 184), anchor="mm")

    # Pasos 1 - 2 - 3 gigantes
    pasos = [
        ("1️⃣", "Toca nuestra foto de perfil de TikTok"),
        ("2️⃣", "Haz clic en el enlace de la Biografía (Link in Bio)"),
        ("3️⃣", "Entra al canal y recibe las alertas en tiempo real")
    ]
    y = 780
    for num, txt in pasos:
        draw.rounded_rectangle([120, y, 960, y + 100], radius=18, fill=(30, 41, 59), outline=(71, 85, 105), width=2)
        draw.text((170, y + 50), num, font=f_step, fill=(255, 255, 255), anchor="mm")
        draw.text((230, y + 50), txt, font=f_sub, fill=(248, 250, 252), anchor="lm")
        y += 140

    # Botón brillante de llamada a la acción
    draw.rounded_rectangle([120, 1320, 960, 1460], radius=24, fill=(34, 197, 94))
    draw.text((540, 1390), "👉 ¡LINK EN EL PERFIL! 👈", font=f_btn, fill=(15, 23, 42), anchor="mm")

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
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Visual,Arial Black,48,&H0000FFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,7,2,2,80,80,220,1

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
                eventos.append(f"Dialogue: 0,{inicio},{fin},Visual,,0,0,0,,{texto}")

    with open(ruta_ass, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(eventos))

def ensamblar_video_cinematico(escenas: list, duraciones: list, ruta_audio: Path, ruta_ass: Path, ruta_final: Path):
    """Ensambla cortes con zoom fluido (Ken Burns acelerado), voz y subtítulos limpios."""
    ffmpeg_bin = obtener_ruta_ffmpeg()
    ass_escaped = str(ruta_ass).replace("\\", "/").replace(":", "\\:")

    clips = []
    for idx, (img_path, dur) in enumerate(zip(escenas, duraciones)):
        clip_path = OUTPUT_DIR / f"clip_visual_{idx+1}.mp4"
        # Zoom cinematográfico dinámico
        cmd_clip = [
            ffmpeg_bin, "-y",
            "-loop", "1", "-i", str(img_path),
            "-t", str(dur),
            "-vf", f"scale=1080:1920,zoompan=z='min(zoom+0.0012,1.12)':d={int(dur*30)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            str(clip_path)
        ]
        subprocess.run(cmd_clip, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        clips.append(clip_path)

    # Concatenar clips
    concat_file = OUTPUT_DIR / "concat_visual.txt"
    with open(concat_file, "w", encoding="utf-8") as f:
        for c in clips:
            f.write(f"file '{c.name}'\n")

    video_raw = OUTPUT_DIR / "video_visual_raw.mp4"
    subprocess.run([ffmpeg_bin, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file), "-c", "copy", str(video_raw)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Quemar subtítulos y pegar audio
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
    print(f"🎬 ¡VÍDEO CINEMÁTICO REAL ESTATE GENERADO!: {ruta_final}")

async def main():
    print("🚀 Iniciando generador cinematográfico Idea 1 (Google Earth + Fotos Inmueble)...")
    e1 = OUTPUT_DIR / "earth_e1.png"
    e2 = OUTPUT_DIR / "earth_e2.png"
    e3 = OUTPUT_DIR / "earth_e3.png"
    e4 = OUTPUT_DIR / "earth_e4.png"

    # 1. Preparar las 4 escenas visuales fotográficas
    preparar_escena_1_satelite(e1)
    preparar_escena_2_fachada(e2)
    preparar_escena_3_interior(e3)
    preparar_escena_4_telegram(e4)

    ruta_audio = OUTPUT_DIR / "visual_locucion.mp3"
    ruta_srt = OUTPUT_DIR / "visual_subtitulos.srt"
    ruta_ass = OUTPUT_DIR / "visual_subtitulos.ass"
    ruta_final = OUTPUT_DIR / "subasta_tiktok_EARTH_VISUAL.mp4"

    # 2. Generar audio y subtítulos
    await generar_locucion_y_subtitulos(GUION_VISUAL, ruta_audio, ruta_srt)
    convertir_srt_a_ass(ruta_srt, ruta_ass)

    # 3. Duraciones sincronizadas con las frases:
    # Escena 1 (Satélite): 3.5s
    # Escena 2 (Fachada): 5.0s
    # Escena 3 (Interior reformado + margen): 6.5s
    # Escena 4 (Telegram onboarding): 7.0s
    duraciones = [3.5, 5.0, 6.5, 7.0]

    # 4. Render final con FFmpeg
    ensamblar_video_cinematico([e1, e2, e3, e4], duraciones, ruta_audio, ruta_ass, ruta_final)

if __name__ == "__main__":
    asyncio.run(main())
