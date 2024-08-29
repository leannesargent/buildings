import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import os
import re

wanted_wd = 'buildings'

os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)


variable_path = './data/test_data/srv/'
# economy_list = pd.read_csv(variable_path + 'APEC_economies.csv').iloc[:, 0]


#import needed data sets
test_data = pd.read_csv(variable_path + 'Test_EI_srv.csv')
pop_data = pd.read_csv(variable_path + 'population_test.csv')
energy_data = pd.read_csv(variable_path + 'energy_data_srv.csv')

#Data manipulation

# Create DataFrame
df = pd.DataFrame(test_data)

df.replace('..', np.nan, inplace=True)

for col in df.columns[3:]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Melt the DataFrame to long format
df_long = pd.melt(df, id_vars=["Country", "End use", "Indicator"], var_name="Year", value_name="GJ/cap")
df_long = df_long[df_long["End use"] != "Total Services"]

pop_long = pd.melt(pop_data, id_vars=["Country"], var_name="Year", value_name="Population")
pop_long["Year"] = pop_long["Year"].astype(str)

energy_data_long = pd.melt(energy_data, id_vars=['Country', 'End use', 'Product'], var_name='Year', value_name='Energy PJ')
energy_data_long['Energy PJ'] = pd.to_numeric(energy_data_long['Energy PJ'], errors='coerce')


# df_long
# pop_long
# energy_data_long

df_long = df_long.merge(pop_long, on=["Country", "Year"], how="left")

df_long.rename(columns={'Population':'Population (thousands)'}, inplace=True)
df_long['Population'] = df_long['Population (thousands)'] *1000

df_long["inverse_pop"] = 1 / df_long["Population"]
df_long["GJ (GJ/cap x Pop)"] = df_long["GJ/cap"] * df_long["Population"]

df_long['EI derived PJ'] = df_long['GJ (GJ/cap x Pop)'] / 1e6
df_long

df_long = df_long.merge(energy_data_long, on=['Country', 'End use', 'Year'], how="left")
# df_long.drop(columns=['Population (thousands)', 'Product'])

df_long = df_long.sort_values(by=['Country', 'End use', 'Year'])
df_long

# # Assuming df_long is your DataFrame
# output_path = './data/test_data/output.csv'  # Specify your desired output file path
# df_long.to_csv(output_path, index=False)

# print(df_long["Country"].unique())

#Plot the PJ from EI*pop on same plot with direct energy PJ use from IEA
df_long['EI PJ - Energy PJ / Energy PJ (%)'] = ((abs(df_long['EI derived PJ'] - df_long['Energy PJ']))/df_long['Energy PJ']) * 100
df_long['EI PJ - Energy PJ (abs)'] = abs(df_long['EI derived PJ'] - df_long['Energy PJ'])
df_long

output_dir_data = variable_path + '/data_output/'
if not os.path.exists(output_dir_data):
    os.makedirs(output_dir_data)

output_path = output_dir_data + 'output_srv_EI_vs_energy_comp.csv'
df_long.to_csv(output_path, index=False)

###### energy intesntiy data for srv only has certain rows for some economies - Fin's analysis shows the rows missing

# Plotting
# for economy in df_long["Country"].unique():
#     country_data = df_long[df_long["Country"] == economy]
#     print(economy)
    
#     plt.figure(figsize=(12, 8))

#     # Create primary y-axis
#     ax1 = plt.gca()
#     lines1 = []
#     labels1 = []
#     for end_use in country_data["End use"].unique():
#         subset = country_data[country_data["End use"] == end_use]
#         line, = ax1.plot(subset["Year"], subset["EI PJ - Energy PJ / Energy PJ (%)"], label=f'{end_use} (%)')
#         lines1.append(line)
#         labels1.append(f'{end_use} (%)')

#     ax1.set_xlabel('Year')
#     plt.xticks(rotation=50)
#     ax1.set_ylabel('[EI PJ - Energy PJ / Energy PJ] (%)')
#     ax1.set_ylim(0, 50)

#     # Create secondary y-axis
#     ax2 = ax1.twinx()
#     lines2 = []
#     labels2 = []
#     for end_use in country_data["End use"].unique():
#         subset = country_data[country_data["End use"] == end_use]
#         line, = ax2.plot(subset["Year"], subset["EI PJ - Energy PJ (abs)"], linestyle='--', label=f'{end_use} Abs', alpha=0.7)
#         lines2.append(line)
#         labels2.append(f'{end_use} Abs')

#     ax2.set_ylabel('[EI PJ - Energy PJ] (PJ)')
#     ax2.set_ylim(0, df_long['EI PJ - Energy PJ (abs)'].max() * 1.1)

#     # Combine legends
#     lines = lines1 + lines2
#     labels = labels1 + labels2
#     ax1.legend(lines, labels, loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0., ncol=1, fontsize='small', frameon=False)

#     plt.title(economy)
#     plt.tight_layout()  # Adjust layout to make room for the legend

#     plt.show()



# plt.figure(figsize=(12,8))

# for economy in df_long["Country"].unique():
#     country_data = df_long[df_long["Country"] == economy]
#     print(economy)

#     # Iterate through each unique "end use" and plot
#     for end_use in country_data["End use"].unique():
#         subset = country_data[country_data["End use"] == end_use]
#         plt.plot(subset["Year"], subset["EI PJ - Energy PJ / Energy PJ (%)"], label=end_use)

#    # # Customize the plot
#     # plt.title('Energy Intensity by End Use')
#     # plt.xlabel('Year')
#     # plt.ylabel('Per Capita Energy Intensity (GJ/cap)')
#     plt.title(economy)
#     plt.ylabel('[EI PJ - Energy PJ / Energy PJ] (%)')
#     plt.xlabel('Year')
#     plt.xticks(rotation=50)
#     # plt.ylim(0,50)
#     plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0., ncol=1, fontsize='small', frameon=False)
#     # plt.grid(True)
#     # plt.xticks(df_long["Year"].unique())  # Ensure all years are shown on the x-axis

#     # Show the plot
#     plt.show()


# plt.figure(figsize=(12,8))

# for economy in df_long["Country"].unique():
#     country_data = df_long[df_long["Country"] == economy]
#     print(economy)

#     # Iterate through each unique "end use" and plot
#     for end_use in country_data["End use"].unique():
#         subset = country_data[country_data["End use"] == end_use]
#         plt.plot(subset["Year"], subset["EI PJ - Energy PJ (abs)"], label=end_use)

#    # # Customize the plot
#     # plt.title('Energy Intensity by End Use')
#     # plt.xlabel('Year')
#     # plt.ylabel('Per Capita Energy Intensity (GJ/cap)')
#     plt.title(economy)
#     plt.ylabel('EI PJ - Energy PJ (abs)')
#     plt.xlabel('Year')
#     plt.xticks(rotation=50)
#     # plt.ylim(0,50)
#     plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0., ncol=1, fontsize='small', frameon=False)
#     # plt.grid(True)
#     # plt.xticks(df_long["Year"].unique())  # Ensure all years are shown on the x-axis

#     # Show the plot
#     plt.show()

########################################################################################################################
########################################################################################################################
# # Save the figures
# output_dir = variable_path + '/plots/'
# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)

# # Plot and save both plots (percentage and absolute) for each economy
# for economy in df_long["Country"].unique():
#     country_data = df_long[df_long["Country"] == economy]
#     print(economy)

#     # Create a figure with two subplots
#     fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 16), sharex=True)

#     # Plot "EI PJ - Energy PJ / Energy PJ (%)" on the first subplot
#     for end_use in country_data["End use"].unique():
#         subset = country_data[country_data["End use"] == end_use]
#         ax1.plot(subset["Year"], subset["EI PJ - Energy PJ / Energy PJ (%)"], label=end_use)

#     ax1.set_title(f'{economy}')
#     ax1.set_ylabel('[EI PJ - Energy PJ / Energy PJ] (%)')
#     ax1.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0., ncol=1, fontsize='small', frameon=False)
#     # ax1.set_ylim(0, 50)
#     ax1.grid(True)
#     ax1.tick_params(axis='x', rotation=50)  # Rotate x-axis labels

#     # Plot "EI PJ - Energy PJ (abs)" on the second subplot
#     for end_use in country_data["End use"].unique():
#         subset = country_data[country_data["End use"] == end_use]
#         ax2.plot(subset["Year"], subset["EI PJ - Energy PJ (abs)"], label=end_use)

#     ax2.set_ylabel('EI PJ - Energy PJ (abs)')
#     ax2.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0., ncol=1, fontsize='small', frameon=False)
#     # ax2.set_ylim(0, df_long['EI PJ - Energy PJ (abs)'].max() * 1.1)
#     ax2.grid(True)
#     ax2.tick_params(axis='x', rotation=50)  # Rotate x-axis labels

#     # Common x-axis label
#     ax2.set_xlabel('Year')

#     # Adjust layout to make room for the legend
#     plt.tight_layout()

#     # Save the figure to a file
#     plt.savefig(os.path.join(output_dir, f'{economy}_energy_intensity_combined.png'))
#     plt.close()

# for economy in df_long["Country"].unique():
#     country_data = df_long[df_long["Country"] == economy]
#     print(economy)

#     # Create a figure with a 2x2 grid of subplots
#     fig, axs = plt.subplots(2, 2, figsize=(16, 12), sharex=True)

#     # Plot "EI PJ - Energy PJ / Energy PJ (%)" on the first subplot
#     for end_use in country_data["End use"].unique():
#         subset = country_data[country_data["End use"] == end_use]
#         axs[0, 0].plot(subset["Year"], subset["EI PJ - Energy PJ / Energy PJ (%)"], label=end_use)

#     axs[0, 0].set_title(f'{economy} - Percentage')
#     axs[0, 0].set_ylabel('[EI PJ - Energy PJ / Energy PJ] (%)')
#     axs[0, 0].legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0., ncol=1, fontsize='small', frameon=False)
#     # axs[0, 0].set_ylim(0, 50) ~   
#     axs[0, 0].grid(True)    

#     # Plot "EI PJ - Energy PJ (abs)" on the         second subplot
#     for end_use in country_data["End use"].unique():
#         subset = country_data[country_data["End use"] == end_use]
#         axs[0, 1].plot(subset["Year"], subset["EI PJ - Energy PJ (abs)"], label=end_use)

#     axs[0, 1].set_title(f'{economy} - Absolute')
#     axs[0, 1].set_ylabel('EI PJ - Energy PJ (abs)')
#     axs[0, 1].legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0., ncol=1, fontsize='small', frameon=False)
#     # axs[0, 1].set_ylim(0, df_long['EI PJ - Energy PJ (abs)'].max() * 1.1)
#     axs[0, 1].grid(True)

#     # Plot "Population" on the third subplot
#     axs[1, 0].plot(country_data["Year"].unique(), country_data.groupby("Year")["Population"].sum(), label='Population', color='green')
#     axs[1, 0].set_title(f'{economy} - Population')
#     axs[1, 0].set_ylabel('Population')
#     axs[1, 0].grid(True)

#     # Plot "GJ/cap" on the fourth subplot
#     for end_use in country_data["End use"].unique():
#         subset = country_data[country_data["End use"] == end_use]
#         axs[1, 1].plot(subset["Year"], subset["GJ/cap"], label=end_use)

#     axs[1, 1].set_title(f'{economy} - GJ/cap')
#     axs[1, 1].set_ylabel('GJ/cap')
#     axs[1, 1].legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0., ncol=1, fontsize='small', frameon=False)
#     axs[1, 1].grid(True)

#     # Common x-axis label
#     for ax in axs.flat:
#         ax.set_xlabel('Year')
#         ax.tick_params(axis='x', rotation=50)  # Rotate x-axis labels

#     # Adjust layout to make room for the legends
#     plt.tight_layout()

#     # Save the figure to a file
#     plt.savefig(os.path.join(output_dir, f'{economy}_energy_intensity_combined.png'))
#     plt.close()
########################################################################################################################
########################################################################################################################


# Stan Dev
########################################################################################################################
########################################################################################################################
# Initialize a dictionary to store the results
std_dev_dict = {}
mean_dict = {}

output_dir = variable_path + '/plots/mean_stan_dev'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop through each unique end use in the DataFrame
for end_use in df_long['End use'].unique():
    # Filter the DataFrame for the current end use
    filtered_df = df_long[df_long['End use'] == end_use]
    
    # Group the filtered data by 'Year' and calculate the standard deviation for the value column
    std_dev_by_year = filtered_df.groupby('Year')['GJ/cap'].std()

    # Group the filtered data by 'Year' and calculate the mean for the value column
    mean_by_year = filtered_df.groupby('Year')['GJ/cap'].mean()
    
    # Store the result in the dictionary with the end use as the key
    std_dev_dict[end_use] = std_dev_by_year.reset_index()
    std_dev_dict[end_use].columns = ['Year', 'Standard Deviation of GJ/cap']

    mean_dict[end_use] = mean_by_year.reset_index()
    mean_dict[end_use].columns = ['Year', 'Mean of GJ/cap']

# Convert the dictionary to a DataFrame for better visualization (optional)
std_dev_df = pd.concat(std_dev_dict, axis=0).reset_index(level=0).rename(columns={'level_0': 'End use'})
mean_df = pd.concat(mean_dict, axis=0).reset_index(level=0).rename(columns={'level_0': 'End use'})

std_dev_df
mean_df

comp_df = pd.merge(std_dev_df, mean_df, on=['End use', 'Year'])
comp_df.to_csv(variable_path + 'std_of_GJ_per_cap.csv')
comp_df

for end_use in comp_df['End use'].unique():
    # Filter data for the current end use
    filtered_df = comp_df[comp_df['End use'] == end_use]

    # Plotting the mean with standard deviation as error bars
    plt.figure(figsize=(10, 6))

    plt.errorbar(filtered_df['Year'], filtered_df['Mean of GJ/cap'], yerr=filtered_df['Standard Deviation of GJ/cap'], fmt='-o', capsize=5)

    # Customize the plot
    plt.title(f'{end_use} Mean GJ/cap with Standard Deviation Over Time')
    plt.xlabel('Year')
    plt.ylabel('GJ/cap')
    plt.xticks(rotation=45)
    plt.grid(True)

    # Show the plot
    # plt.show()

    # Save the figure to a file
    plt.savefig(os.path.join(output_dir, f'{end_use}_mean_stan_dev.png'))
    plt.close()
########################################################################################################################
########################################################################################################################



apec_data_df_all_data = pd.read_csv("./data/9th_historical_values/model_df_wide_20240119.csv")
apec_data_df_all_data

filtered_df = apec_data_df_all_data[apec_data_df_all_data['sectors'] == '16_other_sector']
filtered_df = filtered_df[filtered_df['sub1sectors'] == '16_01_buildings']
filtered_df = filtered_df[filtered_df['sub2sectors'] == '16_01_01_commercial_and_public_services']
filtered_df = filtered_df[filtered_df['scenarios'] == 'reference']
apec_totals = filtered_df[filtered_df['fuels'] == '19_total']
apec_totals

OECD_countries = ['01_AUS', '03_CDA', '04_CHL', '06_HKC', '20_USA', '08_JPN', '09_ROK', '11_MEX', '12_NZ', '18_CT']

OECD_totals_df_all_columns = apec_totals[apec_totals['economy'].isin(OECD_countries)]
OECD_totals_df_all_columns

OECD_totals_df1 = OECD_totals_df_all_columns.drop(columns=['fuels', 'scenarios', 'sectors', 'sub1sectors', 'sub2sectors', 'sub3sectors', 'sub4sectors', 'subfuels', 'is_subtotal'])
OECD_totals_df1


OECD_totals_df_long = pd.melt(OECD_totals_df1, id_vars=["economy"], var_name="Year", value_name="19_total")
OECD_totals_df_long = OECD_totals_df_long.sort_values(by=['economy', 'Year'])
OECD_totals_df_long["Year"] = OECD_totals_df_long["Year"].astype(int)
APERC_energytotals_df = OECD_totals_df_long[OECD_totals_df_long['Year'].between(2000, 2021)]
APERC_energytotals_df["Year"] = APERC_energytotals_df["Year"].astype(str)
APERC_energytotals_df 


####################
# filter and sum the IEA energy values to get one value for energy use calculated, PJ, for each year for each economy
results = []


for economy in df_long['Country'].unique():
    # Filter data for the current end use
    filtered_df = df_long[df_long['Country'] == economy]

    for year in filtered_df['Year'].unique():
        filtered_df2 = filtered_df[filtered_df['Year'] == year]
        
        # Taking the energy in PJ derived from multiplying the IEA EI value by the APERC population value
        energy_sum = filtered_df2['EI derived PJ'].sum()

        results.append({'Country': economy, 'Year': year, 'IEA EI*APERC Pop': energy_sum})

IEA_energyresults_df = pd.DataFrame(results)
IEA_energyresults_df = IEA_energyresults_df[IEA_energyresults_df['Country'] != 'IEA Total']
IEA_energyresults_df = IEA_energyresults_df.rename(columns={'Country': 'economy'})
IEA_energyresults_df

df_IEA_APERC_energy = APERC_energytotals_df.merge(IEA_energyresults_df, on=['economy', 'Year'], how="left")
df_IEA_APERC_energy

output_dir = variable_path + '/plots/'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for economy in df_IEA_APERC_energy['economy'].unique():
    # Filter data for the current economy
    plot_data = df_IEA_APERC_energy[df_IEA_APERC_energy['economy'] == economy]

    # Plot data for the current economy
    plt.plot(plot_data['Year'], plot_data['19_total'], marker='o', label='APERC Reported')
    plt.plot(plot_data['Year'], plot_data['IEA EI*APERC Pop'], marker='o', label='IEA EI*APERC Pop')
    
    # Set the title and labels
    plt.title(f'Energy Data for {economy}')
    plt.xlabel('Year')
    plt.xticks(rotation=50)
    plt.ylabel('Total Energy (PJ)')
    plt.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9), fontsize='small')
    plt.legend(loc='upper right', bbox_to_anchor=(1, 1), fontsize='small', frameon=False)

    # Show the plot for the current economy
    # plt.show()
    # Save the figure to a file
    plt.savefig(os.path.join(output_dir, f'Basic values - {economy}.png'))
    plt.close()

df_IEA_APERC_comp = df_IEA_APERC_energy.copy()

df_IEA_APERC_comp['Absolute Difference'] = abs(df_IEA_APERC_comp['IEA EI*APERC Pop'] - df_IEA_APERC_comp['19_total'])
df_IEA_APERC_comp['% Diff'] = (df_IEA_APERC_comp['Absolute Difference']/df_IEA_APERC_comp['19_total']) * 100
# df_IEA_APERC_comp

df_IEA_APERC_comp.to_csv(variable_path + 'data_output/iea_aperc_comp.csv')

output_dir = variable_path + '/plots/IEA vs APERC Energy/abs and perc sep plots'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for economy in df_IEA_APERC_comp['economy'].unique():
    # Filter data for the current economy
    plot_data_perc = df_IEA_APERC_comp[df_IEA_APERC_comp['economy'] == economy]

    # Plot data for the current economy
    plt.plot(plot_data_perc['Year'], plot_data_perc['% Diff'], marker='o')
    
    # Set the title and labels
    plt.title(f'% Difference between IEA and APERC reported for {economy}')
    plt.xlabel('Year')
    plt.xticks(rotation=50)
    plt.ylabel('% Difference')

    # Show the plot for the current economy
    # plt.show()
    # Save the figure to a file
    plt.savefig(os.path.join(output_dir, f'% Difference {economy}.png'))
    plt.close()

for economy in df_IEA_APERC_comp['economy'].unique():
    # Filter data for the current economy
    plot_data_abs = df_IEA_APERC_comp[df_IEA_APERC_comp['economy'] == economy]

    # Plot data for the current economy
    plt.plot(plot_data_abs['Year'], plot_data_abs['Absolute Difference'], marker='o')
    
    # Set the title and labels
    plt.title(f'Absolute Difference between IEA and APERC reported for {economy}')
    plt.xlabel('Year')
    plt.xticks(rotation=50)
    plt.ylabel('Abs Difference')

    # Show the plot for the current economy
    # plt.show()
    # Save the figure to a file
    plt.savefig(os.path.join(output_dir, f'Abs Difference {economy}.png'))
    plt.close()


output_dir = variable_path + '/plots/IEA vs APERC Energy/both'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for economy in df_IEA_APERC_comp['economy'].unique():
    # Filter data for the current economy
    plot_data_both = df_IEA_APERC_comp[df_IEA_APERC_comp['economy'] == economy]

#     # Create a figure with two subplots
    fig_comp, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 16), sharex=True)

    ax1.plot(plot_data_both['Year'], plot_data_both['% Diff'], marker='o', label='% Diff')
    ax1.set_title(f'{economy}')
    ax1.set_ylabel('[% Difference')
    ax1.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0., ncol=1, fontsize='small', frameon=False)
    # ax1.set_ylim(0, 50)
    ax1.grid(True)
    ax1.tick_params(axis='x', rotation=50)  # Rotate x-axis labels
    # Common x-axis label
    ax1.set_xlabel('Year')

    ax2.plot(plot_data_both['Year'], plot_data_both['Absolute Difference'], marker='x', label='Abs Diff')
    ax2.set_ylabel('Absolute Difference')
    ax2.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0., ncol=1, fontsize='small', frameon=False)
    # ax2.set_ylim(0, df_long['EI PJ - Energy PJ (abs)'].max() * 1.1)
    ax2.grid(True)
    ax2.tick_params(axis='x', rotation=50)  # Rotate x-axis labels

    # Common x-axis label
    ax2.set_xlabel('Year')

    # Adjust layout to make room for the legend
    plt.tight_layout()

    # Save the figure to a file
    plt.savefig(os.path.join(output_dir, f'{economy}_absolute and percent difference.png'))
    plt.close()

# # Plotting
# plt.figure(figsize=(12, 8))

# for economy in df_long["Country"].unique():
#     country_data = df_long[df_long["Country"] == economy]
#     print(economy)

#     # Iterate through each unique "end use" and plot
#     for end_use in country_data["End use"].unique():
#         subset = country_data[country_data["End use"] == end_use]
#         plt.plot(subset["Year"], subset["Value"], label=end_use)

#     # plt.twinx()  # Create a secondary y-axis
#     # plt.plot(country_data["Year"], country_data["Population"], 'r--', label='Population', alpha=0.7)

#     # # Customize the plot
#     # plt.title('Energy Intensity by End Use')
#     # plt.xlabel('Year')
#     # plt.ylabel('Per Capita Energy Intensity (GJ/cap)')
#     plt.title(economy)
#     plt.ylabel('Per capita energy intensity (GJ/cap)')
#     plt.xlabel('Year')
#     plt.xticks(rotation=50)
#     plt.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9), fontsize='small')
#     plt.legend(loc='upper right', bbox_to_anchor=(1, 1), fontsize='small', frameon=False)
#     # plt.grid(True)
#     # plt.xticks(df_long["Year"].unique())  # Ensure all years are shown on the x-axis

#     # Show the plot
#     plt.show()
