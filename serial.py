#El serial
import glob,re

# docs = glob.glob("./*.txt")
docs = glob.glob("./docs/*.txt")

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

for i in range(len(docs)):
    for j in range(i,len(docs)):
        print i," comparado con ",j
        # set1 = create_set(docs[i])
        # set2 = create_set(docs[j])
        # jaccard(set1,set2)
