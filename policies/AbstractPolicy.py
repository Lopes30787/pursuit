import abc


class AbstractPolicy(abc.ABC):
    def __init__(self, env):
        self.env = env

    @abc.abstractmethod
    def __call__(self):
        raise NotImplementedError()
