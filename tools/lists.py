import math
import random


def choose(list_):
    return list_[random.randint(0, len(list_) - 1)]


def flatten2d(list_):
    end_list = []
    for row in list_:
        end_list.extend(row)
    return end_list

def extract(list_, function):
    answers = []
    for item in list_:
        answers.append(function(item))

    nl = []
    ol = []

    for i in range(len(answers)):
        if answers[i]:
            nl.append(list_[i])
        else:
            ol.append(list_[i])

    return nl, ol


def hash_bit_array(list_):
    hash_ = 0
    for i in range(len(list_)):
        if list_[i]:
            hash_ += math.pow(2, i)
    return hash_
