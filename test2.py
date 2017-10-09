from mpi4py import MPI
import glob
import re

docs = glob.glob("./*.txt")



comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.size
name = MPI.Get_processor_name()



def create_set(infile):
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


for j in range(rank,len(docs)):
    print docs[rank]," comparado con ",docs[j], "rank ",rank
    set1 = create_set(docs[rank])
    set2 = create_set(docs[j])
    jaccard(set1,set2)


