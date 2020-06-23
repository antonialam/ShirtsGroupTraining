import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

<<<<<<< HEAD

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
=======
# Some general comments:
# 1. Consider using argparse to make the code more flexible
# 2. Consider using autopep8 to ensure the best readability (PEP8 coding style)
# 3. Consider making the RMSF calculation a function and adding docstrings
# 4. Use if __name__ == '__main__' 
# 5. Make your code able to read in multiple .xvg files and generate multiple 
# plots at one 
# 6. Use numpy methods like np.mean() instead in your RMSF calculation (You 
# might also need np.power and np.sqrt)
# 7. Consider using f string instead of .format()

#Reading the File
f = open('volume.xvg','r')
>>>>>>> ef05c57d575f6275d7a9368c59f8d6473edeaf55
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

plt.plot(x, y, linewidth=0.5)
plt.title(args)
plt.xlabel(args)
plt.ylabel(args)
plt.grid()
<<<<<<< HEAD
# plt.savefig('Simulation_Analysis.png', dpi=600)
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
=======
plt.show()
# Consider using plt.savefig to automatically save the figure here

#Printing Out Statistics
result_str = "Data analysis of the file: volume.xvg"
print(result_str)
print('=' * len(result_str))
>>>>>>> ef05c57d575f6275d7a9368c59f8d6473edeaf55
print("Analyzing the file ...")
print("Plotting and saving figure ...")
print(f"The average of volume (nm^3): {average_volume} (RMSF: {RMSF_rounded}, max: {max_volume}, min: {min_volume})")
print(f"The maximum occurs at {time_of_max_volume} ns while the minimum occurs at {time_of_min_volume} ns.")
print(f"The configuration at {time_of_value_closest_to_Q} ns has the volume {value_closest_to_Q} nm^3 that is closest to the average volume.")
