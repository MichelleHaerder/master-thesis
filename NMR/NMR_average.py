import numpy as np
import os
import pprint

import matplotlib.pyplot as plt 
from mpl_toolkits import mplot3d

pp = pprint.PrettyPrinter(indent=4)
verbose = True

# Paths
importPath = 'Result_data'
exportFolder = '_avg_result'
exportPath = os.path.join(importPath,exportFolder)
# Create _avg_result folder
if not os.path.exists(os.path.join(exportPath)):
        if verbose:
            print('Creating folder ' + exportPath)
        os.makedirs(exportPath)

#get data
listAllResultFolders = os.listdir(importPath)
d = {'NF5580': [],
     'NF8055': [],
     #'NF055' : [],
     '3DF5580': [],
     '3DF8055': [],
     #'3DF055' : []
    }
blackList = ["1","1q","2","4q","6","7","8b","11"]

for rF in listAllResultFolders:

    fInitials = ''.join(rF.split("_")[1:])
    sampleN = rF.split('_')[0]
    if fInitials in d and not sampleN in blackList:
        d[fInitials].append(rF)



#currentList = d['NF5580']

currentData = []
distFromOrigin = []
for key in d: 
    nTimeSeries = len([item for item in os.listdir(os.path.join(importPath,d[key][0])) if not item=='Plots'])
    for timeSeries in range(4):
        
        for i,currentElement in enumerate(d[key]):
            currentElementChildren = sorted([item for item in os.listdir(os.path.join(importPath,currentElement)) if not item=='Plots'])
            if i == 0:
                currentData = np.genfromtxt(os.path.join(importPath,currentElement,currentElementChildren[timeSeries],'h2o_content_m.csv'),delimiter=',')
            else:
                currentData = np.column_stack((currentData,np.genfromtxt(os.path.join(importPath,currentElement,currentElementChildren[timeSeries],'h2o_content_m.csv'),delimiter=',')[:,1]))

            currentMean = np.array([currentData[:,0],np.mean(currentData[:,1:],axis= 1)])
            currentMean = np.swapaxes(currentMean,1,0)

            currDataName = key + "_" + str(timeSeries) + ".csv"

            # Create _avg_result folder
            if not os.path.exists(os.path.join(exportPath,key)):
                if verbose:
                    print('Creating folder ' + exportPath+key)
                os.makedirs(os.path.join(exportPath,key))

            np.savetxt(os.path.join(exportPath,key,currDataName),currentMean,delimiter=',')
                

