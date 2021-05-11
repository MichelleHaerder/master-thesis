# Investigation of hygric properties of clay

## Overview
The search for concrete substitutes is an ongoing research field. Clay is a promising candidate. However, its mechanical properties are heavily dependent on moisture content. Since the physical processes of moisture transport in the case of clay are not fully understood, it is imperative to find suitable models that explain its hygric behavior.
The chosen ansatz is to take an existing moisture transport model that has been validated for other porous materials and find fitting parameters for clay. In particular, the model consist of a coupling of moisture and heat transport, as used by [Fraunhofer's WUFI software](https://wufi.de/literatur/K%C3%BCnzel%201995%20-%20Simultaneous%20Heat%20and%20Moisture%20Transport.pdf).
This repository contains the coding part of my master's thesis. It is split into 2 main folders.
* NMR: a pipeline that automates processing and plotting of data obtained in Nuclear Magnetic Resonance tests. 
* Feuchtemodell: 1D FVM (finite volume method) model of moisture and heat transport for clay.


## Requirements

The code is based only on Python and Anaconda was used to create a virtua environment (not necessary, but recommended). Once Anaconda is installed, the environment can be directly imported from the [environment.yml](https://github.com/MichelleHaerder/master-thesis/blob/main/config/environment.yml) file.

## Usage

### NMR

[nmr_analysis.py](https://github.com/MichelleHaerder/master-thesis/blob/main/NMR/nmr_analysis.py) is the main file to be executed to process data acquired from Nuclear Magnetic Resonance tests. It provide flags to customize data processing. For a detailed list of the flags, type python `nmr_analysis.py -h`.

Raw data is taken in as `.csv` and need to be placed in a folder named *Raw_data*. If the folder does not exist, please create one.

The folder structure inside *Raw_data* is:
* folder, e.g. "3_3DF_55_80", which corresponds to *<sampleNr_clayType_initHumidity_finalHumidity>*
  * folder e.g. "3271", which corresponds to *<testNr>*
    * folder "Experiment...Lehm_3DF", which contains the nmr slice samples.
      * one `.csv` per slice
    * folder "Experiment...Folie", which contains a nmr measurement of the foil.
      * one `.csv` for the foil
    * folder "Experiment...H2O", which contains a nmr measurement of water.
      * one `.csv` for the foil
    * folder "Experiment...Lehm_leer", t.b.d.
      * one `.csv` t.b.d.

Keep in mind that modifying the folder structure requires making changes in the code.

avg_plots require calling other scripts (t.b.d)
3D plots require calling other scripts (t.b.d.)

###Feuchtemodell
t.b.d.

## Results

Insert some avg resiöts



