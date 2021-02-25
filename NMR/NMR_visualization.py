import csv
import matplotlib.pyplot as plt
import numpy as np
import os


#get paths
importFolder = "Result_data" 
folderName = "3163_105_55_3DF" #adjust
exportFolder = 'Result_data'
exportPath = os.path.join(exportFolder,folderName)
if not os.path.exists(os.path.join(exportPath,'plots')):
    os.mkdir(os.path.join(exportPath,'plots'))

fileName = 'h2o_content.csv'
filePath = os.path.join(importFolder,folderName,fileName)
#load data from 
data = np.genfromtxt(filePath,delimiter=',')#, names=True, dtype=None, encoding=None)
plt.plot(data[:,0],data[:,1])
#plt.show()
plotName = folderName + '_01.png'
plt.savefig(os.path.join(exportPath,'plots',plotName),dpi=300)

