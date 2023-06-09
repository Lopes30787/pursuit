from .GreedyPolicy import GreedyPolicy


class SocialPolicy(GreedyPolicy):
    def __init__(self, env):
        super().__init__(env)
        self.leaders = [None for _ in range(len(env.agents))]

    def __call__(self, observation, agent):
        evaders = observation[0]
        pursuers = observation[1]
        agent_pos = pursuers[agent]
        selected_pos = self.get_closest(evaders, agent_pos, agent)
        return self.get_move(selected_pos, agent_pos)

    def get_closest(self, evaders, agent, agent_name):
        idx = self.get_id(agent_name)

        if idx == 0 or idx == 1:
            closest = self.get_closest_evaders(evaders, agent)
            i = 1
            self.leaders[idx] = closest[0]
            while self.leaders[idx] == self.leaders[idx ^ 1] and i < len(closest):
                self.leaders[idx] = closest[i]
                i += 1

        follow = self.leaders[idx % 2]

        match (idx // 2):
            case 0:  # Up
                return [follow[0] + 1, follow[1]]
            case 1:  # Right
                return [follow[0], follow[1] + 1]
            case 2:  # Left
                return [follow[0], follow[1] - 1]
            case 3:  # Down
                return [follow[0] - 1, follow[1]]

    def get_closest_evaders(self, evaders, agent):
        return sorted(evaders, key=lambda x: self.distance(x, agent))
