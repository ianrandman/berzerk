from skimage.measure import block_reduce
from . import look_around
from . import network
import numpy as np
import time

network_file = 'neat_agent/network_data.dat'


def get_move(outputs):
    max = -1000
    for output in outputs:
        if output > max:
            max = output
    return outputs.index(max)


class NEATAgent(object):
    """The world's simplest agent!"""
    def __init__(self, action_space):
        self.action_space = action_space
        # data
        ########################################
        self.is_level_end = True
        self.start_time = time.time()

        self.num_levels = 0
        self.total_steps = 0
        self.elapsed_time = 0
        ########################################

    def is_start_of_level(self, observation):
        if observation[4][4][0] != 0 and self.is_level_end:
            self.is_level_end = False
            return True

    def is_end_of_level(self, observation):
        if observation[4][4][0] == 0:
            self.is_level_end = True

        # You should modify this function

    def act(self, observation, reward, done):
        # data
        ###################################################
        self.total_steps += 1

        self.is_end_of_level(observation)
        if self.is_start_of_level(observation):
            self.num_levels += 1

        elif done:
            self.elapsed_time = time.time() - self.start_time

        ###################################################

        brain = network.load_network(network_file)
        data = block_reduce(observation, block_size=(2, 2, 1), func=np.max)
        vision = look_around.parse_observations(data)
        if vision is None:  # no player object on screen
            return self.action_space.sample()
        else:
            move = get_move(brain.activate(vision))
            return move
