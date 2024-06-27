import pandas as pd

import os
import re

wanted_wd = 'buildings'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

eighth_results = pd.read_excel('./data/test_data/output8.xlsx')
eighth_results
ninth_historical_values = pd.read_excel('./data/test_data/output9.xlsx')
ninth_historical_values

mapping_file = pd.read_excel('./data/buildings_mapping_scenario.xlsx')
mapping_file

mapping_dictionary = mapping_file.set_index(['Scenario_8th', '8th_fuels']).apply(list, axis=1).to_dict()
mapping_dictionary

eighth_results_map = eighth_results.copy()
eighth_results_map


#adding the four columns to the 8th and doing the match based on the FUEL column of the 8th, which is mapped to the four columns through the dictionary
eighth_results_map[['scenario', 'sub1sectors', 'sub2sectors', 'fuels', 'subfuels']] = eighth_results[['SCENARIO', 'FUEL']].apply(lambda row: tuple(row), axis=1).map(mapping_dictionary).apply(pd.Series)
eighth_results_map

# columns_to_merge2 = eighth_results_map.loc[:, 2017:'subfuels']
# columns_to_merge2


ninth_trunc = ninth_historical_values.iloc[:, 0:11].copy()
ninth_trunc


# merged_results_full = pd.DataFrame()

# economies = ('01_AUS', '02_BD', '03_CDA', '04_CHL', '05_PRC', '06_HKC', '07_INA', '08_JPN', '09_ROK', '10_MAS', '11_MEX', '12_NZ', '13_PNG', '14_PE', '15_PHL', '16_RUS', '17_SGP', '18_CT', '19_THA', '20_USA', '21_VN')

# for economy in economies:
#     print (economy)

economies = ('01_AUS', '03_CDA')

# Define the directory where you want to save the Excel files
output_directory = "./results/test_results"

for economy in economies:
    subset_9th_unique_economy = ninth_trunc[ninth_trunc['economy'] == economy]
    subset_8th_unique_economy = eighth_results_map[eighth_results_map['REGION'] == economy]
    merged_economy = subset_9th_unique_economy.merge(subset_8th_unique_economy, on=['scenario', 'sub1sectors', 'sub2sectors', 'fuels', 'subfuels'], how='left')
    
    # Define the file name with full path for each economy
    file_name = os.path.join(output_directory, f"{economy}.xlsx")

    # Save the merged DataFrame to Excel
    merged_economy.to_excel(file_name, index=False)




# import os

# # Define the directory where you want to save the Excel files
# output_directory = "path/to/your/directory"

# for economy in buildings_9th_historical_trunc['economy'].unique():
#     subset_8th_unique_economy = buildings_8th_projected_map[buildings_8th_projected_map['REGION'] == economy]
#     merged_9th_economy = buildings_9th_historical_trunc.merge(subset_8th_unique_economy, on=['scenarios', 'sub1sectors', 'sub2sectors', 'fuels', 'subfuels'], how='left')
    
#     # Define the file name with full path for each economy
#     file_name = os.path.join(output_directory, f"merged_data_{economy}.xlsx")
    
#     # Save the merged DataFrame to Excel
#     merged_9th_economy.to_excel(file_name, index=False)




# for economy in ninth_trunc['economy'].unique():
#     #file_location = './results/buildings_merge/{}/'.format(economy)
#     subset_9th_unique_economy = ninth_trunc[ninth_trunc['economy'] == economy]
#     #subset_9th_unique_economy
#     subset_8th_unique_economy = eighth_results_map[eighth_results_map['REGION'] == economy]
#     #subset_8th_unique_economy
#     merged_9th_economy = ninth_trunc.merge(subset_8th_unique_economy, on=['scenario', 'sub1sectors', 'sub2sectors', 'fuels', 'subfuels'], how='left')
#     #merged_9th_economy
#     merged_results_full = pd.concat([merged_results_full, merged_9th_economy], ignore_index=True)
#     #merged_results_full

# # for economy in ninth_trunc['economy'].unique():
# #     subset_8th_unique_economy = eighth_results_map[eighth_results_map['REGION'] == economy]
# #     merged_9th_economy = ninth_trunc.merge(subset_8th_unique_economy, on=['scenario', 'sub1sectors', 'sub2sectors', 'fuels', 'subfuels'], how='left')

# # merged_9th_economy
#     # file_name = f"merged_data_{economy}.xlsx"
#     # merged_9th_economy.to_excel(file_name, index=False)

# # for economy in buildings_9th_historical_trunc['economy'].unique():
# #     subset_8th_unique_economy = buildings_8th_projected_map[buildings_8th_projected_map['REGION'] == economy]
# #     merged_9th_economy = buildings_9th_historical_trunc.merge(subset_8th_unique_economy, on=['scenarios', 'sub1sectors', 'sub2sectors', 'fuels', 'subfuels'], how='left')
    
# #     # Define the file name for each economy
# #     file_name = f"merged_data_{economy}.xlsx"
    
# #     # Save the merged DataFrame to Excel
# #     merged_9th_economy.to_excel(file_name, index=False)




# # #for scenario_ninth in ninth_trunc['scenarios'].unique():
# #    # for scenario_eighth in eighth_results_map['SCENARIO'].unique():
# #     #eight_results_merge = eighth_results_map[eighth_results_map['SCENARIO'] == scenario_eighth]
# #     #eight_results_merge
# #     #columns_to_merge2 = eight_results_merge.loc[:, 2017:'subfuels']
# #     #columns_to_merge2
    
# # merged_9th = ninth_trunc[ninth_trunc['scenarios'] == scenario_ninth]
# # merged_9th
# # merged_df = merged_9th.merge(columns_to_merge2, on=['sub1sectors', 'sub2sectors', 'fuels', 'subfuels', 'scenario'], how='left')
# # merged_df
# #         #append the results from merged df to merged_results
# # merged_results = pd.concat([merged_results, merged_df], ignore_index=True)
    
# # merged_results


# # #for each unique scenario in the 9th file
# # #filter the eighth 

# # #the issue is that when i filter the 9th for a scenario, the 8th still has both scenarios so thre are two places where identifier from map matchs properly

# # testing_copy_8th[['sub1sectors', 'sub2sectors', 'fuels', 'subfuels']] = testing_copy_8th['FUEL'].map(mapping_dictionary).apply(pd.Series)
# # testing_copy_8th    
# # #testing_copy_8th.to_excel('output8.xlsx', index=False)  # This will save the DataFrame to 'output.xlsx' without row indices

# # #print(testing_copy_8th.columns)
# # #print(type(testing_copy_8th))
# # #print(testing_copy_8th.head())

# # #truncate the 9th results to stop at the year 2021
# # testing_copy_9th_trunc = testing_copy_9th.iloc[:, 0:52].copy()
# # testing_copy_9th_trunc

# # #select the columns from the 8th to merge to the ninth
# # columns_to_merge = testing_copy_8th.loc[:, 2021:'subfuels']
# # columns_to_merge

# # merged_df = testing_copy_9th_trunc.merge(columns_to_merge, on=['sub1sectors', 'sub2sectors', 'fuels', 'subfuels'], how='left')
# # merged_df
# # merged_df.to_excel('Merged_8th_into_9th.xlsx', index=False)