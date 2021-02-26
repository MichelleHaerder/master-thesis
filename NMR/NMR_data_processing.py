"""
Created on Fri Apr  5 13:57:42 2019
@author: snagel1

Adaption on Fri Feb 25 10:00:00 2021
@adapted: MichelleHaerder
          Github Repository: https://github.com/MichelleHaerder/master-thesis

nmr_data_processing: Function for NMR Phase Correction of Slice Samples
--------------------------------

This function reads plural NMR T2 measurement slice files as csv-files.
It reads the foil measurements and subtracts its phase-corrected values from the slice samples.
Also, it phase-corrects the h2o sample file
The phase-corrected slice samples are saved as csv files with raw-data header.
 
--------------------------------
Positional Arguments

folderName: Folder containing the slice, h2o and foil samples
            Structure of this folder must be <folderName> -->
                                             <folderContaining"experimentInitials">,
                                             <folderContaining"Folie">,
                                             <folderContaining"H2O">
Optional Arguments

verbose: If True prints readable info into the terminal

--------------------------------
Future work to do:

"""

import numpy as np
import os
from FunctionsCollection import read_data, saving_in_csv, create_new_csv, PhaseCorrection, SubtractionNew, readPhase

def nmr_data_processing(folderName,verbose):

    #Define import and export folders
    importFolder = "Raw_data" 
    #folderName = "3163_105_55_3DF" #adjust
    exportFolder = 'Processed_data'
    sampleFolder = ""
    foilFolder = ''
    h2oFolder = ''
    exportPath = os.path.join(exportFolder,folderName)
    allExperiments = os.listdir(os.path.join(importFolder,folderName))
    folderInitials = folderName.split("_")[-1]

    #create export folder in process data with name exportPath if it doesnt exist already
    if not os.path.exists(exportPath):
        os.mkdir(exportPath)

    for experiment in allExperiments:
        if folderInitials in experiment:
            sampleFolder = experiment
        if 'Folie'in experiment:
            foilFolder = experiment
        if 'H2O' in experiment:
            h2oFolder = experiment

    #Take all .csv into list to analyse
    allSlicesPath = os.path.join(importFolder,folderName,sampleFolder)
    allSlices = os.listdir(allSlicesPath)
    for theSlice in allSlices:
        if not ".csv" in theSlice:
            allSlices.remove(theSlice)
    allSlices = sorted(allSlices)

    #read, correct and save foil.csv
    foilFile = ""
    foilPath = os.path.join(importFolder,folderName,foilFolder)
    allFoils = os.listdir(foilPath)
    for theFoil in allFoils:
        if ".csv" in theFoil:
            foilFile = theFoil

    T_foil, RV_foil, IV_foil, AV_foil = read_data(os.path.join(foilPath,foilFile))
    Phase_foil = readPhase(os.path.join(foilPath,foilFile), 'foil',verbose)
    APhaseCorrected_foil = PhaseCorrection(Phase_foil, RV_foil, IV_foil,verbose)

    #read, correct and save h20.csv
    h2oFile = ""
    h2oPath = os.path.join(importFolder,folderName,h2oFolder)
    allH2o = os.listdir(h2oPath)
    for theH2o in allH2o:
        if ".csv" in theH2o:
            h2oFile = theH2o

    T_h2o, RV_h2o, IV_h2o, AV_h2o = read_data(os.path.join(h2oPath,h2oFile))
    Phase_h2o = readPhase(os.path.join(h2oPath,h2oFile), 'h2o',verbose)
    APhaseCorrected_h2o = PhaseCorrection(Phase_h2o, RV_h2o, IV_h2o,verbose)
    data_h2o = create_new_csv(T_h2o, APhaseCorrected_h2o, os.path.join(h2oPath,h2oFile), os.path.join(exportFolder,folderName,'h2o.csv'))
    saving_in_csv(data_h2o, os.path.join(exportFolder,folderName,'h2o.csv'))
    if verbose:
        print('H2O-Samples are corrected and saved')

    #For loop over all slice samples
    for theSlice in allSlices:

        ###Samplefile/ Emptyfile and folder definition
        SampleName = theSlice 
        SampleFile = os.path.join(importFolder,folderName,sampleFolder,SampleName)
        T_sample, RV_sample, IV_sample, AV_sample = read_data(SampleFile)
        Phase_sample = readPhase(SampleFile, SampleName,verbose) 

        #%%foil subtraction and/or phasecorrection
        APhaseCorrected_sample = PhaseCorrection(Phase_sample, RV_sample, IV_sample,verbose)
        AFinal = SubtractionNew(APhaseCorrected_sample, APhaseCorrected_foil,verbose)

        #create exporting name
        exportName = os.path.join(exportPath,SampleName)
        if verbose:
            print('Sample ', SampleName,': Foil subtraced and phase corrected! Exporting...')
            
        #%%saving
        data_Samples = create_new_csv(T_sample, AFinal, SampleFile, exportName)
        saving_in_csv(data_Samples, exportName)
        if verbose:
            print('Sample ', SampleName,': Exported to folder',exportPath,'\n')
            print('*****Processing next Sample*****\n')
    if verbose:
        print("*****Data processing completed*****\n")
        


