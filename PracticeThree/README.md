# Practice 3 of Shirts Group Training
### Description
The following code runs a simulation when the user specifies the length and the number of particles of the simulation box. Given this information, each particle is assigned a random three-dimensional coordinate. The total energy of the system is then calculated by finding the distance and its respective Lennard-Jones potential between all pairs of particles. 

The first plot shows the time elapsed calculating the total energy as a function of the number of particles. As the graph indicates, as the number of particles in the simulation box increases, the time taken to calculate the total energy increases non-linearly. The two variables have a polynomial relationship with a degree of 2. Given this graph, the time taken to calculate the total energy for systems with more than 100 particles can be roughly approximated, giving the user some insight into the computational expense of running a simulation. In this specific graph, the box length is 5, and the number of particles is n = 2 to n = 100 (increment of 1).   

The second plot shows a histogram of the distribution of the total energies. In this specific graph, 1000 trials were run with 100 particles and a box length of 5. 
