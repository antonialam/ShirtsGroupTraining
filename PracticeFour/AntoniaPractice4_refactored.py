from itertools import combinations
import numpy as np
import math
import yaml
from tqdm.auto import tqdm
#from scipy.constants import k
from matplotlib import rc
import matplotlib.pyplot as plt

class Initialization:
    def __init__(self, YAML):
        print("Reading in simulation parameters")
        with open(YAML) as ymlfile:
        params = yaml.load(ymlfile, Loader=yaml.FullLoader)
        self.sigma = param['sigma']
        self.epsilon = param['epsilon']
        self.N_particles = param['num_particles']
        self.rho = param['density']
        self.d_max = param['d_max']
        self.dim = param['dim']
        self.temp = param['temp']

        self.box_length = (self.N_particles / self.rho) ** (1 / self.dim)
    
    def initiliaze_particle(self): 
        """
        Parameters:
            particles (int): The number of particles in the simulation box.
            box_length (float): The length of the side of the simulation box.
        Returns:
            The random 3-dimensional coordinates of each particle.
        """
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
    rc -= box_length * np.round(rc / box_length)
    potential = 4 * epsilon * (((sigma/distance)**12) - ((sigma/distance)**6))
    rc_potential = 4 * epsilon * (((sigma/rc)**12) - ((sigma/rc)**6))
    if distance <= rc:
        truncated_potential = potential - rc_potential
    else:
        truncated_potential = 0
    volume = box_length ** 3
    tail = ((8 * math.pi * (particles**2)) / (3 * volume) * epsilon * sigma**3) * ((((sigma/rc)**9) - ((sigma/rc)**3)) / 3)
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


if __name__ == "__main__":

    


box_length = (params['num_particles'] / params['density']) ** (1 / params['dim'])
initial_position = initialize_particles(params['num_particles'], box_length)
initial_energy = calc_sys_potential(params['num_particles'], initial_position, box_length)
new_position = initial_position.copy()
steps = []
energy = []
prob_acc_list = []

for step in tqdm(range(1, params['num_steps'] + 1)):
    steps.append(step)
    energy.append(initial_energy)
    random_particle = np.random.randint(0, params['num_particles'])
    new_coordinate = initial_position[random_particle] + ((np.random.rand(1, 3) - 0.5) * 2 * params['d_max'])
    new_position[random_particle, :] = new_coordinate
    new_energy = calc_sys_potential(params['num_particles'], new_position, box_length)
    energy_diff = new_energy - initial_energy
    k = 1
    prob_acc = np.exp(-(1 / (k * params['temp'])) * energy_diff)
    prob_acc_list.append(prob_acc)
    if energy_diff < 0:
        initial_position = new_position
        initial_energy = new_energy
    else:
        if np.random.rand() <= prob_acc:
            initial_position = new_position
            initial_energy = new_energy
        else:
            initial_position = initial_position

    for i in range(1000, params['num_steps'], 1000):
        avg = np.mean(prob_acc_list)
        if avg < 0.48:
            params['d_max'] *= 0.8
        elif avg > 0.52:
            params['d_max'] *= 1.2


rc('font', **{
    'family': 'sans-serif',
    'sans-serif': ['DejaVu Sans'],
    'size': 10})
rc('mathtext', **{'default': 'regular'})
plt.rc('font', family='serif')

plt.title("Time Elapsed Calculating Energy as a Function of the Number of Particles")
plt.xlabel("Number of Monte Carlo Steps")
plt.ylabel("Total Potential Energy")
plt.grid()
plt.plot(steps, energy)
plt.show()