import gym
from gym import error, spaces, utils
from gym.utils import seeding

#import zmq
import socketio

from pyppeteer import launch
import asyncio, uvicorn
import socketio, pyppeteer
import time, os, subprocess, signal
import multiprocessing
from multiprocessing import Process, Pipe

import logging
logger = logging.getLogger(__name__)

class MetaStateChange:
  def __init__(self):
    self.type
    self.data
    self.label


# Entrypoint into metacad occurs here

class MetaCADEnv(gym.Env):
  metadata = {
    'render.modes': ['human', "rgb_array", "state_pixels"],
    'video.frames_per_second': FPS,
    }

  def events(app, sender):
    # Make this "internal" only?
    @sio.event
    async def connect(sid, environ):
        print('connect ', sid)

    @sio.event
    async def message(sid, data):
        sender.send(data)
        print('message ', data)

    @sio.event
    async def disconnect(sid):
        print('disconnect ', sid)

    uvicorn.run(app, host='0.0.0.0', port=3001)

  
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

  def __init__(self):
    # Start the node server
    self.node = subprocess.Popen(['node', 'run', 'dev'], cwd='/app/metacad')
    # Start listening for Socketio connection 
    sio = socketio.AsyncServer(async_mode = 'asgi', cors_allowed_origins='http://localhost:3000')
    # Generic Python ASGI
    app = socketio.ASGIApp(sio)
    receiver, sender = Pipe(duplex=False)
    self.receiver = receiver
    self.socketio = Process(target=events, args=(app, sender,))
    self.socketio.start()
    # Start pyppeteer
    self.browser = browser('http://localhost:3000')

    # Fail if not good 
    # ???

  def step(self, action):
    ...
  def reset(self):
    ...
  def render(self, mode='human'):
    ...
  def close(self):
    self.browser.close()
    self.socketio.terminate()
    # Wait for Process to terminate
    self.socketio.join()
