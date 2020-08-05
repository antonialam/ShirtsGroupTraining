import time
from itertools import combinations
import numpy as np
import math
from astropy import k_B
from matplotlib import rc
import matplotlib.pyplot as plt


def initialize():

    parser = argparse.ArgumentParser(
        description='Carry out the Metropolis-Hastings algorithm')
    parser.add_argument('-p',
                        '--particles',
                        help='The number of particles in the simulation box.')
    parser.add_argument('-l',
                        '--box_length',
                        help='The length of the side of the simulation box.')
    parser.add_argument('-d',
                        '--max_displacement',
                        help='The maximum distance a particle can travel in one direction.')
    parser.add_argument('-t',
                        '--temperature',
                        help='The temperature of the system.')

    args_parse = parser.parse_args()
    return args_parse

class Initialization:
    def __init__(self, params_file): 
        with open(params_file) as file:
            params = yaml.load(file, Loader=yaml.FullLoader) 
            self.N_particles = params['num_particles']
            self.rho = params['density']
            self.N_steps = params['num_steps']
            self.d_max = params['d_max']
            self.epsilon = params['epsilon']
            self.sigma = params['sigma']
            self.dim = params['dim']

            self.box_length = (self.N_particles / self.rho) ** (1 / self.dim)

    def initialize_coordinates(self):
        return (np.random.rand(self.N_particles, self.dim) - 0.5) * self.box_length


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


def truncated_lennard_jones(coord_a, coord_b, box_length, particles, epsilon=1, sigma=1):
    """
        Parameters:
            coord_a (list): The 3-dimensional coordinates of a particle.
            coord_b (list): The 3-dimensional coordinates of another particle.
            box_length (float): The length of the side of the simulation box.
       Returns:
            potential (float): Uses the calc_distance function to return the Lennard-Jones potential between two particles.
    """
    distance = calc_distance(coord_a, coord_b, box_length)
    rc = 2.5 * sigma
    potential = 4 * epsilon * (((sigma/distance)**12) - ((sigma/distance)**6))
    rc_potential = 4 * epsilon * (((sigma/rc)**12) - ((sigma/rc)**6))
    if distance <= rc:
        truncated_potential = potential - rc_potential
    else:
        truncated_potential = 0
    tail = ((8 * math.pi * (particles**2)) / (3 * potential) * epsilon * sigma**3) * ((((sigma/rc)**9) - ((sigma/rc)**3)) / 3)
    total_potential = truncated_potential + tail
    return total_potential


def calc_sys_potential(particles, coordinates, box_length):
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
        total += truncated_lennard_jones(coordinates[i[0] - 1], coordinates[i[1] - 1], box_length, particles)
    return total


particles = args.particles
box_length = args.box_length
max_displacement = args.max_displacement
temp = args.temperature

initial_position = initialize_particles(particles, box_length)
new_position = initial_position.copy()
for i in range(1, 500001):
    random_particle = np.random.randint(0, particles)
    new_coordinate = new_position[random_particle] + ((np.random.rand(1, 3) - 0.5) * 2 * max_displacement)
    new_position[random_particle, :] = new_coordinate
    initial_energy = calc_sys_potential(particles, initial_position, box_length)
    new_energy = calc_sys_potential(particles, new_position, box_length)
    energy_diff = new_energy - initial_energy
    prob_acc = np.exp(-(1 / (k_B * temp)) * energy_diff)
    if energy_diff < 0:
        initial_position = new_position
        initial_energy = new_energy
    else:
        if np.random.rand() <= prob_acc:
            initial_position = new_position
            initial_energy = new_energy
        else:
            initial_position = initial_position

if __name__ == "__main__":

    # Graphing the time elapsed calculating energy as a function of the number of particles
    particle_num = []
    time_y = []
    for num in range(2, 101):
        random_coordinates = initialize_particles(num, 5)
        t1 = time.time()
        total_energy = calc_sys_potential(num, random_coordinates, 5)
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
    plt.hist(y, bins=500)
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


