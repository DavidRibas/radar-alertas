import os
from playwright.sync_api import sync_playwright

docs_path = os.path.abspath("docs/descarga-kit.html")
file_url = f"file:///{docs_path.replace(os.sep, '/')}"
artifacts_dir = os.environ.get("GEMINI_BRAIN_DIR", r"C:\Users\DRA\.gemini\antigravity\brain\57493430-4498-4ef1-aae2-14f86664084c")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    page.goto(file_url, wait_until="networkidle")
    
    # Check elements
    btn_dl = page.locator("#btnDescargarKit")
    assert btn_dl.is_visible(), "Botón de descarga no visible"
    
    shot_path = os.path.join(artifacts_dir, "PAGINA_EXITO_POST_PAGO_290.png")
    page.locator(".success-card").screenshot(path=shot_path)
    print(f"Saved success page screenshot: {shot_path}")
    
    # Mobile view
    page.set_viewport_size({"width": 390, "height": 844})
    page.wait_for_timeout(300)
    shot_mobile = os.path.join(artifacts_dir, "PAGINA_EXITO_MOBILE_290.png")
    page.screenshot(path=shot_mobile)
    print(f"Saved mobile success screenshot: {shot_mobile}")
    
    browser.close()
    print("SUCCESS PAGE TEST COMPLETED!")
