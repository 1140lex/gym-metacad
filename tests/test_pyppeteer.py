
from pyppeteer import launch
import asyncio
import time

async def drag(page, x: int, y: int):
        mouse = page.mouse
        await mouse.move
        await mouse.down()
        await mouse.move(x, y)
        await mouse.up()

async def main():
	browser = await launch( args=['--no-sandbox', '--window-size=1920,1080', '--start-maximized'], defaultViewport=None)
	page = await browser.newPage()
	await page.goto('http://localhost:3000')
    # Wait till model to load here 
    time.sleep(3)
	await page.screenshot({'path': 'example.png'})
	await browser.close()

asyncio.get_event_loop().run_until_complete(main())
