'''
Function clears all contents of Processed_data and data Results
'''
import os, shutil

def clear_folders():
    ResultDataPath = 'Result_data'
    ProcessedDataPath = 'Processed_data'
    FoldersToClean = [ResultDataPath, ProcessedDataPath]
    for ftc in FoldersToClean:
        for filename in os.listdir(ftc):
            file_path = os.path.join(ftc, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))