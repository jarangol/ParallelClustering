import re
infile = open('William Wordsworth___The Prose Works of William Wordsworth.txt', 'r')
# Mostramos por pantalla lo que leemos desde el fichero

items = set()

for line in infile:
    for word in line.split(' '):
        res = re.sub('[^A-Za-z0-9]+', '', word)
        items.add(res.lower())

infile.close()



infile = open('John Bunyan___The Works of John Bunyan.txt', 'r')
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

result = (intersection/float(union))
print("result")
print(result)
