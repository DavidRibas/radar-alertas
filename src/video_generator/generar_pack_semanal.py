"""
Generador de Lote Semanal Automático de Vídeos (Batching):
Genera de una sola tacada los 5 a 7 vídeos de la semana para que no tengas que estar pendiente a diario.
Copia los vídeos con nombres ordenados en output/semana_actual/ y genera el archivo copys_semana.txt
con los textos y hashtags listos para copiar y pegar en Metricool o Buffer.
"""
import os
import shutil
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = BASE_DIR / "output"
SEMANA_DIR = OUTPUT_DIR / "semana_actual"
SEMANA_DIR.mkdir(parents=True, exist_ok=True)

def empaquetar_semana():
    print("=" * 60)
    print("📦 GENERADOR DE PACK SEMANAL DE CONTENIDO - RADARALERTAS")
    print("=" * 60)

    # 1. Definir los vídeos clave disponibles con ganchos virales de alto impacto
    catalogo = [
        {
            "dia": "01_LUNES_Subasta_Inmueble",
            "origen": OUTPUT_DIR / "subasta_tiktok_EARTH_PERFECTO.mp4",
            "titulo": "❌ Idealista: 260.000 € vs ✅ BOE: 75.000 € (Piso en Madrid)",
            "copy": (
                "❌ IDEALISTA: 260.000 € vs ✅ BOE: 75.000 €\n\n"
                "Subasta judicial en Madrid con un 65% de ahorro y cargas canceladas por Ley (Art. 674 LEC).\n"
                "📖 Descarga la Guía Práctica Oficial en PDF y entra al radar gratis en el enlace del perfil.\n\n"
                "📌 Pinned Comment: 'Te he dejado la Guía Oficial en PDF en el link de mi perfil para que aprendas a pujar sin cometer errores.'\n\n"
                "#subastasboe #idealista #inversioninmobiliaria #chollos #vivienda #madrid #espana"
            )
        },
        {
            "dia": "02_MARTES_Coche_Embargado",
            "origen": OUTPUT_DIR / "vehiculo_ULTRA_VISUAL.mp4",
            "titulo": "⚠️ NO compres coche usado antes de ver este embargo del BOE",
            "copy": (
                "⚠️ NO COMPRES COCHE USADO ANTES DE VER ESTO\n\n"
                "Turismos, SUV y furgonetas embargadas por juzgados y Seguridad Social desde 980 €.\n"
                "🚗 Descarga la Guía Oficial de Coches Embargados en el enlace de la bio.\n\n"
                "📌 Pinned Comment: 'Tienes la Guía de Coches Embargados paso a paso gratis en el link de mi perfil.'\n\n"
                "#coches #embargos #subastas #cochesdesegundamano #chollos #motor #dgt"
            )
        },
        {
            "dia": "03_MIERCOLES_Ayuda_Fondo_Perdido",
            "origen": OUTPUT_DIR / "ayuda_ULTRA_VISUAL_942802.mp4",
            "titulo": "💸 El Estado da hasta 20.000 € a fondo perdido y casi nadie lo pide",
            "copy": (
                "💸 EL ESTADO DA HASTA 20.000 € A FONDO PERDIDO\n\n"
                "Convocatoria oficial abierta en la Base de Datos Nacional de Subvenciones para autónomos y pymes.\n"
                "💰 Activa las alertas de dinero público gratis en el enlace de la bio.\n\n"
                "📌 Pinned Comment: 'El enlace directo a la sede electrónica oficial está en nuestro canal gratuito del perfil.'\n\n"
                "#ayudas #subvenciones #autonomos #emprendedores #dinero #negocios"
            )
        },
        {
            "dia": "04_JUEVES_Licitacion_Publica",
            "origen": OUTPUT_DIR / "licitacion_ULTRA_VISUAL.mp4",
            "titulo": "📑 Cómo facturar 15.000 € a la Administración Pública sin ser funcionario",
            "copy": (
                "📑 CONTRATOS MENORES DEL ESTADO ABIERTOS A AUTÓNOMOS\n\n"
                "Servicios, obras, mantenimiento y tecnología con cobro garantizado por el Estado.\n"
                "👉 Recibe los pliegos oficiales en el enlace de la bio.\n\n"
                "📌 Pinned Comment: 'Todos los pliegos en PDF oficiales están disponibles en el radar del perfil.'\n\n"
                "#licitaciones #contratospublicos #pymes #autonomos #empresas #boe"
            )
        },
        {
            "dia": "05_VIERNES_Empleo_Oposiciones",
            "origen": OUTPUT_DIR / "empleo_ULTRA_VISUAL.mp4",
            "titulo": "🚨 Bolsas urgentes y plazas del BOE con sueldo de +2.150 € al mes",
            "copy": (
                "🚨 PLAZAS URGENTES DEL BOE CON +2.150 € AL MES\n\n"
                "Nuevas convocatorias fijas y temporales con plazo de inscripción abierto hoy.\n"
                "💼 Consulta requisitos y resoluciones oficiales en el link del perfil.\n\n"
                "📌 Pinned Comment: 'Entra al canal gratuito en el enlace del perfil para ver las convocatorias de hoy.'\n\n"
                "#empleopublico #oposiciones #trabajo #empleo #sueldo #boe"
            )
        }
    ]

    archivo_copys = SEMANA_DIR / "copys_semana.txt"
    with open(archivo_copys, "w", encoding="utf-8") as f_out:
        f_out.write("============================================================\n")
        f_out.write("📱 CALENDARIO EDITORIAL Y COPYS SEMANALES - RADARALERTAS\n")
        f_out.write(f"Fecha de compilación: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        f_out.write("Subir 1 al día a las 18:00h en TikTok, Reels y Shorts con Metricool o a mano\n")
        f_out.write("============================================================\n\n")

        for item in catalogo:
            origen = item["origen"]
            dest_nombre = f"{item['dia']}.mp4"
            dest_path = SEMANA_DIR / dest_nombre

            if origen.exists():
                shutil.copy2(origen, dest_path)
                print(f"  ✅ Vídeo preparado: {dest_nombre} ({dest_path.stat().st_size / 1024 / 1024:.1f} MB)")
            else:
                print(f"  ⚠️ Archivo origen no encontrado: {origen.name}")

            f_out.write(f"--- {item['dia']} ---\n")
            f_out.write(f"Título: {item['titulo']}\n\n")
            f_out.write(f"Texto / Copy para publicar:\n{item['copy']}\n\n")
            f_out.write("Comentario fijado obligatorio:\n")
            f_out.write("👉 Acceso oficial y Guía en PDF gratis en el enlace de mi perfil: https://radar-alertas-bot.onrender.com\n")
            f_out.write("=" * 60 + "\n\n")

    print(f"\n🎉 ¡Pack Semanal Listo en: {SEMANA_DIR}!")
    print(f"📄 Consulta los textos listos para copiar en: {archivo_copys}")

if __name__ == "__main__":
    empaquetar_semana()
