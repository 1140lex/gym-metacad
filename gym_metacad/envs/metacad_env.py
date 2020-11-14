import gym
import asyncio, uvicorn
import socketio, pyppeteer
import time, os, subprocess, signal
import multiprocessing
from multiprocessing import Process, Pipe
from functools import partial
from gym.utils import seeding
from pyppeteer import launch
from datetime import datetime
from gym import error, spaces, utils

import logging
logger = logging.getLogger(__name__)

class MetaCADEnv(gym.Env):
  metadata = {
    'render.modes': ['human']
    }

  def label_timestamp(self) -> str:
    # label snapshots with appropriate identifier + 
    now = datetime.now()
    return self.sid + '-' + datetime.fromtimestamp(datetime.timestamp(now))

  def events(self, app, sender):
    # Make this "internal" only?
    @self.sio.event
    async def connect(sid, environ):
        sender.send(sid)
        print('connect ', sid)

    @sio.event
    async def message(sid, data):
        sender.send(data)
        print('message ', data)

    @sio.event
    async def disconnect(sid):
        print('disconnect ', sid)

    uvicorn.run(app, host='0.0.0.0', port=3001)

  async def click(self, page):
    mouse = page.mouse
    await mouse.down()
    await mouse.up()
  
  async def drag(self, page, x: int, y: int):
    mouse = page.mouse
    await mouse.move
    await mouse.down()
    await mouse.move(x, y)
    await mouse.up()

  async def _browser(self, url: str):
    browser = await launch( args=['--no-sandbox', '--window-size=1920,1080', '--start-maximized'], defaultViewport=None)
    page = await browser.newPage()
    await page.goto(url)
    # Wait till model to load here 
    return page
  
  async def screenshot(self, page):
    '''Warning: This is not a real time feature, only use to establish sequential order per session id'''
    stamp = label_timestamp()
    await page.screenshot({self.path: stamp + '.png'})
    return stamp

  # TODO gym.Env format demands passing args 
  def __init__(self, path = 'path'):
    # Start the node server
    self.node = subprocess.Popen(['node', 'run', 'dev'], cwd='/app/metacad')
    # Start listening for Socketio connection 
    # Going to need to handle multiple ports here somehow.  
    sio = socketio.AsyncServer(async_mode = 'asgi', cors_allowed_origins='http://localhost:3000')
    # Generic Python ASGI
    app = socketio.ASGIApp(sio)
    receiver, sender = Pipe(duplex=False)
    self.receiver = receiver
    self.socketio = Process(target=self.events, args=(app, sender,))
    self.socketio.start()
    # Start pyppeteer
    self.browser = asyncio.run(self._browser('http://localhost:3000'))
    self.sid = receiver.recv()
    # Set the path for screenshots
    self.path = path
    # Wait for web environment to load
    time.sleep(2)
    self.start = asyncio.run(self.screenshot(self.page))
    self.state
    # For plugin assesment at a later time
    self.rewarder = None
  
  def step(self, action, timeout = 1):
    '''Sample call step(partial(action, args1, args2))'''
    # Take some action
    if asyncio.iscoroutinefunction(action):
      asyncio.run(action())
    else:
      action()
    observation = asyncio.run(screenshot(self.page))
    reward = 0.0 #Todo downstream
    done = False #Todo downstream

    dictionary = {}
    i = 0
    # Metacad branch at time of writing throughput natively convertible
    while(self.receiver.poll(timeout = timeout)):
      dictionary[i] = self.receiver.recv()
      i += 1 #TODO sys.maxint opportunity here

    info = dictionary
    return (observation, reward, done, info)
  
  def reset(self):
    pass

  def render(self, mode='human'):
    pass

  def close(self):
    # Stop Pyppeteer 
    self.browser.close()
    self.socketio.terminate()
    # Wait for Process to terminate
    self.socketio.join()
    # Stop nodejs
    self.node
