import argparse
import os

from NMR_data_processing import nmr_data_processing
from NMR_data_evaluation import nmr_data_evaluation
from NMR_visualization import nmr_visualization
from NMR_rel_humidity import nmr_rel_humidity
from clear import clear_folders

def Main():
    #init parser
    parser = argparse.ArgumentParser(
                        description='This script phase-corrects NMR samples, evaluates water content. visualizes results and saves plots.')
    #add positional arguments
    parser.add_argument('-fn','--folderName', action='store',type=str, nargs='*',
                        help='any number of Name(s) of experiment folder(s). Seperated by a space, e.g. <1_NF_105_55 2_3DF_55_80>.')
    #add positional arguments
    parser.add_argument('-ef','--experimentFolder', action='store',type=str, nargs='*',
                        help='any number of Name(s) of experiment folder(s). Seperated by a space, e.g. <3325 3146>.')
    #add optional arguments    print(args.folderName)
    parser.add_argument('-v','--verbose',action='store_true', 
                        help= 'Outputs readable information about code to terminal on runtime.')
    parser.add_argument('-fh','--figureHide',action='store_true', 
                        help='If this flag is used, the figure will not be shown.')
    parser.add_argument('-fds','--figureDontSave',action='store_true', 
                        help='If this flag is used, the figure will not be saved.')
    parser.add_argument('-ps','--peakSelection', nargs=2,action='store',type=int, 
                        help='choose min and max peaks to analyze. Arguments are seperated by a space. E.g. -tsteps 1 5. Default is 2 5. Means 2,3,4 are used.')
    parser.add_argument('-fr','--figureResolution',action='store',type=int, 
                        help='Resolution chosen for plot. Default is 300 dpi. Note that if not specified the figure will be overwritten.')
    parser.add_argument('-cf','--clearFolders',action='store_true',
                        help='Removes ALL content from the Result_data and Processed_data folders. Raw_data IS NOT Touched.')
    parser.add_argument('-stff','--saveToFrontFolder',action='store_true',
                        help='Will also save plots on NMR/Plots')

    #parse
    args = parser.parse_args()
    
    
    #checking if front Plot folder exists
    if not os.path.exists('Plots'):
        if args.verbose:
            print('Creating /Plots folder in NMR')
        os.mkdir('Plots')
    #check if folderNames is used or not to load all folders
    RawDataPath = 'Raw_data'
    if args.folderName is None:
        if args.verbose:
            print('No folderNames were specified. Using all folders in Raw_data...')
        args.folderName = [ item for item in os.listdir(RawDataPath) if os.path.isdir(os.path.join(RawDataPath, item)) ]

    #check for the error when experiment folders are specified and we dont have exactly one foldername
    if not len(args.folderName) == 1 and args.experimentFolder is not None:
        parser.error( "Don't get too fancy: \n --exprimentFolder can only be specified within exactly one --folderName. \n Try again...")
        
    #Clearing folder content if clearFolders is selected
    if args.clearFolders:
        if args.verbose:
            print('Clearing Content of folders Result_data and Processed_data...')
        clear_folders()
    if args.verbose:
        print('Starting NMR experimemt evaluation with '+str(len(args.folderName))+' experiments.')
        print('List of experiments for NMR Evaluation:')
    
    #Setting default values for args
    if args.peakSelection is None:
        args.peakSelection = [2,5]
    # if args.plotName is None:
    #     args.plotName = fN+'_01.png'
    if args.figureResolution is None:
        args.figureResolution = 300
    if args.figureHide is None:
        args.figureHide = False
    if args.figureDontSave is None:
        args.figureDontSave = False
    #outer loop that iterates over all experiments
    for i,fN in enumerate(args.folderName):
        if args.experimentFolder is None or i>0:
            fNPath = os.path.join(RawDataPath,fN)
            if args.verbose:
                print('No experimentFolders were specified. Using all folders in ' + args.folderName[0])
            args.experimentFolder = [ item for item in os.listdir(fNPath) 
                                    if (os.path.isdir(os.path.join(fNPath, item)) and not item == "Plots")]
            args.experimentFolder = sorted(args.experimentFolder)

        for counter,eF in enumerate(args.experimentFolder):
            #run scripts with arguments from parser
            #run nmr_data_processing
            if args.verbose:
                print('Executing nmr_data_processing with foldername ' + fN + "_" + eF + '...\n')
            nmr_data_processing(fN,eF,args.verbose)

            #run nmr_data_evaluation
            if args.verbose:
                print('Executing nmr_data_evaluation with foldername ' + fN + "_" + eF + '...\n')
            nmr_data_evaluation(fN, eF, args.verbose, args.peakSelection)

            #run nmr_rel_humidity
            if args.verbose:
                print('Executing nmr_rel_humidity with foldername ' + fN + "_" + eF + '...\n')
            nmr_rel_humidity(fN, eF, counter)

            #run nmr_visualization
            if args.verbose:
                print('Executing nmr_data_visualization with:')
                print('plotName = ',args.plotName)
                print('figureResolution = ',args.figureResolution)
            nmr_visualization(fN,  
                            eF,
                            args.figureResolution,
                            args.figureHide,
                            args.figureDontSave,
                            args.saveToFrontFolder,
                            args.verbose)

    if args.verbose:
        print('We are done here.')
if __name__ == '__main__':
    Main()