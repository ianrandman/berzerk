from non_learning_agent import look_around
import math
from astar import AStar
import numpy as np


class PathSolver(AStar):
    def __init__(self, obs, start, end, vision):
        self.obs = obs
        self.new_obs = transform_obs(obs, start)
        self.start = start
        self.end = end
        self.vision = vision

        self.algorithm_start = True

    def heuristic_cost_estimate(self, current, goal):
        return math.hypot((current[0] - goal[0]), (current[1] - goal[1]))

    def distance_between(self, n1, n2):
        if n1[0] - n2[0] == 0 or n1[1] - n2[1] == 0:
            path_cost = 1
        else:  # diagonal
            path_cost = 1.4142136

        return path_cost

    def neighbors(self, current_node):
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            node_position = (current_node[0] + new_position[0], current_node[1] + new_position[1])

            too_close_to_wall = False

            vertical_distance_from_wall = 9
            horizontal_distance_from_wall = 5

            # check for walls within specified vertical and horizontal radii
            check_position_x = node_position[0] - horizontal_distance_from_wall
            while check_position_x <= node_position[0] + horizontal_distance_from_wall:
                check_position_y = node_position[1] - vertical_distance_from_wall

                if not 0 < check_position_x < 79:
                    check_position_x += 1
                    continue

                while check_position_y <= node_position[1] + vertical_distance_from_wall:
                    if not 0 < check_position_y < 109:
                        check_position_y += 1
                        continue

                    if self.new_obs[check_position_y][check_position_x] == 1:  # wall color
                        too_close_to_wall = True
                        break

                    check_position_y += 1

                check_position_x += 1

            if not too_close_to_wall:  # wall color
                children.append(node_position)

            # if self.obs[node_position[1]][node_position[0]] != 1:  # wall color
            #     children.append(node_position)

        if self.algorithm_start and len(children) == 0: # if frame skipping caused the agent to get too close to a wall, move away
            vision = look_around.look_around(self.obs, self.start, shift=False)

            closest_wall_direction = 0
            direction_index = -1
            distance_to_closest_wall = 1000  # big enough value
            for direction in vision:
                direction_index += 1

                if direction[1] != -1 and direction[1] < distance_to_closest_wall:
                    distance_to_closest_wall = direction[1]
                    closest_wall_direction = direction_index

            if closest_wall_direction == 0:
                new_position = (0, 1)
            elif closest_wall_direction == 1:
                new_position = (-1, 1)
            elif closest_wall_direction == 2:
                new_position = (-1, 1)
            elif closest_wall_direction == 3:
                new_position = (-1, 1)
            elif closest_wall_direction == 4:
                new_position = (-1, 0)
            elif closest_wall_direction == 5:
                new_position = (-1, -1)
            elif closest_wall_direction == 6:
                new_position = (-1, -1)
            elif closest_wall_direction == 7:
                new_position = (-1, -1)
            elif closest_wall_direction == 8:
                new_position = (0, -1)
            elif closest_wall_direction == 9:
                new_position = (1, -1)
            elif closest_wall_direction == 10:
                new_position = (1, -1)
            elif closest_wall_direction == 11:
                new_position = (1, -1)
            elif closest_wall_direction == 12:
                new_position = (1, 0)
            elif closest_wall_direction == 13:
                new_position = (1, 1)
            elif closest_wall_direction == 14:
                new_position = (1, 1)
            elif closest_wall_direction == 15:
                new_position = (1, 1)

            self.move = (current_node[0] + new_position[0], current_node[1] + new_position[1])

        self.algorithm_start = False
        return children

    def solve(self):
        try:
            path = list(self.astar(self.start, self.end))
            return path[1]
        except TypeError: # no path
            return self.move


def transform_obs(obs, player_center):
    new_obs = np.ndarray(shape=(105, 80))
    for row in range(obs.shape[0]):
        for col in range(obs.shape[1]):
            color = obs[row][col]
            if np.array_equal(color, look_around.WALL_CLR):
                new_obs[row][col] = 1
            else:
                new_obs[row][col] = 0
            new_obs[player_center[1]][player_center[0]] = -1

    return new_obs


def astar_next_direction(obs, start, end, vision):
    return PathSolver(obs, start, end, vision).solve()


class Node():
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def old_astar_next_direction(obs, start, end):
    open_list = []
    closed_list = []

    start_node = Node(start)

    end_node = Node(end)

    open_list.append(start_node)

    while len(open_list) > 0:
        current_node = open_list[0]
        current_node_index = 0

        open_list_index = -1
        for node in open_list:
            open_list_index += 1
            if node.f < current_node.f:
                current_node_index = open_list_index
                current_node = node

        open_list.pop(current_node_index)
        closed_list.append(current_node)

        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            path = path[::-1]  # Return reversed path

            #current_node = current_node.parent
            return path[1]

        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if obs[node_position[1]][node_position[0]] != 1: # wall color
                children.append(Node(node_position, current_node))

        for child in children:
            if child.position[0] - current_node.position[0] == 0 or child.position[1] - current_node.position[1] == 0:
                path_cost = 1
            else: # diagonal
                path_cost = 2

            child_current_cost = current_node.g + path_cost

            if child in open_list and child_current_cost < child.g:
                open_list.remove(child)
            if child in closed_list and child_current_cost < child.g:
                closed_list.remove(child)
            if child not in open_list and child not in closed_list:
                child.g = child_current_cost
                open_list.append(child)

                child.h = math.sqrt(((child.position[0] - end_node.position[0]) ** 2) + (
                        (child.position[1] - end_node.position[1]) ** 2))
                child.f = child.g + child.h

                child.parent = current_node
