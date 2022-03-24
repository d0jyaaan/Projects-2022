import sys
import csv


def main():

    # input checker
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py CSV txt")

    # assign files

    DNA = open(sys.argv[2], 'r').read()
    csv_file = open(sys.argv[1], 'r')
    # read files
    person = {}
    strands = []

    for ind, row in enumerate(csv_file):
        if ind == 0:
            strands = [strand for strand in row.strip().split(',')[1:]]
        else:
            current_row = row.strip().split(',')
            person[current_row[0]] = [int(x) for x in current_row[1:]]

    # strand counting
    strand_counter = []
    for strand in strands:
        i = 0
        max_ = -1
        current_max = 0
        while i < len(DNA):
            if DNA[i:i+len(strand)] == strand:
                current_max += 1
                max_ = max(max_, current_max)
                i += len(strand)

            else:
                current_max = 0
                i += 1
        # writing the value to counter
        strand_counter.append(max_)

    # if match print name
    for name, data in person.items():
        if data == strand_counter:
            print(name)
            sys.exit(0)

    print("No match")


main()