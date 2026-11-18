"""
Extractor oficial de subastas de vehículos del BOE (subastas.boe.es).
Busca subastas activas de turismos, furgonetas, todoterrenos y motos embargados
por Juzgados, Seguridad Social y Ayuntamientos.
Extrae marca, modelo, matrícula, año, tasación, puja mínima y depósito.
"""
import re
import urllib.parse
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional

BOE_SEARCH_URL = "https://subastas.boe.es/subastas_ava.php"
BOE_BASE_URL = "https://subastas.boe.es/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

MARCAS_POPULARES = [
    "MERCEDES", "BMW", "AUDI", "VOLKSWAGEN", "SEAT", "RENAULT", "PEUGEOT",
    "CITROEN", "FORD", "TOYOTA", "OPEL", "NISSAN", "FIAT", "HYUNDAI", "KIA",
    "VOLVO", "PORSCHE", "TESLA", "JEEP", "LAND ROVER", "MAZDA", "SKODA",
    "HONDA", "MINI", "ALFA ROMEO", "SUZUKI", "MITSUBISHI", "DACIA", "CUPRA",
    "YAMAHA", "HONDA", "KAWASAKI", "DUCATI", "IVECO", "MAN", "SCANIA"
]

def limpiar_precio(texto_precio: str) -> float:
    """Convierte cadenas tipo '15.800,00 €' en float 15800.00."""
    if not texto_precio or "no consta" in texto_precio.lower():
        return 0.0
    limpio = re.sub(r"[^\d,]", "", texto_precio).replace(",", ".")
    try:
        return float(limpio)
    except ValueError:
        return 0.0

def extraer_marca_modelo(descripcion: str, marca_dada: str = "", modelo_dado: str = "") -> tuple:
    """Extrae o limpia la marca y el modelo a partir de los datos o de la descripción."""
    marca = marca_dada.strip().upper() if marca_dada else ""
    modelo = modelo_dado.strip().upper() if modelo_dado else ""

    if not marca:
        for m in MARCAS_POPULARES:
            if re.search(r"\b" + re.escape(m) + r"\b", descripcion, re.IGNORECASE):
                marca = m
                break

    if not modelo and marca:
        # Intentar buscar la palabra que sigue a la marca
        patron = re.compile(rf"\b{re.escape(marca)}\s+([A-Za-z0-9\.\-]+(?:\s+[A-Za-z0-9\.\-]+)?)", re.IGNORECASE)
        match = patron.search(descripcion)
        if match:
            modelo = match.group(1).strip().upper()

    if not marca and not modelo:
        # Si no se detecta marca conocida, usar la descripción resumida
        marca = "VEHÍCULO"
        modelo = descripcion[:30].strip()

    return marca, modelo

def buscar_subastas_vehiculos(provincia_cod: str = "", limite: int = 25) -> List[str]:
    """
    Busca subastas activas de vehículos (BIEN.TIPO = 'V') en el BOE.
    Si provincia_cod = '', busca en toda España.
    """
    data = {
        "campo[0]": "SUBASTA.ORIGEN", "dato[0]": "",
        "campo[2]": "SUBASTA.ESTADO.CODIGO", "dato[2]": "EJ", # En celebración
        "campo[3]": "BIEN.TIPO", "dato[3]": "V",              # Vehículos
        "page_hits": str(limite),
        "sort_field[0]": "SUBASTA.FECHA_FIN",
        "sort_order[0]": "asc",
        "accion": "Buscar"
    }
    if provincia_cod:
        data["campo[8]"] = "BIEN.COD_PROVINCIA"
        data["dato[8]"] = provincia_cod

    try:
        r = requests.post(BOE_SEARCH_URL, headers=HEADERS, data=data, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print(f"❌ Error al conectar con subastas.boe.es (Vehículos): {e}")
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    items = soup.find_all("li", class_="resultado-busqueda")
    print(f"🔍 Encontradas {len(items)} subastas de vehículos activas en el BOE.")

    subastas = []
    for item in items[:limite]:
        link_tag = item.find("a", href=lambda x: x and "idSub=" in x)
        if not link_tag:
            continue
        href = link_tag.get("href")
        m = re.search(r"idSub=([A-Z0-9\-]+)", href)
        if not m:
            continue
        id_sub = m.group(1)
        subastas.append(id_sub)

    return subastas

def obtener_detalle_vehiculo(id_subasta: str) -> Optional[Dict]:
    """Extrae la información general y los datos del vehículo (pestaña 1 y 3)."""
    # 1. Pestaña 1: Información General
    url_gen = f"https://subastas.boe.es/detalleSubasta.php?idSub={id_subasta}&ver=1"
    try:
        r_gen = requests.get(url_gen, headers=HEADERS, timeout=12)
        soup_gen = BeautifulSoup(r_gen.text, "html.parser")
    except Exception as e:
        print(f"❌ Error al leer general de {id_subasta}: {e}")
        return None

    datos_gen = {}
    for tr in soup_gen.find_all("tr"):
        th, td = tr.find("th"), tr.find("td")
        if th and td:
            datos_gen[th.text.strip().lower()] = td.text.strip()

    # 2. Pestaña 3: Bienes (Vehículo)
    url_bien = f"https://subastas.boe.es/detalleSubasta.php?idSub={id_subasta}&ver=3"
    try:
        r_bien = requests.get(url_bien, headers=HEADERS, timeout=12)
        soup_bien = BeautifulSoup(r_bien.text, "html.parser")
    except Exception as e:
        print(f"❌ Error al leer bien de {id_subasta}: {e}")
        return None

    datos_bien = {}
    for tr in soup_bien.find_all("tr"):
        th, td = tr.find("th"), tr.find("td")
        if th and td:
            datos_bien[th.text.strip().lower()] = td.text.strip()

    # Si no hay datos en pestaña 3, intentar buscar texto en el cuerpo
    desc_raw = datos_bien.get("descripción", "")
    if not desc_raw:
        # Fallback a texto general
        desc_raw = datos_gen.get("descripción", id_subasta)

    marca_raw = datos_bien.get("marca", "")
    modelo_raw = datos_bien.get("modelo", "")
    marca, modelo = extraer_marca_modelo(desc_raw, marca_raw, modelo_raw)

    matricula = datos_bien.get("matrícula", "No consta")
    bastidor = datos_bien.get("número de bastidor", "No consta")
    fecha_mat = datos_bien.get("fecha de matriculación", "No consta")
    provincia = datos_bien.get("provincia", "España")
    deposito_lugar = datos_bien.get("depósito", "Depósito judicial")
    visitable = datos_bien.get("visitable", "Consultar")
    cargas = datos_bien.get("cargas", "Sin cargas preferentes conocidas")

    # Precios
    valor_subasta_str = datos_bien.get("valor subasta") or datos_gen.get("valor subasta", "0 €")
    tasacion_str = datos_bien.get("valor de tasación") or datos_gen.get("tasación", "0 €")
    puja_min_str = datos_bien.get("puja mínima") or datos_gen.get("puja mínima", "0 €")
    deposito_str = datos_bien.get("importe del depósito") or datos_gen.get("importe del depósito", "0 €")

    valor_subasta = limpiar_precio(valor_subasta_str)
    tasacion = limpiar_precio(tasacion_str)
    puja_min = limpiar_precio(puja_min_str)
    deposito = limpiar_precio(deposito_str)

    valor_referencia = max(valor_subasta, tasacion)
    precio_salida = puja_min if puja_min > 0 else (valor_referencia * 0.5 if valor_referencia > 0 else 500.0)

    ahorro_pct = 0
    if valor_referencia > 0 and precio_salida > 0 and valor_referencia > precio_salida:
        ahorro_pct = int(((valor_referencia - precio_salida) / valor_referencia) * 100)

    # Título comercial de impacto
    titulo_comercial = f"{marca} {modelo}".strip()
    if not titulo_comercial or titulo_comercial == "VEHÍCULO":
        titulo_comercial = desc_raw[:45]

    # URL Google Maps al depósito judicial
    lugar_busqueda = deposito_lugar if len(deposito_lugar) > 5 and "judicial" not in deposito_lugar.lower() else f"Depósito vehículos {provincia}"
    query_maps = urllib.parse.quote_plus(f"{lugar_busqueda}, España")
    url_maps = f"https://www.google.com/maps/search/?api=1&query={query_maps}"

    # Score de Oportunidad RadarAlertas (1 a 10)
    score = 5.0
    if ahorro_pct >= 60:
        score += 3.0
    elif ahorro_pct >= 40:
        score += 2.0
    elif ahorro_pct >= 20:
        score += 1.0

    if marca and marca.upper() in ["MERCEDES", "BMW", "AUDI", "VOLKSWAGEN", "TOYOTA"]:
        score += 1.0

    if matricula and len(matricula) >= 6 and "no consta" not in matricula.lower():
        score += 0.5

    if "si" in visitable.lower():
        score += 0.5

    score = min(9.9, max(1.0, round(score, 1)))
    if score >= 8.5:
        score_badge = f"⭐ {score}/10 (Oportunidad Oro 🏆)"
    elif score >= 7.0:
        score_badge = f"⭐ {score}/10 (Oportunidad Plata 🥈)"
    else:
        score_badge = f"⭐ {score}/10 (Oportunidad Interesante)"

    return {
        "id_subasta": id_subasta,
        "titulo": titulo_comercial,
        "marca": marca,
        "modelo": modelo,
        "matricula": matricula,
        "bastidor": bastidor,
        "fecha_matriculacion": fecha_mat,
        "provincia": provincia,
        "deposito_lugar": deposito_lugar,
        "url_maps": url_maps,
        "score_oportunidad": score,
        "score_badge": score_badge,
        "visitable": visitable,
        "cargas": cargas[:250],
        "descripcion": desc_raw[:300],
        "valor_referencia": valor_referencia,
        "valor_referencia_formato": f"{valor_referencia:,.0f} €".replace(",", "."),
        "precio_salida": precio_salida,
        "precio_salida_formato": f"{precio_salida:,.0f} €".replace(",", "."),
        "ahorro_porcentaje": ahorro_pct,
        "deposito": f"{deposito:,.0f} €".replace(",", "."),
        "fecha_fin": datos_gen.get("fecha de conclusión", "Consultar en portal"),
        "url_oficial": url_gen
    }

def filtrar_mejores_vehiculos(ids_subastas: List[str], max_resultados: int = 5) -> List[Dict]:
    """Analiza las subastas de vehículos y devuelve las que tienen mejor descuento o marcas atractivas."""
    vehiculos = []
    print("⏳ Analizando expedientes de vehículos en el BOE...")
    for id_sub in ids_subastas:
        detalle = obtener_detalle_vehiculo(id_sub)
        if not detalle:
            continue

        # Descartar lotes vacíos o sin valor
        if detalle["valor_referencia"] < 300 and detalle["precio_salida"] < 300:
            continue

        vehiculos.append(detalle)
        print(f"  🚗 VEHÍCULO DETECTADO [{detalle['id_subasta']}]: {detalle['titulo']} ({detalle['provincia']}) | Val: {detalle['valor_referencia_formato']} -> Salida: {detalle['precio_salida_formato']} (-{detalle['ahorro_porcentaje']}%)")

        if len(vehiculos) >= max_resultados:
            break

    # Ordenar por ahorro y valor
    vehiculos.sort(key=lambda x: (x["ahorro_porcentaje"], x["valor_referencia"]), reverse=True)
    return vehiculos

if __name__ == "__main__":
    ids = buscar_subastas_vehiculos(limite=10)
    top = filtrar_mejores_vehiculos(ids, max_resultados=3)
    for v in top:
        print("\n---")
        print(v["titulo"], "|", v["matricula"], "|", v["provincia"])
        print(f"Salida: {v['precio_salida_formato']} (Tasación: {v['valor_referencia_formato']}, Ahorro: {v['ahorro_porcentaje']}%)")
