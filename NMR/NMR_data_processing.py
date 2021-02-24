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
folderPath/
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

#select FolderPath to import files and exportFolder to export results
folderPath = "Raw_data/" 
folderName = "3147_105_55" #adjust
exportFolder = 'Processed_data'
exportPath = exportFolder + '/' + folderName + '_results'
allExperiments = os.listdir(folderPath + folderName)
folderInitials = 'NF' #or 'DF', adjust

#create export folder in process data with name exportPath if it doesnt exist already
if not os.path.exists(exportPath):
    os.mkdir(exportPath)

folderToUse = ""
for experiment in allExperiments:
    if folderInitials in experiment:
        folderToUse = experiment

#Take all .csv into list to analyse
allSlices = os.listdir(folderPath + folderName + "/" + folderToUse)
for theSlice in allSlices:
    if not ".csv" in theSlice:
        allSlices.remove(theSlice)
allSlices = sorted(allSlices)
#For loop over all slices
for theSlice in allSlices:

    ###Samplefile/ Emptyfile and folder definition
    SampleName = theSlice

    #%%reading data T = Time; RV = RealValue; IV = ImValue; AV = AbsValue 
    SampleFile = str(folderPath) + folderName + '/' + folderToUse + '/' + SampleName 
    T_sample, RV_sample, IV_sample, AV_sample = read_data(SampleFile)
    Phase_sample = readPhase(SampleFile, SampleName) 

    #%%emptyfile subtraction and/or phasecorrection

    emptyFile = str(folderPath)+ 'foil.csv'
    ###empty_001 without foil
    ###empty_002 with foil
    T_empty, RV_empty, IV_empty, AV_empty = read_data(emptyFile)
    Phase_empty = readPhase(emptyFile, 'emptyfile')
    
    APhaseCorrected_sample = PhaseCorrection(Phase_sample, RV_sample, IV_sample)
    APhaseCorrected_empty = PhaseCorrection(Phase_empty, RV_empty, IV_empty)
    
    AFinal = SubtractionNew(APhaseCorrected_sample, APhaseCorrected_empty)
    newName = str(exportPath) +'/' + str(SampleName)+ '_corrected.csv'

    APhaseCorrected_sample= PhaseCorrection(Phase_sample, RV_sample, IV_sample)
    newName = str(exportPath) +'/' +str(SampleName)+'_corrected.csv'
    print('Sample: Phase corrected!\n')
        
#%%saving
    data_final = create_new_csv(T_sample, AFinal, SampleFile, newName)
    saving_in_csv(data_final, newName)

