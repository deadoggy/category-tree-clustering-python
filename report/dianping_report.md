# 大众点评实验结果

## 实验流程

1. 对点评上海的商家数据进⾏提取和清洗，排除异常数据。 结果共有25985个商家数据。
2. 计算每个商家的地理坐标(GeoM) 和 ⾏政坐标(GeoG)
3.  分别采⽤ GeoG, GeoM 和 GeoG+GeoM作为坐标系, 利⽤KMeans 和 DBSCAN对25985个商家进⾏聚类， 每个商家的neighbors就是它所在类的其他全部商家。
4.  利⽤提取好的Neighbors信息和商家的类别信息，Rate信息等计算features. 计算的features有:
    1. Section 3 中全部的features
    2. Section 4 中第⼀个features
5. 对不同坐标系和聚类算法⽣成的features + 坐标系下坐标形成商家的最终特征，进⾏Linear Regression, Random Forest Regression 和 SVM 实验.

## 聚类的结果图



## 实验结果

结果中<Linear Regression>和<Random Forest Regression>是回归实验， 计算的误差是 |预测商家评分 - 真实商家评分| 的平均值； SVM是分类实
验， 商家的标签是 1, 2, 3, 4, 5中的⼀个；

.| Linear Regression | Random Forest Regression | SVM
:-:|:-:|:-:|:-:
GeoG+KMeans|1.124|1.170|0.46
GeoM+KMeans|1.122|1.122|0.45
Both+KMeans|1.122|1.166|0.45
GeoG+DBSCAN|1.122|1.122|0.45
GeoM+DBSCAN|1.122|1.167|0.45
Both+DBSCAN|1.120|1.164|0.48