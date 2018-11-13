#coding:utf-8

from matplotlib import pyplot as plt
import sys
import time
import json
# jaccard similarity category
keys = [ -1., 0., .02, .04, .06, .08, .1, .12, .14, .16, .18, .2, .4, .6, .8, 1.]
sigmas = [1., 0.1, 0.01, 0.001, 0.0001]

jac_stat = [0 for i in xrange(len(keys)-1)]
vec_stat = [[0. for i in xrange(len(keys)-1)] for j in xrange(len(sigmas))]

print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + " begin loading"
for key_index in xrange(len(keys)-1):
    count = 0
    with open(sys.path[0] + "/distance_%f"%keys[key_index+1], 'r') as dist_in:
        print '=============================================='
        print 'distance_%f'%keys[key_index+1]
        line = dist_in.readline()
        while line!='':
            count += 1
            if count%1000000==0:
                print count
            line = line.split(',')
            jac_stat[key_index] += 1
            for line_idx, str_v in enumerate(line):
                if line_idx<=2:
                    continue
                vec_stat[line_idx-3][key_index] += float(str_v)
            line = dist_in.readline()
for i in xrange(len(sigmas)):
    for j in xrange(len(keys)-1):
        vec_stat[i][j] /= jac_stat[j] if jac_stat[j] > 0 else 1
print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + " begin drawing"

with open("distance_stat.json", "w") as dis_out:
    out_dict = {"jac_stat":jac_stat, "vec_stat":vec_stat}
    print out_dict
    json.dump(out_dict, dis_out)

with open('/home/yinjia/distance_stat.json', 'r') as distance_in:
    dist_json = json.load(distance_in)
    vec_stat = dist_json['vec_stat']
    jac_stat = dist_json['jac_stat']

x_keys = [ str(keys[i]) for i in xrange(1, len(keys))]
fig = plt.figure(figsize=(15,10))
ax = plt.subplot()
ax.bar(x_keys, jac_stat, width=-1., align='edge', edgecolor='#ffffff')
for a, b in zip(x_keys, jac_stat):
    ax.text(a, b+0.000000001, '%d'%b, ha='right', va= 'bottom',fontsize=10)
ax.set_title('Jaccard Similarity Distribution')
ax.set_xlabel('jaccard similarity')
ax.set_ylabel('count')
plt.savefig('JaccardSimilarityDistribution.png')

fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(8,8))
fig.set_figwidth(18)
fig.set_figheight(12)
axs = axs.flatten()

for i, ax in enumerate(axs.tolist()):
    if i>=len(vec_stat):
        continue
    ax.bar(x_keys,vec_stat[i], width=-1., align='edge', edgecolor='#ffffff')
    ax.set_xlabel('jaccard similarity')
    ax.set_ylabel('average category-dist')
    ax.set_title("Sigma:%f"%sigmas[i])

plt.tight_layout()
plt.savefig('CateVecDist-Jaccard.png')
