import pandas as pd
import numpy as np

# Load in logged solar data for the experiment
def load_and_prep_data(data_path):
    raw_df = pd.read_csv(data_path)
    data_df = raw_df.copy()
    # Make current positive
    data_df = data_df.drop_duplicates(subset=['motor_1_position','motor_2_position'])
    data_df['I_ivp_1'] = data_df['I_ivp_1'].abs()
    data_df['power'] = data_df['I_ivp_1'] * data_df['V_ivp_1']
    return data_df

class SolarEnv:
    def __init__(self, value_array, movement_penalty=0, roll_frequency=500):
        # Initialize with passed in value array, penalty per index of movement
        self.reward_array = value_array
        self.movement_penalty = movement_penalty
        self.total_steps = 0
        self.roll_frequency = roll_frequency

    def roll_values(self):
        self.reward_array = self.reward_array.copy().roll(1, axis=0).roll(1, axis=1)
    
    def env_step(self, action_tuple, last_state_tuple):
        # Reward is power received
        reward = self.reward_array[action_tuple]
        # Add a cost from moving motors to new position
        cost = self.movement_penalty * (abs(last_state_tuple[0] - action_tuple[0]) +
                                   abs(last_state_tuple[1] - action_tuple[1]))
        # Increment step count, do roll of values if specified for env
        self.total_steps += 1
        if self.roll_frequency is not None:
            if self.total_steps // self.roll_frequency == 0:
                self.roll_values()

        return reward - cost, action_tuple

    # Access Functions
    def get_reward_array(self):
        return self.reward_array

    def get_env_shape(self):
        return self.reward_array.shape