from .GreedyPolicy import GreedyPolicy


class RolePolicyBad(GreedyPolicy):
    def __init__(self, env):
        super().__init__(env)

    def __call__(self, observation, agent_name):
        evaders = observation[0]
        pursuers = observation[1]
        agent_pos = pursuers[agent_name]

        selected_pos = self.get_destination(evaders, pursuers, agent_name)
        return self.get_move(selected_pos, agent_pos)


    # calculate where this agent should be headed
    def get_destination(self, evaders, pursuers, agent_name):
        leaders = self.get_leaders(pursuers)
        target_evaders = self.find_target_evaders(evaders, pursuers, leaders)
        target_positions = self.get_adjacencies(target_evaders)

        pursuer_names = sorted(pursuers.keys())
        for pursuer in pursuer_names:
            pursuer_pos = pursuers[pursuer]

            if len(target_positions) == 0:
                return pursuer_pos

            chosen = self.get_closest(target_positions, pursuer_pos)
            target_positions.remove(chosen)
            if pursuer == agent_name:
                return chosen


    # chooses leaders deterministically (one for each four pursuers)
    # leaders will be used to choose target evaders
    def get_leaders(self, pursuers):
        return sorted(pursuers.keys())[::4]

    # finds the evaders closest to the leaders (1 per leader) that arent against a wall
    # these will be our targets
    def find_target_evaders(self, evaders, pursuers, leaders):
        targets = []

        for leader in leaders:
            closest_evaders = self.get_closest_evaders(evaders, pursuers[leader])

            for evader in closest_evaders:
                if self.is_against_wall(evader):
                    continue
                if evader not in targets:
                    targets.append(evader)
                    break

        return targets

    # for each target evader, calculate the coordinates of its adjacencies
    # each of these coordinates will be the destination of exactly one pursuer
    def get_adjacencies(self, targets):
        adjacencies = []

        for t in targets:
            adjacencies.append([t[0]-1, t[1]])
            adjacencies.append([t[0]  , t[1]-1])
            adjacencies.append([t[0]+1, t[1]])
            adjacencies.append([t[0]  , t[1]+1])

        return adjacencies

    # verifies if a given coordinate is against a wall or in a corner
    def is_against_wall(self, pos):
        limit = 15

        if pos[0] == 0 or pos[1] == 0:
            return True

        if pos[0] == limit or pos[1] == limit:
            return True

        return False

    def get_target_positions_patrol(self, target_positions, leader_id):
        if leader_id >= len(target_positions):
            return target_positions[:4]
        return target_positions[leader_id:leader_id+4]


    """
    def get_destination():
        1. calculate leaders
        2. find evader closest to each leader (all distinct)
        3. calculate list of each adjacent position to each evader (total of 8 positions*)
        4. for each pursuer:
        4.1. assign pursuer to closest adjacent position (from 3.)
        4.2. make chosen position unavailable
        5. return position assigned to self


        * unless one of the evaders is against a wall (in this case what happens?)
    """

    def get_closest_evaders(self, evaders, agent):
        return sorted(evaders, key=lambda x: self.distance(x, agent))
