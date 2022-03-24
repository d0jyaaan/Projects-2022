"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # In the initial game state, X gets the first move. Subsequently, the player alternates with each additional move
    # Any return value is acceptable if a terminal board is provided as input (i.e., the game is already over)

    counter = 1

    # loop through whole board
    for row in range(3):
        for cell in range(3):

            # if not empty, add to counter
            if board[row][cell] != EMPTY:
                counter = counter + 1

    # if 1, X
    # if 0, O
    if counter % 2 == 1:
        return (X)

    elif counter % 2 == 0:
        return (O)

    else:
        return None


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # Each action should be represented as a tuple (i, j) where i corresponds to the row of the move (0, 1, or 2) and j corresponds to which cell in the row corresponds to the move (also 0, 1, or 2).
    # Possible moves are any cells on the board that do not already have an X or an O in them.
    # Any return value is acceptable if a terminal board is provided as input

    action = set()

    for row in range(3):
        for cell in range(3):

            if board[row][cell] == EMPTY:
                action.add((row, cell))

    return(action)


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    """
    If action is not a valid action for the board, your program should raise an exception.

    The returned board state should be the board that would result from taking the original input board,
    and letting the player whose turn it is make their move at the cell indicated by the input action.

    Importantly, the original board should be left unmodified:
    since Minimax will ultimately require considering many different board states during its computation.
    This means that simply updating a cell in board itself is not a correct implementation of the result function.
    You’ll likely want to make a deep copy of the board first before making any changes.
    """
    if action == EMPTY:
        return(board)

    turn = player(board)
    
    row = int(action[0])
    cell = int(action[1])

    # invalid action
    if board[row][cell] != EMPTY:
        raise Exception("Invalid action")

    else:
        temp = copy.deepcopy(board)
        temp[row][cell] = turn

    return(temp)


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # row and cell checking
    for cell in range(3):
        # vertical
        if board[0][cell] == board[1][cell] and board[2][cell] == board[1][cell]:
            
            if board[0][cell] == X:
                return X

            elif board[0][cell] == O:
                return O

    for row in range(3):
        # horizontal
        if board[row][0] == board[row][1] and board[row][2] == board[row][1]:

            if board[row][0] == X:
                return X

            elif board[row][0] == O:
                return O

    # diagonals
    if board[0][0] == board[1][1] and board[2][2] == board[1][1]:

        if board[0][0] == X:
            return X

        elif board[0][0] == O:
            return O

    if board[0][2] == board[1][1] and board[2][0] == board[1][1]:

        if board[0][2] == X:
            return X

        elif board[0][2] == O:
            return O

    # if draw or game in progress
    return None

def tie(board):

    total = 9

    for row in range(3):
        for cell in range(3):

            if board[row][cell] is not EMPTY:
                total = total - 1
    
    return total == 0


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    game = winner(board)
    counter = 0

    # if there is a winner
    if winner(board) or tie(board):
        return True

    else: 
        return None


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    game = winner(board)

    # X wins
    if game == X:
        return 1

    # O wins
    elif game == O:
        return -1

    # if draw
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # The move returned should be the optimal action (i, j) that is one of the allowable actions on the board. 
    # If multiple moves are equally optimal, any of those moves is acceptable.
    # If the board is a terminal board, the minimax function should return None
    
    # if board is terminal board
    if terminal(board):
        return None

    # player x
    elif player(board) == X:

        score = []
        for action in actions(board):
            score.append([min_eval(result(board, action)), action])

        optimal = sorted(score, key=lambda x: x[0], reverse=True)[0][1]
        return optimal

    # player o
    elif player(board) == O:

        score = []

        for action in actions(board):
            score.append([max_eval(result(board, action)), action])

        optimal = sorted(score, key=lambda x: x[0])[0][1]
        return optimal


    
def max_eval(board):

    # max value state
    v = float("-inf")
    
    if terminal(board):
        return(utility(board))

    for action in actions(board):

        v = max(v, min_eval(result(board, action)))

    return v


def min_eval(board):
    # min value state
    v = float("inf")

    if terminal(board):
        return(utility(board))

    for action in actions(board):

        v = min(v, max_eval(result(board, action)))

    return v
        