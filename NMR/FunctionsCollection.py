# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 09:02:53 2019

@author: snagel1
"""
import numpy as np
import csv

  
#%%
def read_data(filename):
    """
    Reading of csv or txt files.
    Extracts time, real component, imagninary component and absolute component.
    
    """
    header = np.genfromtxt(filename, delimiter ='\t',unpack=True, max_rows = 2)
    data = np.loadtxt(filename, delimiter='\t',  skiprows = 3, unpack=True)

    time= np.array(data[0])
    realValue = np.array(data[1])
    imagValue = np.array(data[2])
    absValue = np.array(data[3])

    return  time, realValue, imagValue, absValue

#%%
def readPhase(filename, samplename):
    """
  
    """
    with open (filename) as csv_file:
        reader = csv.reader(csv_file, delimiter = '\t')
    
        for row in reader:
            phase_sample = next(reader)
            break
    
    phaseSample = phase_sample[0].split(' ')[3]
    print('Sample:', samplename)
    print('Phase:', phaseSample)
   
    return phaseSample

#%%
def PhaseCorrection(phase, RV, IV):
    """
  
    """    
    Amp_sample = np.array(RV + 1j* IV)
    PhaseCorrected = Amp_sample * np.exp(-1j*float(phase))
    print('Phase corrected!')
   
    return PhaseCorrected

#%%
def Subtraction(File1, File2, phase, i, EmptyID):
    """
  
    """
    T_1, RV_1, IV_1, AV_1 = read_data(File1)
    T_2, RV_2, IV_2, AV_2 = read_data(File2)

    ###As complex numbers
    Amp_1 = np.array(RV_1 + 1j* IV_1)
    Amp_2 = np.array(RV_2 + 1j* IV_2)
     
    ###subtraction of the emptyfile
    Amp = Amp_1 - Amp_2[0:len(Amp_1)]
    
    
    if EmptyID == True:
        
        print('Emptyfiledata for case_'+ str(i+1)+ ' subtracted!')
        
        Amp_final = Amp * np.exp(-1j*float(phase))
        print('Phase corrected!')
    
    else:
        Amp_final = Amp
        print('Subtraction complete!')
   
    return Amp_final

#%%
def SubtractionNew(Amp_1, Amp_2,):

    Amp = Amp_1 - Amp_2[0:len(Amp_1)]

    print('Subtraction complete!')
   
    return Amp

#%%
def create_new_csv (T, Amp, sampleFile, newName):
    """
    This script creates a new csv file and copies the header from the origin data file.
      
    """
    data_final= np.column_stack((T, np.real(Amp), np.imag(Amp), np.abs(Amp)))
    
    with open(sampleFile, 'r') as master, open(newName, 'w') as matched:
        cr = csv.reader(master)
        cw = csv.writer(matched, lineterminator = '\n')
        for i in range(3):
            cw.writerow(next(cr))
    
    return data_final

#%%            
def saving_in_csv (data_final, newName):    
    """
    This script opens the new csv file (created by the function 'create_new_csv') 
    and appends the corrected data (emptyfile subtracted).
      
    """

    with open(newName, 'a', newline ='')as csvfile:
        writer = csv.writer(csvfile, delimiter = '\t')
        #print(data_final)
        writer.writerows(data_final)
