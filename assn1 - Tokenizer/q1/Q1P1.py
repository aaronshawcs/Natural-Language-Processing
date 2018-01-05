import nltk
f = open('sample.txt', 'r')
i = f.read()
tokens = nltk.word_tokenize(i,'english')
wordcount = len(tokens)
wordtypes = sorted(set(tokens))
print("Number of tokens: {0}\nNumber of word types: {1}".format(len(tokens),len(wordtypes)))
frequency = nltk.FreqDist(tokens)
print("Most frequent 20 words:")
for sample in frequency.most_common(20):
    print("{0}\t:\t{1} ({2}%)".format(sample[0], sample[1], 100*float(sample[1])/wordcount))
print("Singletons ({0}% of file each):".format(100.0/wordcount))
for sample in frequency.items():
    if sample[1] == 1:
        print(sample[0])