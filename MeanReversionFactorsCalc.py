import sympy as sp
from scipy import stats
import numpy as np
from scipy.optimize import fsolve
import pandas as pd

def getMeanReversionFactor(f,subset,MOExtrinsic):
    
    v1   = subset['+MOD VOL1']
    v2   = subset['+MOD VOL2']
    s1   = subset['UNDERLYING1'].astype(float)
    s2   = subset['UNDERLYING2'].astype(float)
    p    = subset['+MOD CORR']
    t    = subset['+MOD TIME'].astype(float)
    r    = subset['+MOD IR'].astype(float)
    U = np.array([34.121411565 if i == 'ZB-HTE' else 1 for i in subset['1COMPONENT']])
    w    = subset.weight
    intr = subset['+OPT INTRINSIC']
    v    = (v1**2+v2**2-2*p*v1*v2)**(1/2)
    d1   = (np.log(s1/s2)+(f*v)**2*t/2)/((f*v)*t**(1/2))
    d2   = d1-(f*v)*t**(1/2)
    N1   = stats.norm.cdf(d1)
    N2   = stats.norm.cdf(d2)
    Kirk = np.exp(-r*t)*(s1*N1-s2*N2)*U
    
#----------------------------------------------------
    
    Aligne          = sum(Kirk*w)/sum(w)
    AligneIntrinsic = sum(intr*w)/sum(w)
    AligneExtr      = Aligne - AligneIntrinsic
    
    return AligneExtr - MOExtrinsic


def getMeanReversionFactorArray(months, sAndFData, MOExtrinsic):
    
    factors = []
    
    for i in range(len(months)):
        
        subset = sAndFData[sAndFData['+1START'].astype('datetime64[M]') == months[i]]
        subset.weight = [0.5 if np.is_busday(i) == True else 1 for i in subset['+1START'].astype('datetime64[D]')]
        
        solution = fsolve(getMeanReversionFactor, 1, args=(subset,MOExtrinsic[i]))
        
        factors.append(solution[0])

    print('MR Factors calculated succesfully')
        
    return factors


#The following two functions are for storing the Aligne data:

def getAligneData(subset):
    
    v1   = subset['+MOD VOL1']
    v2   = subset['+MOD VOL2']
    s1   = subset['UNDERLYING1'].astype(float)
    s2   = subset['UNDERLYING2'].astype(float)
    p    = subset['+MOD CORR']
    t    = subset['+MOD TIME'].astype(float)
    r    = subset['+MOD IR'].astype(float)
    U = np.array([34.121411565 if i == 'ZB-HTE' else 1 for i in subset['1COMPONENT']])
    w    = subset.weight
    intr = subset['+OPT INTRINSIC']
    v    = (v1**2+v2**2-2*p*v1*v2)**(1/2)
    d1   = (np.log(s1/s2)+v**2*t/2)/(v*t**(1/2))
    d2   = d1-v*t**(1/2)
    N1   = stats.norm.cdf(d1)
    N2   = stats.norm.cdf(d2)
    Kirk = np.exp(-r*t)*(s1*N1-s2*N2)*U
    
#----------------------------------------------------
    
    Aligne          = sum(Kirk*w)/sum(w)
    AligneIntrinsic = sum(intr*w)/sum(w)
    AligneS1        = sum(s1*w)/sum(w)
    AligneS2        = sum(s2*w)/sum(w)
    AligneV1        = sum(v1*w)/sum(w)
    AligneV2        = sum(v2*w)/sum(w)
    AligneExtr      = Aligne - AligneIntrinsic
    
    return Aligne, AligneIntrinsic, AligneS1, AligneS2, AligneV1, AligneV2, AligneExtr

def addAligneData(months, sAndFData):
    
    Aligne, AligneIntrinsic, AligneS1, AligneS2, AligneV1, AligneV2, AligneExtr = [],[],[],[],[],[],[]
    variables = [Aligne, AligneIntrinsic, AligneS1, AligneS2, AligneV1, AligneV2, AligneExtr]
    
    for i in range(len(months)):

        subset = sAndFData[sAndFData['+1START'].astype('datetime64[M]') == months[i]]
        subset.weight = [0.5 if np.is_busday(i) == True else 1 for i in subset['+1START'].astype('datetime64[D]')]

        output = getAligneData(subset)

        [variables[i].append(output[i]) for i in range(len(variables))]
    
    return pd.DataFrame({'Aligne':Aligne, 'AligneIntrinsic':AligneIntrinsic, 
                 'AligneS1':AligneS1, 'AligneS2':AligneS2, 'AligneV1':AligneV1,
                 'AligneV2':AligneV2, 'AligneExtr':AligneExtr})

        
    
