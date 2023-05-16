import numpy as np
class State:
    def __init__(self, obs, act):
        self.observation = obs
        self.action = act

    def __eq__(self, other):
        return self.action == other.action and np.array_equal(np.array(self.observation), np.array(other.observation))

    def __lt__(self, other):
        return False
