"""
Extractor Oficial de Empleo Público y Oposiciones (BOE Sección 2B)
Detecta convocatorias de plazas, bolsas extraordinarias y oposiciones en España.
Coste: 0,00 € (API REST de Datos Abiertos del BOE).
"""
import requests
import datetime
from typing import List, Dict

URL_BOE_API = "https://www.boe.es/datosabiertos/api/boe/sumario/"

def obtener_empleo_publico_reciente(fecha: str = None) -> List[Dict]:
    """Extrae las convocatorias de empleo público y oposiciones publicadas en el BOE."""
    if not fecha:
        fecha = datetime.date.today().strftime("%Y%m%d")

    convocatorias = []
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
                s2b = next((s for s in secciones if s.get("codigo") == "2B"), None)
                if not s2b:
                    continue

                depts = s2b.get("departamento", [])
                if isinstance(depts, dict):
                    depts = [depts]

                for dep in depts:
                    organismo = dep.get("nombre", "Administración Pública")
                    items = dep.get("item", [])
                    if isinstance(items, dict):
                        items = [items]
                    
                    if not items and "epigrafe" in dep:
                        epis = dep.get("epigrafe", [])
                        if isinstance(epis, dict):
                            epis = [epis]
                        for ep in epis:
                            ep_items = ep.get("item", [])
                            if isinstance(ep_items, dict):
                                ep_items = [ep_items]
                            items.extend(ep_items)
                    
                    for it in items:
                        titulo = it.get("titulo", "")
                        id_boe = it.get("identificador", "")
                        url_pdf = it.get("url_pdf", {}).get("texto", f"https://www.boe.es/diario_boe/xml.php?id={id_boe}")
                        
                        convocatorias.append({
                            "id_convocatoria": id_boe,
                            "organismo": organismo,
                            "titulo": titulo,
                            "fecha_publicacion": f,
                            "url_pdf": url_pdf
                        })

                if convocatorias:
                    print(f"📦 Encontradas {len(convocatorias)} convocatorias de empleo para fecha {f}")
                    break
        except Exception as e:
            print(f"⚠️ Error al consultar empleo BOE para fecha {f}: {e}")

    return convocatorias

if __name__ == "__main__":
    print("🔍 Buscando convocatorias de empleo público y oposiciones en el BOE...")
    empleos = obtener_empleo_publico_reciente()
    print(f"🎯 Total plazas/convocatorias detectadas: {len(empleos)}")
    for em in empleos[:4]:
        print("\n" + "=" * 50)
        print(f"🏛️ {em['organismo']}")
        print(f"💼 {em['titulo'][:120]}...")
        print(f"🔗 PDF Oficial: {em['url_pdf']}")
