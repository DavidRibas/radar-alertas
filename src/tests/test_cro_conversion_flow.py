import os
import sys
from playwright.sync_api import sync_playwright

def test_cro_flow():
    docs_path = os.path.abspath("docs/index.html")
    file_url = f"file:///{docs_path.replace(os.sep, '/')}"
    artifacts_dir = os.environ.get("GEMINI_BRAIN_DIR", r"C:\Users\DRA\.gemini\antigravity\brain\57493430-4498-4ef1-aae2-14f86664084c")
    os.makedirs(artifacts_dir, exist_ok=True)
    
    print(f"Testing CRO Flow on {file_url}...")
    
    with sync_playwright() as p:
        # 1. Desktop Test
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()
        page.goto(file_url, wait_until="networkidle")
        
        # Verify Sample Unlocked element
        sample_btn = page.locator("a.btn-unlock-single[download]").first
        sample_btn.scroll_into_view_if_needed()
        page.wait_for_timeout(1000)
        
        # Take screenshot of the sample card
        sample_card = page.locator(".card").filter(has=page.locator("a.btn-unlock-single[download]")).first
        sample_shot = os.path.join(artifacts_dir, "CRO_MUESTRA_GRATIS_DESBLOQUEADA.png")
        sample_card.screenshot(path=sample_shot)
        print(f"Saved sample card screenshot: {sample_shot}")
        
        # Verify sample download button
        assert sample_btn.is_visible(), "Botón de muestra gratis no visible"
        href = sample_btn.get_attribute("href")
        print(f"Sample download link: {href}")
        assert "Dictamen_Verificado_Final.pdf" in href, "El enlace de muestra no apunta al dictamen PDF"
        
        # Verify another card that is locked
        locked_btn = page.locator("button.btn-unlock-single").first
        locked_btn.scroll_into_view_if_needed()
        page.wait_for_timeout(500)
        locked_btn.click()
        
        page.wait_for_timeout(800)
        modal = page.locator("#modalUnlock")
        assert modal.is_visible(), "Modal de desbloqueo no se abrió"
        
        modal_shot = os.path.join(artifacts_dir, "CRO_NUEVO_MODAL_CONVERSION_290.png")
        modal.locator(".modal-box").screenshot(path=modal_shot)
        print(f"Saved modal conversion screenshot: {modal_shot}")
        
        # Close modal
        page.locator("#modalUnlock button.modal-close").click()
        page.wait_for_timeout(500)
        assert not modal.is_visible(), "Modal no se cerró"
        
        browser.close()
        
        # 2. Mobile Viewport Test (iPhone 14)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True)
        page = context.new_page()
        page.goto(file_url, wait_until="networkidle")
        
        # Click on locked card to test modal on mobile
        locked_btn_mobile = page.locator("button.btn-unlock-single").first
        locked_btn_mobile.scroll_into_view_if_needed()
        page.wait_for_timeout(500)
        locked_btn_mobile.click()
        
        page.wait_for_timeout(800)
        mobile_modal_shot = os.path.join(artifacts_dir, "CRO_MODAL_MOBILE_290.png")
        page.screenshot(path=mobile_modal_shot)
        print(f"Saved mobile modal screenshot: {mobile_modal_shot}")
        
        browser.close()
        print("ALL CRO TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_cro_flow()
