# Parallel Clustering with K-means

Proyecto realizado para el modulo de HPC en la materia tópicos especiales en
telemática, Ingeniería de Sistemas, Universidad EAFIT, 2017-2.

## Limpieza del dataset

Se retiran las palabras más usadas y con menos significado en cada lenguaje, ya que estas no son determinantes para diferenciar los documentos que son similares, en el sentido en que probablemente estas palabras se encuentren en casi todos los documentos.

Esto se investigo en diferentes Frequency lists, buscando los de mayor precisión y confiabilidad, gracias al tamaño de las palabras que ellos analizan para determinar la frecuencia en el idioma correspondiente.

Se selecciona una lista de frecuencia basada en el Corpus of Contemporary American English (COCA) 
