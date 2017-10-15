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

superset= comm.allgather(dataR)[3]



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
    print i," frecuencias ",frecuencias[i]

#     docs_arrays[i]=create_array(docs[i])
#
# comm.bcast(docs_arrays, root=rank)
#
# res= comm.allgather(docs_arrays)
#
# print res, "rank: ",rank

# superset = set()
# docs_arrays = {}
# if rank==3:
#     for i in range(docs_size):
#         docs_arrays[i]=create_array(docs[i])
#     comm.bcast(docs_arrays, root=3)
#
# docs_arrays = comm.allgather(docs_arrays)[3]
#
# print  docs_arrays, "rank " , rank


if rank == master:
    print "super ",superset

tiempo_final = time()
tiempo_ejecucion = tiempo_final - tiempo_inicial
# print 'El tiempo de ejecucion fue:',tiempo_ejecucion/60 #En segundos
