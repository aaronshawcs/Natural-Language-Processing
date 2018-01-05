import os
from collections import Counter
from math import log


def addtoken(in_list, in_token):
    in_list.append(in_token)
    return


def generate_tokens(in_list, text):
    word = []
    state = "not in word"
    for letter in text:
        if state == "in word":
            if letter == " ":
                addtoken(in_list, ''.join(word))
                state = "not in word"
            else:
                word.append(letter.lower())
        else:
            if letter is not " ":
                word = []
                state = "in word"
                word.append(letter.lower())
    return in_list


def generate_vocab(in_list):
    tuples = Counter(in_list)
    tuples = sorted(tuples.items(), key=lambda a: a[1], reverse=True)
    return tuples


def get_count(target, in_list):
    for i in in_list:
        if i[0] == target:
            return i[1]
    return 0


all_train_spam = []
for filename in os.listdir("spam-train"):
    file_data = generate_tokens([], open(os.path.join("spam-train", filename)).read())
    all_train_spam += file_data

all_train_non_spam = []
for filename in os.listdir("nonspam-train"):
    file_data = generate_tokens([], open(os.path.join("nonspam-train", filename)).read())
    all_train_non_spam += file_data

spam_test_docs = []
all_test_spam = []
for filename in os.listdir("spam-test"):
    file_data = generate_tokens([], open(os.path.join("spam-test", filename)).read())
    all_test_spam += file_data
    spam_test_docs.append(generate_vocab(file_data))

non_spam_test_docs = []
all_test_nonspam = []
for filename in os.listdir("nonspam-test"):
    file_data = generate_tokens([], open(os.path.join("nonspam-test", filename)).read())
    all_test_nonspam += file_data
    non_spam_test_docs.append(generate_vocab(file_data))
all_data = generate_vocab(all_test_nonspam + all_test_spam + all_train_non_spam + all_train_spam)
all_train_data = generate_vocab(all_train_non_spam + all_train_spam)
all_test_data = generate_vocab(all_test_nonspam + all_test_spam)
all_train_non_spam = generate_vocab(all_train_non_spam)
all_train_spam = generate_vocab(all_train_spam)
true_pos = 0
false_pos = 0
true_neg = 0
false_neg = 0
for email in spam_test_docs:
    prob_spam = 0.0
    prob_non_spam = 0.0
    for feature in email:
        numerator = float(get_count(feature[0], all_train_spam))
        denominator = float(get_count(feature[0], all_data))
        if numerator != 0.0:
            for i in range(0, feature[1], 1):
                prob_spam += log((numerator / denominator), 2)
        numerator = float(get_count(feature[0], all_train_non_spam))
        if numerator != 0.0:
            for i in range(0, feature[1], 1):
                prob_non_spam += log((numerator / denominator), 2)
    prob_spam = pow(2, prob_spam)
    prob_non_spam = pow(2, prob_non_spam)
    if prob_spam > prob_non_spam:
        true_pos += 1
    else:
        false_neg += 1
for email in non_spam_test_docs:
    prob_spam = 0.0
    prob_non_spam = 0.0
    for feature in email:
        numerator = float(get_count(feature[0], all_train_spam))
        denominator = float(get_count(feature[0], all_data))
        if numerator != 0.0:
            for i in range(0, feature[1], 1):
                prob_spam += log((numerator / denominator), 2)
        numerator = float(get_count(feature[0], all_train_non_spam))
        if numerator != 0.0:
            for i in range(0, feature[1], 1):
                prob_non_spam += log((numerator / denominator), 2)
    prob_spam = pow(2, prob_spam)
    prob_non_spam = pow(2, prob_non_spam)
    if prob_spam > prob_non_spam:
        false_pos += 1
    else:
        true_neg += 1
precision = float(true_pos) / float(true_pos + false_pos)
recall = float(true_pos) / float(true_pos + false_neg)
print("True Positives: {0}\tFalse Positives: {1}\n"
      "True Negatives: {2}\tFalse Negatives: {3}\n\n"
      "Precision: {4}\n"
      "Recall: {5}\n"
      "F-Score: {6}".format(true_pos, false_pos, true_neg, false_neg, precision, recall,
                            (2 * ((precision * recall) / (precision + recall)))))
