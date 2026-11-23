import os

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    docs_path = os.path.join(base_dir, 'docs', 'index.html')
    root_path = os.path.join(base_dir, 'index.html')

    # CSS a añadir
    trend_css = '''
        /* Píldora de Tendencia Empleo en Hero */
        .trend-callout {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            background: rgba(244, 63, 94, 0.12);
            border: 1px solid rgba(244, 63, 94, 0.35);
            padding: 8px 18px;
            border-radius: 999px;
            cursor: pointer;
            margin: 16px auto 0;
            transition: all 0.25s ease;
            text-decoration: none;
            max-width: 95%;
        }
        .trend-callout:hover {
            background: rgba(244, 63, 94, 0.22);
            border-color: rgba(244, 63, 94, 0.6);
            transform: translateY(-2px);
            box-shadow: 0 4px 18px rgba(244, 63, 94, 0.25);
        }
        .trend-badge {
            background: #f43f5e;
            color: #ffffff;
            font-size: 10.5px;
            font-weight: 900;
            padding: 3px 8px;
            border-radius: 999px;
            letter-spacing: 0.5px;
            flex-shrink: 0;
        }
        .trend-text {
            font-size: 13px;
            font-weight: 600;
            color: #fecdd3;
        }
        .trend-cta {
            font-size: 12px;
            font-weight: 800;
            color: #fb7185;
            text-decoration: underline;
            margin-left: 4px;
            flex-shrink: 0;
        }
        body.theme-light .trend-callout {
            background: #fff1f2;
            border-color: #fecdd3;
            box-shadow: 0 2px 10px rgba(244, 63, 94, 0.08);
        }
        body.theme-light .trend-text {
            color: #9f1239;
        }
        body.theme-light .trend-cta {
            color: #e11d48;
        }

        .hot-pill {
            background: #f43f5e;
            color: #ffffff;
            font-size: 9.5px;
            font-weight: 900;
            padding: 2px 7px;
            border-radius: 999px;
            margin-left: 6px;
            letter-spacing: 0.4px;
        }
'''

    # HTML de la píldora en Hero
    trend_html = '''
        <!-- Píldora de Tendencia Empleo -->
        <div>
            <div class="trend-callout" onclick="irACategoriaEmpleo()" role="button" title="Ver Convocatorias de Empleo Público en Directo">
                <span class="trend-badge">🔥 MÁS BUSCADO HOY</span>
                <span class="trend-text">Bolsas de Empleo del Estado (+2.150 €/mes sin oposición)</span>
                <span class="trend-cta">Ver Plazas →</span>
            </div>
        </div>
'''

    # Función JS para ir a categoría empleo
    js_empleo = '''
        function irACategoriaEmpleo() {
            const tab = document.getElementById('tabEmpleo');
            if (tab) setCategory('empleo', tab);
            const seccion = document.getElementById('catalogo');
            if (seccion) seccion.scrollIntoView({ behavior: 'smooth' });
        }
'''

    for path in [docs_path, root_path]:
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()

        # 1. Insertar CSS si no está
        if '/* Píldora de Tendencia Empleo en Hero */' not in html:
            idx_css = html.find('</style>')
            assert idx_css != -1
            html = html[:idx_css] + trend_css + '\n    ' + html[idx_css:]

        # 2. Insertar HTML en Hero justo después de <p>Monitorizamos...
        anchor_hero = '</p>\n\n        <!-- Botón Destacado de Vídeo Tutorial -->'
        if anchor_hero in html:
            html = html.replace(anchor_hero, '</p>' + trend_html + '\n        <!-- Botón Destacado de Vídeo Tutorial -->')

        # 3. Actualizar pestaña de categoría para que Empleo vaya en 2ª posición con badge
        old_tabs_block = '''        <div class="category-tabs">
            <button class="tab-btn active" onclick="setCategory('all', this)">⚡ Todo el Radar (26)</button>
            <button class="tab-btn" onclick="setCategory('vivienda', this)">🏠 Alquiler & VPO (400€)</button>
            <button class="tab-btn" onclick="setCategory('vehiculo', this)">🚗 Coches & Decomisos</button>
            <button class="tab-btn" onclick="setCategory('empleo', this)">💼 Empleo Sin Examen</button>
            <button class="tab-btn" onclick="setCategory('inmueble', this)">🏛️ Subastas Pisos BOE</button>
            <button class="tab-btn" onclick="setCategory('ayuda', this)">💰 Ayudas & Bonos</button>
        </div>'''

        new_tabs_block = '''        <div class="category-tabs">
            <button class="tab-btn active" onclick="setCategory('all', this)">⚡ Todo el Radar (26)</button>
            <button class="tab-btn" id="tabEmpleo" onclick="setCategory('empleo', this)">💼 Empleo Sin Examen <span class="hot-pill">🔥 POPULAR</span></button>
            <button class="tab-btn" onclick="setCategory('vivienda', this)">🏠 Alquiler & VPO (400€)</button>
            <button class="tab-btn" onclick="setCategory('vehiculo', this)">🚗 Coches & Decomisos</button>
            <button class="tab-btn" onclick="setCategory('inmueble', this)">🏛️ Subastas Pisos BOE</button>
            <button class="tab-btn" onclick="setCategory('ayuda', this)">💰 Ayudas & Bonos</button>
        </div>'''

        if old_tabs_block in html:
            html = html.replace(old_tabs_block, new_tabs_block)

        # 4. Insertar función JS irACategoriaEmpleo y auto-selección por ?cat=empleo
        if 'function irACategoriaEmpleo()' not in html:
            idx_fn = html.find('function setCategory(')
            assert idx_fn != -1
            html = html[:idx_fn] + js_empleo + '\n        ' + html[idx_fn:]

        # Auto-activar ?cat=empleo en la inicialización
        old_init = '''// Inicialización
        inicializarTema();'''
        new_init = '''// Inicialización
        inicializarTema();
        try {
            const urlCat = new URLSearchParams(window.location.search).get('cat');
            if (urlCat === 'empleo') {
                setTimeout(irACategoriaEmpleo, 200);
            }
        } catch(e) {}'''

        if old_init in html:
            html = html.replace(old_init, new_init)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f'Actualizado {path} con destacado de Empleo elegante y minimalista.')

if __name__ == '__main__':
    main()
