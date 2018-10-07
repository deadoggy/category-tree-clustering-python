#coding:utf-8

from matplotlib import pyplot as plt

with open('/home/yinjia/Documents/category-tree-clustering/log') as log_f:
    lines = log_f.read().split('\n')



k = [ str(i) for i in xrange(2,25)]

for i, line in enumerate(lines):
    if i ==0 or i==6:
        fig, axes = plt.subplots(2,3)
        fig.set_size_inches(16, 10)
    if line == '':
        continue
    str_vals = line.split(' ')
    index_name = str_vals[0]
    index_name = index_name[0:len(index_name)-1]
    
    y = []
    for j in xrange(1, len(str_vals)):
        if '' == str_vals[j]:
            continue
        y.append(float(str_vals[j]))
    
    row = i / 3 - 2
    col = i % 3
    axe = axes[row][col]

    axe.plot(k,y, 'k-D')
    axe.set_title(index_name)
    axe.grid('true', linestyle=":", linewidth=0.7)
    if i==5 or i ==10:
        plt.show()