import numpy as np
import math
import scipy.linalg 
import matplotlib.pyplot as plt
import functionCollection as fC
import time
import random
"""
To do:
1) Define and update parameters
2) Initial and boundary conditions
3) Create the tridiag
4) Solve system of linear equations
After 1-4 works, do ADI method to update parameters in tridiag with step = 1/2(phi_n + phi_n-1)
"""
#1) Define the parameters
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

# define fixed parameters 
p_sat = 2814.6337703571003
delta_pw = 6.579*10**-11

# define list of results for humidity and water content
lstPhi = []
lstW = []
lstPhi.append(phi_n1)
# for loop to solve for timesteps
for i in range(0,timeSteps+1):
    
    # update variable parameters
    D_phi = fC.calc_D_phi(phi_n1)
    #D_phi = 1.2*10**-7 * np.ones(25)
    dw_dphi = fC.derivative_dw_dphi(phi_n1)
    # calculate F
    #proxy = [10*random.uniform(0,1)+170 for n in range(0,dw_dphi.shape[0])]
    #print(proxy)
    F = -(D_phi + delta_pw * p_sat) * (1 / dw_dphi ) * (dt / (dx**2))
    #F = 1e-9 * dt / dx**2 *np.ones(25)
    #print((D_phi + delta_pw * p_sat) / dw_dphi)
    #print(F)
    b = phi_n1
    b[0] = b[-1] = bc_phi
    tridiag = fC.make_tridiag(F,spatialSteps)
    phi_n = scipy.linalg.solve(tridiag,b)
    if i in range(0,2):
        print("-"*20 + "Iteration number is {}".format(i) + "-"*20)
        for arr in [("D_phi",D_phi),("dw_dphi",dw_dphi),("F",F),("tridiag",tridiag)]:
            print("-"*50)
            print(arr[0],"\n",arr[1])

    lstPhi.append(phi_n)
    phi_n1 = phi_n
plt.figure()
for phi in lstPhi:
    plt.plot(phi)
plt.show()

