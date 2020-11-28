# -*- coding: utf-8 -*-


import os
import numpy as np
import mne
from statsmodels.tsa.stattools import grangercausalitytests
import pandas as pd
import matplotlib.pyplot as plt

from pandas import read_csv
from matplotlib import pyplot
import networkx as nx

    
def channel_connection(data):
    result = []
    G = nx.DiGraph()
    G.add_node("E1")
    G.add_node("E2")
    G.add_node("E3")
    G.add_node("E4")
    G.add_node("E5")
    G.add_node("E6")
    G.add_node("E7")
    G.add_node("E8")
    G.add_node("E9")
    G.add_node("E10")
    G.add_node("E11")
    G.add_node("E12")
    G.add_node("E13")
    G.add_node("E14")
    G.add_node("E15")
    G.add_node("E16")
    G.add_node("E17")
    G.add_node("E18")
    G.add_node("E19")
    G.add_node("E20")
    G.add_node("E21")
    G.add_node("E22")
    G.add_node("E23")
    G.add_node("E24")
    G.add_node("E25")
    G.add_node("E26")
    G.add_node("E27")
    G.add_node("E28")
    G.add_node("E29")
    G.add_node("E30")
    G.add_node("E31")
    G.add_node("E32")
    G.add_node("E33")
    G.add_node("E34")
    G.add_node("E35")
    G.add_node("E36")
    G.add_node("E37")
    G.add_node("E38")
    G.add_node("E39")
    G.add_node("E40")
    G.add_node("E41")
    G.add_node("E42")
    G.add_node("E43")
    G.add_node("E44")
    G.add_node("E45")
    G.add_node("E46")
    G.add_node("E47")
    G.add_node("E48")
    G.add_node("E49")
    G.add_node("E50")
    G.add_node("E51")
    G.add_node("E52")
    G.add_node("E53")
    G.add_node("E54")
    G.add_node("E55")
    G.add_node("E56")
    G.add_node("E57")
    G.add_node("E58")
    G.add_node("E59")
    G.add_node("E60")
    G.add_node("E61")
    G.add_node("E62")
    G.add_node("E63")
    G.add_node("E64")
    pos = nx.spring_layout(G)
    
    for i in range(1,65):
        a = list(range(1,65))
        a.pop(i-1)
        for j in a:
            ts_df = data[['E'+str(j),'E'+str(i)]]
            #pyplot.plot(ts_df)
            #pyplot.show()
            gc_res = grangercausalitytests(ts_df, 5, verbose=False)
            pvalues = [round(gc_res[i+1][0]['ssr_ftest'][1],5) for i in k]
            result.append(pvalues)
            if (pvalues<[0.05]):
                #print("E", i, " granger causes channel E", j, " pvalue = ", pvalues)
                nx.draw_networkx_nodes(G, pos)
                nx.draw_networkx_labels(G, pos)
                G.add_edge("E"+str(i),"E"+str(j))
                options = {
                    'node_color': 'blue',
                    'node_size': 100,
                    'width': 1,
                    'arrowstyle': '-|>',
                    'arrowsize': 9,
                    }
                nx.draw_networkx_edges(G, pos, arrows = True, edge_color='r', **options)
                #pos, edge_color='r',
                plt.show()
            else: 
                #print("E", i, " does not granger cause channel E", j, " pvalue = ", pvalues)
                print (" ")
    return result 
        
global k
k = [4]

#col_list = ['Time','E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9',	'E10',	'E11',	'E12',	'E13',	'E14',	'E15',	'E16',	'E17',	'E18',	'E19',	'E20',	'E21',	'E22',	'E23',	'E24',	'E25',	'E26',	'E27',	'E28',	'E29',	'E30',	'E31',	'E32',	'E33',	'E34',	'E35',	'E36',	'E37',	'E38',	'E39',	'E40',	'E41',	'E42',	'E43',	'E44',	'E45',	'E46',	'E47',	'E48',	'E49',	'E50',	'E51',	'E52',	'E53',	'E54',	'E55',	'E56',	'E57',	'E58',	'E59',	'E60',	'E61',	'E62',	'E63',	'E64',	'E65' ]
df = pd.read_csv('righthand.csv', header=0, index_col=0, nrows=350)

GC_1 = channel_connection(df)

result_2 = []
for j in range(1,3):
    df_2 = pd.read_csv('righthand.csv', header=0, index_col=0, skiprows =[i for i in range(1, 350*j)], nrows=350)
    GC_2 = channel_connection(df_2)
    result_2.extend(GC_2)
    
GC_1.extend(result_2)
np.savetxt("granger.csv", GC_1, fmt='%s', delimiter = ",", header='pvalues')





#for i in range (0, 64):
    #E_i = GC_1[63*i:63*i+63]
    
#E1 = GC_1[0:63]
#E2 = GC_1[63:126]
#E3 = GC_1[126:189]
#print(GC_1)
#df = pd.DataFrame({'E1':E1})
#df_final = df.assign(**{'E2':E2,'E3':E3})

#compression_opts = dict(method='zip',
#                        archive_name='out.csv')  
#df_final.to_csv('out.zip', index=False,
#          compression=compression_opts)


#mne.viz.plot_arrowmap(df, info_from=df['E1'], info_to=None, scale=3e-10, vmin=None, vmax=None, cmap=None, sensors=True, res=64, axes=None, names=None, show_names=False, mask=None, mask_params=None, outlines='head', contours=6, image_interp='bilinear', show=True, onselect=None, extrapolate='auto', sphere=None)

