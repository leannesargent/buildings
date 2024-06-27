# Set the output file type and name
set terminal png
set output 'C:\Users\leanne.sargent\Projects\buildings\results\test_results\plot.png'

# Set plot title and labels
set title "Fuel Consumption Over Time"
set xlabel "Year"
set ylabel "Fuel Consumption"

# Set the style of the lines
set style data lines

# Plot the data
plot 'C:\Users\leanne.sargent\Projects\buildings\data\test_data\plot_testing.csv' using 1:2 title 'GAS', \
     '' using 1:3 title 'DIESEL', \
     '' using 1:4 title 'PEAT', \
     '' using 1:5 title 'ELECTRICITY', \
     '' using 1:6 title 'HYDROGEN'
