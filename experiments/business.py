#coding:utf-8

import sys
sys.path.append(sys.path[0] + "/../")
from config.load_config import Config
from dist import vectorized_user_cate_dist
from index.index import *
from data_loader.data_loader import DataLoader
from dist.vectorized_user_cate_dist import *
from pyproj import Proj, transform
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import json

config = Config().config
PATH_BEG_OFFSET = 0
PATH_END_PFFSET = 1
GAUSSIAN_SIGMA = 0.

# u'CorrByydi35r-6SvmhYFHA'
exception_bid = [
    u'nMMlTMTLgtG7tJg6w7vmSA',
    u'fJFVpJN6X5rB1KjwtP4VZg'
    u'LwG4QsmvOibEsEUlryrPsw',
    u'8d8QHAktYg8Q2C3ZpAhwvQ',
    u'ivLJuOmDavlBmKIh0nnisg',
    u'FlLkjcSzfqmQBK6iEHRtTg',
    u'FaUk138U3lXk5EaTpI_37w',
    u's44fonP-M6Gzh7goJi559w',
    u'NTu31vavstnDW4pc68HJOA',
    u'CES01QjtAbJpYn_HI98gHg',
    u'HIZ5619cs1L-EA4MAHlWnw',
    u'MOKA2TABC6T04tKjzZ1_rw',
    u'b12qS86-9a_prAfFIdRD2w',
    u'pYeoaUJ6veQ3FEiSBnVMcw',
    u'ZpK3cU9lIPddzFcaV_rygg', 
]

def lonlat_to_3857(lon, lat):
    p1 = Proj(init='epsg:4326')
    p2 = Proj(init='epsg:3857')
    x1, y1 = p1(lon, lat)
    x2, y2 = transform(p1, p2, x1, y1, radians=True)
    return x2, y2


def generate_geog_pivots(plus_offset, minus_offset):
    '''
        generate a address pivots set 

        @plus_offset: offset at the begining of path
        @minus_offset: offset at the end of path
    '''
    with open(config["processed_data_path"] + "/lasvegas_business_info.json", "r") as din:
        datajson = json.load(din)

    pivots_list = {}
    for bid in datajson.keys():
        if bid in exception_bid:
            continue
        shop = datajson[bid]
        neighborhood = shop['neighborhood']
        if neighborhood not in pivots_list.keys():
            pivots_list[neighborhood] = CateTree()

        addrpath = shop['address']
        if addrpath == '':
            addrpath = ['']
        
        pivots_list[neighborhood].insert(addrpath[plus_offset : len(addrpath)-minus_offset])
    
    return pivots_list.values()

def generate_geog_vec():
    shopvec = {}
    pivots = generate_geog_pivots(PATH_BEG_OFFSET, PATH_END_PFFSET)
    
    with open(config['processed_data_path'] + "/lasvegas_business_info.json") as din:
        datajson = json.load(din)
    
    for bid in datajson:
        if bid in exception_bid:
            continue
        addrpath = datajson[bid]['address']
        if addrpath == '':
            addrpath = ['']
        shopvec[bid] = [ 0. for i in xrange(len(pivots)) ]

        for idx in xrange(len(pivots)):
            shopvec[bid][idx] = pivots[idx].similarity([addrpath[PATH_BEG_OFFSET : len(addrpath)-PATH_END_PFFSET]])
            if GAUSSIAN_SIGMA != 0.:
                shopvec[bid][idx] = np.exp(-(np.power(shopvec[bid][idx], 2.))/(2*GAUSSIAN_SIGMA**2))
    return shopvec

def generate_geom_vec():
    shopvec = {}
    with open(config['processed_data_path'] + '/lasvegas_business_info.json') as din:
        datajson = json.load(din)
    
    for bid in datajson:
        if bid in exception_bid:
            continue
        lat = datajson[bid]['latitude']
        lon = datajson[bid]['longitude']
        x,y = lonlat_to_3857(lon, lat)
        shopvec[bid] = [x, y]
    return shopvec


print "Generating GeoG Vectors..."
geog_data = generate_geog_vec()
print "Generating GeoM Vectors..."
geom_data = generate_geom_vec()

geog_vec = np.array(geog_data.values())
geom_vec = np.array(geom_data.values())

minmaxscaler = MinMaxScaler()

geog_vec = minmaxscaler.fit_transform(geog_vec)
geom_vec = minmaxscaler.fit_transform(geom_vec)

vec = np.concatenate((geog_vec, geom_vec), axis=1)

print vec

print "KMeans..."
#KMeans 
top_k = int(np.sqrt(len(vec)))
sc_vals = []
for k in xrange(2, top_k):
    label = KMeans(n_clusters=k).fit_predict()
    sc = silhouette_score(vec, label)
    print "k=%d, sc=%f"%(k, sc)
    sc_vals.append(sc)

plt.plot(range(2, top_k), sc_vals)
plt.savefig("geog+geom.png")
