import numpy as np
import matplotlib.pyplot as plt 
from mpl_toolkits import mplot3d

#data

importPath = "Result_data/_avg_result"
importFolder = "3DF5580"

h2o_content_m = np.genfromtxt(importPathH2o, delimiter=',', skip_header=0)
distFromOrigin = h2o_content_m[:,0]
h2o_content_m = h2o_content_m[:,1]

ax = plt.axes(projection='3d')



plt.show()