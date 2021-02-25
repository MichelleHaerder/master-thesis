import numpy as np
import csv
import os
from FunctionsCollection import read_data

#Should the h20 file also be corrected?
h20Path = "Raw_data/3147_105_55/Experiment_20210219112328582_3147_Lehm_H2O/echo_train_slice_001.csv"
_,_,_,AbsValueH2o = read_data(h20Path)
tSteps2Analyse = range(1,4)
meanH2o = np.mean(AbsValueH2o[tSteps2Analyse])
#take paths here
importFolder = "Processed_data" 
folderName = "3147_105_55" #adjust
exportFolder = 'Result_data'
exportPath = os.path.join(exportFolder,folderName)

#create folder with name exportPath if folder doesnt exist
if not os.path.exists(exportPath):
    os.mkdir(exportPath)

allSlices = os.listdir(os.path.join(importFolder,folderName))
for theSlice in allSlices:
    if not ".csv" in theSlice:
        allSlices.remove(theSlice)
allSlices = sorted(allSlices)
print(allSlices)
#allMeans is a dictionary
#key= sampleName, value = [distanceFromOrigin,meanAbsValue]
allMeans = {}
sliceThickness = 5 # in mm
for counter, theSlice in enumerate(allSlices):
    importPath = os.path.join(importFolder,folderName,theSlice)
    _,_,_,AbsValue = read_data(importPath)
    mean = np.mean(AbsValue[tSteps2Analyse])
    allMeans[theSlice] = [counter*sliceThickness, mean]



