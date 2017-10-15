#El serial
import glob,re
import numpy as npy
import sys
import pylab as plt
import numpy as np
plt.ion()

must_used = set(["the","be","and","of","a","in","to","have","to","it","I","that","for","you","he",
    "with","on","do","say","this","they","at","but","we","his","from","that","not",
    "n't","by","she","or","as","what","go","their","can","who","get","if","would",
    "her","all","my","make","about","know","will","as","up","one","time","there",
    "year","so","think","when","which","them","some","me","people","take","out","into",
    "just","see","him","your","come","could","now","than","like","other","how","then",
    "its","our","two","more","these","want","way","look","first","also","new","because",
    "day","more","use","no","man","find","here","thing","give","many","well"])

# docs = glob.glob("./*.txt")
docs = glob.glob("./dos/*.txt")

size = (len(docs))

group1 = set()
group1 = set()

jaccard_matriz = npy.zeros((size,size))

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

def kMeans(X, K, maxIters = 4):

    centroids = X[npy.random.choice(npy.arange(len(X)), K), :]
    for i in range(maxIters):
        # Cluster Assignment step
        C = npy.array([npy.argmin([npy.dot(x_i-y_k, x_i-y_k) for y_k in centroids]) for x_i in X])
        # Move centroids step
        centroids = [X[C == k].mean(axis = 0) for k in range(K)]
    return npy.array(centroids) , C

for i in range(0,5):
    for j in range(0,5):

        set1 = create_set(docs[i])
        set2 = create_set(docs[j])
        jaccard_matriz[i][j] = jaccard(set1,set2)
    print i

for fila in range(len(jaccard_matriz)):
    for col in range(len(jaccard_matriz)):
        sys.stdout.write(str('{:^1.2f}'.format(jaccard_matriz[fila][col])))
        sys.stdout.write("   ")
    print  "\n"

print docs
centroids, C = kMeans(jaccard_matriz, K = 2)
print centroids
print C
