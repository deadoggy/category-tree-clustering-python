import sys
sys.path.append(sys.path[0] + '/../')
import numpy as np
from util.dunn import dunn_index


data = np.array([
    [1,1],
    [1,2],
    [2,1],
    [2,2],
    [5,5],
    [5,6],
    [6,5],
    [6,6],
    [5,2],
    [6,2],
    [6,3],
    [5,3]
])

label = np.array([
    0,0,0,0,1,1,1,1, 2,2,2,2
])


dunn = dunn_index(data, label)
print(dunn)

