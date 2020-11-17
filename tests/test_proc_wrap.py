import asyncio
from multiprocessing import Process, Pipe
from datetime import datetime


class TestProc()

    def label_timestamp(self) -> str:
        # label snapshots with appropriate identifier +
        return 'Test_Proc' + '-' + str(datetime.now())

    def browser_main(self, browser_out, url: str):
        async def _browser(self, url: str):
            browser = print(url)
            # page = await browser.newPage()
            # await page.goto(url)
            # Wait till model to load here
            return browser

        async def _screenshot(null):
            '''Warning: This is not a real time feature, only use to establish sequential order per session id'''
            stamp = self.label_timestamp()
            await asyncio.sleep(1)
            print('Screenshot')

        async def _click(null):
            #mouse = self.page.mouse
            # await mouse.down()
            await asyncio.sleep(1)
            # await mouse.up()
            print('Click')

        async def _drag(self, coordinates):
            #mouse = self.page.mouse
            # await mouse.move
            # await mouse.down()
            # await mouse.move(x, y)
            # await mouse.up()
            await asyncio.sleep(1)
            (x, y) = coordinates
            print('Drag ({x}, {y})')

        loop = asyncio.get_event_loop()
        async def event_loop():
            self.page = await self._browser(url)

            while True:
                if browser_out.poll(timeout=None):
                    command = browser_out.recv()
                    await command[0](command[1])
        
        loop.run_forever(event_loop())
    


    def __init__(self):
        self.browser_out, self.browser_command = Pipe(duplex: False)
        self.browser = Process(target=self.browser_main, args=(
            self.browser_out, 'http://localhost:3000'),)
        self.browser.start()

    def screenshot(self):
        self.browser_command.send((_screenshot, 0))

    def click(self):
        self.browser_command.send((_click, 0))

    def drag(self, x: int, y: int):
        self.browser_command.send((_drag, (x, y)))
