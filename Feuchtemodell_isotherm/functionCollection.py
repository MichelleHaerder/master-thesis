import numpy as np
import math

def rf_to_h2o_content(phi,is_increasing=True):
    """
    Maps relative humidity [-] to water content in [kg/m³] using the curve fitting described in Künzel et. al.
    correction factor: b_ad = 1.55379379, b_de = 2.4556701
    adjusted free water saturation only for fitting "Sorptionsisotherme": a_ad = 109.60291049, a_de = 108.87296769
    """
    a = (109.60291049, 108.87296769) # adjusted free water saturation (a_ad, a_de)
    b = (1.55379379, 2.4556701)  # correction factor (b_ad, b_de)
    if is_increasing:
        w = a[0]*(b[0]-1)*np.array(phi)/(b[0]-np.array(phi))
    else:
        w = a[1]*(b[1]-1)*np.array(phi)/(b[1]-np.array(phi))

    return w

def derivative_dw_dphi(phi,is_increasing=True):
    """
    Derivative of "Feuchtespeicherfunktion" [kg/m³].
    Returns the gradient for dw/dphi at given phi.
    """
    a = (109.60291049, 108.87296769) # adjusted free water saturation (a_ad, a_de)
    b = (1.55379379, 2.4556701)  # correction factor (b_ad, b_de)
    if is_increasing:
        dw_dphi = a[0]*((b[0]-1) * (b[0]-phi) + (b[0]-1)*phi) / (b[0]-phi)**2
    else:
        dw_dphi = a[1]*((b[1]-1) * (b[1]-phi) + (b[1]-1)*phi) / (b[1]-phi)**2

    return dw_dphi


def _calc_D_ws(w):
    """
    Calculate "Kapillartransportkoeffizient für den Saugvorgang" [m²/s]
    Needs water content of last/current step.
    """
    w_f = 274.175 # free water saturation [kg/m3]
    A = 0.0247126 # Wasseraufnahmekoeffizient [kg/m2s0.5]
    D_ws = 3.8 * (A / w_f)**2 * 1000**(w/w_f-1) 

    return D_ws

def calc_D_phi(phi, is_increasing=True):
    """
    Calculate "Flüssigleitkoeffzient" D_phi = D_w * dw/dphi [kg/ms]
    """
    w = rf_to_h2o_content(phi,is_increasing)
    D_ws = _calc_D_ws(w)
    dw_dphi = derivative_dw_dphi(phi,is_increasing)
    D_phi = D_ws * dw_dphi

    return D_phi

def make_tridiag(F,tridiagDim):
    """tridiagDim excludes the extension."""
    A = np.zeros((tridiagDim+2, tridiagDim+2))
    for i in range(1, tridiagDim+1):
        A[i,i-1] = -F[i-1]
        A[i,i+1] = -F[i+1]
        A[i,i] = 1 + 2*F[i]
    A[0,0] = A[tridiagDim+1,tridiagDim+1] = 1
    #A[0,1] = -F[i+1]
    #A[-1,-2] = -F[i+1]
    return A