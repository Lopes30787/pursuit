from .GreedyPolicy import GreedyPolicy
import itertools
import math


class MixedPolicy(GreedyPolicy):
    def __init__(self, env):
        super().__init__(env)
        self.groups = {}
        self.convention = None
        self.leaders = [None, None]
        self.follow = [None, None]

    def __call__(self, observation, agent):
        evaders = observation[0]
        pursuers = observation[1]
        agent_pos = pursuers[agent]

        if self.convention == None:
            self.calculate_groups(evaders, pursuers)

        selected_pos = self.get_closest(evaders, agent_pos, agent)
        return self.get_move(selected_pos, agent_pos)
    
    def get_closest(self, evaders, agent, agent_name):
        idx = self.get_id(agent_name)
        group = self.groups[idx]

        if self.leaders[group] == idx:
            closest = self.get_closest_evaders(evaders, agent, self.follow[group ^ 1])
            i = 1
            self.follow[group] = closest[0]
            while self.follow[group] == self.follow[group ^ 1] and i < len(closest):
                self.follow[group] = closest[i]
                i += 1

        follow = self.follow[group]

        match (self.convention[group].index(idx)):
            case 0:  # Up
                return [follow[0] + 1, follow[1]]
            case 1:  # Right
                return [follow[0], follow[1] + 1]
            case 2:  # Left
                return [follow[0], follow[1] - 1]
            case 3:  # Down
                return [follow[0] - 1, follow[1]]

    def calculate_groups(self, evaders, pursuers):
        # data structure - 0: cumulative distance, 1: combination of agents, 2: leader
        sums = []

        for comb in itertools.permutations(pursuers.keys(), 4):
            # up is leader
            self.calculate_helper(comb, evaders, pursuers, 0, sums)
            
            # right is leader
            self.calculate_helper(comb, evaders, pursuers, 1, sums)

            # left is leader
            self.calculate_helper(comb, evaders, pursuers, 2, sums)

            # down is leader
            self.calculate_helper(comb, evaders, pursuers, 3, sums)

        # data structure - 0: cumulative distance, 1: combination of agents, 2: leader
        possible = []
        for s1 in sums:
            for s2 in sums:
                if len(s1[1].union(s2[1])) == 8 and s1[2] != s2[2]:
                    possible.append((s1[0] + s2[0], (s1[1], s2[1]), [s1[2], s2[2]]))

        m = math.inf 
        for p in possible:
            if p[0] < m:
                m = p[0]
                self.convention = [list(p[1][0]), list(p[1][1])]
                self.leaders = p[2]
                
        if self.convention == None:
            # default convention just in case everything goes wrong
            self.convention = [[0, 1, 2, 3], [4, 5, 6, 7]]
            self.leaders = [0, 4]
                
        for agent in self.convention[0]:
            self.groups[agent] = 0

        for agent in self.convention[1]:
            self.groups[agent] = 1
        
    def calculate_helper(self, comb, evaders, pursuers, pos, sums):
        # due to evaders not being labeled, to avoid wrong agent moves the leader must be the agent with the lowest id of the group 
        if comb[pos] == sorted(comb)[0]:
            evader = self.get_closest_evaders(evaders, pursuers[comb[pos]], None)[0]
            sums.append((
                    self.cumulative_distance(comb, pursuers, evader),
                set(map(self.get_id, comb)),
                self.get_id(comb[pos])
            ))
        return sums
    
    def cumulative_distance(self, comb, pursuers, evader):
        return self.distance([evader[0] + 1, evader[1]], pursuers[comb[0]]) + \
                self.distance([evader[0], evader[1] + 1], pursuers[comb[1]]) + \
                self.distance([evader[0], evader[1] - 1], pursuers[comb[2]]) + \
                self.distance([evader[0] - 1, evader[1]], pursuers[comb[3]])
                
    def get_closest_evaders(self, evaders, agent, rival):
        if rival is not None:
            # intruduces a bias to influence the two groups to walk away from each other 
            BIAS = 0.775
            return sorted(evaders, key=lambda x: self.distance(x, agent) * BIAS - self.distance(x, rival) * (1 - BIAS))
        else:
            return sorted(evaders, key=lambda x: self.distance(x, agent))
