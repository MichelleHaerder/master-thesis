import csv
import matplotlib.pyplot as plt
import numpy as np
import os

def nmr_visualization(folderName,plotName,figResolution,figureTitle,figureHide,figureDontSave,verbose):
    #get paths
    importFolder = "Result_data" 
    exportFolder = 'Result_data'
    exportPath = os.path.join(exportFolder,folderName)
    if not os.path.exists(os.path.join(exportPath,'plots')):
        if verbose:
            print('Creating folder ' + os.path.join(exportPath,'plots'))
        os.mkdir(os.path.join(exportPath,'plots'))

    fileName = 'h2o_content.csv'
    filePath = os.path.join(importFolder,folderName,fileName)
    #load data from 
    data = np.genfromtxt(filePath,delimiter=',')
    plt.plot(data[:,0],data[:,1],label=folderName)
    plt.title(figureTitle)
    plt.ylabel('H2O content in [Vol. %]')
    plt.xlabel('Distance from origin in [mm]')
    plt.legend()
    
    if figureDontSave:
        if verbose:
            print('Figure will not be saved as figureDontSave is True')
    else:
        plt.savefig(os.path.join(exportPath,'plots',plotName),dpi=figResolution)
        print('Figure saved at ' + os.path.join(exportPath,'plots',plotName), ' .')
    
    if figureHide:
        if verbose:
            print('Figure will not be shown as figureHide is True')
    else:
        plt.show()
    
