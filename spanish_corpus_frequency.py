from urllib.request import urlopen
import io
import re
import pandas as pd

# choose a language different from Czech and English and also from your native language
# find on-line sources of texts for the language, containing altogether more than 1 million words, and download them
# convert the material into one large plain-text utf8 file
# tokenize the file on word boundaries and print 50 most frequent tokens
# organize all these steps into a Makefile so that the whole procedure is executed after running make all
# commit the Makefile into hw/my-corpus in your git repository for this course
# do not store the data in the repository; it must be possible to (re)construct the corpus just by running the Makefile

# extra resources
# https://www.gutenberg.org/files/49836/49836-0.txt
# https://www.gutenberg.org/cache/epub/5201/pg5201.txt
# https://www.gutenberg.org/files/57648/57648-0.txt

gutenberg_url_list = ["https://www.gutenberg.org/cache/epub/17013/pg17013.txt",
"https://www.gutenberg.org/files/2000/2000-0.txt",
"https://www.gutenberg.org/cache/epub/17073/pg17073.txt",
"https://www.gutenberg.org/cache/epub/28281/pg28281.txt"]
start_of_text = "*** START OF"
end_of_text = "*** END OF"
filename = "my_spanish_corpus.txt"

spanish_stop_words = ['un', 'una', 'unas', 'unos', 'uno', 'sobre', 'todo', 'también', 'tras', 'otro', 'algún', 'alguno', 'alguna', 'algunos', \
'algunas', 'ser', 'es', 'soy', 'eres', 'somos', 'sois', 'estoy', 'esta', 'estamos', 'estais', 'estan', 'como', 'en', \
'para', 'atras', 'porque', 'que', 'estado', 'estaba', 'ante', 'antes', 'siendo', 'ambos', 'pero', 'por', 'poder', 'puede', 'puedo', \
'podemos', 'podeis', 'pueden', 'fui', 'fue', 'fuimos', 'fueron', 'hacer',    'hago', 'hace', 'hacemos', 'haceis', 'hacen', \
'cada', 'fin', 'incluso', 'primero', 'desde', 'conseguir', 'consigo', 'consigue', 'consigues', 'conseguimos', 'consiguen', \
'ir', 'voy', 'va', 'vamos', 'vais', 'van', 'vaya', 'gueno', 'ha', 'tener', 'tengo', 'tiene', 'tenemos', 'teneis', 'tienen', \
'el', 'la', 'lo', 'las', 'los', 'su', 'se', 'de', 'aqui', 'mio', 'tuyo', 'ellos', 'ellas', 'nos', 'nosotros', 'vosotros', 'vosotras', \
'si', 'dentro', 'solo', 'solamente', 'saber', 'sabes', 'sabe', 'sabemos', 'sabeis', 'saben', 'ultimo', 'largo', 'bastante', \
'haces', 'muchos', 'aquellos', 'aquellas', 'sus', 'entonces', 'tiempo', 'verdad', 'verdadero', 'verdadera', 'cierto', \
'ciertos', 'cierta', 'ciertas', 'intentar', 'intento', 'intenta', 'intentas', 'intentamos', 'intentais', 'intentan', 'dos', \
'bajo', 'arriba', 'encima', 'usar', 'uso', 'usas', 'usa', 'usamos', 'usais', 'usan', 'emplear', 'empleo', 'empleas', \
'emplean', 'ampleamos', 'empleais', 'y', 'valor', 'muy', 'era', 'eras', 'eramos', 'eran', 'modo', 'bien', 'cual', 'cuando', \
'donde', 'mientras', 'quien', 'con', 'entre', 'sin', 'trabajo', 'trabajar', 'trabajas', 'trabaja', 'trabajamos', 'trabajais', \
'trabajan', 'podria', 'podrias', 'podriamos', 'podrian', 'podriais', 'yo', 'aquel', 'a', 'no', '']

# Download from URLs and write all to one file
corpus_file = io.open(filename, 'w', encoding='utf8')
for url in gutenberg_url_list:
    with urlopen(url) as from_file:
        content = from_file.read().decode()
        start_i = content.find(start_of_text)
        end_i = content.find(end_of_text)
        corpus_file.write(content[start_i+len(start_of_text)+200:end_i])
corpus_file.close()

corpus_file = io.open(filename, encoding='utf-8')
corpus = corpus_file.read()

corpus = corpus.lower()
corpus_split_list = re.split(r"[\b\W\b]+", corpus)

print("total # of raw tokens", len(corpus_split_list))

corpus_df = pd.DataFrame({'word': corpus_split_list})
frequency_df = pd.DataFrame(data=corpus_df['word'].value_counts(dropna=True)).reset_index()
frequency_df.columns = ['word', 'count']

print("total # of unique tokens", len(frequency_df))

print("\n50 most frequent tokens\n", frequency_df.head(50))

frequency_stop_words_df = frequency_df[~frequency_df['word'].isin(spanish_stop_words)]
print("\n50 most frequent tokens without stop words\n", frequency_stop_words_df.head(50))

frequency_stop_words_long_df = frequency_stop_words_df[frequency_stop_words_df['word'].str.len() > 3]
print("\n50 most frequent tokens without stop words and short words\n", frequency_stop_words_long_df.head(50))
