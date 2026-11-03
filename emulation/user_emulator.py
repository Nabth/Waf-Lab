import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        target_url = "http://192.168.56.40:8080"
        
        print(f"Opening {target_url}...")
        await page.goto(target_url)
        
        # Ждем загрузки интерфейса
        await page.wait_for_timeout(3000)
        
        # 1. Закрываем баннер приветствия (если есть)
        try:
            dismiss_btn = page.locator("button:has-text('Dismiss')")
            if await dismiss_btn.is_visible():
                print("Closing welcome banner...")
                await dismiss_btn.click()
                await page.wait_for_timeout(500)
        except Exception:
            pass

        # 2. Закрываем всплывающее окно с куки (если есть)
        try:
            cookie_btn = page.locator("a:has-text('Me want it!')")
            if await cookie_btn.is_visible():
                print("Closing cookie banner...")
                await cookie_btn.click()
                await page.wait_for_timeout(500)
        except Exception:
            pass
        
        # 3. Кликаем по иконке поиска
        print("Clicking search icon...")
        # Используем force=True на случай, если остались невидимые оверлеи
        await page.locator("mat-icon:has-text('search')").first.click(force=True)
        await page.wait_for_timeout(1000)
        
        # 4. Вводим текст
        print("Typing search query...")
        await page.locator("input[type='text']").first.fill("apple")
        await page.keyboard.press("Enter")
        
        await page.wait_for_timeout(2000)
        print("Done!")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
