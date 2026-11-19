import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

BASE_DIR = Path("C:/Ideas/radar-alertas")
OUTPUT_DIR = BASE_DIR / "output"
HTML_PATH = BASE_DIR / "docs" / "index.html"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # 1. Desktop
        page_desk = await browser.new_page(viewport={"width": 1440, "height": 900})
        await page_desk.goto(HTML_PATH.as_uri())
        await page_desk.screenshot(path=str(OUTPUT_DIR / "WEB_DESKTOP_PREVIEW.png"), full_page=True)
        print("✓ Desktop OK")

        # 2. Mobile iPhone
        page_mob = await browser.new_page(viewport={"width": 390, "height": 844})
        await page_mob.goto(HTML_PATH.as_uri())
        await page_mob.screenshot(path=str(OUTPUT_DIR / "WEB_MOBILE_PREVIEW.png"), full_page=False)
        print("✓ Mobile OK")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
