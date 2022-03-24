import random
import copy 

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # if all the cells are mines return all
        if len(self.cells) == self.count:
            return self.cells

        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        # if all cells are not mines return the all
        if self.count == 0:
            return self.cells

        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # check if cell in sentence cells
        if cell in self.cells:
            # update the sentence so that cell is no longer in the sentence
            self.cells.remove(cell)
            # reduce the mine count by 1
            self.count -= 1

        return None

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # check if cell in sentence cells
        if cell in self.cells:
            # update the sentence so that cell is no longer in the sentence
            self.cells.remove(cell)

        return None


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # 1
        # mark as a move that has been made
        self.moves_made.add(cell)

        # 2
        # mark cell as safe
        self.safes.add(cell)

        # 3
        nearby_cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell or (i, j) in self.safes:
                    continue
                # add cells within bounds
                if 0 <= i < self.height and 0 <= j < self.width:
                    nearby_cells.add((i, j))

        # add new sentence
        new_sentence = Sentence(nearby_cells, count)
        if len(new_sentence.cells) != 0:
            self.knowledge.append(new_sentence)

        # 4
        self.additional()

        # 5
        if len(self.knowledge) > 1:
            for sentence1 in self.knowledge:
                for sentence2 in self.knowledge:
                    # if sentence1 is a subset of sentence 2
                    if sentence1.cells.issubset(sentence2.cells):
                        # set 2 - set 1
                        inference_cell = sentence2.cells - sentence1.cells
                        # count 2 - count 1
                        inference_count = sentence2.count - sentence1.count
                        new_knowledge = Sentence(inference_cell, inference_count)
                        
                        # add known safes and known mines
                        if new_knowledge.known_safes():
                            for safes in new_knowledge.known_safes():
                                self.mark_safe(safes)

                        if new_knowledge.known_mines():
                            for mines in new_knowledge.known_mines():
                                self.mark_mine(mines)

    def additional(self):
        """
        mark any additional cells as safe or as mines
        if it can be concluded based on the AI's knowledge base
        """
        
        for sentence in copy.deepcopy(self.knowledge):
            # remove empty sets
            if len(sentence.cells) == 0:
                try:
                    self.knowledge.remove(sentence)
                except ValueError:
                    pass
            
            # update knowledge if got mines or safes
            mines = sentence.known_mines()
            safes = sentence.known_safes()

            if mines:
                for mine in mines:
                    self.mark_mine(mine)
                    self.conclusion()
            
            if safes:
                for safe in safes:
                    self.mark_safe(safe)
                    self.conclusion()

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        # if there are safe cells
        
        for safe in self.safes:
            # if the cell hasnt been moved before
            if safe not in self.moves_made:
                return safe

        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        
        moves = list()
        for count in range(0, self.width * self.height, 1):
            # get random width and height
            height = random.randrange(0, self.height)
            width = random.randrange(0, self.width)
            
            # not mine and not move that have been made
            if (height, width) not in self.mines and (height, width) not in self.moves_made:
                
                moves.append((height, width))

        if len(moves) == 0:
            return None
        
        else:
            random_number = random.randrange(0, len(moves))
            return moves[random_number]
