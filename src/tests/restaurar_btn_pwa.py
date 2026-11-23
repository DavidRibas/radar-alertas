import os

def update_pwa():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    docs_path = os.path.join(base_dir, 'docs', 'index.html')
    root_path = os.path.join(base_dir, 'index.html')

    with open(docs_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update CSS for btn-pwa-nav so it is always cleanly visible
    old_css = '''.btn-pwa-nav {
            display: none;
            align-items: center;
            gap: 6px;
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(56, 189, 248, 0.2));
            border: 1px solid rgba(16, 185, 129, 0.45);
            color: #34d399;
            padding: 8px 14px;
            border-radius: 9999px;'''

    new_css = '''.btn-pwa-nav {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(16, 185, 129, 0.15);
            border: 1px solid rgba(16, 185, 129, 0.4);
            color: #34d399;
            padding: 7px 14px;
            border-radius: 999px;
            font-size: 12.5px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s ease;
            white-space: nowrap;'''

    assert old_css in html, 'old_css not found'
    html = html.replace(old_css, new_css)

    # 2. Add light-mode style for btn-pwa-nav
    pwa_light_css = '''
        body.theme-light .btn-pwa-nav {
            background: #ecfdf5;
            border-color: #a7f3d0;
            color: #065f46;
        }
        body.theme-light .btn-pwa-nav:hover {
            background: #d1fae5;
        }'''

    idx_theme_light = html.find('body.theme-light .theme-switch-btn')
    assert idx_theme_light != -1, 'body.theme-light .theme-switch-btn not found'
    html = html[:idx_theme_light] + pwa_light_css + '\n        ' + html[idx_theme_light:]

    # 3. Update header HTML to show btnPwaNav without style="display:none;"
    old_header_actions = '''            <div class="nav-actions">
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
            </div>'''

    new_header_actions = '''            <div class="nav-actions">
                <!-- Selector Deslizante Claro / Oscuro -->
                <button id="btnThemeToggle" onclick="alternarTema()" class="theme-switch-btn" title="Alternar entre Modo Claro y Oscuro" type="button" aria-label="Cambiar tema">
                    <span class="theme-slider" id="themeSlider"></span>
                    <span class="theme-opt opt-light" id="themeOptLight">☀️ Claro</span>
                    <span class="theme-opt opt-dark active" id="themeOptDark">🌙 Oscuro</span>
                </button>

                <!-- Botón App Móvil PWA -->
                <button id="btnPwaNav" onclick="iniciarInstalacionPwa()" class="btn-pwa-nav" title="Instalar App en iPhone o Android">
                    📲 App Móvil
                </button>

                <!-- Acceso Plan PRO -->
                <a href="#planes" class="btn-pro-nav">
                    ⭐ Plan PRO
                </a>
            </div>'''

    assert old_header_actions in html, 'old_header_actions not found'
    html = html.replace(old_header_actions, new_header_actions)

    with open(docs_path, 'w', encoding='utf-8') as f:
        f.write(html)
    with open(root_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print('Updated docs/index.html and index.html: btnPwaNav is now always active and visible!')

if __name__ == '__main__':
    update_pwa()
