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


def heatmap(array, show_values=False, width=600, height=600):
    """
    Plot a heatmap of an array
    
    Args:
        array (Numpy): A numpy array of values to plot
    Kwargs:
        show_values (bool): True to display values in each cell, False to hide
        width (int): Width of the plot
        height (int): Height of the plot
    Returns:
        None
    """
    return px.imshow(array, text_auto=show_values, width=width, height=height)
            


def load_and_visualize_data_adjusted(data_path):
    """
    Load in collected data and create a 3d heatmap to visualize
    
    Args:
        data_path (str): Path to the data collected
    Returns:
        None
    """
    raw_df = pd.read_csv(data_path)
    data_df = raw_df.copy()
    
    # Make current positive
    data_df['I_ivp_1'] = data_df['I_ivp_1'].abs()
    data_df['power'] = data_df['I_ivp_1'] * data_df['V_ivp_1']
    
    # Generate data for visualization
    viz_df = data_df[['power', 'motor_1_position', 'motor_2_position']]
    viz_df = viz_df.drop_duplicates(subset=['motor_1_position', 'motor_2_position'])
    viz_df = viz_df.sort_values(by=['motor_1_position','motor_2_position'])
    fig = px.scatter_3d(viz_df, x='motor_1_position', y='motor_2_position', z='power',
                      color='power', opacity=1, width=600, height=600)#, #size_max=10, # size='power',
                   #range_z=[0,0.015], range_color=[0,0.015])
    fig.update_traces(marker={'size': 5})
    fig.show()


def subplots(df, x, subplot_group_list, height=400, width=400, plot_title=''):
    """
    Creates subplots with plotly
    
    Args:
        df (DataFrame): The dataframe containing data to plot
        x (str): The name of the column to use as common x axis
        subplot_group_list (list): A list of dicts containing keys 'title' and 'columns'
    Kwargs:
        height (int): Height of the plot
        width (int): Width of the plot
        plot_title (str): Title of the entire plot
    Returns:
        None
    """
    fig = make_subplots(rows=len(subplot_group_list), cols=1, shared_xaxes=True,
                        subplot_titles=[x['title'] for x in subplot_group_list])

    for i in range(len(subplot_group_list)):
        row = i + 1
        title = subplot_group_list[i]['title']
        for column_name in subplot_group_list[i]['columns']:
            fig.append_trace(go.Scatter(
                x=df[x],
                y=df[column_name], name=column_name
            ), row=row, col=1)

    fig.update_layout(height=height, width=width, title_text=plot_title)
    fig.show()

    
def plot_array_evolution(array_list, step_interval, width=400, height=400, zmax=None, zmin=None):
    """
    Plots an array over time to see changes in values visually
    
    Args:
        array_list (list): A list of the arrays to plot (sequential order)
        step_interval (int): Frequency of logging during the experiment
    Kwargs:
        width (int): Width of the plot
        height (int): Height of the plot
        zmax (float): Max value for scale, or None
        zmin (float): Min value for scale, or None
    Returns:
        None
    """
    fig = go.Figure(
        data=[go.Heatmap(z=array_list[0], zmax=zmax, zmin=zmin)],layout=go.Layout(
                title="Step 0",
                updatemenus=[dict(
                    type="buttons",
                    buttons=[dict(label="Play",
                                  method="animate",
                                  args=[None]),
                            dict(label="Pause",
                                 method="animate",
                                 args=[None,
                                       {"frame": {"duration": 0, "redraw": False},
                                        "mode": "immediate",
                                        "transition": {"duration": 0}}],
                                 )])]
            ),
            frames=[go.Frame(data=[go.Heatmap(z=array_list[i])],
                             layout=go.Layout(title_text=f"Step {i * step_interval}")) for i in range(1,len(array_list))]
    )
    fig.update_yaxes(autorange="reversed")
    fig.update_layout({
        'height': height,
        'width': width}
    )

    return fig


def plot_rolling_power(progress_df, exp_env, height=600, width=800):
    """
    Creates a visualization to assess agent performance
    
    Args:
        progress_df (DataFrame): The tracking df generated during an experiment
        exp_env (SolarEnv): The environment used in the experiment
    Kwargs:
        width (int): Width of the plot
        height (int): Height of the plot
    Returns:
        None
    """
    max_output = exp_env.get_reward_array().max()
    progress_df['env_max'] = max_output
    progress_df['optimal_energy'] = progress_df['step'].astype(float) * max_output
    progress_df['difference'] = (progress_df['rolling_power'] - progress_df['env_max']) / progress_df['env_max']
    subplots(df=progress_df, x='step', subplot_group_list=[
        {
            'title': 'Reward Comparison (Agent vs Max)',
            'columns': ['env_max', 'rolling_power']
        },
        {
            'title': 'Energy Comparison (Agent vs Max)',
            'columns': ['total_energy', 'optimal_energy']
        },
        {
            'title': 'Agent Learning',
            'columns': ['delta']
        },
    ], height=height, width=width, plot_title='<b>Agent Assessment</b>'
                       )
    
def plot_hyperparameter_study(study_df, exp_env, height=600, width=800):
    """
    Creates a visualization to assess agent performance
    
    Args:
        progress_df (DataFrame): The tracking df generated during an experiment
        exp_env (SolarEnv): The environment used in the experiment
    Kwargs:
        width (int): Width of the plot
        height (int): Height of the plot
    Returns:
        None
    """
    max_output = exp_env.get_reward_array().max()
    progress_df['env_max'] = max_output
    progress_df['optimal_energy'] = progress_df['step'].astype(float) * max_output
    progress_df['difference'] = (progress_df['rolling_power'] - progress_df['env_max']) / progress_df['env_max']
    subplots(df=progress_df, x='step', subplot_group_list=[
        {
            'title': 'Reward Comparison (Agent vs Max)',
            'columns': ['env_max', 'rolling_power']
        },
        {
            'title': 'Energy Comparison (Agent vs Max)',
            'columns': ['total_energy', 'optimal_energy']
        },
        {
            'title': 'Agent Learning',
            'columns': ['delta']
        },
    ], height=height, width=width, plot_title='<b>Agent Assessment</b>'
                       )
