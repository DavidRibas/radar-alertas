"""
Generador del Boletín Express Matutino en Audio (Voice Note Telegram):
Sintetiza un resumen ejecutivo de 40-50 segundos con las principales oportunidades
del día en Inmuebles, Vehículos y Subvenciones del Estado.
Utiliza Microsoft Edge Neural TTS (voz ultra-realista sin coste 0,00 €).
"""
import os
import asyncio
import datetime
from pathlib import Path
from typing import Optional, Dict, List
import edge_tts

from src.extractores.boe_inmuebles import buscar_subastas_inmuebles, obtener_detalle_subasta
from src.extractores.boe_vehiculos import buscar_subastas_vehiculos, obtener_detalle_vehiculo
from src.extractores.ayudas_subvenciones import obtener_convocatorias_recientes, filtrar_mejores_ayudas

BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = BASE_DIR / "output" / "audios"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Voces recomendadas en castellano de alta fidelidad:
# es-ES-AlvaroNeural (Masculina, ejecutiva y enérgica)
# es-ES-ElviraNeural (Femenina, institucional y clara)
VOZ_PREDETERMINADA = "es-ES-AlvaroNeural"

def redactar_guion_matutino(
    inmueble: Optional[Dict] = None,
    vehiculo: Optional[Dict] = None,
    ayuda: Optional[Dict] = None,
    fecha_str: Optional[str] = None
) -> str:
    """Redacta un texto optimizado para locución natural de ~45 segundos."""
    if not fecha_str:
        hoy = datetime.date.today()
        dias_semana = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        fecha_str = f"{dias_semana[hoy.weekday()]}, {hoy.day} de {meses[hoy.month - 1]}"

    guion = f"¡Buenos días! Hoy es {fecha_str}. Este es el Boletín Express de RadarAlertas con las oportunidades más destacadas del Boletín Oficial del Estado. "

    if inmueble:
        loc = inmueble.get("localidad", "Madrid")
        tasacion = inmueble.get("valor_referencia_formato", "180.000 euros")
        salida = inmueble.get("precio_salida_formato", "85.000 euros")
        ahorro = inmueble.get("ahorro_porcentaje", 50)
        guion += f"En subastas inmobiliarias, se ha publicado una vivienda en {loc}, tasada oficialmente en {tasacion}, con un precio de salida de {salida}, lo que supone un descuento del {ahorro}%. "
    else:
        guion += "En el mercado inmobiliario, el BOE abre hoy varias subastas residenciales libres de cargas con importantes descuentos sobre tasación. "

    if vehiculo:
        nombre_v = vehiculo.get("vehiculo_formato", "vehículo")
        salida_v = vehiculo.get("precio_salida_formato", "1.500 euros")
        guion += f"En la sección de motor, detectado un {nombre_v} en depósito judicial con un precio inicial de {salida_v}. "
    else:
        guion += "En vehículos embargados, nuevas furgonetas y turismos disponibles para puja telemática con depósito legal reembolsable. "

    if ayuda:
        titulo_ayuda = ayuda.get("titulo", "ayudas a fondo perdido")[:50]
        presupuesto = ayuda.get("presupuesto_formato", "fondos públicos")
        guion += f"Y en subvenciones públicas, convocatoria activa con una partida de {presupuesto} para {titulo_ayuda}. "

    guion += (
        "Tienes todos los expedientes directos, enlaces a Street View, informes catastrales y deudas verificadas "
        "en nuestros canales VIP de Telegram. ¡Mucho éxito en tus operaciones y feliz jornada!"
    )
    return guion

async def generar_audio_boletin(
    texto: str,
    archivo_salida: Optional[Path] = None,
    voz: str = VOZ_PREDETERMINADA
) -> Path:
    """Convierte el guión en un archivo de audio MP3 usando Edge-TTS."""
    if not archivo_salida:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo_salida = OUTPUT_DIR / f"Boletin_RadarAlertas_{timestamp}.mp3"

    print(f"🎙️ Generando locución neural con voz '{voz}'...")
    comunicador = edge_tts.Communicate(texto, voz, rate="+5%", pitch="+0Hz")
    await comunicador.save(str(archivo_salida))
    print(f"✅ Audio generado con éxito en: {archivo_salida} ({archivo_salida.stat().st_size / 1024:.1f} KB)")
    return archivo_salida

async def compilar_boletin_diario(fecha_str: Optional[str] = None) -> Path:
    """Función de alto nivel: extrae datos en vivo, redacta y genera el audio."""
    print("📡 Obteniendo datos destacados del BOE para el Boletín Express...")
    
    inmueble_top = None
    try:
        subastas = buscar_subastas_inmuebles(provincia_cod="28", limite=5)
        for s_id in subastas:
            det = obtener_detalle_subasta(s_id)
            if det and det.get("ahorro_porcentaje", 0) >= 30:
                inmueble_top = det
                break
    except Exception as e:
        print(f"Nota: No se pudo obtener inmueble top en vivo: {e}")

    vehiculo_top = None
    try:
        sub_v = buscar_subastas_vehiculos(provincia_cod="", limite=5)
        for vid in sub_v:
            det_v = obtener_detalle_vehiculo(vid)
            if det_v and det_v.get("precio_salida", 0) > 0:
                vehiculo_top = det_v
                break
    except Exception as e:
        print(f"Nota: No se pudo obtener vehículo top en vivo: {e}")

    ayuda_top = None
    try:
        convs = obtener_convocatorias_recientes(max_paginas=1)
        ayudas = filtrar_mejores_ayudas(convs, max_resultados=2)
        if ayudas:
            ayuda_top = ayudas[0]
    except Exception as e:
        print(f"Nota: No se pudo obtener ayuda top en vivo: {e}")

    guion = redactar_guion_matutino(
        inmueble=inmueble_top,
        vehiculo=vehiculo_top,
        ayuda=ayuda_top,
        fecha_str=fecha_str
    )

    print("\n📝 Guión redactado:")
    print("-" * 50)
    print(guion)
    print("-" * 50)

    audio_path = await generar_audio_boletin(guion)
    return audio_path

if __name__ == "__main__":
    asyncio.run(compilar_boletin_diario())
