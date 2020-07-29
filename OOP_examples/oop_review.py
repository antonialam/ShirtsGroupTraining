# this is the case that r is not an attribute
param = {'sigma': 1, 'epsilon': 1}
lj = LJ_energy(param)
lj.LJ(2)
lj.LJ(4)
lj.LJ(6)
lj.LJ(7.45234)
lj.LJ(234234)


# say that we just made r as an attribute
param = {'sigma': 1, 'epsilon': 1, 'r': 2}
lj = LJ_energy(param)     # self.r = 2
lj.LJ()   # energy of a pair of particles separated by a distance of 2

param_2 = {'sigma': 1, 'epsilon': 1, 'r': 4}
lj_2 = LJ_energy(param)
lj_2.LJ()    # energy of a pair of particles separated by a distance of 4
