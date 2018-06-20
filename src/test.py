import collections

ngram = 1
line1 = ["I", "love", "that", "day", "its", "such", "a", "sunny", "day"]

coll = collections.Counter()
deck = collections.deque(maxlen=ngram)

with open('./testing/alt.atheism/53068', 'rb', encoding='UTF8') as f:
    for line in f:
        for w in line:
            if ngram == 1:
                coll[w] += 1
                continue

            deck.append(w)
            if len(deck) >= ngram:
                ng = tuple(deck)
                coll[ng] += 1

print(deck)
print(coll)
