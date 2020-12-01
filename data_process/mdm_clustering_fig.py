from matplotlib import pyplot as plt
import matplotlib
import json
import numpy as np
from matplotlib import ticker
from matplotlib.pyplot import MultipleLocator

font = {'family' : 'serif',
        'weight' : 'normal',
        'size'   : 10}
matplotlib.rc('font', **font)

tag = 'address'

fig, axes = plt.subplots(ncols=1, nrows=3)
fig.set_size_inches(5,9)

with open('mdm_result_%s.json'%tag) as fin:
    data = json.load(fin)

dist_text = 'Address'
alg_list = [
    'km',
    'sp',
    'hac'
]
alg_name = [
    'K-Means',
    'Spectral',
    'Hierarchical'
]

k = range(2,40)
str_k = [str(i) if i%2==0 else '' for i in range(2,40)]

formatter = ticker.ScalarFormatter(useMathText=True)
formatter.set_scientific(True) 
formatter.set_powerlimits((-1,1)) 
for idx in range(3):
    sc_axe = axes[idx]
    mse_axe = sc_axe.twinx()
    sc_y = data[alg_list[idx]+'_sc']
    mse_y = data[alg_list[idx]+'_mse']
    sc_axe.plot(k, sc_y, 'b-.', label='SC')
    mse_axe.plot(k, mse_y, 'g:x', label='MSE')

    sc_axe.grid(axis='y')
    sc_axe.set_facecolor('#DBDBDB')
    sc_axe.text(20, 0.6, '%s+%s'%(dist_text, alg_name[idx]), bbox=dict(fc="none"))
    mse_axe.yaxis.get_major_formatter().set_powerlimits((0,1))
    mse_axe.yaxis.get_major_formatter().set_scientific(True)
    mse_axe.yaxis.get_major_formatter().set_useMathText(True)
    # mse_axe.yaxis.set_major_formatter(formatter)

    if idx==0:
        sc_axe.legend(loc='upper right', bbox_to_anchor=(0.14, 1.15),
               ncol=1, mode=None, borderaxespad=0., frameon=False , fontsize=10)
        mse_axe.legend(loc='upper right', bbox_to_anchor=(0.34, 1.15),
               ncol=1, mode=None, borderaxespad=0., frameon=False , fontsize=10) 
    if idx==2:
        sc_axe.set_xlabel('No. of clusters')
fig.text(.05, 0.5, 'Silhouette Coefficient (SC)',
        horizontalalignment='right',
        verticalalignment='center',
        rotation='vertical')
fig.text(1.01, 0.5, 'Mean Squared Error (MSE)',
        horizontalalignment='right',
        verticalalignment='center',
        rotation='vertical')
# plt.tight_layout()       
# plt.show()
plt.savefig('mdm_cls_%s.png'%(tag), bbox_inches ='tight')


