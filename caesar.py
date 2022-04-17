from sys import *

import os

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
          'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

if len(argv) == 2:
    key = argv[1]
    if isinstance(key, int):

        key = int(argv[1])

        text = input("plaintext:")

        lst = list()
        for letter in text:
            print(letter)

            if letter == " ":
                lst.append(letter)

            else:
                for i in range(0, len(letters), 1):

                    if letters[i] == letter:

                        new = key + i
                        if new > 25:
                            new -= 26

                        if letter.isupper():
                            lst.append(letters[new].upper())
                        else:
                            lst.append(letters[new])

        print("ciphertext:")

        for letter in lst:
            print(letter, end="")

        print("\n")

    else:
        print("Please input integer")

else:
    print("Usage: python caesar.py key")


