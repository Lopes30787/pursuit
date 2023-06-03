from .AbstractPolicy import AbstractPolicy
import numpy as np
import math

LEFT = 0
RIGHT = 1
DOWN = 2
UP = 3
STAY = 4


class GreedyPolicy(AbstractPolicy):

    def __call__(self, observation, agent):
        evaders = observation[0]
        pursuers = observation[1]
        agent_pos = pursuers[agent]
        selected_pos = self.get_closest(evaders, agent_pos)
        return self.get_move(selected_pos, agent_pos)

    def get_move(self, selected, agent):
        distances = np.array(selected) - np.array(agent)
        abs_distances = np.absolute(distances)
        if abs_distances[0] > abs_distances[1]:
            return self._close_horizontally(distances)
        elif abs_distances[0] < abs_distances[1]:
            return self._close_vertically(distances)
        else:
            roll = np.random.uniform(0, 1)
            return self._close_horizontally(distances) if roll > 0.5 else self._close_vertically(distances)

    def _close_horizontally(self, distances):
        if distances[0] > 0:
            return RIGHT
        elif distances[0] < 0:
            return LEFT
        else:
            return STAY

    def _close_vertically(self, distances):
        if distances[1] > 0:
            return DOWN
        elif distances[1] < 0:
            return UP
        else:
            return STAY

    def get_closest(self, evaders, agent):
        min_dist = math.inf
        selected = None
        for evader in evaders:
            dist = self.distance(evader, agent)

            if dist < min_dist:
                min_dist = dist
                selected = evader

        return selected

    def distance(self, evader, pursuer):
        return abs(evader[0] - pursuer[0]) + abs(evader[1] - pursuer[1])
