'''Implementation and of K Means Clustering'''
import numpy as np

def kMeans2(X, K, maxIters = 10):
    # generamos k centroides con valores aleatorios
    centroides = np.random.rand(K,len(X))
    for i in range(maxIters):
        # Cluster Assignment step
        C = np.array([np.argmin([np.dot(x_i-y_k, x_i-y_k) for y_k in centroids]) for x_i in X])
        # Move centroids step
        centroids = [X[C == k].mean(axis = 0) for k in range(K)]
    return np.array(centroids)

def kMeans(X, K, maxIters = 10):
    # generamos k centroides con valores aleatorios
    centroides = np.random.rand(K,len(X))
    for i in range(maxIters):
        # Cluster Assignment step
        C = asignar()
        # Move centroids step
        centroids = [X[C == k].mean(axis = 0) for k in range(K)]
    return np.array(centroids)

def asignar():
    C2 = []
    for xi in X:
        print "xi",xi
        dists = []
        for ci in centroids:
            print "ci",ci
            dist = np.linalg.norm(np.array(xi)-np.array(ci))
            dists.append(dist)
            print "dist ",dist
        menor = np.argmin(dists)
        C2.append(menor)
        print "menor: ",dists[np.argmin(dists)]," en ",menor
    print C2
    return C2

def mover():
    centroids = []
    for k in range(K):
        ks = []
        for c in range(len(C2)):
            if C2[c] == k:
                ks.append(X[c])
        print "k ",k," ks ",ks
        if len(ks)>0:
            mean =  np.mean(ks,axis=0)
        print "centroide ",k," movido de ",centroids[k]," a ",mean
        centroids[k]=mean
