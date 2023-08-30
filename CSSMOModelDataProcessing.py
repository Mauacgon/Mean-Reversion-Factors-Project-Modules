#CODE FOR DAILY BASELOAD CSS OPTION VALUATION FUNCTION #THIS IS THE ONE THAT WORKS!!

def emptyFunction():

    return 1


def DailyCssOptionValuation(date):

    import pandas as pd
    import glob
    import os
    import numpy as np
    import datetime as datetime

    def listPatternFiles(searchDir, pattern):
        files = glob.glob(os.path.join(searchDir, pattern), recursive = True)
        return files

    #Read the hourly power data:

    today = pd.to_datetime(date)
    tYear = today.year
    tMonth = today.month
    tDay = today.day
    
    strMonth = ''
    strDay = ''

    if len(str(tMonth)) < 2:
        strMonth = '0'+str(tMonth)
    else:
        strMonth = str(tMonth)

    if len(str(tDay)) < 2:
        strDay = '0'+str(tDay)
    else:
        strDay = str(tDay)

    pattern = 'Daily_'+str(tYear)+strMonth+strDay+'*HourlyReleveld.csv'    
    searchDir = 'I:/BU Portfolio Analytics/Market Analysis/Power/Models & Tools/Merit Order/PDP/Summary Outputs/'

    HourlyData = pd.read_csv(listPatternFiles(searchDir, pattern)[0], sep = ";")

    #Process the format and transform it to daily data:

    HourlyData['VALUEDATETIME'] = pd.to_datetime(HourlyData['VALUEDATETIME'])
    HourlyData = HourlyData[HourlyData['VALUEDATETIME'] >= pd.Timestamp(today)]
    HourlyData['day'] = [str(i.year) + '-' + str(i.month) + '-' + str(i.day) for i in HourlyData['VALUEDATETIME']]
    HourlyData = HourlyData.groupby('day').agg(np.mean)
    HourlyData.index = pd.to_datetime(HourlyData.index)
    HourlyData.sort_index(inplace = True)

    #Read gas and carbon daily data:

    pattern = 'Daily_'+str(tYear)+strMonth+strDay+'*BASE CASE_Daily.csv'
    gasAndCarbon = pd.read_csv(listPatternFiles(searchDir, pattern)[0], sep = ";")

    #Process the format:

    gasAndCarbon['VALUEDATETIME'] = pd.to_datetime(gasAndCarbon['VALUEDATETIME'])
    gasAndCarbon = gasAndCarbon[gasAndCarbon['VALUEDATETIME'] >= pd.Timestamp(today)]

    #Creating separated dataframes for Carbon and gas from the previous dataframe and setting their index:

    carbonList = ['CARBON_Sim_'+str(i) for i in range(1,501)]
    gasList = ['GAS_Sim_'+str(i) for i in range(1,501)]
    carbonData = gasAndCarbon[carbonList]
    gasData = gasAndCarbon[gasList]
    carbonData.index, gasData.index = (gasAndCarbon['VALUEDATETIME'] for i in range(1,3))

    #Creating CSS database (the efficiency is understated, but this happened to be conservative):

    CssDaily = pd.DataFrame(HourlyData.values - 1.91900818*gasData.values - 0.353084*carbonData.values)
    CssDaily.columns = ['CSS_NL_Sim_'+str(i) for i in range(1,501)]
    CssDaily.index = HourlyData.index
    CssDaily['Year&Month'] = [str(i.year)+ '-' + str(i.month) for i in CssDaily.index]

    #Creating CSS fwd curve:

    CssMonthlyFWD=CssDaily.groupby('Year&Month').agg(np.mean).T.mean().T
    CssMonthlyFWD.index = pd.to_datetime(CssMonthlyFWD.index)
    CssMonthlyFWD.sort_index(inplace = True)

    #Creating CSS fwd option value:

    CssDaily = CssDaily.iloc[:,:-1]
    CssDailyOption = pd.DataFrame(CssDaily.where(CssDaily > 0,0))
    CssDailyOption['Year&Month'] = [str(i.year)+'-'+str(i.month) for i in CssDailyOption.index]
    CssOptMonthly = CssDailyOption.groupby('Year&Month').agg(np.mean)
    CssOptMonthly.index = pd.to_datetime(CssOptMonthly.index)
    CssOptMonthly.sort_index(inplace = True)
    CssOptMonthly = CssOptMonthly.T.mean().T
    
    #Creating Monthly intrinsic:

    CssDailyAvg = CssDaily.T.mean()
    CssDailyIntr = pd.DataFrame(CssDailyAvg.where(CssDailyAvg>0,0))
    CssDailyIntr['Year&Month'] = [str(i.year) + '-' +str(i.month) for i in CssDailyIntr.index]
    CssMonthlyIntr=CssDailyIntr.groupby('Year&Month').agg(np.mean)
    CssMonthlyIntr.index = pd.to_datetime(CssMonthlyIntr.index)
    CssMonthlyIntr.sort_index(inplace=True)
    CssMonthlyIntr = pd.Series(CssMonthlyIntr[0])

    #Creating Final Data Frame:

    data = pd.DataFrame({'Forward_CSS': CssMonthlyFWD,
                  'Forward_Option_Css':CssOptMonthly,
                         'Forward_Intr':CssMonthlyIntr,
                  'Forward_Extrinsic':CssOptMonthly - CssMonthlyIntr})

    #Saving CSV:

    data.to_csv('C:/Users/D110148/OneDrive - pzem/data/CSSExtrinsicMODaily'+str(tYear)+strMonth+strDay+'.csv')

    print('MO Data processed succesfully')
    
    return data

    
