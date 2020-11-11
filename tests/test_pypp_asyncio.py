import asyncio
import pyppeteer
from pyppeteer import launch
import time

async def drag(page, x: int, y: int):
    mouse = page.mouse
    await mouse.move
    await mouse.down()
    await mouse.move(x, y)
    await mouse.up()


async def browser(url: str):
    browser = await launch( args=['--no-sandbox', '--window-size=1920,1080', '--start-maximized'], defaultViewport=None)
    page = await browser.newPage()
    await page.goto(url)
    # Wait till model to load here 
    return page


browser = asyncio.run(browser('http://localhost:3000'))
print(browser)