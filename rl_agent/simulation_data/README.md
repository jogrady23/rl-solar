# Generate Simulation Data

The agent was developed in a simulated environment that was generated using real data 
from the solar panel. This directory holds a script to generate and visualize simulation data.

While connected to the solar panel, run `create_simulation_data.ipynb` to create and visualize simulation data.

Generated data is written out to `data/`

### Folders
  * `dev/` contains development code to operate the Arduino to generate a simulation data set
    * *You can read about how the Arduino communication works at* `firmware/README`
  * `data/` contains some example logged data sets from sweeps that I ran