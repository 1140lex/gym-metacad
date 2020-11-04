import gym
import zmq
from gym import error, spaces, utils
from gym.utils import seeding


class MetaStateChange:
  def __init__(self):
    self.type
    self.data
    self.label


# Entrypoint into metacad occurs here



class MetaCADenv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self):
    # Start the node server
    # Start the zmq messenger
    # Wait for the zmq to connect 
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