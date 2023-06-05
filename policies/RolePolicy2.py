from .GreedyPolicy import GreedyPolicy


class RolePolicy2(GreedyPolicy):
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
        target_positions = [self.get_adjacencies(t) for t in target_evaders]

        l_id = self.get_id((agent_name)) // 4
        pursuer_names_patrol = sorted(pursuers.keys())[4*l_id:4*l_id+4]


        target_positions_patrol = self.get_target_positions_patrol(target_positions, l_id)
        for pursuer in pursuer_names_patrol:
            pursuer_pos = pursuers[pursuer]
            chosen = self.get_closest(target_positions_patrol, pursuer_pos)
            target_positions_patrol.remove(chosen)
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
                if evader not in targets:
                    targets.append(evader)
                    break

        return targets

    # for each target evader, calculate the coordinates of its adjacencies
    # each of these coordinates will be the destination of exactly one pursuer
    def get_adjacencies(self, t):
        adjacencies = []
        adjacencies.append([t[0]-1, t[1]])
        adjacencies.append([t[0]  , t[1]-1])
        adjacencies.append([t[0]+1, t[1]])
        adjacencies.append([t[0]  , t[1]+1])

        return adjacencies

    def get_target_positions_patrol(self, target_positions, leader_id):
        n_targets = len(target_positions)
        return target_positions[leader_id % n_targets]


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
    def get_id(self, agent):
        return int(agent.split("_")[1])

    def get_closest_evaders(self, evaders, agent):
        return sorted(evaders, key=lambda x: self.distance(x, agent))
