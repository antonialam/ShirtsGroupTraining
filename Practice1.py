import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc


# Making the code more flexible
def initialize():

    parser = argparse.ArgumentParser(
        description='Plot volume as a function of time')
    parser.add_argument('-file',
                        '--xvg',
                        help='The name of the file being analyzed.')
    parser.add_argument('-t',
                        '--title',
                        help='The title of the plot.')
    parser.add_argument('-x',
                        '--xlabel',
                        help='The label and units of the x-axis.')
    parser.add_argument('-y',
                        '--ylabel',
                        help='The label and units of the y-axis.')

    args_parse = parser.parse_args()

    return args_parse


args = initialize()

# Reading the file
f = open(args.xvg, 'r')
lines = f.readlines()
f.close()

# Extracting data from the file
x, y = [], []
for line in lines:
    if line[0] != '#' and line[0] != '@':
        x.append(float(line.split()[0]))
        y.append(float(line.split()[1]))

# Executing the RMSF equation
Q = np.mean(y)  # <Q>
Q2 = np.mean(np.power(y, 2))  # <Q^2>
RMSF = ((Q2 - (Q ** 2)) ** 0.5) / Q

# Graphing the plot
rc('font', **{
    'family': 'sans-serif',
    'sans-serif': ['DejaVu Sans'],
    'size': 10})
rc('mathtext', **{'default': 'regular'})
plt.rc('font', family='serif')

plt.plot(x, y, linewidth=0.75)
plt.title(args)
plt.xlabel(args)
plt.ylabel(args)
plt.grid()
plt.savefig('Simulation_Analysis.png', dpi=600)
# plt.show()

# Important values
average_volume = round(Q, 3)
RMSF_rounded = round(RMSF, 3)
max_volume = round(max(y), 3)
min_volume = round(min(y), 3)
time_of_max_volume = round(x[y.index(max(y))]/1000, 4)
time_of_min_volume = round(x[y.index(min(y))]/1000, 4)
time_of_value_closest_to_Q = round(x[y.index(min(y, key=lambda x: abs(x-Q)))]/1000, 3)
value_closest_to_Q = round(min(y, key=lambda x: abs(x-Q)), 6)

# Printing out statistics
print("Data analysis of the file: volume.xvg")
print("=====================================")
print("Analyzing the file ...")
print("Plotting and saving figure ...")
print(f"The average of volume (nm^3): {average_volume} (RMSF: {RMSF_rounded}, max: {max_volume}, min: {min_volume})")
print(f"The maximum occurs at {time_of_max_volume} ns while the minimum occurs at {time_of_min_volume} ns.")
print(f"The configuration at {time_of_value_closest_to_Q} ns has the volume {value_closest_to_Q} nm^3 that is closest to the average volume.")
