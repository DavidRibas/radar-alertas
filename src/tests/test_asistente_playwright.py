import os
from playwright.sync_api import sync_playwright

docs_path = os.path.abspath("docs/index.html")
file_url = f"file:///{docs_path.replace(os.sep, '/')}"
artifacts_dir = os.environ.get("GEMINI_BRAIN_DIR", r"C:\Users\DRA\.gemini\antigravity\brain\57493430-4498-4ef1-aae2-14f86664084c")

print("Testing Asistente IA and Academia with Playwright...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 950})
    page.goto(file_url, wait_until="networkidle")
    page.wait_for_timeout(1000)

    # 1. Test Academia Modal
    btn_academia = page.locator("a:has-text('Mini-Curso & Guías')").first
    btn_academia.click()
    page.wait_for_timeout(500)
    
    modal_tut = page.locator("#modalTutorial")
    assert modal_tut.is_visible(), "Modal Academia no se abrió"
    
    # Switch to Subastas tab
    page.locator("#tabCursoSubastas").click()
    page.wait_for_timeout(400)
    shot_academia = os.path.join(artifacts_dir, "ACADEMIA_MINICURSO_MODAL.png")
    modal_tut.locator(".modal-box").screenshot(path=shot_academia)
    print(f"Saved Academia Screenshot: {shot_academia}")
    
    # Close Academia modal
    page.locator("#modalTutorial .modal-close").click()
    page.wait_for_timeout(500)

    # 2. Test Floating AI Assistant Chat
    btn_ai = page.locator("#btnOpenAiChat")
    assert btn_ai.is_visible(), "Botón Asistente IA no visible"
    btn_ai.click()
    page.wait_for_timeout(500)
    
    chat_win = page.locator("#aiChatWindow")
    assert chat_win.is_visible(), "Ventana de chat IA no se abrió"
    
    # Click on FAQ: fianza
    page.locator(".ai-chip:has-text('fianza')").first.click()
    page.wait_for_timeout(800)
    
    shot_chat = os.path.join(artifacts_dir, "ASISTENTE_IA_CHAT_ABIERTO.png")
    chat_win.screenshot(path=shot_chat)
    print(f"Saved Chat Screenshot: {shot_chat}")
    
    browser.close()

    # 3. Mobile View (iPhone 14)
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 390, "height": 844})
    page.goto(file_url, wait_until="networkidle")
    page.wait_for_timeout(800)
    
    page.locator("#btnOpenAiChat").click()
    page.wait_for_timeout(500)
    
    shot_mobile = os.path.join(artifacts_dir, "ASISTENTE_IA_CHAT_MOBILE.png")
    page.screenshot(path=shot_mobile)
    print(f"Saved Mobile Chat Screenshot: {shot_mobile}")
    
    browser.close()
    print("ALL TESTS PASSED: ASISTENTE IA & ACADEMIA OPERATIONAL!")
