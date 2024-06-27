import pandas as pd

import os
import re

wanted_wd = 'buildings'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

#Eighth results contain only buildings values, for future projection
buildings_8th_projected = pd.read_excel('./data/test_data/output8.xlsx')

#Ninth results contain values for all sectors, read in total csv and subset in the next lines
buildings_9th_historical = pd.read_excel('./data/test_data/output9.xlsx')



#can use these lines to check the dfs
buildings_8th_projected
buildings_9th_historical
#buildings_9th_historical.to_excel('./data/excel_checks/Buildings_9th_historical_sub2sector_filtered.xlsx', index=False)

#Read in mapping file
mapping_file = pd.read_excel('./data/buildings_mapping_scenario.xlsx')
mapping_file

# Convert mapping_file into a dictionary
mapping_dictionary = mapping_file.set_index(['Scenario_8th', '8th_fuels']).apply(list, axis=1).to_dict()
mapping_dictionary

buildings_8th_projected_map = buildings_8th_projected.copy()
buildings_8th_projected_map

buildings_8th_projected_map[['scenarios', 'sub1sectors', 'sub2sectors', 'fuels', 'subfuels']] = buildings_8th_projected[['SCENARIO', 'FUEL']].apply(lambda row: tuple(row), axis=1).map(mapping_dictionary).apply(pd.Series)
buildings_8th_projected_map

buildings_9th_historical_trunc = buildings_9th_historical.iloc[:, 0:11].copy()
buildings_9th_historical_trunc



economies = ('01_AUS', '03_CDA')

output_directory = "./results/test_results"

combined_merge = []

def calculate_difference(row):
    return row[2017] - row['2017_8th']

for economy in economies:
    subset_9th_unique_economy = buildings_9th_historical_trunc[buildings_9th_historical_trunc['economy'] == economy]
    subset_9th_unique_economy
    subset_8th_unique_economy_v1 = buildings_8th_projected_map[buildings_8th_projected_map['REGION'] == economy]
    subset_8th_unique_economy = subset_8th_unique_economy_v1.rename(columns={2017: '2017_8th'})
    subset_8th_unique_economy
    columns_to_merge = subset_8th_unique_economy.loc[:, '2017_8th':'subfuels']
    #merged_economy = subset_9th_unique_economy.merge(subset_8th_unique_economy, on=['scenarios', 'sub1sectors', 'sub2sectors', 'fuels', 'subfuels'], how='left')
    merged_economy = subset_9th_unique_economy.merge(columns_to_merge, on=['scenarios', 'sub1sectors', 'sub2sectors', 'fuels', 'subfuels'], how='left')
    merged_economy
 
    merged_economy_calc = merged_economy.copy()
    merged_economy_calc['2017_diff'] = merged_economy.apply(calculate_difference, axis=1)
    merged_economy_calc

    columns_to_update = merged_economy_calc.loc[:, 2017:2021]
    columns_to_update

    merged_economy_calc_add = merged_economy_calc.copy()

    for index, row in merged_economy_calc_add.iterrows():
        diff = row['2017_diff']

        for col in columns_to_update:
            merged_economy_calc_add.at[index, col] += diff
            merged_economy_calc_add
   
   

   
