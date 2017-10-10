infile = open('Abraham Lincoln___Lincoln Letters.txt', 'r')
# Mostramos por pantalla lo que leemos desde el fichero

items = set()

for line in infile:
    for word in line.split(' '):
        items.add(word.rstrip())
infile.close()

print(items)
