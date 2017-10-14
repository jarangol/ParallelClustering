import sys


infile = open('must_used.txt', 'r')
array = []
for line in infile:
    array.append(line)

sys.stdout.write('[')
for word in array:
    word = word.strip()
    sys.stdout.write('"'+word.rstrip()+'"'+',')
infile.close()
sys.stdout.write(']')
