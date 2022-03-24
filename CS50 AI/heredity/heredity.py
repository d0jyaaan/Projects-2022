import csv
from inspect import trace
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    gene_prob = 0
    # list to count probability
    probability = []

    # go through people
    for person in people:

        # get the parents and put in a dict
        mother = people[person]["mother"]
        father = people[person]["father"]

        # dict for tracking probabilities of parent's gene
        parents = {
            mother : None,
            father : None
        }

        # gene event
        # if no parents
        if mother is None and father is None:
            # if person in one gene
            if person in one_gene:
                gene_prob = PROBS["gene"][1]

            # else if person in two genes
            elif person in two_genes:
                gene_prob = PROBS["gene"][2]

            # else if not in any
            elif person not in one_gene and person not in two_genes:
                gene_prob = PROBS["gene"][0]

        # if have parents
        else:
            # get genes of both parents
            for name in parents:

                # mutation probability
                mutation = PROBS["mutation"]

                # the possiblity of parent passing gene that is mutated to child
                # if parent has no mutation
                if name not in one_gene and name not in two_genes: 
                    # can only pass mutated gene if it mutated
                    parents[name] = mutation

                # else if parent in one gene
                elif name in one_gene:
                    # can only pass it on half of the time
                    parents[name] = 0.5

                # else if parent has two genes
                elif name in two_genes:
                    # will always give the mutated gene unless it mutates
                    parents[name] = 1 - mutation

            # math
            # 1 gene
                # prob of father(yes) * prob of mother(no) + prob of father(no) * prob of mother(yes)

            # 0 gene
                # 1 - prob of parent gene
                # (1 - prob of mother) * (1 - prob of father)
            # 2 gene
                # mother * father
                # prob of mother * prob of father

            # if person in one gene
            if person in one_gene:
                first_part = parents[father] * (1 - parents[mother])
                second_part = parents[mother] * (1 - parents[father])
                gene_prob = first_part + second_part

            # else if person in two genes
            elif person in two_genes:
                gene_prob = parents[mother] * parents[father]

            # else if not in any
            elif person not in one_gene and person not in two_genes:
                first_part = 1 - parents[mother]
                second_part = 1 - parents[father]
                gene_prob = first_part * second_part

        # trait event
        # get how many genes does current person have
        gene = 0
        if person in one_gene:
            gene = 1
        elif person in two_genes:
            gene = 2
        
        # if person has traits
        if person in have_trait:
            trait_prob = PROBS["trait"][gene][True]
        else:
            trait_prob = PROBS["trait"][gene][False]

        # joint probability
        temporary = trait_prob * gene_prob
        probability.append(temporary)

    # multiplying to get the joint probability
    prob = 1
    for value in probability:
        prob = prob * value

    return prob

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    # for every name in probabilities
    # update probabilities by adding p to the specific part
    # add to the following :
        # 1 : everyone in set `one_gene` has one copy of the gene, and
        # 2 : everyone in set `two_genes` has two copies of the gene, and
        # 3 : everyone not in `one_gene` or `two_gene` does not have the gene, and
        # 4 : everyone in set `have_trait` has the trait, and
        # 5 :everyone not in set` have_trait` does not have the trait.
    for name in probabilities:
        # genes
        # 1
        if name in one_gene:
            probabilities[name]["gene"][1] += p

        # 2
        elif name in two_genes:
            probabilities[name]["gene"][2] += p    

        # 3
        elif name not in one_gene and name not in two_genes:
            probabilities[name]["gene"][0] += p

        # traits
        # 4
        if name in have_trait:
            probabilities[name]["trait"][True] += p
        # 5
        else:
            probabilities[name]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    # math
    # old probability * 1 / the total of the probabilities

    for name in probabilities:
        # genes
        # get the total of the probabilities
        total_gene = 0
        for values in probabilities[name]["gene"]:
            total_gene += probabilities[name]["gene"][values]

        # 1 / the total of the probabilities
        multiplier_gene = 1 / total_gene
        for values in probabilities[name]["gene"]:
            # old probability * 1 / the total of the probabilities
            probabilities[name]["gene"][values] *= multiplier_gene

        # traits
        total_trait = 0
        for values in probabilities[name]["trait"]:
            total_trait += probabilities[name]["trait"][values]

        multiplier_trait = 1 / total_trait
        for values in probabilities[name]["trait"]:
            probabilities[name]["trait"][values] *= multiplier_trait

        # error checking
        print(f"Multipliers : {multiplier_gene} ; {multiplier_trait}")

        check = 0
        for values in probabilities[name]["gene"]:
            check += probabilities[name]["gene"][values]
        if check != 1:
            print(f"GENES ERROR : {check}")

        check = 0
        for values in probabilities[name]["trait"]:
            check += probabilities[name]["trait"][values]
        if check != 1:
            print(f"TRAIT ERROR : {check}")


if __name__ == "__main__":
    main()
