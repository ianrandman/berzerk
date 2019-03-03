import argparse
import random

import numpy as np
#import pdb
import gym
from gym import logger

import sys
sys.path.append('/non_learning_agent')
# from non_learning_agent.non_learning_agent import NonLearningAgent
from neat_agent.neat_agent import NEATAgent
from random_agent.random_agent import RandomAgent

class Agent(object):
    """The world's simplest agent!"""
    def __init__(self, action_space):
        self.action_space = action_space

    # You should modify this function
    def act(self, observation, reward, done):
        return self.action_space.sample()


## YOU MAY NOT MODIFY ANYTHING BELOW THIS LINE OR USE
## ANOTHER MAIN PROGRAM
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('--env_id', nargs='?', default='Berzerk-v0', help='Select the environment to run')
    args = parser.parse_args()

    # You can set the level to logger.DEBUG or logger.WARN if you
    # want to change the amount of output.
    # logger.set_level(logger.INFO)

    print("run number, score, number of levels, total steps, total elapsed time")

    for i in range(100):
        env = gym.make(args.env_id)

        # You provide the directory to write to (can be an existing
        # directory, including one with existing data -- all monitor files
        # will be namespaced). You can also dump to a tempdir if you'd
        # like: tempfile.mkdtemp().
        outdir = 'random-agent-results'


        env.seed(0)
        agent = NEATAgent(env.action_space)

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
            # env.render()

        agent.act(ob, reward, done)

        agent_num_levels = agent.num_levels
        agent_total_steps = agent.total_steps
        agent_elapsed_time = agent.elapsed_time
        # Close the env and write monitor result info to disk
        #print ("Your score: %d" % score)
        print(str(i+1)+', '+str(score)+', '+str(agent_num_levels)+', '+str(agent_total_steps)+', '+str(agent_elapsed_time))
        env.close()
