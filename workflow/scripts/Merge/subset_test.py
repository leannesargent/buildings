import pandas as pd

import os
import re

wanted_wd = 'buildings'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

#Eighth results contain only buildings values, for future projection
eighth_results = pd.read_excel('./data/8th_results/data_sheet_buildings.xlsx', sheet_name='AccumulatedAnnualDemand')

#Ninth results contain values for all sectors, read in total csv then subset only buildings sub1sector
ninth_historical_values = pd.read_csv('./data/9th_historical_values/model_df_wide_20240112.csv')
#buildings_9th = ninth_historical_values[ninth_historical_values['sub1sectors'] == '16_01_buildings']

buildings_9th = ninth_historical_values[
    (ninth_historical_values['sub2sectors'] == '16_01_01_commercial_and_public_services') |
    (ninth_historical_values['sub2sectors'] == '16_01_02_residential')
]

eighth_results
ninth_historical_values
buildings_9th

#Read in excel file that matches 8th results notation to fuel identifiers in 9th
mapping_file = pd.read_excel('./data/buildings_mapping.xlsx')
mapping_file

# Convert mapping_file into a dictionary
mapping_dictionary = mapping_file.set_index(mapping_file.columns[0]).apply(list, axis=1).to_dict()
mapping_dictionary

subset_CDA_9th = buildings_9th[buildings_9th['economy'] == '03_CDA']
subset_CDA_8th = eighth_results[eighth_results['REGION'] == '03_CDA']

subset_CDA_9th
subset_CDA_8th


#Mapping_sheets = list(pd.read_excel(path_mapping + 'mapping_for_2020.xlsx', sheet_name = None).key(df.columns[0])).to_dict[orient='index']
#Mapping_file = pd.DataFrame()

#for sheet in Mapping_sheets:
#   interim_map = pd.read_excel(path_mapping + 'mapping_for_2020.xlsx', sheet_name = sheet, skiprows = 1)
#   Mapping_file = Mapping_file.append(interim_map).reset_index(drop = True)

#for region in ref_aggregate_df1['REGION'].unique():
#    interim_df1 = ref_aggregate_df1[ref_aggregate_df1['REGION'] == region]
#    interim_df1 = interim_df1.merge(Mapping_TFC_TPES, how = 'left', on = ['TECHNOLOGY', 'FUEL'])
#    interim_df1 = interim_df1.groupby(['item_code_new', 'fuel_code']).sum().reset_index()

testing_copy_9th = subset_CDA_9th.copy()
testing_copy_9th
#testing_copy_9th.to_excel('output9.xlsx', index=False)  # This will save the DataFrame to 'output.xlsx' without row indices

testing_copy_8th = subset_CDA_8th.copy()
testing_copy_8th
#print(testing_copy_8th.columns)

# Merge df2 with df1 using the dictionary
#testing_copy_9th['8th_identifier'] = testing_copy_9th[['sub1sectors', 'sub2sectors', 'fuels', 'subfuels']].apply(lambda row: mapping_dictionary.get(list(row)), axis=1)
#testing_copy_9th                            
                                                                                                                 
# Merge df2 with df1 using the dictionary
#adding the four columns to the 8th and doing the match based on the FUEL column of the 8th, which is mapped to the four columns through the dictionary
testing_copy_8th[['sub1sectors', 'sub2sectors', 'fuels', 'subfuels']] = testing_copy_8th['FUEL'].map(mapping_dictionary).apply(pd.Series)
testing_copy_8th    
#testing_copy_8th.to_excel('output8.xlsx', index=False)  # This will save the DataFrame to 'output.xlsx' without row indices

#print(testing_copy_8th.columns)
#print(type(testing_copy_8th))
#print(testing_copy_8th.head())

#truncate the 9th results to stop at the year 2021
testing_copy_9th_trunc = testing_copy_9th.iloc[:, 0:52].copy()
testing_copy_9th_trunc

#select the columns from the 8th to merge to the ninth
#columns_to_merge = testing_copy_8th.loc[:, 2021:'subfuels']
#columns_to_merge

#merged_df = testing_copy_9th_trunc.merge(columns_to_merge, on=['sub1sectors', 'sub2sectors', 'fuels', 'subfuels'], how='left')
merged_df = testing_copy_9th_trunc.merge(testing_copy_8th, on=['sub1sectors', 'sub2sectors', 'fuels', 'subfuels'], how='left')
merged_df
merged_df.to_excel('Merged_8th_into_9th.xlsx', index=False)