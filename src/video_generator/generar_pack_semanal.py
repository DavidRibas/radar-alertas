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

    # Limpiar archivos antiguos del directorio semanal para evitar mezclas
    for old_file in SEMANA_DIR.glob("*.mp4"):
        try:
            old_file.unlink()
        except Exception:
            pass

    # 1. Definir los vídeos clave disponibles con ganchos virales de alto impacto (DISEÑO STITCH HD DEFINITIVO)
    catalogo = [
        {
            "dia": "01_LUNES_Piso_Barcelona_Eixample",
            "origen": OUTPUT_DIR / "VIDEO_BARCELONA_Y_RADARALERTAS_PROMO.mp4",
            "titulo": "❌ Idealista: 340.000 € vs ✅ BOE: 54.000 € (Piso en Barcelona Eixample)",
            "copy": (
                "❌ IDEALISTA: 340.000 € vs ✅ BOE: 54.000 €\n\n"
                "Piso de 85 m² en pleno Eixample de Barcelona publicado en el BOE.\n"
                "🛡️ 0,00 € de deudas anteriores canceladas por Decreto Judicial (Art. 674 LEC) y fianza 5% retornable.\n\n"
                "🌐 Prueba el Buscador y la Calculadora de Rentabilidad oficial gratis en el enlace de mi perfil:\n"
                "👉 https://radaralertas.com\n\n"
                "📌 Pinned Comment: 'Te he dejado el enlace al buscador oficial con simulador de impuestos y la Guía en PDF gratis en el link de mi perfil.'\n\n"
                "#subastasboe #idealista #barcelona #inmobiliaria #inversion #chollos #vivienda"
            )
        },
        {
            "dia": "02_MARTES_Coche_BMW_DGT",
            "origen": OUTPUT_DIR / "VIDEO_VEHICULOS_PROMO.mp4",
            "titulo": "⚠️ NO compres coche usado antes de ver este embargo del BOE (BMW por 4.800 €)",
            "copy": (
                "⚠️ NO COMPRES COCHE USADO ANTES DE VER ESTO\n\n"
                "BMW Serie 3 Berlina (Año 2021) automático con 68.000 km que sale a subasta judicial por 4.800 €.\n"
                "En portales de ocasión está en 24.500 € (-80% de ahorro). Precintos y multas canceladas por Mandamiento Judicial.\n\n"
                "🚗 Accede al buscador y descarga la Guía Oficial de Vehículos Embargados en el link de la bio:\n"
                "👉 https://radaralertas.com\n\n"
                "📌 Pinned Comment: 'Tienes el buscador de vehículos y la Guía de Coches Embargados paso a paso gratis en el link de mi perfil.'\n\n"
                "#coches #embargos #subastas #bmw #cochessegundamano #chollos #dgt #motor"
            )
        },
        {
            "dia": "03_MIERCOLES_Ayudas_Fondo_Perdido",
            "origen": OUTPUT_DIR / "VIDEO_AYUDAS_PROMO.mp4",
            "titulo": "💸 Hasta 12.000 € a fondo perdido para Autónomos y Pymes (BDNS)",
            "copy": (
                "💸 EL ESTADO DA HASTA 12.000 € A FONDO PERDIDO\n\n"
                "Nueva partida oficial en la Base de Datos Nacional de Subvenciones con fondos europeos.\n"
                "Sin devolución y sin intereses bancarios. Para autónomos y micropymes.\n\n"
                "💰 Consulta la convocatoria abierta y los requisitos oficiales en el radar gratuito:\n"
                "👉 https://radaralertas.com\n\n"
                "📌 Pinned Comment: 'El enlace directo a la sede electrónica y el filtro de ayudas está en el buscador de mi perfil.'\n\n"
                "#ayudas #subvenciones #autonomos #pymes #emprendedores #dinero #negocios"
            )
        },
        {
            "dia": "04_JUEVES_Licitacion_Publica",
            "origen": OUTPUT_DIR / "VIDEO_LICITACIONES_PROMO.mp4",
            "titulo": "📑 Cómo facturar 42.000 € a la Administración Pública sin ser gran empresa",
            "copy": (
                "📑 CONTRATO MENOR DE 42.000 € ABIERTO A PYMES Y AUTÓNOMOS\n\n"
                "Mantenimiento, servicios y suministros del sector público.\n"
                "Sin avales bancarios gigantescos y con cobro garantizado por Ley a 30 días.\n\n"
                "👉 Filtra contratos menores de tu provincia en el link del perfil:\n"
                "👉 https://radaralertas.com\n\n"
                "📌 Pinned Comment: 'Todos los pliegos técnicos oficiales disponibles en el radar del perfil.'\n\n"
                "#licitaciones #contratospublicos #pymes #autonomos #empresas #boe"
            )
        },
        {
            "dia": "05_VIERNES_Subasta_Inmueble_Madrid",
            "origen": OUTPUT_DIR / "VIDEO_BARCELONA_HD_DINAMICO.mp4",
            "titulo": "🏢 Oportunidad Judicial: Cómo auditar un piso del BOE antes de pujar",
            "copy": (
                "🏢 CÓMO AUDITAR UN PISO DEL BOE ANTES DE PUJAR\n\n"
                "Antes de meter un solo euro, simula el ITP autonómico, aranceles registrales y cargas con la calculadora interactiva.\n"
                "Descubre cómo cazar inmuebles con hasta un 84% de descuento de forma 100% legal.\n\n"
                "🧮 Simula tu operación con la Calculadora Oficial en el link de la bio:\n"
                "👉 https://radaralertas.com\n\n"
                "📌 Pinned Comment: 'Calculadora de rentabilidad e impuestos de subastas gratis en el link de mi perfil.'\n\n"
                "#inversioninmobiliaria #subastasjudiciales #boe #vivienda #proptech #finanzas"
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
                shutil.copyfile(origen, dest_path)
                try:
                    os.utime(dest_path, None)
                except Exception:
                    pass
                print(f"  ✅ Vídeo preparado: {dest_nombre} ({dest_path.stat().st_size / 1024 / 1024:.1f} MB)")
            else:
                print(f"  ⚠️ Archivo origen no encontrado: {origen.name}")

            f_out.write(f"--- {item['dia']} ---\n")
            f_out.write(f"Título: {item['titulo']}\n\n")
            f_out.write(f"Texto / Copy para publicar:\n{item['copy']}\n\n")
            f_out.write("Comentario fijado obligatorio:\n")
            f_out.write("👉 Acceso oficial y Guía en PDF gratis en el enlace de mi perfil: https://radaralertas.com\n")
            f_out.write("=" * 60 + "\n\n")

    print(f"\n🎉 ¡Pack Semanal Listo en: {SEMANA_DIR}!")
    print(f"📄 Consulta los textos listos para copiar en: {archivo_copys}")

if __name__ == "__main__":
    empaquetar_semana()
