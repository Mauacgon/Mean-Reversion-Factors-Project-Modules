import pandas as pd
import numpy as np
import datetime

def readMeanRevertExcel(dateString):

    date = pd.to_datetime(dateString)

    if date.day < 10:
        day = '0'+str(date.day)
    else:
        day = str(date.day)

    if date.month < 10:
        month = '0' + str(date.month)
    else:
        month = str(date.month)

    year = str(date.year)

    nameString = 'MEAN_REVER_OPT_%s_%s_%s.xls' % (day,month,year)

    data = pd.read_excel('C:/Users/D110148/OneDrive - pzem/Modelos y Simulaciones/Mean Reversion Factor vs Aligne/%s' % (nameString), skiprows=5).dropna()
    
    return data.to_records(index=False)

def sortData(aligneInput):
    
    sort_indices = np.lexsort((aligneInput['+1START'],aligneInput['TNUM']))
    
    data = aligneInput[sort_indices]
    
    return data

def filteredByData(sortedData):
    
    firstOcc, firstOccInd = np.unique(sortedData['+1START'], return_index= True)
    datetimes = firstOcc.astype('datetime64[D]')
    weekDay = np.is_busday(datetimes)
    secondOccInd = np.array([firstOccInd[i]+1 for i in range(len(firstOcc)) if weekDay[i] == True])

    allIndices = np.concatenate((firstOccInd,secondOccInd))
    allIndices.sort()

    data = sortedData[allIndices]
    
    return data

def correctedVolData(sAndFData, MRFactor):
    
    sAndFData['+MOD VOL1'] = np.array([[i/float(MRFactor)] for i in sAndFData['+MOD VOL1']]).reshape(sAndFData.shape[0],)
    sAndFData['+MOD VOL2'] = np.array([[i/float(MRFactor)] for i in sAndFData['+MOD VOL2']]).reshape(sAndFData.shape[0],)
    
    return sAndFData
    
