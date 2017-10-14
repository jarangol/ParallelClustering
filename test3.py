from mpi4py import MPI
import glob,re
import numpy as npy
from time import time

stop_words = set(["the","be","and","of","a","in","to","have","to","it","I","that","for","you","he",
    "with","on","do","say","this","they","at","but","we","his","from","that","not",
    "n't","by","she","or","as","what","go","their","can","who","get","if","would",
    "her","all","my","make","about","know","will","as","up","one","time","there",
    "year","so","think","when","which","them","some","me","people","take","out","into",
    "just","see","him","your","come","could","now","than","like","other","how","then",
    "its","our","two","more","these","want","way","look","first","also","new","because",
    "day","more","use","no","man","find","here","thing","give","many","well"])

# docs = glob.glob("./*.txt")
docs = glob.glob("./dos/*.txt")
docs_size = 4
print docs

def create_array(inp):
    infile = open(inp, 'r')
    doc_words = []
    for line in infile:
        for word in line.split('\s*'):
            res = re.sub('[^A-Za-z0-9]+', '', word)
            doc_words.append(res.lower())
    infile.close()
    return doc_words

docs_arrays = []
for i in range(docs_size):
    docs_arrays.append(create_array(docs[i]))

tiempo_inicial = time()
print docs_arrays
# el set de todas las palabras
superset = set()
print  superset
sets = []
for i in range(docs_size):
    print "el set ",set(docs_arrays[i])
    set_doc = set(docs_arrays[i])
    sets.append(set_doc-stop_words)
    superset = superset.union(set_doc)

print  superset

matriz = npy.zeros((docs_size,len(superset)))
for i in range(docs_size):
    for j,palabra in enumerate(superset):
        if palabra in sets[i]:
            matriz[i][j] = docs_arrays[i].count(palabra)
        else:
            matriz[i][j] = 0

print matriz

tiempo_final = time()
tiempo_ejecucion = tiempo_final - tiempo_inicial
print 'El tiempo de ejecucion fue:',tiempo_ejecucion/60 #En segundos
