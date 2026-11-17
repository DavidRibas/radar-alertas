"""
Extractor Oficial de Licitaciones y Contratos Públicos (BOE Sección 5A)
Detecta contratos de obras, servicios, suministros, limpieza, reformas y tecnología.
Coste: 0,00 € (API REST de Datos Abiertos del BOE).
"""
import requests
import datetime
from typing import List, Dict

URL_BOE_API = "https://www.boe.es/datosabiertos/api/boe/sumario/"

def obtener_licitaciones_recientes(fecha: str = None) -> List[Dict]:
    """Extrae las licitaciones públicas oficiales del BOE para la fecha indicada (YYYYMMDD)."""
    if not fecha:
        fecha = datetime.date.today().strftime("%Y%m%d")

    licitaciones = []
    # Probar hoy o fecha previa si es primera hora de la mañana
    fechas_a_probar = [fecha]
    dt = datetime.datetime.strptime(fecha, "%Y%m%d")
    for i in range(1, 4):
        fechas_a_probar.append((dt - datetime.timedelta(days=i)).strftime("%Y%m%d"))

    for f in fechas_a_probar:
        url = f"{URL_BOE_API}{f}"
        try:
            r = requests.get(url, headers={"Accept": "application/json"}, timeout=10)
            if r.status_code == 200:
                data = r.json()
                diarios = data.get("data", {}).get("sumario", {}).get("diario", [])
                if not diarios:
                    continue
                secciones = diarios[0].get("seccion", [])
                s5a = next((s for s in secciones if s.get("codigo") == "5A"), None)
                if not s5a:
                    continue

                depts = s5a.get("departamento", [])
                if isinstance(depts, dict):
                    depts = [depts]

                for dep in depts:
                    organismo = dep.get("nombre", "Administración Pública")
                    items = dep.get("item", [])
                    if isinstance(items, dict):
                        items = [items]
                    
                    for it in items:
                        titulo = it.get("titulo", "")
                        id_boe = it.get("identificador", "")
                        url_pdf = it.get("url_pdf", {}).get("texto", f"https://www.boe.es/diario_boe/xml.php?id={id_boe}")
                        
                        # Extraer tipo de contrato y palabras clave
                        t_lower = titulo.lower()
                        es_interesante = any(k in t_lower for k in [
                            "servicio", "obra", "suministro", "limpieza", "reforma", 
                            "mantenimiento", "pintura", "tecnolog", "informática", 
                            "seguridad", "transporte", "vehículo", "consultoría"
                        ])

                        if es_interesante:
                            licitaciones.append({
                                "id_licitacion": id_boe,
                                "organismo": organismo,
                                "titulo": titulo,
                                "fecha_publicacion": f,
                                "url_pdf": url_pdf
                            })

                if licitaciones:
                    print(f"📦 Encontradas {len(licitaciones)} licitaciones para fecha {f}")
                    break
        except Exception as e:
            print(f"⚠️ Error al consultar BOE para fecha {f}: {e}")

    return licitaciones

if __name__ == "__main__":
    print("🔍 Buscando contratos y licitaciones públicas oficiales en el BOE...")
    lics = obtener_licitaciones_recientes()
    print(f"🎯 Total licitaciones detectadas: {len(lics)}")
    for l in lics[:4]:
        print("\n" + "=" * 50)
        print(f"🏛️ {l['organismo']}")
        print(f"📑 {l['titulo'][:120]}...")
        print(f"🔗 PDF Oficial: {l['url_pdf']}")
