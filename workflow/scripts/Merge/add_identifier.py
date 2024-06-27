import pandas as pd

import os
import re


wanted_wd = 'buildings'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)


#read in the file that contains the column of identifier labels to make plotting easier
identifier = pd.read_excel("./data/identifiers/identifier.xlsx")
identifier

#economies minus AUS, CHL, PRC, HKC, NZ, USA which can't use generic identifier file - done below
#economies_full = ('01_AUS', '02_BD', '03_CDA', '04_CHL', '05_PRC', '06_HKC', '07_INA', '08_JPN', '09_ROK', '10_MAS', '11_MEX', '12_NZ', '13_PNG', '14_PE', '15_PHL', '16_RUS', '17_SGP', '18_CT', '19_THA', '20_USA', '21_VN')
economies = ('02_BD', '03_CDA', '07_INA', '08_JPN', '09_ROK', '10_MAS', '11_MEX', '13_PNG', '14_PE', '15_PHL', '16_RUS', '17_SGP', '18_CT', '19_THA', '21_VN')
economies

# russia = [economies_full[15]]
# russia

################### FOR ADJUSTED VALUES #######################################
#   define directory for file input ADJUSTED
input_directory_adjusted = "./results/buildings_merge/adjusted"
#   define output file directory ADJUSTED
output_directory_adjusted = "./results/buildings_merge/adjusted/identifier"

# add identifier column into the 9th position for each economy
for economy in economies:
    file_name_adjusted = os.path.join(input_directory_adjusted, f"{economy}_adjusted.xlsx")
    economy_adjusted = pd.read_excel(file_name_adjusted)
    #economy_adjusted

    position = 9

    #adding identifier column into the adjusted data sheet
    economy_identifier_adjusted = economy_adjusted.iloc[:, :position].join(identifier).join(economy_adjusted.iloc[:, position:])
    #economy_idenfitier

    # define file name for the output files and save to excel
    file_name_identifier_adjusted = os.path.join(output_directory_adjusted, f"{economy}_identifier.xlsx")
    economy_identifier_adjusted.to_excel(file_name_identifier_adjusted, index=False)
##############################################################################
    

################### FOR NON ADJUSTED VALUES #######################################
#   define directory for file input NON ADJUSTED
input_directory_nonadjusted = "./results/buildings_merge/nonadjusted"
#   define output file directory NON ADJUSTED
output_directory_nonadjusted = "./results/buildings_merge/nonadjusted/identifier"

# add identifier column into the 9th position for each economy
for economy in economies:
    file_name_nonadjusted = os.path.join(input_directory_nonadjusted, f"{economy}_nonadjusted.xlsx")
    economy_nonadjusted = pd.read_excel(file_name_nonadjusted)

    position = 9

    #adding identifier column into the adjusted data sheet
    economy_identifier_nonadjusted = economy_nonadjusted.iloc[:, :position].join(identifier).join(economy_nonadjusted.iloc[:, position:])
    #economy_idenfitier

    # define file name for the output files and save to excel
    file_name_identifier_nonadjusted = os.path.join(output_directory_nonadjusted, f"{economy}_identifier.xlsx")
    economy_identifier_nonadjusted.to_excel(file_name_identifier_nonadjusted, index=False)
##############################################################################
    

######### FOR OTHER ECONOMIES ###############
    
# # AUSTRALIA
# identifier_AUS = pd.read_excel("./data/identifiers/identifier_AUS.xlsx")
# economy = '01_AUS'

#     # ADJUSTED
# input_directory_adjusted = "./results/buildings_merge/adjusted"
# output_directory_adjusted = "./results/buildings_merge/adjusted/identifier"

# file_name_adjusted = os.path.join(input_directory_adjusted, f"{economy}_adjusted.xlsx")
# economy_adjusted = pd.read_excel(file_name_adjusted)
# position = 9
# economy_identifier_adjusted = economy_adjusted.iloc[:, :position].join(identifier_AUS).join(economy_adjusted.iloc[:, position:])

# file_name_identifier_adjusted = os.path.join(output_directory_adjusted, f"{economy}_identifier.xlsx")
# economy_identifier_adjusted.to_excel(file_name_identifier_adjusted, index=False)

#     # NONADJUSTED
# input_directory_nonadjusted = "./results/buildings_merge/nonadjusted"
# output_directory_nonadjusted = "./results/buildings_merge/nonadjusted/identifier"

# file_name_nonadjusted = os.path.join(input_directory_nonadjusted, f"{economy}_nonadjusted.xlsx")
# economy_nonadjusted = pd.read_excel(file_name_nonadjusted)
# position = 9
# economy_identifier_nonadjusted = economy_nonadjusted.iloc[:, :position].join(identifier_AUS).join(economy_nonadjusted.iloc[:, position:])

# file_name_identifier_nonadjusted = os.path.join(output_directory_nonadjusted, f"{economy}_identifier.xlsx")
# economy_identifier_nonadjusted.to_excel(file_name_identifier_nonadjusted, index=False)

# # CHILE
# identifier_CHL = pd.read_excel("./data/identifiers/identifier_CHL.xlsx")
# economy = '04_CHL'

#     # ADJUSTED
# input_directory_adjusted = "./results/buildings_merge/adjusted"
# output_directory_adjusted = "./results/buildings_merge/adjusted/identifier"

# file_name_adjusted = os.path.join(input_directory_adjusted, f"{economy}_adjusted.xlsx")
# economy_adjusted = pd.read_excel(file_name_adjusted)
# position = 9
# economy_identifier_adjusted = economy_adjusted.iloc[:, :position].join(identifier_CHL).join(economy_adjusted.iloc[:, position:])

# file_name_identifier_adjusted = os.path.join(output_directory_adjusted, f"{economy}_identifier.xlsx")
# economy_identifier_adjusted.to_excel(file_name_identifier_adjusted, index=False)

#     # NONADJUSTED
# input_directory_nonadjusted = "./results/buildings_merge/nonadjusted"
# output_directory_nonadjusted = "./results/buildings_merge/nonadjusted/identifier"

# file_name_nonadjusted = os.path.join(input_directory_nonadjusted, f"{economy}_nonadjusted.xlsx")
# economy_nonadjusted = pd.read_excel(file_name_nonadjusted)
# position = 9
# economy_identifier_nonadjusted = economy_nonadjusted.iloc[:, :position].join(identifier_CHL).join(economy_nonadjusted.iloc[:, position:])

# file_name_identifier_nonadjusted = os.path.join(output_directory_nonadjusted, f"{economy}_identifier.xlsx")
# economy_identifier_nonadjusted.to_excel(file_name_identifier_nonadjusted, index=False)

# # CHINA
# identifier_PRC = pd.read_excel("./data/identifiers/identifier_PRC.xlsx")
# economy = '05_PRC'

#     # ADJUSTED
# input_directory_adjusted = "./results/buildings_merge/adjusted"
# output_directory_adjusted = "./results/buildings_merge/adjusted/identifier"

# file_name_adjusted = os.path.join(input_directory_adjusted, f"{economy}_adjusted.xlsx")
# economy_adjusted = pd.read_excel(file_name_adjusted)
# position = 9
# economy_identifier_adjusted = economy_adjusted.iloc[:, :position].join(identifier_PRC).join(economy_adjusted.iloc[:, position:])

# file_name_identifier_adjusted = os.path.join(output_directory_adjusted, f"{economy}_identifier.xlsx")
# economy_identifier_adjusted.to_excel(file_name_identifier_adjusted, index=False)

#     # NONADJUSTED
# input_directory_nonadjusted = "./results/buildings_merge/nonadjusted"
# output_directory_nonadjusted = "./results/buildings_merge/nonadjusted/identifier"

# file_name_nonadjusted = os.path.join(input_directory_nonadjusted, f"{economy}_nonadjusted.xlsx")
# economy_nonadjusted = pd.read_excel(file_name_nonadjusted)
# position = 9
# economy_identifier_nonadjusted = economy_nonadjusted.iloc[:, :position].join(identifier_PRC).join(economy_nonadjusted.iloc[:, position:])

# file_name_identifier_nonadjusted = os.path.join(output_directory_nonadjusted, f"{economy}_identifier.xlsx")
# economy_identifier_nonadjusted.to_excel(file_name_identifier_nonadjusted, index=False)

# # HONG KONG CHINA
# identifier_HKC = pd.read_excel("./data/identifiers/identifier_HKC.xlsx")
# economy = '06_HKC'

#     # ADJUSTED
# input_directory_adjusted = "./results/buildings_merge/adjusted"
# output_directory_adjusted = "./results/buildings_merge/adjusted/identifier"

# file_name_adjusted = os.path.join(input_directory_adjusted, f"{economy}_adjusted.xlsx")
# economy_adjusted = pd.read_excel(file_name_adjusted)
# position = 9
# economy_identifier_adjusted = economy_adjusted.iloc[:, :position].join(identifier_HKC).join(economy_adjusted.iloc[:, position:])

# file_name_identifier_adjusted = os.path.join(output_directory_adjusted, f"{economy}_identifier.xlsx")
# economy_identifier_adjusted.to_excel(file_name_identifier_adjusted, index=False)

#     # NONADJUSTED
# input_directory_nonadjusted = "./results/buildings_merge/nonadjusted"
# output_directory_nonadjusted = "./results/buildings_merge/nonadjusted/identifier"

# file_name_nonadjusted = os.path.join(input_directory_nonadjusted, f"{economy}_nonadjusted.xlsx")
# economy_nonadjusted = pd.read_excel(file_name_nonadjusted)
# position = 9
# economy_identifier_nonadjusted = economy_nonadjusted.iloc[:, :position].join(identifier_HKC).join(economy_nonadjusted.iloc[:, position:])

# file_name_identifier_nonadjusted = os.path.join(output_directory_nonadjusted, f"{economy}_identifier.xlsx")
# economy_identifier_nonadjusted.to_excel(file_name_identifier_nonadjusted, index=False)

# # NEW ZEALAND
# identifier_NZ = pd.read_excel("./data/identifiers/identifier_NZ.xlsx")
# economy = '12_NZ'

#     # ADJUSTED
# input_directory_adjusted = "./results/buildings_merge/adjusted"
# output_directory_adjusted = "./results/buildings_merge/adjusted/identifier"

# file_name_adjusted = os.path.join(input_directory_adjusted, f"{economy}_adjusted.xlsx")
# economy_adjusted = pd.read_excel(file_name_adjusted)
# position = 9
# economy_identifier_adjusted = economy_adjusted.iloc[:, :position].join(identifier_NZ).join(economy_adjusted.iloc[:, position:])

# file_name_identifier_adjusted = os.path.join(output_directory_adjusted, f"{economy}_identifier.xlsx")
# economy_identifier_adjusted.to_excel(file_name_identifier_adjusted, index=False)

#     # NONADJUSTED
# input_directory_nonadjusted = "./results/buildings_merge/nonadjusted"
# output_directory_nonadjusted = "./results/buildings_merge/nonadjusted/identifier"

# file_name_nonadjusted = os.path.join(input_directory_nonadjusted, f"{economy}_nonadjusted.xlsx")
# economy_nonadjusted = pd.read_excel(file_name_nonadjusted)
# position = 9
# economy_identifier_nonadjusted = economy_nonadjusted.iloc[:, :position].join(identifier_NZ).join(economy_nonadjusted.iloc[:, position:])

# file_name_identifier_nonadjusted = os.path.join(output_directory_nonadjusted, f"{economy}_identifier.xlsx")
# economy_identifier_nonadjusted.to_excel(file_name_identifier_nonadjusted, index=False)

# # UNITED STATES
# identifier_USA = pd.read_excel("./data/identifiers/identifier_USA.xlsx")
# economy = '20_USA'

#     # ADJUSTED
# input_directory_adjusted = "./results/buildings_merge/adjusted"
# output_directory_adjusted = "./results/buildings_merge/adjusted/identifier"

# file_name_adjusted = os.path.join(input_directory_adjusted, f"{economy}_adjusted.xlsx")
# economy_adjusted = pd.read_excel(file_name_adjusted)
# position = 9
# economy_identifier_adjusted = economy_adjusted.iloc[:, :position].join(identifier_USA).join(economy_adjusted.iloc[:, position:])

# file_name_identifier_adjusted = os.path.join(output_directory_adjusted, f"{economy}_identifier.xlsx")
# economy_identifier_adjusted.to_excel(file_name_identifier_adjusted, index=False)

#     # NONADJUSTED
# input_directory_nonadjusted = "./results/buildings_merge/nonadjusted"
# output_directory_nonadjusted = "./results/buildings_merge/nonadjusted/identifier"

# file_name_nonadjusted = os.path.join(input_directory_nonadjusted, f"{economy}_nonadjusted.xlsx")
# economy_nonadjusted = pd.read_excel(file_name_nonadjusted)
# position = 9
# economy_identifier_nonadjusted = economy_nonadjusted.iloc[:, :position].join(identifier_USA).join(economy_nonadjusted.iloc[:, position:])

# file_name_identifier_nonadjusted = os.path.join(output_directory_nonadjusted, f"{economy}_identifier.xlsx")
# economy_identifier_nonadjusted.to_excel(file_name_identifier_nonadjusted, index=False)