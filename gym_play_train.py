import argparse
#import pdb
import gym
import os
import numpy
from skimage.measure import block_reduce

import neat
from non_learning_agent import analyze


def get_move(outputs):
    max = -1000
    for output in outputs:
        if output > max:
            max = output
    return outputs.index(max)


class Agent(object):
    """The world's simplest agent!"""
    def __init__(self, action_space):
        self.action_space = action_space

    # You should modify this function
    def act(self, observation, reward, done, brain):

        # reduces the size of the observation for quicker analysis
        data = block_reduce(observation, block_size=(2, 2, 1), func=numpy.max)

        # to save observation to file:
        # f = open('screenshots/screenshot'+str(i)+'.png', 'wb')  # binary mode is important
        # w = png.Writer(80, 105, greyscale=False)
        # new_observation = numpy.reshape(data, (-1, 240))
        # w.write(f, new_observation)
        # f.close()

        vision = analyze.parse_observations(data)
        if vision is None:  # no player object on screen
            return self.action_space.sample()
        else:
            move = get_move(brain.activate(vision))
            return move


def eval_genome(genome, config):
    brain = neat.nn.FeedForwardNetwork.create(genome, config)
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('--env_id', nargs='?', default='Berzerk-v0', help='Select the environment to run')
    args = parser.parse_args()
    #logger.set_level(logger.INFO)
    env = gym.make(args.env_id)
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
    idle_count = 0
    idle_limit = 100
    while not done:
        action = agent.act(ob, reward, done, brain)
        if action <= 1 or action >= 10:  # shooting and not moving
            idle_count += 1
        else:
            idle_count = 0
        if idle_count == idle_limit:
            break
        ob, reward, done, x = env.step(action)
        score += reward
        env.render()

    # Close the env and write monitor result info to disk
    print("Your score: %d" % score)
    env.close()
    return score

def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-13')

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    # Run until goal is met
    pe = neat.ParallelEvaluator(10, eval_genome)
    winner = p.run(pe.evaluate, 3000)

## YOU MAY NOT MODIFY ANYTHING BELOW THIS LINE OR USE
## ANOTHER MAIN PROGRAM
if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    run(config_path)