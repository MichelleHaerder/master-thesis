import numpy as np
from v1feuchtemodell_kiesl import FeuchteModell
from numpy.core.fromnumeric import resize
import matplotlib.pyplot as plt
import pprint
pp = pprint.PrettyPrinter(indent=4)


MyFM = FeuchteModell()
# phi = 0.5*np.ones((4,1))
# tridiag_bc = MyFM._make_tri_diag(phi)
# print(tridiag_bc)
# print(tridiag_bc.shape)
phi_arr = MyFM.solve()
print("Phi array is ")
#pp.pprint(phi_arr)

plt.figure()
plt.plot(phi_arr,label="phi")
plt.legend()
plt.show

    #plottype 3D
# plt.figure()
# plt.title("Feuchteverlauf ")
# plt.xlabel("Probenlänge [mm]")
# plt.ylabel("Zeitschritt[d]")
# for i,curr_phi in enumerate(phi_arr):
#     if i % 3600 ==0:
#         plt.plot(curr_phi)
    
# plt.show()
# w,D_ws,D_phi,dw_dphi = MyFM._calc_D_phi(0.65)
# print("w: {}, D_ws: {}, D_phi: {}, dw_dphi: {}".format(w,D_ws,D_phi,dw_dphi))

