# Normal imports
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

# Module imports
import rl_agent
from rl_agent import SoftmaxAgent

import solar_env
from solar_env import SolarEnv

from common_functions import *


# Run individual step of experiment
def run_experiment_step(env:SolarEnv, agent:SoftmaxAgent, step):
    """
    Carry out one step of interaction between agent and environment
    
    Args:
        env (SolarEnv): the environment being used in the experiment
        agent (SoftmaxAgent): the agent being used in the experiment
        step (int): the step number of the experiment
    Returns:
        None
    """
    
    action = agent.agent_policy()
    reward, next_state_tuple = env.env_step(convert_1d_index_to_2d_index(action, env.get_env_shape()), 
                                            convert_1d_index_to_2d_index(agent.get_agent_last_state(), env.get_env_shape()))
    agent.agent_step(reward, convert_2d_index_to_1d_index(next_state_tuple, env.get_env_shape()))
    
    
# Creates a dict for metrics at a single step of an experiment
def create_tracking_dict(step, env:SolarEnv, agent:SoftmaxAgent):
    """
    Generate a tracking dict for a given step of an experiment
    
    Args:
        step (int): the step number of an experiment
        env (SolarEnv): the environment of an experiment
        agent (SoftmaxAgent): the agent of an experiment
    Returns:
        dict: a tracking dict with keys seen in function below
    """
    
    tracking_dict = {
        'step': step,
        'delta': agent.get_agent_last_delta(),
        'state_value': agent.get_critic_array(),
        'action_prob': agent.get_actor_array(),
        'rolling_power': agent.get_agent_rolling_reward(),
        'state_visits': agent.get_state_visits(),
        'total_energy': agent.get_agent_total_reward(),
        'env_rewards': env.get_reward_array()
    }
    return tracking_dict


# Runs an experiment end to end
def run_agent_experiment(environment:SolarEnv, steps, seed, actor_step_size, critic_step_size, 
                         avg_reward_step_size, temperature, rolling_steps_measurement=10, 
                         logging_interval=1000, hide_progress_bar=False):
    """
    Run an end-to-end experiment with the agent and determine the total reward during the experiment
    
    Args:
        environment (SolarEnv): The environment class for the agent to interact with
        steps (int): The number of steps to run the experiment for
        seed (int): The random seed number to use for the agent
        actor_step_size (float): Step-size parameter for actor in agent
        critic_step_size (float): Step-size parameter for critic in agent
        avg_reward_step_size (float): Step-size parameter for avg reward in agent
        temperature (float): Temperature parameter for actor policy
    Kwargs:
        rolling_steps_measurement (int): For tracking, the rolling avg steps for calculating running power from agent
        logging_interval (int): Frequency of steps to log metrics from experiment, None to avoid logging
        hide_progress_bar (bool): Set to True to hide the tqdm bar
    Returns:
        float, DataFrame: the total reward the agent achieved in experiment, the tracking df of results in steps
    """
    
    # Create agent with properties
    experiment_agent = SoftmaxAgent(actor_step_size=actor_step_size, critic_step_size=critic_step_size,
                                avg_reward_step_size=avg_reward_step_size,
                                temperature_value=temperature, env_shape=environment.get_env_shape(), 
                                reward_rolling_avg_window=rolling_steps_measurement, random_seed=seed)
    # Initialize Agent
    experiment_agent.agent_start()
    
    # Initialize a tradcking dict
    tracking_dict_list = []
    tracking_dict_list.append(create_tracking_dict(step=0, env=environment, agent=experiment_agent))
    
    # Only do one conditional logging check to improve runtime
    if logging_interval is not None:
        # Run specified number of steps
        for i in tqdm(range(1, steps + 1), disable=hide_progress_bar):
            run_experiment_step(environment, experiment_agent, step=i)
            if i % logging_interval == 0:
                tracking_dict_list.append(create_tracking_dict(step=i, env=environment, agent=experiment_agent))
        tracking_df = pd.DataFrame(tracking_dict_list)
    
    # If no logging, just run the experiment straight
    else:
        for i in tqdm(range(1, steps + 1), disable=hide_progress_bar):
            run_experiment_step(environment, experiment_agent, step=i)
        tracking_df = pd.DataFrame() # empty df
    
    # Return total reward from experiment
    if not tracking_df.empty:
        return experiment_agent.get_agent_total_reward(), tracking_df
    else:
        return experiment_agent.get_agent_total_reward()