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
        #self.d = 0.15
        self.dx = 0.005
        self.dt = 3600
        self.x = 0.15
        self.t = 3600*24
        self.T = 23
        self.nSlices = int(self.x/self.dx)
        self.phi = []
        self.w_f = (109.60291049, 108.87296769) #(wf_ad, wf_de)
        self.b = (1.55379379, 2.4556701)  #correction factor (b_ad, b_de)
        self.A = 0.0247126 # [kg/m²sqrt(s)]
        

    def _initial_and_boundary_conditions(self):
        #later we can change the conditions
        #we take constant initial and boundary conditions
        if self.increasing:
            self.phi_initial = 0.5
            self.phi_boundary = 0.9
            
        else:
            self.phi_initial = 0.9
            self.phi_boundary = 0.5

        self.phi_initial_arr = self.phi_initial*np.ones((self.nSlices,1))
        self.phi_boundary_arr = self.phi_boundary*np.ones((self.nSlices,1))
        # Unclear what the boundary condition should be here.
        # Should be water content so with dw_dphi mapping
        ibc_phi = self.phi_initial*np.ones((self.nSlices+2,1))
        ibc_phi[0,0] = self.phi_boundary
        ibc_phi[-1,0] = self.phi_boundary
        #Not sure which ibc is right. Trying out..
        #ibc_phi is phi_n
        ibc = ibc_phi * self._derivative_dw_dphi(ibc_phi) * self.dx**2/self.dt
        #ibc = self._rf_to_h2o_content(ibc_phi)
        return ibc

    def _make_tri_diag(self,phi):
        """
        Create the tridiagonal matrix to solve one timestep. The tridiagonal matrix represents the gradient in space.
        """
        a_w, a_p, a_e = self._make_tridiag_coeff(phi)
        tridiag = self._tridiag(a_w,a_p,a_e)
        #print("a_w: {} | a_p: {} | a_e: {} |".format(a_w,a_p,a_e))
        tridiag = self._tridiag_bc_extension(tridiag)
        return tridiag

    def _tridiag_bc_extension(self,tridiag):
        """
        Including the boundary condition in the tridiag matrix requires 
        extend the matrix by the bc and still be a square matrix
        """
        #get tridiag coefficient for boundary conditions
        if len(self.phi)==0:
            a_w,_,_ = self._make_tridiag_coeff(self.phi_boundary_arr)
        else: 
            a_w,_,_ = self._make_tridiag_coeff(self.phi[-1])
        a_w = a_w[0]
        a_e = a_w
        #concatenating columns
        bc_l = np.zeros((self.nSlices,1))
        bc_r = np.zeros((self.nSlices,1))
        bc_l[0,0] = a_w
        bc_r[-1,0] = a_e
        tridiag_bc = np.concatenate((bc_l,tridiag,bc_r),axis=1)
        #concatenating rows
        upper_row = np.zeros((1,self.nSlices+2))
        lower_row = upper_row.copy()
        upper_row[0,0] = self._derivative_dw_dphi(self.phi_boundary)*self.dx**2/self.dt
        lower_row[0,-1] = self._derivative_dw_dphi(self.phi_boundary)*self.dx**2/self.dt
        tridiag_bc = np.concatenate((upper_row,tridiag_bc,lower_row),axis=0)
        return tridiag_bc


    def test_tridiag(self):
        phi = 0.6 * np.ones(self.nSlices)
        tridiag = self._make_tri_diag(phi)
        return tridiag

    def solve(self):
        ibc = self._initial_and_boundary_conditions()
        tridiag = self._make_tri_diag(self.phi_initial_arr)
        # print(ibc)
        #print("Tridiag is: {}".format(tridiag))
        # print(ibc.shape)
        # print(tridiag.shape)
        for step in range(0,86400):
            if step == 0:
                next_phi = np.linalg.solve(tridiag,ibc)
                self.phi.append(next_phi)
            else:
                tridiag = self._make_tri_diag(self.phi[-1][1:-1])
                b = self.phi[-1]*self._derivative_dw_dphi(self.phi[-1])*self.dx**2/self.dt
                next_phi = np.linalg.solve(tridiag,b)
                self.phi.append(next_phi)
            #print("Tridiag is: {}".format(tridiag))
        
        return self.phi

        # print("u at start is: ",ibc)
        # print("next phi is: ",next_phi)
        # print(type(ibc))
        # print(type(next_phi))
        return ibc,next_phi
        


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
        a_w = np.reshape(a_w, (a_w.shape[0],))
        a_p = np.reshape(a_p, (a_p.shape[0],))
        a_e = np.reshape(a_e, (a_e.shape[0],))
        return np.diag(a_w, k1) + np.diag(a_p, k2) + np.diag(a_e, k3)

    def _make_tridiag_coeff(self,phi):
        """
        Returns the coefficients for the tridiagonal matrix. They are dependent on the last/current phi.
        Mind that we had a wrong sign in our calculation and we took the signs from Künzel et. al.
        """
        phi_w = phi[1:]
        phi_p = phi
        phi_e = phi[:-1]
        #a_w = (self._calc_D_phi(phi_w) * (self.d/self.dx) + self._calc_p_sat() * self.delta_pw * (self.d/self.dx))
        #a_p = -(2*self._calc_D_phi(phi_p) * (self.d/self.dx) + 2*self._calc_p_sat() * self.delta_pw * (self.d/self.dx) - self._derivative_dw_dphi(phi_p) * (self.d*self.dx/self.dt))
        #a_e = (self._calc_D_phi(phi_e) * (self.d/self.dx) + self._calc_p_sat() * self.delta_pw * (self.d/self.dx))
        a_w = -(self._calc_D_phi(phi_w)+self._calc_p_sat()*self.delta_pw)
        a_p = self._derivative_dw_dphi(phi_p)*self.dx**2/self.dt + 2*(self._calc_D_phi(phi_p)+self._calc_p_sat()*self.delta_pw)
        a_e = -(self._calc_D_phi(phi_e)+self._calc_p_sat()*self.delta_pw)


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
            D_ws = 3.8 * (self.A / self.w_f[0])**2 * 1000**(w/(self.w_f[0])-1) 
        else:
            D_ws = 3.8 * (self.A / self.w_f[1])**2 * 1000**(w/(self.w_f[1]-1)) 

        return D_ws

    def _calc_D_phi(self,phi):
        """
        Calculate "Flüssigleitkoeffzient" D_phi = D_w * dw/dphi [kg/ms]
        """
        w = self._rf_to_h2o_content(phi)
        D_ws = self._calc_D_ws(w)
        dw_dphi = self._derivative_dw_dphi(phi)
        D_phi = D_ws * dw_dphi

        return D_phi




