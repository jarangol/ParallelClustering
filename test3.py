from mpi4py import MPI
import glob,re

# docs = glob.glob("./*.txt")
docs = glob.glob("./docs/*.txt")


comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.size
name = MPI.Get_processor_name()


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


for j in range(rank,len(docs)):
    # set1 = create_set(docs[rank])
    print rank," comparado con ",j, " rank ",rank
    # set2 = create_set(docs[j])
    # jaccard(set1,set2)
