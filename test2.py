from mpi4py import MPI
import glob,re
import numpy as npy
from time import time

must_used = set(["the","be","and","of","a","in","to","have","to","it","I","that","for","you","he",
    "with","on","do","say","this","they","at","but","we","his","from","that","not",
    "n't","by","she","or","as","what","go","their","can","who","get","if","would",
    "her","all","my","make","about","know","will","as","up","one","time","there",
    "year","so","think","when","which","them","some","me","people","take","out","into",
    "just","see","him","your","come","could","now","than","like","other","how","then",
    "its","our","two","more","these","want","way","look","first","also","new","because",
    "day","more","use","no","man","find","here","thing","give","many","well"])

# docs = glob.glob("./*.txt")
docs = glob.glob("./docs/*.txt")
docs_size = 100
# print docs

comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.size
name = MPI.Get_processor_name()

jaccard_matriz = npy.zeros((docs_size,docs_size))

def create_set(inp):
    infile = open(inp, 'r')
    items = set()
    for line in infile:
        for word in line.split(' '):
            res = re.sub('[^A-Za-z0-9]+', '', word)
        items.add(res.lower())
    infile.close()
    return items

def jaccard(set1,set2):
    intersection = len(set.intersection(*[set(set1), set(set2)]))
    union = len(set.union(*[set(set1), set(set2)]))
    result = (intersection / float(union))
    return result


tiempo_inicial = time()
share = []
for i in range(rank,docs_size,size):

    for j in range(docs_size):
        set1 = create_set(docs[i])
        set2 = create_set(docs[j])
        c = jaccard(set1,set2)
        share.append([i,j,c])


tiempo_final = time()

tiempo_ejecucion = tiempo_final - tiempo_inicial
print 'El tiempo de ejecucion fue:',tiempo_ejecucion/60 #En segundos
#     comm.send(share, dest=3)
#
# if rank==3:
#     print comm.recv(source=0)
#     print comm.recv(source=1)
#     print comm.recv(source=2)
