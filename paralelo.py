#coding=utf-8
from mpi4py import MPI
import glob,re,random
import numpy as npy
from time import time


tiempo_inicial = time()

comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.size
name = MPI.Get_processor_name()
master = size-1
#inicializacion de variables

<<<<<<< HEAD
stop_words = set(["the","be","and","of","a","in","to","have","to","it","I","that","for","you","he",
    "with","on","do","say","this","they","at","but","we","his","from","that","not",
    "n't","by","she","or","as","what","go","their","can","who","get","if","would",
    "her","all","my","make","about","know","will","as","up","one","time","there",
    "year","so","think","when","which","them","some","me","people","take","out","into",
    "just","see","him","your","come","could","now","than","like","other","how","then",
    "its","our","two","more","these","want","way","look","first","also","new","because",
    "day","more","use","no","man","find","here","thing","give","many","well"])
=======
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
>>>>>>> b1c1345b1656cad3fb82de62aabf6c7b50facb4f

# docs = glob.glob("./dos/*.txt")
# docs_size = len(docs)
docs = glob.glob("./docs/*.txt")
docs_size = 10

def asignar(X,centroids):
    C = {}
    for i in X:
        dists = []
        for ci in centroids:
            # calculamos la distancia euclidiana del documento i al centroide ci
            dist = npy.linalg.norm(npy.array(X[i])-npy.array(ci))
            #concatenamos todas las distancias en una lista
            dists.append(dist)
        # asignamos como centroide el indice del ci de menor distancia al doc i
        C[i] = npy.argmin(dists)
    return C

def mover(centroids,X,K,C):
    # Agrupar todos los documentos que pertenecen a cada k
    k_groups = {}
    for doc in X:
        k_groups.setdefault(C[doc], []).append(X[doc])

    # promediar cada grupo del centroide k y multiplicar po el numero de docs
    # que pertenecen a ese centroide y estan esta maquina.
    pre_ponderado = {}
    for centroide in k_groups:
        mean = npy.mean(k_groups[centroide],axis=0)*len(k_groups[centroide])
        pre_ponderado[centroide]= mean

    # enviar pre ponderado al master
    comm.send(pre_ponderado,dest=master)

    if rank==master:
        #agrupamos por centroide los promedios que envia cada uno de los nodos
        agrupado = {}
        for i in range(size):
            recibido = comm.recv(source=i)
            for k in recibido:
                agrupado.setdefault(k, []).append(recibido[k])
        # se termina la ponderacion al sumar los promedios de cada centroide
        # y dividiendose por el total de documentos de cada centroide.
        for centroide in agrupado:
            total = C.values().count(centroide)
            ponderado = [sum(i)/float(total) for i in zip(*agrupado[centroide])]
            centroids[centroide] = ponderado
        # se envia la nueva ubicacion de los centroides a todos
        comm.bcast(centroids, root=master)
    # se actualizan los centroides en cada nodo
    centroids= comm.allgather(centroids)[size-1]
    return centroids

def kMeans(X,K,maxIters = 10):
    if len(X)<K:
        if rank == master:
            print "El K debe ser >= a numero de docs"
    else:
        centroides = []
        if rank==master:
            centroides = random.sample(X.values(), K)
            comm.bcast(centroides, root=master)
        centroides= comm.allgather(centroides)[size-1]
        for i in range(maxIters):
            print "iteracion ",i
            # if rank == master:
                # print "iter ",i
            # assinacion de centroides
            C = asignar(X,centroides)
            comm.send(C,dest=master)
            if rank==master:
                for i in range(size):
                    C.update(comm.recv(source=i))
                comm.bcast(C, root=master)

            C = comm.allgather(C)[size-1]
            # calculamos el promedio para cada centroide
            centroides = mover(centroides,X,K,C)
            comm.bcast(centroides, root=master)
            centroides= comm.allgather(centroides)[size-1]
        return C

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

docs_words = {}
superset = set()
sets = {}
for i in range(rank,docs_size,size):
    docs_words[i] = create_array(docs[i])
    set_doc = set(docs_words[i])
    sets[i] = set_doc-stop_words
    superset = superset.union(sets[i])

comm.send(superset, dest=master)

dataR = set()
if rank==master:
    for i in range(size):
        dataR = dataR.union(comm.recv(source=i))
    comm.bcast(dataR, root=master)

superset= comm.allgather(dataR)[size-1]

frecuencias = {}
for i in range(rank,docs_size,size):
    doc_frec = []
    for j,palabra in enumerate(superset):
        if palabra in sets[i]:
            doc_frec.append(docs_words[i].count(palabra))
            # print palabra," ",docs_words[i].count(palabra)," veces en doc ",i
            # matriz[i][j] = docs_arrays[i].count(palabra)
        else:
            doc_frec.append(0)
    frecuencias[i] = doc_frec
    # print i," frecuencias ",frecuencias[i]

<<<<<<< HEAD


resultado = kMeans(frecuencias,3) #, "centroides"
=======
resultado = kMeans(frecuencias,5) #, "centroides"
>>>>>>> b1c1345b1656cad3fb82de62aabf6c7b50facb4f

if rank == master:
    if resultado != None:
        for val in resultado:
            print docs[val], "pertenece al centroide ",resultado[val]
        tiempo_final = time()
        tiempo_ejecucion = tiempo_final - tiempo_inicial
        print 'El tiempo de ejecucion fue:',tiempo_ejecucion/60
