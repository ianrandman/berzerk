import random
from skimage.measure import block_reduce
import non_learning_agent as nla

import numpy as np


class NonLearningAgent(object):
    """The world's simplest agent!"""
    def __init__(self, action_space):
        self.action_space = action_space

        self.random_move = False

    # You should modify this function
    def act(self, observation, reward, done):
        # reduces the size of the observation for quicker analysis
        new_obs = block_reduce(observation, block_size=(2, 2, 1), func=np.max)

        player_center = nla.analyze.get_player_center(new_obs)
        vision = nla.analyze.parse_observations(new_obs, player_center)

        if vision is None:
            return 0

        exits = nla.analyze.find_exits(new_obs)

        if nla.analyze.is_friendly_bullet_in_air(new_obs):
            if self.random_move:
                self.random_move = False
                return random.randint(2, 9)
            else:
                action = nla.figure_out_action.move(vision, new_obs, player_center, exits)
                if action != -1:
                    self.random_move = True
                    return action
        else:
            if True:#not self.just_fired:
                action = nla.figure_out_action.try_shoot_enemy(vision)
                if action != -1:
                    return action

            if self.random_move:
                self.random_move = False
                return random.randint(2, 9)
            else:
                action = nla.figure_out_action.move(vision, new_obs, player_center, exits)
                if action != -1:
                    self.random_move = True
                    return action

        #sleep(0.00)
        #plt.imshow(new_obs)
        #plt.show()

        print("why did it get down here")
        return 0