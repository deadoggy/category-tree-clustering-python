# !/bin/bash

echo GeoG+KMeans
touch geog_km.log
python dianping_features.py GeoG kmeans 

echo GeoM+KMeans
touch geom_km.log
python dianping_features.py GeoM kmeans 

echo Both+Kmeans
touch both_km.log
python dianping_features.py Both kmeans 

#echo GeoG+DBscan
#touch geog_dbscan.log
#python dianping_features.py GeoG dbscan > geog_dbscan.log

#echo GeoM+DBscan
#touch geom_dbscan.log
#python dianping_features.py GeoM dbscan > geom_dbscan.log

#echo Both+DBscan
#touch both_dbscan.log
#python dianping_features.py Both dbscan > both_dbscan.log
