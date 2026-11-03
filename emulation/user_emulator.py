import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("Opening Juice Shop and performing search...")
        
        # Переходим сразу на страницу поиска с нужным параметром. 
        # Angular сам сформирует GET-запрос к /rest/products/search?q=orange%27
        await page.goto("http://192.168.56.40:8080/#/search?q=orange'")
        
        # Ждем, пока отработают все фоновые запросы
        await page.wait_for_timeout(3000)
        
        # Делаем скриншот (на этот раз на нем должно быть пусто или ошибка, если WAF сработает)
        await page.screenshot(path="debug_search.png")
        
        print("Done! Check logs.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
