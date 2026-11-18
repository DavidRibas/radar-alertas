"""
Extractor oficial de subastas de inmuebles del BOE (subastas.boe.es).
Busca subastas activas, extrae dirección, tasación, puja mínima, referencia catastral y calcula el score de oportunidad.
"""
import re
import urllib.parse
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from datetime import datetime, timedelta

def generar_enlace_google_calendar(titulo: str, fecha_fin_str: str, direccion: str, id_subasta: str, url_oficial: str) -> str:
    """Genera un enlace de 1 clic para añadir la fecha de cierre de la subasta a Google Calendar con alarma."""
    end_dt = None
    m_iso = re.search(r"(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})", fecha_fin_str)
    if m_iso:
        y, mo, d, h, mi, s = map(int, m_iso.groups())
        end_dt = datetime(y, mo, d, h, mi, s)
    else:
        m_es = re.search(r"(\d{2})-(\d{2})-(\d{4})\s+(\d{2}):(\d{2})", fecha_fin_str)
        if m_es:
            d, mo, y, h, mi = map(int, m_es.groups())
            end_dt = datetime(y, mo, d, h, mi, 0)

    if not end_dt:
        end_dt = datetime.now() + timedelta(days=7, hours=18)

    start_dt = end_dt - timedelta(hours=2)
    fmt = "%Y%m%dT%H%M%SZ"
    dates_param = f"{start_dt.strftime(fmt)}/{end_dt.strftime(fmt)}"

    t_enc = urllib.parse.quote_plus(f"⏰ Cierre Subasta BOE: {titulo[:35]}")
    d_enc = urllib.parse.quote_plus(f"Subasta Judicial en el BOE.\nExpediente: {id_subasta}\n👉 Enlace para pujar: {url_oficial}")
    loc_enc = urllib.parse.quote_plus(direccion or "España")

    return f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={t_enc}&dates={dates_param}&details={d_enc}&location={loc_enc}"

BOE_SEARCH_URL = "https://subastas.boe.es/subastas_ava.php"
BOE_BASE_URL = "https://subastas.boe.es/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

def limpiar_precio(texto_precio: str) -> float:
    """Convierte cadenas tipo '158.037,39 €' en float 158037.39."""
    if not texto_precio or "no consta" in texto_precio.lower():
        return 0.0
    limpio = re.sub(r"[^\d,]", "", texto_precio).replace(",", ".")
    try:
        return float(limpio)
    except ValueError:
        return 0.0

def buscar_subastas_inmuebles(provincia_cod: str = "28", limite: int = 15) -> List[Dict]:
    """
    Busca subastas activas de inmuebles en la provincia especificada (28 = Madrid, 08 = Barcelona, etc.).
    Si provincia_cod = '', busca en toda España.
    """
    data = {
        "campo[0]": "SUBASTA.ORIGEN", "dato[0]": "",
        "campo[2]": "SUBASTA.ESTADO.CODIGO", "dato[2]": "EJ", # En celebración (abiertas)
        "campo[3]": "BIEN.TIPO", "dato[3]": "I",              # Inmuebles
        "campo[8]": "BIEN.COD_PROVINCIA", "dato[8]": provincia_cod,
        "page_hits": str(limite),
        "sort_field[0]": "SUBASTA.FECHA_FIN",
        "sort_order[0]": "asc",
        "accion": "Buscar"
    }

    try:
        r = requests.post(BOE_SEARCH_URL, headers=HEADERS, data=data, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print(f"❌ Error al conectar con subastas.boe.es: {e}")
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    items = soup.find_all("li", class_="resultado-busqueda")
    print(f"🔍 Encontradas {len(items)} subastas activas en el BOE.")

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

def obtener_detalle_subasta(id_subasta: str) -> Optional[Dict]:
    """Extrae la información general y los datos del inmueble (pestaña 1 y pestaña 3)."""
    # 1. Pestaña 1: Información General
    url_gen = f"https://subastas.boe.es/detalleSubasta.php?idSub={id_subasta}&ver=1"
    try:
        r_gen = requests.get(url_gen, headers=HEADERS, timeout=12)
        soup_gen = BeautifulSoup(r_gen.text, "html.parser")
    except Exception as e:
        print(f"❌ Error al leer información general de {id_subasta}: {e}")
        return None

    datos_gen = {}
    for tr in soup_gen.find_all("tr"):
        th, td = tr.find("th"), tr.find("td")
        if th and td:
            datos_gen[th.text.strip().lower()] = td.text.strip()

    # 2. Pestaña 3: Bienes y Lotes
    url_bien = f"https://subastas.boe.es/detalleSubasta.php?idSub={id_subasta}&ver=3"
    try:
        r_bien = requests.get(url_bien, headers=HEADERS, timeout=12)
        soup_bien = BeautifulSoup(r_bien.text, "html.parser")
    except Exception as e:
        print(f"❌ Error al leer bienes de {id_subasta}: {e}")
        return None

    datos_bien = {}
    for tr in soup_bien.find_all("tr"):
        th, td = tr.find("th"), tr.find("td")
        if th and td:
            datos_bien[th.text.strip().lower()] = td.text.strip()

    # Consolidar datos
    valor_subasta_str = datos_bien.get("valor subasta") or datos_gen.get("valor subasta", "0 €")
    tasacion_str = datos_bien.get("valor de tasación") or datos_gen.get("tasación", "0 €")
    puja_min_str = datos_bien.get("puja mínima") or datos_gen.get("puja mínima", "0 €")
    deposito_str = datos_bien.get("importe del depósito") or datos_gen.get("importe del depósito", "0 €")

    valor_subasta = limpiar_precio(valor_subasta_str)
    tasacion = limpiar_precio(tasacion_str)
    puja_min = limpiar_precio(puja_min_str)
    deposito = limpiar_precio(deposito_str)

    # El valor de referencia más alto es el valor tasado o de subasta
    valor_referencia = max(valor_subasta, tasacion)

    # Si la puja mínima es 0 o no consta, la salida estimada suele ser un % de tasación o tramo inicial
    precio_salida = puja_min if puja_min > 0 else (valor_referencia * 0.3 if valor_referencia > 0 else 0)

    # Calcular ahorro potencial
    ahorro_pct = 0
    if valor_referencia > 0 and precio_salida > 0 and valor_referencia > precio_salida:
        ahorro_pct = int(((valor_referencia - precio_salida) / valor_referencia) * 100)

    direccion = datos_bien.get("dirección", "")
    localidad = datos_bien.get("localidad", "Madrid")
    cp = datos_bien.get("código postal", "")
    ref_catastral = datos_bien.get("referencia catastral", "No consta").strip()
    descripcion = datos_bien.get("descripción", "")

    # Auditoría de Ocupación / Situación Posesoria
    sit_raw = datos_bien.get("situación posesoria", "No consta").strip()
    sit_lower = sit_raw.lower()
    if any(k in sit_lower for k in ["libre", "desocupad", "vacia", "vacía"]):
        situacion_formato = "🟢 Libre de ocupantes (Desocupada)"
    elif any(k in sit_lower for k in ["arrendad", "alquiler", "inquilino"]):
        situacion_formato = "🔴 Con contrato de arrendamiento previo"
    elif any(k in sit_lower for k in ["ejecutad", "demandad"]):
        situacion_formato = "🟡 Ocupada por el ejecutado (desalojo ordinario Art. 675 LEC)"
    elif "ocupad" in sit_lower:
        situacion_formato = "🟡 Ocupada (requiere posesión judicial)"
    else:
        situacion_formato = "⚪ No especificada en edicto (consultar juzgado)"

    visitable = datos_bien.get("visitable", "No consta").strip()

    # URL Google Maps / Street View
    dir_completa = f"{direccion}, {cp} {localidad}".strip(" ,")
    query_maps = urllib.parse.quote_plus(f"{dir_completa}, España")
    url_maps = f"https://www.google.com/maps/search/?api=1&query={query_maps}"

    # Cálculo de Potencial de Alquiler y Rentabilidad Bruta (ROI %)
    alquiler_estimado_mes = 0
    roi_alquiler = 0.0
    if valor_referencia > 0:
        alquiler_estimado_mes = max(400, int(round((valor_referencia * 0.065) / 12, -1)))
        if precio_salida > 0:
            roi_alquiler = round(((alquiler_estimado_mes * 12) / precio_salida) * 100, 1)

    # URL Oficial Sede del Catastro
    url_catastro = None
    if ref_catastral and len(ref_catastral) >= 14 and "no consta" not in ref_catastral.lower():
        url_catastro = f"https://www1.sedecatastro.gob.es/CYCAssist/ConsultaBien.aspx?refcat={ref_catastral}"

    # URL Comparador de Mercado en Idealista
    query_idealista = urllib.parse.quote_plus(f"idealista venta viviendas {direccion} {localidad}".strip())
    url_idealista = f"https://www.google.com/search?q={query_idealista}"

    # URL 1-Clic Guardar en Google Calendar con Alarma
    fecha_fin_raw = datos_gen.get("fecha de conclusión", "En los próximos días")
    url_calendar = generar_enlace_google_calendar(
        titulo=f"Piso en {localidad} ({cp})",
        fecha_fin_str=fecha_fin_raw,
        direccion=dir_completa,
        id_subasta=id_subasta,
        url_oficial=url_gen
    )

    # Algoritmo de Calificación de Oportunidad (Score 1 a 10)
    score = 5.0
    if ahorro_pct >= 60:
        score += 3.0
    elif ahorro_pct >= 40:
        score += 2.0
    elif ahorro_pct >= 25:
        score += 1.0

    if deposito > 0 and deposito <= 5000:
        score += 1.0
    elif deposito <= 12000:
        score += 0.5

    if "🟢" in situacion_formato:
        score += 1.0
    elif "🔴" in situacion_formato:
        score -= 1.5

    if url_catastro:
        score += 0.5

    score = min(9.9, max(1.0, round(score, 1)))
    if score >= 8.5:
        score_badge = f"⭐ {score}/10 (Oportunidad Oro 🏆)"
    elif score >= 7.0:
        score_badge = f"⭐ {score}/10 (Oportunidad Plata 🥈)"
    else:
        score_badge = f"⭐ {score}/10 (Oportunidad Moderada)"

    return {
        "id_subasta": id_subasta,
        "titulo": f"Inmueble en {localidad} ({cp})",
        "direccion": dir_completa,
        "localidad": localidad,
        "codigo_postal": cp,
        "referencia_catastral": ref_catastral,
        "descripcion": descripcion[:200] + "..." if len(descripcion) > 200 else descripcion,
        "situacion_posesoria": situacion_formato,
        "visitable": visitable,
        "url_maps": url_maps,
        "url_catastro": url_catastro,
        "url_idealista": url_idealista,
        "url_calendar": url_calendar,
        "alquiler_estimado_mes": alquiler_estimado_mes,
        "roi_alquiler": roi_alquiler,
        "score_oportunidad": score,
        "score_badge": score_badge,
        "valor_referencia": valor_referencia,
        "valor_referencia_formato": f"{valor_referencia:,.0f} €".replace(",", "."),
        "precio_salida": precio_salida,
        "precio_salida_formato": f"{precio_salida:,.0f} €".replace(",", "."),
        "ahorro_porcentaje": ahorro_pct,
        "deposito": f"{deposito:,.0f} €".replace(",", "."),
        "fecha_fin": datos_gen.get("fecha de conclusión", "En los próximos días"),
        "url_oficial": url_gen
    }

def filtrar_mejores_chollos(ids_subastas: List[str], max_resultados: int = 3) -> List[Dict]:
    """Analiza las subastas y devuelve las que tienen mejor descuento y datos completos."""
    chollos = []
    print("⏳ Analizando expedientes detallados en el BOE...")
    for id_sub in ids_subastas:
        detalle = obtener_detalle_subasta(id_sub)
        if not detalle:
            continue
        # Filtros de calidad:
        # 1. Debe tener dirección conocida
        if len(detalle["direccion"]) < 5:
            continue
        # 2. Debe tener un valor de tasación significativo (> 50.000 €)
        if detalle["valor_referencia"] < 50000:
            continue
        # 3. Debe representar un ahorro potencial
        if detalle["ahorro_porcentaje"] >= 30:
            chollos.append(detalle)
            print(f"  ⭐ CHOLLO DETECTADO [{detalle['id_subasta']}]: {detalle['direccion']} | Val: {detalle['valor_referencia_formato']} -> Salida: {detalle['precio_salida_formato']} (-{detalle['ahorro_porcentaje']}%)")

        if len(chollos) >= max_resultados:
            break

    # Ordenar de mayor a menor descuento
    chollos.sort(key=lambda x: x["ahorro_porcentaje"], reverse=True)
    return chollos

if __name__ == "__main__":
    print("🚀 Probando Extractor de Subastas Inmobiliarias del BOE...")
    ids = buscar_subastas_inmuebles(provincia_cod="28", limite=15)
    mejores = filtrar_mejores_chollos(ids, max_resultados=3)

    print("\n🏆 TOP CHOLLOS SELECCIONADOS HOY:")
    for i, c in enumerate(mejores, 1):
        print(f"\n[{i}] {c['titulo']}")
        print(f"    📍 Dirección: {c['direccion']}")
        print(f"    💰 Valor Oficial: {c['valor_referencia_formato']} | Salida: {c['precio_salida_formato']} (Ahorro: -{c['ahorro_porcentaje']}%)")
        print(f"    📑 Catastro: {c['referencia_catastral']}")
        print(f"    🔗 Enlace BOE: {c['url_oficial']}")
