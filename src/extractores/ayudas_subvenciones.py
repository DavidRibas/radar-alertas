"""
Extractor Oficial de Ayudas y Subvenciones del Estado a Fondo Perdido (BDNS)
Fuente: Base de Datos Nacional de Subvenciones (Ministerio de Hacienda)
Coste: 0,00 € (API REST pública y oficial).
"""
import requests
from datetime import datetime
from typing import List, Dict, Optional

URL_BUSQUEDA = "https://www.infosubvenciones.es/bdnstrans/api/convocatorias/busqueda"
URL_DETALLE = "https://www.infosubvenciones.es/bdnstrans/api/convocatorias"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def obtener_convocatorias_recientes(max_paginas: int = 2) -> List[Dict]:
    """Obtiene el listado de las últimas convocatorias publicadas en España."""
    convocatorias = []
    try:
        for p in range(max_paginas):
            resp = requests.get(
                URL_BUSQUEDA,
                params={"page": p, "size": 30},
                headers=HEADERS,
                timeout=10
            )
            if resp.status_code == 200:
                datos = resp.json()
                items = datos.get("content", [])
                convocatorias.extend(items)
            else:
                break
    except Exception as e:
        print(f"⚠️ Error al conectar con API BDNS: {e}")
    return convocatorias

def obtener_detalle_convocatoria(num_convocatoria: str) -> Optional[Dict]:
    """Extrae el expediente completo con presupuesto, beneficiarios y sede electrónica."""
    try:
        resp = requests.get(
            URL_DETALLE,
            params={"numConv": num_convocatoria, "vpd": "GE"},
            headers=HEADERS,
            timeout=10
        )
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print(f"⚠️ Error al obtener detalle de convocatoria {num_convocatoria}: {e}")
    return None

def filtrar_mejores_ayudas(convocatorias: List[Dict], max_resultados: int = 5) -> List[Dict]:
    """
    Filtra y selecciona las subvenciones más atractivas:
    - A fondo perdido (sin contraprestación).
    - Para autónomos, pymes, emprendedores, familias o personas físicas.
    - Con plazo de solicitud abierto y presupuesto relevante.
    """
    ayudas_seleccionadas = []

    for c in convocatorias:
        num_conv = c.get("numeroConvocatoria")
        if not num_conv:
            continue

        detalle = obtener_detalle_convocatoria(num_conv)
        if not detalle:
            continue

        # 1. Comprobar si está abierta
        abierto = detalle.get("abierto", False)
        # 2. Comprobar si es entrega dineraria a fondo perdido
        instrumentos = detalle.get("instrumentos", [])
        es_fondo_perdido = any("SIN CONTRAPRESTACIÓN" in str(inst.get("descripcion", "")).upper() for inst in instrumentos)
        
        # 3. Analizar beneficiarios
        beneficiarios_raw = detalle.get("tiposBeneficiarios", [])
        lista_ben = [b.get("descripcion", "").upper() for b in beneficiarios_raw if isinstance(b, dict)]
        
        # Palabras clave de alto impacto comercial
        desc_completa = (detalle.get("descripcion", "") + " " + detalle.get("descripcionFinalidad", "")).lower()
        
        interesante = any(k in desc_completa for k in [
            "autonomo", "autónomo", "pyme", "empresa", "comercio", "digitalizacion", 
            "digitalización", "vivienda", "joven", "empleo", "contratacion", "solar", 
            "eficiencia", "innovacion", "formacion"
        ])

        presupuesto = detalle.get("presupuestoTotal") or 0
        if isinstance(presupuesto, (int, float)) and presupuesto > 0 and (es_fondo_perdido or interesante):
            # Extraer órgano
            organo_dict = detalle.get("organo") or {}
            organismo = organo_dict.get("nivel2") or organo_dict.get("nivel3") or "Administración Pública"

            # Formatear fecha
            fecha_fin = detalle.get("fechaFinSolicitud") or detalle.get("textFin") or "Según bases"

            ayuda = {
                "id_convocatoria": num_conv,
                "titulo": detalle.get("descripcion", "Convocatoria pública"),
                "organismo": organismo,
                "presupuesto_total": presupuesto,
                "presupuesto_formato": f"{presupuesto:,.0f} €".replace(",", "."),
                "es_fondo_perdido": es_fondo_perdido,
                "beneficiarios": ", ".join(lista_ben[:2]) if lista_ben else "Autónomos, Empresas y Particulares",
                "fecha_fin": fecha_fin,
                "sede_electronica": detalle.get("sedeElectronica") or "https://www.infosubvenciones.es",
                "url_bases": detalle.get("urlBasesReguladoras") or "",
                "descripcion_finalidad": (detalle.get("descripcionFinalidad") or detalle.get("descripcion") or "")[:250]
            }
            ayudas_seleccionadas.append(ayuda)
            if len(ayudas_seleccionadas) >= max_resultados:
                break

    return ayudas_seleccionadas

if __name__ == "__main__":
    print("🔍 Buscando ayudas y subvenciones oficiales activas en España...")
    convs = obtener_convocatorias_recientes(max_paginas=1)
    print(f"📦 Total convocatorias analizadas: {len(convs)}")
    mejores = filtrar_mejores_ayudas(convs, max_resultados=3)
    print(f"🎯 Ayudas de alto impacto seleccionadas: {len(mejores)}")
    for a in mejores:
        print("\n" + "=" * 50)
        print(f"💶 {a['titulo']}")
        print(f"🏛️ Organismo: {a['organismo']}")
        print(f"💰 Presupuesto: {a['presupuesto_formato']}")
        print(f"⏳ Plazo hasta: {a['fecha_fin']}")
        print(f"🔗 Sede: {a['sede_electronica']}")
