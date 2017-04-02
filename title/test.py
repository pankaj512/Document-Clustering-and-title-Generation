import nltk
s = "i am pankaj kumar"
data = s.split()
bigram = list(nltk.bigrams(data))
list_of_bi = []
for b in bigram:
    list_of_bi.append(' '.join(b))
print(list_of_bi)