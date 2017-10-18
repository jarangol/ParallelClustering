#coding=utf-8
from mpi4py import MPI
import glob,re
import numpy as npy
from time import time


tiempo_inicial = time()

comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.size
name = MPI.Get_processor_name()
master = size-1
#inicializacion de variables

stop_words = set(["the","be","and","of","a","in","to","have","to","it","I","that","for","you","he",
    "with","on","do","say","this","they","at","but","we","his","from","that","not",
    "n't","by","she","or","as","what","go","their","can","who","get","if","would",
    "her","all","my","make","about","know","will","as","up","one","time","there",
    "year","so","think","when","which","them","some","me","people","take","out","into",
    "just","see","him","your","come","could","now","than","like","other","how","then",
    "its","our","two","more","these","want","way","look","first","also","new","because",
    "day","more","use","no","man","find","here","thing","give","many","well"])

docs = glob.glob("./dos/*.txt")
docs_size = len(docs)
# docs = glob.glob("./docs/*.txt")
# docs_size = 4

def asignar(X,centroids):
    C = {}
    for i in X:
        dists = []
        for ci in centroids:
            # print "ci ",ci," rank ",rank
            dist = npy.linalg.norm(npy.array(X[i])-npy.array(ci))
            dists.append(dist)
        C[i] = npy.argmin(dists)
    # print "asignacion quedó ",C," rank ",rank
    return C

def mover(centroids,X,K,C):
    groups = {}
    for doc in X:
        groups.setdefault(C[doc], []).append(X[doc])
    # print "groups 0 ",groups[0]," rank ",rank
    for i in range(size):
        comm.bcast(groups,root=i)

    # for centro in groups:
    #     print "dic ",dict(groups.items()[0])
    #     print (centro+size)%size
    #     comm.send(groups[centro], dest=(centro+size)%size)
    #     print "centro ",centro, "rank "
    vectores = []

    # for i in range(size):
    vectores += comm.allgather(groups)
    for k in range(K):
        if rank == k%size:
            vector_k  = []
            for i in vectores:
                if k in i:
                    vector_k+=i[k]
            # print "vectork ",vector_k," rank",rank," k ",k
            if len(vector_k)>0:
                mean =  npy.mean(vector_k,axis=0)
                # print "mean ",mean," k ",k
                # print "centroide ",k," movido    de ",centroids[k]," a ",mean
                centroids[k] = mean
    # print "centroides quedaron ",centroids
    return centroids


    #     ks = []
    #     for c in range(len(C)):
    #         if C[c] == k:
    #             ks.append(X[c])
    #     # print "k ",k," ks ",ks
    #     if len(ks)>0:
    #         mean =  npy.mean(ks,axis=0)
    #         print "centroide ",k," movido de ",centroids[k]," a ",mean
    #         centroids[k] = mean
        # else:
            # print "centroide sigue en la posicion ",centroids[k]
    # print "centroides quedaron ",centroids
    # return centroids

def kMeans(X,K,maxIters = 10):
    centroides = []
    if rank==master:
        centroides = npy.random.rand(K,len(X.values()[0]))
        comm.bcast(centroides, root=master)

    centroides= comm.allgather(centroides)[size-1]
    for i in range(maxIters):
        # if rank == master:
            # print "iter ",i
        # assinacion de centroides
        C = asignar(X,centroides)
        comm.send(C,dest=master)
        if rank==master:
            for i in range(size):
                C.update(comm.recv(source=i))
            comm.bcast(C, root=master)

        C = comm.allgather(C)[size-1]
        # calculamos el promedio para cada centroide
        centroides = mover(centroides,X,K,C)
        comm.bcast(centroides, root=master)
        centroides= comm.allgather(centroides)[size-1]
    return C

def create_array(inp):
    infile = open(inp, 'r')
    doc_words = []
    for line in infile:
        for word in line.split(' '):
            res = re.sub('[^A-Za-z0-9]+', '', word)
            if res!='':
                doc_words.append(res.lower())
    infile.close()
    return doc_words

docs_words = {}
superset = set()
sets = {}
for i in range(rank,docs_size,size):
    docs_words[i] = create_array(docs[i])
    set_doc = set(docs_words[i])
    sets[i] = set_doc-stop_words
    superset = superset.union(sets[i])

comm.send(superset, dest=master)

dataR = set()
if rank==master:
    for i in range(size):
        dataR = dataR.union(comm.recv(source=i))
    comm.bcast(dataR, root=master)

superset= comm.allgather(dataR)[size-1]

frecuencias = {}
for i in range(rank,docs_size,size):
    doc_frec = []
    for j,palabra in enumerate(superset):
        if palabra in sets[i]:
            doc_frec.append(docs_words[i].count(palabra))
            # print palabra," ",docs_words[i].count(palabra)," veces en doc ",i
            # matriz[i][j] = docs_arrays[i].count(palabra)
        else:
            doc_frec.append(0)
    frecuencias[i] = doc_frec
    # print i," frecuencias ",frecuencias[i]



resultado = kMeans(frecuencias,4) #, "centroides"

if rank == master:
    print "r",resultado
    print docs

    for val in resultado:
        print docs[val], "pertenece al centroide ",resultado[val]
    tiempo_final = time()
    tiempo_ejecucion = tiempo_final - tiempo_inicial
    print 'El tiempo de ejecucion fue:',tiempo_ejecucion/60
