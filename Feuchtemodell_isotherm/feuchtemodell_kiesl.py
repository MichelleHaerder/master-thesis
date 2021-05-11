import numpy as np
import math
import time

class FeuchteModell():
    def __init__(self):
        self.increasing = True
        self.delta_pw = 6.579*10**-11
        self.delta_pd = None
        self.rho_material = 1833
        self.rho_w = 1.000
        self.dx = 0.005
        self.dt = 600
        self.x = 0.15
        self.t = 36000
        self.T = 23
        self.nSlices = int(self.x/self.dx)
        self.phi = []
        self.w_f = (109.60291049, 108.87296769) #(wf_ad, wf_de)
        self.b = (1.55379379, 2.4556701)  #correction factor (b_ad, b_de)
        self.A = 0.0247126 # [kg/m²sqrt(s)]
        

    def initial_and_boundary_conditions(self):
        #later we can change the conditions
        self.phi_initial = 0.5
        self.phi_boundary = 0.9
    
    def make_tri_diag(self,phi):
        """
        Create the tridiagonal matrix to solve one timestep. The tridiagonal matrix represents the gradient in space.
        """
        a_w, a_p, a_e = self._make_tridiag_coeff(phi)
        triDiag = self._tridiag(a_w,a_p,a_e)

        return triDiag
    
    def test_tridiag(self):
        phi = 0.6 * np.ones(self.nSlices)
        tridiag = self.make_tri_diag(phi)
        print(tridiag)
    #********************************************************************************
    #extensions/helper functions
    def _calc_p_sat(self):
        """
        Returns saturation pressure depending on Temperature.
        """
        p_sat = 611*np.exp(17.08*self.T/(234.18+self.T))

        return p_sat

    def _tridiag(self,a_w, a_p, a_e, k1=-1, k2=0, k3=1):
        """
        Returns a tridiagonal matrix with:
        a_p as main diagonal,
        a_w as lower diagonal,
        a_e as upper diagonal
        """
        return np.diag(a_w, k1) + np.diag(a_p, k2) + np.diag(a_e, k3)

    def _make_tridiag_coeff(self,phi):
        """
        Returns the coefficients for the tridiagonal matrix. They are dependent on the last/current phi.
        Mind that we had a wrong sign in our calculation and we took the signs from Künzel et. al.
        """
        phi_w = phi[1:]
        phi_p = phi
        phi_e = phi[:-1]
        a_w = self._calc_D_phi(phi_w) * (1/self.dx) - self._calc_p_sat() * self.delta_pw * (1/self.dx)
        a_p = -self._calc_D_phi(phi_p) * (1/self.dx) - self._calc_p_sat() * self.delta_pw * (1/self.dx) - self._derivative_dw_dphi(phi_p) * (self.dx/self.dt)
        a_e = self._calc_D_phi(phi_e) * (1/self.dx) - self._calc_p_sat() * self.delta_pw * (1/self.dx)
        

        return a_w, a_p, a_e

    def _rf_to_h2o_content(self,phi):
        """
        Maps relative humidity [-] to water content in [kg/m³] using the curve fitting described in Künzel et. al.
        correction factor: b_ad = 1.55379379, b_de = 2.4556701
        free water saturation: w_f,ad = 109.60291049, w_f,de = 108.87296769
        """
        if self.increasing:
            w = self.w_f[0]*(self.b[0]-1)*np.array(phi)/(self.b[0]-np.array(phi))
        else:
            w = self.w_f[1]*(self.b[1]-1)*np.array(phi)/(self.b[1]-np.array(phi))

        return w
    
    def _derivative_dw_dphi(self,phi):
        """
        Derivative of "Feuchtespeicherfunktion" [kg/m³].
        Returns the gradient for dw/dphi at given phi.
        """
        if self.increasing:
            dw_dphi = self.w_f[0]*((self.b[0]-1) * (self.b[0]-phi) + (self.b[0]-1)*phi) / (self.b[0]-phi)**2
        else:
            dw_dphi = self.w_f[1]*((self.b[1]-1) * (self.b[1]-phi) + (self.b[1]-1)*phi) / (self.b[1]-phi)**2

        return dw_dphi


    def _calc_D_ws(self,w):
        """
        Calculate "Kapillartransportkoeffizient für den Saugvorgang" [m²/s]
        Needs water content of last/current step.
        """
        if self.increasing:
            D_ws = 3.8 * (self.A / self.w_f[0])**2 * 1000**(w/(self.w_f[0]-1)) 
        else:
            D_ws = 3.8 * (self.A / self.w_f[1])**2 * 1000**(w/(self.w_f[1]-1)) 

        return D_ws

    def _calc_D_phi(self,phi):
        """
        Calculate "Flüssigleitkoeffzient" D_phi = D_w * dw/dphi [kg/ms]
        """
        w = self._rf_to_h2o_content(phi)
        D_ws = self._calc_D_ws(w)
        D_phi = D_ws * self._derivative_dw_dphi(phi)

        return D_phi




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