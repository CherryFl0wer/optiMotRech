import sys
import os
import re
import collections

"""
 Aide à la rédaction

 1. Prend un ensemble de texte
 2. Extraire les ngrams
 3. Classer ces ngrams en utilisant TF-IDF
 4. Détecter la langue

 Support UTF8, plusieurs langues supporté sauf idéogramme (Chinois, Japonais, Koréan)

 Use of https://docs.python.org/2/library/collections.html
 Counter and Deque
"""

#ngrams = collections.Counter()

nbgram = 2


def tokenize(text):
    text = text.lower()
    return re.findall(r"<a.*?/a>|<[^\>]*>|[\w'@#]+", text)


"""
    @description: Perform IDF on all the documents and 
    associate IDF with n-gram
"""


def idf(file):
    print("Processing IDF {0}gram on {1} file".format(nbgram, file))

    deck = collections.deque(maxlen=nbgram)
    idfl = collections.Counter()
    with open(file, 'rb') as f:
        for line in f:
            line = str(line, 'UTF-8')
            tokens = tokenize(line)

            for w in tokens:
                deck.append(w)
                if len(deck) >= nbgram:
                    ng = tuple(deck)
                    idfl[ng] = 1
    
    return idfl

"""
    @description: Perform TF on all the documents 
"""

def tf(file, tftotal):
    print("Processing TF {0}gram on {1} file".format(nbgram, file))

    deck = collections.deque(maxlen=nbgram)
    nb_word = 0

    tf = collections.Counter()

    with open(file, 'rb') as f:
        for line in f:
            line = str(line, 'UTF-8')
            tokens = tokenize(line)

            nb_word += len(tokens)

            for w in tokens:
                deck.append(w)
                if len(deck) >= nbgram:
                    ng = tuple(deck)
                    tf[ng] += 1

    print(nb_word)
    for e in tf.most_common():
        freq = e[1] / nb_word
        tftotal[e[0]] = freq



def setupIDF(path):
    counter = collections.Counter()
    nb_files = 0 
    for root, dirs, files in os.walk(path):
        for file in files:
            nb_files += 1
            ratio = idf(root + "/" + file)
            counter += ratio

    return counter, nb_files


#TODO TF
def calculateTF(path):
    tf_freq = {}
    
    for root, dirs, files in os.walk(path):
        for file in files:
            tf(root + "/" + file, tf_freq)

    return tf_freq

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('You need to precise a folder or a text file and the number of ngram')
        sys.exit(1)

    nbgram = int(sys.argv[1])
    folder = sys.argv[2]

    idf, nb_files = setupIDF(folder)
    tf = calculateTF(folder)

    
   # print(ngrams.most_common(10))
