import glob
import re

files = glob.glob("./*.txt")
print(files)
infile = open(files[1], 'r')
# Mostramos por pantalla lo que leemos desde el fichero

items = set()


for line in infile:
    for word in line.split(' '):
        res = re.sub('[^A-Za-z0-9]+', '', word)
        items.add(res.lower())

infile.close()



infile = open(files[3], 'r')
# Mostramos por pantalla lo que leemos desde el fichero

items2 = set()

for line in infile:
    for word in line.split(' '):
        res = re.sub('[^A-Za-z0-9]+', '', word)
        items2.add(res.lower())

infile.close()


intersection = len(set.intersection(*[set(items), set(items2)]))
union = len(set.union(*[set(items), set(items2)]))
print("union")
print(union)
print("intersection")
print(intersection)

result = (intersection/float(union))*100
print("result")
print(result)
print("----------")
