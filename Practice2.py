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
                        nargs='+',
                        help='The name of the file being analyzed.')
    parser.add_argument('-n',
                        '--nvars',
                        default=1,
                        help='The number of dependent variables. This flag allows \
                            for different columns to be plotted along the \
                            y_axis.')
    parser.add_argument('-t',
                        '--title',
                        help='The title of the plot.')
    parser.add_argument('-x',
                        '--xlabel',
                        help='The label and units of the x-axis.')
    parser.add_argument('-y',
                        '--ylabel',
                        help='The label and units of the y-axis.')
    parser.add_argument('-l',
                        '--legend',
                        nargs='+',
                        help='This allows the user to specify the legend of the plot.')
    parser.add_argument('-s',
                        '--save',
                        help='This specifies what the plot should be saved as.')
    parser.add_argument('-m',
                        choices=['single', 'multiple'],
                        help='Whether to plot the data in multiple figures or just one figures \
                            if multiple files are given.')

    args_parse = parser.parse_args()

    if args_parse.save is None:   # if args_parse.save is not specified
        args_parse.save = [args_parse.xvg[i].split('.')[0] + '.png' for i in range(len(args_parse.xvg))]

    return args_parse


if __name__ == "__main__":
    args = initialize()

    # Reading the file
    for file in args.xvg:
        f = open(file, 'r')
        lines = f.readlines()
        f.close()

    # Extracting data from the file
        x = []
        y = []
        for i in range(int(args.nvars)):
            y.append([])

        for line in lines:
            if line[0] != '#' and line[0] != '@':
                x.append(float(line.split()[0]))
                for i in range(int(args.nvars)):
                    y[i].append(float(line.split()[i + 1]))

    # Executing the RMSF equation
        Q = np.mean(y)  # <Q>
        Q2 = np.mean(np.power(y[0], 2))  # <Q^2>
        RMSF = ((Q2 - (Q ** 2)) ** 0.5) / Q

    # Customizing the font of the plot
        rc('font', **{
            'family': 'sans-serif',
            'sans-serif': ['DejaVu Sans'],
            'size': 10})
        rc('mathtext', **{'default': 'regular'})
        plt.rc('font', family='serif')

    # Graphing the plot (one file given)
        for i in range(int(args.nvars)):
            if args.legend is None:
                plt.plot(x, y[i], linewidth=0.5)
            else:
                plt.plot(x, y[i], linewidth=0.5, label=args.legend[i])
        plt.title(args.title)
        plt.xlabel(args.xlabel)
        plt.ylabel(args.ylabel)
        plt.grid()
        if args.legend is not None:
            plt.legend()
        plt.savefig(args.save[0], dpi=600)
        # plt.show()

    # Important values
        average_volume = Q
        RMSF_rounded = RMSF
        max_volume = max(y[0])
        min_volume = min(y[0])
        time_of_max_volume = x[y[0].index(max(y[0]))]/1000
        time_of_min_volume = x[y[0].index(min(y[0]))]/1000
        time_of_value_closest_to_Q = x[y[0].index(min(y[0], key=lambda x: abs(x-Q)))]/1000
        value_closest_to_Q = min(y[0], key=lambda x: abs(x-Q))

    # Printing out statistics
        result_str = "\nData analysis of the file: " + "".join((args.xvg))
        print(result_str)
        print("=" * len(result_str))  # consider using this instead
        print("Analyzing the file ...")
        print("Plotting and saving figure ...")
        print(f'The average of volume (nm^3):{average_volume: .3f} (RMSF:{RMSF_rounded: .3f}, max:{max_volume: .3f}, min:{min_volume: .3f})')
        print(f'The maximum occurs at{time_of_max_volume: .4f} ns while the minimum occurs at{time_of_min_volume: .4f} ns.')
        print(f'The configuration at{time_of_value_closest_to_Q: .3f} ns has the volume{value_closest_to_Q: .6f} nm^3 that is closest to the average volume.')
