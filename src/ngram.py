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
    replaced = re.sub(r"[0-9]", "", text)
    return re.findall(r"<a.*?/a>|[\w]+", replaced)


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


def tfidf(tfdoc, idf, N, output_file):
    tmp = {}
    for gram, freq in tfdoc.items():
        tmp[gram] = freq * math.log(N / idf[gram])

    with open(output_file, "a", encoding="utf-8") as f:
        for key, value in sorted(tmp.items(), key=itemgetter(1), reverse=True):
            try:
                f.write(str(key) + "," + str(value) + '\n')
            except:
                print('Error writing ' + str(key) + ", " + str(value) + 'to ' + output_file)



def calculateTFIDF(path, idf, N, output_file):
    for root, dirs, files in os.walk(path):
        for file in files:
            tfOnDoc = tf(root + "/" + file)
            tfidf(tfOnDoc, idf, N, output_file)


# Usage:
# $ python ngram.py TEXT_FOLDER [OUPUT_FILE='output.csv'] [NB_GRAM=1]
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('You need to precise a folder or a text file and the number of ngram')
        print('Usage: $ python ngram.py TEXT_FOLDER [OUPUT_FILE=\'output.csv\'] [NB_GRAM=1]')
        sys.exit(1)

    input_folder = sys.argv[1]
    output_file = 'output.csv'
    nbgram = 1
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    if len(sys.argv) >= 4:
        nbgram = int(sys.argv[3])
    print('Starting calculating TF-IDF with parameters:')
    print('  - input_folder: ' + input_folder)
    print('  - output_file: ' + output_file)
    print('  - nbgram: ' + str(nbgram))

    idf, nb_files = setupIDF(input_folder)
    calculateTFIDF(input_folder, idf, nb_files, output_file)
