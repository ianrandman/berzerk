import numpy as np
from non_learning_agent import analyze
import math

PLAYER_CLR = np.array([240, 170, 103])
BLACK_CLR = np.array([0, 0, 0])
WALL_CLR = np.array([84, 92, 214])

RIGHT_EDGE = 78
SMALL_EDGE = 1
BOTTOM_EDGE = 90


def look_around(obs, the_player_center, shift):
    if shift:
        player_center = (the_player_center[0] + 2, the_player_center[1] - 3)
    else:
        player_center = (the_player_center[0], the_player_center[1])

    return [look_up(obs, player_center) ,                   # 0
            look_up_right_skip_x(obs, player_center) ,      # 1
            look_45_up_right(obs, player_center) ,          # 2
            look_up_right_skip_y(obs, player_center) ,      # 3
            look_right(obs, player_center) ,                # 4
            look_down_right_skip_y(obs, player_center) ,    # 5
            look_45_down_right(obs, player_center) ,        # 6
            look_down_right_skip_x(obs, player_center) ,    # 7
            look_down(obs, player_center) ,                 # 8
            look_down_left_skip_x(obs, player_center) ,     # 9
            look_45_down_left(obs, player_center) ,         # 10
            look_down_left_skip_y(obs, player_center) ,     # 11
            look_left(obs, player_center) ,                 # 12
            look_up_left_skip_y(obs, player_center) ,       # 13
            look_45_up_left(obs, player_center) ,           # 14
            look_up_left_skip_x(obs, player_center)]        # 15


def look_right(obs, player_center):
    right_observations = [-1, -1, [-1, (-1, -1)], -1, -1]  # enemy, wall, exit, enemy bullet, friendly bullet
    max_dist = RIGHT_EDGE  # TODO may need adjusted to reach wall
    player_sprite_cooldown = 2
    distance_looked = 0
    x = player_center[0] + distance_looked
    y = player_center[1]
    while x < max_dist:
        distance_looked += 1
        x = player_center[0] + distance_looked
        player_sprite_cooldown = analyze_one_pixel(obs, x, y, right_observations, distance_looked, player_sprite_cooldown, max_dist, 0, player_center)
    return right_observations


def look_left(obs, player_center):
    observations = [-1, -1, [-1, (-1, -1)], -1, -1]  # enemy, wall, exit, enemy bullet, friendly bullet
    max_dist = SMALL_EDGE  # TODO may need adjusted to reach wall
    player_sprite_cooldown = 2
    distance_looked = 0
    x = player_center[0] - distance_looked
    y = player_center[1]
    while x > max_dist:
        distance_looked += 1
        x = player_center[0] - distance_looked
        player_sprite_cooldown = analyze_one_pixel(obs, x, y, observations, distance_looked, player_sprite_cooldown, RIGHT_EDGE, 0, player_center)
    return observations


def look_up(obs, player_center):
    observations = [-1, -1, [-1, (-1, -1)], -1, -1]  # enemy, wall, exit, enemy bullet, friendly bullet
    max_dist = SMALL_EDGE  # TODO may need adjusted to reach wall
    player_sprite_cooldown = 5
    distance_looked = 0
    x = player_center[0]
    y = player_center[1] - distance_looked
    while y > max_dist:
        distance_looked += 1
        y = player_center[1] - distance_looked
        player_sprite_cooldown = analyze_one_pixel(obs, x, y, observations, distance_looked, player_sprite_cooldown, BOTTOM_EDGE, 1, player_center)
    return observations


def look_down(obs, player_center):
    observations = [-1, -1, [-1, (-1, -1)], -1, -1]  # enemy, wall, exit, enemy bullet, friendly bullet
    max_dist = BOTTOM_EDGE  # TODO may need adjusted to reach wall
    player_sprite_cooldown = 5
    distance_looked = 0
    x = player_center[0]
    y = player_center[1] + distance_looked
    while y < max_dist:
        distance_looked += 1
        y = player_center[1] + distance_looked
        player_sprite_cooldown = analyze_one_pixel(obs, x, y, observations, distance_looked, player_sprite_cooldown, max_dist, 1, player_center)
    return observations


def look_45_up_right(obs, player_center):
    observations = [-1, -1, [-1, (-1, -1)], -1, -1]  # enemy, wall, exit, enemy bullet, friendly bullet
    max_y = SMALL_EDGE
    max_x = RIGHT_EDGE
    player_sprite_cooldown = 2
    distance_looked = 0
    x = player_center[0] + distance_looked
    y = player_center[1] - distance_looked
    while y > max_y and x < max_x:
        distance_looked += 1
        x = player_center[0] + distance_looked
        y = player_center[1] - distance_looked
        player_sprite_cooldown = analyze_one_pixel(obs, x, y, observations, distance_looked, player_sprite_cooldown, max_x, 0, player_center)
    return observations


def look_45_down_right(obs, player_center):
    observations = [-1, -1, [-1, (-1, -1)], -1, -1]  # enemy, wall, exit, enemy bullet, friendly bullet
    max_y = BOTTOM_EDGE
    max_x = RIGHT_EDGE
    player_sprite_cooldown = 2
    distance_looked = 0
    x = player_center[0] + distance_looked
    y = player_center[1] + distance_looked
    while y < max_y and x < max_x:
        distance_looked += 1
        x = player_center[0] + distance_looked
        y = player_center[1] + distance_looked
        player_sprite_cooldown = analyze_one_pixel(obs, x, y, observations, distance_looked, player_sprite_cooldown, max_x, 0, player_center)
    return observations


def look_45_up_left(obs, player_center):
    observations = [-1, -1, [-1, (-1, -1)], -1, -1]  # enemy, wall, exit, enemy bullet, friendly bullet
    max_y = SMALL_EDGE
    max_x = SMALL_EDGE
    player_sprite_cooldown = 2
    distance_looked = 0
    x = player_center[0] - distance_looked
    y = player_center[1] - distance_looked
    while y > max_y and x > max_x:
        distance_looked += 1
        x = player_center[0] - distance_looked
        y = player_center[1] - distance_looked
        player_sprite_cooldown = analyze_one_pixel(obs, x, y, observations, distance_looked, player_sprite_cooldown, RIGHT_EDGE, 0, player_center)
    return observations

def look_45_down_left(obs, player_center):
    observations = [-1, -1, [-1, (-1, -1)], -1, -1]  # enemy, wall, exit, enemy bullet, friendly bullet
    max_y = BOTTOM_EDGE
    max_x = SMALL_EDGE
    player_sprite_cooldown = 2
    distance_looked = 0
    x = player_center[0] - distance_looked
    y = player_center[1] + distance_looked
    while y < max_y and x > max_x:
        distance_looked += 1
        x = player_center[0] - distance_looked
        y = player_center[1] + distance_looked
        player_sprite_cooldown = analyze_one_pixel(obs, x, y, observations, distance_looked, player_sprite_cooldown, RIGHT_EDGE, 0, player_center)
    return observations


def look_up_right_skip_x(obs, player_center):
    observations = [-1, -1, [-1, (-1, -1)], -1, -1]  # enemy, wall, exit, enemy bullet, friendly bullet
    max_y = SMALL_EDGE
    max_x = RIGHT_EDGE
    player_sprite_cooldown = 2
    distance_looked = 0
    increment_x = False
    x = player_center[0] - distance_looked
    y = player_center[1] + distance_looked
    while y > max_y and x < max_x:
        distance_looked += 1
        increment_x = not increment_x
        if increment_x:
            x = x + 1
        y = player_center[1] - distance_looked
        player_sprite_cooldown = analyze_one_pixel(obs, x, y, observations, distance_looked, player_sprite_cooldown, max_x, 0, player_center)
    return observations


def look_up_right_skip_y(obs, player_center):
    observations = [-1, -1, [-1, (-1, -1)], -1, -1]  # enemy, wall, exit, enemy bullet, friendly bullet
    max_y = SMALL_EDGE
    max_x = RIGHT_EDGE
    player_sprite_cooldown = 2
    distance_looked = 0
    increment_y = False
    x = player_center[0] + distance_looked
    y = player_center[1] - distance_looked
    while y > max_y and x < max_x:
        distance_looked += 1
        increment_y = not increment_y
        if increment_y:
            y = y - 1
        x = player_center[0] + distance_looked
        player_sprite_cooldown = analyze_one_pixel(obs, x, y, observations, distance_looked, player_sprite_cooldown, max_x, 0, player_center)
    return observations


def look_down_right_skip_x(obs, player_center):
    observations = [-1, -1, [-1, (-1, -1)], -1, -1]  # enemy, wall, exit, enemy bullet, friendly bullet
    max_y = BOTTOM_EDGE
    max_x = RIGHT_EDGE
    player_sprite_cooldown = 2
    distance_looked = 0
    increment_x = False
    x = player_center[0] + distance_looked
    y = player_center[1] + distance_looked
    while y < max_y and x < max_x:
        distance_looked += 1
        increment_x = not increment_x
        if increment_x:
            x = x + 1
        y = player_center[1] + distance_looked
        player_sprite_cooldown = analyze_one_pixel(obs, x, y, observations, distance_looked, player_sprite_cooldown, max_x, 0, player_center)
    return observations


def look_down_right_skip_y(obs, player_center):
    observations = [-1, -1, [-1, (-1, -1)], -1, -1]  # enemy, wall, exit, enemy bullet, friendly bullet
    max_y = BOTTOM_EDGE
    max_x = RIGHT_EDGE
    player_sprite_cooldown = 2
    distance_looked = 0
    increment_y = False
    x = player_center[0] + distance_looked
    y = player_center[1] + distance_looked
    while y < max_y and x < max_x:
        distance_looked += 1
        increment_y = not increment_y
        if increment_y:
            y = y + 1
        x = player_center[0] + distance_looked
        player_sprite_cooldown = analyze_one_pixel(obs, x, y, observations, distance_looked, player_sprite_cooldown, max_x, 0, player_center)
    return observations


def look_up_left_skip_x(obs, player_center):
    observations = [-1, -1, [-1, (-1, -1)], -1, -1]  # enemy, wall, exit, enemy bullet, friendly bullet
    max_y = SMALL_EDGE
    max_x = SMALL_EDGE
    player_sprite_cooldown = 2
    distance_looked = 0
    increment_x = False
    x = player_center[0] - distance_looked
    y = player_center[1] - distance_looked
    while y > max_y and x > max_x:
        distance_looked += 1
        increment_x = not increment_x
        if increment_x:
            x = x - 1
        y = player_center[1] - distance_looked
        player_sprite_cooldown = analyze_one_pixel(obs, x, y, observations, distance_looked, player_sprite_cooldown, RIGHT_EDGE, 0, player_center)
    return observations


def look_up_left_skip_y(obs, player_center):
    observations = [-1, -1, [-1, (-1, -1)], -1, -1]  # enemy, wall, exit, enemy bullet, friendly bullet
    max_y = SMALL_EDGE
    max_x = SMALL_EDGE
    player_sprite_cooldown = 2
    distance_looked = 0
    increment_y = False
    x = player_center[0] - distance_looked
    y = player_center[1] - distance_looked
    while y > max_y and x > max_x:
        distance_looked += 1
        increment_y = not increment_y
        if increment_y:
            y = y - 1
        x = player_center[0] - distance_looked
        player_sprite_cooldown = analyze_one_pixel(obs, x, y, observations, distance_looked, player_sprite_cooldown, RIGHT_EDGE, 0, player_center)
    return observations


def look_down_left_skip_x(obs, player_center):
    observations = [-1, -1, [-1, (-1, -1)], -1, -1]  # enemy, wall, exit, enemy bullet, friendly bullet
    max_y = BOTTOM_EDGE
    max_x = SMALL_EDGE
    player_sprite_cooldown = 2
    distance_looked = 0
    increment_x = False
    x = player_center[0] - distance_looked
    y = player_center[1] + distance_looked
    while y < max_y and x > max_x:
        distance_looked += 1
        increment_x = not increment_x
        if increment_x:
            x = x - 1
        y = player_center[1] + distance_looked
        player_sprite_cooldown = analyze_one_pixel(obs, x, y, observations, distance_looked, player_sprite_cooldown, RIGHT_EDGE, 0, player_center)
    return observations


def look_down_left_skip_y(obs, player_center):
    observations = [-1, -1, [-1, (-1, -1)], -1, -1]  # enemy, wall, exit, enemy bullet, friendly bullet
    max_y = BOTTOM_EDGE
    max_x = SMALL_EDGE
    player_sprite_cooldown = 2
    distance_looked = 0
    increment_y = False
    x = player_center[0] - distance_looked
    y = player_center[1] + distance_looked
    while y < max_y and x > max_x:
        distance_looked += 1
        increment_y = not increment_y
        if increment_y:
            y = y + 1
        x = player_center[0] - distance_looked
        player_sprite_cooldown = analyze_one_pixel(obs, x, y, observations, distance_looked, player_sprite_cooldown, RIGHT_EDGE, 0, player_center)
    return observations


def distance_decay(dist, maxim):
    # function to calculate the input to the network based on the distance of an object
    # from the player. An object 1 pixel away returns 1.0, and an object 168 pixels away
    # (the distance from top to bottom) will return 0.0
    if dist <= 0:
        return 1.0
    return ((-1 / (math.sqrt(maxim - 1))) * (math.sqrt(dist - 1))) + 1


def analyze_one_pixel(obs, x, y, observations, distance_looked, player_sprite_cooldown, max_dist, lrud, player_center):
    # lrud is 0 if we are looking right/left, and 1 if we are looking up/down
    lr_factor = 1
    ud_factor = 4
    pixel = obs[y][x]
    if not np.array_equal(pixel, BLACK_CLR):
        if np.array_equal(pixel, PLAYER_CLR):
            if player_sprite_cooldown < 0:
                # found friendly bullet
                if observations[4] == -1:
                    if lrud == 0:
                        observations[4] = distance_looked - lr_factor#distance_decay(distance_looked - lr_factor, max_dist + 4)
                    else:
                        observations[4] = distance_looked - ud_factor#distance_decay(distance_looked - ud_factor, max_dist + 4)
            else:
                player_sprite_cooldown -= 1
        elif np.array_equal(pixel, WALL_CLR): # straight line distance, not pixel distance
            # found wall
            if observations[1] == -1:
                observations[1] = math.hypot(x - player_center[0], y - player_center[1])
        else:
            surrounding_values = [False, False, False, False]  # up, right, down, left
            ignore = [False, False, False, False]  # up, right, down, left
            prev_moves = []  # up, right, down, left
            check_proj = analyze.check_projectile(obs, y, x, surrounding_values, ignore, prev_moves, 5, 3)[0]
            if check_proj:
                # found enemy bullet
                if observations[3] == -1:
                    if lrud == 0:
                        observations[3] = distance_looked - lr_factor#distance_decay(distance_looked - lr_factor, max_dist + 4)
                    else:
                        observations[3] = distance_looked - ud_factor#distance_decay(distance_looked - ud_factor, max_dist + 4)
            else:
                # found enemy agent
                if observations[0] == -1:
                    if lrud == 0:
                        observations[0] = distance_looked - lr_factor#distance_decay(distance_looked - lr_factor, max_dist + 4)
                    else:
                        observations[0] = distance_looked - ud_factor#distance_decay(distance_looked - ud_factor, max_dist + 4)
    else:
        if lrud == 1: # left/right
            if x == 3 or x == 76:
                observations[2] = [distance_looked, (x, y)]
        else: # up/down
            if y == 3 or y == 88:
                observations[2] = [distance_looked, (x, y)]

    return player_sprite_cooldown

