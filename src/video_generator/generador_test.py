import asyncio
import os
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import edge_tts

# Directorios base
BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Datos de la alerta de prueba
ALERTA_TEST = {
    "categoria": "🚨 SUBASTA BOE DESTACADA",
    "titulo": "Piso 80 m² en Madrid",
    "subtitulo": "Barrio del Pilar • 3 Habitaciones",
    "tasacion": "190.000 €",
    "salida": "42.000 €",
    "descuento": "-78%",
    "detalles": [
        "✔ Sin cargas hipotecarias previas",
        "✔ Depósito para pujar: 2.100 €",
        "✔ Plazo: Finaliza en 6 días"
    ],
    "guion_locucion": (
        "¡Atento a esta oportunidad del BOE en Madrid! "
        "Sale a subasta un piso de ochenta metros cuadrados tasado en ciento noventa mil euros "
        "por tan solo cuarenta y dos mil euros. "
        "Es un setenta y ocho por ciento de ahorro respecto a su valor real. "
        "El expediente no presenta cargas hipotecarias anteriores. "
        "El enlace oficial al expediente y todos los datos los tienes en nuestro canal de Telegram. "
        "Tienes el enlace en la biografía."
    )
}

def crear_imagen_vertical(alerta: dict, ruta_salida: Path):
    """Crea una tarjeta vertical 1080x1920 con diseño moderno optimizado para TikTok."""
    ancho, alto = 1080, 1920
    # Fondo con degradado oscuro moderno (azul oscuro a negro)
    img = Image.new("RGB", (ancho, alto), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)

    # Fuentes del sistema Windows
    try:
        font_badge = ImageFont.truetype("arialbd.ttf", 42)
        font_titulo = ImageFont.truetype("arialbd.ttf", 68)
        font_sub = ImageFont.truetype("arial.ttf", 40)
        font_precio_label = ImageFont.truetype("arial.ttf", 36)
        font_precio_tachado = ImageFont.truetype("arialbd.ttf", 60)
        font_precio_ganga = ImageFont.truetype("arialbd.ttf", 100)
        font_descuento = ImageFont.truetype("arialbd.ttf", 48)
        font_item = ImageFont.truetype("arial.ttf", 42)
        font_cta = ImageFont.truetype("arialbd.ttf", 44)
    except Exception:
        font_badge = font_titulo = font_sub = font_precio_label = None
        font_precio_tachado = font_precio_ganga = font_descuento = font_item = font_cta = None

    # 1. Badge superior
    badge_rect = [100, 180, 980, 260]
    draw.rounded_rectangle(badge_rect, radius=20, fill=(225, 29, 72))  # Rojo/Crimson llamativo
    draw.text((540, 220), alerta["categoria"], font=font_badge, fill=(255, 255, 255), anchor="mm")

    # 2. Título y subtítulo
    draw.text((540, 360), alerta["titulo"], font=font_titulo, fill=(255, 255, 255), anchor="mm")
    draw.text((540, 440), alerta["subtitulo"], font=font_sub, fill=(148, 163, 184), anchor="mm")

    # 3. Tarjeta central de precios
    card_rect = [80, 520, 1000, 1050]
    draw.rounded_rectangle(card_rect, radius=32, fill=(30, 41, 59), outline=(51, 65, 85), width=4)

    # Valor tasación
    draw.text((540, 590), "VALOR DE TASACIÓN OFICIAL", font=font_precio_label, fill=(148, 163, 184), anchor="mm")
    draw.text((540, 660), alerta["tasacion"], font=font_precio_tachado, fill=(239, 68, 68), anchor="mm")
    # Línea que tacha el precio
    draw.line([(380, 660), (700, 660)], fill=(239, 68, 68), width=6)

    # Precio de salida
    draw.text((540, 770), "PRECIO DE SALIDA EN SUBASTA", font=font_precio_label, fill=(148, 163, 184), anchor="mm")
    draw.text((540, 870), alerta["salida"], font=font_precio_ganga, fill=(34, 197, 94), anchor="mm")  # Verde brillante

    # Badge de ahorro
    desc_rect = [380, 950, 700, 1020]
    draw.rounded_rectangle(desc_rect, radius=16, fill=(34, 197, 94))
    draw.text((540, 985), f"AHORRO {alerta['descuento']}", font=font_descuento, fill=(15, 23, 42), anchor="mm")

    # 4. Lista de puntos clave
    card_info_rect = [80, 1100, 1000, 1420]
    draw.rounded_rectangle(card_info_rect, radius=32, fill=(30, 41, 59), outline=(51, 65, 85), width=2)
    y_item = 1170
    for detalle in alerta["detalles"]:
        draw.text((140, y_item), detalle, font=font_item, fill=(241, 245, 249), anchor="lm")
        y_item += 85

    # 5. Call To Action (Pie inferior)
    cta_rect = [80, 1500, 1000, 1720]
    draw.rounded_rectangle(cta_rect, radius=32, fill=(37, 99, 235))  # Azul vibrante
    draw.text((540, 1570), "EXPEDIENTE COMPLETO EN TELEGRAM", font=font_cta, fill=(255, 255, 255), anchor="mm")
    draw.text((540, 1640), "👉 Enlace directo en el perfil (Link en Bio)", font=font_sub, fill=(191, 219, 254), anchor="mm")

    img.save(ruta_salida, quality=95)
    print(f"✅ Imagen generada: {ruta_salida}")

async def generar_audio(texto: str, ruta_salida: Path, voz: str = "es-ES-AlvaroNeural"):
    """Genera la locución con la voz neuronal de Microsoft Edge (100% gratuita)."""
    com = edge_tts.Communicate(texto, voz, rate="+5%")
    await com.save(str(ruta_salida))
    print(f"✅ Audio generado con voz '{voz}': {ruta_salida}")

import shutil

def obtener_ruta_ffmpeg() -> str:
    """Busca ffmpeg en PATH o en las rutas habituales de instalación de Windows."""
    ruta_en_path = shutil.which("ffmpeg")
    if ruta_en_path:
        return ruta_en_path
    
    # Rutas típicas de WinGet y Chocolatey en Windows
    rutas_candidatas = [
        Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WinGet" / "Packages" / "Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe" / "ffmpeg-9.0.2-full_build" / "bin" / "ffmpeg.exe",
        Path("C:/ffmpeg/bin/ffmpeg.exe"),
        Path(os.environ.get("ProgramFiles", "")) / "ffmpeg" / "bin" / "ffmpeg.exe"
    ]
    for r in rutas_candidatas:
        if r.exists():
            return str(r)
    return "ffmpeg"

def ensamblar_video(ruta_imagen: Path, ruta_audio: Path, ruta_video: Path):
    """Ensambla imagen estática + audio en un archivo MP4 vertical listo para TikTok."""
    ffmpeg_bin = obtener_ruta_ffmpeg()
    cmd = [
        ffmpeg_bin,
        "-y",
        "-loop", "1",
        "-i", str(ruta_imagen),
        "-i", str(ruta_audio),
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        str(ruta_video)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"🎬 ¡Vídeo TikTok completado con éxito!: {ruta_video}")

async def main():
    print("🚀 Iniciando Fase 1: Generador de vídeo automatizado...")
    ruta_img = OUTPUT_DIR / "frame_subasta.png"
    ruta_audio = OUTPUT_DIR / "locucion_subasta.mp3"
    ruta_video = OUTPUT_DIR / "subasta_tiktok_demo.mp4"

    # Paso 1: Generar imagen
    crear_imagen_vertical(ALERTA_TEST, ruta_img)

    # Paso 2: Generar audio
    await generar_audio(ALERTA_TEST["guion_locucion"], ruta_audio)

    # Paso 3: Ensamblar vídeo MP4
    ensamblar_video(ruta_img, ruta_audio, ruta_video)

if __name__ == "__main__":
    asyncio.run(main())
