from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
statement0 = And(AKnight, AKnave)

knowledge0 = And(

    # general knowledge
    # must be either knight or knave
    Or(AKnight, AKnave),

    # cant be both 
    Not(And(AKnight, AKnave)),

    # if statement true, a is a knight
    # if statement false, a is knave
    Biconditional(AKnight, statement0)

)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
statement1 = And(AKnave, BKnave)

knowledge1 = And(

    # general knowledge 
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),

    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    
    # if statement1 is true, A is a knight
    # else false
    Biconditional(statement1, AKnight)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
statement2A = Or(And(AKnave, BKnave), And(AKnight, BKnight))
statement2B = Or(And(AKnight, BKnave), And(AKnave, BKnight))

knowledge2 = And(

    # general knowledge
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),

    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),

    # if statement A/B is true, A/B is a knight
    # else false
    Biconditional(statement2A, AKnight),

    Biconditional(statement2B, BKnight)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
statement3A = Or(AKnight, AKnave)
statement3B = And(AKnave, CKnave)
statement3C = AKnight

knowledge3 = And(

    # general knowledge
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
 
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),

    # if statement A/B/C is true, A/B/C is a knight
    # else false
    Biconditional(statement3A, AKnight),

    Biconditional(statement3B, BKnight),

    Biconditional(statement3C, CKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
