import math
from os import dup
import numpy as np

text = '''Humpty Dumpty sat on a wall
Humpty Dumpty had a great fall
all the king's horses and all the king's men
couldn't put Humpty together again'''


def main(text):
    # tasks your code should perform:

    # 1. split the text into words, and get a list of unique words that appear in it
    # a short one-liner to separate the text into sentences (with words lower-cased to make words equal
    # despite casing) can be done with
    docs = [line.lower().split() for line in text.split('\n')]

    # 2. go over each unique word and calculate its term frequency, and its document frequency
    vector = dict()
    for line in docs:
        for word in line:

            if word not in vector.keys():

                df = 0
                for dup_line in docs:
                    if word in dup_line:
                        df += 1

                df = df / len(docs)
                vector[word] = df

    # print(vector)
    # 3. after you have your term frequencies and document frequencies, go over each line in the text and
    # calculate its TF-IDF representation, which will be a vector

    words = []
    for line in docs:

        list = []
        for word in vector.keys():

            tf = line.count(word) / len(line)
            tf_idf = tf * math.log(1 / vector[word], 10)
            list.append(tf_idf)

        words.append(list)

    # print(np.array(words))

    nearest_vector = []
    # 4. after you have calculated the TF-IDF representations for each line in the text, you need to
    # calculate the distances between each line to find which are the closest.
    for line1 in words:

        temp_list = []

        for line2 in words:

            if line1 == line2:
                temp_list.append(np.inf)

            else:
                temp_list.append(nearest_neigh(line1, line2))

        nearest_vector.append(temp_list)

    nearest_vector = np.array(nearest_vector)
    nearest = np.unravel_index(np.argmin(nearest_vector), nearest_vector.shape)
    print(nearest)


def nearest_neigh(a, b):

    sum = 0
    for ai, bi in zip(a, b):
        sum += abs(ai - bi)

    return sum


main(text)
