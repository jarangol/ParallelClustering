#coding=utf-8
'''Implementation and of K Means Clustering'''
import numpy as np

# el de nosotros
def kMeans(X, K, maxIters = 10):
    # generamos k centroides con valores aleatorios
    centroides = np.random.rand(K,len(X[0]))
    for i in range(maxIters):
        # assinacion de centroides
        C = asignar(X,centroides)
        # calculamos el promedio para cada centroide
        centroides = mover(centroides,X,K,C)
    return np.array(C)

def asignar(X,centroids):
    C2 = []
    for xi in X:
        # print "xi",xi
        dists = []
        for ci in centroids:
            # print "ci",ci
            dist = np.linalg.norm(np.array(xi)-np.array(ci))
            dists.append(dist)
        # print "dist ",dists
        menor = np.argmin(dists)
        # print menor
        C2.append(menor)

        # print "menor: ",dists[np.argmin(dists)]," en ",menor
    # print "asiganacion quedó ",C2
    return C2

def mover(centroids,X,K,C):
    for k in range(K):
        ks = []
        for c in range(len(C)):
            if C[c] == k:
                ks.append(X[c])
        if len(ks)>0:
            mean =  np.mean(ks,axis=0)
            # print "centroide ",k," movido de ",centroids[k]," a ",mean
            centroids[k] = mean
        # else:
            # print "centroide sigue en la posicion ",centroids[k]
    # print "centroides quedaron ",centroids
    return centroids


# K = 1
#
# X = [[ 23.,  24.,  18.,  22.,   0.,  29.],
#  [  0. ,  0. ,  1. ,  0.  , 0.  , 0.],
#  [  0. ,  0.  , 1. ,  1. ,  0. ,  0.],
#  [  0. ,  0. ,  0. ,  0. ,  1. ,  0.]]
# X = [[ 0.33333333, 0.375, 0.45833333, 0.0, 0.25],[1.0, 0.5, 1.0, 1.0, 0.0 ],
#      [2.0, 0.2, 0.0, 1.0, 0.3 ],[0.01, 1.0, 0.2, 1.0, 0.0 ],[0.7, 0.6, 0.5, 1.0, 0.0 ]]
# print "K: ",K,"X: ",X
# print "result: ",kMeans(X,K)
