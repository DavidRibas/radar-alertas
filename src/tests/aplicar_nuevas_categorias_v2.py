import os

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    docs_path = os.path.join(base_dir, 'docs', 'index.html')
    root_path = os.path.join(base_dir, 'index.html')

    with open(docs_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. CSS nuevo para modalidades y categorías
    new_css = '''
        /* Badges de Modalidad y Nuevas Categorías */
        .card-modality-badge {
            position: absolute;
            bottom: 12px;
            left: 14px;
            font-size: 11px;
            font-weight: 800;
            padding: 5px 10px;
            border-radius: 6px;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            backdrop-filter: blur(8px);
            z-index: 2;
        }
        .badge-mod-directa {
            background: rgba(16, 185, 129, 0.95);
            color: #022c22;
            border: 1px solid rgba(255, 255, 255, 0.4);
            box-shadow: 0 2px 8px rgba(16, 185, 129, 0.4);
        }
        .badge-mod-subasta {
            background: rgba(30, 64, 175, 0.92);
            color: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 2px 8px rgba(30, 64, 175, 0.4);
        }
        .tag-vpo {
            background: linear-gradient(135deg, #059669, #10b981) !important;
            color: #ffffff !important;
        }
        .tag-decomiso {
            background: linear-gradient(135deg, #dc2626, #b91c1c) !important;
            color: #ffffff !important;
        }
        .savings-pill-banner.housing {
            background: rgba(16, 185, 129, 0.15);
            border: 1px solid rgba(16, 185, 129, 0.4);
            color: #34d399;
        }
        body.theme-light .savings-pill-banner.housing {
            background: #ecfdf5;
            border-color: #a7f3d0;
            color: #065f46;
        }

        /* Barra Explicativa de 3 Pasos */
        .how-it-works-strip {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            max-width: 1240px;
            margin: 0 auto 28px;
            padding: 0 24px;
        }
        .how-step {
            background: var(--bg-card);
            border: 1px solid var(--border-glass);
            border-radius: 16px;
            padding: 16px 18px;
            display: flex;
            align-items: flex-start;
            gap: 12px;
            transition: all 0.2s ease;
        }
        .how-step:hover {
            border-color: var(--border-glow);
            transform: translateY(-2px);
        }
        .step-num {
            background: linear-gradient(135deg, #2563eb, #3b82f6);
            color: #ffffff;
            font-size: 13px;
            font-weight: 800;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }
        .step-desc {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        .step-desc strong {
            font-size: 13.5px;
            color: var(--text-main);
        }
        .step-desc span {
            font-size: 12px;
            color: var(--text-muted);
            line-height: 1.4;
        }
        body.theme-light .how-step {
            background: #ffffff;
            border-color: #e2e8f0;
            box-shadow: 0 4px 16px rgba(15, 23, 42, 0.05);
        }
        body.theme-light .step-desc strong {
            color: #0f172a;
        }
        body.theme-light .step-desc span {
            color: #64748b;
        }

        @media (max-width: 768px) {
            .how-it-works-strip {
                grid-template-columns: 1fr;
                gap: 10px;
                padding: 0 16px;
                margin-bottom: 20px;
            }
        }
'''

    if '/* Badges de Modalidad y Nuevas Categorías */' not in html:
        idx_style_close = html.find('</style>')
        assert idx_style_close != -1
        html = html[:idx_style_close] + new_css + '\n    ' + html[idx_style_close:]

    # 2. Insertar Barra de 3 Pasos
    how_it_works_html = '''
    <!-- Barra Explicativa de 3 Pasos -->
    <div class="how-it-works-strip">
        <div class="how-step">
            <span class="step-num">1</span>
            <div class="step-desc">
                <strong>Rastreo Oficial 24/7</strong>
                <span>Monitorizamos BOE, DGT, Vivienda Protegida y Fondos de Decomisos.</span>
            </div>
        </div>
        <div class="how-step">
            <span class="step-num">2</span>
            <div class="step-desc">
                <strong>2 Modalidades Claras</strong>
                <span><strong style="color: #38bdf8;">🔨 Subastas</strong> (pujas) o <strong style="color: #10b981;">📋 Solicitud Directa</strong> (inscripción 100% gratis).</span>
            </div>
        </div>
        <div class="how-step">
            <span class="step-num">3</span>
            <div class="step-desc">
                <strong>Sin Intermediarios</strong>
                <span>Desbloqueas el expediente para acceder a la sede electrónica oficial.</span>
            </div>
        </div>
    </div>
'''

    if '<!-- Barra Explicativa de 3 Pasos -->' not in html:
        idx_search_panel = html.find('<section class="search-panel" id="catalogo">')
        assert idx_search_panel != -1, 'search-panel not found'
        html = html[:idx_search_panel] + how_it_works_html + '\n    ' + html[idx_search_panel:]

    # 3. Pestañas de categoría
    old_tabs = '''        <div class="category-tabs">
            <button class="tab-btn active" onclick="setCategory('all', this)">⚡ Todas las Oportunidades</button>
            <button class="tab-btn" onclick="setCategory('empleo', this)">💼 Empleo Público (BOE)</button>
            <button class="tab-btn" onclick="setCategory('vehiculo', this)">🚗 Coches Embargados (DGT/BOE)</button>
            <button class="tab-btn" onclick="setCategory('inmueble', this)">🏢 Pisos y Chalets (BOE)</button>
            <button class="tab-btn" onclick="setCategory('ayuda', this)">💶 Ayudas a Fondo Perdido</button>
            <button class="tab-btn" onclick="setCategory('licitacion', this)">📋 Licitaciones Menores</button>
        </div>'''

    new_tabs = '''        <div class="category-tabs">
            <button class="tab-btn active" onclick="setCategory('all', this)">⚡ Todo el Radar (26)</button>
            <button class="tab-btn" onclick="setCategory('vivienda', this)">🏠 Alquiler & VPO (400€)</button>
            <button class="tab-btn" onclick="setCategory('vehiculo', this)">🚗 Coches & Decomisos</button>
            <button class="tab-btn" onclick="setCategory('empleo', this)">💼 Empleo Sin Examen</button>
            <button class="tab-btn" onclick="setCategory('inmueble', this)">🏛️ Subastas Pisos BOE</button>
            <button class="tab-btn" onclick="setCategory('ayuda', this)">💰 Ayudas & Bonos</button>
        </div>'''

    if old_tabs in html:
        html = html.replace(old_tabs, new_tabs)

    # 4. Chips rápidos
    old_chips = '''        <!-- Chips de Filtros Rápidos -->
        <div class="quick-filter-chips">
            <span class="chip-label">Filtros exprés:</span>
            <button class="chip-btn" id="chipBolsas" onclick="aplicarFiltroRapido('bolsas')">💼 Bolsas sin Oposición</button>
            <button class="chip-btn" id="chipCoches" onclick="aplicarFiltroRapido('coches_baratos')">🚗 Coches &lt; 3.000 €</button>
            <button class="chip-btn" id="chipDescuentos" onclick="aplicarFiltroRapido('descuento_top')">🔥 Chollos &gt; 70% Ahorro</button>
            <button class="chip-btn chip-clear" id="btnLimpiarChips" onclick="limpiarFiltrosRapidos()" style="display: none;">✖ Ver Todo</button>
        </div>'''

    new_chips = '''        <!-- Chips de Filtros Rápidos -->
        <div class="quick-filter-chips">
            <span class="chip-label">Filtros exprés:</span>
            <button class="chip-btn" id="chipVpo" onclick="aplicarFiltroRapido('alquiler_vpo')">🏠 Alquiler Protegido</button>
            <button class="chip-btn" id="chipDecomisos" onclick="aplicarFiltroRapido('decomisos_lujo')">🏎️ Decomisos del Estado</button>
            <button class="chip-btn" id="chipBolsas" onclick="aplicarFiltroRapido('bolsas')">💼 Bolsas Sin Oposición</button>
            <button class="chip-btn" id="chipDescuentos" onclick="aplicarFiltroRapido('descuento_top')">🔥 Chollos &gt; 70% Ahorro</button>
            <button class="chip-btn chip-clear" id="btnLimpiarChips" onclick="limpiarFiltrosRapidos()" style="display: none;">✖ Ver Todo</button>
        </div>'''

    if old_chips in html:
        html = html.replace(old_chips, new_chips)

    # 5. generarBannerAhorro en JS
    old_generar_banner = '''function generarBannerAhorro(item) {
            if (item.tipo === 'empleo') {
                return `<div class="savings-pill-banner employment"><span>💼 Salario Oficial Fijo:</span> <strong>${item.precioBoe} (14 Pagas)</strong></div>`;
            }
            if (item.tipo === 'ayuda') {
                return `<div class="savings-pill-banner grant"><span>💰 Subvención Directa:</span> <strong>Hasta ${item.precioBoe} (A Fondo Perdido)</strong></div>`;
            }
            if (item.tipo === 'licitacion') {
                return `<div class="savings-pill-banner grant"><span>📑 Presupuesto Adjudicación:</span> <strong>${item.precioBoe} (Pago Garantizado)</strong></div>`;
            }'''

    new_generar_banner = '''function generarBannerAhorro(item) {
            if (item.tipo === 'vivienda') {
                return `<div class="savings-pill-banner housing"><span>🏠 Alquiler Regulado Oficial:</span> <strong>${item.precioBoe} (-60% Ahorro)</strong></div>`;
            }
            if (item.tipo === 'empleo') {
                return `<div class="savings-pill-banner employment"><span>💼 Salario Oficial Fijo:</span> <strong>${item.precioBoe} (14 Pagas)</strong></div>`;
            }
            if (item.tipo === 'ayuda') {
                return `<div class="savings-pill-banner grant"><span>💰 Subvención Directa:</span> <strong>Hasta ${item.precioBoe} (A Fondo Perdido)</strong></div>`;
            }
            if (item.tipo === 'licitacion') {
                return `<div class="savings-pill-banner grant"><span>📑 Presupuesto Adjudicación:</span> <strong>${item.precioBoe} (Pago Garantizado)</strong></div>`;
            }'''

    if old_generar_banner in html:
        html = html.replace(old_generar_banner, new_generar_banner)

    # 6. Filtros rápidos en JS
    old_filtros_js = '''                let matchRapido = true;
                if (filtroRapidoActual === 'bolsas') {
                    matchRapido = item.tipo === 'empleo';
                } else if (filtroRapidoActual === 'coches_baratos') {
                    const boeVal = parseEuro(item.precioBoe);
                    matchRapido = item.tipo === 'vehiculo' && boeVal > 0 && boeVal <= 3000;
                } else if (filtroRapidoActual === 'descuento_top') {
                    const ahorroStr = item.ahorro || '';
                    matchRapido = ahorroStr.includes('-70%') || ahorroStr.includes('-80%') || ahorroStr.includes('-85%') || ahorroStr.includes('-90%') || ahorroStr.includes('CHOLLO');
                }'''

    new_filtros_js = '''                let matchRapido = true;
                if (filtroRapidoActual === 'alquiler_vpo') {
                    matchRapido = item.tipo === 'vivienda';
                } else if (filtroRapidoActual === 'decomisos_lujo') {
                    const tagStr = (item.tag || '').toUpperCase();
                    const titStr = (item.titulo || '').toUpperCase();
                    matchRapido = item.tipo === 'vehiculo' && (tagStr.includes('DECOMISO') || titStr.includes('DECOMISO'));
                } else if (filtroRapidoActual === 'bolsas') {
                    matchRapido = item.tipo === 'empleo';
                } else if (filtroRapidoActual === 'descuento_top') {
                    const ahorroStr = item.ahorro || '';
                    matchRapido = ahorroStr.includes('-70%') || ahorroStr.includes('-80%') || ahorroStr.includes('-85%') || ahorroStr.includes('-90%') || ahorroStr.includes('CHOLLO');
                }'''

    if old_filtros_js in html:
        html = html.replace(old_filtros_js, new_filtros_js)

    # 7. Renderizado de tarjeta con badges y textos de modalidad
    old_card_head = '''grid.innerHTML = filtradas.map(item => `
                <article class="card">
                    <div class="card-img" style="background-image: url('${item.img}');">
                        <span class="card-tag ${item.tagClass}">${item.tag}</span>
                        ${item.badgeVisual ? `<span class="badge-brand-pill">${item.badgeVisual}</span>` : ''}
                        <span class="discount-badge">${item.ahorro}</span>
                    </div>'''

    new_card_head = '''grid.innerHTML = filtradas.map(item => {
                const esDirecta = item.modalidad === 'directa';
                const modBadgeClass = esDirecta ? 'badge-mod-directa' : 'badge-mod-subasta';
                const modBadgeText = esDirecta ? '📋 SOLICITUD DIRECTA' : '🔨 SUBASTA PÚBLICA';
                const labelMercado = esDirecta ? (item.tipo === 'vivienda' ? 'Alquiler Libre' : 'Sin Alerta') : 'Mercado Libre';
                const labelOficial = esDirecta ? (item.tipo === 'vivienda' ? 'Alquiler Protegido' : 'Oficial Estado') : 'Precio Salida';
                const ctaBtnText = item.ctaLabel || (esDirecta ? '📋 Desbloquear Solicitud y Requisitos • 2,90 €' : '🔨 Desbloquear Expediente • 2,90 €');

                return `
                <article class="card">
                    <div class="card-img" style="background-image: url('${item.img}');">
                        <span class="card-tag ${item.tagClass}">${item.tag}</span>
                        <span class="card-modality-badge ${modBadgeClass}">${modBadgeText}</span>
                        ${item.badgeVisual ? `<span class="badge-brand-pill">${item.badgeVisual}</span>` : ''}
                        <span class="discount-badge">${item.ahorro}</span>
                    </div>'''

    if old_card_head in html:
        html = html.replace(old_card_head, new_card_head)

    # Precios
    old_prices = '''                        <div class="prices-box">
                            <div class="market-p">
                                <span class="market-label">Mercado Libre</span>
                                <span class="market-val">${item.precioMercado}</span>
                            </div>
                            <div class="boe-p">
                                <span class="boe-label">Precio Salida</span>
                                <span class="boe-val">${item.precioBoe}</span>
                            </div>
                        </div>'''

    new_prices = '''                        <div class="prices-box">
                            <div class="market-p">
                                <span class="market-label">${labelMercado}</span>
                                <span class="market-val">${item.precioMercado}</span>
                            </div>
                            <div class="boe-p">
                                <span class="boe-label">${labelOficial}</span>
                                <span class="boe-val">${item.precioBoe}</span>
                            </div>
                        </div>'''

    if old_prices in html:
        html = html.replace(old_prices, new_prices)

    # Botón desbloqueo
    old_unlock_btn = '''                                        🔓 Desbloquear Expediente • 2,90 €
                                    </button>'''

    new_unlock_btn = '''                                        ${ctaBtnText}
                                    </button>'''

    if old_unlock_btn in html:
        html = html.replace(old_unlock_btn, new_unlock_btn)

    # Cierre de función map
    old_map_tail = '''                        <button class="btn-share-wa" onclick="compartirCholloWhatsApp('${encodeURIComponent(item.titulo)}', '${item.precioBoe}', '${item.ahorro}')">
                            <span>📲 Avisar por WhatsApp a un amigo</span>
                        </button>
                    </div>
                </article>
            `).join('');'''

    new_map_tail = '''                        <button class="btn-share-wa" onclick="compartirCholloWhatsApp('${encodeURIComponent(item.titulo)}', '${item.precioBoe}', '${item.ahorro}')">
                            <span>📲 Avisar por WhatsApp a un amigo</span>
                        </button>
                    </div>
                </article>
                `;
            }).join('');'''

    if old_map_tail in html:
        html = html.replace(old_map_tail, new_map_tail)

    with open(docs_path, 'w', encoding='utf-8') as f:
        f.write(html)
    with open(root_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print('docs/index.html and root index.html updated successfully with new categories, modalities and visual guide!')

if __name__ == '__main__':
    main()
