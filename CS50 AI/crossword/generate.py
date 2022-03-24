from ast import Assign
from audioop import cross
from ctypes import resize
from distutils.log import error
import queue
from re import T
from sre_constants import FAILURE
from ssl import ALERT_DESCRIPTION_ACCESS_DENIED
import sys
from tempfile import tempdir
from typing import Reversible, final

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # value in domain is consistent with the unary constraints
        # value has same number as variables length

        # for value in domain:
        for variable in self.crossword.variables:
            # for word in value:
            for x in self.crossword.words:
                # if len(word) != variable length:
                if len(x) != variable.length:
                    # self.domains[v].remove(x)
                    self.domains[variable].remove(x)
        # no return value

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # remove any value in x domain that dont have possible value in y domain

        # revised = false
        # for x in X.domain:
            # if no y in Y.domain satisfies constraint for (X,Y):
                # delete x from X.domain
                # revised = true
        # return revised

        # get overlap
        overlap = self.crossword.overlaps[x,y]
        removed = list()

        if overlap:
            for value in self.domains[x].copy():
                for check in self.domains[y]:
                    revised = False
                    # if x is not same as y, if x overlap is not same as y overlap
                    if value != check and value[overlap[0]] == check[overlap[1]]:
                        revised = True
                        break
                
                if not revised:
                    removed.append(value)

            for word in removed:
                self.domains[x].remove(word)

        return False


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.        
        """

        # if arcs is none
        if arcs is None:
            temp_list = list()
            # all the arcs
            for arc1 in self.crossword.variables    :
                # get the variables that x is linked to
                for arc2 in self.crossword.neighbors(arc1):
                    if arc1 != arc2:
                        # add arc into list
                        arc = (arc1, arc2)
                        temp_list.append(arc)
            # queue
            queue = temp_list

        queue = arcs
        # while queue is not empty
        while queue:
            # dequeue
            (x, y) = queue.pop()

            if self.revise(x, y):
                # cant solve question, return False
                if len(self.domains[x]) == 0:
                    return False
                
                neighbour = self.crossword.neighbors(x)
                # enqueue
                if y in neighbour:
                    neighbour = neighbour - {y}
                for z in neighbour:
                    queue.append((z, x))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for variable in self.crossword.variables:
            # if variable does not exist in assignment
            if variable not in assignment.keys():
                return False

        # return True if assignment is complete
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """    

        # length
        for key in assignment:
            if assignment[key] is not None:
                if len(assignment[key]) != key.length:
                    return False

        # conflicting
        for variable in assignment:
            for neighbour in self.crossword.neighbors(variable):
                if neighbour in assignment:
                    x, y = self.crossword.overlaps[variable, neighbour]
                    if assignment[variable][x] != assignment[neighbour][y]:
                        return False
                        
        # distinct
        Alist = [*assignment.values()]
        if len(set(Alist)) != len(Alist):
            return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        # list to store values according to their values
        values = list()

        # heuristic
        for word in self.domains[var]:
            counter = 0
            for overlap in self.crossword.neighbors(var):
                
                if overlap in assignment:
                    continue

                x, y = self.crossword.overlaps[var, overlap]

                for overlap_word in self.domains[overlap]:
                    # if words not same
                    if overlap_word[y] != word[x]:
                        counter += 1

            values.append((word, counter))

        # sort the list from least to most
        values.sort(key=lambda value:value[1])

        final = list()
        # put all the words in another sorted list
        for value in values:
            final.append(value[0])
        
        return final


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variabsle with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        temp_list = list()

        # for all variables
        for variable in self.crossword.variables:
            # if variable not in assignment
            if variable not in assignment.keys():
                temp_list.append((variable, len(self.domains[variable])))

        temp_list.sort(key=lambda value:value[1])

        return temp_list[0][0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        # if assisgnment is complete, return
        if self.assignment_complete(assignment):
            return assignment

        variable = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(variable, assignment):

            assignment[variable] = value

            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                
            del assignment[variable]

        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None
    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
