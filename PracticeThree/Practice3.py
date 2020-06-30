import itertools
from itertools import combinations
import numpy as np



def initialize_particles(p, l):
    """
    Parameters:
        p (int): The number of particles in the simulation box.
        l (float): The length of the side of the simulation box.
    Returns:
        The random 3-dimensional coordinates of each particle.
    """
    return np.random.uniform(low=-l/2, high=l/2, size=(p, 3))
# print(initialize_particles(5,1))


def calc_distance(a, b, l):
    """
       Parameters:
           a (list): The 3-dimensional coordinates of a particle.
           b (list): The 3-dimensional coordinates of another particle.
           l (float): The length of the side of the simulation box.
       Returns:
           r (float): The distance between two particles with the consideration of periodic boundary conditions (PBCs).
    """
    x = (a[0] - b[0]) ** 2
    y = (a[1] - b[1]) ** 2
    z = (a[2] - b[2]) ** 2
    distance = (x + y + z) ** 0.5
    if distance > 0.5 * l:
        global n
        for n in itertools.count(start=1):
            if distance - (n * l) < 0.5 * l:
                break
    return abs(distance - (n * l))
# print(calc_distance([1,2,5],[1,2,100],7.0))


def lennard_jones(a, b, l):
    """
       Returns:
           potential (float): Uses the calc_distance function to return the Lennard-Jones potential between two particles.
    """
    r = calc_distance(a, b, l)
    potential = 4 * ((1 / (r**12)) - (1 / (r**6)))
    return potential
#print(lennard_jones([1, 2, 5], [1, 2, 100], 7.0))


def calc_sys_potential(p, coordinates, l):
    total = 0
    for i in combinations(list(range(1, p + 1)), 2):
        total += lennard_jones(coordinates[i[0] - 1], coordinates[i[1] - 1], l)
    return total

x = ([[0.280658  , 0.5280338, 0 ],
       [0.89481114, 0.75999593, 0],
       [0.80558062, 0.52409808, 0],
       [0.07831073, 0.74807289, 0],
       [0.07833195, 0.08513294, 0]])

print(calc_sys_potential(5,x,1))








