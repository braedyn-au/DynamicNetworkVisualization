
# read the data (the sample used here is the raw data file the I had from Rian)

import pandas as pd
import numpy as np
import scipy.stats as stats 
from scipy.stats import pearsonr
import pingouin as pg        # package for partial corelation

TS = pd.read_csv(r'EEG_Cat_Study4_Resting_S1_data.csv', header = None)

TS = TS.drop(index = 0, axis = 0)  # removing the chanel number
TS = TS.drop(0, axis = 1)          # removing the time column

TS = TS.astype(float)   # convert all objects in dataframe to float64 for calculating correlations

#%%
#Pearson Correlation

# fast method for only calculating correlation coefficients
#corr_TS = TS.corr(method="pearson") 

# calculating pearson correlation coefficients with p_value

size = TS.shape[1]
ADJ_corr = pd.DataFrame(np.zeros((size, size)))
ADJ_corr.index = np.arange(1, len(ADJ_corr) + 1) # indexing from 1
ADJ_corr.columns = np.arange(1, len(ADJ_corr) + 1)

# threshold = 0.05, 0.01, 0.001   # choosing the p_value
# network = 'Binary network', 'Weighted network'       

# default
threshold = 0.05
network = 'Weighted network'   

for i in TS:
    for j in TS:
        if i < j and i != j:   # to save time only calculating for the upper diagonal elements

            [corr_TS, Pval_TS] = pearsonr(TS[i], TS[j])

            if Pval_TS < threshold:
                if network == 'Weighted network':
                    ADJ_corr[i][j] = corr_TS
                    ADJ_corr[j][i] = corr_TS
                else:    
                    ADJ_corr[i][j] = 1
                    ADJ_corr[j][i] = 1
                
        ADJ_corr[i][i] = 1  # setting the diagonal elements 
        
        
#%%
#partial correlation

# fast method for only calculating correlation coefficients
#pcorr_TS = pg.pcorr(TS)
        
TS.columns = TS.columns.astype(str)  # converting the column names to string        

# calculating partial correlation coefficients with p_value

size = TS.shape[1]
ADJ_partialcorr = pd.DataFrame(np.zeros((size, size)))
ADJ_partialcorr.index = np.arange(1, len(ADJ_partialcorr) + 1) # indexing from 1
ADJ_partialcorr.columns = np.arange(1, len(ADJ_partialcorr) + 1)
ADJ_partialcorr.index = ADJ_partialcorr.index.astype(str) 
ADJ_partialcorr.columns = ADJ_partialcorr.columns.astype(str) 

#threshold = 0.05, 0.01, 0.001   # choosing the p_value
#network = 'Binary network', 'Weighted network'    

# default
threshold = 0.05
network = 'Weighted network' 

for i in TS:
    for j in TS:
        if i < j and i != j: # to save time only calculating for the upper diagonal
            
            temp_TS = TS.drop([str(i), str(j)], axis=1, inplace=False)
            TS_partial_corr = TS.partial_corr(x=str(i), y=str(j), covar=list(temp_TS.columns), tail='two-sided', method='pearson')

            if float(TS_partial_corr['p-val']) < threshold:
                if network == 'Weighted network':
                    ADJ_partialcorr[i][j] = float(TS_partial_corr['r'])
                    ADJ_partialcorr[j][i] = float(TS_partial_corr['r'])
                else:    
                    ADJ_partialcorr[i][j] = 1
                    ADJ_partialcorr[j][i] = 1
                    
        ADJ_partialcorr[i][i] = 1  # setting the diagonal elements    
        
        



        