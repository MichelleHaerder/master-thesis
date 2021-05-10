import numpy as np
import math
import time

class FeuchteModell():
    def __init__(self):
        self.delta_pw = 6.579*10**-11
        self.delta_pd = None
        self.D_w = 8.029*10**-11
        self.rho_material = 1750
        self.rho_w = 1.000
        self.dx = 0.1
        self.dt = 600
        self.x = 1.15
        self.t = 36000
        self.T = 23
        self.nSlices = int(self.x/self.dx)
        self.p_sat = self._calc_p_sat()
        self.F = self._calc_F()

    def initial_and_boundary_conditions(self):
        #later we can change the conditions
        self.phi_initial = 0.5
        self.phi_boundary = 0.9
    
    def make_tri_diag(self):
        a = c = -self.F*np.ones(self.nSlices-1)
        b = (1 + 2*self.F)*np.ones(self.nSlices)
        triDiag = self._tridiag(a,b,c)

        return triDiag



    #extensions/helper functions
    def _calc_p_sat(self):
        """
        Returns saturation pressure depending on Temperature.
        """
        p_sat = 611*np.exp(17.08*self.T/(234.18+self.T))

        return p_sat

    def _calc_F(self):
        """
        Returns key parameter.
        """
        F = self.dt/self.dx**2*(self.D_w*self.rho_w + self.delta_pw*self.p_sat)

        return F

    def _tridiag(self,a, b, c, k1=-1, k2=0, k3=1):
        """
        Returns a tridiagonal matrix with:
        b as main diagonal,
        a as lower diagonal,
        c as upper diagonal
        """
        return np.diag(a, k1) + np.diag(b, k2) + np.diag(c, k3)

# if __name__ == "__main__":

#     def initialize_parameters():
#         #3DF
#         #Wasserdampfpermeabilität/Wasserdampfdiffusionsleitkoeffizient (wet, dry) [kg/msPa]
#         delta_pw = 6.579*10**-11
#         delta_pd = None
#         #Kapillartransportkoeffizient für Saugvorgang [m²/s]
#         D_w = 8.029*10**-11
#         #Dichte  Baustoff
#         rho_material = 1750
#         #Dichte Wasser
#         rho_w = 1.000
#         #Schrittgrößen
#         dx = 0.005 #in m
#         dt = 600  #in s
#         #Dimensionen der Probe
#         x = 0.115 #in m
#         #Untersuchungszeit
#         t = 36000 #in s
#         params = {
#             "delta_pw" : 6.579*10**-11,
#             "delta_pd" : None,
#             "D_w" : 8.029*10**-11,
#             "rho_material" : 1750,
#             "rho_w" : 1.000,
#             "dx" : 0.005,
#             "dt" : 600,
#             "x" : 0.115,
#             "t" : 36000,
#             "T" : 25
#         }
        
#         return params

#     #Definieren der Anfangs- und Randbedingungen (Initial and Boundary Conditions (IBC))    
#     def ibc(dx, dt,x,t):
#         nCols = int(x/dx)
#         nRows = int(x/dx)
#         #Anfangsbedingungen
#         phi_0 = 0.5 # in %
#         Phi_0 = phi_0*np.ones((1,nCols))
#         #Randbedingungen
#         phi_bc = 0.9
#         Phi_bc = np.zeros((nRows,1))
#         Phi_bc[0] = phi_bc
#         Phi_bc[-1] = phi_bc

#         return Phi_0, Phi_bc

#     #Tridiagonalmatrix für Temperaturmodell definieren
#     def make_tri_diag_Theta(dt, dx ,x ,cp ,rho_material, lamb):
#         nRows = int(x/dx)
#         a_m = math.pow(dx,2) / dt * cp * rho_material + 2 * lamb
#         a_l = -lamb
#         a_r = -lamb
#         diag_m = np.ones(nRows)
#         diag_r = np.ones(nRows-1)
#         diag_l = np.ones(nRows-1)
#         triDiag_m = np.diag(diag_m,k=0)
#         triDiag_r = np.diag(diag_r,k=1)
#         triDiag_l = np.diag(diag_l,k=-1)
#         triDiag_Theta = a_m * triDiag_m + a_r * triDiag_r + a_l * triDiag_l
        
#         return triDiag_Theta

#     #Bestimmungsvektor für Temperaturmodell definieren (relative Luftfeuchte kommt in S_h vor)
#     def make_b_Theta(dx, dt, cp, rho_material, currTheta, S_h, Theta_bc): 
#         a_b = math.pow(dx,2) / dt * cp * rho_material
#         currTheta = np.reshape(currTheta,(1,len(currTheta)))
#         currTheta = np.transpose(currTheta)
#         b_Theta = a_b * currTheta - S_h + Theta_bc

#     return b_Theta

#     #Tridiagonalmatrix für Feuchtemodell definieren
#     def make_tri_diag_Phi(dt, dx, x, rho_material, D_w, delta_pw,nextTheta):
#         nRows = int(x/dx)
#         nextTheta_m = nextTheta
#         nextTheta_r = nextTheta[:-1] #"-1" bedeutet bis ausschließlich letzer eintrag im array
#         nextTheta_l = nextTheta[1:] #"1" bedeutet zweiter Eintrag im Array
#         a_m = math.pow(dx,2) / dt * rho_material + 2 * rho_material * D_w + delta_pw * calc_P_sat(nextTheta_m)
#         a_l = -rho_material * D_w + calc_P_sat(nextTheta_l)
#         a_r = -rho_material * D_w + calc_P_sat(nextTheta_r)
#         diag_m = np.ones(nRows)
#         diag_r = np.ones(nRows-1)
#         diag_l = np.ones(nRows-1)
#         triDiag_m = np.diag(diag_m,k=0)
#         triDiag_r = np.diag(diag_r,k=1)
#         triDiag_l = np.diag(diag_l,k=-1)
#         a_l = np.insert(a_l,0,0)
#         a_l = np.reshape(a_l,(len(a_l),1))
#         a_r = np.append(a_r,0)
#         a_r = np.reshape(a_r,(len(a_r),1))
#         triDiag_Phi = a_m * triDiag_m + a_r * triDiag_r + a_l * triDiag_l
    

#         return triDiag_Phi

#     #Bestimmungsbektor für Feuchtemodell definieren (Temperatur kommt in S_h vor)
#     def make_b_Phi(dx, dt, rho_material, Phi, Phi_bc):
#         b_Phi = math.pow(dx,2) / dt *rho_material * Phi + Phi_bc
        
#         return b_Phi

#     #Später kann delta_pw durch andere Parameter ersetzt werden.
#     def calc_S_h(h_v, delta_pw,currTheta,currPhi):
#         p_sat = calc_P_sat(currTheta)
#         S_h = h_v * delta_pw * currPhi * p_sat
#         S_h = np.reshape(S_h,(1,len(S_h)))
#         S_h = np.transpose(S_h)

#         return S_h
#     #For Temperature: Theta is currTheta, for Phi: Theta is nextTheta
#     def calc_p_sat(Theta):
#         P_sat = 611*np.exp(17.08*Theta/(234.18+Theta))

#         return p_sat

#     #Übersetzt relative Luftfeuchte in Wassergehalt
#     def phi_to_u_mapping(Phi,mapping):
#         u = None

#         return u



#     #******Main Code******
#     #Initialisuerung Anfangs und Randbedingungen
#     delta, mu_dry, mu_wet, rho_w, D_w, h_v, cp, rho_material, lamb, dx, dt, x, t, delta_pw, delta_pd = initialize_parameters()
#     Phi_0, Phi_bc = ibc(dx, dt,x,t)
#     #Definition der Ergebnismatrizen
#     nCols = int(x/dx)
#     nRows = int(t/dt)
#     Theta = np.zeros((nRows,nCols))
#     Phi = np.zeros((nRows,nCols))
#     Theta[0,:] = Theta_0
#     Phi[0,:] = Phi_0
#     #nRows-1 als läufer um beim letzten timestep nicht in die Leere zu schreiben (SegmentationFault)
#     #Implicit Euler also in timstep n wird in n+1 geschrieben
#     for timestep in range(nRows-1):
#         currTheta = Theta[timestep,:]
#         currPhi = Phi[timestep,:]
#         #Theta
#         S_h = calc_S_h(h_v,delta_pw,currTheta,currPhi)
#         b_Theta = make_b_Theta(dx, dt, cp, rho_material,currTheta , S_h, Theta_bc)
#         triDiag_Theta = make_tri_diag_Theta(dt, dx ,x ,cp ,rho_material, lamb)
#         nextTheta = np.linalg.solve(triDiag_Theta,b_Theta)
#         Theta[timestep+1]= nextTheta[:,0]
#         #Phi - p_sat wird in make_tri_diag aufgerufen
#         b_Phi = make_b_Phi(dx, dt, rho_material,currPhi, Phi_bc)
#         triDiag_Phi = make_tri_diag_Phi(dt,dx,x,rho_material,D_w,delta_pw,nextTheta)
#         nextPhi = np.linalg.solve(triDiag_Phi,b_Phi)

#         Phi[timestep+1] =  nextPhi[:,0]
#         if timestep % 10 == 0:
#             print("Done with step ", timestep)
#             time.sleep(0.5)
#     print("Theta: \n",Theta)
#     print("Phi: \n",Phi)