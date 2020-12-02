from matplotlib import pyplot as plt
import matplotlib
import json
import numpy as np
from matplotlib import ticker
from matplotlib.pyplot import MultipleLocator
font = {'family' : 'serif',
        'weight' : 'normal',
        'size'   : 11}
matplotlib.rc('font', **font)


data = np.array([
    0.18, 0.06, 0.02, 0.01, 0.01, 0.01, 0.04, 0.11, 1.43, 0.10, 0.01, 0.00
])

data = data * 1e8

fig, axe = plt.subplots(1,1)
fig.set_size_inches(5,5)
x = range(len(data))
x_ticklabels = ['=0.0', '(0.0,0.2]', '(0.2,0.4]', '(0.4,0.6]','(0.6,0.8]','(0.8,1.0]','(1.0,1.2]','(1.2,1.4]','(1.4,1.6]', '(1.6,1.8]', '(1.8,2.0]', '(2.0,2.2]']
axe.bar(x, data, width=-1, align='edge', color='black', edgecolor='white')
axe.set_xticks(x)
axe.set_xticklabels(x_ticklabels, rotation=30, ha='right')
axe.grid(axis='y')
axe.set_facecolor('#DBDBDB')
axe.yaxis.get_major_formatter().set_powerlimits((0,1))
axe.yaxis.get_major_formatter().set_scientific(True)
axe.yaxis.get_major_formatter().set_useMathText(True)
axe.set_xlabel('Distance Ranges', fontsize=12)
axe.set_ylabel('Pairs', fontsize=12)
plt.tight_layout()
plt.show()

