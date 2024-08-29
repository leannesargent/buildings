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
#print(economy_list)
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
print(eb_data)

eb_data_long = eb_data.melt(id_vars=['economy', 'product_code', 'item_code'], var_name='year', value_name='PJ')
print(eb_data_long)

# this would need to be a for loop beginning, for each economy, for each item...
economy = '01_AUS'
item = '16_2_residential'
#item = '16_1_commercial_and_public_services'
eb_filtered = eb_data_long[(eb_data_long['economy'] == economy) & (eb_data_long['item_code'] == item) & (eb_data_long['product_code'].isin(fuels_list_plot))]
# eb_filtered = eb_data_long[(eb_data_long['economy'] == economy) & (eb_data_long['product_code'].isin(fuels_list_plot))]
print(eb_filtered)

eb_pivot = eb_filtered.pivot(index='year', columns='product_code', values='PJ')
print(eb_pivot)
#eb_pivot.to_csv('pivot.csv', index=False)

# Ensure the Year index is integer
eb_pivot.index = eb_pivot.index.astype(int)


# plot stacked area
eb_pivot.plot(kind='area', stacked=True)

plt.title(f'Stacked Area Plot for {economy} - {item}')
plt.xlabel('Year')
plt.ylabel('PJ')

# Set x-ticks to be the unique years in the data
plt.xticks(ticks=eb_pivot.index, labels=eb_pivot.index)
plt.xticks(rotation=90)

# Show the plot
plt.show()





