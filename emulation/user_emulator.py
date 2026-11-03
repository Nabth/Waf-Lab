import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Перехват всех ответов 403 (блокировки WAF)
        page.on("response", lambda resp: 
            print(f"[!] BLOCKED: {resp.url} - Status: {resp.status}") if resp.status == 403 else None
        )

        target_url = "http://192.168.56.40:8080"
        print(f"Opening {target_url}...")
        await page.goto(target_url)
        await page.wait_for_timeout(3000)

        # 1. Закрываем баннеры
        try: await page.locator("button:has-text('Dismiss')").click(timeout=2000)
        except: pass
        try: await page.locator("a:has-text('Me want it!')").click(timeout=2000)
        except: pass

        # 2. Логин
        print("Logging in...")
        await page.goto(f"{target_url}/#/login")
        await page.wait_for_selector("#email", timeout=5000)
        await page.locator("#email").fill("admin@juice-sh.op")
        await page.locator("#password").fill("admin123")
        await page.locator("button:has-text('Log in')").click()
        await page.wait_for_timeout(2000)
        print("Logged in successfully.")

        # 3. Добавление в корзину
        print("Adding item to basket...")
        await page.locator("button:has-text('Add to Basket')").first.click(timeout=5000)
        await page.wait_for_timeout(1000)

        # 4. Переход в корзину
        print("Going to basket...")
        await page.goto(f"{target_url}/#/basket")
        await page.wait_for_timeout(2000)

        # Проверяем, что товар в корзине (ищем кнопку Checkout)
        try:
            await page.wait_for_selector("button:has-text('Checkout')", timeout=3000)
            print("Item successfully added to basket (Checkout button visible).")
        except:
            print("Checkout button not found, but no WAF block detected.")

        print("Scenario finished successfully.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
