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

    # 1. Definir los vídeos clave disponibles
    catalogo = [
        {
            "dia": "01_LUNES_Subasta_Inmueble",
            "origen": OUTPUT_DIR / "subasta_tiktok_EARTH_PERFECTO.mp4",
            "titulo": "🚨 Subasta Judicial en Madrid: Piso tasado con -65% de descuento",
            "copy": (
                "🚨 SUBASTA JUDICIAL EN EL BOE\n"
                "Inmueble verificado con cargas canceladas según Art. 674 LEC.\n"
                "👉 Descarga la Guía Gratuita y entra al Radar en el enlace de la bio.\n\n"
                "#subastasboe #inversioninmobiliaria #chollos #vivienda #madrid"
            )
        },
        {
            "dia": "02_MARTES_Coche_Embargado",
            "origen": OUTPUT_DIR / "vehiculo_ULTRA_VISUAL.mp4",
            "titulo": "🚗 Coche Embargado por el Estado desde 980 €",
            "copy": (
                "🚗 COCHES Y VEHÍCULOS EMBARGADOS POR EL ESTADO\n"
                "Salidas públicas en el portal del BOE desde solo 980 €.\n"
                "👉 Consulta todos los lotes y depósitos en el enlace de la bio.\n\n"
                "#coches #embargos #subastas #oportunidad #motor"
            )
        },
        {
            "dia": "03_MIERCOLES_Ayuda_Fondo_Perdido",
            "origen": OUTPUT_DIR / "ayuda_ULTRA_VISUAL_942802.mp4",
            "titulo": "💰 Subvención a Fondo Perdido aprobada en el BDNS",
            "copy": (
                "💰 AYUDAS Y SUBVENCIONES OFICIALES\n"
                "Fondos públicos abiertos para autónomos, pymes y particulares.\n"
                "👉 Recibe avisos directos en Telegram desde el enlace de la bio.\n\n"
                "#ayudas #subvenciones #autonomos #emprendedores #dinero"
            )
        },
        {
            "dia": "04_JUEVES_Licitacion_Publica",
            "origen": OUTPUT_DIR / "licitacion_ULTRA_VISUAL.mp4",
            "titulo": "📑 Contrato Público del Estado: Oportunidad para profesionales",
            "copy": (
                "📑 LICITACIONES Y CONTRATOS MENORES DEL ESTADO\n"
                "Obras, suministros y servicios públicos sin intermediarios.\n"
                "👉 Toda la información en el enlace de la bio.\n\n"
                "#licitaciones #contratospublicos #empresas #negocios #boe"
            )
        },
        {
            "dia": "05_VIERNES_Empleo_Oposiciones",
            "origen": OUTPUT_DIR / "empleo_ULTRA_VISUAL.mp4",
            "titulo": "💼 Plazas Urgentes de Empleo Público en el BOE",
            "copy": (
                "💼 EMPLEO PÚBLICO Y BOLSAS DE TRABAJO\n"
                "Nuevas plazas convocadas hoy en el Boletín Oficial del Estado.\n"
                "👉 Enlace en la bio para ver requisitos y plazos de inscripción.\n\n"
                "#empleopublico #oposiciones #trabajo #empleo #boe"
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
