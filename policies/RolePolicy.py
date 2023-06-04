from .GreedyPolicy import GreedyPolicy


class RolePolicy(GreedyPolicy):
    def __init__(self, env):
        super().__init__(env)

    def __call__(self, observation, agent_name):
        evaders = observation[0]
        pursuers = observation[1]
        agent_pos = pursuers[agent]

        selected_pos = self.get_destination(evaders, pursuers, agent_name)
        return self.get_move(selected_pos, agent_pos)


    # calculate where this agent should be headed
    def get_destination(evaders, pursuers, agent_name):
        leaders = get_leaders(pursuers)
        target_evaders = find_target_evaders(evaders, pursuers, leaders)
        target_positions = get_adjacencies(target_evaders)

        pursuer_names = pursuers.keys().sorted()
        for pursuer in pursuer_names:
            pursuer_pos = pursuers[pursuer]
            chosen = get_closest(target_positions, pursuer_pos)
            target_positions.remove(chosen)
            if pursuer == agent_name:
                return chosen


    # chooses leaders deterministically (one for each four pursuers)
    # leaders will be used to choose target evaders
    def get_leaders(pursuers):
        return pursuers.keys().sorted()[::4]

    # finds the evaders closest to the leaders (1 per leader)
    # these will be our targets
    def find_target_evaders(evaders, pursuers, leaders):
        targets = []

        for leader in leaders:
            closest_evaders = get_closest_evaders(evaders, pursuers[leader])

            for evader in closest_evaders:
                if evader not in targets:
                    target.append(evader)
                    break

        return targets

    # for each target evader, calculate the coordinates of its adjacencies
    # each of these coordinates will be the destination of exactly one pursuer
    def get_adjacencies(targets):
        # TODO
        # what if the pursuer is against the wall??
        pass


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
