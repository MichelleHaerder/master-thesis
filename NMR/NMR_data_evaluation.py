import numpy as np
import csv
import os
from FunctionsCollection import read_data

#Should the h20 file also be corrected?
h20Path = "/home/stefan/Documents/MHMA/NMR/Raw_data/3147_105_55/Experiment_20210219112328582_3147_Lehm_H2O/echo_train_slice_001.csv"
_,_,_,AbsValueH2o = read_data(h20Path)
tSteps2Analyse = range(1,4)
meanH2o = np.mean(AbsValueH2o[tSteps2Analyse])
#take paths here
folderPath = "Processed_data/" 
folderName = "3147_105_55_corrected" #adjust
exportFolder = 'Result_data'
exportPath = exportFolder + '/' + folderName + '_evaluated'


if not os.path.exists(exportPath):
    os.mkdir(exportPath)

allSlices = os.listdir(folderPath + folderName)
for theSlice in allSlices:
    if not ".csv" in theSlice:
        allSlices.remove(theSlice)
allSlices = sorted(allSlices)
print(allSlices)
#THis code will be repeated for all slices
allMeans = []
_,_,_,AbsValue = read_data(currentCSVPath)

mean = np.mean(AbsValue[tSteps2Analyse])
#print(mean)


