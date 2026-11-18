"""
Módulo de Gestión de Espacio y Limpieza Automática de Disco para RadarAlertas.
Elimina archivos temporales de renderizado y purga automáticamente
vídeos y archivos de trabajo con más de 3 días de antigüedad.
"""
import os
import time
from pathlib import Path

BASE_ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = BASE_ROOT / "output"

def purgar_archivos_antiguos(dias: int = 3) -> dict:
    """
    Elimina cualquier archivo en output/ que tenga más de 'dias' días de antigüedad.
    Devuelve un diccionario con el total de archivos eliminados y MB liberados.
    """
    if not OUTPUT_DIR.exists():
        return {"borrados": 0, "mb_liberados": 0.0}

    ahora = time.time()
    segundos_limite = dias * 86400
    archivos_borrados = 0
    bytes_liberados = 0

    for archivo in OUTPUT_DIR.iterdir():
        if archivo.is_file():
            try:
                mtime = archivo.stat().st_mtime
                if (ahora - mtime) > segundos_limite:
                    tam = archivo.stat().st_size
                    archivo.unlink()
                    archivos_borrados += 1
                    bytes_liberados += tam
            except Exception as e:
                print(f"⚠️ No se pudo eliminar {archivo.name}: {e}")

    mb = bytes_liberados / (1024 * 1024)
    if archivos_borrados > 0:
        print(f"🧹 [Auto-Limpieza] Eliminados {archivos_borrados} archivos con más de {dias} días ({mb:.2f} MB liberados).")
    return {"borrados": archivos_borrados, "mb_liberados": mb}

def limpiar_temporales_render():
    """
    Elimina archivos temporales de trabajo de FFmpeg (clips intermedios, concatenaciones)
    para que solo queden los vídeos finales terminados y ahorrar disco al instante.
    """
    if not OUTPUT_DIR.exists():
        return

    patrones_temporales = [
        "clip_*.mp4",
        "video_*raw*.mp4",
        "concat*.txt",
        "*_audio.mp3",
        "*_sub.ass",
        "*_sub.srt",
        "browser_record.webm",
        "market_screen.webm"
    ]

    borrados = 0
    bytes_liberados = 0
    for patron in patrones_temporales:
        for f in OUTPUT_DIR.glob(patron):
            try:
                # Conservar solo los que NO sean el archivo FINAL
                if "FINAL" not in f.name:
                    tam = f.stat().st_size
                    f.unlink()
                    borrados += 1
                    bytes_liberados += tam
            except Exception:
                pass

    if borrados > 0:
        mb = bytes_liberados / (1024 * 1024)
        print(f"🗑️ [Limpieza Inmediata] Eliminados {borrados} archivos temporales de render ({mb:.2f} MB liberados).")

if __name__ == "__main__":
    limpiar_temporales_render()
    purgar_archivos_antiguos(dias=3)
