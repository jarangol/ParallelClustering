from mpi4py import MPI
import glob,re
import numpy as npy
from time import time
from kmeans import *
tiempo_inicial = time()
stop_words = set(['secondly', 'all', 'consider', 'whoever', 'four', 'edu', 'go', 'causes',
                     'seemed', 'whose', 'certainly', 'everywhere', 'containing', 'to', 'does', 'th',
                     'under', 'sorry', "a's", 'sent', 'far', 'every', 'yourselves', "we'll", 'did',
                     'cause', "they've", 'try', "it'll", "i'll", 'says', "you'd", 'likely', 'further',
                     'even', "n't", 'what', 'appear', 'brief', 'goes', 'sup', 'new', 'ever',
                     "c'mon", 'respectively', 'never', 'here', 'let', 'others', "hadn't",
                     'along', "aren't", 'allows', "i'd", 'howbeit', 'usually', 'que', "i'm",
                     'changes', 'thats', 'hither', 'via', 'followed', 'merely', 'viz',
                     'everybody', 'use', 'from', 'would', 'contains', 'two', 'next', 'few',
                     'therefore', 'taken', 'themselves', 'thru', 'tell', 'more', 'knows', 'clearly',
                     'becomes', 'hereby', 'it', "ain't", 'particular', 'known', 'must', 'me',
                     'none', 'this', 'getting', 'anywhere', 'nine', 'can', 'of', 'following',
                     'my', 'example', 'indicated', 'give', "didn't", 'near', 'indicates',
                     'something', 'want', 'needs', 'rather', 'six', 'how', 'instead',
                     'okay', 'tried', 'may', 'after', 'them', 'hereupon', 'such', 'man',
                     'a', 'third', 'whenever', 'maybe', 'appreciate', 'cannot', 'so',
                     'specifying', 'allow', 'keeps', 'looking', "that's", 'help', "don't",
                     'indeed', 'over', 'mainly', 'soon', 'course', 'through', 'looks',
                     'still', 'its', 'before', 'thank', "he's", 'selves', 'inward', 'actually',
                     'better', 'willing', 'thanx', 'ours', 'might', "haven't", 'then', 'non',
                     'someone', 'somebody', 'thereby', "you've", 'they', 'not', 'now', 'day',
                     'nor', 'gets', 'hereafter', 'always', 'reasonably', 'whither', 'each',
                     'went', "isn't", 'mean', 'everyone', 'doing', 'eg', 'ex', 'year', 'our',
                     'beyond', 'out', 'by', 'furthermore', 'since', 'rd', 're', 'seriously',
                     "shouldn't", "they'll", 'got', 'get', 'forth', 'thereupon', "doesn't",
                     'little', 'quite', 'whereupon', 'besides', 'ask', 'anyhow', 'could',
                     'tries', 'keep', 'thing', 'ltd', 'hence', 'onto', 'think', 'first',
                     'already', 'seeming', 'thereafter', 'yourself', 'done', 'another',
                     'awfully', "you're", 'given', 'indicate', 'inasmuch', 'least', 'anyone',
                     'their', 'too', 'gives', 'mostly', 'that', 'nobody', 'took', 'immediate',
                     'regards', 'somewhat', 'off', 'believe', 'herself', 'than', "here's",
                     'unfortunately', 'gotten', 'second', 'were', 'toward', 'anyways', 'and',
                     'well', 'beforehand', 'say', 'unlikely', 'have', 'need', 'seen', 'seem',
                     'saw', 'any', 'relatively', 'zero', 'thoroughly', 'latter', "i've", 'downwards',
                     'aside', 'thorough', 'also', 'take', 'which', 'exactly', 'unless', 'shall',
                     'who', "where's", 'most', 'eight', 'amongst', 'nothing', 'why', 'sub',
                     'especially', 'noone', 'later', "you'll", 'definitely', 'normally',
                     'came', 'saying', 'particularly', 'anyway', 'find', 'fifth', 'one',
                     'outside', 'should', 'only', 'going', 'specify', 'sure', 'do', 'his',
                     'above', 'meanwhile', 'hopefully', 'overall', 'truly', "they'd", 'ones',
                     'nearly', 'despite', 'during', 'him', 'regarding', 'qv', 'twice', 'she',
                     'contain', "won't", 'where', 'greetings', 'ignored', "hasn't", 'namely',
                     'are', 'best', 'wonder', 'said', 'away', 'currently', 'please', "wasn't",
                     'behind', "there's", 'various', 'between', 'probably', 'neither', 'across',
                     'available', 'we', 'however', 'come', 'both', 'last', 'many', "wouldn't",
                     'thence', 'according', 'against', 'etc', 'became', 'com', "can't", 'otherwise',
                     'among', 'presumably', 'co', 'afterwards', 'had', 'whatever', 'alone',
                     "couldn't", 'moreover', 'throughout', 'considering', 'sensible', 'described',
                     "it's", 'three', 'been', 'whom', 'much', 'hardly', "it'd", 'wants', 'corresponding',
                     'latterly', 'concerning', 'else', 'hers', 'former', 'those', 'myself', 'novel', 'look',
                     'these', 'nd', 'value', 'will', 'while', 'theres', 'seven', 'whereafter',
                     'almost', 'wherever', 'is', 'thus', 'herein', 'cant', 'vs', 'in', 'ie', 'if',
                     'different', 'perhaps', 'insofar', 'make', 'same', 'wherein', 'beside',
                     'several', "weren't", 'used', 'see', 'somewhere', 'I', 'upon', 'uses',
                     'kept', 'whereby', 'nevertheless', 'whole', 'itself', 'anybody', 'obviously',
                     'without', 'comes', 'very', 'the', 'yours', 'lest', 'just', 'less', 'being',
                     'able', 'liked', 'thanks', 'useful', 'yes', 'yet', 'unto', "we've", 'seems',
                     'except', 'has', 'ought', "t's", 'around', "who's", 'possible', 'five',
                     'know', 'using', 'apart', 'name', 'necessary', 'like', 'follows', 'either',
                     'become', 'therein', 'because', 'old', 'often', 'people', 'some', 'somehow',
                     'self', 'towards', 'specified', 'ourselves', 'happens', 'for', 'though',
                     'per', 'everything', 'asking', 'provides', 'tends', 'be', 'nowhere',
                     'although', 'entirely', 'on', 'about', 'ok', 'anything', 'oh', 'theirs',
                     'whence', 'plus', 'consequently', 'or', 'seeing', 'own', 'formerly',
                     'into', 'within', 'down', 'appropriate', 'right', "c's", 'your', 'her',
                     'there', 'accordingly', 'inner', 'way', 'was', 'himself', 'elsewhere',
                     'enough', 'becoming', 'but', 'hi', 'trying', 'with', 'he', "they're",
                     'whether', 'wish', 'up', 'us', 'until', 'placed', 'below', 'un', "we'd",
                     'gone', 'sometimes', 'associated', 'certain', 'am', 'an', 'as', 'sometime',
                     'at', 'et', 'inc', 'again', 'no', 'whereas', 'when', 'lately', 'other',
                     'you', 'really', "what's", 'regardless', 'welcome', "let's", 'together',
                     'hello', "we're", 'time', 'serious', 'having', 'once'])

# docs = glob.glob("./*.txt")
docs = glob.glob("./dos/*.txt")
docs_size = len(docs)

# docs = glob.glob("./docs/*.txt")
# docs_size = 100
# print docs

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

docs_arrays = []
for i in range(docs_size):
    docs_arrays.append(create_array(docs[i]))



# el set de todas las palabras
superset = set()
sets = []
for i in range(docs_size):
    set_doc = set(docs_arrays[i])
    sets.append(set_doc-stop_words)
    superset = superset.union(set_doc)

# print superset
matriz = npy.zeros((docs_size,len(superset)))
for i in range(docs_size):
    for j,palabra in enumerate(superset):
        # print j
        if palabra in sets[i]:
            matriz[i][j] = docs_arrays[i].count(palabra)


C = kMeans(matriz, 4, maxIters = 10)
print C
for i,centro in enumerate(C):
    print docs[i], "pertenece al centroide ",centro


tiempo_final = time()
tiempo_ejecucion = tiempo_final - tiempo_inicial
print 'El tiempo de ejecucion fue:',tiempo_ejecucion/60 #En segundos
