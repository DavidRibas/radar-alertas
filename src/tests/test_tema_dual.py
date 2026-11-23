from playwright.sync_api import sync_playwright
import os

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        html_file = os.path.abspath("docs/index.html").replace("\\", "/")
        file_path = f"file:///{html_file}"
        page.goto(file_path)
        page.wait_for_timeout(500)

        # 1. Comprobar botón presente
        btn = page.locator("#btnThemeToggle")
        assert btn.is_visible(), "El botón de tema no es visible"
        txt_inicial = btn.inner_text()
        print("Texto inicial en modo oscuro (Terminal):", txt_inicial)
        assert "LegalTech" in txt_inicial, "Debe invitar a pasar a LegalTech"

        # 2. Captura modo oscuro inicial
        page.screenshot(path="C:/Users/DRA/.gemini/antigravity/brain/57493430-4498-4ef1-aae2-14f86664084c/WEB_TEMA_OSCURO_TERMINAL.png")
        print("Captura modo oscuro (Terminal) tomada.")

        # 3. Pulsar para cambiar a Modo Claro (LegalTech)
        btn.click()
        page.wait_for_timeout(500)
        has_light = page.evaluate("document.body.classList.contains('theme-light')")
        print("Clase theme-light activa:", has_light)
        assert has_light, "No se activó el modo claro"

        txt_light = btn.inner_text()
        print("Texto en modo claro (LegalTech):", txt_light)
        assert "Terminal" in txt_light, "Debe invitar a pasar a Terminal"

        # Captura modo claro
        page.screenshot(path="C:/Users/DRA/.gemini/antigravity/brain/57493430-4498-4ef1-aae2-14f86664084c/WEB_TEMA_CLARO_LEGALTECH.png")
        print("Captura modo claro (LegalTech) tomada.")

        # 4. Modo móvil en tema claro
        page_mob = browser.new_page(viewport={"width": 390, "height": 844})
        page_mob.goto(file_path)
        page_mob.wait_for_timeout(500)
        page_mob.click("#btnThemeToggle")
        page_mob.wait_for_timeout(500)
        page_mob.screenshot(path="C:/Users/DRA/.gemini/antigravity/brain/57493430-4498-4ef1-aae2-14f86664084c/WEB_TEMA_CLARO_MOBILE.png")
        print("Captura móvil modo claro tomada.")

        browser.close()
    print("VERIFICACION TEMA DUAL SKETCH 100% EXITOSA")

if __name__ == "__main__":
    test()
