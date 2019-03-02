import time

class RandomAgent(object):
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

        return self.action_space.sample()