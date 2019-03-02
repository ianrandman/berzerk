import argparse
import math
import random

import numpy as np
#import pdb
import gym
from gym import logger
from skimage.measure import block_reduce

from non_learning_agent import find_next_move, analyze


class Agent(object):
    """The world's simplest agent!"""
    def __init__(self, action_space):
        self.action_space = action_space

        self.random_move = False

    # You should modify this function
    def act(self, observation, reward, done):
        # reduces the size of the observation for quicker analysis
        new_obs = block_reduce(observation, block_size=(2, 2, 1), func=np.max)

        player_center = analyze.get_player_center(new_obs)
        vision = analyze.parse_observations(new_obs, player_center)

        if vision is None:
            return 0

        exits = analyze.find_exits(new_obs)

        if analyze.is_friendly_bullet_in_air(new_obs):
            if self.random_move:
                self.random_move = False
                return random.randint(2, 9)
            else:
                action = move(vision, new_obs, player_center, exits)
                if action != -1:
                    self.random_move = True
                    return action
        else:
            if True:#not self.just_fired:
                action = try_shoot_enemy(vision)
                if action != -1:
                    return action

            if self.random_move:
                self.random_move = False
                return random.randint(2, 9)
            else:
                action = move(vision, new_obs, player_center, exits)
                if action != -1:
                    self.random_move = True
                    return action

        #sleep(0.00)
        #plt.imshow(new_obs)
        #plt.show()

        print("why did it get down here")
        return 0


def distance_to_exit(player_center, exit):
    return math.hypot((player_center[0] - exit[0]), (player_center[1] - exit[1]))


def find_direction(start_location, end_location):
    start_x = start_location[0]
    start_y = start_location[1]
    end_x = end_location[0]
    end_y = end_location[1]

    if end_x - start_x < 0: # left
        if end_y - start_y < 0: # up
            return 14
        elif end_y - start_y == 0: # no movement y
            return 12
        elif end_y - start_y > 0: # down
            return 10
    elif end_x - start_x == 0: # no movement x
        if end_y - start_y < 0: # up
            return 0
        elif end_y - start_y > 0: # down
            return 8
    elif end_x - start_x > 0: # right
        if end_y - start_y < 0: # up
            return 2
        elif end_y - start_y == 0: # no movement y
            return 4
        elif end_y - start_y > 0: # down
            return 6

    return -1 # should never get here


def fix_action(vision, action):
    if action == 2: # UP
        if -1 < vision[15][1] < 4 or -1 < vision[14][1] < 4:
            return 3 # RIGHT
        if -1 < vision[1][1] < 4 or -1 < vision[2][1] < 4:
            return 4 # LEFT
        return 2
    if action == 6:  # UPRIGHT
        if -1 < vision[0][1] < 4 or -1 < vision[1][1] < 4:
            return 3  # RIGHT
        if -1 < vision[3][1] < 4 or -1 < vision[4][1] < 4:
            return 2  # UP
        return 6
    if action == 3:  # RIGHT
        if -1 < vision[2][1] < 4 or -1 < vision[3][1] < 4:
            return 5  # DOWN
        if -1 < vision[5][1] < 4 or -1 < vision[6][1] < 4:
            return 2  # UP
        return 3
    if action == 8:  # DOWNRIGHT
        if -1 < vision[4][1] < 4 or -1 < vision[5][1] < 4:
            return 5  # DOWN
        if -1 < vision[7][1] < 4 or -1 < vision[8][1] < 4:
            return 3  # RIGHT
        return 8
    if action == 5: # DOWN
        if -1 < vision[6][1] < 4 or -1 < vision[7][1] < 4:
            return 4 # LEFT
        if -1 < vision[9][1] < 4 or -1 < vision[10][1] < 4:
            return 3 # RIGHT
        return 5
    if action == 9: # DOWNLEFT
        if -1 < vision[8][1] < 4 or -1 < vision[9][1] < 4:
            return 4 # LEFT
        if -1 < vision[11][1] < 4 or -1 < vision[12][1] < 4:
            return 5 # DOWN
        return 9
    if action == 4: # LEFT
        if -1 < vision[10][1] < 4 or -1 < vision[11][1] < 4:
            return 2 # UP
        if -1 < vision[13][1] < 4 or -1 < vision[14][1] < 4:
            return 5 # DOWN
        return 4
    if action == 7: # UPLEFT
        if -1 < vision[12][1] < 4 or -1 < vision[13][1] < 4:
            return 2 # UP
        if -1 < vision[15][1] < 4 or -1 < vision[0][1] < 4:
            return 4 # LEFT
        return 7


def move(vision, obs, player_center, exits):
    closest_exit_index = 0
    exit_index = -1
    distance_to_closest_exit = 1000 # big enough value
    for exit in exits:
        exit_index += 1

        dte = distance_to_exit(player_center, exit)
        if dte < distance_to_closest_exit:
            distance_to_closest_exit = dte
            closest_exit_index = exit_index

    exit_location = exits[closest_exit_index]
    next_position = find_next_move.astar_next_direction(obs, player_center, exit_location, vision)
    direction_index = find_direction(player_center, next_position)

    direction_to_action = {-1: -1, 0: 2, 1: 6, 2: 6, 3: 6, 4: 3, 5: 8, 6: 8, 7: 8, 8: 5,
                           9: 9, 10: 9, 11: 9, 12: 4, 13: 7, 14: 7, 15: 7}

    action = direction_to_action[direction_index]

    return action


def try_shoot_enemy(vision):
    worry_direction_index = -1
    worry_distance = 1000 # big enough value

    direction_index = -1
    for direction in vision: # check for bullets
        direction_index += 1

        if direction_index % 4 == 0 and direction[3] != -1 and direction[3] < direction[1] and direction[3] < worry_distance:
            worry_direction_index = direction_index
            worry_distance = direction[3]

    if worry_direction_index == -1:
        direction_index = -1
        for direction in vision:  # check for bullets
            direction_index += 1

            if not direction_index % 4 != 0 and direction[3] != -1 and direction[3] < direction[1] and direction[
                3] < worry_distance:
                worry_direction_index = direction_index
                worry_distance = direction[3]

    direction_to_action = {-1: -1, 0: 10, 1: 14, 2: 14, 3: 14, 4: 11, 5: 16, 6: 16, 7: 16, 8: 13,
                           9: 17, 10: 17, 11: 17, 12: 12, 13: 15, 14: 15, 15: 15}

    action = direction_to_action[worry_direction_index]
    if worry_direction_index == -1: # check for enemies
        direction_index = -1
        for direction in vision:
            direction_index += 1

            if direction_index % 4 == 0 and direction[0] != -1 and direction[0] < direction[1] and direction[0] < worry_distance:
                worry_direction_index = direction_index
                worry_distance = direction[0]

        if worry_direction_index == -1:
            direction_index = -1
            for direction in vision:
                direction_index += 1

                if direction_index % 4 != 0 and direction[0] != -1 and direction[0] < direction[1] and direction[
                    0] < worry_distance:
                    worry_direction_index = direction_index
                    worry_distance = direction[0]

        if worry_direction_index != -1:
            action = direction_to_action[worry_direction_index]

    else:
        z = 1
    return action


# def is_friendly_bullet_in_air(vision):
#     for direction in vision:
#         if direction[4] != -1:
#             return True
#
#     return False

## YOU MAY NOT MODIFY ANYTHING BELOW THIS LINE OR USE
## ANOTHER MAIN PROGRAM
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('--env_id', nargs='?', default='Berzerk-v0', help='Select the environment to run')
    args = parser.parse_args()

    # You can set the level to logger.DEBUG or logger.WARN if you
    # want to change the amount of output.
    logger.set_level(logger.INFO)

    env = gym.make(args.env_id)

    # You provide the directory to write to (can be an existing
    # directory, including one with existing data -- all monitor files
    # will be namespaced). You can also dump to a tempdir if you'd
    # like: tempfile.mkdtemp().
    outdir = 'random-agent-results'


    env.seed(0)
    agent = Agent(env.action_space)

    episode_count = 100
    reward = 0
    done = False
    score = 0
    special_data = {}
    special_data['ale.lives'] = 3
    ob = env.reset()
    while not done:
        
        action = agent.act(ob, reward, done)
        ob, reward, done, x = env.step(action)
        score += reward
        env.render()
     
    # Close the env and write monitor result info to disk
    print ("Your score: %d" % score)
    env.close()
