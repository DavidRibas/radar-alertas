from playwright.sync_api import sync_playwright
import os

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 950})
        html_file = os.path.abspath("docs/index.html").replace("\\", "/")
        file_path = f"file:///{html_file}"
        page.goto(file_path)
        page.wait_for_timeout(600)

        # 1. Comprobar barra de 3 pasos
        strip = page.locator(".how-it-works-strip")
        assert strip.is_visible(), "La barra de 3 pasos debe ser visible"
        print("Barra de 3 pasos visible con éxito.")

        # Captura de la barra explicativa
        page.screenshot(path="C:/Users/DRA/.gemini/antigravity/brain/57493430-4498-4ef1-aae2-14f86664084c/BARRA_EXPLICATIVA_3_PASOS.png")

        # 2. Filtrar por Vivienda VPO
        tab_vivienda = page.locator("button:has-text('Alquiler & VPO')")
        assert tab_vivienda.is_visible(), "Pestaña Vivienda VPO no encontrada"
        tab_vivienda.click()
        page.wait_for_timeout(400)

        # Verificar que se muestran tarjetas de VPO
        cards_vpo = page.locator("#cardsGrid article.card")
        count_vpo = cards_vpo.count()
        print("Tarjetas mostradas en Alquiler & VPO:", count_vpo)
        assert count_vpo >= 3, "Deben mostrarse al menos 3 promociones de VPO"

        # Verificar que tienen el badge de SOLICITUD DIRECTA
        directa_badge = page.locator(".badge-mod-directa").first
        assert directa_badge.is_visible(), "El badge de SOLICITUD DIRECTA debe ser visible"
        print("Badge SOLICITUD DIRECTA verificado:", directa_badge.inner_text())

        # Captura catálogo Vivienda VPO
        page.screenshot(path="C:/Users/DRA/.gemini/antigravity/brain/57493430-4498-4ef1-aae2-14f86664084c/CATALOGO_VIVIENDA_VPO_DESKTOP.png")

        # 3. Filtrar por Coches & Decomisos
        tab_coches = page.locator("button:has-text('Coches & Decomisos')")
        tab_coches.click()
        page.wait_for_timeout(400)

        cards_coches = page.locator("#cardsGrid article.card")
        count_coches = cards_coches.count()
        print("Tarjetas mostradas en Coches & Decomisos:", count_coches)
        assert count_coches >= 5, "Deben mostrarse coches y decomisos"

        # Verificar badge SUBASTA PÚBLICA
        subasta_badge = page.locator(".badge-mod-subasta").first
        assert subasta_badge.is_visible(), "El badge de SUBASTA PÚBLICA debe ser visible"
        print("Badge SUBASTA PÚBLICA verificado:", subasta_badge.inner_text())

        # Captura catálogo Coches & Decomisos
        page.screenshot(path="C:/Users/DRA/.gemini/antigravity/brain/57493430-4498-4ef1-aae2-14f86664084c/CATALOGO_DECOMISOS_DESKTOP.png")

        # 4. Modo móvil (390 x 844) en Vivienda
        page_mob = browser.new_page(viewport={"width": 390, "height": 844})
        page_mob.goto(file_path)
        page_mob.wait_for_timeout(600)
        page_mob.locator("button:has-text('Alquiler & VPO')").click()
        page_mob.wait_for_timeout(400)
        page_mob.screenshot(path="C:/Users/DRA/.gemini/antigravity/brain/57493430-4498-4ef1-aae2-14f86664084c/CATALOGO_VIVIENDA_MOBILE.png")
        print("Captura móvil de Vivienda VPO tomada.")

        # 5. Modo Claro en Alquiler & VPO
        page.locator("#btnThemeToggle").click()
        page.wait_for_timeout(400)
        tab_vivienda.click()
        page.wait_for_timeout(400)
        page.screenshot(path="C:/Users/DRA/.gemini/antigravity/brain/57493430-4498-4ef1-aae2-14f86664084c/VIVIENDA_VPO_MODO_CLARO.png")
        print("Captura Vivienda VPO en Modo Claro tomada.")

        browser.close()
    print("VERIFICACION E2E DE NUEVAS CATEGORIAS Y MODALIDADES 100% EXITOSA")

if __name__ == "__main__":
    test()
