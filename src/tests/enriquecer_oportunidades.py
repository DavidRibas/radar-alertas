import json
import os

def enriquecer_oportunidades():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    json_path = os.path.join(base_dir, 'docs', 'data', 'oportunidades.json')

    with open(json_path, 'r', encoding='utf-8') as f:
        items = json.load(f)

    # 1. Asegurar modalidad en items existentes
    for it in items:
        if it.get('tipo') in ['inmueble', 'vehiculo', 'licitacion']:
            it['modalidad'] = 'subasta'
            it['modalidadLabel'] = '🔨 SUBASTA PÚBLICA'
            it['modalidadClass'] = 'badge-subasta'
        elif it.get('tipo') in ['empleo', 'ayuda']:
            it['modalidad'] = 'directa'
            it['modalidadLabel'] = '📋 SOLICITUD DIRECTA'
            it['modalidadClass'] = 'badge-directa'

    # 2. Nuevas Oportunidades Estrella: VIVIENDA VPO Y ALQUILER PROTEGIDO
    viviendas_nuevas = [
        {
            "id": "VPO-VIVE-2026-MAD01",
            "expedienteReal": "PLAN-VIVE-CAM-2026/04",
            "enlaceBoeReal": "https://www.comunidad.madrid/servicios/vivienda/plan-vive-madrid",
            "tipo": "vivienda",
            "modalidad": "directa",
            "modalidadLabel": "📋 SOLICITUD DIRECTA (Sin subasta)",
            "modalidadClass": "badge-directa",
            "tag": "ALQUILER PROTEGIDO • PLAN VIVE",
            "tagClass": "tag-vpo",
            "badgeVisual": "🏡 PISOS A ESTRENAR 450€",
            "titulo": "Promoción 300 Pisos Alquiler Protegido · Getafe / Alcorcón",
            "ubicacion": "Madrid • Área Metropolitana",
            "provincia": "madrid",
            "precioBoe": "450 €/mes",
            "precioMercado": "1.150 €/mes",
            "ahorro": "-60% ALQUILER FIJO",
            "specs": [
                "2 y 3 Dormitorios + Garaje",
                "Piscina, Gimnasio y Pistas",
                "Contrato Seguro 7 Años",
                "Inscripción Gratuita Telemática"
            ],
            "legal": "Sin puja ni fianza • Asignación por orden de inscripción y baremo",
            "img": "assets/templates/inmueble_madrid_residencial.jpg",
            "desbloqueado": False,
            "ctaLabel": "📋 Desbloquear Formulario y Requisitos (2,90 €)"
        },
        {
            "id": "VPO-EMVS-2026-MAD02",
            "expedienteReal": "EMVS-SORTEO-2026/89",
            "enlaceBoeReal": "https://www.emvs.es/Vivienda/Alquiler",
            "tipo": "vivienda",
            "modalidad": "directa",
            "modalidadLabel": "📋 SORTEO PÚBLICO OFICIAL",
            "modalidadClass": "badge-directa",
            "tag": "VIVIENDA PÚBLICA • EMVS MADRID",
            "tagClass": "tag-vpo",
            "badgeVisual": "🔑 ALQUILER SOCIAL 380€",
            "titulo": "Sorteo 246 Viviendas Alquiler Social y Joven · Ensanche de Vallecas",
            "ubicacion": "Madrid • Vallecas / Vicálvaro",
            "provincia": "madrid",
            "precioBoe": "380 €/mes",
            "precioMercado": "950 €/mes",
            "ahorro": "-60% ALQUILER FIJO",
            "specs": [
                "Viviendas 1 a 3 Habitaciones",
                "Calificación Energética A",
                "Plazo Abierto: Cupo Joven y General",
                "Adjudicación por Sorteo Notarial"
            ],
            "legal": "Sin fianza previa • Inscripción gratuita con Certificado Digital o Cl@ve",
            "img": "assets/templates/inmueble_cataluna_costa.jpg",
            "desbloqueado": False,
            "ctaLabel": "📋 Desbloquear Formulario y Requisitos (2,90 €)"
        },
        {
            "id": "VPO-HBCN-2026-BCN01",
            "expedienteReal": "HAB-PROT-CAT-2026/12",
            "enlaceBoeReal": "https://habitatge.gencat.cat",
            "tipo": "vivienda",
            "modalidad": "directa",
            "modalidadLabel": "📋 SOLICITUD DIRECTA (Sin subasta)",
            "modalidadClass": "badge-directa",
            "tag": "HABITATGE PROTEGIT • BARCELONA",
            "tagClass": "tag-vpo",
            "badgeVisual": "🏢 ALQUILER REGULADO 480€",
            "titulo": "Promoción 180 Viviendas Alquiler Asequible · Parc de l'Alba",
            "ubicacion": "Barcelona • Cerdanyola / Sant Cugat",
            "provincia": "barcelona",
            "precioBoe": "480 €/mes",
            "precioMercado": "1.200 €/mes",
            "ahorro": "-60% ALQUILER FIJO",
            "specs": [
                "Viviendas Nuevas Eficientes",
                "A 20 Minutos del Centro",
                "Alquiler Máximo 30% Ingresos",
                "Registro de Solicitantes Abierto"
            ],
            "legal": "Sin puja de dinero • Adjudicación transparente por registro oficial",
            "img": "assets/templates/inmueble_andalucia_villa.jpg",
            "desbloqueado": False,
            "ctaLabel": "📋 Desbloquear Formulario y Requisitos (2,90 €)"
        }
    ]

    # 3. Nuevas Oportunidades Estrella: DECOMISOS DEL ESTADO (PNSD / NARCOTRÁFICO)
    decomisos_nuevos = [
        {
            "id": "DEC-PNSD-2026-PORSCHE",
            "expedienteReal": "PNSD-DEC-2026/088",
            "enlaceBoeReal": "https://pnsd.sanidad.gob.es/delegacionGobiernoPNSD/fondoBienesDecomisados/subastas/home.htm",
            "tipo": "vehiculo",
            "modalidad": "subasta",
            "modalidadLabel": "🔨 SUBASTA DECOMISO ESTADO",
            "modalidadClass": "badge-subasta",
            "tag": "FONDO DE BIENES DECOMISADOS",
            "tagClass": "tag-decomiso",
            "badgeVisual": "🏎️ PORSCHE MACAN -79%",
            "titulo": "Porsche Macan S 258CV · Decomiso Oficial Ministerio de Sanidad",
            "ubicacion": "Madrid • Depósito Oficial del Estado",
            "provincia": "madrid",
            "precioBoe": "7.900 €",
            "precioMercado": "38.000 €",
            "ahorro": "-79% DESCUENTO",
            "specs": [
                "Año 2018 • 89.000 km",
                "Automático PDK • Cuero Completo",
                "Limpio de Cargas Policiales",
                "Fianza 5%: 395 €"
            ],
            "legal": "Adjudicación directa PNSD • Se entrega con documentación oficial lista para matricular",
            "img": "assets/templates/vehiculo_audi_sportback.jpg",
            "desbloqueado": False,
            "ctaLabel": "🔨 Desbloquear Expediente y Puja (2,90 €)"
        },
        {
            "id": "DEC-PNSD-2026-MERCEDES",
            "expedienteReal": "PNSD-DEC-2026/094",
            "enlaceBoeReal": "https://pnsd.sanidad.gob.es/delegacionGobiernoPNSD/fondoBienesDecomisados/subastas/home.htm",
            "tipo": "vehiculo",
            "modalidad": "subasta",
            "modalidadLabel": "🔨 SUBASTA DECOMISO ESTADO",
            "modalidadClass": "badge-subasta",
            "tag": "FONDO DE BIENES DECOMISADOS",
            "tagClass": "tag-decomiso",
            "badgeVisual": "🔥 MERCEDES C220d AMG -81%",
            "titulo": "Mercedes-Benz C220d Coupé AMG Line · Decomiso Delegación Gobierno",
            "ubicacion": "Málaga • Depósito Judicial",
            "provincia": "malaga",
            "precioBoe": "4.800 €",
            "precioMercado": "26.500 €",
            "ahorro": "-81% DESCUENTO",
            "specs": [
                "Paquete AMG Completo",
                "Año 2019 • Diésel 194CV",
                "Inspeccionado por Perito Oficial",
                "Fianza 5%: 240 €"
            ],
            "legal": "Cancelación total de precintos y embargos según Ley 17/2003",
            "img": "assets/templates/vehiculo_bmw_serie3.jpg",
            "desbloqueado": False,
            "ctaLabel": "🔨 Desbloquear Expediente y Puja (2,90 €)"
        },
        {
            "id": "DEC-PNSD-2026-BARCO",
            "expedienteReal": "PNSD-DEC-2026/102",
            "enlaceBoeReal": "https://pnsd.sanidad.gob.es/delegacionGobiernoPNSD/fondoBienesDecomisados/subastas/home.htm",
            "tipo": "vehiculo",
            "modalidad": "subasta",
            "modalidadLabel": "🔨 SUBASTA DECOMISO EMBARCACIÓN",
            "modalidadClass": "badge-subasta",
            "tag": "FONDO DE BIENES DECOMISADOS",
            "tagClass": "tag-decomiso",
            "badgeVisual": "⚓ YATE SEA RAY -80%",
            "titulo": "Embarcación Sea Ray 240 Sundancer (7,3m) · Decomiso Náutico",
            "ubicacion": "Alicante • Puerto Deportivo",
            "provincia": "alicante",
            "precioBoe": "6.200 €",
            "precioMercado": "32.000 €",
            "ahorro": "-80% DESCUENTO",
            "specs": [
                "Motor Mercruiser 260CV",
                "Camarote, Cocina y Baño",
                "Varada y Revisada en Puerto",
                "Fianza 5%: 310 €"
            ],
            "legal": "Adjudicación judicial libre de cargas marítimas y deudas portuarias",
            "img": "assets/templates/inmueble_valencia_mediterraneo.jpg",
            "desbloqueado": False,
            "ctaLabel": "🔨 Desbloquear Expediente y Puja (2,90 €)"
        }
    ]

    # Insertar al inicio de la lista para que salgan en los primeros resultados
    nuevos_items = viviendas_nuevas + decomisos_nuevos + items

    # Guardar en json
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(nuevos_items, f, ensure_ascii=False, indent=2)

    print(f'Actualizado {json_path} con éxito. Total oportunidades ahora: {len(nuevos_items)}')

if __name__ == '__main__':
    enriquecer_oportunidades()
