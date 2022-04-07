import pandas as pd
import numpy as np


class TestEnv:
    def __init__(self, value_array, movement_penalty=0):
        self.reward_array = value_array
        self.movement_penalty = movement_penalty

    def env_step(self, action_tuple, last_state_tuple):
        # Return reward, next state
        reward = self.reward_array[action_tuple]
        cost = self.movement_penalty * (abs(last_state_tuple[0] - action_tuple[0]) +
                                   abs(last_state_tuple[1] - action_tuple[1]))
        return reward - cost, action_tuple

    # For debugging
    def get_reward_array(self):
        return self.reward_array

    def get_env_shape(self):
        return self.reward_array.shape
