# Parallel Clustering with K-means

Proyecto realizado para el modulo de HPC en la materia tópicos especiales en
telemática, Ingeniería de Sistemas, Universidad EAFIT, 2017-2.

##### Python version 2.7.X

## Ejecución

## Serial
######  $python ./serial.py

## Paralelo
Se requiere la biblioteca MPI4py

#### Instalación con Pip:
  $ pip install mpi4py
#### MPI execution

  Se puede ejecutar con el archivo executor.sh
  el cual tiene por defecto asignado 4 nucleos.

  También desde la linea de comandos con:
###### $ mpiexec -np 4 python ./paralelo.py


## Paralelización de k-means
### Lectura de archivos
Se hace división por dominio, es decir, se asignan a cada núcleo un subconjunto
 del total de documentos, cada núcleo va tomando según su rank documento por documento.

El núcleo se hace responsable de recorrer sus documentos palabra por palabra,
, de crear una lista de todas las palabras que contiene cada documento y
también crea un conjunto de las palabras que ocurren almenos una vez,
con el objetivo de construir el conjunto global de palabras de todos los documentos.
Se genera un diccionario con el indice del documento (una key) y un arreglo de
todas las palabras que contiene.

### Limpieza del dataset

Posteriormente, se retiran del conjunto de palabras que contiene cada documento
las palabras más usadas y con menos significado para  la clasificación (stop words),
 ya que estas no son determinantes para agrupar los documentos similares, en el
sentido en que probablemente estas palabras se encuentren en la mayoría de los
documentos y son palabras "vacias".

Esto se investigo en diferentes Frequency lists, buscando los de mayor precisión
y confiabilidad, gracias al tamaño de las palabras que ellos analizan para
determinar la frecuencia en el idioma correspondiente.

Se selecciona una lista de stop words, que es una combinación de una [frequency List](https://www.wordfrequency.info) basada en el
Corpus of Contemporary American English (COCA) y la lista MySQL
[Stopwords](https://www.ranks.nl/stopwords) que es la usada por defecto
por MySQL.

A partir de esto se ha generado un set de palabras que contienen los documentos
de cada nodo, este es enviado desde cada nodo al master para ser unido en un
solo "superset" y posteriormente devuelto a cada nodo/core, para actualizar la
información presente en cada uno de ellos.

### Cálculo de frecuencias
Las palabras presentes en el "superset", son las que se van a medir.
Cada núcleo cuenta el numero de ocurrencias de estas palabras en cada uno de
los documentos que son de su dominio, y se almacenan en un diccionario,
que contiene el índice del documento como key y como valor, un arreglo con el número
de ocurrencias de cada palabra del superset en ese documento.

Se hizo una optimización sobre esto, y solo se calcula con base en las palabras que ya se sabe que
tiene cada documento, ya que anteriormente se generó un set con la
lista de palabras halladas en cada documento en el momento de la lectura.
Las palabras que no aparecen en ese set se les asigna con 0 ocurrencias, evitando
este conteo.

### Asignación de centroides
Luego de obtener esta "vectorización" de los términos ya podemos comparar
cuantitativamente cada uno de ellos, se procede a aplicar k-means.
El master calcula los centroides iniciales aleatoriamente y los envía a todos los demás,
cada núcleo (worker) realiza la asignación de centroides para los documentos que le pertenecen
a partir de la minimización de la distancia desde cada documento a cada uno de
los centroides, se genera un diccionario con el índice del documento (key) y el
índice del centroide al que pertenece (value).

Como cada nucleo tiene solo una parte de los documentos, este diccionario es
enviado al master para ser unificado y poder proceder con el recalculo de la
posicion de los centroides.

### Cálculo de centroides
Es aqui de donde el algoritmo toma su nombre, se calcula la nueva posición de cada
centroide como el promedio (mean) de todos los vectores (documentos) que pertenecen a
dicho centroide. El promedio se realiza dimensión por dimensión y el resultado
es un vector (nueva posición del centroide).

Este cálculo se ha paralelizado tambien. Se calcula el promedio de cada centroide
con los documentos que tiene cada núcleo/nodo, ya que cada uno de ellos es quien
tiene los vectores que se van a promediar y se guarda en un diccionario con el
índice del centroide (ki) como key y como valor el vector resultante del promedio
, este vector es multiplicado por la cantidad de documentos que se promediaron,
con el objetivo de calcular un promedio ponderado.
Este diccionario es enviado desde cada uno de los al master, donde se calcula el
promedio ponderado, sumando los promedios parciales de cada centroide(k)
dimensión por dimensión y dividiendo esto por el total de documentos pertenecientes
a cada centroide, obteniendo así el promedio ponderado de los k centroides.

Nuevamente se envían estos valores a cada uno de los workers (slaves), para
proceder con una nueva iteración (si aplica) en donde se asignan centroides y
calculan promedios.

El método finaliza por número de iteraciones, que se pueden enviar como parámetro
o por defecto se puso un límite de 10.

Al final se imprime una respuesta indicando a que cluster pertenece cada documento.
