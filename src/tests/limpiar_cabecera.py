import os

def update_header():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    docs_path = os.path.join(base_dir, 'docs', 'index.html')
    root_path = os.path.join(base_dir, 'index.html')

    with open(docs_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update CSS for nav-actions and new theme-switch
    old_css_anchor = '/* Botón Modo Claro / Oscuro Dual */'
    idx_css = html.find(old_css_anchor)
    assert idx_css != -1, 'old_css_anchor not found'
    
    # Find where media query begins or where hero begins
    idx_hero = html.find('/* Hero */', idx_css)
    assert idx_hero != -1, 'idx_hero not found'

    new_css = '''/* Switch Moderno Claro / Oscuro (Universal & Elegante) */
        .theme-switch-btn {
            position: relative;
            display: inline-flex;
            align-items: center;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.16);
            border-radius: 999px;
            padding: 3px;
            cursor: pointer;
            transition: all 0.25s ease;
            user-select: none;
            outline: none;
        }
        .theme-switch-btn:hover {
            border-color: rgba(255, 255, 255, 0.35);
        }
        .theme-opt {
            position: relative;
            z-index: 2;
            padding: 5px 12px;
            font-size: 12px;
            font-weight: 700;
            color: #94a3b8;
            transition: color 0.25s ease;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }
        .theme-opt.active {
            color: #ffffff;
        }
        .theme-slider {
            position: absolute;
            top: 3px;
            bottom: 3px;
            left: 3px;
            width: calc(50% - 3px);
            border-radius: 999px;
            background: #1e293b;
            border: 1px solid rgba(255, 255, 255, 0.18);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.35);
            transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            z-index: 1;
        }
        /* Por defecto en modo oscuro: slider a la derecha */
        body:not(.theme-light) .theme-slider {
            transform: translateX(100%);
            background: #1e293b;
        }
        /* En modo claro: slider a la izquierda */
        body.theme-light .theme-slider {
            transform: translateX(0);
            background: #ffffff;
            border-color: #cbd5e1;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.12);
        }
        body.theme-light .theme-switch-btn {
            background: #e2e8f0;
            border-color: #cbd5e1;
        }
        body.theme-light .theme-opt {
            color: #64748b;
        }
        body.theme-light .theme-opt.active {
            color: #0f172a;
        }

        /* Estilo Limpio Botón PRO en Nav */
        .btn-pro-nav {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            color: #ffffff;
            font-size: 12.5px;
            font-weight: 800;
            padding: 7px 16px;
            border-radius: 999px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            box-shadow: 0 2px 10px rgba(245, 158, 11, 0.3);
            transition: all 0.2s ease;
            white-space: nowrap;
            border: none;
        }
        .btn-pro-nav:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 14px rgba(245, 158, 11, 0.5);
        }

        @media (max-width: 900px) {
            .nav-links { display: none; }
        }
        @media (max-width: 540px) {
            .theme-opt {
                padding: 4px 8px;
                font-size: 11px;
            }
            .btn-pro-nav {
                padding: 6px 12px;
                font-size: 11.5px;
            }
        }
        
        '''

    html = html[:idx_css] + new_css + html[idx_hero:]

    # 2. Update Header HTML
    idx_header_start = html.find('<header>')
    idx_header_end = html.find('</header>') + len('</header>')
    assert idx_header_start != -1 and idx_header_end != -1, 'header not found'

    new_header = '''<header>
        <div class="nav-wrap">
            <a href="#" class="brand">
                <div class="brand-icon">⚡</div>
                RadarAlertas
            </a>
            <nav class="nav-links">
                <a href="#catalogo" class="nav-link">Catálogo de Chollos</a>
                <a href="#calculadora" class="nav-link">Calculadora LEC</a>
                <a href="#planes" class="nav-link">Planes & Precios</a>
                <a href="javascript:void(0)" onclick="abrirModalTutorial()" class="nav-link" style="color: #38bdf8;">▶ Vídeo Tutorial</a>
            </nav>
            <div class="nav-actions">
                <!-- Selector Deslizante Claro / Oscuro -->
                <button id="btnThemeToggle" onclick="alternarTema()" class="theme-switch-btn" title="Alternar entre Modo Claro y Oscuro" type="button" aria-label="Cambiar tema">
                    <span class="theme-slider" id="themeSlider"></span>
                    <span class="theme-opt opt-light" id="themeOptLight">☀️ Claro</span>
                    <span class="theme-opt opt-dark active" id="themeOptDark">🌙 Oscuro</span>
                </button>
                <a href="#planes" class="btn-pro-nav">
                    ⭐ Plan PRO
                </a>
                <button id="btnPwaNav" onclick="iniciarInstalacionPwa()" class="btn-pwa-nav" style="display:none;">
                    📲 Instalar App
                </button>
            </div>
        </div>
    </header>'''

    html = html[:idx_header_start] + new_header + html[idx_header_end:]

    # 3. Update aplicarTema JS
    idx_fn_start = html.find('function aplicarTema(')
    assert idx_fn_start != -1, 'aplicarTema not found'
    idx_fn_end = html.find('function cerrarModales()', idx_fn_start)
    assert idx_fn_end != -1, 'cerrarModales not found'

    new_js_theme = '''function aplicarTema(tema) {
            const body = document.body;
            const optLight = document.getElementById('themeOptLight');
            const optDark = document.getElementById('themeOptDark');

            if (tema === 'light') {
                body.classList.add('theme-light');
                if (optLight) optLight.classList.add('active');
                if (optDark) optDark.classList.remove('active');
                localStorage.setItem('radar_theme', 'light');
            } else {
                body.classList.remove('theme-light');
                if (optLight) optLight.classList.remove('active');
                if (optDark) optDark.classList.add('active');
                localStorage.setItem('radar_theme', 'dark');
            }
        }

        function alternarTema() {
            const esLight = document.body.classList.contains('theme-light');
            aplicarTema(esLight ? 'dark' : 'light');
        }

        function inicializarTema() {
            const guardado = localStorage.getItem('radar_theme');
            if (guardado === 'light') {
                aplicarTema('light');
            } else {
                aplicarTema('dark');
            }
        }

        '''

    html = html[:idx_fn_start] + new_js_theme + html[idx_fn_end:]

    with open(docs_path, 'w', encoding='utf-8') as f:
        f.write(html)
    with open(root_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print('Updated docs/index.html and root index.html with clean navbar and universal switch!')

if __name__ == '__main__':
    update_header()
