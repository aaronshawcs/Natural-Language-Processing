def tokenizer(tokens, text):
    word = []
    state = "not in word"
    carriagereturn = "false"
    for letter in text:
        if (letter == '\r') or (letter == '\n'):
            if carriagereturn == "false":
                carriagereturn = "true"
                addtoken(tokens, ''.join(word))
                if state == "period":
                    addtoken(tokens, ".")
                state = "not in word"
        else:
            carriagereturn = "false"
            if letter != '"':
                if (state == "in word") or (state == "period"):
                    if letter == " ":
                        addtoken(tokens, ''.join(word))
                        if state == "period":
                            addtoken(tokens, ".")
                        state = "not in word"
                    elif (letter == ",") or (letter == "?") or (letter == "!") or (letter == ";"):
                        addtoken(tokens, ''.join(word))
                        addtoken(tokens, letter)
                        state = "not in word"
                    elif letter == ".":
                        if state == "period":
                            skipnextletter = "true"
                            addtoken(tokens, ''.join(word))
                            addtoken(tokens, "...")
                            state = "not in word"
                        elif len(word) > 1:
                            if (word[0] == "m") and ((word[1] == "r") or (word[1] == "s")):
                                word.append(letter.lower())
                                addtoken(tokens, ''.join(word))
                                state = "not in word"
                            else:
                                state = "period"
                        else:
                            state = "period"

                    else:
                        if state == "period":
                            word.append(".")
                            state = "in word"
                        word.append(letter.lower())
                else:
                    if letter is not " ":
                        word = []
                        state = "in word"
                        word.append(letter.lower())
    return tokens


def addtoken(inlist, intoken):
    inlist.append(intoken)
    return


def sentencecount(inlist):
    count = 0
    for word in inlist:
        if (word == ".") or (word == "!") or (word == "?"):
            count += 1
    return count


def wordtypes(inlist):
    vocabulary = []
    tuples = []
    for word in inlist:
        if word in vocabulary:
            for tuple in tuples:
                if tuple[0] == word:
                    tuple[1]+=1
                    break
        else:
            vocabulary.append(word)
            tuples.append([word, 1])
    newarr = sorted(tuples, key=lambda a: a[1], reverse=True)
    return newarr


def stopwordtypes(inlist, stoplist, punctuationlist):
    vocabulary = []
    tuples = []
    for word in inlist:
        if (word in stoplist) or (word in punctuation):
            if word in vocabulary:
                for tuple in tuples:
                    if tuple[0] == word:
                        tuple[1]+=1
                        break
            else:
                vocabulary.append(word)
                tuples.append([word, 1])
    newarr = sorted(tuples, key=lambda a: a[1], reverse=True)
    return newarr


def mostcommon(num, inlist, wordcount):
    for x in xrange (num):
        print("\t{0}:\t{1}\t{2}\t({3}%)".format((x+1), (inlist[x][0]), (inlist[x][1]), round(((100.0*(inlist[x][1]))/wordcount), 2)))
    return


def removestops(inlist, instops):
    stoppedlist = []
    for word in inlist:
        if word not in instops:
            stoppedlist.append(word)
    return stoppedlist


def depunctuate(inlist, inpunctuation):
    depunctuatedlist = []
    for word in inlist:
        if word not in inpunctuation:
            depunctuatedlist.append(word)
    return depunctuatedlist


def singletons(inlist):
    singletonlist = []
    for tuple in inlist:
        if tuple[1] == 1:
            singletonlist.append(tuple)
    return singletonlist


def containsdigits(inword):
    for letter in inword:
        if letter.isdigit():
            return True
    return False


def tokenswithdigits(inlist):
    tokenswithdigitslist = []
    for word in inlist:
        if containsdigits(word):
            tokenswithdigitslist.append(word)
    return tokenswithdigitslist


def containsalphas(inword):
    for letter in inword:
        if letter.isalpha():
            return True
    return False


def alphanums(inlist):
    alphanumlist = []
    for word in inlist:
        if containsalphas(word):
            alphanumlist.append(word)
    return alphanumlist



def tokenswithpunc(inlist):
    tokenswithpunclist = []
    for word in inlist:
        if not word.isalnum():
            tokenswithpunclist.append(word)
    return tokenswithpunclist


def pairs(inlist):
    pairlist = []
    index = 0
    for word in inlist:
        pairlist.append((inlist[index], inlist[index+1]))
        index += 1
        if index == len(inlist)-1:
            break
    return pairlist

print("generating token list...")
tokenlist = tokenizer([], open('sample.txt', 'r').read())

print("generating stop words...")
stopwords = tokenizer([], open('stopwords.txt', 'r').read())
punctuation = ['.',',','?','!',':',';']
print("filtering tokens...")
filteredlist = depunctuate((removestops(tokenlist, stopwords)), punctuation)
print("generating token pairs...")
tokenpairs = pairs(filteredlist)
print("generating vocabulary...")
vocabulary = wordtypes(filteredlist)
print("generating fullvocab...")
fullvocab = vocabulary + stopwordtypes(tokenlist, stopwords, punctuation)

fullvocab = sorted(fullvocab, key=lambda tup: tup[1], reverse=True)

print("a. Number of Sentences: {0}".format(sentencecount(tokenlist)))
print("b. Number of word tokens: {0}".format(len(tokenlist)))
print("c. Number of word types: {0}".format(len(vocabulary)))
print("d. Word count and percentage of the 100 most frequent tokens in the vocabulary (including stopwords and punctuations):")
mostcommon(100, fullvocab, len(tokenlist))
print("e. Word count and percentage of the 100 most frequent tokens in the vocabulary (excluding stopwords and punctuations):")
mostcommon(100, vocabulary, len(filteredlist))
print("f. Number of singletons in the corpus: {0}".format(len(singletons(vocabulary))))
print("g. Number of tokens in the vocabulary containing digits [0-9]: {0}".format(len(tokenswithdigits(filteredlist))))
print("h. Number of tokens in the vocabulary containing punctuation: {0}".format(len(tokenswithpunc(tokenlist))))
print("i. Number of tokens in the vocabulary containing both alpha [A-Za-z] and numerics [0-9]: {0}".format(len(alphanums(tokenswithdigits(filteredlist)))))
print("j. Frequency and percentage of the 100 most frequent word pairs in the corpus (excluding stopwords and punctuations):")
mostcommon(100, wordtypes(tokenpairs), len(tokenpairs))
