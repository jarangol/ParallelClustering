from mpi4py import MPI
import glob,re
import numpy as npy
from time import time


tiempo_inicial = time()

comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.size
name = MPI.Get_processor_name()

#inicializacion de variables

stop_words = set(["the","be","and","of","a","in","to","have","to","it","I","that","for","you","he",
    "with","on","do","say","this","they","at","but","we","his","from","that","not",
    "n't","by","she","or","as","what","go","their","can","who","get","if","would",
    "her","all","my","make","about","know","will","as","up","one","time","there",
    "year","so","think","when","which","them","some","me","people","take","out","into",
    "just","see","him","your","come","could","now","than","like","other","how","then",
    "its","our","two","more","these","want","way","look","first","also","new","because",
    "day","more","use","no","man","find","here","thing","give","many","well"])

docs = glob.glob("./docs/*.txt")
docs_size = 10


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
superset = set()
docs_arrays = []
if rank==3:
    for i in range(docs_size):
        docs_arrays.append(create_array(docs[i]))
    sets = []
    for i in range(docs_size):
        set_doc = set(docs_arrays[i])
        sets.append(set_doc-stop_words)
        superset = superset.union(set_doc)

    comm.bcast(superset, root=3)
    comm.bcast(docs_arrays, root=3)

superset = comm.bcast(superset, root=3)
docs_arrays = comm.bcast(docs_arrays, root=3)
print  rank
# print docs_arrays , "rank " , rank




tiempo_final = time()
tiempo_ejecucion = tiempo_final - tiempo_inicial
print 'El tiempo de ejecucion fue:',tiempo_ejecucion/60 #En segundos
