from .AbstractPolicy import AbstractPolicy
import numpy as np


class RandomPolicy(AbstractPolicy):
    def __call__(self, observation, agent):
        return self.env.action_space(agent).sample()
