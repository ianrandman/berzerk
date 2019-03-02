import numpy as np
from . import look_around

PLAYER_CLR = np.array([240, 170, 103])
BLACK_CLR = np.array([0, 0, 0])
WALL_CLR = np.array([84, 92, 214])


def parse_observations(obs, player_center):
    #player_center = get_player_center(obs)
    if player_center is not None:
        vision = look_around.look_around(obs, player_center, shift=True)
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
