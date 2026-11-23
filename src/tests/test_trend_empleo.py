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

        # 1. Comprobar píldora de tendencia en hero
        callout = page.locator(".trend-callout")
        assert callout.is_visible(), "La píldora de tendencia debe ser visible"
        print("Píldora de tendencia visible:", callout.inner_text().replace("\n", " "))

        # Captura del hero con la píldora
        page.screenshot(path="C:/Users/DRA/.gemini/antigravity/brain/57493430-4498-4ef1-aae2-14f86664084c/HERO_CON_TENDENCIA_EMPLEO.png")

        # 2. Pulsar la píldora y comprobar que filtra a empleo
        callout.click()
        page.wait_for_timeout(400)
        cards = page.locator("#cardsGrid article.card").count()
        print("Tarjetas filtradas tras pulsar la píldora:", cards)
        assert cards == 4, "Deben ser 4 ofertas de empleo"

        page.screenshot(path="C:/Users/DRA/.gemini/antigravity/brain/57493430-4498-4ef1-aae2-14f86664084c/FILTRADO_EMPLEO_DESDE_PILDORA.png")

        # 3. Probar en modo móvil
        page_mob = browser.new_page(viewport={"width": 390, "height": 844})
        page_mob.goto(file_path)
        page_mob.wait_for_timeout(500)
        assert page_mob.locator(".trend-callout").is_visible()
        page_mob.screenshot(path="C:/Users/DRA/.gemini/antigravity/brain/57493430-4498-4ef1-aae2-14f86664084c/HERO_EMPLEO_MOBILE.png")
        print("Captura móvil tomada con éxito.")

        browser.close()
    print("VERIFICACION TENDENCIA EMPLEO 100% EXITOSA")

if __name__ == "__main__":
    test()
