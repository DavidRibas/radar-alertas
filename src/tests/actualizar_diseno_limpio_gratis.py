import json
import os
import re

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    json_path = os.path.join(base_dir, 'docs', 'data', 'oportunidades.json')
    docs_path = os.path.join(base_dir, 'docs', 'index.html')
    root_path = os.path.join(base_dir, 'index.html')

    # 1. Actualizar oportunidades.json con esGratis
    with open(json_path, 'r', encoding='utf-8') as f:
        items = json.load(f)

    for it in items:
        tipo = it.get('tipo')
        mod = it.get('modalidad')
        # Determinar si es 100% gratis
        if it['id'] == 'INM-SUB-AT-2026-23R2886001483': # Las Rozas Muestra
            it['esGratis'] = True
            it['desbloqueado'] = True
            it['tagGratis'] = '🎁 MUESTRA OFICIAL GRATIS'
            it['ctaLabel'] = '📄 Descargar Dictamen Oficial en PDF (Gratis) →'
        elif tipo == 'empleo':
            it['esGratis'] = True
            it['tagGratis'] = '🟢 100% GRATIS · CONVOCATORIA'
            it['ctaLabel'] = '📋 Ver Convocatoria y Bases Oficiales (Gratis) →'
        elif tipo == 'vivienda' and mod == 'directa':
            it['esGratis'] = True
            it['tagGratis'] = '🟢 100% GRATIS · SOLICITUD'
            it['ctaLabel'] = '🏠 Ver Requisitos y Solicitar Vivienda (Gratis) →'
        elif tipo == 'ayuda':
            it['esGratis'] = True
            it['tagGratis'] = '🟢 100% GRATIS · SUBVENCIÓN'
            it['ctaLabel'] = '💰 Ver Bases y Solicitar Subvención (Gratis) →'
        else:
            it['esGratis'] = False
            it['tagGratis'] = None
            it['ctaLabel'] = 'Desbloquear Expediente • 2,90 € →'

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print(f"Actualizado {json_path}: {sum(1 for i in items if i.get('esGratis'))} oportunidades gratis.")

    # 2. Actualizar HTML en docs/index.html y root index.html
    for p in [docs_path, root_path]:
        with open(p, 'r', encoding='utf-8') as f:
            html = f.read()

        # Inyectar OPORTUNIDADES actualizado
        json_str = json.dumps(items, ensure_ascii=False, indent=8)
        start_tag = 'let OPORTUNIDADES = ['
        idx_start = html.find(start_tag)
        assert idx_start != -1
        idx_end = html.find('];', idx_start)
        assert idx_end != -1
        html = html[:idx_start] + 'let OPORTUNIDADES = ' + json_str + html[idx_end+1:]

        # Añadir chip de Filtro 100% Gratis en quick-filter-chips
        old_chips_markup = '''<div class="quick-filter-chips">
            <span class="chip-label">Filtros exprés:</span>
            <button class="chip-btn" id="chipVpo" onclick="aplicarFiltroRapido('alquiler_vpo')">🏠 Alquiler Protegido</button>'''
        
        new_chips_markup = '''<div class="quick-filter-chips">
            <span class="chip-label">Filtros exprés:</span>
            <button class="chip-btn chip-free-highlight" id="chipGratis" onclick="aplicarFiltroRapido('solo_gratis')" style="background: rgba(16, 185, 129, 0.2); border-color: #10b981; color: #34d399; font-weight: 800; box-shadow: 0 0 10px rgba(16,185,129,0.2);">🟢 100% Gratis / Muestras</button>
            <button class="chip-btn" id="chipVpo" onclick="aplicarFiltroRapido('alquiler_vpo')">🏠 Alquiler Protegido</button>'''
        
        if old_chips_markup in html:
            html = html.replace(old_chips_markup, new_chips_markup)
        elif 'chipGratis' not in html:
            print("Warning: old_chips_markup not found exactly, searching for quick-filter-chips...")
            qfc_idx = html.find('<div class="quick-filter-chips">')
            assert qfc_idx != -1
            lbl_idx = html.find('>', qfc_idx) + 1
            lbl_end = html.find('</span>', lbl_idx) + 7
            chip_code = '\n            <button class="chip-btn chip-free-highlight" id="chipGratis" onclick="aplicarFiltroRapido(\'solo_gratis\')" style="background: rgba(16, 185, 129, 0.2); border-color: #10b981; color: #34d399; font-weight: 800; box-shadow: 0 0 10px rgba(16,185,129,0.2);">🟢 100% Gratis / Muestras</button>'
            html = html[:lbl_end] + chip_code + html[lbl_end:]

        # Actualizar lógica de aplicarFiltroRapido
        old_filtro_code = "if (tipo === 'alquiler_vpo') {"
        new_filtro_code = """if (tipo === 'solo_gratis') {
                const btn = document.getElementById('chipGratis');
                if (btn) btn.classList.add('active');
                categoriaActual = 'all';
                actualizarTabsUI('all');
            } else if (tipo === 'alquiler_vpo') {"""
        if old_filtro_code in html and "tipo === 'solo_gratis'" not in html:
            html = html.replace(old_filtro_code, new_filtro_code)

        # Actualizar condición en filtrarOportunidades
        old_match_rapido = "let matchRapido = true;"
        new_match_rapido = """let matchRapido = true;
                if (filtroRapidoActual === 'solo_gratis') {
                    matchRapido = item.esGratis === true || item.desbloqueado === true;
                } else """
        if old_match_rapido in html and "filtroRapidoActual === 'solo_gratis'" not in html:
            html = html.replace(old_match_rapido, new_match_rapido)

        # 3. Rediseño limpio de las tarjetas:
        # Encontramos la plantilla de renderizado de la tarjeta
        # Buscamos desde 'grid.innerHTML = filtradas.map(item => {' hasta '</article>'
        start_map_idx = html.find("grid.innerHTML = filtradas.map(item => {")
        assert start_map_idx != -1
        end_map_idx = html.find("}).join('');", start_map_idx)
        assert end_map_idx != -1

        new_map_function = """grid.innerHTML = filtradas.map(item => {
                const esGratis = item.esGratis === true || item.desbloqueado === true;
                const esDirecta = item.modalidad === 'directa';
                
                // Etiquetas de cabecera limpias
                const tagSuperior = esGratis 
                    ? `<span class="card-tag" style="background:#059669; color:#ffffff; font-weight:800; border:none; box-shadow:0 2px 8px rgba(5,150,105,0.4);">${item.tagGratis || '🟢 100% GRATIS'}</span>`
                    : `<span class="card-tag ${item.tagClass}">${item.tag}</span>`;

                const modBadgeClass = esDirecta ? 'badge-mod-directa' : 'badge-mod-subasta';
                const modBadgeText = esDirecta ? '📋 SOLICITUD DIRECTA' : '🔨 SUBASTA PÚBLICA';
                const labelMercado = esDirecta ? (item.tipo === 'vivienda' ? 'Alquiler Libre' : 'Sin Alerta') : 'Mercado Libre';
                const labelOficial = esDirecta ? (item.tipo === 'vivienda' ? 'Alquiler Protegido' : 'Oficial Estado') : 'Precio Salida';

                return `
                <article class="card ${esGratis ? 'card-free-deal' : ''}">
                    <div class="card-img" style="background-image: url('${item.img}');">
                        ${tagSuperior}
                        <span class="card-modality-badge ${modBadgeClass}">${modBadgeText}</span>
                        ${item.ahorro ? `<span class="discount-badge">${item.ahorro}</span>` : ''}
                    </div>
                    <div class="card-body">
                        <div class="card-location">📍 ${item.ubicacion}</div>
                        <h3 class="card-title">${item.titulo}</h3>
                        <div class="card-specs">
                            ${item.specs.map(s => `<span class="spec-item">${s}</span>`).join('')}
                        </div>

                        <!-- Precios Claros -->
                        <div class="prices-box">
                            <div class="market-p">
                                <span class="market-label">${labelMercado}</span>
                                <span class="market-val">${item.precioMercado}</span>
                            </div>
                            <div class="boe-p">
                                <span class="boe-label">${labelOficial}</span>
                                <span class="boe-val">${item.precioBoe}</span>
                            </div>
                        </div>

                        <!-- 1 Sola Línea de Garantía Legal / Salario Oficial (Sin Saturar) -->
                        <div class="clean-legal-row">
                            <span class="clean-legal-icon">🛡️</span>
                            <span class="clean-legal-text">${item.legal}</span>
                        </div>

                        <!-- ZONA DE ACCIÓN: CLARA, LIMPIA Y SIN LÍOS -->
                        ${esGratis ? `
                        <!-- OPORTUNIDAD 100% GRATUITA -->
                        <div class="action-box-clean free-box">
                            <div class="action-status-line">
                                <span class="status-dot"></span>
                                <span class="status-text">${item.desbloqueado ? 'Muestra Oficial Auditada · Descarga Inmediata' : 'Convocatoria Oficial Abierta · Acceso Libre'}</span>
                                <span class="free-pill">GRATIS</span>
                            </div>
                            <a href="${item.pdfMuestra || item.enlaceBoeReal || '#'}" ${item.desbloqueado ? 'download' : 'target="_blank"'} class="btn-clean-cta btn-free-cta">
                                ${item.ctaLabel}
                            </a>
                        </div>
                        ` : `
                        <!-- SUBASTA CON DICTAMEN PERICIAL (2,90 €) -->
                        <div class="action-box-clean paid-box">
                            <div class="action-status-line">
                                <span class="paid-title">📄 Dictamen Pericial Oficial + Expediente</span>
                                <span class="paid-pill">2,90 €</span>
                            </div>
                            <button class="btn-clean-cta btn-paid-cta" onclick="abrirModalDesbloqueo('${item.id}')">
                                🔓 Desbloquear Expediente • 2,90 € →
                            </button>
                            <button class="btn-clean-sublink" onclick="abrirModalPro()">
                                ⭐ O acceso ilimitado con Plan PRO (14,99 €/mes)
                            </button>
                        </div>
                        `}

                        <button class="btn-share-wa" onclick="compartirWhatsApp('${item.titulo.replace(/'/g, "\\'")}', '${item.ahorro}', '${item.precioBoe}', '${item.id}')">
                            📲 Avisar por WhatsApp a un amigo
                        </button>
                    </div>
                </article>
                `;
            """

        html = html[:start_map_idx] + new_map_function + html[end_map_idx:]

        # 4. Estilos CSS modernos, limpios y desaturados para las tarjetas
        clean_css = """
        /* === ESTILOS TARJETAS LIMPIAS (CERO LÍO, MÁXIMA CLARIDAD) === */
        .clean-legal-row {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 10px;
            margin: 10px 0;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 8px;
            font-size: 11.5px;
            color: #94a3b8;
        }
        body.theme-light .clean-legal-row {
            background: #f1f5f9;
            border-color: #e2e8f0;
            color: #475569;
        }
        .clean-legal-icon {
            font-size: 14px;
            flex-shrink: 0;
        }

        .action-box-clean {
            border-radius: 12px;
            padding: 12px;
            margin: 12px 0 10px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        /* Caja Gratuita (Verde Limpio) */
        .action-box-clean.free-box {
            background: rgba(16, 185, 129, 0.08);
            border: 1.5px solid rgba(16, 185, 129, 0.4);
        }
        body.theme-light .action-box-clean.free-box {
            background: #ecfdf5;
            border-color: #10b981;
        }
        .card-free-deal {
            border-color: rgba(16, 185, 129, 0.4) !important;
        }

        .action-status-line {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
        }
        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #10b981;
            box-shadow: 0 0 8px #10b981;
            display: inline-block;
        }
        .status-text {
            font-size: 11px;
            font-weight: 700;
            color: #34d399;
            flex: 1;
        }
        body.theme-light .status-text {
            color: #059669;
        }
        .free-pill {
            background: #10b981;
            color: #ffffff;
            font-size: 10px;
            font-weight: 900;
            padding: 3px 8px;
            border-radius: 20px;
            letter-spacing: 0.5px;
        }

        /* Caja de Pago (2,90 € Elegante) */
        .action-box-clean.paid-box {
            background: rgba(30, 41, 59, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        body.theme-light .action-box-clean.paid-box {
            background: #f8fafc;
            border-color: #cbd5e1;
        }
        .paid-title {
            font-size: 12px;
            font-weight: 700;
            color: #cbd5e1;
        }
        body.theme-light .paid-title {
            color: #1e293b;
        }
        .paid-pill {
            background: rgba(56, 189, 248, 0.15);
            border: 1px solid rgba(56, 189, 248, 0.4);
            color: #38bdf8;
            font-size: 11px;
            font-weight: 800;
            padding: 3px 8px;
            border-radius: 6px;
        }
        body.theme-light .paid-pill {
            background: #e0f2fe;
            border-color: #0284c7;
            color: #0284c7;
        }

        /* Botones de Acción Nuevos */
        .btn-clean-cta {
            width: 100%;
            padding: 12px 14px;
            border-radius: 9px;
            font-size: 13.5px;
            font-weight: 800;
            cursor: pointer;
            text-align: center;
            text-decoration: none;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            border: none;
            transition: all 0.2s ease;
        }
        .btn-free-cta {
            background: linear-gradient(135deg, #059669 0%, #10b981 100%);
            color: #ffffff;
            box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35);
        }
        .btn-free-cta:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(16, 185, 129, 0.5);
        }
        .btn-paid-cta {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            color: #ffffff;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
        }
        .btn-paid-cta:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5);
        }
        .btn-clean-sublink {
            background: transparent;
            border: none;
            color: #94a3b8;
            font-size: 11.5px;
            cursor: pointer;
            text-align: center;
            padding: 4px;
            transition: color 0.2s;
        }
        .btn-clean-sublink:hover {
            color: #fbbf24;
            text-decoration: underline;
        }
        body.theme-light .btn-clean-sublink {
            color: #64748b;
        }
        """

        if '/* === ESTILOS TARJETAS LIMPIAS' not in html:
            idx_style_end = html.find('</style>')
            assert idx_style_end != -1
            html = html[:idx_style_end] + clean_css + html[idx_style_end:]

        with open(p, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Actualizado {p} con nuevo diseño limpio.")

if __name__ == '__main__':
    main()
