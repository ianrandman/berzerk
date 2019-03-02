import math
from non_learning_agent import find_next_move


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