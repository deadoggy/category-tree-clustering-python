# 距离分布实验

### 实验设计

用户总量120万左右, 实验中选择了消费记录大于5条的用户, 共3.28万左右.

1. 计算每一对用户之间的 Jaccard Similarity, 并统计距离在不同 Jaccard Similarity 区间内的分布情况。 即共有 ( 3.28k * 3.28k ) / 2 个Jaccard Similarity。 实验中统计了这些距离在{ ==0.0, (0.0, 0.02], (0.02, 0.04], (0.04, 0.06], (0.06, 0.08], (0.08, 0.10], (0.10, 0.12], (0.12, 0.14], (0.14, 0.16], (0.16, 0.18], (0.18, 0.20], (0.2, 0.4], (0.4, 0.8], (0.8, 1.0] } 这些区间内的数量分布。

2. 分别计算在 sigma = {1.0, 0.1, 0.01, 0.001, 0.0001} 时， 不同区间内 category tree distance 的平均值


### 实验结果

#### 实验1

![](JaccardSimilarityDistribution.png)


<br/><br/><br/><br/><br/><br/><br/>

#### 实验2

**两个用户间最大距离为 sqrt(22)

![](CateVecDist-Jaccard.png)


### 讨论

> Jaccard Similarity 下，绝大部分相似度都是0, 对用户的区分度很小。 

> 随着 Jaccard Similarity 增大， category tree distance 趋势变小， 符合距离定义。

> 随着 sigma 调优， 可以使得 category tree distance的距离分布变的合理。

### Next Step

> 可以进行在 Jaccard Similarity 为 0 时 category tree distance 的分布实验

> 为什么当 Jaccard Similarity 为 0 时 category tree distance 的平均距离要小于 Jaccard Similarity 在 (0.0, 0.02] 范围内时的平均距离。