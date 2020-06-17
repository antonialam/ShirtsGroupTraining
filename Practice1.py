import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

#Reading the File
f = open('volume.xvg','r')
lines = f.readlines()
f.close()

#Extracting Data From the File
x,y = [],[]
for line in lines:
    if line[0] != '#' and line[0] != '@':
        x.append(float(line.split()[0]))
        y.append(float(line.split()[1]))

#Executing the RMSF Equation
total1 = 0   #total1 represents the sum of the volume values
total2 = 0  #total2 represents the sum of the squared volume values
for number in y:
    total1 += number
    total2 += number**2
Q = total1 / len(y)   #<Q>
Q2 = total2 / len(y) #<Q^2>
RMSF = ((Q2 - (Q**2))**0.5) / Q

#Graphing the Plot
rc('font', **{
   'family': 'sans-serif',
   'sans-serif': ['DejaVu Sans'],
   'size': 10
})
rc('mathtext', **{'default': 'regular'})
plt.rc('font', family='serif')

plt.plot(x,y,linewidth=0.75)
plt.title("Volume as a function of time")
plt.xlabel("Time(ps)")
plt.ylabel("Volume($nm^3$)")
plt.grid()
plt.show()

#Printing Out Statistics
print("Data analysis of the file: volume.xvg")
print("=====================================")
print("Analyzing the file ...")
print("Plotting and saving figure ...")
print("The average of volume (nm^3): {0:.3f} (RMSF: {1:.3f}, max: {2:.3f}, min: {3:.3f})".format(Q,RMSF,max(y),min(y)))
print("The maximum occurs at {0:.4f} ns while the minimum occurs at {1:.4f} ns.".format(x[y.index(max(y))]/1000,x[y.index(min(y))]/1000))
print("The configuration at {0:.3f} ns has the volume ({1:.6f} nm^3) that is closest to the average volume.".format(x[y.index(min(y, key=lambda x : abs(x-Q)))]/1000,min(y, key=lambda x : abs(x-Q))))













