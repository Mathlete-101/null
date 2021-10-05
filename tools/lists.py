import random


def choose(list_):
    return list_[random.randint(0, list_.length - 1)]


def flatten2d(list_):
    end_list = []
    for row in list_:
        end_list.extend(row)

    return end_list
