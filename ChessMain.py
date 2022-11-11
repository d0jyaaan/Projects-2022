import sys
import os
import random
import termcolor
import pyfiglet

from multiprocessing import Process, Queue

import ChessEngine
from ChessAI import *

# dont print pygame welcome message
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

HEIGHT = 512
WIDTH = 800
DIMENSIONS = 8
SQ_SIZE = int(HEIGHT / DIMENSIONS)
MAX_FPS = 15
IMAGES = {}

BOARD_COLORS = [[(235, 235, 207), (119, 148, 84)]]

winCount = {"w": 0, "b": 0}

# get the piece to promote to
keyDict = {
    pygame.K_1: 1,
    pygame.K_2: 2,
    pygame.K_3: 3,
    pygame.K_4: 4,
}


def loadImages():
    """
    Initialise dictionary of images.
    """

    # the names of the images to load for a specific piece
    pieces = [
        "bR",
        "bN",
        "bB",
        "bQ",
        "bK",
        "bP",
        "wR",
        "wN",
        "wB",
        "wQ",
        "wK",
        "wP",
        "wKCML",  # white king checkmate (lose)
        "wKCMW",  # white king checkmate (win)
        "bKCML",  # black king checkmate (lose)
        "bKCMW",  # black king checkmate (win)
        "wKSM",  # white king stalemate
        "bKSM",  # black king stalemate
    ]

    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(
            pygame.image.load("chessai/pieces/" + piece + ".png"), (SQ_SIZE, SQ_SIZE)
        )


def main():

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color(BOARD_COLORS[0][0]))

    gamestate = ChessEngine.GameState()
    # print(gamestate.board)

    # load images
    loadImages()
    running = True

    # keep track of player clicks [(0, 4), (0, 5)]
    click = ()
    playerClicks = []

    # flag variable for if piece was dragged
    dragging = False
    # flag variable for if move was made
    moveMade = False
    # flag variable for click and drop
    clickAndDrop = False
    clickFlag = False
    # flag variable for drag and drop
    dragFlag = False
    # flag variable for pawn promotion
    promotion = False

    validMoves = gamestate.getValidMoves()

    start = False

    # print headers in the terminal
    os.system("cls" if os.name == "nt" else "clear")

    f = pyfiglet.Figlet(font="doom")
    print(termcolor.colored(f.renderText("Chess Engine"), "white"))

    print("Chess by D0jyaaan")
    print("Copyright © 2022 D0jyaaan")
    print("https://github.com/d0jyaaan")
    print("All rights reserved.\n")
    print("Thanks For Playing.")

    f = pyfiglet.Figlet(font="small")
    print(termcolor.colored(f.renderText("Controls"), "white"))

    print(termcolor.colored(f.renderText("Select Screen"), "white"))
    print("SELECT GAMEMODE : AI and Multiplayer")
    print("Q : Load PGN")
    print("W : Load FEN")

    print(termcolor.colored(f.renderText("Board"), "white"))
    print("D : Get FEN of current position")
    print("E : Get PGN of current position")
    print("R : Reset the board")

    while running:

        for event in pygame.event.get():

            # quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # select game mode
            if not start:

                screen.fill((5, 5, 5))

                # title
                font = pygame.font.SysFont("Bahnschrift SemiBold Condensed", 80)
                screen.blit(
                    font.render("Chess", True, (220, 220, 220)),
                    ((WIDTH / 2) - 85, (HEIGHT / 2) - 200),
                )

                # subtitle
                font = pygame.font.SysFont("Bahnschrift SemiBold Condensed", 40)
                screen.blit(
                    font.render("by D0jyaaan", True, (220, 220, 220)),
                    ((WIDTH / 2) - 85, (HEIGHT / 2) - 120),
                )

                # play against ai select
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),
                    ((WIDTH / 2) - 125, (HEIGHT / 2) - 50, 250, 75),
                    0,
                )

                screen.blit(
                    font.render("Play against AI", True, (5, 5, 5)),
                    ((WIDTH / 2) - 100, (HEIGHT / 2) - 25),
                )

                # multiplayer select
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),
                    ((WIDTH / 2) - 125, (HEIGHT / 2) + 35, 250, 75),
                    0,
                )

                screen.blit(
                    font.render("Multiplayer", True, (5, 5, 5)),
                    ((WIDTH / 2) - 75, (HEIGHT / 2) + 60),
                )

                # validate clicks
                if event.type == pygame.MOUSEBUTTONDOWN:

                    position = pygame.mouse.get_pos()

                    # print(position)
                    if (WIDTH / 2) - 125 <= position[0] <= (WIDTH / 2) + 125:

                        # selected play against ai
                        if ((HEIGHT / 2) - 50) <= position[1] <= ((HEIGHT / 2) + 25):
                            playagainstAI = True
                            start = True
                            playerColor = random.choice(["w", "b"])

                        # selected multiplayer
                        elif ((HEIGHT / 2) + 35) <= position[1] <= ((HEIGHT / 2) + 110):
                            playagainstAI = False
                            start = True

                if event.type == pygame.KEYDOWN:
                    # load FEN position
                    if event.key == pygame.K_q:

                        fen = input("Please input FEN. \n")
                        # check the input first
                        if checkFEN(fen):

                            gamestate.loadFENposition(fen)
                            validMoves = gamestate.getValidMoves()

                        else:
                            print("Please input a valid FEN.")

                    # load PGN position
                    elif event.key == pygame.K_w:

                        pgn = input("Please input PGN \n")

                        gamestate.loadPGNposition(pgn)
                        validMoves = gamestate.getValidMoves()

                pygame.display.update()

            # if game has started
            else:

                # if checkmate or stalemate, dont allow any moves on the board
                if gamestate.checkmate:
                    winner = gamestate.moveLog[-1].pieceMoved[0]

                    if gamestate.pgnMoveLog[-1][-1][-1] != "#":
                        winCount[winner] += 1
                        gamestate.pgnMoveLog[-1][-1] += "#"

                elif gamestate.checkmate:

                    if gamestate.pgnMoveLog[-1][-1][-1] != "=":
                        winCount["w"] += 1 / 2
                        winCount["b"] += 1 / 2
                        gamestate.pgnMoveLog[-1][-1] += "="

                else:

                    # print("here")
                    # if is pawn promotion, get input for pawn promotion
                    if promotion:

                        if playagainstAI:

                            promotionPieceKey = keyDict[1]

                            move = ChessEngine.Move(
                                playerClicks[0],
                                playerClicks[1],
                                gamestate.board,
                            )

                            move.promotionPiece = promotionPieceKey

                        elif event.type == pygame.KEYDOWN:

                            if event.key in keyDict.keys():
                                promotionPieceKey = keyDict[event.key]

                                move = ChessEngine.Move(
                                    playerClicks[0],
                                    playerClicks[1],
                                    gamestate.board,
                                )

                                move.promotionPiece = promotionPieceKey

                                # if piece moved is own piece
                                if move.pieceMoved[0] == allycolor:
                                    # print(move.getChessNotation())
                                    # if move is valid move, make the move then reset playerClicks and clicks
                                    # print("Piece Chosen and Moved :")
                                    # print(move.pieceMoved, move.pieceCaptured)
                                    # print(move.endRow, move.endCol)

                                    for i in range(len(validMoves)):
                                        # if move is a valid move
                                        if move == validMoves[i]:
                                            # print("MOVE MADE")
                                            gamestate.makeMove(move)  # make move
                                            playerClicks = []  # reset click
                                            click = ()

                                            moveMade = True

                                    # if the move made is an invalid move, keep the selection on the piece the user initially pressed
                                    if moveMade == False:
                                        playerClicks = []
                                        click = ()

                                promotion = False
                                clickFlag = False
                                dragFlag = False

                                clickAndDrop = False
                                dragging = False

                                moveMade = True

                            else:
                                promotion = True

                    # if it is not pawn promotion, just execute the code like normal
                    else:

                        # if playing against ai, 1 move is player move another is ai move
                        # only allow mouse clicks input during player move
                        if playagainstAI:

                            if gamestate.WhiteToMove and playerColor == "w":
                                playerToMove = True

                            elif gamestate.WhiteToMove == False and playerColor == "b":
                                playerToMove = True

                            else:
                                queue = Queue()
                                aiProcess = Process(
                                    target=getBestMove,
                                    args=(gamestate, validMoves, queue),
                                )
                                aiProcess.start()

                                # allMoves = []
                                # flag = True
                                move = queue.get()

                                # while flag:
                                #     print("YES")
                                #     if queue.empty():
                                #         flag = False
                                #     else:
                                #         item = queue.get()
                                #         print(item)
                                #         allMoves.append(item)

                                # sorted(allMoves, key=lambda x: x[1])
                                # aiMove = allMoves[0]

                                # if no ai moves
                                if move is None:
                                    move = random.choice(validMoves)

                                gamestate.makeMove(move)
                                moveMade = True
                                playerToMove = True

                        # mulitplayer: dont need special conditionals
                        else:
                            playerToMove = True

                        if playerToMove:

                            if event.type == pygame.MOUSEBUTTONDOWN:

                                dragging = True
                                startLocation = pygame.mouse.get_pos()

                            elif event.type == pygame.MOUSEBUTTONUP:

                                if dragging:

                                    endLocation = pygame.mouse.get_pos()

                                    startRow = int(startLocation[1] / SQ_SIZE)
                                    startCol = int(startLocation[0] / SQ_SIZE)

                                    endRow = int(endLocation[1] / SQ_SIZE)
                                    endcol = int(endLocation[0] / SQ_SIZE)

                                    # print(startRow, startCol, endRow, endcol)

                                    if endcol < 8 and startCol < 8:
                                        # means that it on click
                                        if endLocation == startLocation:

                                            if click != (startRow, startCol):
                                                click = (startRow, startCol)
                                                playerClicks.append(click)

                                            clickAndDrop = True
                                            # print(playerClicks)

                                        # click and drag
                                        else:
                                            # mouse down has been clicked before
                                            if dragging:

                                                if len(playerClicks) == 1:
                                                    if playerClicks[0] != (
                                                        startRow,
                                                        startCol,
                                                    ):
                                                        playerClicks.append(
                                                            (startRow, startCol)
                                                        )

                                                elif len(playerClicks) == 0:
                                                    playerClicks.append(
                                                        (startRow, startCol)
                                                    )
                                                    playerClicks.append(
                                                        (endRow, endcol)
                                                    )

                                                dragFlag = True

                                        # print(playerClicks)
                                        # in case or error: if playerclicks has more than 3 indexes
                                        if len(playerClicks) >= 3:
                                            playerClicks = []
                                            click = []

                                        if len(playerClicks) == 2:

                                            # if the first click is not an empty square
                                            if (
                                                gamestate.board[playerClicks[0][0]][
                                                    playerClicks[0][1]
                                                ]
                                                != "--"
                                            ):

                                                if clickAndDrop:

                                                    # if the piece captured is own piece, select that piece instead
                                                    # if click on the same square twice, deselect that piece
                                                    if (
                                                        gamestate.board[
                                                            playerClicks[0][0]
                                                        ][playerClicks[0][1]][0]
                                                        == gamestate.board[
                                                            playerClicks[1][0]
                                                        ][playerClicks[1][1]][0]
                                                    ) or (
                                                        gamestate.board[
                                                            playerClicks[0][0]
                                                        ][playerClicks[0][1]]
                                                        == gamestate.board[
                                                            playerClicks[1][0]
                                                        ][playerClicks[1][1]]
                                                    ):
                                                        click = (
                                                            playerClicks[1][0],
                                                            playerClicks[1][1],
                                                        )
                                                        playerClicks = []
                                                        playerClicks.append(click)
                                                        clickFlag = False

                                                    else:
                                                        clickFlag = True

                                                if dragFlag:
                                                    if (
                                                        playerClicks[0]
                                                        == playerClicks[1]
                                                    ):
                                                        playerClicks = []
                                                        dragFlag = False

                                                # if is click and drop / drag and drop
                                                if clickFlag or dragFlag:

                                                    if gamestate.WhiteToMove:
                                                        # print("WHITE TO MOVE")
                                                        allycolor = "w"
                                                        enemyColor = "b"
                                                    else:
                                                        # print("BLACK TO MOVE")
                                                        allycolor = "b"
                                                        enemyColor = "w"

                                                    piece = gamestate.board[
                                                        playerClicks[0][0]
                                                    ][playerClicks[0][1]]

                                                    # if is a pawn promotion
                                                    if (
                                                        (
                                                            piece == "wP"
                                                            and playerClicks[1][0] == 0
                                                        )
                                                        or (
                                                            piece == "bP"
                                                            and playerClicks[1][0] == 7
                                                        )
                                                        and not gamestate.autoPromoteToQueen
                                                    ):

                                                        promotion = True

                                                    else:

                                                        move = ChessEngine.Move(
                                                            playerClicks[0],
                                                            playerClicks[1],
                                                            gamestate.board,
                                                        )

                                                        # if piece moved is own piece
                                                        if (
                                                            move.pieceMoved[0]
                                                            == allycolor
                                                        ):
                                                            # print(move.getChessNotation())
                                                            # if move is valid move, make the move then reset playerClicks and clicks
                                                            # print(
                                                            #     "Piece Chosen and Moved :"
                                                            # )
                                                            # print(
                                                            #     move.pieceMoved,
                                                            #     move.pieceCaptured,
                                                            # )
                                                            # print(
                                                            #     move.endRow, move.endCol
                                                            # )

                                                            for i in range(
                                                                len(validMoves)
                                                            ):
                                                                # if move is a valid move
                                                                if (
                                                                    move
                                                                    == validMoves[i]
                                                                ):

                                                                    # if move is en passant
                                                                    if validMoves[
                                                                        i
                                                                    ].enPassant:
                                                                        move.enPassant = (
                                                                            True
                                                                        )

                                                                    # if move is castling
                                                                    if validMoves[
                                                                        i
                                                                    ].castle:
                                                                        move.castle = (
                                                                            True
                                                                        )
                                                                        move.castleSide = validMoves[
                                                                            i
                                                                        ].castleSide

                                                                    # print("MOVE MADE")
                                                                    gamestate.makeMove(
                                                                        move
                                                                    )  # make move

                                                                    playerClicks = (
                                                                        []
                                                                    )  # reset click
                                                                    click = ()

                                                                    moveMade = True

                                                            # if the move made is an invalid move, keep the selection on the piece the user initially pressed
                                                            if moveMade == False:
                                                                playerClicks = []
                                                                click = ()

                                                        else:
                                                            playerClicks = (
                                                                []
                                                            )  # reset click
                                                            click = ()

                                                # print(clickFlag)
                                                # print(dragFlag)

                                                # print(clickAndDrop)
                                                # print(dragging)

                                        elif len(playerClicks) == 1:
                                            continue

                                        else:
                                            playerClicks = []  # reset click
                                            click = ()

                                    # print(playerClicks)

                                    clickFlag = False
                                    dragFlag = False

                                    clickAndDrop = False
                                    dragging = False
                                    playerToMove = False
                                    if not moveMade:
                                        playerClicks = []

                        if moveMade:
                            validMoves = gamestate.getValidMoves()
                            gamestate.fiftyMoveRule(move)

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_z:
                        # undo move

                        if playagainstAI:
                            gamestate.undoMove()

                        gamestate.undoMove()
                        moveMade = True
                        validMoves = gamestate.getValidMoves()

                    elif event.key == pygame.K_r:
                        # reset board
                        temp = ChessEngine.GameState()
                        gamestate = temp
                        gamestate.checkmate = False
                        gamestate.stalemate = False
                        playerClicks = []

                        validMoves = gamestate.getValidMoves()

                    elif event.key == pygame.K_e:
                        # get the pgn of current state
                        print(termcolor.colored(f.renderText("PGN"), "white"))
                        gamestate.getPGN()

                    elif event.key == pygame.K_d:
                        # get the fen of current state
                        print(termcolor.colored(f.renderText("FEN"), "white"))
                        gamestate.convertToFEN()

                drawGameState(screen, gamestate, moveMade, validMoves, playerClicks)
                if moveMade:
                    moveMade = False
                clock.tick(MAX_FPS)
                pygame.display.flip()


def highlightSquares(screen, gamestate, validMoves, playerClicks):

    if len(playerClicks) != 0:
        if playerClicks[0] != ():
            row, col = playerClicks[0]

            if gamestate.board[row][col][0] == ("w" if gamestate.WhiteToMove else "b"):

                s = pygame.Surface((SQ_SIZE, SQ_SIZE))
                s.set_alpha(255)
                s.fill((pygame.Color(246, 246, 105)))

                # highlight the selected square
                screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))

                s.set_alpha(125)
                s.fill((pygame.Color(120, 120, 120)))

                # highlight the squares piece can move to
                for move in validMoves:
                    if move.startRow == row and move.startCol == col:

                        screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))


def drawPGN(screen, gamestate, movemade):

    """
    Display all the previous move in pgn form
    """

    length = 0
    rect = pygame.Rect(HEIGHT, 0, WIDTH - HEIGHT, HEIGHT)
    pygame.draw.rect(screen, (39, 37, 34), rect, 0)
    font = pygame.font.Font("freesansbold.ttf", 20)

    text = font.render(
        f"White : {winCount['w']}  Black : {winCount['b']}",
        True,
        (255, 255, 255),
        (39, 37, 34),
    )

    screen.blit(text, (HEIGHT + 20, 10))

    if len(gamestate.pgnMoveLog) > 20:
        length = len(gamestate.pgnMoveLog) - 20

    for i, j in enumerate(gamestate.pgnMoveLog):

        if i >= length:
            if len(j) == 1:
                text = font.render(
                    f"{i+1}.  {j[0]}", True, (255, 255, 255), (39, 37, 34)
                )

            elif len(j) == 2:
                text = font.render(
                    f"{i+1}.  {j[0]}  {j[1]}", True, (255, 255, 255), (39, 37, 34)
                )

            screen.blit(text, (HEIGHT + 20, 40 + (i - length) * 23))


def drawGameState(screen, gamestate, movemade, validMoves, playerClicks):
    """
    Graphics
    """

    drawBoard(screen)
    highlightSquares(screen, gamestate, validMoves, playerClicks)
    drawPieces(screen, gamestate)

    drawPGN(screen, gamestate, movemade)


def drawBoard(screen):
    """
    Draw the squares on the board
    """

    # row
    for x in range(DIMENSIONS):
        # col
        for y in range(DIMENSIONS):

            # choose color of board
            # first index is for pair of board color
            color = BOARD_COLORS[0][((x + y) % 2)]

            rect = pygame.Rect(y * SQ_SIZE, x * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(screen, color, rect, 0)


def drawPieces(screen, gamestate):
    """
    Draw the pieces of the current gamestate
    """

    convert = {"W": "White", "B": "Black"}
    # row
    for x in range(DIMENSIONS):
        # col
        for y in range(DIMENSIONS):

            # if square is not empty
            piece = gamestate.board[x][y]
            if piece != "--":

                # if checkmate, change the king icon
                if gamestate.checkmate:

                    if gamestate.WhiteToMove:
                        winner = "b"
                        loser = "w"
                    else:
                        winner = "w"
                        loser = "b"

                    if piece == winner + "K":
                        piece = winner + "K" + "CMW"

                    elif piece == loser + "K":
                        piece = loser + "K" + "CML"

                elif gamestate.stalemate:
                    if piece[1] == "K":
                        piece = winner + "K" + "SM"

                screen.blit(
                    IMAGES[piece],
                    pygame.Rect(y * SQ_SIZE, x * SQ_SIZE, SQ_SIZE, SQ_SIZE),
                )


def checkFEN(fen):

    """
    Check the FEN string
        If invalid, raise error
        If valid, continue

        FEN format :
            1. piece placement data
            2. active color
            3. castling rights
            4. en passant target sq
            5. half move clock
            6. full move clock

        If any of those are missing, raise error
        Check individual parts, if type error, raise error

        Example FEN :
            rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
                                1                       2  3   4 5 6
    """

    splited = fen.split(" ")
    if len(splited) != 6:
        return False

    for x, item in enumerate(splited):

        if item == "":
            return False

        if 0 <= x <= 3:

            if x == 1:
                if len(item) != 1:
                    return False

            elif x == 2:
                for i in str(item):
                    if i not in ["K", "Q", "k", "q", "-"]:
                        return False

                    if i == "-" and len(i) != 1:
                        return False

        else:
            try:
                int(item)

            except TypeError:
                return False

    return True


if __name__ == "__main__":
    main()
