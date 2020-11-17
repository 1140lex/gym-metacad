import asyncio
from multiprocessing import Process, Pipe
from datetime import datetime


class TestProc():

    def label_timestamp(self) -> str:
        # label snapshots with appropriate identifier +
        return 'Test_Proc' + '-' + str(datetime.now())

    def browser_main(self, browser_out, url: str):
        async def _browser(url: str):
            browser = print(url)
            await asyncio.sleep(0)
            # page = await browser.newPage()
            # await page.goto(url)
            # Wait till model to load here
            return browser

        async def _screenshot():
            '''Warning: This is not a real time feature, only use to establish sequential order per session id'''
            stamp = self.label_timestamp()
            await asyncio.sleep(0)
            print('Screenshot')

        async def _click():
            #mouse = self.page.mouse
            # await mouse.down()
            await asyncio.sleep(0)
            # await mouse.up()
            print('Click')

        async def _drag(coordinates):
            #mouse = self.page.mouse
            # await mouse.move
            # await mouse.down()
            # await mouse.move(x, y)
            # await mouse.up()
            await asyncio.sleep(0)
            (x, y) = coordinates
            print(f"Drag ({x}, {y})")

        #loop = asyncio.new_event_loop()

        async def event_loop(self, url):
            self.page = await _browser(url=url)

            while True:
                if browser_out.poll(timeout=None):
                    command = browser_out.recv()
                    if command[0] == 1:
                        await _screenshot()
                    elif command[0] == 2:
                        await _click()
                    elif command[0] == 3:
                        await _drag(command[1])

        asyncio.run(event_loop(self=self, url=url))

    def __init__(self):
        self.browser_out, self.browser_command = Pipe(duplex=False)
        self.browser = Process(target=self.browser_main, args=(
            self.browser_out, 'http://localhost:3000'),)
        self.browser.start()

    def screenshot(self):
        self.browser_command.send((1, 0))

    def click(self):
        self.browser_command.send((2, 0))

    def drag(self, x: int, y: int):
        self.browser_command.send((3, (x, y)))


# async def main():
#    x = TestProc()

if __name__ == '__main__':
    x = TestProc()
