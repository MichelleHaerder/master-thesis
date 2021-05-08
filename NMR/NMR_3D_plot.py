import os
import numpy as np
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import pprint

verbose = True
pp = pprint.PrettyPrinter(indent=4)

importPath = "Result_data/avg_result"
#importFolder = "3DF5580"
importFolder = sorted(os.listdir(importPath))
if not os.path.exists(os.path.join(importPath,"avgPlots")):
        if verbose:
            print('Creating folder ' + importPath + "/Plots")
        os.makedirs(os.path.join(importPath,"Plots"))

for iF in importFolder:
    avgFiles = sorted(os.listdir(os.path.join(importPath,iF)))
    distFromOrigin = []
    avgData = np.array([])
    #avgData_append = np.array([])
    for i,aF in enumerate(avgFiles):
        if i == 0:
            distFromOrigin = np.genfromtxt(os.path.join(importPath,iF,aF),delimiter=',')[:,0]
            avgData = np.array(np.genfromtxt(os.path.join(importPath,iF,aF),delimiter=',')[:,1])
        else:
            avgData = np.column_stack((avgData,np.array(np.genfromtxt(os.path.join(importPath,iF,aF),delimiter=',')[:,1])),)
            
    avgData = np.swapaxes(avgData,1,0)

    #plottype 3D
    fig = plt.figure()
    timesteps = avgData.shape[0]
    accTimesteps = [0,2,4,7,10,15,17,21,31,36]
    ax = Axes3D(fig)
    interval = np.ones(avgData.shape[1])
    plt.title("Feuchteverlauf "+ iF)
    plt.xlabel("Probenlänge [mm]")
    plt.ylabel("Zeitschritt[d]")
    #for t in range(timesteps):                                                                                                                                                                                                                                                                                                             
        #ax.scatter(distFromOrigin,(t+1)*interval,avgData[t,:],label="interval="+str(accTimesteps[i]),s=0.5)
    for i,t in enumerate(accTimesteps):
        ax.scatter(distFromOrigin,accTimesteps[i]*interval,avgData[i,:],s=10)
    
    plt.savefig(os.path.join(importPath,"Plots",iF + '_3D'),dpi=300)

    #plottype 2D
    fig = plt.figure()
    plt.title("Feuchteverlauf "+ iF)
    plt.xlabel("Probenlänge [mm]")
    plt.ylabel("Wassergehalt [M.%]")
    for i,t in enumerate(accTimesteps):
        plt.scatter(distFromOrigin,avgData[i,:],label="Tag = "+str(accTimesteps[i]),s=0.5)
        plt.plot(distFromOrigin,avgData[i,:],linestyle='dashed', linewidth= 0.3, marker= ".")
    plt.legend()

    plt.savefig(os.path.join(importPath,"Plots",iF + '_2D'),dpi=300)
    
