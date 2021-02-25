# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 13:57:42 2019

@author: snagel1

Script for emptyfile subtraction
--------------------------------

This script reads plural NMR T2 measurement slice files as csv-files and one emptyfile.
After subtraction of the emptyfile, the new corrected data for every single slice
will be saved in a new csv-file with the same header as of the origin file. 

what to change?
---------------

SampleName/
importFolder/
OutputFolder:    name of the dataset and/or folder

"""
import argparse
import numpy as np
import os
from FunctionsCollection import read_data, saving_in_csv, create_new_csv, PhaseCorrection, SubtractionNew, readPhase
#parser stuff
# parser = argparse.ArgumentParser()
# parser.add_argument("folderName", help="name of the folder containing experiment directories")
# parser.add_argument("ExperimentKeyword",help="Mostly either 'NF' or 'DF'")

#select importFolder to import files and exportFolder to export results
importFolder = "Raw_data" 
folderName = "3147_105_55" #adjust
exportFolder = 'Processed_data'
#suffix = "_corrected"
exportPath = os.path.join(exportFolder,folderName)
allExperiments = os.listdir(os.path.join(importFolder,folderName))
folderInitials = 'NF' #or 'DF', adjust

#create export folder in process data with name exportPath if it doesnt exist already
if not os.path.exists(exportPath):
    os.mkdir(exportPath)

folderToUse = ""
for experiment in allExperiments:
    if folderInitials in experiment:
        folderToUse = experiment

#Take all .csv into list to analyse
allSlicesPath = os.path.join(importFolder,folderName,folderToUse)
allSlices = os.listdir(allSlicesPath)
for theSlice in allSlices:
    if not ".csv" in theSlice:
        allSlices.remove(theSlice)
allSlices = sorted(allSlices)

#read foil.csv
foilCSVName = 'foil.csv'
foilPath = os.path.join(importFolder,foilCSVName)
T_foil, RV_foil, IV_foil, AV_foil = read_data(foilPath)
Phase_foil = readPhase(foilPath, 'foil')
APhaseCorrected_foil = PhaseCorrection(Phase_foil, RV_foil, IV_foil)
#For loop over all slices
for theSlice in allSlices:

    ###Samplefile/ Emptyfile and folder definition
    SampleName = theSlice 
    SampleFile = os.path.join(importFolder,folderName,folderToUse,SampleName)
    T_sample, RV_sample, IV_sample, AV_sample = read_data(SampleFile)
    Phase_sample = readPhase(SampleFile, SampleName) 

    #%%foil subtraction and/or phasecorrection
    APhaseCorrected_sample = PhaseCorrection(Phase_sample, RV_sample, IV_sample)
    AFinal = SubtractionNew(APhaseCorrected_sample, APhaseCorrected_foil)

    #create exporting name
    exportName = os.path.join(exportPath,SampleName)
    print('Sample ', SampleName,': Foil subtraced and phase corrected! Exporting...\n')
        
    #%%saving
    data_final = create_new_csv(T_sample, AFinal, SampleFile, exportName)
    saving_in_csv(data_final, exportName)
    print('Sample ', SampleName,':Exported to folder ',exportPath)

print("Done")

