import os
from collections import Counter
from math import log
import itertools
import sys

def addtoken(in_list, in_token, in_tag="no tag"):
    if in_tag == "no tag":
        in_list.append(in_token)
    else:
        in_list.append((in_token, in_tag))
    return


def find_ngrams(input_list, n):
    return zip(*[input_list[i:] for i in range(n)])


def generate_tokens(text):
    new_list = []
    word = []
    tag = []
    state = "in word"
    carriage_return = "false"
    for letter in text:
        if (letter == '\r') or (letter == '\n'):
            if carriage_return == "false":
                carriage_return = "true"
                addtoken(new_list, ''.join(word), ''.join(tag))
                word = []
                tag = []
                state = "in word"
        else:
            carriage_return = "false"
            if letter == '/':
                state = "in tag"
            else:
                if state == "in word":
                    word.append(letter.lower())
                elif state == "in tag":
                    tag.append(letter)
    return new_list


def generate_tags(input_list):
    tags = ['###']
    for item in input_list:
        tags.append(item)
    tags.pop()
    return set(tags)


def generate_transitions(input_list):
    transition_dict = {}
    tag_sorted_transitions = []
    for item in input_list:
        tag_sorted_transitions.append((item[0][0][1], item[0][1][1]))
    tag_sorted_transitions = sorted(generate_vocab(tag_sorted_transitions), key=lambda a: a[0][0])
    for k, v in itertools.groupby(tag_sorted_transitions, key=lambda a: a[0][0]):
        k_t = []
        sum = 0.0
        k_list = list(v)
        for tuple in k_list:
            sum += float(tuple[1])
        for tuple in k_list:
            k_t.append((tuple[0][1], (tuple[1]+ 1.0) / (sum + len(tag_totals))))
        k_t = sorted(k_t, key=lambda a: a[1], reverse=True)
        transition_dict[k] = k_t
    return transition_dict


def generate_vocab(input_list):
    tuples = Counter(input_list)
    tuples = sorted(tuples.items(), key=lambda a: a[1], reverse=True)
    return tuples


def generate_emissions(counts):
    emission_dict = {}
    tag_sorted_vocab = sorted(counts, key=lambda a: a[0][1])
    for k, v in itertools.groupby(tag_sorted_vocab, key=lambda a: a[0][1]):
        k_e = []
        sum = 0.0
        k_list = list(v)
        for tuple in k_list:
            sum += float(tuple[1])
        for tuple in k_list:
            if tuple[0][0] == "###":
                k_e.append((tuple[0][0], (tuple[1]) / (sum )))
            else:
                k_e.append((tuple[0][0], (tuple[1] + 1) / (sum + len(vocabulary))))
        k_e = sorted(k_e, key=lambda a: a[1], reverse=True)
        emission_dict[k] = k_e
    return emission_dict


def generate_tag_totals(counts):
    tag_totals = []
    tag_sorted_vocab = sorted(counts, key=lambda a: a[0][1])
    for k, v in itertools.groupby(tag_sorted_vocab, key=lambda a: a[0][1]):
        sum = 0.0
        k_list = list(v)
        for tuple in k_list:
            sum += float(tuple[1])
        tag_totals.append((k, sum))
    return tag_totals


def reverse_dict(input_dict, key_list):
    new_dict = {}
    for i in key_list:
        new_dict[i] = []
    for i in input_dict:
        for j in input_dict[i]:
            new_dict[j[0]].append((i, j[1]))
    return new_dict


def generate_word_keys(input_list):
    keys = []
    for item in input_list:
        keys.append(item[0])
    keys = set(keys)
    return keys


def generate_test_sentences(text):
    new_list = []
    sentence = ["###"]
    word = []
    state = "in word"
    carriage_return = "false"
    for letter in text[9:]:
        if (letter == '\r') or (letter == '\n'):
            if carriage_return == "false":
                carriage_return = "true"
                word = ''.join(word)
                addtoken(sentence, word)
                if word == "###":
                    addtoken(new_list, sentence)
                    sentence = ["###"]
                word = []
                state = "in word"
        else:
            carriage_return = "false"
            if letter == '/':
                state = "in tag"
            else:
                if state == "in word":
                    word.append(letter.lower())
    return new_list


def generate_test_answers(text):
    new_list = []
    sentence = ["###"]
    word = []
    state = "in word"
    carriage_return = "false"
    for letter in text[9:]:
        if (letter == '\r') or (letter == '\n'):
            if carriage_return == "false":
                carriage_return = "true"
                word = ''.join(word)
                addtoken(sentence, word)
                if word == "###":
                    addtoken(new_list, sentence)
                    sentence = ["###"]
                word = []
                state = "in word"
        else:
            carriage_return = "false"
            if letter == '/':
                state = "in tag"
            else:
                if state == "in tag":
                    word.append(letter)
    return new_list


def process_raw(text):
    new_list = ["oov"]
    word = []
    carriage_return = "false"
    for letter in text:
        if (letter == '\r') or (letter == '\n'):
            if carriage_return == "false":
                carriage_return = "true"
                word = ''.join(word)
                addtoken(new_list, word)
                word = []
        else:
            carriage_return = "false"
            word.append(letter.lower())
    new_list = set(new_list)
    return new_list


def calculate_probabilities(sentence):
    apples = {}
    back_pointer = [[("###", 1)]]
    for i in range(1, len(sentence), 1):
        back_pointer.append([])
        emission_candidates = {}
        if sentence[i] in list(vocabulary):
            cur_word = sentence[i]
            for pos, prob in word_from_tag[cur_word]:
                emission_candidates[pos] = prob
        else:
            cur_word = "oov"
            for tag, count in tag_totals:
                emission_candidates[tag] = ((1.0) / (count + len(list(vocabulary))))
        apples[cur_word] = emission_candidates
        for cur_tag in apples[cur_word]:
            largest = -100000.0
            for prev_tag in tag_from_tag[cur_tag]:
                for j in range(0, len(back_pointer[i - 1]), 1):
                    if back_pointer[i - 1][j][0] == prev_tag[0]:
                        temp = log(prev_tag[1], 2) + log(apples[cur_word][cur_tag], 2) + (back_pointer[i - 1][j][1])
                        if temp > largest:
                            largest = temp
            if largest > -100000.0:
                back_pointer[i].append((cur_tag, largest))
    tag_sequence = []
    for i in reversed(range(0, len(back_pointer), 1)):
        largest = -100000
        tag = ''
        for j, k in back_pointer[i]:
            if k > largest:
                largest = k
                tag = j
        tag_sequence.insert(0, tag)
    return tag_sequence


def compare(guesses, answers, sentences):
    total = 0
    correct = 0
    total_novel = 0
    correct_novel = 0
    for i in range(0, len(guesses), 1):
        for j in range(0, len(guesses[i]), 1):
            if sentences[i][j] not in vocabulary:
                total_novel += 1
                if guesses[i][j] == answers[i][j]:
                    correct_novel += 1
            else:
                if guesses[i][j] != "###":
                    total += 1
                    if guesses[i][j] == answers[i][j]:
                        correct += 1
    return (float(correct), float(correct_novel), float(total), float(total_novel))


if __name__=="__main__":
    train_data = generate_tokens(open(os.path.join("data", "en", "entrain25k.txt")).read())
    test_sentences = generate_test_sentences(open(os.path.join("data", "en", "entest.txt")).read())
    test_answers = generate_test_answers(open(os.path.join("data", "en", "entest.txt")).read())
    raw_words = process_raw(open(os.path.join("data", "en", "enraw.txt")).read())
    vocabulary = generate_word_keys(train_data)
    bigrams = generate_vocab(find_ngrams(train_data, 2))
    counts = generate_vocab(train_data)
    tag_totals = generate_tag_totals(counts)
    tag_to_tag = generate_transitions(bigrams)
    tag_from_tag = reverse_dict(tag_to_tag, generate_tags(open("tags.txt").read()))
    tag_to_word = generate_emissions(counts)
    word_from_tag = reverse_dict(tag_to_word, vocabulary)
    results = []
    j = 0
    for i in test_sentences:
        results.append(calculate_probabilities(i))
        #print "Sentence", j+1
        #print "Tagger:", results[j]
        #print "Actual:", test_answers[j]
        if j%50 == 0:
            sys.stderr.write(".")
        j += 1
    fs = compare(results, test_answers, test_sentences)
    print("\nTagging accuracy (Viterbi decoding):{0}% (known: {1}% novel: {2}%)".format(100*((fs[0]+fs[1])/(fs[2]+fs[3])), 100*(fs[0]/fs[2]), 100*(fs[1]/fs[3])))