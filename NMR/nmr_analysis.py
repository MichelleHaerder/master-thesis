import argparse

from NMR_data_processing import nmr_data_processing
from NMR_data_evaluation import nmr_data_evaluation
from NMR_visualization import nmr_visualization
def Main():
    #init parser
    parser = argparse.ArgumentParser(
                        description='This script phase-corrects NMR samples, evaluate water content. visualizes results and saves plots.')
    #add positional arguments
    parser.add_argument('folderName', action='store',type=str, 
                        help='Name of experiment folder, e.g. 3146_105_55_NF.')
    #add optional arguments
    parser.add_argument('-v','--verbose',action='store_true', 
                        help= 'Outputs readable information about code to terminal on runtime.')
    parser.add_argument('-fh','--figureHide',action='store_true', 
                        help='If this flag is used, the figure will not be shown.')
    parser.add_argument('-fds','--figureDontSave',action='store_false', 
                        help='If this flag is used, the figure will not be saved.')
    parser.add_argument('-ps','--peakSelection', nargs=2,action='store',type=int, 
                        help='choose min and max peaks to analyze. Arguments are seperated by a space. E.g. -tsteps 1 5. Default is 1 4.')
    parser.add_argument('-pn','--plotName',action='store',type=str, 
                        help='Choose a PlotName for your plot. Default is <folderName+_01.png>.')
    parser.add_argument('-fr','--figureResolution',action='store',type=int, 
                        help='Resolution chosen for plot. Default is 300 dpi. Note that if not specified the figure will be overwritten.')
    parser.add_argument('-ft','--figureTitle',action='store',type=str, 
                        help='Title for figure. Default is <H2O content Vol.%% in experiment foldername')

    
    #parse
    args = parser.parse_args()
    #Setting default values for args
    if args.peakSelection is None:
        args.peakSelection = [1, 4]
    if args.plotName is None:
        args.plotName = '_01.png'
    if args.figureResolution is None:
        args.figureResolution = 300
    if args.figureTitle is None:
        args.figureTitle = 'H2O content [Vol.%] in experiment ' + args.folderName
    if args.figureHide is None:
        args.figureHide = False
    if args.figureDontSave is None:
        args.figureDontSave = False

    #run scripts with arguments from parser
    #run nmr_data_processing
    if args.verbose:
        print('Executing nmr_data_processing with foldername '+args.folderName+'...\n')
    nmr_data_processing(args.folderName,args.verbose)

    #run nmr_data_evaluation
    if args.verbose:
        print('Executing nmr_data_evaluation with foldername '+args.folderName+'...\n')
    nmr_data_evaluation(args.folderName, args.verbose, args.peakSelection)

    if args.verbose:
        print('Executing nmr_data_evaluation with:')
        print('plotName = ',args.plotName)
        print('figureResolution = ',args.figureResolution)
    nmr_visualization(args.folderName,
                      args.plotName,
                      args.figureResolution,
                      args.figureTitle,
                      args.figureHide,
                      args.figureDontSave,
                      args.verbose)

    if args.verbose:
        print('We are done here.')
if __name__ == '__main__':
    Main()