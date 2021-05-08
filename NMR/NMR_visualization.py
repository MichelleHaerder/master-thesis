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
    importFolder = "Result_data/indi_result" 
    exportFolder = 'Result_data/indi_result'
    exportPath = os.path.join(exportFolder,folderName,"Plots")
    if not os.path.exists(os.path.join(exportPath)):
        if verbose:
            print('Creating folder ' + exportPath)
        os.makedirs(exportPath)
    
    #plots with mm, Vol.% and mm, M.%
    #Sufix for visualization files
    plotList = ['_vol','_m']
    titleList = ['[Vol.%]' , '[M.%]']
    for i,sufix in enumerate(plotList):
        fileName = 'h2o_content' + sufix + '.csv'
        filePath = os.path.join(importFolder,folderName,experimentFolder,fileName)

        plotName = folderName + "_" + experimentFolder + sufix + '.png'
        figureTitle = 'H2O content ' + titleList[i] + ' in experiment ' + folderName + "_" + experimentFolder

        #load data from 
        data = np.genfromtxt(filePath,delimiter=',')
        plt.plot(data[:,0],data[:,1],label=folderName, linestyle='dashed', linewidth= 0.2, marker= ".")
        plt.scatter(data[:,0],data[:,1],s=0.5)
        plt.title(figureTitle)
        plt.ylabel('Wassergehalt {}'.format(titleList[i]))
        plt.xlabel('Probenlänge [mm]')
        plt.legend()

        if figureDontSave:
            if verbose:
                print('Figure will not be saved as figureDontSave is True')
        else:
            plt.savefig(os.path.join(exportPath,plotName),dpi=figResolution)
            if verbose:
                print('Figure saved at ' + os.path.join(exportPath,'plots',plotName), ' .')

        if saveToFrontFolder:
            plt.savefig(os.path.join('Plots',plotName),dpi=figResolution)
            if verbose:
                print('Figure saved at ' + os.path.join('Plots',plotName), ' .')

        if figureHide:
            if verbose:
                print('Figure will not be shown as figureHide is True')
        else:
            plt.show()
        plt.close()

    #plot with mm, M.% and rel humidity
    #get data from
    #fileName = 'rel_humidity.csv'
    #filePath = os.path.join(importFolder,folderName,experimentFolder,fileName)
    #data = np.genfromtxt(filePath,delimiter=',')

    #fig, ax1 = plt.subplots()
    #ax2 = ax1.twinx()

    #ax1.set_xlabel("Distance from origin in [mm]")
    #ax1.set_ylabel("H2O content in [M.%]")
    #ax1.plot(data[:,0],data[:,1],linewidth= 0.2, linestyle= "dashed")
    #ax1.scatter(data[:,0],data[:,1],marker="x")
    #figureTitle = 'H2O content and relative humidity in experiment ' + folderName + "_" + experimentFolder
    #ax1.title[figureTitle]

    #ax2.set_ylabel("Relative Humidity in [%]")
    #ax2.plot(data[:,0],data[:,2], alpha=1)

    #fig.tight_layout()

    #save plots
    #plotName = folderName + "_" + experimentFolder + '_rel_humidity.png'
    #if figureDontSave:
        #if verbose:
            #print('Figure will not be saved as figureDontSave is True')
    #else:
        #plt.savefig(os.path.join(exportPath,plotName),dpi=figResolution)
        #if verbose:
            #print('Figure saved at ' + os.path.join(exportPath,'plots',plotName), ' .')

    #if saveToFrontFolder:
        #plt.savefig(os.path.join('Plots',plotName),dpi=figResolution)
        #if verbose:
            #print('Figure saved at ' + os.path.join('Plots',plotName), ' .')

    #if figureHide:
        #if verbose:
            #print('Figure will not be shown as figureHide is True')
    #else:
        #plt.show()
    #plt.close()

        
