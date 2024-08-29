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
economy_list
subsector_list = ['16_1_commercial_and_public_services', '16_2_residential']

# Import entire EB EGEDA file - all subsectors
# DF columns "economy", "product_code" (subfuel), "item_code" (subsector), 1980-2021
eb_data_all = pd.read_csv("./data/EGEDA/EGEDA_2020_created_14112022.csv")

# Filter EGEDA data to select only RES and SRV subsectors
eb_data = eb_data_all[
    (eb_data_all['item_code'] == '16_1_commercial_and_public_services') |
    (eb_data_all['item_code'] == '16_2_residential')]
eb_data

########################################################################################################
# Placeholder for selections (update with actual values as needed) ##FIX
economy_sel = economy_list[15]
# print(economy_sel)
subsector_sel = subsector_list[1]
# print(subsector_sel)
########################################################################################################

# Filtering the data based on selections
####### CURRENTLY THIS SELECTION SELECTS ONLY TOTAL
filtered_economy = eb_data[(eb_data["economy"] == economy_sel) & (eb_data["item_code"] == subsector_sel) & (eb_data['product_code'] == '19_total')].reset_index(drop=True)
filtered_economy

eb_final = filtered_economy.drop(columns=['product_code'])
eb_final
# DF with columns: economy (selected above), item code (selected above), year, and value (sum of all fuels for that year)
eb_melted = eb_final.melt(id_vars=['economy', 'item_code'], var_name='year', value_name='value')
# eb_melted
# DF with columns: economy (selected above), year, year, and subsector with values
eb_pivoted = eb_melted.pivot(index=['economy', 'year'], columns='item_code', values='value').reset_index()
# eb_pivoted
# Flatten the column headers
eb_pivoted.columns.name = None
eb_pivoted.columns = [col if not isinstance(col, tuple) else col[-1] for col in eb_pivoted.columns]
eb_df_filtered = eb_pivoted[(eb_pivoted["year"].astype(int) >= 1990)].drop(columns=['economy']).reset_index(drop=True)


# LOAD MACRO DATA
GDP_data = pd.read_csv(variable_path + 'GDP.csv')
GDP_economy = GDP_data[GDP_data["Economy"] == economy_sel]

Population_data = pd.read_csv(variable_path + 'Population.csv')
Population_economy = Population_data[Population_data["Economy"] == economy_sel]

urbanization_data = pd.read_csv(variable_path + 'urbanization.csv')
urbanization_economy = urbanization_data[urbanization_data["Economy"] == economy_sel]

# urbanization_economy
# Population_economy
# GDP_economy

def prepare_macro(df, value_col):
    df_filtered = df.melt(id_vars=["Economy", "Unit"], var_name="year", value_name=value_col).drop(columns=["Economy", "Unit"])
    return df_filtered.reset_index(drop=True)

GDP_df_filtered = prepare_macro(GDP_economy, 'GDP')
Population_df_filtered = prepare_macro(Population_economy, 'Population')
urbanization_df_filtered = prepare_macro(urbanization_economy, 'urbanization')

eb_df_filtered
GDP_df_filtered
Population_df_filtered
urbanization_df_filtered

variables = eb_df_filtered.merge(GDP_df_filtered, on='year').merge(Population_df_filtered, on='year').merge(urbanization_df_filtered, on='year')
if subsector_sel == subsector_list[1]:
    variables = variables.rename(columns={'16_2_residential': 'subsector_energy_total'})
else:
    variables = variables.rename(columns={'16_1_commercial_and_public_services': 'subsector_energy_total'})

variables['log_subsector_energy_total'] = np.log(variables['subsector_energy_total'])
variables['log_GDP'] = np.log(variables['GDP'])
variables['log_Population'] = np.log(variables['Population'])
variables

# Create the plot
plt.figure(figsize=(10, 6))

# Plot each line
plt.plot(variables['year'], variables['subsector_energy_total'], label=subsector_sel, color='blue')
plt.plot(variables['year'], variables['GDP']/10000, label='GDP', color='green')
plt.plot(variables['year'], variables['Population']/100, label='Population', color='red')
plt.plot(variables['year'], variables['urbanization'], label='urbanization', color='orange')
plt.plot(variables['year'], variables['log_subsector_energy_total'], label='logEnergy', color='purple')
plt.plot(variables['year'], variables['log_GDP'], label='logGDP', color='pink')
plt.plot(variables['year'], variables['log_Population'], label='logPopulation', color='grey')

# Add title and labels
plt.title('Variables')
plt.xlabel('Year')
# plt.ylabel('Y-axis label')
plt.xticks(rotation=90)

# Add a legend
plt.legend()

# Show the plot
plt.show()


# Define linear models to test for projection
model_linear1 = ols('subsector_energy_total ~ GDP', data=variables).fit()
model_linear2 = ols('subsector_energy_total ~ GDP + Population', data=variables).fit()
model_linear3 = ols('subsector_energy_total ~ GDP/Population', data=variables).fit()
model_linear4 = ols('subsector_energy_total ~ urbanization', data=variables).fit()
model_linear5 = ols('log_subsector_energy_total ~ log_GDP + log_Population', data=variables).fit()
model_linear6 =ols('subsector_energy_total ~ Population', data=variables).fit()

models = [model_linear1, model_linear2, model_linear3, model_linear4, model_linear5, model_linear6]
adj_r2_scores = [model.rsquared_adj for model in models]
aic_scores = [model.aic for model in models]


# Assess scores to identify best LM for projection
print("Adjusted R-squared scores:", adj_r2_scores)
print("AIC scores:", aic_scores)


# INPUT FORMULA FROM BEST LM HERE
# Train-test split
train, test = train_test_split(variables, test_size=0.25, random_state=42)
# fm = 'log_subsector_energy_total ~ log_GDP + log_Population' ############################################################################## ENSURE FM CORRECT
fm = 'subsector_energy_total ~ Population'
linearRegressor = ols(fm, data=train).fit()

# Predictions
ypredicted_test = linearRegressor.predict(test)
ypredicted_train = linearRegressor.predict(train)

# Performance dataframes
performance_testdf = pd.DataFrame({"y_actual": test["subsector_energy_total"], "y_predicted": np.exp(ypredicted_test)})
performance_traindf = pd.DataFrame({"y_actual": train["subsector_energy_total"], "y_predicted": np.exp(ypredicted_train)})

# Error calculations
performance_testdf["error"] = performance_testdf["y_actual"] - performance_testdf["y_predicted"]
performance_testdf["error_sq"] = performance_testdf["error"] ** 2
performance_traindf["error"] = performance_traindf["y_actual"] - performance_traindf["y_predicted"]
performance_traindf["error_sq"] = performance_traindf["error"] ** 2

# Plot test results
plt.figure(figsize=(10, 6))
plt.scatter(performance_testdf["y_actual"], performance_testdf["y_predicted"], label="Test")
plt.plot([performance_testdf["y_actual"].min(), performance_testdf["y_actual"].max()], 
         [performance_testdf["y_actual"].min(), performance_testdf["y_actual"].max()], color='red')
plt.xlabel("Actual")
plt.ylabel("Predicted")
plt.title("Test Results")
plt.legend()
plt.show()

# Plot training results
plt.figure(figsize=(10, 6))
plt.scatter(performance_traindf["y_actual"], performance_traindf["y_predicted"], label="Train")
plt.plot([performance_traindf["y_actual"].min(), performance_traindf["y_actual"].max()], 
         [performance_traindf["y_actual"].min(), performance_traindf["y_actual"].max()], color='red')
plt.xlabel("Actual")
plt.ylabel("Predicted")
plt.title("Training Results")
plt.legend()
plt.show()

# Error analysis
plt.figure(figsize=(10, 6))
plt.hist(performance_testdf["error"], bins=5)
plt.title("Test Error Analysis")
plt.xlabel("Error")
plt.ylabel("Frequency")
plt.show()

plt.figure(figsize=(10, 6))
plt.hist(performance_traindf["error"], bins=5)
plt.title("Training Error Analysis")
plt.xlabel("Error")
plt.ylabel("Frequency")
plt.show()

# Scatter plots for error trends
plt.figure(figsize=(10, 6))
plt.scatter(performance_traindf["y_actual"], performance_traindf["error"])
plt.title("Training Error Trend")
plt.xlabel("Actual")
plt.ylabel("Error")
plt.show()

plt.figure(figsize=(10, 6))
plt.scatter(performance_testdf["y_actual"], performance_testdf["error"])
plt.title("Test Error Trend")
plt.xlabel("Actual")
plt.ylabel("Error")
plt.show()

# Cross-validation function
def cross_validation(train, k, formula):
    errors = []
    fold_size = len(train) // k
    for i in range(k):
        validation = train.iloc[i * fold_size:(i + 1) * fold_size]
        training = pd.concat([train.iloc[:i * fold_size], train.iloc[(i + 1) * fold_size:]])
        model = ols(formula, data=training).fit()
        predictions = model.predict(validation)
        error = validation["log_subsector_energy_total"] - predictions
        errors.append(np.mean(np.abs(error)))
    return errors

cv_errors = cross_validation(train, 10, fm)
print("Cross-validation errors:", cv_errors)

# Model Forecasting
GDP_df_prediction = GDP_df_filtered[31:81]
Population_df_prediction = Population_df_filtered[31:81]
urbanization_df_prediction = urbanization_df_filtered[31:81]
GDP_df_prediction

# Prepare predictors for forecasting
predictors = GDP_df_prediction.merge(Population_df_prediction, on="year")
predictors['log_GDP'] = np.log(predictors['GDP'])
predictors['log_Population'] = np.log(predictors['Population'])
predictors["GDPpercapita"] = predictors["GDP"] / predictors["Population"] / 10000000
predictors = predictors.merge(urbanization_df_prediction, on="year")
predictors["PopulationRural"] = predictors["Population"] - predictors["Population"] * predictors["urbanization"] / 100
predictors["PopulationUrban"] = predictors["Population"] - predictors["PopulationRural"]
predictors

# Forecasting
# dependent_projected = np.exp(linearRegressor.predict(predictors))
dependent_projected = linearRegressor.predict(predictors)
# dependent_projected
years2 = list(range(2021, 2071))
# years2

# Convert year column to int in eb_df_filtered if necessary
if eb_df_filtered['year'].dtype != 'int':
    eb_df_filtered['year'] = eb_df_filtered['year'].astype(int)


forecast_df = pd.DataFrame(years2, columns=['year'])
# Convert year column to int in forecast_df if necessary
if forecast_df['year'].dtype != 'int':
    forecast_df['year'] = forecast_df['year'].astype(int)
forecast_df['projections'] = dependent_projected
forecast_df
# print("Length of years2:", len(years2))
# print("Length of dependent_projected:", len(dependent_projected))

plt.figure(figsize=(10, 6))
plt.scatter(eb_df_filtered['year'], eb_df_filtered[subsector_sel], label=subsector_sel)
plt.scatter(forecast_df['year'], forecast_df['projections'], label="Projected", color='red')
plt.legend()
plt.xlabel("Year")
plt.ylabel("Energy")
plt.xticks(rotation=90)
plt.title("Energy Forecasting")
plt.show()