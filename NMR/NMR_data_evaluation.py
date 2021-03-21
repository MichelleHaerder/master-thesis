import numpy as np
import csv
import os
import math
from FunctionsCollection import read_data

def nmr_data_evaluation(folderName,experimentFolder,verbose,peakSelection):
    #Define Paths for import and export
    importFolder = "Processed_data" 
    exportFolder = 'Result_data'
    exportPath = os.path.join(exportFolder,folderName,experimentFolder)
    folderInitials = folderName.split("_")[1]


    if verbose:
        print('PEAK SELECTION: '+str(peakSelection[0]+1)+'-'+str(peakSelection[1]))
    
    #create folder with name exportPath if folder doesnt exist
    if not os.path.exists(exportPath):
        if verbose:
            print('Creating folder in ',exportPath)
        os.makedirs(exportPath)
    if verbose:
        print('Calculating absValue of h2o...')
    #Should the h20 file also be corrected?
    h20Path = os.path.join(importFolder,folderName,experimentFolder,'h2o.csv')
    _,_,_,AbsValueH2o = read_data(h20Path)
    meanH2o = np.mean(AbsValueH2o[range(peakSelection[0],peakSelection[1])])
    #calculating absValue of slices
    if verbose:
        print('Calculating absValue of slices...')
    allSlices = os.listdir(os.path.join(importFolder,folderName,experimentFolder))
    for theSlice in allSlices:
        if not ".csv" in theSlice:
            allSlices.remove(theSlice)
        if 'h2o'in theSlice:
            allSlices.remove(theSlice)
    allSlices = sorted(allSlices)
    #allMeans is a dictionary
    allMeans = {}
    sliceThickness = 5 # in mm
    for counter, theSlice in enumerate(allSlices):
        importPath = os.path.join(importFolder,folderName,experimentFolder,theSlice)
        _,_,_,AbsValue = read_data(importPath)
        mean = np.mean(AbsValue[range(peakSelection[0],peakSelection[1])])
        allMeans[theSlice] = [counter*sliceThickness, mean]
    if verbose:
        print('The slices are saved in a dictionary. Here is the dictionary:\n')
        for mean in allMeans:
            print(mean,allMeans[mean])
        print('')

    fieldNames = ['Dist from origin [mm]','mean of absValue [nT]']

    #******************Include the metadata in the future as header in csv
    # metadata = {'Experiment ID'        : folderName,
    #             'Sample Type'          : 'NF',
    #             'Slice Thickness in mm': sliceThickness
    #             }
    # for key, value in metadata.items():
    #     print (key, value)
    #******************
    if verbose:
        print('Exporting absValues of slices as csv at '+os.path.join(exportFolder,folderName,experimentFolder,'meanValues.csv')+'...')
    #write absValue of samples into csv
    with open(os.path.join(exportFolder,folderName,experimentFolder,'meanValues.csv'),'w',newline='') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=fieldNames)
        writer.writeheader()
        for key, value in allMeans.items():
            writer.writerow({'Dist from origin [mm]':value[0],'mean of absValue [nT]':value[1]})

    if verbose:
        print('Exporting absValues of h2o as csv at '+os.path.join(exportFolder,folderName,experimentFolder,'meanValuesH2o.csv')+'...')
    #write abs value of h2o into csv
    h2oDict = {'wassermessung':[0,meanH2o]}
    with open(os.path.join(exportFolder,folderName,experimentFolder,'meanValuesH2o.csv'),'w',newline='') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=fieldNames)
        writer.writeheader()
        for key, value in h2oDict.items():
            writer.writerow({'Dist from origin [mm]':value[0],'mean of absValue [nT]':value[1]})

    #Compute volume
    if verbose:
        print('Computing slice volume...')
    #formula for volume of cylinder is V=pi*r²*h in mm³
    #for sample
    r_sample = 20
    h_sample = sliceThickness
    V_sample = math.pi * math.pow(r_sample,2) * h_sample
    #for h2o
    r_h2o = 20
    h_h2o = sliceThickness
    V_h2o = math.pi * math.pow(r_h2o,2) * h_h2o

    #extract absVaue from dictionary
    absValue = []
    distFromOrigin = []
    for key, value in allMeans.items():
        absValue.append(value[1])
        distFromOrigin.append(value[0])
    absValue = np.array(absValue)
    
    if verbose:
        print('Computing water content in slices in [Vol.%]')
    #note that here the volume is constant. In general, it can vary and the code must be adapted in the future
    SliceVolumeMode = 'CONSTANT'
    if verbose:
        print('note that here the slice volume is assumed to be '+SliceVolumeMode+'. Consider changing this in the future for more accuracy...')
    meansPVol = absValue / V_sample

    h2oAbsValue = []
    for key, value in h2oDict.items():
        h2oAbsValue.append(value[1])
    h2oAbsValue = np.array(h2oAbsValue)
    meanPVolH2o = h2oAbsValue / V_h2o

    #compute the water content in slices [Vol.%]
    h2o_content_vol = meansPVol / meanPVolH2o * 100
    if verbose:
        print('List containing the h2o content in [Vol.%] of every slice:\n')
        print(h2o_content_vol)
        print('')
    data2export = np.column_stack((distFromOrigin,h2o_content_vol))
    np.savetxt(os.path.join(exportPath,'h2o_content_vol.csv'),data2export,delimiter=',')



    #dry density for samples and water 
    rho_sample = 0
    if folderInitials == 'NF':
        rho_sample= 1750 #kg/m3
    elif folderInitials == '3DF':
        rho_sample = 1811 #kg/m3
    rho_h2o = 997 #kg/m3

    #compute the water content in slices [M.%]
    h2o_content_m = h2o_content_vol * rho_h2o/rho_sample
    if verbose:
        print('List containing the h2o content in [M.%] of every slice:\n')
        print(h2o_content_m)
        print('')
    data2export = np.column_stack((distFromOrigin,h2o_content_m))
    np.savetxt(os.path.join(exportPath,'h2o_content_m.csv'),data2export,delimiter=',')