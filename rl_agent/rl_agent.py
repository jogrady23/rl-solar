import serial
import time
import random
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import tqdm
from tqdm import tqdm

from common_functions import *

# Declare random seed
RANDOM_SEED = 1

# Set default constants for problem
ARRAY_DIMENSION_TUPLE = (37,37)
MOTOR_ANGLE_POWER_DRAW = 0.0001


# Policy
def softmax_prob(actor_av_array, temperature=1):
    """
    Uses a softmax policy to select a value from an array
    
    Args:
        actor_av_array (numpy array): the array of values to select from
    Kwargs:
        temperature (float): temperature factor for softmax
    Returns:
        numpy array: array of softmax probabilities
    """
    # Divide all values by temperature
    temperature_array = actor_av_array/temperature
    
    # Find max state value
    max_value = np.max(temperature_array)
    
    # Generate the numerator for each element by subtracting max value and exponentiating
    numerator_array = temperature_array - max_value
    numerator_array = np.exp(numerator_array)

    # Get the denominator by summing all values in the numerator
    denominator_array = np.sum(numerator_array)
    
    
    # Calculate the softmax value array and return to agent
    softmax_array = numerator_array / denominator_array
    
    return softmax_array

class SoftmaxAgent:
    def __init__(self, actor_step_size, critic_step_size, avg_reward_step_size, temperature_value, env_shape, reward_rolling_avg_window, 
                 random_seed=RANDOM_SEED, actor_init_value=None, critic_init_value=None):
        # Set step sizes
        self.actor_step_size = actor_step_size
        self.critic_step_size = critic_step_size
        self.avg_reward_step_size = avg_reward_step_size
        self.temperature = temperature_value
        
        # Set up memory for the actor and critic
        self.env_shape = env_shape
        max_index_2d = self.env_shape[0] - 1
        max_index_1d = convert_2d_index_to_1d_index((max_index_2d, max_index_2d), dimensions=self.env_shape)
        self.agent_shape = (max_index_1d + 1, max_index_1d + 1)
        
        # Set init values of actor and critic
        # Actor
        if actor_init_value:
            self.actor_array = np.full(self.agent_shape, actor_init_value)
        else:
            self.actor_array = np.zeros(self.agent_shape)
        # Critic
        if critic_init_value:
            self.critic_array = np.full(self.agent_shape, critic_init_value)
        else:
            self.critic_array = np.zeros(self.agent_shape)
        
        # Create the actions and feature vectors
        self.actions_vector = np.array(range(0, max_index_1d + 1))
        self.base_feature_vector = np.zeros(max_index_1d + 1)
        
        # Set up fields for agent steps -- all agent internal functions are 1d index
        self.random_generator = np.random.RandomState(random_seed) 
        self.last_state = None
        self.last_action = None
        self.state = None
        self.last_reward = None
        self.avg_reward = 0
        self.step_softmax_prob = None
    
        # Set up tracking metric items
        self.state_visits = np.zeros(self.env_shape) # track in 2d to better map to env map
        self.total_reward = 0
        self.rolling_reward = 0
        self.rolling_window = reward_rolling_avg_window
        self.transition_dict = None
        self.last_delta = 0
    
    # Agent Operation
    # =============================================
    def agent_start(self):
        # Initialize the agent
        self.avg_reward = 0
        self.last_state = self.agent_shape[0]//2  # Set to the middle state for init
        self.last_action = self.last_state
        self.last_reward = 0
        
        # For tracking
        self.state_visits[convert_1d_index_to_2d_index(self.last_state, dimensions=self.env_shape)] += 1
    
    
    def agent_policy(self):
        # Compute the softmax prob for actions in given state
        softmax_prob_array = softmax_prob(self.actor_array[self.last_state], self.temperature)
        
        # Overlay the softmax probs onto actions vector
        chosen_action = self.random_generator.choice(self.actions_vector, p=softmax_prob_array)
        
        # save softmax_prob as it will be useful later when updating the Actor
        self.step_softmax_prob = softmax_prob_array.copy()
        self.last_action = chosen_action
        
        # Return the 1d index of action
        return chosen_action
        
    
    def agent_step(self, reward, next_state):
        # Compute delta
        delta = reward - self.avg_reward + np.mean(self.critic_array[next_state]) - np.mean(self.critic_array[self.last_state])
        
        # Update avg reward
        self.avg_reward += self.avg_reward_step_size * delta
        
        # Update critic weights
        self.critic_array[self.last_state][self.last_action] += self.critic_step_size * delta
        
        # Update actor weights
        feature_vector = self.base_feature_vector.copy() # copy the zeros vector
        feature_vector[self.last_action] = 1 # set last action to one
        self.actor_array[self.last_state] += self.actor_step_size * delta * (feature_vector - self.step_softmax_prob)
        
        # Update last state, etc
        self.last_state = next_state
        
        # For tracking
        self.total_reward += reward
        self.rolling_reward = rolling_avg_calc(reward, self.rolling_reward, self.rolling_window)
        self.state_visits[convert_1d_index_to_2d_index(self.last_state, self.env_shape)] += 1
        self.last_delta = delta
    
    # Tracking
    # =============================================
    
    def get_critic_array(self):
        return self.critic_array.copy()
    
    def get_actor_array(self):
        return self.actor_array.copy()
    
    def set_actor_array(self, array):
        self.actor_array = array
        
    def get_actions_vector(self):
        return self.actions_vector
    
    def get_agent_avg_reward(self):
        return self.avg_reward
    
    def get_agent_last_delta(self):
        return self.last_delta
    
    def get_agent_last_state(self):
        return self.last_state
    
    def get_base_feature_vector(self):
        return self.base_feature_vector
    
    def get_agent_total_reward(self):
        return self.total_reward
    
    def get_agent_rolling_reward(self):
        return self.rolling_reward
    
    def get_state_visits(self):
        return self.state_visits.copy()