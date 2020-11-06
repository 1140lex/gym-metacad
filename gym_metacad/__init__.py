from gym.envs.registration import register
import logging

logger = logging.getLogger(__name__)

register(
    id='metacad-v0',
    entry_point='gym_metacad.envs:MetaCADEnv',
)
