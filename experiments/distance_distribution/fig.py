import json
from matplotlib import pyplot as plt

fn = 'statistic'
sigmas = [0.001, 0.0001, 0.00001, 0.000001, 0.0000001, 0.00000001]
with open(fn) as fin:
    stat = json.load(fin)


def draw(data, x):
    figure, axes = plt.subplots(nrows=1, ncols=len(data))
    figure.set_figwidth(12)
    figure.set_figheight(4)
    for i, ax in enumerate(axes):
        ax.bar(x, data[i][0:30])
    plt.tight_layout()
    plt.show()

x = [ str(i) for i in range(30)]

draw(stat['amazon_distance'], x)
