import numpy as np
import math
import time

def initialize_parameters():
    #******Verdampfungsmenge******
    #Wasserdampfdiffusionsleitkoeffizient  Luft (Einheiten prüfen)
    delta = 1.95*np.power(10,float(-10))
    #Wasserdampfdiffusionswiderstandszahl  Baustoff 
    mu_dry = 10
    mu_wet = 5
    #Wasserdampfpermeabilität (wet, dry)
    delta_pw = delta / mu_wet
    delta_pd = None
    #******FEUCHTETRANSPORT******
    #Dichte Wasser
    rho_w = 1.000
    #Kapillartransportkoeffizient  Baustoff 
    # Muss noch bestimmt WERDEN UND IST DEUTLICH KLEINER ALS 1
    D_w = 5*np.power(10,float(-7))
    #******Wärmetransport******
    #Verdampfungsenthalpie  Wasser
    h_v = 2257
    #Spez. Wärmekapazität  Baustoff
    cp = 1.0
    #Dichte  Baustoff
    rho_material = 1750
    #Wärmeleitfähigkeit  Baustoff
    lamb = 1.1
    #Schrittgrößen
    dx = 0.005 #in m
    dt = 600  #in s
    #Dimensionen der Probe
    x = 0.115 #in m
    #Untersuchungszeit
    t = 36000 #in s
    
    return delta, mu_dry, mu_wet, rho_w, D_w, h_v, cp, rho_material, lamb, dx, dt, x, t, delta_pw, delta_pd

#Definieren der Anfangs- und Randbedingungen (Initial and Boundary Conditions (IBC))    
def ibc(dx, dt,x,t):
    nCols = int(x/dx)
    nRows = int(x/dx)
    #Anfangsbedingungen
    theta_0 = 26 # in Grad Celsius
    Theta_0 = theta_0*np.ones((1,nCols))
    phi_0 = 0.5 # in %
    Phi_0 = phi_0*np.ones((1,nCols))
    #Randbedingungen
    theta_bc = 20
    Theta_bc = np.zeros((nRows,1))
    Theta_bc[0] = theta_bc
    Theta_bc[-1] = theta_bc
    phi_bc = 0.8
    Phi_bc = np.zeros((nRows,1))
    Phi_bc[0] = phi_bc
    Phi_bc[-1] = phi_bc

    return Theta_0, Phi_0, Theta_bc, Phi_bc

#Tridiagonalmatrix für Temperaturmodell definieren
def make_tri_diag_Theta(dt, dx ,x ,cp ,rho_material, lamb):
    nRows = int(x/dx)
    a_m = math.pow(dx,2) / dt * cp * rho_material + 2 * lamb
    a_l = -lamb
    a_r = -lamb
    diag_m = np.ones(nRows)
    diag_r = np.ones(nRows-1)
    diag_l = np.ones(nRows-1)
    triDiag_m = np.diag(diag_m,k=0)
    triDiag_r = np.diag(diag_r,k=1)
    triDiag_l = np.diag(diag_l,k=-1)
    triDiag_Theta = a_m * triDiag_m + a_r * triDiag_r + a_l * triDiag_l
    
    return triDiag_Theta

#Bestimmungsvektor für Temperaturmodell definieren (relative Luftfeuchte kommt in S_h vor)
def make_b_Theta(dx, dt, cp, rho_material, currTheta, S_h, Theta_bc): 
   a_b = math.pow(dx,2) / dt * cp * rho_material
   currTheta = np.reshape(currTheta,(1,len(currTheta)))
   currTheta = np.transpose(currTheta)
   b_Theta = a_b * currTheta - S_h + Theta_bc

   return b_Theta

#Tridiagonalmatrix für Feuchtemodell definieren
def make_tri_diag_Phi(dt, dx, x, rho_material, D_w, delta_pw,nextTheta):
    nRows = int(x/dx)
    nextTheta_m = nextTheta
    nextTheta_r = nextTheta[:-1] #"-1" bedeutet bis ausschließlich letzer eintrag im array
    nextTheta_l = nextTheta[1:] #"1" bedeutet zweiter Eintrag im Array
    a_m = math.pow(dx,2) / dt * rho_material + 2 * rho_material * D_w + delta_pw * calc_P_sat(nextTheta_m)
    a_l = -rho_material * D_w + calc_P_sat(nextTheta_l)
    a_r = -rho_material * D_w + calc_P_sat(nextTheta_r)
    diag_m = np.ones(nRows)
    diag_r = np.ones(nRows-1)
    diag_l = np.ones(nRows-1)
    triDiag_m = np.diag(diag_m,k=0)
    triDiag_r = np.diag(diag_r,k=1)
    triDiag_l = np.diag(diag_l,k=-1)
    a_l = np.insert(a_l,0,0)
    a_l = np.reshape(a_l,(len(a_l),1))
    a_r = np.append(a_r,0)
    a_r = np.reshape(a_r,(len(a_r),1))
    triDiag_Phi = a_m * triDiag_m + a_r * triDiag_r + a_l * triDiag_l
 

    return triDiag_Phi

#Bestimmungsbektor für Feuchtemodell definieren (Temperatur kommt in S_h vor)
def make_b_Phi(dx, dt, rho_material, Phi, Phi_bc):
    b_Phi = math.pow(dx,2) / dt *rho_material * Phi + Phi_bc
    
    return b_Phi

#Später kann delta_pw durch andere Parameter ersetzt werden.
def calc_S_h(h_v, delta_pw,currTheta,currPhi):
    p_sat = calc_P_sat(currTheta)
    S_h = h_v * delta_pw * currPhi * p_sat
    S_h = np.reshape(S_h,(1,len(S_h)))
    S_h = np.transpose(S_h)

    return S_h
#For Temperature: Theta is currTheta, for Phi: Theta is nextTheta
def calc_P_sat(Theta):
    P_sat = 611*np.exp(17.08*Theta/(234.18+Theta))

    return P_sat

#Übersetzt relative Luftfeuchte in Wassergehalt
def phi_to_u_mapping(Phi,mapping):
    u = None

    return u



#******Main Code******
#Initialisuerung Anfangs und Randbedingungen
delta, mu_dry, mu_wet, rho_w, D_w, h_v, cp, rho_material, lamb, dx, dt, x, t, delta_pw, delta_pd = initialize_parameters()
Theta_0, Phi_0, Theta_bc, Phi_bc = ibc(dx, dt,x,t)
#Definition der Ergebnismatrizen
nCols = int(x/dx)
nRows = int(t/dt)
Theta = np.zeros((nRows,nCols))
Phi = np.zeros((nRows,nCols))
Theta[0,:] = Theta_0
Phi[0,:] = Phi_0
#nRows-1 als läufer um beim letzten timestep nicht in die Leere zu schreiben (SegmentationFault)
#Implicit Euler also in timstep n wird in n+1 geschrieben
for timestep in range(nRows-1):
    currTheta = Theta[timestep,:]
    currPhi = Phi[timestep,:]
    #Theta
    S_h = calc_S_h(h_v,delta_pw,currTheta,currPhi)
    b_Theta = make_b_Theta(dx, dt, cp, rho_material,currTheta , S_h, Theta_bc)
    triDiag_Theta = make_tri_diag_Theta(dt, dx ,x ,cp ,rho_material, lamb)
    nextTheta = np.linalg.solve(triDiag_Theta,b_Theta)
    Theta[timestep+1]= nextTheta[:,0]
    #Phi - p_sat wird in make_tri_diag aufgerufen
    b_Phi = make_b_Phi(dx, dt, rho_material,currPhi, Phi_bc)
    triDiag_Phi = make_tri_diag_Phi(dt,dx,x,rho_material,D_w,delta_pw,nextTheta)
    nextPhi = np.linalg.solve(triDiag_Phi,b_Phi)

    Phi[timestep+1] =  nextPhi[:,0]
    if timestep % 10 == 0:
        print("Done with step ", timestep)
        time.sleep(0.5)
print("Theta: \n",Theta)
print("Phi: \n",Phi)