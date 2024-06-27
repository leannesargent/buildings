import pandas as pd
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "plotly_mimetype"
import plotly.graph_objects as go
import plotly.subplots as sp

import kaleido

import datetime
current_date = datetime.datetime.now().strftime("%Y_%m_%d")
# current_date

import os
import re


wanted_wd = 'buildings'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

economies = ['01_AUS', '02_BD', '03_CDA', '04_CHL', '05_PRC', '06_HKC', '07_INA', '08_JPN', '09_ROK', '10_MAS', '11_MEX', '12_NZ', '13_PNG', '14_PE', '15_PHL', '16_RUS', '17_SGP', '18_CT', '19_THA', '20_USA', '21_VN']
economies


#   define input and output directories for adjusted data
#   SELECT EITHER INPUT/OUTPUT FOR ADJUSTED OR NON ADJUSTED RESULTS
#   ALSO MUST CHANGE OUTPUT FILE NAME AT BOTTOM OF CODE FOR ADJUSTED OR NONADJUSTED
    # adjusted
input_directory = "./results/buildings_merge/adjusted/identifier"
# output_directory = "./results/buildings_merge/adjusted/plots"

# OUTPUT FOR 1X2 CHARTS SEPARATED BY SRV VS. RES
output_directory = "./results/buildings_merge/adjusted/plots/charts"

    # non adjusted
# input_directory = "./results/buildings_merge/nonadjusted/identifier"
# output_directory = "./results/buildings_merge/nonadjusted/plots"


# generate plots for each economy
# perform for a single economy by redefining economies variable above
# for economy in economies:

# select only economies not yet completed for buildings modelling
economies_save = economies[0:2] + [economies[3]] + economies [5:7] + economies[8:17] + [economies[20]]
#economies_save = economies[15]
economies_save

russia = [economies[15]]
russia

for economy in economies_save:
#for economy in russia:
        #  READ IN COMMAND FOR ADJUSTED RESULTS
    file_name = os.path.join(input_directory, f"{economy}_identifier.xlsx")
    economy_data = pd.read_excel(file_name)
    #economy_data

    # subset each economy into residential (res) and commerical and public services (srv) for reference case (ref) and target case (tgt)
    economy_ref_res = economy_data[(economy_data['scenarios'] == 'reference') & (economy_data['sub2sectors'] == '16_01_02_residential')]
    economy_ref_srv = economy_data[(economy_data['scenarios'] == 'reference') & (economy_data['sub2sectors'] == '16_01_01_commercial_and_public_services')]

    economy_tgt_res = economy_data[(economy_data['scenarios'] == 'target') & (economy_data['sub2sectors'] == '16_01_02_residential')]
    economy_tgt_srv = economy_data[(economy_data['scenarios'] == 'target') & (economy_data['sub2sectors'] == '16_01_01_commercial_and_public_services')]

    ####################### REFERENCE ################################
        # RESIDENTIAL
    # reorder column wise data into row wise for processing
    melted_economy_ref_res = economy_ref_res.melt(id_vars=['scenarios', 'economy', 'sectors', 'sub1sectors', 'sub2sectors', 'sub3sectors', 'sub4sectors', 'fuels', 'subfuels', 'identifier', 'is_subtotal'], var_name='Year', value_name='Fuel Consumption')
    melted_economy_ref_res['Year'] = melted_economy_ref_res['Year'].astype(str)

    #generate figure
    fig_ref_res = px.line(melted_economy_ref_res, x='Year', y='Fuel Consumption', color='identifier', line_group='fuels', labels={'Year': 'Year', 'Fuel Consumption': 'Fuel Consumption'}, title='Reference, Residential', line_shape='spline')
    fig_ref_res.add_trace(go.Scatter(x=[2021, 2021], y=[melted_economy_ref_res['Fuel Consumption'].min(), melted_economy_ref_res['Fuel Consumption'].max()], mode='lines', name='Historical cutoff, 2021', line=dict(color='gray', width=1, dash='dash'), showlegend=False))
    fig_ref_res.update_layout(xaxis=dict(showgrid=False), yaxis=dict(gridcolor='lightgray'), width=1000, height=800, showlegend=True, legend=dict(font=dict(size=10)), plot_bgcolor='white')
    #fig_ref_res.show()


        #  COMMERCIAL AND PUBLIC SERVICES
    # reorder column wise data into row wise for processing
    melted_economy_ref_srv = economy_ref_srv.melt(id_vars=['scenarios', 'economy', 'sectors', 'sub1sectors', 'sub2sectors', 'sub3sectors', 'sub4sectors', 'fuels', 'subfuels', 'identifier', 'is_subtotal'], var_name='Year', value_name='Fuel Consumption')
    melted_economy_ref_srv['Year'] = melted_economy_ref_srv['Year'].astype(str)
   
    #generate figure
    fig_ref_srv = px.line(melted_economy_ref_srv, x='Year', y='Fuel Consumption', color='identifier', line_group='fuels', labels={'Year': 'Year', 'Fuel Consumption': 'Fuel Consumption'}, title='Reference, Commercial and Public Services', line_shape='spline')
    fig_ref_srv.add_trace(go.Scatter(x=[2021, 2021], y=[melted_economy_ref_srv['Fuel Consumption'].min(), melted_economy_ref_srv['Fuel Consumption'].max()], mode='lines', name='Historical cutoff, 2021', line=dict(color='gray', width=1, dash='dash'), showlegend=False))
    fig_ref_srv.update_layout(xaxis=dict(showgrid=False), yaxis=dict(gridcolor='lightgray'), width=1000, height=800, showlegend=True, legend=dict(font=dict(size=10)), plot_bgcolor='white')
    #fig_ref_srv.show()


    ####################### TARGET ################################
        # RESIDENTIAL
    # reorder column wise data into row wise for processing
    melted_economy_tgt_res = economy_tgt_res.melt(id_vars=['scenarios', 'economy', 'sectors', 'sub1sectors', 'sub2sectors', 'sub3sectors', 'sub4sectors', 'fuels', 'subfuels', 'identifier', 'is_subtotal'], var_name='Year', value_name='Fuel Consumption')
    melted_economy_tgt_res['Year'] = melted_economy_tgt_res['Year'].astype(str)
  
    #generate figure
    fig_tgt_res = px.line(melted_economy_tgt_res, x='Year', y='Fuel Consumption', color='identifier', line_group='fuels', labels={'Year': 'Year', 'Fuel Consumption': 'Fuel Consumption'}, title='Target, Residential', line_shape='spline')
    fig_tgt_res.add_trace(go.Scatter(x=[2021, 2021], y=[melted_economy_tgt_res['Fuel Consumption'].min(), melted_economy_tgt_res['Fuel Consumption'].max()], mode='lines', name='Historical cutoff, 2021', line=dict(color='gray', width=1, dash='dash'), showlegend=False))
    fig_tgt_res.update_layout(xaxis=dict(showgrid=False), yaxis=dict(gridcolor='lightgray'), width=1000, height=800, showlegend=True, legend=dict(font=dict(size=10)), plot_bgcolor='white')
    #fig_tgt_res.show()


        #  COMMERCIAL AND PUBLIC SERVICES
    # reorder column wise data into row wise for processing
    melted_economy_tgt_srv = economy_tgt_srv.melt(id_vars=['scenarios', 'economy', 'sectors', 'sub1sectors', 'sub2sectors', 'sub3sectors', 'sub4sectors', 'fuels', 'subfuels', 'identifier', 'is_subtotal'], var_name='Year', value_name='Fuel Consumption')
    melted_economy_tgt_srv['Year'] = melted_economy_tgt_srv['Year'].astype(str)
  
    #generate figure
    fig_tgt_srv = px.line(melted_economy_tgt_srv, x='Year', y='Fuel Consumption', color='identifier', line_group='fuels', labels={'Year': 'Year', 'Fuel Consumption': 'Fuel Consumption'}, title='Target, Commercial and Public Services', line_shape='spline')
    fig_tgt_srv.add_trace(go.Scatter(x=[2021, 2021], y=[melted_economy_tgt_srv['Fuel Consumption'].min(), melted_economy_ref_srv['Fuel Consumption'].max()], mode='lines', name='Historical cutoff, 2021', line=dict(color='gray', width=1, dash='dash'), showlegend=False))
    fig_tgt_srv.update_layout(xaxis=dict(showgrid=False), yaxis=dict(gridcolor='lightgray'), width=1000, height=800, showlegend=True, legend=dict(font=dict(size=10)), plot_bgcolor='white')
    #fig_tgt_srv.show()

    ##################### COMBINING PLOTS ##########################

    # generate placeholder for a set of 4 figures organized into 2 rows and 2 columnns, with the given figure title names
#     economy_figures = sp.make_subplots(rows=2, cols=2, subplot_titles=("REF, Residential",  "TGT, Residential", "REF, Commercial and Public Services", "TGT, Commerical and Public Services"))

#     # Add all traces from each plot to the combined figure
#     # add each figure to the desired row/col location in the combined plots
#     for trace in fig_ref_res['data']:
#         economy_figures.add_trace(trace, row=1, col=1)

#     for trace in fig_tgt_res['data']:
#         economy_figures.add_trace(trace, row=1, col=2)

#     for trace in fig_ref_srv['data']:
#         economy_figures.add_trace(trace, row=2, col=1)

#     for trace in fig_tgt_srv['data']:
#         economy_figures.add_trace(trace, row=2, col=2)

#     # plots don't have usable shared legend possibility, so omit legend
#     economy_figures.update_traces(showlegend=False, row=1, col=1)
#     economy_figures.update_traces(showlegend=False, row=1, col=2)
#     economy_figures.update_traces(showlegend=False, row=2, col=1)
#     economy_figures.update_traces(showlegend=False, row=2, col=2)

#     # show grid for y axis, colour light gray
#     economy_figures.update_yaxes(showgrid=True, gridcolor='lightgray', row=1, col=1)
#     economy_figures.update_yaxes(showgrid=True, gridcolor='lightgray', row=1, col=2)
#     economy_figures.update_yaxes(showgrid=True, gridcolor='lightgray', row=2, col=1)
#     economy_figures.update_yaxes(showgrid=True, gridcolor='lightgray', row=2, col=2)

#    # change size of combined figure
#     economy_figures.update_layout(width=1400, height=1100, plot_bgcolor='white')

    #economy_figures.show()


    ########### EXPORTING FIGURES ###################

    # ######## FOR ADJUSTED ##############
    # # to APERC files
    # save_directory = f"C:/Users/leanne.sargent/APERC/Outlook-9th - Modelling/Integration/{economy}/01_Demand/01_01_Buildings/charts/"
    # if not os.path.isdir(save_directory):
    #     os.makedirs(save_directory)
 
    # file_name = os.path.join(save_directory, f"{economy}_2021adjusted_srv_and_res_{current_date}.html")
    # pio.write_html(economy_figures, file_name)
  #  # to personal files
    # combined_image_file_name = os.path.join(output_directory, f"{economy}_plots_adjusted.html")
    # pio.write_html(economy_figures, combined_image_file_name)

    ######### FOR NON ADJUSTED ##############
    # combined_image_file_name = os.path.join(output_directory, f"{economy}_plots_nonadjusted.html")
    # pio.write_html(economy_figures, combined_image_file_name)

# ############# COMMERICAL AND PUBLIC SERVICES PLOTS ######################   

#     economy_figures_srv = sp.make_subplots(rows=2, cols=1, subplot_titles=("REF, Commercial and Public Services", "TGT, Commerical and Public Services"))

#     # Add all traces from each plot to the combined figure
#     # add each figure to the desired row/col location in the combined plots

#     for trace in fig_ref_srv['data']:
#         economy_figures_srv.add_trace(trace, row=1, col=1)

#     for trace in fig_tgt_srv['data']:
#         economy_figures_srv.add_trace(trace, row=2, col=1)

#     # plots don't have usable shared legend possibility, so omit legend
#     economy_figures_srv.update_traces(showlegend=True, row=1, col=1)
#     economy_figures_srv.update_traces(showlegend=False, row=2, col=1)

#     # show grid for y axis, colour light gray
#     economy_figures_srv.update_yaxes(showgrid=True, gridcolor='lightgray', row=1, col=1)
#     economy_figures_srv.update_yaxes(showgrid=True, gridcolor='lightgray', row=2, col=1)

#     # change size of combined figure
#     economy_figures_srv.update_layout(width=1400, height=1100, plot_bgcolor='white')

#     # # save to personal
#     # combined_image_file_name_srv = os.path.join(output_directory, f"{economy}_plots_srv.html")
#     # pio.write_html(economy_figures_srv, combined_image_file_name_srv)

#         # save to APERC files
#     save_directory = f"C:/Users/leanne.sargent/APERC/Outlook-9th - Modelling/Integration/{economy}/01_Demand/01_01_Buildings/charts/"
#     if not os.path.isdir(save_directory):
#         os.makedirs(save_directory)
 
#     # file_name = os.path.join(save_directory, f"{economy}_2021adjusted_services_{current_date}.html")
#     #pio.write_html(economy_figures_srv, file_name)
#     file_name = os.path.join(save_directory, f"{economy}_2021adjusted_services_{current_date}.png")
#     economy_figures_srv.write_image(file_name, engine='kaleido')

############# RESIDENTIAL PLOTS ######################  

    economy_figures_res = sp.make_subplots(rows=2, cols=1, subplot_titles=("REF, Residential",  "TGT, Residential"))

    for trace in fig_ref_res['data']:
        economy_figures_res.add_trace(trace, row=1, col=1)

    for trace in fig_tgt_res['data']:
        economy_figures_res.add_trace(trace, row=2, col=1)

    economy_figures_res.update_traces(showlegend=True, row=1, col=1)
    economy_figures_res.update_traces(showlegend=False, row=2, col=1)

    economy_figures_res.update_yaxes(showgrid=True, gridcolor='lightgray', row=1, col=1)
    economy_figures_res.update_yaxes(showgrid=True, gridcolor='lightgray', row=2, col=1)
    
    # change size of combined figure
    economy_figures_res.update_layout(width=1400, height=1100, plot_bgcolor='white')

    # # save to personal files
    # combined_image_file_name_res = os.path.join(output_directory, f"{economy}_plots_res.html")
    # pio.write_html(economy_figures_res, combined_image_file_name_res)

    # save to APERC files
    save_directory = f"C:/Users/leanne.sargent/APERC/Outlook-9th - Modelling/Integration/{economy}/01_Demand/01_01_Buildings/charts/"
    if not os.path.isdir(save_directory):
        os.makedirs(save_directory)
 
    # file_name = os.path.join(save_directory, f"{economy}_2021adjusted_residential_{current_date}.html")
    # pio.write_html(economy_figures_res, file_name)
    
    file_name = os.path.join(save_directory, f"{economy}_2021adjusted_residential_{current_date}.png")
    economy_figures_res.write_image(file_name, engine='kaleido')
