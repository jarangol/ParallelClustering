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
# docs_size = 10

def asignar(X,centroids):
    C = {}
    for i in X:
        dists = []
        for ci in centroids:
            # calculamos la distancia euclidiana del documento i al centroide ci
            dist = npy.linalg.norm(npy.array(X[i])-npy.array(ci))
            #concatenamos todas las distancias en una lista
            dists.append(dist)
        # asignamos como centroide el indice del ci de menor distancia al doc i
        C[i] = npy.argmin(dists)
    return C

def mover(centroids,X,K,C):
    # Agrupar todos los documentos que pertenecen a cada k
    k_groups = {}
    for doc in X:
        k_groups.setdefault(C[doc], []).append(X[doc])

    # promediar cada grupo del centroide k y multiplicar po el numero de docs
    # que pertenecen a ese centroide y estan esta maquina.
    pre_ponderado = {}
    for centroide in k_groups:
        mean = npy.mean(k_groups[centroide],axis=0)*len(k_groups[centroide])
        pre_ponderado[centroide]= mean

    # enviar pre ponderado al master
    comm.send(pre_ponderado,dest=master)

    if rank==master:
        #agrupamos por centroide los promedios que envia cada uno de los nodos
        agrupado = {}
        for i in range(size):
            recibido = comm.recv(source=i)
            for k in recibido:
                agrupado.setdefault(k, []).append(recibido[k])
        # se termina la ponderacion al sumar los promedios de cada centroide
        # y dividiendose por el total de documentos de cada centroide.
        for centroide in agrupado:
            total = C.values().count(centroide)
            ponderado = [sum(i)/float(total) for i in zip(*agrupado[centroide])]
            centroids[centroide] = ponderado
        # se envia la nueva ubicacion de los centroides a todos
        comm.bcast(centroids, root=master)
    # se actualizan los centroides en cada nodo
    centroids= comm.allgather(centroids)[size-1]
    return centroids

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

resultado = kMeans(frecuencias,5) #, "centroides"

if rank == master:
    # print "r",resultado
    # print docs
    for val in resultado:
        print docs[val], "pertenece al centroide ",resultado[val]
    tiempo_final = time()
    tiempo_ejecucion = tiempo_final - tiempo_inicial
    print 'El tiempo de ejecucion fue:',tiempo_ejecucion/60
