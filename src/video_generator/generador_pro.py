import asyncio
import os
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import edge_tts

BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Guion humano, periodístico y con intriga (no teletienda)
GUION = (
    "Mira lo que acaba de publicar el BOE hace unas horas en Madrid. "
    "Un piso de ochenta metros cuadrados que sale a subasta judicial por tan solo cuarenta y dos mil euros, "
    "cuando su tasación oficial supera los ciento noventa mil. "
    "Pero mucho cuidado, ¿dónde está el truco? "
    "Hemos revisado el expediente judicial y está completamente limpio de cargas hipotecarias anteriores. "
    "El enlace directo al expediente oficial lo tienes ahora mismo en nuestro canal de Telegram. "
    "Tienes el enlace en la biografía."
)

def obtener_ruta_ffmpeg() -> str:
    ruta = shutil.which("ffmpeg")
    if ruta:
        return ruta
    winget_path = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WinGet" / "Packages" / "Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe" / "ffmpeg-9.0.2-full_build" / "bin" / "ffmpeg.exe"
    if winget_path.exists():
        return str(winget_path)
    return "ffmpeg"

def crear_escena_1(ruta: Path):
    """Escena 1: El gancho e intriga con estética oficial del BOE."""
    img = Image.new("RGB", (1080, 1920), color=(11, 15, 25))
    draw = ImageDraw.Draw(img)

    f_h1 = ImageFont.truetype("arialbd.ttf", 64)
    f_sub = ImageFont.truetype("arial.ttf", 38)
    f_badge = ImageFont.truetype("arialbd.ttf", 36)
    f_bold = ImageFont.truetype("arialbd.ttf", 44)

    # 1. Cabecera simulada Portal Oficial
    draw.rectangle([0, 0, 1080, 180], fill=(15, 23, 42))
    draw.text((60, 60), "MINISTERIO DE LA PRESIDENCIA Y JUSTICIA", font=f_sub, fill=(148, 163, 184))
    draw.text((60, 110), "PORTAL DE SUBASTAS DEL BOE", font=f_badge, fill=(248, 250, 252))

    # 2. Badge de urgencia
    draw.rounded_rectangle([100, 260, 980, 350], radius=18, fill=(220, 38, 38))
    draw.text((540, 305), "⚠️ PUBLICADO HOY EN MADRID", font=f_badge, fill=(255, 255, 255), anchor="mm")

    # 3. Tarjeta central de la duda
    card = [80, 420, 1000, 1150]
    draw.rounded_rectangle(card, radius=32, fill=(24, 32, 53), outline=(51, 65, 85), width=3)

    draw.text((540, 520), "¿CÓMO ES POSIBLE", font=f_h1, fill=(255, 255, 255), anchor="mm")
    draw.text((540, 600), "ESTE PRECIO?", font=f_h1, fill=(234, 179, 8), anchor="mm") # Amarillo

    draw.text((540, 720), "Piso 80 m² • 3 Dormitorios", font=f_bold, fill=(226, 232, 240), anchor="mm")
    draw.text((540, 790), "Zona Norte de Madrid (Barrio del Pilar)", font=f_sub, fill=(148, 163, 184), anchor="mm")

    # Separador
    draw.line([(160, 870), (920, 870)], fill=(51, 65, 85), width=2)

    draw.text((540, 940), "Expediente Judicial SUB-JA-2026", font=f_sub, fill=(148, 163, 184), anchor="mm")
    draw.text((540, 1020), "Salida por solo 42.000 €", font=f_bold, fill=(34, 197, 94), anchor="mm")

    # 4. Pie de pantalla con gancho
    draw.rounded_rectangle([80, 1260, 1000, 1500], radius=24, fill=(30, 41, 59))
    draw.text((540, 1340), "Analizamos el edicto oficial", font=f_bold, fill=(248, 250, 252), anchor="mm")
    draw.text((540, 1420), "¿Tiene trampa o deudas ocultas? 👇", font=f_sub, fill=(203, 213, 225), anchor="mm")

    img.save(ruta, quality=95)

def crear_escena_2(ruta: Path):
    """Escena 2: Contraste brutal de números (El Chollo)."""
    img = Image.new("RGB", (1080, 1920), color=(11, 15, 25))
    draw = ImageDraw.Draw(img)

    f_title = ImageFont.truetype("arialbd.ttf", 52)
    f_sub = ImageFont.truetype("arial.ttf", 36)
    f_num_big = ImageFont.truetype("arialbd.ttf", 108)
    f_num_tachado = ImageFont.truetype("arialbd.ttf", 72)
    f_badge = ImageFont.truetype("arialbd.ttf", 46)

    # Cabecera
    draw.rectangle([0, 0, 1080, 180], fill=(15, 23, 42))
    draw.text((540, 90), "COMPARATIVA DE MERCADO", font=f_title, fill=(255, 255, 255), anchor="mm")

    # Tarjeta 1: Tasación oficial
    draw.rounded_rectangle([80, 250, 1000, 620], radius=28, fill=(24, 32, 53), outline=(71, 85, 105), width=2)
    draw.text((540, 330), "VALORACIÓN OFICIAL EN EL EXPEDIENTE", font=f_sub, fill=(148, 163, 184), anchor="mm")
    draw.text((540, 440), "190.000 €", font=f_num_tachado, fill=(239, 68, 68), anchor="mm")
    draw.line([(320, 440), (760, 440)], fill=(239, 68, 68), width=8)
    draw.text((540, 540), "(Precio medio de mercado en la zona)", font=f_sub, fill=(100, 116, 139), anchor="mm")

    # Tarjeta 2: Precio de subasta
    draw.rounded_rectangle([80, 680, 1000, 1140], radius=32, fill=(16, 44, 34), outline=(34, 197, 94), width=4)
    draw.text((540, 770), "PRECIO DE SALIDA EN LA SUBASTA", font=f_sub, fill=(187, 247, 208), anchor="mm")
    draw.text((540, 900), "42.000 €", font=f_num_big, fill=(34, 197, 94), anchor="mm")
    
    # Badge ahorro
    draw.rounded_rectangle([320, 1010, 760, 1090], radius=20, fill=(34, 197, 94))
    draw.text((540, 1050), "AHORRO DEL 78%", font=f_badge, fill=(11, 15, 25), anchor="mm")

    # Explicación
    draw.rounded_rectangle([80, 1220, 1000, 1500], radius=24, fill=(30, 41, 59))
    draw.text((540, 1300), "Pujas abiertas en el portal judicial", font=f_title, fill=(255, 255, 255), anchor="mm")
    draw.text((540, 1390), "Comprobamos si hay inquilinos o deudas... 👀", font=f_sub, fill=(148, 163, 184), anchor="mm")

    img.save(ruta, quality=95)

def crear_escena_3(ruta: Path):
    """Escena 3: Verificación de cargas y llamada a la acción hacia Telegram."""
    img = Image.new("RGB", (1080, 1920), color=(11, 15, 25))
    draw = ImageDraw.Draw(img)

    f_title = ImageFont.truetype("arialbd.ttf", 54)
    f_sub = ImageFont.truetype("arial.ttf", 38)
    f_check = ImageFont.truetype("arialbd.ttf", 42)
    f_cta = ImageFont.truetype("arialbd.ttf", 46)

    # Cabecera
    draw.rectangle([0, 0, 1080, 180], fill=(15, 23, 42))
    draw.text((540, 90), "DICTAMEN DEL EXPEDIENTE", font=f_title, fill=(255, 255, 255), anchor="mm")

    # Tarjeta de Verificación
    draw.rounded_rectangle([80, 240, 1000, 960], radius=32, fill=(24, 32, 53), outline=(37, 99, 235), width=3)
    
    # Sello de comprobación
    draw.rounded_rectangle([250, 310, 830, 390], radius=16, fill=(34, 197, 94))
    draw.text((540, 350), "EXPEDIENTE REVISADO", font=f_check, fill=(11, 15, 25), anchor="mm")

    items = [
        ("✔ Cargas anteriores:", "0,00 € (LIMPIO)"),
        ("✔ Hipoteca previa:", "Cancelada formalmente"),
        ("✔ Depósito para pujar:", "2.100 € (5%)"),
        ("⏳ Plazo de cierre:", "Finaliza en 6 días")
    ]
    y = 470
    for titulo_item, valor_item in items:
        draw.text((140, y), titulo_item, font=f_check, fill=(255, 255, 255), anchor="lm")
        draw.text((140, y + 48), valor_item, font=f_sub, fill=(148, 163, 184), anchor="lm")
        y += 115

    # Tarjeta de Telegram CTA
    cta_box = [80, 1040, 1000, 1560]
    draw.rounded_rectangle(cta_box, radius=32, fill=(37, 99, 235))
    draw.text((540, 1140), "ENLACE DIRECTO AL BOE", font=f_cta, fill=(255, 255, 255), anchor="mm")
    draw.text((540, 1230), "Publicado en nuestro canal de Telegram", font=f_sub, fill=(219, 234, 254), anchor="mm")
    draw.text((540, 1340), "Acceso a todas las subastas analizadas", font=f_sub, fill=(255, 255, 255), anchor="mm")

    draw.rounded_rectangle([160, 1420, 920, 1500], radius=20, fill=(255, 255, 255))
    draw.text((540, 1460), "👉 LINK EN NUESTRO PERFIL", font=f_cta, fill=(37, 99, 235), anchor="mm")

    img.save(ruta, quality=95)

async def generar_locucion_y_subtitulos(texto: str, ruta_audio: Path, ruta_srt: Path):
    """Genera audio con Edge-TTS y extrae subtítulos con marcas de tiempo precisas."""
    com = edge_tts.Communicate(texto, "es-ES-AlvaroNeural", rate="+6%")
    submaker = edge_tts.SubMaker()
    
    with open(ruta_audio, "wb") as f_audio:
        async for chunk in com.stream():
            if chunk["type"] == "audio":
                f_audio.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.feed(chunk)
                
    with open(ruta_srt, "w", encoding="utf-8") as f_srt:
        f_srt.write(submaker.get_srt())
    print("✅ Locución y subtítulos sincronizados generados con éxito.")

def convertir_srt_a_ass_tiktok(ruta_srt: Path, ruta_ass: Path):
    """Convierte el SRT estándar a un estilo ASS llamativo de TikTok (amarillo con borde negro grueso)."""
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: TikTok,Arial Black,56,&H0000FFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,8,2,2,80,80,240,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    # Leer el SRT y generar eventos ASS
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
                inicio = partes[0][:11]  # 00:00:00.00
                fin = partes[1][:11]
                texto = " ".join(lineas[2:]).upper()
                eventos.append(f"Dialogue: 0,{inicio},{fin},TikTok,,0,0,0,,{texto}")

    with open(ruta_ass, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(eventos))
    print("✅ Estilo de subtítulos TikTok (.ass) generado.")

def generar_musica_fondo(ruta_wav: Path, duracion_seg: float):
    """Crea una pista sutil de tensión rítmica (onda sintetizada) para fondo."""
    import math
    import wave
    import struct

    framerate = 44100
    nframes = int(framerate * duracion_seg)
    with wave.open(str(ruta_wav), "w") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(framerate)
        for i in range(nframes):
            t = float(i) / framerate
            # Ritmo de bajo a 120 bpm (2 Hz) con tono grave de 65Hz y 130Hz
            beat = math.exp(-((t % 0.5) * 8)) # Decaimiento tipo bombo suave
            val = math.sin(2 * math.pi * 65 * t) * 0.25 * beat
            # Tono de tensión sostenido
            ambient = math.sin(2 * math.pi * 110 * t) * 0.05
            sample = int((val + ambient) * 32767 * 0.4)
            wav.writeframesraw(struct.pack('<h', max(-32767, min(32767, sample))))
    print("✅ Pista de fondo de tensión sintetizada.")

def ensamblar_video_pro(escenas: list, ruta_audio: Path, ruta_musica: Path, ruta_ass: Path, ruta_video: Path):
    """Ensambla cortes dinámicos con zoom continuo, subtítulos y audio mezclado."""
    ffmpeg_bin = obtener_ruta_ffmpeg()
    
    # 1. Crear clips de vídeo para cada escena (5.5s para escena 1, 7.5s para escena 2, 7s para escena 3)
    duraciones = [5.0, 7.5, 7.5]
    clips_generados = []
    
    for idx, (img_path, dur) in enumerate(zip(escenas, duraciones)):
        clip_temp = OUTPUT_DIR / f"clip_escena_{idx+1}.mp4"
        # Filtro de zoom lento (Ken Burns)
        cmd_clip = [
            ffmpeg_bin, "-y",
            "-loop", "1", "-i", str(img_path),
            "-t", str(dur),
            "-vf", f"scale=1080:1920,zoompan=z='min(zoom+0.0008,1.08)':d={int(dur*30)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            str(clip_temp)
        ]
        subprocess.run(cmd_clip, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        clips_generados.append(clip_temp)

    # 2. Concatenar las 3 escenas
    concat_txt = OUTPUT_DIR / "concat.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for c in clips_generados:
            f.write(f"file '{c.name}'\n")

    video_concatenado = OUTPUT_DIR / "video_raw_concat.mp4"
    cmd_concat = [
        ffmpeg_bin, "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_txt),
        "-c", "copy",
        str(video_concatenado)
    ]
    subprocess.run(cmd_concat, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 3. Mezclar audio de voz + música de fondo (-18dB) y quemar subtítulos ASS
    # Escapar ruta para filtro de ffmpeg en Windows
    ass_escaped = str(ruta_ass).replace("\\", "/").replace(":", "\\:")
    
    cmd_final = [
        ffmpeg_bin, "-y",
        "-i", str(video_concatenado),
        "-i", str(ruta_audio),
        "-i", str(ruta_musica),
        "-filter_complex",
        f"[2:a]volume=0.15[bg];[1:a][bg]amix=inputs=2:duration=first[aout];[0:v]subtitles='{ass_escaped}'[vout]",
        "-map", "[vout]",
        "-map", "[aout]",
        "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(ruta_video)
    ]
    subprocess.run(cmd_final, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"🔥 ¡VÍDEO PRO GENERADO!: {ruta_video}")

async def main():
    print("🚀 Construyendo generador dinámico de vídeo estilo TikTok...")
    
    e1 = OUTPUT_DIR / "pro_escena_1.png"
    e2 = OUTPUT_DIR / "pro_escena_2.png"
    e3 = OUTPUT_DIR / "pro_escena_3.png"
    
    crear_escena_1(e1)
    crear_escena_2(e2)
    crear_escena_3(e3)

    ruta_audio = OUTPUT_DIR / "pro_locucion.mp3"
    ruta_srt = OUTPUT_DIR / "pro_subtitulos.srt"
    ruta_ass = OUTPUT_DIR / "pro_subtitulos.ass"
    ruta_musica = OUTPUT_DIR / "pro_tension_beat.wav"
    ruta_video_final = OUTPUT_DIR / "subasta_tiktok_PRO.mp4"

    # Generar voz y subtítulos
    await generar_locucion_y_subtitulos(GUION, ruta_audio, ruta_srt)
    convertir_srt_a_ass_tiktok(ruta_srt, ruta_ass)

    # Generar música de fondo (duración ~21 seg)
    generar_musica_fondo(ruta_musica, 21.0)

    # Ensamblar vídeo con movimiento, subtítulos y sonido
    ensamblar_video_pro([e1, e2, e3], ruta_audio, ruta_musica, ruta_ass, ruta_video_final)

if __name__ == "__main__":
    asyncio.run(main())
