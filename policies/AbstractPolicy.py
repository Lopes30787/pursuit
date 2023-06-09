import abc


class AbstractPolicy:
    def __init__(self, env):
        self.env = env

    @abc.abstractmethod
    def __call__(self):
        raise NotImplementedError()

    def get_id(self, agent):
        return int(agent.split("_")[1])