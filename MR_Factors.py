import SloeAligneDataProcessing
import CSSMOModelDataProcessing
import MeanReversionFactorsCalc
import pandas as pd
import os

dateString = '20230424'
MRFactor = '0.2347'


def SloeAligneDataProcess(dateString,MRFactor):

    aligneInput = SloeAligneDataProcessing.readMeanRevertExcel(dateString)

    sortedData = SloeAligneDataProcessing.sortData(aligneInput)

    sAndFData = SloeAligneDataProcessing.filteredByData(sortedData)

    sAndFData = SloeAligneDataProcessing.correctedVolData(sAndFData, MRFactor)

    if all(sAndFData['1MC/2MC'] =='E_PHNL/TENNE2/SLOE/D') == False:
        
        print('Warning: not all the deals left are CSS related')

    else:
        
        print('Data Processing succeded: All deals are CSS related')

    return sAndFData

    # sAndFData.dtype.fields
    # sAndFData.dtype.names


#------------------------------------------------------------------------------------------------------------------------------

#Processing Aligne Data:

AligneData = SloeAligneDataProcess(dateString, MRFactor)

pd.DataFrame(AligneData).to_csv('C:/Users/D110148/OneDrive - pzem/Modelos y Simulaciones/Mean Reversion Factor vs Aligne/AligneData_'+dateString+'.csv')

#Processing MO Data:

MOData = CSSMOModelDataProcessing.DailyCssOptionValuation(str(int(dateString)+1))

#Calculating Extrinsic:

MOExtrinsic = MOData.Forward_Option_Css[:-12] - MOData.Forward_Intr[:-12]

months = list(set(AligneData['+1START'].astype('datetime64[M]')))
months.sort()

meanReversionFactors = MeanReversionFactorsCalc.getMeanReversionFactorArray(months, AligneData, MOExtrinsic)

pd.DataFrame({'MeanRevertFactors': meanReversionFactors}).to_csv('C:/Users/D110148/OneDrive - pzem/Main/Risk Management OTS/Mean Reversion Aligne/MeanReversionFactors.csv')

print(os.getcwd())

