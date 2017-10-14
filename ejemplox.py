import numpy as np

A = [1,2,3]
B = [3,2,1]
K = 3
X = [[ 0.33333333, 0.375, 0.45833333, 0.0, 0.25],[1.0, 2.0, 0.0, 1.0, 0.0 ],
     [2.0, 0.0, 0.0, 1.0, 0.0 ],[3.0, 0.0, 0.0, 1.0, 0.0 ],[4.0, 0.0, 0.0, 1.0, 0.0 ]]
print "X: ",X

# a = np.array(A)
# b = np.array(B)
# dist = np.linalg.norm(a-b)

# C = np.array([np.argmin([np.dot(x_i-y_k, x_i-y_k) for y_k in centroids]) for x_i in X])
# print "Ct: ",C
# centroids = [X[C == k].mean(axis = 0) for k in range(K)]
# print "Centros_t: ",centroids


centroids = np.random.rand(K,len(X))
print "Centroids", centroids

C2 = []
for xi in X:
    # print "xi",xi
    dists = []
    for ci in centroids:
        # print "ci",ci
        dist = np.linalg.norm(np.array(xi)-np.array(ci))
        dists.append(dist)
        # print "dist ",dist
    menor = np.argmin(dists)
    C2.append(menor)
    print "menor: ",dists[np.argmin(dists)]," en ",menor
print "C: ",C2

# a = [[5,5],[4,4]]
# print np.mean(a, axis=0)
for k in range(K):
    ks = []
    for c in range(len(C2)):
        if C2[c] == k:
            ks.append(X[c])
    print "k ",k," ks ",ks
    if len(ks)>0:
        mean =  np.mean(ks,axis=0)
        print "centroide ",k," movido de ",centroids[k]," a ",mean
    else:
        print "centroide sigue en la posicion ",centroids[k]
