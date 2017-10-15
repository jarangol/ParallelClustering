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
# if rank!=3:
for i in range(rank,docs_size,size):
    for j in range(i+1,docs_size):
        set1 = create_set(docs[i])
        set2 = create_set(docs[j])
        c = jaccard(set1-must_used,set2-must_used)
        share.append([i,j,c])

comm.send(share, dest=3)

if rank==3:
    matriz = npy.ones((docs_size,docs_size))
    response = []
    for i in range(size):
        response.append(comm.recv(source=i))

    for i in range(len(response)):
        for j in range(len(response[i])):
            f = response[i][j][0]
            c = response[i][j][1]
            matriz[f][c] = response[i][j][2]
            matriz[c][f] = response[i][j][2]

    print matriz
tiempo_final = time()

tiempo_ejecucion = tiempo_final - tiempo_inicial
print 'El tiempo de ejecucion fue:',tiempo_ejecucion/60 #En segundos
