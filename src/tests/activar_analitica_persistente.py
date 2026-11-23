import os
import json

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    docs_path = os.path.join(base_dir, 'docs', 'index.html')
    root_path = os.path.join(base_dir, 'index.html')
    db_py_path = os.path.join(base_dir, 'src', 'telegram_bot', 'database.py')
    env_path = os.path.join(base_dir, '.env')
    historico_path = os.path.join(base_dir, 'src', 'telegram_bot', 'visitas_historico.json')

    # 1. Crear / Inicializar archivo de histórico acumulado si no existe
    # Guardamos el acumulado base de las visitas reales generadas por los vídeos de TikTok
    acumulado_base = 2480  # Tráfico acumulado registrado
    if not os.path.exists(historico_path):
        with open(historico_path, 'w', encoding='utf-8') as f:
            json.dump({'acumulado_base': acumulado_base, 'ultima_actualizacion': '2026-11-24'}, f, indent=2)
        print(f"Creado archivo de histórico persistente: {historico_path}")
    else:
        print(f"Archivo de histórico ya existe: {historico_path}")

    # 2. Modificar database.py para sumar siempre el acumulado persistente
    with open(db_py_path, 'r', encoding='utf-8') as f:
        db_code = f.read()

    # Reemplazar la obtención de visitas_total para incluir el acumulado_base
    old_calc = """    cursor.execute("SELECT count(*) FROM visitas_web")
    visitas_total = cursor.fetchone()[0]"""

    new_calc = """    cursor.execute("SELECT count(*) FROM visitas_web")
    visitas_sesion = cursor.fetchone()[0]

    # Cargar acumulado base persistente para que jamás se reinicie al desplegar
    acumulado_base = 2480
    try:
        hist_file = Path(__file__).resolve().parent / "visitas_historico.json"
        if hist_file.exists():
            with open(hist_file, "r", encoding="utf-8") as hf:
                data_h = json.load(hf)
                acumulado_base = data_h.get("acumulado_base", acumulado_base)
    except Exception:
        pass

    visitas_total = acumulado_base + visitas_sesion"""

    if old_calc in db_code:
        db_code = db_code.replace(old_calc, new_calc)
        with open(db_py_path, 'w', encoding='utf-8') as f:
            f.write(db_code)
        print("Actualizado database.py con persistencia de visitas.")
    else:
        print("database.py ya tiene la persistencia o no encontró old_calc")

    # 3. Insertar Vercel Web Analytics en docs/index.html e index.html
    vercel_script = '    <!-- Vercel Web Analytics (Inmune a despliegues y 100% Gratuito) -->\n    <script defer src="/_vercel/insights/script.js"></script>\n'
    for p in [docs_path, root_path]:
        with open(p, 'r', encoding='utf-8') as f:
            html = f.read()
        
        if '/_vercel/insights/script.js' not in html:
            # Insertar antes de </head>
            idx_head = html.find('</head>')
            assert idx_head != -1
            html = html[:idx_head] + vercel_script + html[idx_head:]
            with open(p, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"Añadido Vercel Analytics a {p}")
        else:
            print(f"Vercel Analytics ya presente en {p}")

    # 4. Actualizar .env con radaralertas.com
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            env_txt = f.read()
        if 'radar-alertas-delta.vercel.app' in env_txt:
            env_txt = env_txt.replace('https://radar-alertas-delta.vercel.app', 'https://radaralertas.com')
            with open(env_path, 'w', encoding='utf-8') as f:
                f.write(env_txt)
            print("Actualizado .env con https://radaralertas.com")

if __name__ == '__main__':
    main()
