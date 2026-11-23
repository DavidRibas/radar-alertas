import os
from playwright.sync_api import sync_playwright

docs_path = os.path.abspath("docs/index.html")
file_url = f"file:///{docs_path.replace(os.sep, '/')}"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(file_url, wait_until="networkidle")
    script = page.locator('script[src="/_vercel/insights/script.js"]')
    print("Vercel script tag exists in DOM:", script.count() > 0)
    assert script.count() > 0, "No se encontró la etiqueta de Vercel Analytics"
    browser.close()
    print("PLAYWRIGHT VERIFICATION SUCCESSFUL!")
