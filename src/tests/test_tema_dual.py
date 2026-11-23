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

        # 1. Comprobar botón PWA visible en la cabecera
        pwa_btn = page.locator("#btnPwaNav")
        assert pwa_btn.is_visible(), "El botón App Móvil debe ser visible"
        print("Botón App Móvil visible:", pwa_btn.inner_text())

        # 2. Comprobar que al pulsar abre el modal oficial de instalación
        pwa_btn.click()
        page.wait_for_timeout(500)
        modal_pwa = page.locator("#modalPwaInstructions")
        assert modal_pwa.is_visible(), "El modal de instrucciones de la App no se abrió"
        print("Modal de instalación PWA verificado con éxito.")

        # Captura con el modal PWA abierto
        page.screenshot(path="C:/Users/DRA/.gemini/antigravity/brain/57493430-4498-4ef1-aae2-14f86664084c/MODAL_APP_MOVIL_VERIFICADO.png")

        # Cerrar modal
        page.locator("#modalPwaInstructions .modal-close").click()
        page.wait_for_timeout(300)

        # 3. Captura escritorio con App Móvil + Selector Claro/Oscuro + Plan PRO
        page.screenshot(path="C:/Users/DRA/.gemini/antigravity/brain/57493430-4498-4ef1-aae2-14f86664084c/CABECERA_CON_APP_MOVIL.png")
        print("Captura con App Móvil tomada.")

        # 4. Modo móvil
        page_mob = browser.new_page(viewport={"width": 390, "height": 844})
        page_mob.goto(file_path)
        page_mob.wait_for_timeout(1500) # Esperar a que salga también el banner inferior PWA
        page_mob.screenshot(path="C:/Users/DRA/.gemini/antigravity/brain/57493430-4498-4ef1-aae2-14f86664084c/MOBILE_APP_BANNER_VERIFICADO.png")
        print("Captura móvil con banner y botón PWA tomada.")

        browser.close()
    print("VERIFICACION PWA Y CABECERA 100% EXITOSA")

if __name__ == "__main__":
    test()
