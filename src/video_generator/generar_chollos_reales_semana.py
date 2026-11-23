"""
Generador de Vídeos Semanales con Datos Reales del BOE (Stitch HD Dinámico a 6 Mbps)
Compila los chollos reales extraídos en directo hoy del BOE:
1. SUV Mazda CX-5 por 1.842 € (-89%)
2. Piso en Tielmes (Madrid) por 13.956 € (-90%)
3. Mercedes-Benz B 200 D por 802 € (-89%)
4. Piso en Las Rozas (Madrid) por 116.956 € (-70%, +272.000 € margen)
"""
import asyncio
import base64
import os
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
import edge_tts
from playwright.async_api import async_playwright

BASE_DIR = Path("C:/Ideas/radar-alertas")
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

OUTPUT_DIR = BASE_DIR / "output"
TEMPLATES_DIR = BASE_DIR / "assets" / "templates"
SEMANA_DIR = OUTPUT_DIR / "semana_actual"
AUDIO_BEAT = OUTPUT_DIR / "pro_tension_beat.wav"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
SEMANA_DIR.mkdir(parents=True, exist_ok=True)

VOICE = "es-ES-AlvaroNeural"

def img_to_b64(path: Path) -> str:
    with open(path, "rb") as f:
        return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode('utf-8')}"

CHOLLOS_CONFIG = {
    "01_LUNES_SUV_Mazda_CX5": {
        "output_filename": "01_LUNES_SUV_Mazda_CX5_1842eur.mp4",
        "bg_img": TEMPLATES_DIR / "vehiculo_coche_oficial.jpg",
        "hud_tag": "SUBASTA JUDICIAL DGT • BOE",
        "hud_meta": "📍 SUB-AT-2026-26R1586002021",
        "hero_tag": "SUV Y EMBARGOS DGT",
        "headline": "SUV Mazda CX-5 que Sale a Subasta por solo 1.842 €",
        "specs": ["🚘 SUV Mazda CX-5", "⛽ Motor SkyActiv", "🛣️ 65.000 km est.", "⚖️ Juzgado 1ª Instancia", "📅 Plazo Abierto Hoy"],
        "market_label": "VALORACIÓN MERCADO (COCHES.NET)",
        "market_price": "18.424 €",
        "market_sub": "Precio medio en portales de segunda mano y concesionarios",
        "boe_label": "PRECIO SALIDA SUBASTA BOE",
        "hero_target_price": "1.842 €",
        "hero_int_price": 1842,
        "discount": "-89%",
        "discount_int": 89,
        "clean_margin": "+16.582 €",
        "margin_int": 16582,
        "margin_quote": "“¡16.582 € DE MARGEN LIMPIO EN ESTE SUV!”",
        "legal_title": "AUDITORÍA DGT: 0,00 € DE CARGAS ANTERIORES",
        "legal_sub": "Mandamiento judicial de cancelación de precintos y multas",
        "audit_item1": "Estado: <span style='color:#4ade80;'>Libre de cargas anteriores</span>",
        "audit_item2": "Fianza 5%: <span style='color:#38bdf8;'>Retornable si no te lo adjudicas</span>",
        "guion": (
            "Atención si buscas cambiar de coche, porque acaba de publicarse en el BOE este SUV Mazda CX-5 tasado en más de dieciocho mil euros, por un precio de salida de tan solo mil ochocientos cuarenta y dos euros. "
            "En portales de ocasión este modelo supera los dieciocho mil euros. "
            "Son más de dieciséis mil quinientos euros de margen limpio, y el juzgado cancela cualquier embargo o precinto previo por mandamiento judicial. "
            "RadarAlertas escanea el BOE cada madrugada. "
            "Entra al enlace de mi perfil para acceder al explorador web interactivo, simular tu rentabilidad con la calculadora y unirte a nuestros canales de WhatsApp y Telegram."
        )
    },
    "02_MARTES_Piso_Madrid_Tielmes": {
        "output_filename": "02_MARTES_Piso_Madrid_Tielmes_13956eur.mp4",
        "bg_img": TEMPLATES_DIR / "barrio_pilar_aerea.jpg",
        "hud_tag": "SUBASTA JUDICIAL BOE • MADRID",
        "hud_meta": "📍 SUB-AT-2026-26R2886001502",
        "hero_tag": "INMUEBLES JUDICIALES MADRID",
        "headline": "Piso en Madrid que Sale al -90% por solo 13.956 €",
        "specs": ["📐 Vivienda en Madrid", "📍 Tielmes (Paseo Estación)", "🏢 Zona Residencial", "⚖️ Juzgado 1ª Instancia", "📅 Plazo Abierto Hoy"],
        "market_label": "VALOR TASACIÓN / IDEALISTA",
        "market_price": "139.557 €",
        "market_sub": "Valor oficial de tasación pericial del juzgado",
        "boe_label": "PRECIO SALIDA SUBASTA BOE",
        "hero_target_price": "13.956 €",
        "hero_int_price": 13956,
        "discount": "-90%",
        "discount_int": 90,
        "clean_margin": "+125.601 €",
        "margin_int": 125601,
        "margin_quote": "“HABLAMOS DE 125.000 € DE MARGEN LIMPIO”",
        "legal_title": "SEGURIDAD JURÍDICA ART. 674 LEC: 0 € DEUDAS",
        "legal_sub": "Cancelación de hipotecas y embargos anteriores por Decreto Judicial",
        "audit_item1": "Cargas: <span style='color:#4ade80;'>0,00 € Canceladas por Ley</span>",
        "audit_item2": "Fianza 5%: <span style='color:#38bdf8;'>Retornable por el Juzgado</span>",
        "guion": (
            "Fijaos en lo que acaba de publicar el BOE esta misma semana en la Comunidad de Madrid. "
            "Una vivienda tasada por el juzgado en ciento treinta y nueve mil quinientos euros, que sale a subasta judicial por tan solo trece mil novecientos cincuenta y seis euros. "
            "Es un descuento brutal del noventa por ciento. "
            "Y todas las deudas hipotecarias anteriores quedan canceladas a cero euros por decreto judicial según el artículo seiscientos setenta y cuatro de la Ley de Enjuiciamiento Civil. "
            "RadarAlertas escanea el BOE cada madrugada. "
            "Entra al enlace de mi perfil, simula el beneficio neto de esta subasta con la calculadora y accede gratis a nuestros canales de WhatsApp y Telegram."
        )
    },
    "03_MIERCOLES_Mercedes_Benz": {
        "output_filename": "03_MIERCOLES_Mercedes_Benz_802eur.mp4",
        "bg_img": TEMPLATES_DIR / "vehiculo_llaves_concesionario.jpg",
        "hud_tag": "SUBASTA JUDICIAL DGT • BOE",
        "hud_meta": "📍 SUB-AT-2026-26R1586002020",
        "hero_tag": "VEHÍCULOS Y EMBARGOS DGT",
        "headline": "Mercedes-Benz Clase B que Sale a Subasta por solo 802 €",
        "specs": ["🚘 Mercedes-Benz B 200 D", "⛽ Diésel 136 CV", "🔑 Con Llaves y Ficha", "⚖️ Depósito Judicial", "📅 Plazo Abierto Hoy"],
        "market_label": "VALORACIÓN MERCADO LIBRE",
        "market_price": "8.016 €",
        "market_sub": "Valor oficial de peritación en portal de vehículos",
        "boe_label": "PRECIO SALIDA SUBASTA BOE",
        "hero_target_price": "802 €",
        "hero_int_price": 802,
        "discount": "-89%",
        "discount_int": 89,
        "clean_margin": "+7.214 €",
        "margin_int": 7214,
        "margin_quote": "“UN MERCEDES POR MENOS DE 1.000 €”",
        "legal_title": "REGISTRO DGT: MANDAMIENTO DE CANCELACIÓN",
        "legal_sub": "Entrega con documentación oficial y precintos anulados",
        "audit_item1": "Precintos: <span style='color:#4ade80;'>0,00 € Cancelados por Mandamiento</span>",
        "audit_item2": "Fianza 5%: <span style='color:#38bdf8;'>Retornable si no ganas la puja</span>",
        "guion": (
            "¿Un Mercedes-Benz por menos de mil euros? Parece mentira pero está publicado ahora mismo en el portal de subastas del BOE. "
            "Un Mercedes Clase B doscientos diésel valorado en más de ocho mil euros, que sale con una puja inicial de tan solo ochocientos dos euros. "
            "Más de siete mil euros de margen directo y con cancelación de cargas y multas por mandamiento judicial. "
            "Cada madrugada se publican decenas de vehículos embargados y casi nadie sabe cómo pujar sin intermediarios. "
            "Entra al enlace de mi perfil para buscar por provincia en la web, descargar la guía en PDF y unirte a WhatsApp y Telegram."
        )
    },
    "04_JUEVES_Chollo_Las_Rozas": {
        "output_filename": "04_JUEVES_Chollo_Las_Rozas_Madrid.mp4",
        "bg_img": TEMPLATES_DIR / "fachada_edificio.jpg",
        "hud_tag": "SUBASTA JUDICIAL BOE • MADRID",
        "hud_meta": "📍 SUB-AT-2026-23R2886001483",
        "hero_tag": "OPORTUNIDADES DE ALTO VALOR",
        "headline": "Vivienda de 118 m² en Las Rozas con 272.000 € de Margen",
        "specs": ["📐 118 m² Construidos", "📍 Las Rozas de Madrid", "🏢 Zona Exclusiva", "⚖️ Juzgado 1ª Instancia", "📅 Plazo Abierto Hoy"],
        "market_label": "VALOR TASACIÓN JUDICIAL",
        "market_price": "389.855 €",
        "market_sub": "Precio de mercado en Calle Micenas según Idealista",
        "boe_label": "PRECIO SALIDA SUBASTA BOE",
        "hero_target_price": "116.956 €",
        "hero_int_price": 116956,
        "discount": "-70%",
        "discount_int": 70,
        "clean_margin": "+272.899 €",
        "margin_int": 272899,
        "margin_quote": "“¡MÁS DE 272.000 € DE MARGEN LIMPIO!”",
        "legal_title": "EXPEDIENTE AUDITADO: SIN CARGAS HIPOTECARIAS",
        "legal_sub": "Mandamiento judicial al Registro de la Propiedad según Art. 674 LEC",
        "audit_item1": "Cargas: <span style='color:#4ade80;'>0,00 € Canceladas por Decreto</span>",
        "audit_item2": "Fianza 5%: <span style='color:#38bdf8;'>Retornable si no te lo adjudicas</span>",
        "guion": (
            "Mirad esta oportunidad en una de las zonas más cotizadas de Madrid. "
            "Un inmueble de ciento dieciocho metros cuadrados en Las Rozas, tasado en casi cuatrocientos mil euros, que sale a subasta judicial por ciento dieciséis mil euros. "
            "Son más de doscientos setenta y dos mil euros de margen limpio frente a los precios de mercado. "
            "Y todas las cargas previas quedan anuladas por el juez según el artículo seiscientos setenta y cuatro de la Ley de Enjuiciamiento Civil. "
            "RadarAlertas rastrea el BOE cada madrugada para que encuentres estos inmuebles antes de que se entere todo el mundo. "
            "Entra al enlace de mi perfil, usa la calculadora de impuestos en la web y únete gratis a nuestros canales de WhatsApp y Telegram."
        )
    }
}

from src.video_generator.generar_pack_videos_promo import (
    build_service_card_html,
    build_platform_pitch_html
)

async def renderizar_chollo(key: str, cfg: dict, browser):
    print(f"\n🎬 Iniciando render: {key} ({cfg['output_filename']})...")
    
    # 1. Locución neural
    audio_path = OUTPUT_DIR / f"{key}_audio.mp3"
    tts = edge_tts.Communicate(text=cfg["guion"], voice=VOICE, rate="+6%")
    await tts.save(str(audio_path))

    cmd_dur = ["ffmpeg", "-i", str(audio_path), "-f", "null", "-"]
    res = subprocess.run(cmd_dur, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    duracion_real = 35.0
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            partes = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = partes.split(":")
            duracion_real = float(h) * 3600 + float(m) * 60 + float(s)
            break
    print(f"  ✓ Locución generada: {duracion_real:.2f} s")

    p_step1 = int(cfg["hero_int_price"] * 0.25)
    p_step2 = int(cfg["hero_int_price"] * 0.60)
    p_step3 = int(cfg["hero_int_price"] * 0.85)
    m_step1 = int(cfg["margin_int"] * 0.35)
    m_step2 = int(cfg["margin_int"] * 0.70)

    steps = [
        {"type": "prop", "dur": 0.25, "price": f"{p_step1:,} €".replace(",", "."), "disc": "-20%", "strike": "0%", "margin": "+0 €", "quote": "“BUSCANDO OPORTUNIDAD...”", "glow_boe": True},
        {"type": "prop", "dur": 0.25, "price": f"{p_step2:,} €".replace(",", "."), "disc": "-45%", "strike": "0%", "margin": "+0 €", "quote": "“ANALIZANDO EXPEDIENTE...”", "glow_boe": True},
        {"type": "prop", "dur": 0.25, "price": f"{p_step3:,} €".replace(",", "."), "disc": "-65%", "strike": "0%", "margin": "+0 €", "quote": "“CRUCE CON MERCADO...”", "glow_boe": True},
        {"type": "prop", "dur": 0.35, "price": cfg["hero_target_price"], "disc": cfg["discount"], "strike": "0%", "margin": "+0 €", "quote": "“¡OPORTUNIDAD DETECTADA!”", "glow_boe": True},
        {"type": "prop", "dur": 2.50, "price": cfg["hero_target_price"], "disc": cfg["discount"], "strike": "0%", "margin": "+0 €", "quote": cfg["margin_quote"], "glow_boe": True},
        {"type": "prop", "dur": 0.25, "price": cfg["hero_target_price"], "disc": cfg["discount"], "strike": "35%", "margin": "+0 €", "quote": cfg["margin_quote"], "glow_market": True},
        {"type": "prop", "dur": 0.25, "price": cfg["hero_target_price"], "disc": cfg["discount"], "strike": "75%", "margin": "+0 €", "quote": cfg["margin_quote"], "glow_market": True},
        {"type": "prop", "dur": 3.00, "price": cfg["hero_target_price"], "disc": cfg["discount"], "strike": "calc(100% + 16px)", "margin": "+0 €", "quote": cfg["margin_quote"], "glow_market": True},
        {"type": "prop", "dur": 0.30, "price": cfg["hero_target_price"], "disc": cfg["discount"], "strike": "calc(100% + 16px)", "margin": f"+{m_step1:,} €".replace(",", "."), "quote": "“CALCULANDO RENTABILIDAD...”"},
        {"type": "prop", "dur": 0.30, "price": cfg["hero_target_price"], "disc": cfg["discount"], "strike": "calc(100% + 16px)", "margin": f"+{m_step2:,} €".replace(",", "."), "quote": "“CALCULANDO RENTABILIDAD...”"},
        {"type": "prop", "dur": 0.30, "price": cfg["hero_target_price"], "disc": cfg["discount"], "strike": "calc(100% + 16px)", "margin": cfg["clean_margin"], "quote": cfg["margin_quote"]},
        {"type": "prop", "dur": 3.00, "price": cfg["hero_target_price"], "disc": cfg["discount"], "strike": "calc(100% + 16px)", "margin": cfg["clean_margin"], "quote": cfg["margin_quote"]},
        {"type": "prop", "dur": 6.50, "price": cfg["hero_target_price"], "disc": cfg["discount"], "strike": "calc(100% + 16px)", "margin": cfg["clean_margin"], "quote": cfg["margin_quote"], "glow_legal": True},
        {"type": "platform", "dur": 7.00, "glow_cta": False},
        {"type": "platform", "dur": 6.50, "glow_cta": True},
    ]

    duracion_base = sum(s["dur"] for s in steps)
    factor = duracion_real / duracion_base

    frames_sub_dir = OUTPUT_DIR / f"frames_{key}"
    frames_sub_dir.mkdir(parents=True, exist_ok=True)

    bg_uri_service = img_to_b64(cfg["bg_img"])
    bcn_bg_uri = img_to_b64(TEMPLATES_DIR / "barcelona_aerea.jpg")

    page = await browser.new_page(viewport={"width": 1080, "height": 1920})
    frame_files = []

    for idx, s in enumerate(steps, 1):
        if s["type"] == "prop":
            html = build_service_card_html(cfg, bg_uri_service, s)
        else:
            html = build_platform_pitch_html(bcn_bg_uri, glow_cta=s.get("glow_cta", False))

        await page.set_content(html, wait_until="networkidle")
        frame_png = frames_sub_dir / f"f_{idx:02d}.png"
        await page.screenshot(path=str(frame_png))
        frame_files.append((frame_png, s["dur"]))

    await page.close()

    clips = []
    for i, (f_path, dur) in enumerate(frame_files, 1):
        dur_adj = dur * factor
        clip_mp4 = frames_sub_dir / f"c_{i:02d}.mp4"
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

    # Copiar tanto a output/ como a semana_actual/
    ruta_salida_semana = SEMANA_DIR / cfg["output_filename"]
    
    cmd_audio = [
        "ffmpeg", "-y",
        "-i", str(raw_mp4),
        "-i", str(audio_path),
        "-i", str(AUDIO_BEAT),
        "-filter_complex",
        "[1:a]volume=1.0[vocal]; [2:a]volume=0.20[music]; [vocal][music]amix=inputs=2:duration=first:dropout_transition=2[aout]",
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(ruta_salida_semana)
    ]
    subprocess.run(cmd_audio, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    
    # Actualizar fecha y hora actual
    try:
        os.utime(ruta_salida_semana, None)
    except Exception:
        pass

    shutil.rmtree(frames_sub_dir, ignore_errors=True)
    if audio_path.exists():
        audio_path.unlink()

    print(f"  ✅ VÍDEO TERMINADO: {ruta_salida_semana.name} ({ruta_salida_semana.stat().st_size / 1024 / 1024:.1f} MB)")

async def main():
    print("=" * 60)
    print("🔥 GENERADOR DE VÍDEOS DE CHOLLOS REALES DE ESTA SEMANA (BOE)")
    print("=" * 60)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for key, cfg in CHOLLOS_CONFIG.items():
            await renderizar_chollo(key, cfg, browser)
        await browser.close()

    print("\n🎉 ¡TODOS LOS VÍDEOS REALES HAN SIDO RENDERIZADOS CON ÉXITO!")

if __name__ == "__main__":
    asyncio.run(main())
