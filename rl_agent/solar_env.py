import pandas as pd
import numpy as np

# Function to help prep data for class
def load_and_format_solar_df(data_path):
    """
    Converts solar data logged by Arduino into a dataframe whose values can be passed to SolarEnv
    
        * See README for data formatting requirements from Arduino
    
    Args:
        data_path (str): Path to a csv of logged data for an environment
    Returns:
        DataFrame: the values in correct format for generating a numpy value array
    """
    
    data_df = pd.read_csv(data_path)
    data_df = data_df.drop_duplicates(subset=['motor_1_position','motor_2_position'])
    data_df['I_ivp_1'] = data_df['I_ivp_1'].abs() # Make current positive
    data_df['power'] = data_df['I_ivp_1'] * data_df['V_ivp_1']
    return data_df

def convert_solar_df_to_value_array(solar_data_df, degree_discretization=5):
    """
    Convert the solar data df into a reward array to pass to SolarEnv
    
    Args:
        solar_data_df (DataFrame): df returned by load_and_format_solar_df
    Kwargs:
        degree_discretization (int): number of degrees to discretize motor positions by (e.g., 180 // value)
    Returns:
        numpy array: array of environment reward values for SolarEnv
    """
    # Find bounds of motor positions to create max index, zeros array
    max_index = max(solar_data_df['motor_1_position'].max(), solar_data_df['motor_2_position'].max())//degree_discretization
    array_shape = (max_index+1, max_index+1)
    reward_array = np.zeros(array_shape)
    
    # For each data point, populate the array at its index
    for index, row in solar_data_df.iterrows():
        motor_1_index = int(row['motor_1_position'].item()//degree_discretization)
        motor_2_index = int(row['motor_2_position'].item()//degree_discretization)
        position_reward = row['power'].item()
        reward_array[motor_1_index][motor_2_index] = position_reward
    
    return reward_array

# Solar Environment Class
class SolarEnv:
    def __init__(self, value_array, movement_penalty=0.0001, roll_frequency=500):
        """
        Args:
            value_array (numpy): array of square dimensions of values of environment
        Kwargs:
            movement_pentalty (float): penalty for each index of movement by an agent
            roll_frequency (int): frequency of steps with which environment changes (or None for static env)            
        """
        
        # Initialize with passed in value array, penalty per index of movement
        self.reward_array = value_array
        self.movement_penalty = movement_penalty
        self.total_steps = 0
        self.roll_frequency = roll_frequency

    def roll_values(self):
        """
        Changes the environment values by shifting over and up one
        """
        
        self.reward_array = self.reward_array.copy().roll(1, axis=0).roll(1, axis=1)
    
    def env_step(self, action_tuple, last_state_tuple):
        """
        Completes a step of the environment
        
        Args:
            action_tuple (tuple): Index pair to move to in env-based index
            last_state_tuple (tuple): The last state the agent was in, to calculate movement penalty
        Returns:
            reward, next_state_tuple
        """
        
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