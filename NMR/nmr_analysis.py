import argparse

from NMR_data_processing import nmr_data_processing

def Main():
    #init parser
    parser = argparse.ArgumentParser(description='This script phase-corrects NMR samples, evaluate water content. visualizes results and saves plots.')
    #add positional arguments
    parser.add_argument('foldername', action='store',type=str, help='Name of experiment folder, e.g. 3146_105_55_NF')
    #add optional arguments
    parser.add_argument('-v','--verbose',action='store_true',help= 'Outputs readable information about code to terminal on runtime')
    #parse
    args = parser.parse_args()
    #unpack
    verbose = args.verbose
    #run scripts with arguments from parser
    if verbose:
        print('executing nmr_data_processing with foldername '+args.foldername+"...\n")
    nmr_data_processing(args.foldername,args.verbose)

    if verbose:
        print('We are done here.')
if __name__ == '__main__':
    Main()