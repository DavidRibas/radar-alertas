import os
from playwright.sync_api import sync_playwright

docs_path = os.path.abspath("docs/index.html")
file_url = f"file:///{docs_path.replace(os.sep, '/')}"
artifacts_dir = os.environ.get("GEMINI_BRAIN_DIR", r"C:\Users\DRA\.gemini\antigravity\brain\57493430-4498-4ef1-aae2-14f86664084c")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 950})
    page.goto(file_url, wait_until="networkidle")
    page.wait_for_timeout(1000)
    
    # Click on a paid card unlock button
    btn = page.locator(".btn-paid-cta").first
    btn.scroll_into_view_if_needed()
    btn.click()
    page.wait_for_timeout(800)
    
    modal = page.locator("#modalUnlock .modal-box")
    shot_path = os.path.join(artifacts_dir, "MODAL_KIT_SEGURIDAD_3_EN_1.png")
    modal.screenshot(path=shot_path)
    print(f"Saved modal screenshot: {shot_path}")
    
    browser.close()
    print("MODAL TEST COMPLETED!")
