import csv
import matplotlib.pyplot as plt
import numpy as np
import os

def nmr_visualization(folderName,
                    experimentFolder,
                    figResolution,
                    figureHide,
                    figureDontSave,
                    saveToFrontFolder,
                    verbose
                    ):


    #get paths
    importFolder = "Result_data" 
    exportFolder = 'Result_data'
    exportPath = os.path.join(exportFolder,folderName,"Plots")
    if not os.path.exists(os.path.join(exportPath)):
        if verbose:
            print('Creating folder ' + exportPath)
        os.makedirs(exportPath)

    #Preparation for plot [Vol.%]
    fileName_vol = 'h2o_content_vol.csv'
    filePath_vol = os.path.join(importFolder,folderName,experimentFolder,fileName_vol)

    plotName_vol = folderName + "_" + experimentFolder + '_vol' + '.png'
    figureTitle_vol = 'H2O content [Vol.%] in experiment ' + folderName + "_" + experimentFolder

    #load data from 
    data_vol = np.genfromtxt(filePath_vol,delimiter=',')
    plt.plot(data_vol[:,0],data_vol[:,1],label=folderName)
    plt.title(figureTitle_vol)
    plt.ylabel('H2O content in [Vol. %]')
    plt.xlabel('Distance from origin in [mm]')
    plt.legend()

    if figureDontSave:
        if verbose:
            print('Figure will not be saved as figureDontSave is True')
    else:
        plt.savefig(os.path.join(exportPath,plotName_vol),dpi=figResolution)
        if verbose:
            print('Figure saved at ' + os.path.join(exportPath,'plots',plotName_vol), ' .')

    if saveToFrontFolder:
        plt.savefig(os.path.join('Plots',plotName_vol),dpi=figResolution)
        if verbose:
            print('Figure saved at ' + os.path.join('Plots',plotName_vol), ' .')

    if figureHide:
        if verbose:
            print('Figure will not be shown as figureHide is True')
    else:
        plt.show()
    plt.close()

    #Preparation for plot [M.%]
    fileName_m = 'h2o_content_m.csv'
    filePath_m = os.path.join(importFolder,folderName,experimentFolder,fileName_m)

    plotName_m = folderName + "_" + experimentFolder + '_m' + '.png'
    figureTitle_m = 'H2O content [M.%] in experiment ' + folderName + "_" + experimentFolder

    #load data from 
    data_m = np.genfromtxt(filePath_m,delimiter=',')
    plt.plot(data_m[:,0],data_m[:,1],label=folderName)
    plt.title(figureTitle_m)
    plt.ylabel('H2O content in [M. %]')
    plt.xlabel('Distance from origin in [mm]')
    plt.legend()

    if figureDontSave:
        if verbose:
            print('Figure will not be saved as figureDontSave is True')
    else:
        plt.savefig(os.path.join(exportPath,plotName_m),dpi=figResolution)
        if verbose:
            print('Figure saved at ' + os.path.join(exportPath,'plots',plotName_m), ' .')

    if saveToFrontFolder:
        plt.savefig(os.path.join('Plots',plotName_m),dpi=figResolution)
        if verbose:
            print('Figure saved at ' + os.path.join('Plots',plotName_m), ' .')

    if figureHide:
        if verbose:
            print('Figure will not be shown as figureHide is True')
    else:
        plt.show()
    plt.close()
