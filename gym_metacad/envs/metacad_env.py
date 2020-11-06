import gym
from gym import error, spaces, utils
from gym.utils import seeding

import zmq
import socketio

from pyppeteer import launch
import asyncio
import time




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

    # Start pyppeteer
    
    # Start listening for Socketio connection 
    
    # Fail if not good 
    # ???

  def step(self, action):
    ...
  def reset(self):
    ...
  def render(self, mode='human'):
    ...
  def close(self):
    ...