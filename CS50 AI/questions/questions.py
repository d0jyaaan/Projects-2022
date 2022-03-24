import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    dictionary = dict()

    for dir, i, file in os.walk(directory):
        for path in file:
            # join directory and file to form corpus/a.txt
            file_path = os.path.join(dir, path)

            # open the file and read it
            with open(f"{file_path}", encoding="utf8") as f:
                lines = f.read()
                # assign values to dict
                dictionary[path] = lines

    # print(dictionary.keys())
    # print(dictionary.values())

    return dictionary


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    final = list()
    punctuation = [punct for punct in string.punctuation]
    stopword = nltk.corpus.stopwords.words("english")

    # tokenize
    for word in nltk.tokenize.word_tokenize(document):
        word = word.lower()
        if word not in punctuation and word not in stopword:
            final.append(word)

    # print(final)

    return final


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    # number of documents
    total_documents = len(documents.keys())

    # all individual words
    words = set()
    for text in documents.values():
        for word in text:
            if word not in words:
                words.add(word)

    idf = dict()

    for word in words:
        # get how many times a word appears
        count = 0
        for text in documents.values():
            if word in text:
                count += 1

        # idf
        idf_value = math.log(total_documents / count)
        idf[word] = idf_value

    # for i in idf:
    #     print(i ,idf[i])

    return idf


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """

    temp_list = list()

    for key in files.keys():
        sum = 0
        for word in query:
            # get term frequency
            term_frequency = 0
            for word_check in files[key]:
                if word == word_check:
                    term_frequency += 1
            # tf-idf
            value = term_frequency * idfs[word]
            sum += value

        temp_list.append((key, sum))

    # sort according to tf-idf
    temp_list = sorted(temp_list, key=lambda x: x[1], reverse=True)

    final = list()
    for i in temp_list:
        final.append(i[0])

    # print(final)
    # return n top files
    return final[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """

    temp_list = list()

    for key in sentences.keys():
        # get sum of idf values and query term density
        idf = 0
        qt_density = 0
        for word in query:
            # idf
            if word in sentences[key]:
                idf += idfs[word]

            # qt_density
            for word_check in sentences[key]:
                if word == word_check:
                    qt_density += 1

        qt_density = qt_density / len(sentences[key])
        temp_list.append((key, idf, qt_density))

    # sort according to idf and query term density
    temp_list = sorted(temp_list, key=lambda x: (x[1], x[2]), reverse=True)

    final = list()
    for i in temp_list:
        final.append(i[0])

    # return n top files
    return final[:n]


if __name__ == "__main__":
    main()
