import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.formula.api import ols
from sklearn.model_selection import train_test_split

import os
import re

wanted_wd = 'buildings'

os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# Some set up
# Economies (including larger regions)
variable_path = './data/config/'
economy_list = pd.read_csv(variable_path + 'APEC_economies.csv').iloc[:, 0]
# print(economy_list)
fuels_list = pd.read_csv(variable_path + 'EGEDA_fuels.csv').iloc[:, 0]
#print(fuels_list)
fuels_list_plot = fuels_list[fuels_list != '19_total']
#print(fuels_list_plot)
subfuels_list = pd.read_csv(variable_path + 'EGEDA_subfuels.csv').iloc[:, 0]
#print(subfuels_list)

# Import entire EB EGEDA file - all subsectors
eb_data_all = pd.read_csv("./data/EGEDA/EGEDA_2020_created_14112022.csv")

# Filter EGEDA data to select only RES and SRV subsectors
# DF columns "economy", "product_code" (subfuel), "item_code" (subsector), 1980-2021
eb_data = eb_data_all[
    (eb_data_all['item_code'] == '16_1_commercial_and_public_services') |
    (eb_data_all['item_code'] == '16_2_residential')]
eb_data

# eb_filtered = eb_data[(eb_data['economy'] == '01_AUS')]
# eb_filtered
# eb_result_filtered = eb_filtered.groupby(['economy', 'item_code']).sum().reset_index()
eb_result = eb_data.groupby(['economy', 'item_code']).sum().reset_index()
eb_result

eb_final = eb_result.drop(columns=['product_code'])
# eb_final
eb_melted = eb_final.melt(id_vars=['economy', 'item_code'], var_name='year', value_name='value')
# eb_melted

# DF WITH COLUMNS FOR SRV AND RES, SUMMED IN EACH YEAR. FOR PROJECTIONS
eb_pivoted = eb_melted.pivot(index=['economy', 'year'], columns='item_code', values='value').reset_index()
# eb_pivoted

# Plotting
years = eb_pivoted['year'].unique()  # Assuming 'year' is a column in your DataFrame

for economy in economy_list:
    # Filter the data for the current economy
    economy_data = eb_pivoted[eb_pivoted['economy'] == economy]
    
    # Extract the values for SRV and RES
    srv_values = economy_data['16_1_commercial_and_public_services'].values
    res_values = economy_data['16_2_residential'].values
    
    # Create the stacked area plot
    plt.figure(figsize=(10, 6))
    plt.stackplot(years, srv_values, res_values, labels=['SRV', 'RES'], alpha=0.5)
    plt.title(f'Stacked Area Plot for {economy}')
    plt.xlabel('Year')
    plt.ylabel('Value')
    plt.legend(loc='upper left')
    plt.xticks(rotation=90)
    plt.show()

