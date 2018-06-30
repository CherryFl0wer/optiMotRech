import sys
from ngram import tf_idf_main

def evaluate_tfidf(argv):
    tf_idf_main(argv)

# Usage:
# $ python main.py TEXT_FOLDER [OUPUT_FILE='output.csv'] [NB_GRAM=1]
if __name__ == '__main__':
    evaluate_tfidf(sys.argv)
