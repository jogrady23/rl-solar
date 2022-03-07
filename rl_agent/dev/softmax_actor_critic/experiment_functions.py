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

def calculate_value_error(agent_array, env_array):
    return np.sqrt((agent_array - env_array) ** 2).mean()


def progress_dict_to_df(progress_dict):
    dict_list = []
    for x in progress_dict.keys():
        temp_dict = progress_dict[x]
        temp_dict['step'] = x
        dict_list.append(temp_dict)
    return pd.DataFrame(dict_list)


def run_agent_experiment(exp_agent, exp_env, steps, interval):
    progress_dict = {}
    exp_agent.agent_start()
    progress_dict['0'] = {
        'state_value': exp_agent.get_critic_array(),
        'action_prob': exp_agent.get_actor_array(),
        'rolling_power': exp_agent.get_agent_rolling_power(),
        'state_visits': exp_agent.get_state_visits(),
        'total_energy': exp_agent.get_agent_energy()
    }
    for i in tqdm(range(1, steps + 1)):
        # for i in range(1, steps + 1): # no TQDM option
        exp_agent.agent_step()
        if i % interval == 0:
            progress_dict[str(i)] = {
                'state_value': exp_agent.get_critic_array(),
                'action_prob': exp_agent.get_actor_array(),
                'rolling_power': exp_agent.get_agent_rolling_power(),
                'state_visits': exp_agent.get_state_visits(),
                'total_energy': exp_agent.get_agent_energy()
            }
    progress_df = progress_dict_to_df(progress_dict)
    return exp_agent, progress_dict, progress_df


def make_subplots_plot(df, x, subplot_group_list, height=400, width=400, plot_title=''):
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

def plot_array_evolution(exp_progress_dict, exp_interval, field, width_plot, height_plot, zmax=None, zmin=None):
    matrix_list = [exp_progress_dict[x][field] for x in exp_progress_dict.keys()]
    fig = go.Figure(
        data=[go.Heatmap(z=matrix_list[0], zmax=zmax, zmin=zmin)],layout=go.Layout(
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
            frames=[go.Frame(data=[go.Heatmap(z=matrix_list[i])],
                             layout=go.Layout(title_text=f"Step {i * exp_interval}")) for i in range(1, len(matrix_list))]
    )
    fig.update_yaxes(autorange="reversed")
    fig.update_layout({
        'height': height_plot,
        'width': width_plot}
    )

    fig.show()


def plot_rolling_power(progress_df, exp_env, height, width):
    max_output = exp_env.get_reward_array().max()
    progress_df['env_max'] = max_output
    progress_df['optimal_energy'] = progress_df['step'].astype(float) * max_output
    progress_df['difference'] = (progress_df['rolling_power'] - progress_df['env_max']) / progress_df['env_max']
    make_subplots_plot(df=progress_df, x='step', subplot_group_list=[
        {
            'title': 'Reward Comparison (Agent vs Max)',
            'columns': ['env_max', 'rolling_power']
        },
        {
            'title': 'Energy Comparison (Agent vs Max)',
            'columns': ['total_energy', 'optimal_energy']
        }
    ], height=height, width=width
                       )
