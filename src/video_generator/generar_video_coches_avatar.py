"""
Generador de Vídeo Split-Screen con Avatar para Vehículos Embargados (RadarAlertas)
"""
import os
import shutil
import asyncio
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import edge_tts

BASE_DIR = Path("C:/Ideas/radar-alertas")
OUTPUT_DIR = BASE_DIR / "output"
ASSETS_DIR = BASE_DIR / "assets"
TEMPLATES_DIR = ASSETS_DIR / "templates"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

AVATAR_PATH = ASSETS_DIR / "avatar_presentador_1.jpg"
BEAT_PATH = OUTPUT_DIR / "pro_tension_beat.wav"

GUION_COCHES = (
    "¡No compres un coche de segunda mano antes de ver este vídeo! "
    "Porque lo que acaban de publicar los juzgados y la Seguridad Social en el BOE es una locura. "
    "Turismos, todoterrenos y furgonetas embargadas con precios de salida desde solo novecientos ochenta euros. "
    "En portales de segunda mano, estos mismos vehículos cotizan por más de catorce mil euros. "
    "¿Dónde está el peligro? En las cargas y multas de la DGT. "
    "Por eso hemos preparado una Guía Práctica en PDF donde te enseñamos paso a paso "
    "cómo pedir el informe reducido y cómo se cancelan los precintos por Decreto Judicial sin sorpresas. "
    "Tienes la guía completa y las alertas en directo gratis en el enlace de mi perfil. "
    "Entra y descárgatela antes de que empiece la puja."
)

def obtener_ffmpeg() -> str:
    r = shutil.which("ffmpeg")
    if r:
        return r
    winget = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WinGet" / "Packages" / "Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe" / "ffmpeg-9.0.2-full_build" / "bin" / "ffmpeg.exe"
    if winget.exists():
        return str(winget)
    return "ffmpeg"

def obtener_duracion_audio(ruta_audio: Path) -> float:
    try:
        ffmpeg_bin = obtener_ffmpeg()
        cmd = [ffmpeg_bin, "-i", str(ruta_audio), "-f", "null", "-"]
        res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        for line in res.stderr.splitlines():
            if "Duration:" in line:
                partes = line.split("Duration:")[1].split(",")[0].strip()
                h, m, s = partes.split(":")
                return float(h) * 3600 + float(m) * 60 + float(s)
    except Exception as e:
        print("Error calculando duración:", e)
    return 28.0

async def generar_locucion_y_srt(texto: str, ruta_mp3: Path, ruta_srt: Path):
    voz = "es-ES-AlvaroNeural"
    com = edge_tts.Communicate(texto, voz, rate="+8%", pitch="+0Hz")
    submaker = edge_tts.SubMaker()

    with open(ruta_mp3, "wb") as f_audio:
        async for chunk in com.stream():
            if chunk["type"] == "audio":
                f_audio.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.feed(chunk)

    with open(ruta_srt, "w", encoding="utf-8") as f_sub:
        f_sub.write(submaker.get_srt())
    print("✅ Locución coches generada.")

def convertir_srt_a_ass_hormozi(ruta_srt: Path, ruta_ass: Path):
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: HormoziYellow,Arial,68,&H0000E6FF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,6,3,2,40,40,940,1

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
                eventos.append(f"Dialogue: 0,{inicio},{fin},HormoziYellow,,0,0,0,,{texto}")

    with open(ruta_ass, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(eventos))

def preparar_top_avatar(out_path: Path):
    canvas = Image.new("RGB", (1080, 960), "#080d1a")
    if AVATAR_PATH.exists():
        av = Image.open(AVATAR_PATH).convert("RGB")
        target_w, target_h = 1080, 960
        ratio = max(target_w / av.width, target_h / av.height)
        new_size = (int(av.width * ratio), int(av.height * ratio))
        av_resized = av.resize(new_size, Image.Resampling.LANCZOS)
        offset_x = (av_resized.width - target_w) // 2
        offset_y = (av_resized.height - target_h) // 2
        av_cropped = av_resized.crop((offset_x, offset_y, offset_x + target_w, offset_y + target_h))
        canvas.paste(av_cropped, (0, 0))

    draw = ImageDraw.Draw(canvas)
    f_badge = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 26)

    # Badge superior alerta
    draw.rounded_rectangle([40, 40, 470, 95], radius=28, fill=(15, 23, 42, 220), outline="#f59e0b", width=3)
    draw.ellipse([65, 58, 81, 74], fill="#f59e0b")
    draw.text((95, 54), "VEHÍCULOS EMBARGADOS BOE", font=f_badge, fill="#ffffff")

    # Separador luminoso
    draw.line([(0, 956), (1080, 956)], fill="#f59e0b", width=4)
    canvas.save(out_path, quality=95)

def preparar_bottom_c1(out_path: Path):
    """Escena 1: Depósito judicial de vehículos."""
    canvas = Image.new("RGB", (1080, 960), "#0b132b")
    v_img = TEMPLATES_DIR / "vehiculo_coche_oficial.jpg"
    if v_img.exists():
        im = Image.open(v_img).convert("RGB")
        im_crop = im.resize((1080, 960), Image.Resampling.LANCZOS)
        canvas.paste(im_crop, (0, 0))

    dark = Image.new("RGBA", (1080, 960), (10, 15, 30, 120))
    canvas.paste(dark, (0, 0), dark)

    draw = ImageDraw.Draw(canvas)
    f_title = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 52)
    f_badge = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 34)

    draw.rounded_rectangle([60, 280, 1020, 680], radius=24, fill=(11, 19, 43, 235), outline="#f59e0b", width=4)
    draw.rounded_rectangle([90, 310, 520, 370], radius=14, fill="#b45309")
    draw.text((115, 322), "⚠️ DEPÓSITOS JUDICIALES", font=f_badge, fill="#ffffff")

    draw.text((90, 400), "COCHES Y FURGONETAS", font=f_title, fill="#ffffff")
    draw.text((90, 480), "Embargos de Juzgados y Seg. Social", font=ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 38), fill="#cbd5e1")
    draw.text((90, 560), "Salida Oficial: Desde 980 €", font=ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 54), fill="#4ade80")

    canvas.save(out_path, quality=95)

def preparar_bottom_c2(out_path: Path):
    """Escena 2: Comparativa de precio coches segunda mano vs BOE."""
    canvas = Image.new("RGB", (1080, 960), "#080d1a")
    draw = ImageDraw.Draw(canvas)
    f_header = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 46)
    f_tag = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 26)
    f_num = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 68)

    draw.text((70, 60), "COMPARATIVA DE VEHÍCULO", font=f_header, fill="#ffffff")

    # Caja 1: Mercado Segunda Mano
    draw.rounded_rectangle([60, 150, 1020, 460], radius=20, fill=(30, 20, 30), outline="#ef4444", width=4)
    draw.text((95, 185), "❌ PRECIO COCHES.NET / MILANUNCIOS", font=f_tag, fill="#f87171")
    draw.text((95, 235), "14.800 €", font=f_num, fill="#ef4444")
    draw.text((95, 335), "• SUV / Compacto diésel • Precios inflados de mercado", font=ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 28), fill="#94a3b8")
    draw.line([(95, 410), (980, 410)], fill="#334155", width=2)
    draw.text((95, 420), "SOBREPRECIO CONCESIONARIO", font=f_tag, fill="#64748b")

    # Caja 2: Subasta Judicial BOE
    draw.rounded_rectangle([60, 500, 1020, 890], radius=20, fill=(15, 35, 25), outline="#22c55e", width=5)
    draw.text((95, 535), "✅ PRECIO SALIDA SUBASTA BOE", font=f_tag, fill="#4ade80")
    draw.text((95, 585), "1.200 €", font=f_num, fill="#22c55e")
    draw.text((95, 685), "• Descuento: -91% sobre tasación", font=ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 34), fill="#ffffff")
    draw.text((95, 745), "• Ahorro directo: +13.600 €", font=ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 34), fill="#4ade80")

    canvas.save(out_path, quality=95)

def preparar_bottom_c3(out_path: Path):
    """Escena 3: Verificación de cargas y precintos DGT."""
    canvas = Image.new("RGB", (1080, 960), "#080d1a")
    draw = ImageDraw.Draw(canvas)
    f_title = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 46)
    f_item = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 34)
    f_sub = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 26)

    draw.rounded_rectangle([60, 100, 1020, 860], radius=24, fill=(15, 23, 42, 235), outline="#38bdf8", width=3)
    draw.text((100, 140), "🛡️ VERIFICACIÓN LEGAL DGT", font=f_title, fill="#38bdf8")

    items = [
        ("🚗 PRECINTOS JUDICIALES: CANCELADOS", "Decreto de Adjudicación Judicial (Art. 674 LEC)"),
        ("📑 INFORME REDUCIDO DGT", "Comprobación de titularidad y cargas en tráfico"),
        ("🔍 INSPECCIÓN EN DEPÓSITO", "Cita previa para revisar motor, chapa y llaves"),
        ("⚡ SIN COMISIONES DE INTERMEDIARIO", "Puja directa en el portal oficial del Ministerio")
    ]

    y_pos = 240
    for tit, desc in items:
        draw.text((100, y_pos), tit, font=f_item, fill="#ffffff")
        draw.text((100, y_pos + 46), desc, font=f_sub, fill="#94a3b8")
        draw.line([(100, y_pos + 95), (980, y_pos + 95)], fill="#1e293b", width=2)
        y_pos += 140

    canvas.save(out_path, quality=95)

def preparar_bottom_c4(out_path: Path):
    """Escena 4: CTA Guía de Coches Embargados en PDF."""
    canvas = Image.new("RGB", (1080, 960), "#080d1a")
    draw = ImageDraw.Draw(canvas)
    f_title = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 50)
    f_bold = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 36)
    f_sub = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 28)

    draw.rounded_rectangle([60, 80, 1020, 880], radius=24, fill=(20, 30, 60, 245), outline="#f59e0b", width=4)
    draw.text((100, 120), "🎁 GUÍA COCHES EMBARGADOS", font=f_title, fill="#fbbf24")
    draw.text((100, 195), "Manual práctico: Cómo comprar vehículos en el BOE", font=f_sub, fill="#cbd5e1")

    # Caja botón 1
    draw.rounded_rectangle([100, 280, 980, 440], radius=18, fill="#b45309")
    draw.text((140, 315), "🚗 GUÍA VEHÍCULOS EN PDF (GRATIS)", font=f_bold, fill="#ffffff")
    draw.text((140, 375), "Paso a paso para revisar depósitos y cargas DGT", font=f_sub, fill="#fed7aa")

    # Caja botón 2
    draw.rounded_rectangle([100, 480, 980, 640], radius=18, fill="#166534")
    draw.text((140, 515), "📢 CANAL TELEGRAM CON ALERTAS", font=f_bold, fill="#ffffff")
    draw.text((140, 575), "Nuevos coches y furgonetas verificadas cada día", font=f_sub, fill="#86efac")

    # Flecha y aviso final
    draw.rounded_rectangle([100, 690, 980, 830], radius=16, fill="#0f172a", outline="#f59e0b", width=2)
    draw.text((140, 720), "👉 ENLACE DIRECTO EN LA BIO", font=ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 40), fill="#fbbf24")
    draw.text((140, 775), "Descarga el manual gratis ahora en el perfil", font=f_sub, fill="#94a3b8")

    canvas.save(out_path, quality=95)

def componer_frames(img_top: Path, escenas_bottom: list, duraciones: list):
    top = Image.open(img_top).convert("RGB")
    frames = []
    for idx, (b_path, dur) in enumerate(zip(escenas_bottom, duraciones)):
        full = Image.new("RGB", (1080, 1920))
        full.paste(top, (0, 0))
        bot = Image.open(b_path).convert("RGB")
        full.paste(bot, (0, 960))
        f_out = OUTPUT_DIR / f"coche_frame_{idx+1}.png"
        full.save(f_out, quality=95)
        frames.append((f_out, dur))
    return frames

def renderizar(frames_dur: list, ruta_audio: Path, ruta_ass: Path, ruta_final: Path):
    ffmpeg = obtener_ffmpeg()
    ass_escaped = str(ruta_ass).replace("\\", "/").replace(":", "\\:")

    clips = []
    for idx, (f_img, dur) in enumerate(frames_dur):
        c_path = OUTPUT_DIR / f"coche_clip_{idx+1}.mp4"
        cmd = [
            ffmpeg, "-y",
            "-loop", "1", "-i", str(f_img),
            "-t", str(dur),
            "-vf", f"scale=1080:1920,zoompan=z='min(zoom+0.0008,1.06)':d={int(dur*30)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            str(c_path)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        clips.append(c_path)

    concat_txt = OUTPUT_DIR / "concat_coche.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for c in clips:
            f.write(f"file '{c.name}'\n")

    raw_video = OUTPUT_DIR / "coche_raw.mp4"
    subprocess.run([ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c", "copy", str(raw_video)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if BEAT_PATH.exists():
        cmd_final = [
            ffmpeg, "-y",
            "-i", str(raw_video),
            "-i", str(ruta_audio),
            "-i", str(BEAT_PATH),
            "-filter_complex",
            f"[0:v]subtitles='{ass_escaped}'[vout];"
            f"[2:a]volume=0.14[beat];"
            f"[1:a][beat]amix=inputs=2:duration=first:dropout_transition=2[aout]",
            "-map", "[vout]",
            "-map", "[aout]",
            "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            str(ruta_final)
        ]
    else:
        cmd_final = [
            ffmpeg, "-y",
            "-i", str(raw_video),
            "-i", str(ruta_audio),
            "-filter_complex", f"[0:v]subtitles='{ass_escaped}'[vout];[1:a]apad=pad_dur=1.5[aout]",
            "-map", "[vout]",
            "-map", "[aout]",
            "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            str(ruta_final)
        ]

    subprocess.run(cmd_final, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"🎉 ¡VÍDEO COCHES CON AVATAR GENERADO CON ÉXITO!: {ruta_final}")

async def main():
    print("=" * 60)
    print("🚗 GENERANDO VÍDEO SPLIT-SCREEN COCHES CON AVATAR")
    print("=" * 60)

    ruta_mp3 = OUTPUT_DIR / "coche_avatar_locucion.mp3"
    ruta_srt = OUTPUT_DIR / "coche_avatar_subtitulos.srt"
    ruta_ass = OUTPUT_DIR / "coche_avatar_subtitulos.ass"
    ruta_final = OUTPUT_DIR / "video_avatar_coches_PROTOTIPO.mp4"

    await generar_locucion_y_srt(GUION_COCHES, ruta_mp3, ruta_srt)
    convertir_srt_a_ass_hormozi(ruta_srt, ruta_ass)

    dur_total = obtener_duracion_audio(ruta_mp3)
    print(f"⏱️ Duración locución coches: {dur_total:.2f} segundos")

    top_img = OUTPUT_DIR / "coche_top_avatar.png"
    b1 = OUTPUT_DIR / "coche_b1_deposito.png"
    b2 = OUTPUT_DIR / "coche_b2_comparativa.png"
    b3 = OUTPUT_DIR / "coche_b3_dgt.png"
    b4 = OUTPUT_DIR / "coche_b4_cta.png"

    preparar_top_avatar(top_img)
    preparar_bottom_c1(b1)
    preparar_bottom_c2(b2)
    preparar_bottom_c3(b3)
    preparar_bottom_c4(b4)

    d1 = 4.5
    d2 = 7.0
    d3 = 6.5
    d4 = max(6.0, (dur_total - (d1 + d2 + d3)) + 1.5)
    duraciones = [d1, d2, d3, d4]

    frames_dur = componer_frames(top_img, [b1, b2, b3, b4], duraciones)
    renderizar(frames_dur, ruta_mp3, ruta_ass, ruta_final)

if __name__ == "__main__":
    asyncio.run(main())
