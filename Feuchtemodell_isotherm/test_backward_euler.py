import numpy as np
import math
import matplotlib.pyplot as plt
L = 0.15 #in m
Nx = 23
T = 3600*24*36 #in s
Nt = 24*36
D_phi = 0.000358305124719784
delta_pw = 6.579*10**-11
p_sat = 2814.6337703571003
diffu = 1
dw_dphi = 115.46

x = np.linspace(0, L, Nx+1)   # mesh points in space
dx = x[1] - x[0]
t = np.linspace(0, T, (Nt+1))    # mesh points in time
dt  = t[1]-t[0]
u   = np.zeros(Nx+1)          # unknown u at new time level
u_1 = np.zeros(Nx+1)          # u at the previous time level

#Define F
#F = dt/dx**2 * diffu
#F =(D_phi + delta_pw*p_sat)/dw_dphi * dt/dx**2
#F_= (D_phi + delta_pw*p_sat)/dw_dphi
F=1e-9* dt/dx**2
# Data structures for the linear system
A = np.zeros((Nx+1, Nx+1))
b = np.zeros(Nx+1)
print(A)
for i in range(1, Nx):
    A[i,i-1] = -F
    A[i,i+1] = -F
    A[i,i] = 1 + 2*F
A[0,0] = A[Nx,Nx] = 1
print(A)
# Set initial condition u(x,0) = I(x)
for i in range(0, Nx+1):
    #u_1[i] = I(x[i])
    #u_1[i] = math.cos(i/(Nx+1)*math.pi)
    #u_1[i] = (i/(Nx+1-50))**2
    u_1[i] = 0.9

u_1[0]=u_1[-1]=0.5

plt.plot(u_1)
import scipy.linalg

for n in range(0, Nt+1):
    # Compute b and solve linear system
    for i in range(1, Nx):
        b[i] = u_1[i]
    b[0] = 0.5
    b[Nx] = 0.5
    u[:] = scipy.linalg.solve(A, b)

    # Update u_1 before next step
    plt.plot(u)
    u_1[:] = u
    if n in range(0,2):
        print("-"*20 + "Iteration number is {}".format(n) + "-"*20)
        print("-"*50)
        print("A is: \n",A)
    #print(u)


plt.show()
print("F is {}.".format(F))