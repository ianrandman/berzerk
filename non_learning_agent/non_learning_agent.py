import random
from skimage.measure import block_reduce
import time

import numpy as np

from . import look_around
from . import figure_out_action


class NonLearningAgent(object):
    """The world's simplest agent!"""

    def __init__(self, action_space):
        self.action_space = action_space

        self.random_move = False

        # data
        ########################################
        self.is_level_end = True
        self.start_time = time.time()

        self.num_levels = 0
        self.total_steps = 0
        self.elapsed_time = 0

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

        # reduces the size of the observation for quicker analysis
        new_obs = block_reduce(observation, block_size=(2, 2, 1), func=np.max)

        player_center = look_around.get_player_center(new_obs)
        vision = look_around.parse_observations(new_obs, player_center)

        if vision is None:
            return 0

        exits = look_around.find_exits(new_obs)

        if look_around.is_friendly_bullet_in_air(new_obs):
            if self.random_move:
                self.random_move = False
                return random.randint(2, 9)
            else:
                action = figure_out_action.move(vision, new_obs, player_center, exits)
                if action != -1:
                    self.random_move = True
                    return action
        else:
            if True:  # not self.just_fired:
                action = figure_out_action.try_shoot_enemy(vision)
                if action != -1:
                    return action

            if self.random_move:
                self.random_move = False
                return random.randint(2, 9)
            else:
                action = figure_out_action.move(vision, new_obs, player_center, exits)
                if action != -1:
                    self.random_move = True
                    return action

        # sleep(0.00)
        # plt.imshow(new_obs)
        # plt.show()

        print("why did it get down here")
        return 0