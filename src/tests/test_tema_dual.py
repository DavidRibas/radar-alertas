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
        assert btn.is_visible(), "El selector de tema no es visible"

        # 2. Captura modo oscuro inicial
        page.screenshot(path="C:/Users/DRA/.gemini/antigravity/brain/57493430-4498-4ef1-aae2-14f86664084c/NUEVA_CABECERA_LIMPIA_OSCURO.png")
        print("Captura cabecera limpia modo oscuro tomada.")

        # 3. Pulsar para cambiar a Modo Claro
        btn.click()
        page.wait_for_timeout(500)
        has_light = page.evaluate("document.body.classList.contains('theme-light')")
        print("Clase theme-light activa:", has_light)
        assert has_light, "No se activó el modo claro"

        # Captura modo claro
        page.screenshot(path="C:/Users/DRA/.gemini/antigravity/brain/57493430-4498-4ef1-aae2-14f86664084c/NUEVA_CABECERA_LIMPIA_CLARO.png")
        print("Captura cabecera limpia modo claro tomada.")

        # 4. Modo móvil
        page_mob = browser.new_page(viewport={"width": 390, "height": 844})
        page_mob.goto(file_path)
        page_mob.wait_for_timeout(500)
        page_mob.screenshot(path="C:/Users/DRA/.gemini/antigravity/brain/57493430-4498-4ef1-aae2-14f86664084c/NUEVA_CABECERA_LIMPIA_MOBILE.png")
        print("Captura cabecera móvil tomada.")

        browser.close()
    print("VERIFICACION CABECERA LIMPIA 100% EXITOSA")

if __name__ == "__main__":
    test()
