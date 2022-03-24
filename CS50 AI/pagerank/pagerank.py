import os
import random
import re
import sys
from tempfile import TemporaryDirectory
from tkinter import N

from pkg_resources import Distribution

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")

    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # distribution dictionary
    dis_dict = dict()

    # check whether page has link
    if len(corpus[page]) != 0:

        # damping factor / number of the links in the current page
        probability = damping_factor / len(corpus[page])
        # 1 - damping factor / number of pages in corpus
        random_prob = (1 - damping_factor) / len(corpus)

        for pages in corpus:
            # if page not in one of the links
            if pages not in corpus[page]:
                dis_dict[pages] = random_prob
            else:
                dis_dict[pages] = random_prob + probability

    # if page has no outgoing links
    else:
        # length of the corpus
        corpus_length = len(corpus)
        for pages in corpus:
            # probability distribution that chooses randomly among all pages with equal probability
            dis_dict[pages] = 1 / corpus_length

    return dis_dict


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """ 
    dis_dict = {}
    for pages in corpus:
        dis_dict[pages] = 0

    for iteration in range(n):
        # first sample
        if iteration == 0: 
            # randomly choose a key
            keys = list(corpus.keys())
            sample_key = random.choice(keys)
            dis_dict[sample_key] += 1

        else:
            # get prob distribution based on previous sample
            distribution = transition_model(corpus, sample_key, damping_factor)
            keys = list()
            probability = list()
            
            # get random key based on previous sample
            for pages in distribution:
                keys.append(pages)
                probability.append(distribution[pages])

            # make new sample
            sample_key = random.choices(keys, probability).pop()
            dis_dict[sample_key] += 1

    # divide by N
    for page in dis_dict:
        dis_dict[page] = dis_dict[page] / n

    # make sure all values add to 1
    if round(sum(dis_dict.values()), 5) != 1:
        print(f"Sampling Error Total : {round(sum(dis_dict.values()), 5)}")
    else:
        print(f"Sampling Total : {round(sum(dis_dict.values()), 10)}")

    return dis_dict


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # starting
    # number of pages in corpus
    corpus_length = len(corpus)
    # distribution dictionary
    dis_dict = dict()
    
    # assigning each page a rank of 1 / N
    for pages in corpus:
        # if a page that has no links 
        if len(corpus[pages]) == 0:
            # interpreted as having one link for every page in the corpus
            corpus[pages] = {page for page in corpus}

        # assigning each page a rank of 1 / N
        dis_dict[pages] = 1 / corpus_length

    while True:
        # make a copy
        temporary_dict = dis_dict.copy()
        tracker = 0

        for page in dis_dict:

            # first part of the equation
            first = (1 - damping_factor) / len(corpus)
            
            linked = list()

            # i ranges over all pages that link to page p
            for links in corpus:
                if page in corpus[links]:
                    linked.append(links)

            sigma = list()
            
            for links in linked:
                sigma.append(temporary_dict[links] / len(corpus[links]))

            # sum all the values in sigma and form the second part of the equation
            second = sum(sigma) 
            # the output of the equation
            pr = first + (damping_factor * second)
            # append PR(p) to the distribution dictionary
            dis_dict[page] = pr
            # difference between new and previous values
            difference = temporary_dict[page] - dis_dict[page]
            if difference >= 0.001:
                tracker = tracker
            else:
                tracker += 1

        # if all values only have difference of 0.001, break out of while loop
        if tracker == len(dis_dict):
            break
    
    # make sure all values add to 1
    if round(sum(dis_dict.values()), 5) != 1:
        print(f"Iteration Error Total : {round(sum(dis_dict.values()), 5)}")
    else:
        print(f"Iteration Total : {round(sum(dis_dict.values()), 5)}")

    return dis_dict


if __name__ == "__main__":
    main()
