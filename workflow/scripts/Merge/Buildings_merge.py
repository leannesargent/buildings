import pandas as pd

import datetime
current_date = datetime.datetime.now().strftime("%Y_%m_%d")
#current_date

import os
import re


wanted_wd = 'buildings'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

#Read in results from the 8th outlook to use for projected results
buildings_8th_projected = pd.read_excel('./data/8th_results/data_sheet_buildings.xlsx', sheet_name='AccumulatedAnnualDemand')

#Ninth results contain values for all sectors, read in total csv and subset in the next lines
ninth_historical_values = pd.read_csv('./data/9th_historical_values/model_df_wide_20240119.csv')

#Filter ninth_historical_values for just sub2sectors 16_01_01_commercial_and_public_services and 16_01_02_residential
buildings_9th_historical = ninth_historical_values[
    (ninth_historical_values['sub2sectors'] == '16_01_01_commercial_and_public_services') |
    (ninth_historical_values['sub2sectors'] == '16_01_02_residential')
]

#can use these lines to check the dfs
buildings_8th_projected
buildings_9th_historical
#buildings_9th_historical.to_excel('./data/excel_checks/Buildings_9th_historical_sub2sector_filtered.xlsx', index=False)

#Read in mapping file
mapping_file = pd.read_excel('./data/identifiers/buildings_mapping_scenario.xlsx')
mapping_file

# Convert mapping_file into a dictionary
mapping_dictionary = mapping_file.set_index(['Scenario_8th', '8th_fuels']).apply(list, axis=1).to_dict()
mapping_dictionary

#Make a copy of 8th results
buildings_8th_projected_map = buildings_8th_projected.copy()
buildings_8th_projected_map

# Map identifiers from the 9th df into the 8th df
buildings_8th_projected_map[['scenarios', 'sub1sectors', 'sub2sectors', 'fuels', 'subfuels']] = buildings_8th_projected[['SCENARIO', 'FUEL']].apply(lambda row: tuple(row), axis=1).map(mapping_dictionary).apply(pd.Series)
buildings_8th_projected_map

#truncate the 9th results to stop at the year 2021 for ease when merging values from 8th into the 9th
buildings_9th_historical_trunc = buildings_9th_historical.iloc[:, 0:52].copy()
buildings_9th_historical_trunc

#define list of economies to loop through
economies = ['01_AUS', '02_BD', '03_CDA', '04_CHL', '05_PRC', '06_HKC', '07_INA', '08_JPN', '09_ROK', '10_MAS', '11_MEX', '12_NZ', '13_PNG', '14_PE', '15_PHL', '16_RUS', '17_SGP', '18_CT', '19_THA', '20_USA', '21_VN']
# remove Russia which had its trajectory manually altered
economies_filtered = economies[0:15] + economies[16:22]
economies_filtered

# TWO MERGES DEFINED BELOW - ONE FOR VALUES THAT ARE NON ADJUSTED AND ONE FOR VALUES THAT GET ADJUSTED USING DIFFERENCE BETWEEN MODELLED AND REAL 2021 DATA
## way 1 is to simply merge the values for 2022 onwards from the 8th into the 9th with no adjustment - files too be denoted by _nonadjusted
## way 2 is to subtract the real value for 2021 from the 9th data from the modelled value from the 8th projections, and then add that difference to each value in the row for 2022 onwards - files to be denoted by _adjusted


# Define the directory where you want to save the Excel files
# for non adjusted values
# output_directory_nonadjusted = "./results/buildings_merge/nonadjusted"

#for adjusted values
output_directory_adjusted = "./results/buildings_merge/adjusted"

##################################################################################################################################################################
################ NON ADJUSTED ###########################

#create empty list to append economy results
# combined_merge_nonadjusted = []

# #loop through each economy
# for economy in economies:
#     #subset the 9th data sheet for each economy
#     subset_9th_unique_economy_nonadjusted = buildings_9th_historical_trunc[buildings_9th_historical_trunc['economy'] == economy]
#     subset_9th_unique_economy_nonadjusted

#     #subset the 8th data sheet for each economy
#     subset_8th_unique_economy_nonadjusted = buildings_8th_projected_map[buildings_8th_projected_map['REGION'] == economy]
#     subset_8th_unique_economy_nonadjusted
    
#     #define the columns to merge from the 8th into the 9th
#     columns_to_merge_nonadjusted = subset_8th_unique_economy_nonadjusted.loc[:, 2022:'subfuels']

#     #merge results from 8th into 9th
#     merged_economy_nonadjusted = subset_9th_unique_economy_nonadjusted.merge(columns_to_merge_nonadjusted, on=['scenarios', 'sub1sectors', 'sub2sectors', 'fuels', 'subfuels'], how='left')

    
#     # drop rows with no entry at all
#     columns_to_check_nonadjusted = [2022]
#     merged_unique_economy_nonadjusted = merged_economy_nonadjusted.dropna(subset=columns_to_check_nonadjusted)
#     merged_unique_economy_nonadjusted

#     # Define the file name with full path for each economy
#     file_name = os.path.join(output_directory_nonadjusted, f"{economy}_nonadjusted.xlsx")
#     # Save the merged df for each economy to Excel
#     merged_unique_economy_nonadjusted.to_excel(file_name, index=False)

#     #append all economies into the list
#     combined_merge_nonadjusted.append(merged_unique_economy_nonadjusted)

# #concatenate the list of economies into a df
# all_economies_merged_nonadjusted = pd.concat(combined_merge_nonadjusted, ignore_index=True)
# all_economies_merged_nonadjusted
# all_economies_merged_nonadjusted.to_excel("./results/buildings_merge/nonadjusted/all_economies_merged_nonadjusted.xlsx", index=False)


##################################################################################################################################################################

################ ADJUSTED ###########################

#create empty list to append economy results
combined_merge_adjusted = []

#loop through each economy
for economy in economies_filtered:
    #subset the 9th data sheet for each economy
    subset_9th_unique_economy_adjusted = buildings_9th_historical_trunc[buildings_9th_historical_trunc['economy'] == economy]
    subset_9th_unique_economy_adjusted

    #subset the 8th data sheet for each economy
    subset_8th_unique_economy_v1_adjusted = buildings_8th_projected_map[buildings_8th_projected_map['REGION'] == economy]
    #rename the column 2021 to 2021_8th so that when merged for nonadjusted iterations the values from the 9th can be differentiated from the 8th
    subset_8th_unique_economy_adjusted = subset_8th_unique_economy_v1_adjusted.rename(columns={2021: '2021_8th'})
    
    #define the columns to merge from the 8th into the 9th
    columns_to_merge_adjusted = subset_8th_unique_economy_adjusted.loc[:, '2021_8th':'subfuels']

    #merge results from 8th into 9th
    merged_economy_adjusted = subset_9th_unique_economy_adjusted.merge(columns_to_merge_adjusted, on=['scenarios', 'sub1sectors', 'sub2sectors', 'fuels', 'subfuels'], how='left')

    #drop rows with no entry at all
    columns_to_check_adjusted = [2022]
    merged_unique_economy_adjusted = merged_economy_adjusted.dropna(subset=columns_to_check_adjusted)
    merged_unique_economy_adjusted

    #no need to save these results to Excel yet since the adjustement hasn't happened yet

    #append all economies into the list
    combined_merge_adjusted.append(merged_unique_economy_adjusted)

#concatenate the list of economies into a df - still no adjustement at this point
all_economies_merged_adjusted_step1 = pd.concat(combined_merge_adjusted, ignore_index=True)
all_economies_merged_adjusted_step1
#all_economies_merged_adjusted_step1.to_excel("./results/buildings_merge/adjusted/all_economies_merged_step1.xlsx", index=False)

############# calculate and apply adjustment ##############
# Define a custom function to find difference between the ninth data and 8th modelled results
def calculate_difference(row):
    return row['2021'] - row['2021_8th']

# make a copy of the step1 results and then apply the function to calculate the difference for each row
all_economies_merged_2021_adjusted = all_economies_merged_adjusted_step1.copy()
#add a column to store the difference
all_economies_merged_2021_adjusted['2021_difference'] = all_economies_merged_adjusted_step1.apply(calculate_difference, axis=1)
all_economies_merged_2021_adjusted


#identify the columns to adjust
columns_to_update = all_economies_merged_2021_adjusted.loc[:, 2022:2070]
columns_to_update

# through each row pick the value from 2021_difference column
for index, row in all_economies_merged_2021_adjusted.iterrows():
    diff = row['2021_difference']

    # for each column in that row, add the difference value and replace the original value with updated value
    for col in columns_to_update:
        all_economies_merged_2021_adjusted.at[index, col] += diff


# drop columns not needed - 2021 8th results replaced by historical 9th data, don't need 2021 difference column
all_economies_merged_2021_adjusted.drop(columns=['2021_8th', '2021_difference'], inplace=True)
all_economies_merged_2021_adjusted

# for columns 10 (i.e. 1980) to 2070, replace any negative values from the 2021 adjustment process with 0
for col in all_economies_merged_2021_adjusted.columns[10:]:
    all_economies_merged_2021_adjusted[col] = all_economies_merged_2021_adjusted[col].apply(lambda x: 0 if x <0 else x)

all_economies_merged_2021_adjusted
all_economies_merged_2021_adjusted.to_excel("./results/buildings_merge/adjusted/all_economies_merged_adjusted.xlsx", index=False)

# ### SAVE TO APERC FOLDER
# #separate the all_economies data for each economy
# economies_save = economies[0:2] + [economies[3]] + economies [5:7] + economies[8:17] + [economies[20]]
# economies_save

# for economy in economies_save:
#     subset_results_economy_adjusted = all_economies_merged_2021_adjusted[all_economies_merged_2021_adjusted['economy'] == economy]
#     subset_results_economy_adjusted

#     # existing_file_name = f"C:/Users/leanne.sargent/APERC/Outlook-9th - Modelling/Integration/{economy}/01_Demand/01_01_Buildings/{economy}_2021_adjusted.xlsx"
#     # new_file_name = f"C:/Users/leanne.sargent/APERC/Outlook-9th - Modelling/Integration/{economy}/01_Demand/01_01_Buildings/{economy}_2021_adjusted_{current_date}.xlsx"

#     save_directory = f"C:/Users/leanne.sargent/APERC/Outlook-9th - Modelling/Integration/{economy}/01_Demand/01_01_Buildings/"
#     file_name = os.path.join(save_directory, f"{economy}_2021adjusted_{current_date}.xlsx")

#     subset_results_economy_adjusted.to_excel(file_name, index=False)

## SAVE TO PERSONAL FOLDERS
for economy in economies_filtered:
    subset_results_economy_adjusted = all_economies_merged_2021_adjusted[all_economies_merged_2021_adjusted['economy'] == economy]
    subset_results_economy_adjusted

    #output_directory_economy = f"./results/buildings_merge/adjusted/{economy}"

    file_name = os.path.join(output_directory_adjusted, f"{economy}_adjusted.xlsx")

    subset_results_economy_adjusted.to_excel(file_name, index=False)

