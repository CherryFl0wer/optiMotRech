import sys
import os
import re
import math
import codecs
import collections
from operator import itemgetter
"""
 Aide à la rédaction

 1. Prend un ensemble de texte                          CHECK
 2. Extraire les ngrams                                 CHECK
 3. Classer ces ngrams en utilisant TF-IDF              CHECK
 4. Détecter la langue

 Use of https://docs.python.org/2/library/collections.html
 Counter and Deque
"""

#ngrams = collections.Counter()

nbgram = 1


def tokenize(text):
    text = text.lower()
    replaced = re.sub(r"/[0-9]/g", "", text)
    return re.findall(r"<a.*?/a>|<[^\>]*>|[\w'@#]+", replaced)


"""
    @description: Perform IDF on all the documents and 
    associate IDF with n-gram
"""


def idf(file):
    print("Processing IDF {0}gram on {1} file".format(nbgram, file))

    deck = collections.deque(maxlen=nbgram)
    idfl = collections.Counter()
    with codecs.open(file, encoding='utf-8') as f:
        for line in f:
            line = repr(line)
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


def tf(file):
    print("Processing TF {0}gram on {1} file".format(nbgram, file))

    deck = collections.deque(maxlen=nbgram)
    nb_word = 0

    tf = collections.Counter()

    with codecs.open(file, encoding='utf-8') as f:
        for line in f:
            line = repr(line)
            tokens = tokenize(line)

            nb_word += len(tokens)

            for w in tokens:
                deck.append(w)
                if len(deck) >= nbgram:
                    ng = tuple(deck)
                    tf[ng] += 1

    tftotal = {}
    for e in tf.most_common():
        freq = e[1] / nb_word
        tftotal[e[0]] = freq

    return tftotal


def setupIDF(path):
    counter = collections.Counter()
    nb_files = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            nb_files += 1
            ratio = idf(root + "/" + file)
            counter += ratio

    return counter, nb_files


def tfidf(tfdoc, idf, N):
    tmp = {}
    for gram, freq in tfdoc.items():
        tmp[gram] = freq * math.log(N / idf[gram])

    with open("lg.csv", "a") as f:
        for key, value in sorted(tmp.items(), key=itemgetter(1), reverse=True):
            f.write(str(key) + "," + str(value) + "\n")


def calculateTFIDF(path, idf, N):
    for root, dirs, files in os.walk(path):
        for file in files:
            tfOnDoc = tf(root + "/" + file)
            tfidf(tfOnDoc, idf, N)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('You need to precise a folder or a text file and the number of ngram')
        sys.exit(1)

    nbgram = int(sys.argv[1])
    folder = sys.argv[2]

    idf, nb_files = setupIDF(folder)
    calculateTFIDF(folder, idf, nb_files)
