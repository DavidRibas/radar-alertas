import asyncio
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.video_generator.generador_visual_empleo import generar_video_empleo_visual
SEMANA_DIR = BASE_DIR / "output" / "semana_actual"
SEMANA_DIR.mkdir(parents=True, exist_ok=True)

CONVOCATORIAS = [
    {
        "id_convocatoria": "BOE-DEFENSA-2150",
        "organismo": "Ministerio de Defensa",
        "titulo": "Plazas y Bolsas de Empleo del Ministerio de Defensa",
        "sueldo": "+2.150 € / MES",
        "pagas": "14 PAGAS • EMPLEO PARA TODA LA VIDA",
        "plazas": "BOLSAS DE EMPLEO Y PLAZAS FIJAS",
        "requisito_estudios": "Desde Graduado Escolar o ESO",
        "requisito_tipo": "Bolsas de Empleo Temporal y Fijo",
        "salida": SEMANA_DIR / "06_SABADO_Empleo_Defensa_2150eur.mp4"
    },
    {
        "id_convocatoria": "BOE-HACIENDA-2350",
        "organismo": "Ministerio de Hacienda",
        "titulo": "Bolsas de Empleo y Plazas del Ministerio de Hacienda",
        "sueldo": "+2.350 € / MES",
        "pagas": "14 PAGAS • EMPLEO PÚBLICO FIJO",
        "plazas": "CONVOCATORIA Y BOLSAS ABIERTAS",
        "requisito_estudios": "Bachillerato o Equivalente",
        "requisito_tipo": "Incorporación Rápida por Bolsas",
        "salida": SEMANA_DIR / "07_DOMINGO_Empleo_Hacienda_2350eur.mp4"
    }
]

async def main():
    print("🚀 Generando los 2 nuevos vídeos virales de Empleo Público para el fin de semana...")
    for conv in CONVOCATORIAS:
        print(f"\n🎬 Procesando: {conv['titulo']}...")
        await generar_video_empleo_visual(conv, conv["salida"])
        print(f"✅ Generado con éxito: {conv['salida'].name}")

    print("\n🎉 ¡Pack de Fin de Semana completado!")

if __name__ == "__main__":
    asyncio.run(main())
