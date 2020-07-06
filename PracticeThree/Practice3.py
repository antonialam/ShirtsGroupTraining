import time
from itertools import combinations
import numpy as np
from matplotlib import rc
import matplotlib.pyplot as plt


def initialize_particles(particles, box_length):
    """
    Parameters:
        particles (int): The number of particles in the simulation box.
        box_length (float): The length of the side of the simulation box.
    Returns:
        The random 3-dimensional coordinates of each particle.
    """
    return np.random.uniform(low=-box_length/2, high=box_length/2, size=(particles, 3))
# print(initialize_particles(5,1))


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
# print(calc_distance([1,2,5],[1,2,100],7.0))


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
# print(lennard_jones([1, 2, 5], [1, 2, 100], 7.0))


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
        total += lennard_jones(coordinates[i[0] - 1], coordinates[i[1] - 1], box_length)
    return total
x = ([[0.280658, 0.5280338, 0],
      [0.89481114, 0.75999593, 0],
      [0.80558062, 0.52409808, 0],
      [0.07831073, 0.74807289, 0],
      [0.07833195, 0.08513294, 0]])
# print(calc_sys_potential(5,x,1))


# Graphing the time elapsed calculating energy as a function of the number of particles
x = []
y = []
for num in range(2, 101):
    random_coordinates = initialize_particles(num, 5)
    t1 = time.time()
    total_energy = calc_sys_potential(num, random_coordinates, 5)
    t2 = time. time()
    elapsed_time = t2 - t1
    x.append(num)
    y.append(elapsed_time)

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
plt.plot(x, y, linewidth=0.8)
plt.show()


# Graphing histogram of total energy frequencies
y = []
for num in range(1, 1001):
    random_coordinates = initialize_particles(100, 5)
    total_energy = calc_sys_potential(100, random_coordinates, 5)
    y.append(total_energy)

rc('font', **{
    'family': 'sans-serif',
    'sans-serif': ['DejaVu Sans'],
    'size': 10})
rc('mathtext', **{'default': 'regular'})
plt.rc('font', family='serif')

plt.title("Distribution of Total Energy")
plt.xlabel("Total Energy")
plt.ylabel("Number of Trials")
plt.grid()
plt.hist(y, bins=1000)
plt.show()
