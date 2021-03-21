import numpy as np
import os

def nmr_rel_humidity(folderName, experimentFolder):

    #get paths
    importFolder = 'Sorptionsisotherme'
    folderInitials = folderName.split('_')[1]
    if folderInitials == 'NF' :
        fileName = 'Sorptionsisotherme_NF.csv'
        importPath = os.path.join(importFolder,fileName)
    else:
        fileName = 'Sorptionsisotherme_3DF.csv'
        importPath = os.path.join(importFolder,fileName)
    importFolderH2o = 'Result_data'
    importFileH2o = 'h2o_content_m.csv'
    importPathH2o = os.path.join(importFolderH2o,folderName,experimentFolder,importFileH2o)
    exportPath = os.path.join(importFolderH2o,folderName,experimentFolder)

    #get Sorptionsisotherme
    data = np.genfromtxt(importPath, delimiter=';', skip_header=1)
    dataIncreasing = data[0:20]
    dataDecreasing = data[19:]
    folderInitials2 = folderName.split("_")[2]
    folderInitials3 = folderName.split("_")[3]
    activeData = []
    if int(folderInitials2) < int(folderInitials3):
        activeData = dataIncreasing
    else:
        activeData = dataDecreasing

    #get M.% data 
    h2o_content_m = np.genfromtxt(importPathH2o, delimiter=',', skip_header=0)
    distFromOrigin = h2o_content_m[:,0]s
    h2o_content_m = h2o_content_m[:,1]

    #interpolate relative humidity from Sorptionsisotherme
    relHumid = np.interp(h2o_content_m,activeData[:,1],activeData[:,0])

    #save relative humidity as csv
    data2export = np.column_stack((distFromOrigin,h2o_content_m,relHumid))
    np.savetxt(os.path.join(exportPath,'rel_humidity.csv'),data2export,delimiter=',')


