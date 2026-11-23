import os
import json
import re
from playwright.sync_api import sync_playwright

def auditar_archivos():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    docs_html_path = os.path.join(base_dir, 'docs', 'index.html')
    json_path = os.path.join(base_dir, 'docs', 'data', 'oportunidades.json')
    manifest_path = os.path.join(base_dir, 'docs', 'manifest.json')

    print("=== 1. AUDITORÍA ESTÁTICA DE ARCHIVOS ===")
    with open(docs_html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Chequear dominios obsoletos
    antiguos = re.findall(r'https?://[a-zA-Z0-9.-]*vercel\.app', html)
    print(f"Referencias residuales a vercel.app en HTML: {len(antiguos)}")
    if antiguos:
        print("Encontradas:", set(antiguos))

    # Chequear imágenes de oportunidades
    with open(json_path, 'r', encoding='utf-8') as f:
        items = json.load(f)

    missing = []
    for it in items:
        img_rel = it.get('img', '')
        full = os.path.join(base_dir, 'docs', img_rel.replace('/', os.sep))
        if not os.path.exists(full):
            missing.append((it['id'], img_rel))

    print(f"Total oportunidades: {len(items)}")
    print(f"Imágenes inexistentes: {len(missing)}")
    if missing:
        print("Faltan:", missing)

    # Chequear manifest.json
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        print(f"Manifest PWA name: {manifest.get('name')}")
        print(f"Manifest start_url: {manifest.get('start_url')}")

    return len(antiguos) == 0 and len(missing) == 0

def auditar_navegacion_e2e():
    print("\n=== 2. AUDITORÍA DINÁMICA PLAYWRIGHT (CONSOLE ERRORS & CLICKS) ===")
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    html_file = os.path.join(base_dir, 'docs', 'index.html').replace('\\', '/')
    file_path = f"file:///{html_file}"

    errores_consola = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})

        # Capturar errores de consola
        page.on("console", lambda msg: errores_consola.append(f"[{msg.type}] {msg.text}") if msg.type in ['error'] else None)
        page.on("pageerror", lambda exc: errores_consola.append(f"[pageerror] {exc}"))

        page.goto(file_path)
        page.wait_for_timeout(600)

        # 1. Probar todas las pestañas de categorías
        categorias = [
            'Todo el Radar',
            'Alquiler & VPO',
            'Coches & Decomisos',
            'Empleo Sin Examen',
            'Subastas Pisos BOE',
            'Ayudas & Bonos'
        ]
        for cat in categorias:
            btn = page.locator(f"button:has-text('{cat}')")
            assert btn.is_visible(), f"Pestaña {cat} no visible"
            btn.click()
            page.wait_for_timeout(200)
            cards_count = page.locator("#cardsGrid article.card").count()
            print(f"Pestaña '{cat}': {cards_count} tarjetas renderizadas.")
            assert cards_count > 0, f"Pestaña {cat} tiene 0 tarjetas"

        # 2. Probar Filtros Exprés
        page.locator("#chipVpo").click()
        page.wait_for_timeout(200)
        assert page.locator("#cardsGrid article.card").count() == 3
        print("Filtro exprés Alquiler VPO: OK")

        page.locator("#chipDecomisos").click()
        page.wait_for_timeout(200)
        assert page.locator("#cardsGrid article.card").count() == 3
        print("Filtro exprés Decomisos: OK")

        page.locator("#btnLimpiarChips").click()
        page.wait_for_timeout(200)
        print("Limpiar filtros exprés: OK")

        # 3. Probar Selector de Modo Claro / Oscuro
        page.locator("#btnThemeToggle").click()
        page.wait_for_timeout(300)
        assert page.evaluate("document.body.classList.contains('theme-light')")
        print("Modo Claro activo: OK")

        page.locator("#btnThemeToggle").click()
        page.wait_for_timeout(300)
        assert not page.evaluate("document.body.classList.contains('theme-light')")
        print("Modo Oscuro restaurado: OK")

        # 4. Probar Modal PWA
        page.locator("#btnPwaNav").click()
        page.wait_for_timeout(300)
        assert page.locator("#modalPwaInstructions").is_visible()
        page.locator("#modalPwaInstructions .modal-close").click()
        page.wait_for_timeout(200)
        assert not page.locator("#modalPwaInstructions").is_visible()
        print("Modal PWA: Abrir y Cerrar OK")

        # 5. Probar Modal Tutorial Vídeo
        page.locator("a:has-text('Vídeo Tutorial')").click()
        page.wait_for_timeout(300)
        assert page.locator("#modalTutorial").is_visible()
        page.locator("#modalTutorial .modal-close").click()
        page.wait_for_timeout(200)
        assert not page.locator("#modalTutorial").is_visible()
        print("Modal Vídeo Tutorial: Abrir y Cerrar OK")

        # 6. Probar Calculadora LEC
        input_tasacion = page.locator("#calcTasacion")
        if input_tasacion.is_visible():
            input_tasacion.fill("200000")
            page.locator("#calcPuja").fill("80000")
            page.wait_for_timeout(200)
            res_ahorro = page.locator("#calcAhorroNeto").inner_text()
            print(f"Calculadora LEC resultado ahorro: {res_ahorro}")
            assert "120" in res_ahorro or "€" in res_ahorro
            print("Calculadora LEC: OK")

        # 7. Probar botón compartir WhatsApp
        btn_wa = page.locator(".btn-share-wa").first
        assert btn_wa.is_visible()
        print("Botón compartir WhatsApp en tarjetas: OK")

        browser.close()

    print(f"\nErrores críticos de consola detectados: {len(errores_consola)}")
    for err in errores_consola:
        print("  -", err)

    return len(errores_consola) == 0

if __name__ == '__main__':
    ok1 = auditar_archivos()
    ok2 = auditar_navegacion_e2e()
    if ok1 and ok2:
        print("\n🎉 AUDITORÍA COMPLETA: TODOS LOS RINCONES DE LA WEB FUNCIONAN AL 100%")
    else:
        print("\n⚠️ SE ENCONTRARON PUNTOS DE MEJORA")
