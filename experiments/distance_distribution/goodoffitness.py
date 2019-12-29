import numpy as np
import scipy.stats as stats
import json

significance = 0.01
leftmost_rg = 31
rg_size = 100
# load statistic
with open('statistic') as fin:
    data = json.load(fin)
# degree of freedom
df = {
    'amazon_distance': 85,
    'yelp_distance': 22
}
f_df = {
    'amazon_distance': [5, 4],
    'yelp_distance': [5, 4]
}

# cdf
def cdf(key):
    with open(key+'minmax') as fin:
        min_arr = np.array(eval(fin.readline()))
        max_arr = np.array(eval(fin.readline()))
    steps = (max_arr-min_arr)/rg_size
    prob = {}
    
    # gaussian 
    prob['gaussian'] = [[] for i in range(len(data[key]))]
    ## load mean&variance
    with open(key + 'mean') as meanin:
        means = np.array(eval(meanin.readline()))
    with open(key + 'var') as varin:
        variances = np.array(eval(varin.readline()))
    ## calculate probability
    for i in range(len(data[key])): # each sigma
        for j in range(leftmost_rg-1): # each range
            prob['gaussian'][i].append(
                stats.norm.cdf(steps[i]*(j+1),means[i],np.sqrt(variances[i]))
                -(stats.norm.cdf(steps[i]*j,means[i],np.sqrt(variances[i])) if j!=0 else 0.)
            )
        prob['gaussian'][i].append(1-stats.norm.cdf(steps[i]*(leftmost_rg-1), means[i], np.sqrt(variances[i])))

    # chi
    prob['chi'] = [[] for i in range(len(data[key]))]
    ## calcualte probability
    for i in range(len(data[key])): # each sigma
        for j in range(leftmost_rg-1): # each range
            prob['chi'][i].append(
                stats.chi.cdf(steps[i]*(j+1),df[key])
                -(stats.chi.cdf(steps[i]*j,df[key]) if j!=0 else 0.)
            )
        prob['chi'][i].append(1-stats.chi.cdf(steps[i]*(leftmost_rg-1), df[key]))

    # chi-square
    prob['chi2'] = [[] for i in range(len(data[key]))]
    ## calculate probability
    for i in range(len(data[key])): # each sigma
        for j in range(leftmost_rg-1): # each range
            prob['chi2'][i].append(
                stats.chi2.cdf(steps[i]*(j+1),df[key])
                -(stats.chi2.cdf(steps[i]*j,df[key]) if j!=0 else 0.)
            )
        prob['chi2'][i].append(1-stats.chi2.cdf(steps[i]*(leftmost_rg-1), df[key]))
    
    # F distribution
    prob['f'] = [[] for i in range(len(data[key]))]
    ## calculate probability
    for i in range(len(data[key])): # each sigma
        for j in range(leftmost_rg-1): # each range
            prob['f'][i].append(
                stats.f.cdf(steps[i]*(j+1),f_df[key][0], f_df[key][1])
                -(stats.f.cdf(steps[i]*j, f_df[key][0], f_df[key][1]) if j!= 0 else 0.)
            )
        prob['f'][i].append(1-stats.f.cdf(steps[i]*(leftmost_rg-1), f_df[key][0], f_df[key][1]))
    
    return prob

def gof(freq, prob, total):
    freq = np.array(freq)
    prob = np.array(prob)
    ret = np.sum((freq**2)/(total*prob)) - total
    return ret 


gof_val = {}
chi2_val = {}
# convert frequency to probability
for k in data:
    # chi2
    chi2_val[k] = stats.chi2.ppf(significance, df[k]-1)
    # gof
    freq = data[k]
    row_sum = np.sum(freq, axis=1)[0]

    # for different sigma, calculate goodoffitness value of gaussian
    # distribution, chi distribution and chi-squared distribution
    prob = cdf(k)
    gof_val[k] = {
        'gaussian': np.zeros((len(freq),1)).tolist(),
        'chi': np.zeros((len(freq),1)).tolist(),
        'chi2': np.zeros((len(freq), 1)).tolist(),
        'f':  np.zeros((len(freq), 1)).tolist()
    }
    for dt in ['gaussian', 'chi', 'chi2', 'f']:
        for i in range(len(freq)):
            try:
                firstzero_idx = prob[dt][i].index(0.0)
                trim_freq = freq[i][0:firstzero_idx-1]
                trim_freq.append(np.sum(freq[i][firstzero_idx-1:]))
                trim_prob = prob[dt][i][0:firstzero_idx-1]
                trim_prob.append(np.sum(prob[dt][i][firstzero_idx-1:]))
            except Exception as e:
                trim_freq = freq[i][0:leftmost_rg-1]
                trim_freq.append(np.sum(freq[i][leftmost_rg:]))
                trim_prob = prob[dt][i]
            gof_val[k][dt][i] = gof(trim_freq, trim_prob, row_sum) 

with open('gof.json', 'w') as out:
    json.dump({'gof':gof_val, 'chi2':chi2_val}, out, indent=True)
