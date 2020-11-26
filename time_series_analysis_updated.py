
# read the data (the sample used here is the raw data file the I had from Rian)

import pandas as pd
import numpy as np
import scipy.stats as stats 
from scipy.stats import pearsonr
import pingouin as pg        # package for partial corelation
import time
import os
import shutil
import moviepy.video.io.ImageSequenceClip

import matplotlib.pyplot as plt

#TS = pd.read_csv(io.StringIO(u""+df.to_csv(index=False)), header=None, skiprows=1)
#TS = pd.read_csv('righthand_s.csv')
#TS = pd.read_csv('righthand_s.csv', header = None)


#TS = TS.drop(index = 0, axis = 0)  # removing the chanel number
#TS = TS.drop(header_row)  # removing the chanel number

#print(TS)
#TS = TS.drop("Time", axis = 1)          # removing the time column

#TS = TS.astype(float)   # convert all objects in dataframe to float64 for calculating correlations

#print(TS)

#start = time.time()



#df = pd.read_csv('righthand.csv', header=0, index_col=0, nrows=1000)
df = pd.read_csv('righthand.csv', header=0, index_col=0, nrows = 60000)
df = df.drop("E65", axis = 1)

threshold = 0.05
network = 'Weighted network'   
header = df.columns.tolist()
l = len(header)

totsize = len(df.index)

timestep = 500

#fig = plt.figure()

path = os.getcwd()

image_folder='Pear_cor'
shutil.rmtree(image_folder)

path1 = path + "/" + image_folder
os.mkdir(path1)

image_folder='Par_cor'
shutil.rmtree(image_folder)

path1 = path + "/" + image_folder
os.mkdir(path1)


for k in range(0,totsize,timestep):
	
	print(k)
	
	df1 = df[k:k+timestep]
	

	ADJ_corr = np.zeros((l,l))

	for i in range(l):
		ADJ_corr[i][i] = 1  # setting the diagonal elements 
		for j in range(i+1,l):
			
			# converting value to interger were taking more time than taking floating point number.
			
			[corr_TS, Pval_TS] = pearsonr(df1[header[i]], df1[header[j]])

			if Pval_TS < threshold:
				if network == 'Weighted network':
					ADJ_corr[i][j] = corr_TS
					ADJ_corr[j][i] = corr_TS
			else:    
				ADJ_corr[i][j] = 1
				ADJ_corr[j][i] = 1			

	#print(ADJ_corr) 

	#end = time.time()

	#print("To compute Correlation matrix time took:", end-start)
	
	plt.matshow(ADJ_corr)
	plt.colorbar()
	plt.savefig("Pear_cor/Pearson_corr_%1.0f_.png" % k, dpi = 200.0)
	#plt.show()
	plt.clf()
	plt.close()
	
	# Compute partial correlation
	#print(df1[1:2])
	#pcorr_TS = pg.pcorr(df1)
	
	plt.matshow(pcorr_TS)
	plt.colorbar()
	plt.savefig("Par_cor/Partial_corr_%1.0f_.png" % k, dpi = 200.0)
	plt.clf()
	#plt.show()
	plt.close("all")

image_folder='Pear_cor'
fps=1000/timestep

image_files = [image_folder+'/'+img for img in os.listdir(image_folder) if img.endswith(".png")]
clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
clip.write_videofile('pearson_cor.mp4')

image_folder='Par_cor'
fps=1000/timestep

image_files = [image_folder+'/'+img for img in os.listdir(image_folder) if img.endswith(".png")]
clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
clip.write_videofile('partial_cor.mp4')


'''
df2 = pd.read_csv("Partial_corr.csv", index_col = 0)
#df2 = df2.drop("0", axis = 1)

#print(df2)
#fig = plt.figure()
plt.matshow(df2)
plt.colorbar()

#plt.show()

#for x in pcorr_TS.loc["E1"]: 
#	print(x)


#'''


'''
#%%
#partial correlation

# fast method for only calculating correlation coefficients
#pcorr_TS = pg.pcorr(TS)
        
#TS.columns = TS.columns.astype(str)  # converting the column names to string        

# calculating partial correlation coefficients with p_value

#size = TS.shape[1]
#ADJ_partialcorr = pd.DataFrame(np.zeros((size, size)))
#ADJ_partialcorr.index = np.arange(1, len(ADJ_partialcorr) + 1) # indexing from 1
#ADJ_partialcorr.columns = np.arange(1, len(ADJ_partialcorr) + 1)
#ADJ_partialcorr.index = ADJ_partialcorr.index.astype(str) 
#ADJ_partialcorr.columns = ADJ_partialcorr.columns.astype(str) 

#threshold = 0.05, 0.01, 0.001   # choosing the p_value
#network = 'Binary network', 'Weighted network'    

start= time.time()

# default
threshold = 0.05
network = 'Weighted network' 

ADJ_partialcorr = np.zeros((l,l))

for i in range(l):
	ADJ_partialcorr[i][i] = 1  # setting the diagonal elements    
	for j in range(i+1,l):
		temp_TS = df.drop([header[i], header[j]], axis=1, inplace=False)
		TS_partial_corr = df.partial_corr(x=header[i], y=header[j], covar=list(temp_TS.columns), tail='two-sided', method='pearson')

		if float(TS_partial_corr['p-val']) < threshold:
			if network == 'Weighted network':
				ADJ_partialcorr[i][j] = float(TS_partial_corr['r'])
				ADJ_partialcorr[j][i] = float(TS_partial_corr['r'])
			else:    
				ADJ_partialcorr[i][j] = 1
				ADJ_partialcorr[j][i] = 1

        

end= time.time()
print("proper PArtial corr took time: ",end-start)

#print(ADJ_partialcorr[0])

pd.DataFrame(ADJ_partialcorr).to_csv("Partial_corr.csv")
   
#'''


        
