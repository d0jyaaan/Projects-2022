from distutils import text_file
import nltk
import sys
import string

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until" 
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP VP Conj NP VP | S Conj VP | S NP
NP -> N | Det N | AP NP | NP AP | Det AP N | P NP
VP -> V | V NP | VP Conj VP | Adv VP | V Adv 
AP -> Adj | Adj AP | Adv
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # list of lowercase alphabets
    alphabets = string.ascii_lowercase

    # convert characters to lowercase
    sentence = sentence.lower()
    
    # tokenize sentence
    text = nltk.tokenize.word_tokenize(sentence)
    
    seen = list()
    for word in text.copy():
        # if word has been seen, skip
        if word in seen:
            continue
        
        count = 0
        # add word to seen words
        seen.append(word)

        for letters in word:
            # if word contains at least one alphabetic char
            if letters in alphabets:
                count += 1
        
        if count > 0:
            continue
        
        # remove word
        else:
            text.remove(word)

    print(text)
    return (text)


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # get all the subtrees that have the label "NP"
    lst = list()
    for subtree in tree.subtrees():
        if subtree.label() == "NP":
            lst.append(subtree)
    
    # check if a noun phrase appear in a diff noun phrase
    copy_list = lst.copy()
    for phrase1 in copy_list:
        for phrase2 in copy_list:
            # if phrase2 not in phrase1 and they are different noun phrases
            if phrase2 in phrase1 and phrase2 != phrase1:
                # if phrase hasnt been deleted
                if phrase1 in lst:
                    lst.remove(phrase1)
        
    return lst

if __name__ == "__main__":
    main()
