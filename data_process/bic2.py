#coding:utf-8
import matplotlib.pyplot as plt
import numpy as np
import re
from matplotlib import ticker
    
    
log_type = "test"
upper_bound = 14    
    
#log_pattern = "<(.*?)> k:(.*?) distance:eul sc:(.*?) mse:(.*?) cls:"
    
log_pattern = "k:(.*?); dataset:.*?; alg:(.*?); distance_type:vec; runtime:.*?; sc:(.*?); mse:(.*?); rand:(.*?); size.*?\n"

file_names = [
"/log/ctclog/2018-12-18_besttestdata3000_quality_exp.log.0.003",
"/log/ctclog/2018-12-18_besttestdata3000_quality_exp.log.0.004",
"/log/ctclog/2018-12-18_besttestdata3000_quality_exp.log.0.005"]

# file_names = ["/log/ctclog/2018-12-18_besttestdata3000_quality_exp.log.stdvar.0.0002538195462258292",
# "/log/ctclog/2018-12-18_besttestdata3000_quality_exp.log.std_var"]

    
arr_xy = [
    [(5.1, 0.88),(5.1, 0.88),(5.1, 0.88),(5.1,0.88)],
    [(3., 0.40),(3, 0.40),(13.9, 0.4),(10,10)]
]
marr_xy = [
    [(4.1, 0.56),(4.05, 0.55),(4.1, 0.41),(4.1,0.53)],
    [(3.1, 0.425),(3.05, 0.425),(9.1, 0.15),(10,10)]
]
text_xy = [
     [[(5,0.6), (6,0.75)], [(7,0.6),(7,0.7)],  [(5,0.5),(6,0.7)], [(5,0.6),(6,0.75)]],
    [ [(5,0.46),(4,0.32),], [(5,0.46),(4,0.32),],  [(11, 0.20),(11,0.3),], [(10,10.6),(20,20)]]
]
k_txt = [
    ['4','4', '4', '4'],
    ['3','3', '9', '']
]

fig_txt = [
    'Global Variance: 0.00025',
    'Each Dimension Variance'
]

# fig_txt = [
#     '0.003',
#     '0.004',
#     '0.005',
# ]

fig_txt_loc = [
    [0.18, 0.],
    [0.65, 0.],
]

fig,axes = plt.subplots(4,2)
fig.set_size_inches(12, 9)

def drawinternal(fig, axes, col, file_name, fig_txt, fig_txt_loc, arr_xy, marr_xy, text_xy, k_txt, idx):
    log_f = open(file_name)
    log_content = log_f.read(1024*1024*5)
    log_data = {
        "covertree":{
            "bic":[],
            "mse":[],
            "sc":[]
        },
        "hierarchical":{
            "bic":[],
            "mse":[],
            "sc":[]
        },
        "spectral":{
            "bic":[],
            "mse":[],
            "sc":[]
        },
        "kmeans":{
            "bic":[],
            "mse":[],
            "sc":[]
        }
    }
    
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True) 
    formatter.set_powerlimits((-1,1)) 
    
    compiler = re.compile(log_pattern)
    log_rec = compiler.findall(log_content)
    
    for rec in log_rec:
        alg = rec[1]
        sc = float(rec[2])
        mae = float(rec[3])
        log_data[alg]["sc"].append(sc)
        log_data[alg]["mse"].append(mae)
    
    k = range(2, 7)
    sc_y = [i*0.05 for i in range(0, 20)]
    mse_y = range(0, 40000, 2500)
    
    
    title_keys = ["kmeans", "spectral", "covertree", "hierarchical"]
    fig.text(fig_txt_loc[0], fig_txt_loc[1], fig_txt, fontsize=16)
    for index, alg in enumerate(title_keys):
        if alg=='spectral':
            title = 'Spectral'
        elif alg=='hierarchical':
            title = 'Hierarchical'
        elif alg=='kmeans':
            title = 'Kmeans'
        else:
            title = 'PurTreeClust'
        sc_ax  = axes[index][col]
        mse_ax = sc_ax.twinx()
        sc_ax.set_title(title, fontsize=10)
        mse_ax.set_title(title, fontsize=10)
        # sc_ax.spines['top'].set_visible(False)  #去掉上边框
        # sc_ax.spines['right'].set_visible(False) #去掉右边框
        mse_ax.spines['top'].set_visible(False)  #去掉上边框
        # mse_ax.spines['right'].set_visible(False) #去掉右边框
        sc_ax.grid('true', linestyle=":", linewidth=0.7)
        mse_ax.grid('true', linestyle=":", linewidth=0.7)
        # sc_ax.set_xlabel("k", fontsize=5)
        # sc_ax.set_ylabel("SC", fontsize=6)
        # mse_ax.set_xlabel("k", fontsize=5)
        # mse_ax.set_ylabel("MSE", fontsize=6)
    
        sc_ax.set_xticks(k)
        sc_ax.set_yticks(sc_y)
        mse_ax.set_xticks(k)
        #mse_ax.set_yticks(mse_y)
        # if index == 0:
        #     mse_y = range()
    
    
        sc_ax.plot(np.array(k[0:upper_bound]), np.array(log_data[alg]['sc'][0:upper_bound]), "k-o", linewidth = 1.5, markeredgewidth=0.5, label='SC')
        if idx==0 and index==0:
            sc_ax.legend(loc='upper right', bbox_to_anchor=(0.1, 1.18),
               ncol=1, mode=None, borderaxespad=0., frameon=False , fontsize=12)
        # sc_ax.annotate('peek', xy=arr_xy[index], xytext=text_xy[index][1], fontsize = 13,
        #         arrowprops=dict(facecolor='black', shrink=0.05, width=0, headwidth=0),
        #         )
        # sc_ax.annotate('knee', xy=marr_xy[index], xytext=text_xy[index][0], fontsize = 13,
        #         arrowprops=dict(facecolor='black', shrink=0.05, width=0, headwidth=1),
        #         )
        mse_ax.plot(np.array(k[0:upper_bound]), np.array(log_data[alg]['mse'][0:upper_bound]), "k:X", linewidth = 1.5, markeredgewidth=0.5, label='MSE')
        mse_ax.yaxis.set_major_formatter(formatter) 
        if idx==0 and index==0:
            mse_ax.legend(loc='upper right', bbox_to_anchor=(0.3, 1.18),
               ncol=1, mode=None, borderaxespad=0., frameon=False , fontsize=12)        

for i in xrange(0,2):
    drawinternal(fig, axes, i, file_names[i], fig_txt[i], fig_txt_loc[i], arr_xy[0], marr_xy[0], text_xy[0], k_txt[0], i)

plt.tight_layout()
plt.show()

fig,axes = plt.subplots(4,2)
fig.set_size_inches(12, 9)

# file_names = ["/log/ctclog/2018-12-18_besttestdata3000_quality_exp.log.stdvar.0.0002538195462258292",
# "/log/ctclog/2018-12-18_besttestdata3000_quality_exp.log.std_var"]

    
arr_xy = [
    [(4.1, 0.83),(4.1, 0.81),(4.1, 0.95),(4.1,0.81)],
    [(4., 0.79),(4, 0.79),(20, 20.38),(10,10)]
]
text_xy = [
    [(5,0.6), (5,0.6),  (4,0.6), (5,0.6)],
    [(4,0.46), (4,0.46),  (11,20.25), (10,10.6)]
]
k_txt = [
    ['4; ARI=0.86','4; ARI=0.86', '4;ARI>0.95', '4; ARI=0.84'],
    ['4; ARI=0.81','4; ARI=0.80', '', '']
]

# fig_txt = [
#     'Global Variance: 0.00025',
#     'Each Dimension Variance'
# ]

# fig_txt_loc = [
#     [0.20, 0.],
#     [0.70, 0.],
#     [1.20, 0.],
#     [1.70, 0.],
#     [2.20, 0.],
# ]

def draw_ri(fig, axes, col, file_name, fig_txt, fig_txt_loc, arr_xy, marr_xy, text_xy, k_txt):
    log_f = open(file_name)
    log_content = log_f.read(1024*1024*5)
    log_data = {
        "covertree":{
            "rand":[],
        },
        "hierarchical":{
            "rand":[],
        },
        "spectral":{
            "rand":[],
        },
        "kmeans":{
            "rand":[],
        }
    }
    
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True) 
    formatter.set_powerlimits((-1,1)) 
    
    compiler = re.compile(log_pattern)
    log_rec = compiler.findall(log_content)
    
    for rec in log_rec:
        alg = rec[1]
        rand = float(rec[4])
        log_data[alg]["rand"].append(rand)
    
    k = range(2, 7)
    rand_y = [i*0.05 for i in range(0, 20)]
    
    title_keys = ["kmeans", "spectral", "covertree", "hierarchical"]
    fig.text(fig_txt_loc[0], fig_txt_loc[1], fig_txt, fontsize=15)
    for index, alg in enumerate(title_keys):
        if alg=='spectral':
            title = 'Spectral'
        elif alg=='hierarchical':
            title = 'Hierarchical'
        elif alg=='kmeans':
            title = 'Kmeans'
        else:
            title = 'PurTreeClust'
        rand_ax  = axes[index][col]
        rand_ax.set_title(title, fontsize=13)
        rand_ax.grid('true', linestyle=":", linewidth=0.7)
        rand_ax.set_xlabel("k", fontsize=11)
    
        rand_ax.set_xticks(k)
        #rand_ax.set_yticks(rand_y)

    
        rand_ax.plot(np.array(k[0:upper_bound]), np.array(log_data[alg]['rand'][0:upper_bound]), "k-o", linewidth = 1.5, markeredgewidth=0.5, label='ARI')
        rand_ax.legend(loc='upper right', bbox_to_anchor=(0.1, 1.18),
               ncol=1, mode=None, borderaxespad=0., frameon=False , fontsize=12)
        # rand_ax.annotate('k='+k_txt[index], xy=arr_xy[index], xytext=text_xy[index], fontsize = 13,
        #         arrowprops=dict(facecolor='black', shrink=0.05, width=0, headwidth=0),
        #         )
for i in xrange(0,2):
    draw_ri(fig, axes, i, file_names[i], fig_txt[i], fig_txt_loc[i], arr_xy[0], marr_xy[0], text_xy[0], k_txt[0])

plt.tight_layout()
plt.show()