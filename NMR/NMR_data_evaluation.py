import numpy as np
import csv
import os
import math
from FunctionsCollection import read_data

#Define Paths for import and export
importFolder = "Processed_data" 
folderName = "3163_105_55_3DF" #adjust
exportFolder = 'Result_data'
exportPath = os.path.join(exportFolder,folderName)

#create folder with name exportPath if folder doesnt exist
if not os.path.exists(exportPath):
    os.mkdir(exportPath)

#Should the h20 file also be corrected?
h20Path = os.path.join(importFolder,folderName,'h2o.csv')
_,_,_,AbsValueH2o = read_data(h20Path)
tSteps2Analyse = range(1,4)
meanH2o = np.mean(AbsValueH2o[tSteps2Analyse])

allSlices = os.listdir(os.path.join(importFolder,folderName))
for theSlice in allSlices:
    if not ".csv" in theSlice:
        allSlices.remove(theSlice)
    if 'h2o'in theSlice:
        allSlices.remove(theSlice)
allSlices = sorted(allSlices)
#print(allSlices)
#allMeans is a dictionary
allMeans = {}
sliceThickness = 5 # in mm
for counter, theSlice in enumerate(allSlices):
    importPath = os.path.join(importFolder,folderName,theSlice)
    _,_,_,AbsValue = read_data(importPath)
    mean = np.mean(AbsValue[tSteps2Analyse])
    allMeans[theSlice] = [counter*sliceThickness, mean]

fileName = folderName
fieldNames = ['Dist from origin [mm]','mean of absValue [nT]']

#******************Include the metadata in the future as header in csv
# metadata = {'Experiment ID'        : folderName,
#             'Sample Type'          : 'NF',
#             'Slice Thickness in mm': sliceThickness
#             }
# for key, value in metadata.items():
#     print (key, value)
#******************

#write absValue of samples into csv
with open(os.path.join(exportFolder,folderName,'meanValues.csv'),'w',newline='') as csvfile:
    writer = csv.DictWriter(csvfile,fieldnames=fieldNames)
    writer.writeheader()
    for key, value in allMeans.items():
        writer.writerow({'Dist from origin [mm]':value[0],'mean of absValue [nT]':value[1]})

#write abs value of h2o into csv
h2oDict = {'wassermessung':[0,meanH2o]}
with open(os.path.join(exportFolder,folderName,'meanValuesH2o.csv'),'w',newline='') as csvfile:
    writer = csv.DictWriter(csvfile,fieldnames=fieldNames)
    writer.writeheader()
    for key, value in h2oDict.items():
        writer.writerow({'Dist from origin [mm]':value[0],'mean of absValue [nT]':value[1]})

#Compute volume

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

#note that here the volume is constant. In general, it can vary and the code must be adapted in the future
meansPVol = absValue / V_sample

h2oAbsValue = []
for key, value in h2oDict.items():
    h2oAbsValue.append(value[1])
h2oAbsValue = np.array(h2oAbsValue)
meanPVolH2o = h2oAbsValue / V_h2o

#compute the water content in slices [Vol %]
h2o_content = meansPVol / meanPVolH2o * 100

data2export = np.column_stack((distFromOrigin,h2o_content))
np.savetxt(os.path.join(exportPath,'h2o_content.csv'),data2export,delimiter=',')
# with open(os.path.join(exportPath,'h2o_content.csv'), 'a', newline ='') as csvfile:
#         writer = csv.writer(csvfile, delimiter = '\t')
#         #writer.writerow(['Dist from Origin [mm]','h2o content [Vol. %]'])
#         writer.writerows(data2export)
