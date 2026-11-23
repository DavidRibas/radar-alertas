import json
import os

def aplicar_uno_por_clase():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    json_path = os.path.join(base_dir, 'docs', 'data', 'oportunidades.json')
    docs_path = os.path.join(base_dir, 'docs', 'index.html')
    root_path = os.path.join(base_dir, 'index.html')

    with open(json_path, 'r', encoding='utf-8') as f:
        items = json.load(f)

    # Ids seleccionados para ser los 5 embajadores de muestra gratuita (1 por clase):
    ID_GRATIS_INMUEBLE = 'INM-SUB-AT-2026-23R2886001483' # Las Rozas (Madrid)
    ID_GRATIS_VEHICULO = 'VEH-SUB-AT-2026-26R3886002006' # Citroen C5 Aircross Plug-In Hybrid
    ID_GRATIS_EMPLEO   = 'EMP-BOE-A-2026-24530'          # Ministerio de Hacienda (+2.350 €/mes)
    ID_GRATIS_VIVIENDA = 'VPO-VIVE-2026-MAD01'           # Plan VIVE Madrid (Pisos 400 €/mes)
    ID_GRATIS_AYUDA    = 'AYUDA-BDNS-06'                 # Subvencion hasta 12.000 € a fondo perdido

    ids_gratis = {
        ID_GRATIS_INMUEBLE: {
            'tagGratis': '🎁 MUESTRA GRATIS · INMUEBLE',
            'ctaLabel': '📄 Descargar Dictamen Oficial en PDF (Gratis) →',
            'pdfMuestra': 'assets/Dictamen_Verificado_Final.pdf',
            'enlaceBoeReal': 'https://subastas.boe.es'
        },
        ID_GRATIS_VEHICULO: {
            'tagGratis': '🎁 MUESTRA GRATIS · VEHÍCULO',
            'ctaLabel': '📄 Ver Informe DGT y Mandamiento Judicial (Gratis) →',
            'pdfMuestra': 'assets/Dictamen_Verificado_Final.pdf',
            'enlaceBoeReal': 'https://subastas.boe.es'
        },
        ID_GRATIS_EMPLEO: {
            'tagGratis': '🟢 MUESTRA GRATIS · EMPLEO',
            'ctaLabel': '📋 Ver Convocatoria y Bases Oficiales (Gratis) →',
            'enlaceBoeReal': 'https://www.boe.es'
        },
        ID_GRATIS_VIVIENDA: {
            'tagGratis': '🟢 MUESTRA GRATIS · VIVIENDA VPO',
            'ctaLabel': '🏠 Ver Requisitos y Solicitar Vivienda (Gratis) →',
            'enlaceBoeReal': 'https://www.comunidad.madrid/servicios/vivienda/plan-vive'
        },
        ID_GRATIS_AYUDA: {
            'tagGratis': '🟢 MUESTRA GRATIS · SUBVENCIÓN',
            'ctaLabel': '💰 Ver Bases y Solicitar Subvención (Gratis) →',
            'enlaceBoeReal': 'https://www.infosubvenciones.es/bdnstrans/GE/es/index'
        }
    }

    for it in items:
        item_id = it['id']
        if item_id in ids_gratis:
            cfg = ids_gratis[item_id]
            it['esGratis'] = True
            it['desbloqueado'] = True
            it['tagGratis'] = cfg['tagGratis']
            it['ctaLabel'] = cfg['ctaLabel']
            if 'pdfMuestra' in cfg:
                it['pdfMuestra'] = cfg['pdfMuestra']
            it['enlaceBoeReal'] = cfg['enlaceBoeReal']
            print(f"GRATIS CONFIGURADO ({it['tipo'].upper()}): {it['titulo'][:40]}")
        else:
            it['esGratis'] = False
            it['desbloqueado'] = False
            it['tagGratis'] = None
            if it.get('modalidad') == 'directa':
                it['ctaLabel'] = '📋 Desbloquear Solicitud y Requisitos • 2,90 € →'
            else:
                it['ctaLabel'] = '🔓 Desbloquear Expediente • 2,90 € →'

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    # Actualizar docs/index.html y root index.html
    for p in [docs_path, root_path]:
        with open(p, 'r', encoding='utf-8') as f:
            html = f.read()

        json_str = json.dumps(items, ensure_ascii=False, indent=8)
        start_tag = 'let OPORTUNIDADES = ['
        idx_start = html.find(start_tag)
        assert idx_start != -1
        idx_end = html.find('];', idx_start)
        assert idx_end != -1
        html = html[:idx_start] + 'let OPORTUNIDADES = ' + json_str + html[idx_end+1:]

        with open(p, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Actualizado {p}")

if __name__ == '__main__':
    aplicar_uno_por_clase()
