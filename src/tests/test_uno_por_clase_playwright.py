import os
import sys
from playwright.sync_api import sync_playwright

def test_uno_por_clase():
    docs_path = os.path.abspath("docs/index.html")
    file_url = f"file:///{docs_path.replace(os.sep, '/')}"
    artifacts_dir = os.environ.get("GEMINI_BRAIN_DIR", r"C:\Users\DRA\.gemini\antigravity\brain\57493430-4498-4ef1-aae2-14f86664084c")
    os.makedirs(artifacts_dir, exist_ok=True)
    
    print(f"Testing 1 gratis por clase on {file_url}...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 950})
        page.goto(file_url, wait_until="networkidle")
        page.wait_for_timeout(1000)

        # 1. Test Express Chip: 100% Gratis
        page.locator("#chipGratis").click()
        page.wait_for_timeout(800)
        
        cards_gratis = page.locator(".card").count()
        print(f"Total tarjetas gratis en filtro: {cards_gratis}")
        assert cards_gratis == 5, f"Se esperaban exactamente 5 muestras gratis (1 por clase), hay {cards_gratis}"
        
        shot_5_gratis = os.path.join(artifacts_dir, "CATALOGO_5_MUESTRAS_GRATIS_EQUILIBRADAS.png")
        page.screenshot(path=shot_5_gratis)
        print(f"Saved 5 muestras screenshot: {shot_5_gratis}")

        # 2. Test Category Empleo: 1 gratis + 3 de pago
        page.locator("#btnLimpiarChips").click()
        page.wait_for_timeout(500)
        
        page.locator("#tabEmpleo").click()
        page.wait_for_timeout(800)
        
        empleo_cards = page.locator(".card").count()
        empleo_free = page.locator(".card-free-deal").count()
        empleo_paid = page.locator(".card:not(.card-free-deal)").count()
        print(f"Empleo -> Total: {empleo_cards}, Gratis: {empleo_free}, De Pago: {empleo_paid}")
        assert empleo_free == 1 and empleo_paid == 3, "Empleo no tiene 1 gratis y 3 de pago"

        shot_empleo = os.path.join(artifacts_dir, "CATEGORIA_EMPLEO_1_GRATIS_3_PAGO.png")
        page.screenshot(path=shot_empleo)
        print(f"Saved empleo screenshot: {shot_empleo}")

        # 3. Test Category Vehículos: 1 gratis + 7 de pago
        page.locator("button.tab-btn:has-text('Coches & Decomisos')").click()
        page.wait_for_timeout(800)
        
        veh_cards = page.locator(".card").count()
        veh_free = page.locator(".card-free-deal").count()
        veh_paid = page.locator(".card:not(.card-free-deal)").count()
        print(f"Vehículos -> Total: {veh_cards}, Gratis: {veh_free}, De Pago: {veh_paid}")
        assert veh_free == 1 and veh_paid == 7, "Vehículos no tiene 1 gratis y 7 de pago"

        shot_veh = os.path.join(artifacts_dir, "CATEGORIA_VEHICULOS_1_GRATIS_7_PAGO.png")
        page.screenshot(path=shot_veh)
        print(f"Saved vehículos screenshot: {shot_veh}")

        browser.close()
        print("ALL TESTS PASSED: EXACTAMENTE 1 MUESTRA GRATIS POR CLASE!")

if __name__ == "__main__":
    test_uno_por_clase()
