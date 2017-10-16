# Parallel Clustering with K-means

Proyecto realizado para el modulo de HPC en la materia tópicos especiales en
telemática, Ingeniería de Sistemas, Universidad EAFIT, 2017-2.

## Lectura de archivos
Se hace división por dominio, se asignan a cada núcleo una parte del total de documentos,
cada núcleo va tomando según su rank un documento.
cada núcleo se hace responsable de recorrer el documento palabra por palabra,  y de crear una
lista de todas las palabras por documento y un conjunto de las palabras que ocurren almenos una vez, con el objetivo de construir el conjunto de palabras que están presentes en todos los documentos a partir de los conjuntos de palabras. Se genera un diccionario con el indice del documento con key y un arreglo de todas las palabras que contiene.

## Limpieza del dataset

Posteriormente, se retiran las palabras más usadas y con menos significado (stop words) del conjunto de palabras que contiene cada documento, ya que estas no son determinantes para diferenciar los documentos que son similares, en el sentido en que probablemente estas palabras se encuentren en casi todos los documentos y notienen mayor significado.

Esto se investigo en diferentes Frequency lists, buscando los de mayor precisión y confiabilidad, gracias al tamaño de las palabras que ellos analizan para determinar la frecuencia en el idioma correspondiente.

Se selecciona una lista de stop words, que es una combinación de una [frequency List](https://www.wordfrequency.info) basada en el Corpus of Contemporary American English (COCA) y la lista [MySQL Stopwords](https://www.ranks.nl/stopwords) que es la usada por defecto por MySQL.

## Cálculo de frecuencias
Luego de haber limpiado cada set de palabras por documento, estas son enviadas al master para que sea el encargado de unir los sets y conformar el conjunto global de palabras que se hallaron en todos los documentos y el master devuelve a todos los núcleos este "superset"

A partir de este conjunto se obtienen las palabras que importan, es decir, las que se van a medir. Cada núcleo cuenta el numero de ocurrencias de estas palabras en cada uno de los
documentos que son de su dominio, y se almacena en un diccionario con el índice del documento como key y el valor va a ser un arreglo con las ocurrencias de cada palabra del superset en ese documento, para optimizar esto, solo se calcula con base en las palabras que ya se sabe que tiene cada documento, ya que anteriormente se guardó un set generado con la lista de palabras halladas en cada documento en el momento de la lectura. Las palabras que no aparecen en el set de cada documento son asignadas con 0 ocurrencias.

## Asignación de centroides
Luego de obtener esta "vectorización" de los términos, se procede a aplicar k-means. El master calcula los centroides iniciales y los envía a todos los demás, cada núcleo realiza la asignación
de centroides para los documentos que le pertenecen.A partir de la minimización de la distancia
desde cada documento a cada uno de los centroides se genera un diccionario que dice el indice del documento y el indice del centroide al que pertenece.

Como cada nucleo tiene solo una parte de los documentos, este diccionario es enviado al master para ser unificado y poder proceder con el recalculo de la posicion de los centroides.

##
