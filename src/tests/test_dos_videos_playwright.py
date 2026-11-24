import os
from playwright.sync_api import sync_playwright

docs_path = os.path.abspath("docs/index.html")
file_url = f"file:///{docs_path.replace(os.sep, '/')}"
artifacts_dir = os.environ.get("GEMINI_BRAIN_DIR", r"C:\Users\DRA\.gemini\antigravity\brain\57493430-4498-4ef1-aae2-14f86664084c")

print("Testing 2 Videos Selector in Modal with Playwright...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 950})
    page.goto(file_url, wait_until="networkidle")
    page.wait_for_timeout(1000)

    # Open Academia modal
    page.locator("a:has-text('Mini-Curso & Guías')").first.click()
    page.wait_for_timeout(600)
    
    # Switch to Video tab
    page.evaluate("cambiarTabCurso('video')")
    page.wait_for_timeout(500)
    
    # Check selector buttons exist
    btn_dum = page.locator("#btnSelVideoDummies")
    btn_web = page.locator("#btnSelVideoWeb")
    assert btn_dum.is_visible(), "Botón vídeo dummies no visible"
    assert btn_web.is_visible(), "Botón vídeo web no visible"
    
    shot_video = os.path.join(artifacts_dir, "MODAL_VIDEO_DUMMIES_SELECTOR.png")
    page.locator("#modalTutorial .modal-box").screenshot(path=shot_video)
    print(f"Saved Video Selector Screenshot: {shot_video}")

    # Switch to web video
    page.evaluate("cambiarVideoTutorial('web')")
    page.wait_for_timeout(400)
    src = page.locator("#videoTutorialPlayer").get_attribute("src")
    print("Video src switched to:", src)
    assert "tutorial_radaralertas.mp4" in src
    
    # Switch back to dummies video
    page.evaluate("cambiarVideoTutorial('dummies')")
    page.wait_for_timeout(400)
    src_dum = page.locator("#videoTutorialPlayer").get_attribute("src")
    print("Video src switched to dummies:", src_dum)
    assert "tutorial_dummies_paso_a_paso.mp4" in src_dum

    browser.close()
    print("ALL TESTS PASSED: 2 VIDEOS SELECTOR OPERATIONAL!")
