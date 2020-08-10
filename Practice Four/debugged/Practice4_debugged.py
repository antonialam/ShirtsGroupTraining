import numpy as np
from itertools import combinations
import math
import yaml
from tqdm.auto import tqdm
from matplotlib import rc
import matplotlib.pyplot as plt
import copy


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
    rc = 2.5 * sigma

    if (params['truncate'] == 'yes' and distance <= rc) or (params['truncate'] == 'no'):
        r12 = (sigma / distance) ** 12
        r6 = (sigma / distance) ** 6
        potential = 4 * epsilon * (r12 - r6)

        
        if params['shift'] == 'yes':
            #rc -= box_length * np.round(rc / box_length)
            rc12 = (sigma / rc) ** 12
            rc6 = (sigma / rc) ** 6
            rc_potential = 4 * epsilon * (rc12 - rc6)
            potential -= rc_potential
    else:
        potential = 0

    return potential


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
    for i in combinations(range(1, particles + 1), 2):
        total += lennard_jones(coordinates[i[0] - 1], coordinates[i[1] - 1], box_length)

    return total

def LJ_pair_total(coordinates, i, box_length):
    # i: the index of the selected particle of interest
    E_pair_total = 0

    for j in range(len(coordinates)):   # particles: number of particles
        if i != j:
            E_pair_total += lennard_jones(coordinates[i], coordinates[j], box_length)

    return E_pair_total

def tail(particles, box_length, epsilon=1, sigma=1):
    rc = 2.5 * sigma
    rc9 = (sigma / rc) ** 9
    rc3 = (sigma / rc) ** 3
    tail = ((8 * math.pi * (particles ** 2) * epsilon * (sigma ** 3)) / (3 * (box_length ** 3))) * ((rc9 / 3) - rc3)
    return tail

def logger(*args, **kwargs):
    print(*args, **kwargs)
    with open("MC_results_debugged.txt", "a") as f:
        print(file=f, *args, **kwargs)


if __name__ == "__main__":

    logger("Reading in simulation parameters")
    with open('Practice4Parameters.yml') as ymlfile:
        params = yaml.load(ymlfile, Loader=yaml.FullLoader)
    box_len = (params['num_particles'] / params['density']) ** (1 / params['dim'])
    tail_correction = tail(params['num_particles'], box_len)
    initial_position = initialize_particles(params['num_particles'], box_len) 
    
    # new_position = initial_position.copy()
    initial_energy = calc_sys_potential(params['num_particles'], initial_position, box_len)
    logger(f"step 0: {initial_energy / params['num_particles']}")
    steps = []
    energy = []
    n_trials = 0
    n_accept = 0
    total = 0
    new_total = 0


    for step in tqdm(range(1, params['num_steps'] + 1)):
        steps.append(step)
        energy.append(initial_energy + tail_correction)
        n_trials += 1
        rand_particle = np.random.randint(0, params['num_particles']) # index of the selected particle
        new_position = copy.deepcopy(initial_position)
        new_coordinate = new_position[rand_particle] + ((np.random.rand(1, 3) - 0.5) * 2 * params['d_max'])  # the new coordinate of the selected particle
        new_position[rand_particle] = new_coordinate
        new_position[rand_particle] -= box_len * np.round(new_position[rand_particle] / box_len) # PBCs

        E_current = LJ_pair_total(initial_position, rand_particle, box_len)
        E_proposed = LJ_pair_total(new_position, rand_particle, box_len)

        energy_diff = E_proposed - E_current

        if energy_diff < 0:
            initial_position[rand_particle, :] = new_coordinate
            initial_position -= box_len * np.round(initial_position / box_len)
            initial_energy += energy_diff
            n_accept += 1

        else:
            # Note that we don't calculate p_acc outside the if statement
            # since -beta * delta_E could be very large, which can cause overflow in exp
            prob_acc = np.exp(-(1 / params['reduced_temp']) * energy_diff)
            if np.random.rand() <= prob_acc:
                initial_position[rand_particle, :] = new_coordinate
                initial_position -= box_len * np.round(initial_position / box_len)
                initial_energy += energy_diff
                n_accept += 1

        if step % 1000 == 0:
            logger(f"step {step}: {initial_energy / params['num_particles']}")
            acc_rate = n_accept / n_trials
            if acc_rate < 0.38:
                params['d_max'] *= 0.8
            elif acc_rate > 0.42:
                params['d_max'] *= 1.2
            

    rc('font', **{
        'family': 'sans-serif',
        'sans-serif': ['DejaVu Sans'],
        'size': 10})
    rc('mathtext', **{'default': 'regular'})
    plt.rc('font', family='serif')

    plt.title("Total Potential Energy as a Function of the Number of Monte Carlo steps")
    plt.xlabel("Number of Monte Carlo Steps")
    plt.ylabel("Total Potential Energy")
    plt.grid()
    plt.plot(steps[int(0.1 * len(steps)):], np.array(energy[int(0.1 * len(steps)):]) / params['num_particles'])
    plt.show()
    plt.savefig("result_debugged.png", dpi=600)