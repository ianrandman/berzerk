import argparse
import gym
import os
import numpy as np
from skimage.measure import block_reduce

from . import look_around
from . import network
from . import neat_agent
import neat

first_genome = None

PLAYER_CLR = np.array([240, 170, 103])
BLACK_CLR = np.array([0, 0, 0])
WALL_CLR = np.array([84, 92, 214])

SCORE_FACTOR = 3
LEVEL_FACTOR = 0.5
TIME_FACTOR = 1


class Agent(object):
    """The world's simplest agent!"""
    def __init__(self, action_space):
        self.action_space = action_space

    # You should modify this function
    def act(self, data, reward, done, brain):

        vision = look_around.parse_observations(data)
        if vision is None:  # no player object on screen
            return self.action_space.sample()
        else:
            move = neat_agent.get_move(brain.activate(vision))
            return move


def eval_genome(genome, config):
    brain = neat.nn.FeedForwardNetwork.create(genome, config)

    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('--env_id', nargs='?', default='Berzerk-v0', help='Select the environment to run')
    args = parser.parse_args()
    # logger.set_level(logger.INFO)
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
    data = block_reduce(ob, block_size=(2, 2, 1), func=np.max)
    idle_count = 0
    idle_limit = 100
    steps = 0
    max_steps = 0
    is_level_end = True
    extra_levels = -3
    while not done:
        if ob[4][4][0] == 0:
            is_level_end = True
        else:
            if is_level_end:
                # now the start of level
                is_level_end = False
                extra_levels += 1
                if steps > max_steps:
                    max_steps = steps
                steps = 0
        steps += 1
        action = agent.act(data, reward, done, brain)
        if action <= 1 or action >= 10:  # shooting and not moving
            idle_count += 1
        else:
            idle_count = 0
        if idle_count == idle_limit:
            break
        ob, reward, done, x = env.step(action)
        score += reward
        # env.render()

    # Close the env and write monitor result info to disk
    env.close()
    if steps > max_steps:
        max_steps = steps
    fitness = ((SCORE_FACTOR*normalize_score(score)) - (TIME_FACTOR*normalize_time_penalty(steps))
            + (LEVEL_FACTOR*extra_levels))
    print(fitness)
    return fitness


def normalize_score(score):
    max_score = 2000
    normal_factor = 0.3
    return (1/pow(max_score, normal_factor))*pow(score, normal_factor)


def normalize_time_penalty(steps):
    allowed_steps = 250
    deduction = 0.1  # deduction per step amount
    step_amount = 50
    if steps < allowed_steps:
        return 0
    print('OVER TIME LIMIT')
    return (deduction / step_amount) * (steps-allowed_steps)


def normalize_exit_distance(distance):
    board_height = 85
    normal_factor = 0.7
    if distance is not None:
        return (-(1/pow(board_height, normal_factor)))*pow(distance, normal_factor)+1
    return 0


def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    print(config.genome_config.compatibility_weight_coefficient)

    # Create the population, which is the top-level object for a NEAT run.
    # p = neat.Population(config)
    p = neat.Checkpointer.restore_checkpoint('checkpoints/fitness2/neat-checkpoint-195')

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    # Run until goal is met
    pe = neat.ParallelEvaluator(6, eval_genome)
    winner = p.run(pe.evaluate, 10000)

    net = neat.nn.FeedForwardNetwork.create(winner, config)
    network.save_network(net, 'network_data.dat')

## YOU MAY NOT MODIFY ANYTHING BELOW THIS LINE OR USE
## ANOTHER MAIN PROGRAM
if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    run(config_path)

