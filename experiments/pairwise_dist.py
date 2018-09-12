#coding:utf-8
def edit_pairwise_dist(X, Y=None):
    '''
        calculate pairwise edit distance between each pair in X or X and Y

        @X: {array-like, sparse matrix}, shape (n_samples_1, n_features)
        @Y: {array-like, sparse matrix}, shape (n_samples_2, n_features)

        #return: distances : {array, sparse matrix}, shape (n_samples_1, n_samples_2)
    '''

    return [0.0]