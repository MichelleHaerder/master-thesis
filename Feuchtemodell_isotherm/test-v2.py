import functionCollection as fC
import numpy as np


probeLength = 0.15
spatialSteps = 23
timePeriod = 3600*24*36
timeSteps = 24*36
# create meshpoints in space
x = np.linspace(0,probeLength,spatialSteps+1)
# define stepsize
dx = x[1]-x[0]
# create meshpoints in time
t = np.linspace(0,timePeriod,timeSteps+1)
# define stepsize
dt = t[1]-t[0]

# define initial and boundary conditions [-]
ic_phi = 0.5
bc_phi = 0.9
# define vectors for humidity
phi_n = phi_n1 = np.zeros(spatialSteps+2)
# fill ibc
phi_n1 = phi_n1+ic_phi
phi_n1[0] = phi_n1[-1] = bc_phi

# update variable parameters
D_phi = fC.calc_D_phi(phi_n1)

F = 1e-9*dt/dx**2 * np.ones(spatialSteps+2)
A = fC.make_tridiag(F,spatialSteps)