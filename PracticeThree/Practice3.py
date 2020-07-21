import time
from itertools import combinations
import numpy as np
from matplotlib import rc
import matplotlib.pyplot as plt
import yaml


def initialize_particles(particles, box_length):
    """
    Parameters:
        particles (int): The number of particles in the simulation box.
        box_length (float): The length of the side of the simulation box.
    Returns:
        The random 3-dimensional coordinates of each particle.
    """
    return (np.random.rand(particles, 3) - 0.5) * box_length


def calc_distance(coord_a, coord_b, box_length):
    """
       Parameters:
           coord_a (list): The 3-dimensional coordinates of a particle.
           coord_b (list): The 3-dimensional coordinates of another particle.
           box_length (float): The length of the side of the simulation box.
       Returns:
           distance (float): The distance between two particles with the consideration of periodic boundary conditions (PBCs).
    """
    r = np.array(coord_a) - np.array(coord_b)
    r = r - box_length * np.round(r / box_length)
    distance = np.linalg.norm(r)
    return distance


def lennard_jones(coord_a, coord_b, box_length, epsilon=1, sigma=1):
    """
        Parameters:
            coord_a (list): The 3-dimensional coordinates of a particle.
            coord_b (list): The 3-dimensional coordinates of another particle.
            box_length (float): The length of the side of the simulation box.
       Returns:
            potential (float): Uses the calc_distance function to return the Lennard-Jones potential between two particles.
    """
    distance = calc_distance(coord_a, coord_b, box_length)
    potential = 4 * epsilon * \
        ((sigma / (distance**12)) - (sigma / (distance**6)))
    return potential


def calc_sys_potential(particles, coordinates, box_length, sigma=1, epsilon=1):
    """
       Parameters:
           particles (int): The number of particles in the simulation box.
           coordinates (array): The coordinates of all of the particles in the simulation box.
           box_length (float): The length of the side of the simulation box.
       Returns:
           The random 3-dimensional coordinates of each particle.
       """
    total = 0
    for i in combinations(list(range(1, particles + 1)), 2):
        total += lennard_jones(coordinates[i[0] - 1], coordinates[i[1] - 1], box_length, sigma, epsilon)
    return total


if __name__ == "__main__":

    print('Reading in simulation parameters')
    with open('MC_parameters.yml') as ymlfile:
        params = yaml.load(ymlfile, Loader=yaml.FullLoader)

    # Graphing the time elapsed calculating energy as a function of the number of particles
    particle_num = []
    time_y = []

    box_length = (params['num_particles'] / params['density']) ** (1 / params['dim'])

    for num in range(2, params['num_particles'] + 1):
        random_coordinates = initialize_particles(num, box_length)
        t1 = time.time()
        total_energy = calc_sys_potential(num, random_coordinates, box_length, sigma=params['sigma'], epsilon=params['epsilon'])
        t2 = time. time()
        elapsed_time = t2 - t1
        particle_num.append(num)
        time_y.append(elapsed_time)

    rc('font', **{
        'family': 'sans-serif',
        'sans-serif': ['DejaVu Sans'],
        'size': 10})
    rc('mathtext', **{'default': 'regular'})
    plt.rc('font', family='serif')

    plt.title("Time Elapsed Calculating Energy as a Function of the Number of Particles")
    plt.xlabel("Number of Particles")
    plt.ylabel("Time Elapsed Calculating Energy (sec)")
    plt.grid()
    plt.plot(particle_num, time_y, linewidth=0.8)
    plt.show()


    # Graphing histogram of total energy frequencies
    y = []
    for num in range(1, 1001):
        random_coordinates = initialize_particles(100, 5)
        total_energy = calc_sys_potential(100, random_coordinates, 5)
        y.append(total_energy)

    plt.title("Distribution of Total Energy")
    plt.xlabel("Total Energy (J)")
    plt.ylabel("Number of Trials")
    plt.grid()
    plt.hist(y, bins=1000)
    plt.show()

    # Important variables
    average = np.mean(y)
    med = (y[499] + y[500]) / 2
    max = max(y)
    min = min(y)
    std = np.std(y)

    # Print statistics
    result_str = "Data analysis of the file"
    print(result_str)
    print("=" * len(result_str))
    print("Analyzing the file ...")
    print("Plotting and saving figure ...")
    print(f"Average: {average:.3e} J\nMedian: {med:.3e} J")
    print(f"Max: {max:.3e} J    Min: {min:.3e} J")
    print(f"Std Dev: {std:.3e} J")