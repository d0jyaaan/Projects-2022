from cs50 import get_string

# initialisation
temp = get_string("Text: ")
length = len(temp)
letters = 0
words = 0
sentences = 0

# calculate letter, word and sentence
text = temp.lower()
syntax = ['!', '.', '?']

for i in range(0, length, 1):
    if text[i].isalpha() == True:
        letters += 1

    elif text[i] == ' ':
        words += 1

    elif text[i] in syntax:
        sentences += 1

# last word
words += 1

L = letters / (words / 100)
S = sentences / (words / 100)

# algorithm
index = 0.0588 * L - 0.296 * S - 15.8

# round
index = round(index)

# print result
if index > 1 and index < 16:
    print(f"Grade {index}")

elif index <= 1:
    print("Before Grade 1")

elif index >= 16:
    print("Grade 16+")

