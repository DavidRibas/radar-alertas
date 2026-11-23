import os
import sys
from playwright.sync_api import sync_playwright

def test_clean_cards():
    docs_path = os.path.abspath("docs/index.html")
    file_url = f"file:///{docs_path.replace(os.sep, '/')}"
    artifacts_dir = os.environ.get("GEMINI_BRAIN_DIR", r"C:\Users\DRA\.gemini\antigravity\brain\57493430-4498-4ef1-aae2-14f86664084c")
    os.makedirs(artifacts_dir, exist_ok=True)
    
    print(f"Testing clean cards layout on {file_url}...")
    
    with sync_playwright() as p:
        # 1. Desktop Test
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 950})
        page.goto(file_url, wait_until="networkidle")
        page.wait_for_timeout(1000)

        # 1.1 Capture default mixed view showing clean paid card vs clean free card
        first_paid_card = page.locator(".card:not(.card-free-deal)").first
        first_paid_card.scroll_into_view_if_needed()
        page.wait_for_timeout(500)
        shot_paid = os.path.join(artifacts_dir, "NUEVA_TARJETA_SUBASTA_LIMPIA.png")
        first_paid_card.screenshot(path=shot_paid)
        print(f"Saved paid card screenshot: {shot_paid}")

        first_free_card = page.locator(".card-free-deal").first
        first_free_card.scroll_into_view_if_needed()
        page.wait_for_timeout(500)
        shot_free = os.path.join(artifacts_dir, "NUEVA_TARJETA_GRATIS_LIMPIA.png")
        first_free_card.screenshot(path=shot_free)
        print(f"Saved free card screenshot: {shot_free}")

        # 1.2 Click on the new "🟢 100% Gratis / Muestras" express chip!
        btn_chip_gratis = page.locator("#chipGratis")
        assert btn_chip_gratis.is_visible(), "Chip de 100% Gratis no visible"
        btn_chip_gratis.scroll_into_view_if_needed()
        btn_chip_gratis.click()
        page.wait_for_timeout(800)

        # Count cards: should only show free cards (9 items)
        cards_count = page.locator(".card").count()
        print(f"Filtered cards count for 100% Gratis: {cards_count}")
        assert cards_count == 9, f"Se esperaban 9 tarjetas gratis, se encontraron {cards_count}"

        shot_grid_gratis = os.path.join(artifacts_dir, "FILTRO_100_PORCIENTO_GRATIS_DESKTOP.png")
        page.screenshot(path=shot_grid_gratis)
        print(f"Saved filtered grid screenshot: {shot_grid_gratis}")

        # Test modal still opens when clicking a paid card (unfilter first)
        page.locator("#btnLimpiarChips").click()
        page.wait_for_timeout(500)
        
        btn_unlock = page.locator(".btn-paid-cta").first
        btn_unlock.scroll_into_view_if_needed()
        btn_unlock.click()
        page.wait_for_timeout(500)
        assert page.locator("#modalUnlock").is_visible(), "Modal no se abrió"
        page.locator("#modalUnlock .modal-close").click()
        page.wait_for_timeout(300)

        browser.close()

        # 2. Mobile Viewport (iPhone 14)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 390, "height": 844}, is_mobile=True)
        page.goto(file_url, wait_until="networkidle")
        page.wait_for_timeout(1000)

        # Capture mobile card view
        card_mobile = page.locator(".card").first
        card_mobile.scroll_into_view_if_needed()
        page.wait_for_timeout(500)
        shot_mobile = os.path.join(artifacts_dir, "NUEVO_DISENO_TARJETAS_MOBILE.png")
        page.screenshot(path=shot_mobile)
        print(f"Saved mobile screenshot: {shot_mobile}")

        browser.close()
        print("ALL CLEAN CARDS TESTS COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    test_clean_cards()
