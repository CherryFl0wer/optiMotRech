from ngram import tf_idf_main

# Usage:
# $ python test.py
if __name__ == '__main__':
    test_folders = ["short_sentence", "short_text", "subset", "testing2", "wikipedia_test"]
    for folder in test_folders:
        tf_idf_main(["test.py", folder, folder + ".test.csv"])
