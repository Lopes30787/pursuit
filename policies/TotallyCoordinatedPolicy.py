from .GreedyPolicy import GreedyPolicy


class TotallyCoordinatedPolicy(GreedyPolicy):
    def __init__(self, env):
        super().__init__(env)
        self.leaders = {"UPPER": None, "LOWER": None}
        self.groups = {}

    def __call__(self, observation, agent):
        evaders = observation[0]
        pursuers = observation[1]
        agent_pos = pursuers[agent]
        if len(self.groups) == 0:
            self.groups = self.calculate_groups(pursuers)
        selected_pos = self.get_closest(evaders, agent_pos, agent, self.groups)
        return self.get_move(selected_pos, agent_pos)

    def get_closest(self, evaders, agent, agent_name, groups):
        group = "UPPER" if agent_name in groups["UPPER"] else "LOWER"

        idx = groups[group].index(agent_name)
        
        if idx == 0 or self.leaders[group] == None: 
            closest = self.get_closest_evaders(evaders, agent, group)
            self.leaders[group] = closest[0]

        follow = self.leaders[group]

        match (idx):
            case 0:  # Up
                return [follow[0] + 1, follow[1]]
            case 1:  # Right
                return [follow[0], follow[1] + 1]
            case 2:  # Left
                return [follow[0], follow[1] - 1]
            case 3:  # Down
                return [follow[0] - 1, follow[1]]

    def get_closest_evaders(self, evaders, agent, group):
        if group == "UPPER":
            n_evaders = list(filter(lambda x: x[1] < 8, evaders))
        else:
            n_evaders = list(filter(lambda x: x[1] >= 8, evaders))

        if len(n_evaders) == 0:
            return sorted(evaders, key=lambda x: self.distance(x, agent))
        else:
            return sorted(n_evaders, key=lambda x: self.distance(x, agent))

    def calculate_groups(self, agents):
        agents = sorted(list(agents.items()), key = lambda x: x[1][1])
        
        return {
            "UPPER": list(map(lambda x: x[0], agents[:len(agents) // 2])),
            "LOWER": list(map(lambda x: x[0], agents[len(agents) // 2:]))
        }