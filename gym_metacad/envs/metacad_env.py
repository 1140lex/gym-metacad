import gym
import sys
import asyncio
import uvicorn
import socketio
import pyppeteer
import time
import os
import subprocess
from signal import SIGTERM
from multiprocessing import Process, Pipe
from gym.utils import seeding
from gym import error, spaces, utils
from pyppeteer import launch
from datetime import datetime

import socket  # Included to test connectivity on node service in lieu of IPC
import logging
logger = logging.getLogger(__name__)


class MetaCADEnv(gym.Env):
    metadata = {
        'render.modes': ['human']
    }

    def label_timestamp(self) -> str:
        # label snapshots with appropriate identifier +
        return self.sid + '-' + str(datetime.now())

    def events(self, app, sender):
        # Make this "internal" only?
        @self.sio.event
        async def connect(sid, environ):
            sender.send(sid) # sid needs to go to all processes
            print('connect ', sid)

        @self.sio.event #TODO screenshot on submit event
        async def message(sid, data):
            sender.send(data)
            print('message ', data)

        @self.sio.event
        async def disconnect(sid):
            print('disconnect ', sid)

        uvicorn.run(app, host='0.0.0.0', port=3001)

    def browser_main(self, browser_out, url: str,):
        async def _screenshot():
            '''Warning: This is not a real time feature, only use to establish sequential order per session id'''
            stamp = self.label_timestamp()
            await self.page.screenshot({self.path: stamp + '.png'})
            browser_out.send(stamp)

        async def _browser(url: str):
            browser = await launch(args=['--no-sandbox', '--window-size=1920,1080', '--start-maximized'],
                                   defaultViewport=None, stdout=subprocess.DEVNULL)
            page = await browser.newPage()
            await page.goto(url)
            # Wait till model to load here
            return page, browser

        async def _click():
            mouse = self.page.mouse
            await mouse.down()
            await mouse.up()

        async def _drag(coordinates):
            (x, y) = coordinates
            mouse = self.page.mouse
            await mouse.move
            await mouse.down()
            await mouse.move(x, y)
            await mouse.up()

        async def event_loop(self, url):
            self.page, chrome = await _browser(url=url)
            self.sid = self.browser_out.recv()
            while True:
                if browser_out.poll(timeout=None):
                    command = browser_out.recv()
                    if command[0] == 1:
                        await _screenshot()
                    elif command[0] == 2:
                        await _click()
                    elif command[0] == 3:
                        await _drag(command[1])
                    elif command[0] == 4:
                        await self.page.close()
                        await chrome.close()

        asyncio.run(event_loop(self=self, url=url))

    def screenshot(self):
        self.browser_command.send((1, 0))
        return self.browser_command.recv()

    def click(self):
        self.step((2, 0))

    def drag(self, x: int, y: int):
        self.step((3, (x, y)))

    def _close(self):
        self.step((4, 0))

    # TODO gym.Env format demands passing args

    def __init__(self, path='/app/clips'):
        # Set the path for screenshots
        self.path = path
        # Start the node server
        self.node = subprocess.Popen(
            ['npm run dev'], stdout=subprocess.DEVNULL, cwd='/app/metacad', shell=True, preexec_fn=os.setsid)
        # Start listening for Socketio connection
        # Going to need to handle multiple ports here somehow.
        self.sio = socketio.AsyncServer(
            async_mode='asgi', cors_allowed_origins='http://localhost:3000')
        receiver, sender = Pipe(duplex=False)
        # Generic Python ASGI
        app = socketio.ASGIApp(self.sio)
        self.receiver = receiver
        self.socketio = Process(target=self.events, args=(app, sender,))
        self.socketio.start()
        # Start pyppeteer
        # Before we do this, make sure that the local host is listening (via lsof/psutil) on 3000
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        i = 1
        test_location = ('0.0.0.0', 3000)
        while bool(test_socket.connect_ex(test_location)):
            print("Waiting for socket at 3000 to open X" + str(i))
            try:
                i += 1
                time.sleep(1)
            except KeyboardInterrupt:
                self.node.terminate()
                sys.exit()

        test_socket.close()

        self.sid = None # = receiver.recv()
        self.browser_out, self.browser_command = Pipe()
        self.browser = Process(target=self.browser_main, args=(
            self.browser_out, 'http://localhost:3000'),)
        self.browser.start()
        self.sid = receiver.recv()
        self.browser_out.send(self.sid) # Pass sid to timestamper!

        # Wait for web environment to load
        time.sleep(2)
        self.start = self.screenshot()
        # For plugin assesment at a later time
        self.rewarder = None

    def step(self, action, timeout=1):

        # Take some action
        self.browser_command.send(action)
        # Locking could be an issue for below
        observation = self.screenshot()
        reward = 0.0  # Todo downstream
        done = False  # Todo downstream

        dictionary = {}
        i = 0
        # Metacad branch at time of writing throughput natively convertible
        while(self.receiver.poll(timeout=timeout)):
            dictionary[i] = self.receiver.recv()
            i += 1  # TODO sys.maxint opportunity here

        info = dictionary
        return (observation, reward, done, info)

    def reset(self):
        # Add better reset to make sure all processes are killed.
        ...

    def render(self, mode='human'):
        ...

    def close(self):
        # Stop Pyppeteer
        self._close()
        self.browser.close()
        self.browser.join()
        self.socketio.terminate()
        # Wait for Process to terminate
        self.socketio.join()
        # Stop nodejs
        os.killpg(os.getpgid(self.node.pid), SIGTERM)
        self.node.terminate()
