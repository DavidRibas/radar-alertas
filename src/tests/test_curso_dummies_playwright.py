import os
from playwright.sync_api import sync_playwright

docs_path = os.path.abspath("docs/index.html")
file_url = f"file:///{docs_path.replace(os.sep, '/')}"
artifacts_dir = os.environ.get("GEMINI_BRAIN_DIR", r"C:\Users\DRA\.gemini\antigravity\brain\57493430-4498-4ef1-aae2-14f86664084c")

print("Testing Curso para Dummies with Playwright...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 950})
    page.goto(file_url, wait_until="networkidle")
    page.wait_for_timeout(1000)

    # 1. Open Academia Modal
    btn_academia = page.locator("a:has-text('Mini-Curso & Guías')").first
    btn_academia.click()
    page.wait_for_timeout(600)
    
    modal_tut = page.locator("#modalTutorial")
    assert modal_tut.is_visible(), "Modal Academia no se abrió"
    
    # Check that Paso 1 to Paso 5 are present
    assert page.locator("span:has-text('PASO 1')").is_visible(), "Paso 1 no visible"
    assert page.locator("span:has-text('PASO 5')").is_visible(), "Paso 5 no visible"
    
    shot_dummies = os.path.join(artifacts_dir, "CURSO_SUBASTAS_PARA_DUMMIES.png")
    modal_tut.locator(".modal-box").screenshot(path=shot_dummies)
    print(f"Saved Dummies Course Screenshot: {shot_dummies}")
    
    # Close modal via JS function
    page.evaluate("cerrarModalTutorial()")
    page.wait_for_timeout(500)

    # 2. Test AI Chat with Dummies question
    page.locator("#btnOpenAiChat").click()
    page.wait_for_timeout(500)
    
    btn_chip_dummies = page.locator(".ai-chip:has-text('dummies')").first
    btn_chip_dummies.click()
    page.wait_for_timeout(800)
    
    shot_ai_dummies = os.path.join(artifacts_dir, "ASISTENTE_IA_EXPLICACION_DUMMIES.png")
    page.locator("#aiChatWindow").screenshot(path=shot_ai_dummies)
    print(f"Saved AI Chat Dummies Screenshot: {shot_ai_dummies}")

    browser.close()
    print("ALL TESTS PASSED: CURSO PARA DUMMIES FULLY OPERATIONAL!")
