import numpy as np


def generate(p1):
    # change this so that it generates 10000 random zeros and ones
    # where the probability of one is p1
    seq = np.random.choice([0, 1], p=[1-p1, p1], size=10000)

    return seq


def count(seq):
    # insert code to return the number of occurrences of 11111 in the sequence
    count = 0
    # iterate through all elements
    for i in range(0, len(seq), 1):
        check = 0

        # check for 11111
        for j in seq[i: i+5]:
            if j == 1:
                check += 1
        if check == 5:
            count += 1

    return count


def main(p1):
    seq = generate(p1)
    return count(seq)


print(main(2/3))
