import numpy as np
import math

PLAYER_CLR = np.array([240, 170, 103])
BLACK_CLR = np.array([0, 0, 0])
WALL_CLR = np.array([84, 92, 214])

RIGHT_EDGE = 78
SMALL_EDGE = 1
BOTTOM_EDGE = 90


def look_around(obs, the_player_center, shift):
    if shift:
        player_center = (the_player_center[0] + 1, the_player_center[1] - 2)
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
            check_proj = check_projectile(obs, y, x, surrounding_values, ignore, prev_moves, 5, 3)[0]
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


def parse_observations(obs, player_center):
    #player_center = get_player_center(obs)
    if player_center is not None:
        vision = look_around(obs, player_center, shift=True)
        return vision


def is_friendly_bullet_in_air(obs):
    visited = []
    for j in range(4, 88):  # upper and lower bounds of the screen
        row = obs[j]
        for k in range(4, 76):  # left and right bounds of the screen
            pixel = row[k]
            if np.array_equal(pixel, PLAYER_CLR):
                if [k, j] not in visited:
                    surrounding_values = [False, False, False, False]  # up, right, down, left
                    ignore = [False, False, False, False]  # up, right, down, left
                    prev_moves = []  # up, right, down, left
                    check_proj = check_projectile(obs, j, k, surrounding_values, ignore, prev_moves, 5, 3)
                    visited = visited + check_proj[1]
                    if check_proj[0]:
                        return True

    return False


def find_exits(obs):
    exits = []
    start_exit = False

    for x in range(3, 77):
        if not start_exit and np.array_equal(obs[3, x], BLACK_CLR):
            start_exit = True
            start_of_exit = x
        if start_exit and np.array_equal(obs[3, x], WALL_CLR):
            start_exit = False
            end_of_exit = x - 1

            middle_of_exit_location = (int(round((start_of_exit + end_of_exit) / 2)), 3)
            exits.append(middle_of_exit_location)

    for x in range(3, 77):
        if not start_exit and np.array_equal(obs[88, x], BLACK_CLR):
            start_exit = True
            start_of_exit = x
        if start_exit and np.array_equal(obs[88, x], WALL_CLR):
            start_exit = False
            end_of_exit = x - 1

            middle_of_exit_location = (int(round((start_of_exit + end_of_exit)/2)), 88)
            exits.append(middle_of_exit_location)

    for y in range(3, 89):
        if not start_exit and np.array_equal(obs[y, 3], BLACK_CLR):
            start_exit = True
            start_of_exit = y - 1
        if start_exit and np.array_equal(obs[y, 3], WALL_CLR):
            start_exit = False
            end_of_exit = y - 1

            middle_of_exit_location = (3, int(round((start_of_exit + end_of_exit) / 2)))
            exits.append(middle_of_exit_location)

    for y in range(3, 89):
        if not start_exit and np.array_equal(obs[y, 76], BLACK_CLR):
            start_exit = True
            start_of_exit = y
        if start_exit and np.array_equal(obs[y, 76], WALL_CLR):
            start_exit = False
            end_of_exit = y

            middle_of_exit_location = (76, int(round((start_of_exit + end_of_exit) / 2)))
            exits.append(middle_of_exit_location)

    return exits


def get_player_center(obs):
    player_center = -1, -1
    visited = []
    for j in range(4, 88):  # upper and lower bounds of the screen
        row = obs[j]
        for k in range(4, 76):  # left and right bounds of the screen
            pixel = row[k]
            if np.array_equal(pixel, PLAYER_CLR):
                if [k, j] not in visited:
                    surrounding_values = [False, False, False, False]  # up, right, down, left
                    ignore = [False, False, False, False]  # up, right, down, left
                    prev_moves = []  # up, right, down, left
                    check_proj = check_projectile(obs, j, k, surrounding_values, ignore, prev_moves, 5, 3)
                    visited = visited + check_proj[1]
                    if not check_proj[0]:
                        if player_center == (-1, -1):
                            player_center = (k, j+5)
                            return player_center


def check_projectile(obs, y, x, surrounding_values, ignore, prev_moves, length_limit, width_limit):
    prev_moves.append([x, y])
    if length_limit == 0 or width_limit == 0:
        return False, prev_moves
    if [x, y - 1] in prev_moves:
        ignore[0] = True
    if [x + 1, y] in prev_moves:
        ignore[1] = True
    if [x, y + 1] in prev_moves:
        ignore[2] = True
    if [x - 1, y] in prev_moves:
        ignore[3] = True
    pixel_surrounding_values = check_pixel(obs, y, x, ignore)
    if pixel_surrounding_values is None:
        return False, \
               prev_moves
    for direction in range(0, 4):
        ignore = [False, False, False, False]  # up, right, down, left
        if pixel_surrounding_values[direction]:
            surrounding_values[direction] = True
        else:
            surrounding_values_cpy = surrounding_values[:]
            if direction == 0:  # up
                ignore[2] = True  # ignore down
                surrounding_values[0] = check_projectile(obs, y-1, x, surrounding_values_cpy, ignore, prev_moves, length_limit-1, width_limit)[0]
            elif direction == 1:  # right
                ignore[3] = True  # ignore left
                surrounding_values[1] = check_projectile(obs, y, x+1, surrounding_values_cpy, ignore, prev_moves, length_limit, width_limit-1)[0]
            elif direction == 2:  # down
                ignore[0] = True  # ignore up
                surrounding_values[2] = check_projectile(obs, y+1, x, surrounding_values_cpy, ignore, prev_moves, length_limit-1, width_limit)[0]
            elif direction == 3:  # left
                ignore[1] = True  # ignore right
                surrounding_values[3] = check_projectile(obs, y, x-1, surrounding_values_cpy, ignore, prev_moves, length_limit, width_limit-1)[0]
    test_return = True
    for direction in range(0, 4):
        test_return = test_return and surrounding_values[direction]
        if not test_return:
            break
    return test_return, prev_moves


def check_pixel(obs, x, y, ignore):
    # array of whether or not each of the directions is clear
    surrounding_values = [False, False, False, False]  # up, right, down, left
    # check up
    if not np.array_equal(obs[x - 1][y], obs[x][y]):  # one up is clear
        if not np.array_equal(obs[x - 2][y], obs[x][y]):  # two up is clear
            surrounding_values[0] = True
        else:  # one clear, but other not. Not a projectile
            return None
    # check right
    if not np.array_equal(obs[x][y + 1], obs[x][y]):  # one right is clear
        if not np.array_equal(obs[x][y + 2], obs[x][y]):  # two right is clear
            surrounding_values[1] = True
        else:  # one clear, but other not. Not a projectile
            return None
    # check down
    if not np.array_equal(obs[x + 1][y], obs[x][y]):  # one down is clear
        if not np.array_equal(obs[x + 2][y], obs[x][y]):  # two down is clear
            surrounding_values[2] = True
        else:  # one clear, but other not. Not a projectile
            return None
    # check left
    if not np.array_equal(obs[x][y - 1], obs[x][y]):  # one left is clear
        if not np.array_equal(obs[x][y - 2], obs[x][y]):  # two left is clear
            surrounding_values[3] = True
        else:  # one clear, but other not. Not a projectile
            return None

    if ignore[0]:
        surrounding_values[0] = True
    if ignore[1]:
        surrounding_values[1] = True
    if ignore[2]:
        surrounding_values[2] = True
    if ignore[3]:
        surrounding_values[3] = True
    return surrounding_values

