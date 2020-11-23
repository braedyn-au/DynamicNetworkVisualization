# -*- coding: utf-8 -*-


import os
import numpy as np
import mne
from statsmodels.tsa.stattools import grangercausalitytests
import pandas as pd
import matplotlib.pyplot as plt

from pandas import read_csv
from matplotlib import pyplot

    
def channel_connection(data):
    for i in range(1,65):
        a = list(range(1,65))
        a.pop(i-1)
        for j in a:
            ts_df = data[['E'+str(j),'E'+str(i)]]
            pyplot.plot(ts_df)
            pyplot.show()
            gc_res = grangercausalitytests(ts_df, 5, verbose=False)
            pvalues = [round(gc_res[i+1][0]['ssr_ftest'][1],5) for i in k]
            if (pvalues<[0.05]):
                print("E", i, " granger causes channel E", j, " pvalue = ", pvalues)
            else: 
                print("E", i, " does not granger cause channel E", j, " pvalue = ", pvalues)
    return pvalues
        
global k
k = [4]

#col_list = ['Time','E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9',	'E10',	'E11',	'E12',	'E13',	'E14',	'E15',	'E16',	'E17',	'E18',	'E19',	'E20',	'E21',	'E22',	'E23',	'E24',	'E25',	'E26',	'E27',	'E28',	'E29',	'E30',	'E31',	'E32',	'E33',	'E34',	'E35',	'E36',	'E37',	'E38',	'E39',	'E40',	'E41',	'E42',	'E43',	'E44',	'E45',	'E46',	'E47',	'E48',	'E49',	'E50',	'E51',	'E52',	'E53',	'E54',	'E55',	'E56',	'E57',	'E58',	'E59',	'E60',	'E61',	'E62',	'E63',	'E64',	'E65' ]
df = pd.read_csv('rawright.csv', header=0, index_col=0, nrows=350)

GC = channel_connection(df)

for j in range(1,3):
    df_2 = pd.read_csv('rawright.csv', header=0, index_col=0, skiprows =[i for i in range(1, 350*j)], nrows=350)
    GC = channel_connection(df_2)

