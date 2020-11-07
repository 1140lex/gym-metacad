import gym
from gym import error, spaces, utils
from gym.utils import seeding

import zmq
import socketio

from pyppeteer import launch
import asyncio, uvicorn
import socketio, pyppeteer
import time, os, subprocess, signal
import multiprocessing
from multiprocessing import process

import logging
logger = logging.getLogger(__name__)

def browser():


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

  def __init__(self):
    # Start the node server
    self.node = subprocess.Popen(['node', 'run', 'dev'], cwd='/app/metacad')
    # Start pyppeteer
    self.pool = multiprocessing.pool()
    self.browser = launch( args=['--no-sandbox', '--window-size=1920,1080', '--start-maximized'], defaultViewport=None)

    # Start listening for Socketio connection 
    sio = socketio.AsyncServer(async_mode = 'asgi', cors_allowed_origins='http://localhost:3000')
    self.app = socketio.ASGIApp(sio)
    # Fail if not good 
    # ???

  def step(self, action):
    ...
  def reset(self):
    ...
  def render(self, mode='human'):
    ...
  def close(self):
    self.node.terminate()
    self.browser.close()
    ...