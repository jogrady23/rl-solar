# RL Agent

This portion of the repository contains all agent-related source code.

## Running the Agent

For simulation, run `rl_agent.ipynb`, which contains the agent, experiment runtimes, hyperparameter study system, etc.

To actually connect a Python agent (or simply Python control) to the Arduino, a suite of useful functions exists 
in `arduino_interface.py`

## Generating Simulation Data with the Solar Panel

I generate simulation data using the actual solar panel, and code for doing so can be found at 
`simulation_data/dev/collect_simulation_data.ipynb`. This lets you place the solar panel in some real environment, 
sweep the entire space of motor positions, and then log the data to pass into the `rl_agent.ipynb` file above.

## Folders

The top level of this folder holds all of the final files needed to run. 
Descriptions of subfolders are below:

* `dev/` holds agent development, Arduino debugging
  * `initial_bringup/` is the first effort at stringing together the agent and env
  * `initial_q_learning_agent/` is the first attempt at a Q-learning agent
  * `improved_q_learning_agent/` is a research effort to improve Q-learning
    * This was ultimately discarded as I realized there were more fundemental issues with problem formulation
    * You can read more about Q-learning and its issue for the problem here: https://www.jackogrady.me/reinforcement-learning-solar/rl-agent-q-learning
  * `softmax_actor_critic/` contains agents that lead to the final algorithm
    * You can read more about Softmax Actor-Critic agents here: https://www.jackogrady.me/reinforcement-learning-solar/rl-agent-softmax-actor-critic

* `simulation_data/` holds both simulation data and scripts for generating new simulation data when connected to the panel
  * `dev/` contains code to actually operate the Arduino to generate a simulation data set
    * *You can read about how the Arduino communication works at* `firmware/README`
  * `data/` contains some example logged data sets from sweeps that I ran

