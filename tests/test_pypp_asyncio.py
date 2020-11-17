import asyncio
import pyppeteer
from pyppeteer import launch
import time


def screenshot(self):
    self.browser_command(send)


def browser_main(self, browser_out, url: str,):
    async def _browser(self, url: str):
        browser = await launch(args=['--no-sandbox', '--window-size=1920,1080', '--start-maximized'], defaultViewport=None)
        page = await browser.newPage()
        await page.goto(url)
        # Wait till model to load here
        return page

    async def _screenshot():
        '''Warning: This is not a real time feature, only use to establish sequential order per session id'''
        stamp = self.label_timestamp()
        await self.page.screenshot({self.path: stamp + '.png'})

    async def _click():
        mouse = self.page.mouse
        await mouse.down()
        await mouse.up()

    async def _drag(self, x: int, y: int):
        mouse = self.page.mouse
        await mouse.move
        await mouse.down()
        await mouse.move(x, y)
        await mouse.up()

    loop = asyncio.get_event_loop()

    async def event_loop(loop):
        self.page = await self._browser(url)

        while True:
            if browser_out.poll(timeout=None):
                command = browser_out.recv()
                command[0](command[1])

        while browser
