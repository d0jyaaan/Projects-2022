import random
from stockfish import Stockfish
from multiprocessing import Process, Queue

# stockfish evaluation
sf = Stockfish("D:/Downloads/stockfish_15_win_x64_avx2/stockfish_15_x64_avx2")
sf.set_depth(1)
sf.set_skill_level(20)

pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}

knightScores = [
    [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
    [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
    [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
    [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
    [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
    [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
    [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
    [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
]

bishopScores = [
    [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
    [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
    [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
    [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
    [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
    [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
    [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
    [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
]

rookScores = [
    [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
    [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
    [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25],
]

queenScores = [
    [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
    [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
    [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
    [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
    [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
    [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
    [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
    [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
]

pawnScores = [
    [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
    [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
    [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
    [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
    [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
    [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
    [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
    [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
]

piecePositionScores = {
    "wN": knightScores,
    "bN": knightScores[::-1],
    "wB": bishopScores,
    "bB": bishopScores[::-1],
    "wQ": queenScores,
    "bQ": queenScores[::-1],
    "wR": rookScores,
    "bR": rookScores[::-1],
    "wP": pawnScores,
    "bP": pawnScores[::-1],
}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 4


def getBestMove(gamestate, validMoves, queue):

    global nextMove
    nextMove = None

    # basic move ordering:
    # pioritise pieces in this order : K, Q, R, B, N, P
    # pioritise moves that capture pieces
    temp = []
    pieceTypeValue = {"Q": 9, "N": 3, "B": 4, "R": 5, "P": 1, "K": 10}
    for move in validMoves:
        sum = 0
        if move.pieceCaptured != "--":
            sum += 10
        sum += pieceTypeValue[move.pieceMoved[1]]
        temp.append((move, sum))

    validMoves = [x[0] for x in sorted(temp, key=lambda v: v[1], reverse=True)]

    bestMovesList = []
    negaMax(
        gamestate,
        validMoves,
        DEPTH,
        -CHECKMATE,
        CHECKMATE,
        1 if gamestate.WhiteToMove else -1,
        bestMovesList,
    )

    bestMovesList = sorted(bestMovesList, key=lambda x: x[1], reverse=True)

    tempList = []
    # print(bestMovesList)
    highestScore = bestMovesList[0][1]
    for move in bestMovesList:
        if move[1] == highestScore:
            tempList.append(move[0])

    if len(tempList) > 1:
        bestMove = random.choice(tempList)

    else:
        bestMove = tempList.pop()

    queue.put(bestMove)


def negaMax(gamestate, validMoves, depth, alpha, beta, turnMultiplier, bestMovesList):

    if depth == 0:
        return turnMultiplier * evalFunction(gamestate)

    # order : look at more important moves first

    eval = -CHECKMATE
    for move in validMoves:

        # make the move
        gamestate.makeMove(move)
        nextMoves = gamestate.getValidMoves()

        # look at the branch and get back eval
        score = -negaMax(
            gamestate,
            nextMoves,
            depth - 1,
            -beta,
            -alpha,
            -turnMultiplier,
            bestMovesList,
        )

        # if the new score is better than the current eval, keep track of it
        if score > eval:
            eval = score
            if depth == DEPTH:
                nextMove = move
                # print(eval)
                # print(
                #     move.pieceMoved,
                #     move.startRow,
                #     move.startCol,
                #     move.endRow,
                #     move.endCol,
                # )
                bestMovesList.append((nextMove, eval))

        # undo move
        gamestate.undoMove()

        # alpha beta pruning
        oldAlpha = alpha
        alpha = max(alpha, eval)
        if alpha >= beta:
            rand = random.random()
            if rand < 0.7 and not abs(beta - alpha) >= 2:
                alpha = oldAlpha
                break

    return eval


def evalFunction(gamestate):

    if gamestate.checkmate:
        if gamestate.WhiteToMove:
            return -CHECKMATE  # black wins

        else:
            return CHECKMATE  # white wins

    elif gamestate.stalemate:
        return STALEMATE

    if gamestate.WhiteToMove:
        king = gamestate.whiteKingLocation
        allycolor = "w"
        m = 1

    else:
        king = gamestate.blackKingLocation
        allycolor = "b"
        m = -1

    eval = 0
    for row in range(len(gamestate.board)):
        for col in range(len(gamestate.board[row])):

            piece = gamestate.board[row][col]
            if piece != "--":
                if piece[1] != "K":
                    sqPieceScore = piecePositionScores[piece][row][col]

                    if piece[0] == "w":
                        eval += sqPieceScore + pieceScore[piece[1]]

                    if piece[0] == "b":
                        eval -= sqPieceScore + pieceScore[piece[1]]

    # if gamestate is check, reward the checker
    inCheck, pins, checks = gamestate.pinsAndChecks()
    if inCheck:
        eval += 0.1 * m

    # piece activity, reward the number of squares own pieces can move to
    currplayerMoves = gamestate.getAllPossibleMoves()
    eval += (len(currplayerMoves) * 0.02) * m
    gamestate.WhiteToMove = not gamestate.WhiteToMove

    enemyplayerMoves = gamestate.getAllPossibleMoves()
    eval -= (len(enemyplayerMoves) * 0.02) * m
    gamestate.WhiteToMove = not gamestate.WhiteToMove

    # go through current player's moves
    # calculate center control
    # how many pieces are own pieces attacking
    # how many squares around enemy king is being attacked by own piece
    for move in currplayerMoves:
        value = pieceCenterControl(move)
        eval += value * m

    # go through enemy player's moves
    # calculate center control
    # how many pieces are enemy pieces attacking
    # how many squares around own king is being attacked by enemy piece
    for move in enemyplayerMoves:
        value = pieceCenterControl(move)
        eval -= value * m

    if len(gamestate.moveLog) < 16:
        for x, move1 in enumerate(gamestate.moveLog):
            for y, move2 in enumerate(gamestate.moveLog):
                # repetition pieces moved in the first 5 ply
                if x == y:
                    pass
                else:
                    if move != "--":
                        if move1.pieceMoved[0] == move2.pieceMoved[0]:
                            if (
                                move1.pieceMoved[1] != "P"
                                and move2.pieceMoved[1] != "P"
                            ):
                                if (move1.endRow, move1.endCol) == (
                                    move2.startRow,
                                    move2.startCol,
                                ):

                                    # black
                                    if x % 2 == 0:
                                        eval += 0.1
                                    # white
                                    else:
                                        eval -= 0.1

                                    break

        # dont move queen too early
        if len(gamestate.moveLog) < 14:
            for move in gamestate.moveLog:
                if move.pieceMoved[1] == "Q":

                    if move.pieceMoved[0] == "w":
                        eval -= 0.2
                    else:
                        eval += 0.2

    return round(eval, 3)


def pieceCenterControl(move):

    """
    Reward squares in the center that is being controlled
    """

    sum = 0
    piece = move.pieceMoved
    if piece[1] == "P":

        # in the 4 x 4 center
        if (2 <= move.endRow <= 5) and (2 <= move.endCol <= 5):
            # in 2 x 2 center
            if 3 <= move.endCol <= 4:

                # 5th rank
                if move.endRow == 3:
                    if piece[0] == "w":
                        sum += 0.095
                    else:
                        sum += 0.08

                # 4th rank
                if move.endRow == 4:
                    if piece[0] == "w":
                        sum += 0.08
                    else:
                        sum += 0.095

            else:

                # 5th rank and above
                if move.endRow <= 3:

                    # in the center
                    if 3 <= move.endCol <= 4:

                        if piece[0] == "w":
                            sum += 0.07
                        else:
                            sum += 0.05

                    # in the side center
                    else:

                        if piece[0] == "w":
                            sum += 0.065

                        else:
                            sum += 0.045

                # 4th rank and below
                if move.endRow >= 4:

                    # in the center
                    if 3 <= move.endCol <= 4:

                        if piece[0] == "w":
                            sum += 0.05
                        else:
                            sum += 0.07

                    # in the side center
                    else:
                        if piece[0] == "w":
                            sum += 0.045
                        else:
                            sum += 0.065

    else:

        if (2 <= move.endRow <= 5) and (2 <= move.endCol <= 5):
            if (3 <= move.endRow <= 4) and (3 <= move.endCol <= 4):
                sum += 0.045
            else:
                sum += 0.035

    return sum - 0.03
