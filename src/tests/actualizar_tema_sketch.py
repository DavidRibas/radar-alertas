import os

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    docs_path = os.path.join(base_dir, 'docs', 'index.html')
    root_path = os.path.join(base_dir, 'index.html')

    with open(docs_path, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. Update button in HTML
    old_btn = '''<button id="btnThemeToggle" onclick="alternarTema()" class="btn-theme-toggle" title="Cambiar a Modo Claro / Oscuro">
                    <span id="themeToggleIcon">☀️</span>
                    <span id="themeToggleText">Modo Claro</span>
                </button>'''

    new_btn = '''<button id="btnThemeToggle" onclick="alternarTema()" class="btn-theme-toggle" title="Alternar entre Modo LegalTech (Claro) y Terminal (Oscuro)">
                    <span id="themeToggleIcon">☀️</span>
                    <span id="themeToggleText">LegalTech</span>
                </button>'''

    assert old_btn in c, 'old_btn not found'
    c = c.replace(old_btn, new_btn)

    # 2. Update aplicarTema in JS
    old_fn = '''        function aplicarTema(tema) {
            const body = document.body;
            const icon = document.getElementById('themeToggleIcon');
            const txt = document.getElementById('themeToggleText');
            if (tema === 'light') {
                body.classList.add('theme-light');
                if (icon) icon.textContent = '🌙';
                if (txt) txt.textContent = 'Modo Oscuro';
                localStorage.setItem('radar_theme', 'light');
            } else {
                body.classList.remove('theme-light');
                if (icon) icon.textContent = '☀️';
                if (txt) txt.textContent = 'Modo Claro';
                localStorage.setItem('radar_theme', 'dark');
            }
        }'''

    new_fn = '''        function aplicarTema(tema) {
            const body = document.body;
            const icon = document.getElementById('themeToggleIcon');
            const txt = document.getElementById('themeToggleText');
            if (tema === 'light') {
                body.classList.add('theme-light');
                if (icon) icon.textContent = '⚡';
                if (txt) txt.textContent = 'Terminal';
                localStorage.setItem('radar_theme', 'light');
            } else {
                body.classList.remove('theme-light');
                if (icon) icon.textContent = '☀️';
                if (txt) txt.textContent = 'LegalTech';
                localStorage.setItem('radar_theme', 'dark');
            }
        }'''

    assert old_fn in c, 'old_fn not found'
    c = c.replace(old_fn, new_fn)

    # 3. Add extra theme-light styles & mobile styles
    extra_styles = '''
        body.theme-light .savings-pill-banner {
            background: #ecfdf5;
            border-color: #a7f3d0;
            color: #065f46;
        }
        body.theme-light .savings-pill-banner.employment {
            background: #fff1f2;
            border-color: #fecdd3;
            color: #9f1239;
        }
        body.theme-light .savings-pill-banner.grant {
            background: #f5f3ff;
            border-color: #ddd6fe;
            color: #5b21b6;
        }
        body.theme-light .legal-check {
            color: #1e3a8a;
            background: #eff6ff;
            border: 1px solid #bfdbfe;
        }

        @media (max-width: 640px) {
            .nav-actions .btn-tutorial-nav,
            .nav-actions .btn-wa,
            .nav-actions .btn-tg {
                display: none;
            }
            .btn-theme-toggle {
                padding: 6px 11px;
                font-size: 11px;
            }
            .btn-pwa-nav {
                padding: 6px 11px;
                font-size: 11px;
            }
        }
'''

    anchor = 'body.theme-light .modal-item-name {'
    idx = c.find(anchor)
    assert idx != -1, 'anchor not found'
    end_rule = c.find('}', idx) + 1
    c = c[:end_rule] + extra_styles + c[end_rule:]

    with open(docs_path, 'w', encoding='utf-8') as f:
        f.write(c)

    with open(root_path, 'w', encoding='utf-8') as f:
        f.write(c)

    print('Updated docs/index.html and index.html successfully')

if __name__ == '__main__':
    main()
