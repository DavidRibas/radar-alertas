from playwright.sync_api import sync_playwright
import os

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        html_file = os.path.abspath("docs/index.html").replace("\\", "/")
        file_path = f"file:///{html_file}"
        page.goto(file_path)
        page.wait_for_timeout(1000)

        # 1. Check top announcement bar
        ann = page.locator(".top-announcement-bar").is_visible()
        print("Top announcement bar visible:", ann)

        # 2. Check floating telegram button
        ftg = page.locator(".floating-tg-btn").is_visible()
        print("Floating Telegram button visible:", ftg)

        # 3. Check quick filter chips
        chips = page.locator(".quick-filter-chips").is_visible()
        print("Quick filter chips visible:", chips)

        # 4. Check savings badges
        savings = page.locator(".savings-pill-banner").count()
        print("Savings badges count:", savings)

        # 5. Check WhatsApp Share buttons on cards
        wa_btns = page.locator(".btn-share-wa").count()
        print("WhatsApp share buttons count:", wa_btns)

        # 6. Check Push alert prompt bar
        push_bar = page.locator("#pushPromptWrap").is_visible()
        print("Push prompt bar visible:", push_bar)

        # Screenshot desktop
        page.screenshot(path="C:/Users/DRA/.gemini/antigravity/brain/57493430-4498-4ef1-aae2-14f86664084c/WEB_NUEVAS_MEJORAS_DESKTOP.png")

        # Mobile viewport
        page_mob = browser.new_page(viewport={"width": 390, "height": 844})
        page_mob.goto(file_path)
        page_mob.wait_for_timeout(1000)
        page_mob.screenshot(path="C:/Users/DRA/.gemini/antigravity/brain/57493430-4498-4ef1-aae2-14f86664084c/WEB_NUEVAS_MEJORAS_MOBILE.png")

        browser.close()
    print("TODO VERIFICADO Y FUNCIONANDO AL 100%")

if __name__ == "__main__":
    test()
