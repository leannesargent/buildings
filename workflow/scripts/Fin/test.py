import pandas as pd
import numpy as np
import os
import plotly.express as px
from projection_adjust import fuel_intensity_traj

# Minimal test
fuel_intensity_traj(economy='01_AUS', fuels='01_coal', proj_start_year=2022, 
                    shape='peak', magnitude=1.3, apex_mag=1.1, apex_loc=50)
