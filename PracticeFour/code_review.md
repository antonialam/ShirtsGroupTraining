# Overall comments
Here are some comments about your code:
- Remember to first merge `code_reviews` branch to the branch you're working on whenever I provide code reviews. Specifically, now the first step you should do is execute the command `git pull code_reviews` in branch `Pracitce4`. This way, the comments will be incorporated into your work and you can compare my code with yours. You can compare different commits (like my commit and your commit) by following the [procedure that I've previously mentioned](https://shirts-group.slack.com/archives/DUET2AM88/p1593123698009600). Let me know if you're not sure how to do this. 
- Remember that the maximal distance allowed in a simulation box should be smaller than 0.5 * `box_length`. Therefore, you also have to apply PBCs to the cutoff distance (`rc`).
- Maybe I was not clear enough, but there are several issues with your tail correction:
  - V in the denominator is volume, not the potential energy. The notations I used here were not the best. 
  - Tail correction should be added to the total system energy instead of every pairwise energy. Note that it is an overall correction for the energy of the whole system. (Actually, you could tell this from the equation, since the tail correction apparently accounts for the number of particles and the volume, which are dependent on the system size. The larger the system size (the number of the particles simulated), the larger the tail correction should be.)
- When calculating a quantity from a complex equation (like LJ potential), consider breaking down the equation into several terms like below:
  ```python
  def LJ_potential(self, coord_i, coord_j):
        r_ij = Initialization.calc_dist(self, coord_i, coord_j)

        if (self.energy_truncation == 'yes' and r_ij < self.r_c) or (self.energy_truncation == 'no'):
            r12 = (self.epsilon / r_ij) ** 12
            r6 = (self.epsilon / r_ij) ** 6
            p_LJ = 4 * self.epsilon * (r12 - r6)

            if self.shift_energy == 'yes':
                rc = self.r_c - self.box_length * \
                    np.round(self.r_c / self.box_length)
                rc12 = (self.epsilon / rc) ** 12
                rc6 = (self.epsilon / rc) ** 6
                pc_LJ = 4 * self.epsilon * (rc12 - rc6)
                p_LJ -= pc_LJ
        else:
            p_LJ = 0

        return p_LJ
  ```
  Above is just a function that I wrote for another project, but you can see how I broke down an equation. Of course, this could be just a personal preference (whether to break down the equation or how to break down an equation), but doing so would 
  - decrease the chance of making mistakes (like typos)
  - improve readability in general

- The way you calculated the experimental acceptance ratio was wrong. (Maybe I should have mentioned this in the meeting.) What you were doing was just averaging the time series of theoretical acceptance ratio, which could not really reflect the real percentage of trials being accepted. Specifically, the following example shows how you should calculate it:
  - `n_trials = 0`, `n_accept = 0`
  - MC step 1 (`n_trilas += 1`):
    - If the move is accepted, `n_accept += 1`
    - If the move is rejected, don't change `n_accept`
  - MC step 2 (`n_trilas += 1`):
    - If the move is accepted, `n_accept += 1`
    - If the move is rejected, don't change `n_accept`
  - ...
  - MC step 1000 (`n_trilas += 1`):
    - If the move is accepted, `n_accept += 1`
    - If the move is rejected, don't change `n_accept`
    - Calculate the experimental acceptance ratio, `p_acc = n_accept / n_trials` and use it to decide whether your maiximal displacement should be adjusted. 
  - Note that you could have calculated `p_acc` for every MC step, but it is generally not recommended to do so because we want to make our criteria for adjusting the maximal displacement dependent on an observation (`p_acc`) of a period of time instead of an instantaneous value. For example, if the first step is accepted, you will get `p_acc = 1`, which apparently not representative of the behavior of the system. Similarly, we don't want to calculate `p_acc` right after the displacement adjustment because the calculated `p_acc` can not sufficiently represent how the system was changed by the adjustment. This is why I suggest you to calculate `p_acc` and adjust the maximal displacement every 1000 steps. 
- Note that we are using the reduced temperature and it is set as 0.9. Please read through the article that I added last time to understand reduced units and why we want to do that. Also, we set the Boltzmann constant as 1 for the same reason, so you don't have to use `from scipy.constants import k`. Let me know if you have questiosn about reduced units.
- Okay, here comes the part probably bothered you the most, the efficiency of your code! 
  - Let me first talk about how I looked into your code. Rembmer the technique here, which is code **profiling** is useful whenver you want to find the slowest part of your code. To understand profiling, please read through the article that I added to the folder. In the folder you can see `profile_results.txt`, which was generated by the following command:
    ```
    python -m cProfile -s tottime AntoniaPractice4.py > profile_results.py
    ```
    As an additional requirement, please perform profiling after you modify your code to show that the efficiency of the code has been significantly improved. (I've changed the aprameters to 50 steps, so the simulation would not last too long while profiling.) Let me know if you have any questions regarding this.
  - The main issue of your code is that when we calculate the energy difference before and after a particle is moved, we can actually just consider the part of the energy that is relevant to the chosen particle. For example, say that we have 100 particles labeled as particle 1 to particle 100. Whenever we calculate the total energy of the system, we consider the pairwise energy between particle 1 and 2, 1 and 3, ..., 1 and 100, also 2 and 3, 2 and 4, ..., 2 and 100, and so on. (That's why the calculation is intensive. It has to find all the pairs!) Say that in the first MC step, particle 5 is chosen and a new energy is proposed. If the move is accepted, the only part of the energy that changes is the sum of the energy between particle 5 and 1, 5 and 2, ..., 5 and 100. That is, the pairwise energies between any other particles that do not involve particle 5 stay the same. (For example, the pairwise energy between particle 2 and 3 is the same since none of them moved!) Currently, this is what you're doing:
     - Calculate the initial total energy of the system.
     - MC step 1: 
       - current energy = initial energy
       - Pick a particle. Say we choose particle 5.
       - Calculate the new total energy of the system given that particle 5 is moved.
       - Calculate the difference in the total energy of the system. 
       - Decide whether the move should be accepted.
     - MC step 2 ...

    Base on the trick mentioned above, this should work much faster:
    - Calculate the initial total energy of the system.
    - MC step 1:
      - Pick a particle. Say we choose particle 5.
      - Calculate the current sum of the energy between particle 5 and 1, 5 and 2, ... 5 and 100. 
      - Calculate the new sum of the energy between particle 5 and 1, 5 and 2, ... 5 and 100 given that particle 5 is moved. 
      - Calculate the difference between the two sums of the energy above. Note that this difference **should be the same as the difference in the total energy of the system**. Let me know if this doesn't make sense to you.
      - Decide whether the move should be accepted. 

    Note that the second method is faster because we don't loop over 100 * 99 / 2 pairs but just 100 pairs of particles. (Also, let me know if you don't realize how these numbers come from.) This method is, therefore, much faster. 
- Remember to check your coding style with PEP8 in the end before you push your final work. After I provide the final code review for Practice 4 and introduce you the next practice, you then can merge my comments from `code_reviews` and merge `Practice4` to the master branch.
- Please make sure that you **completely understand** all the comments above, since that also maximizes the usefulness of our meetings and my code reviews! I'm happy to recap my words/explain again. :)