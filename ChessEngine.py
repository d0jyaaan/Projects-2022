from multiprocessing.sharedctypes import Value
from shutil import move
from sklearn.inspection import PartialDependenceDisplay
import numpy as np
import copy


class GameState:
    def __init__(self):

        # board is a 8x8 list, each element has 2 characters
        # "--" represents empty space (no piece)
        self.board = np.array(
            [
                ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
                ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
            ]
        )

        # dictionary of functions to get the moves of a certain piece
        self.getPieceMovesFunction = {
            "K": self.getKingMoves,
            "Q": self.getQueenMoves,
            "B": self.getBishopMoves,
            "N": self.getKnightMoves,
            "P": self.getPawnMoves,
            "R": self.getRookMoves,
        }

        self.WhiteToMove = True
        self.moveLog = []

        # black and white king location
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)

        # checks and pins
        self.inCheck = False
        self.pins = []
        self.checks = []

        self.checkmate = False
        self.stalemate = False

        # promotion
        self.autoPromoteToQueen = False

        self.castling = {"wKs": True, "wQs": True, "bKs": True, "bQs": True}
        self.enPassant = False
        self.enPassantTarget = None

        self.fiftyMoveCount = 0

        self.pgnMoveLog = []

        # pawn promotion
        self.pawnPromotionDict = {
            1: "Q",
            2: "R",
            3: "B",
            4: "K",
        }
        self.pawnPromotionDictRev = {v: k for k, v in self.pawnPromotionDict.items()}

    def fiftyMoveRule(self, move):

        """
        Draw if only kings left on board
        Draw if no capture has been made and
        no pawn has been moved in the last fifty consecutive move
        """

        # if only kings are left on the board
        flag = False
        for i in self.board:
            for j in i:
                if j[1] != "k":
                    flag = True
                    break

            if flag:
                break

        if not flag:
            self.stalemate = True

        # 50 move rule
        if move.pieceCaptured != "--" or move.pieceMoved[1] == "P":
            self.fiftyMoveCount += 1
        else:
            self.fiftyMoveCount = 0

        if self.fiftyMoveCount == 50:
            self.stalemate = True

        # print(f"Stalemate : {self.stalemate}")

    def makeMove(self, move):

        """
        Make a move given user input

        Check for special moves and make the move:
            1. pawn promotion
            2. en passant
            3. castling
        """

        self.fiftyMoveRule(move)

        # where the piece moved to
        self.board[move.endRow][move.endCol] = move.pieceMoved
        # empty the square where it moved from
        self.board[move.startRow][move.startCol] = "--"
        # add to move log
        self.moveLog.append(move)

        # update castling rights when rook is moved
        if move.pieceMoved[1] == "R":
            if move.startCol < 4:
                castleside = move.pieceMoved[0] + "Qs"
                self.castling[castleside] = False
            elif move.startCol > 4:
                castleside = move.pieceMoved[0] + "Ks"
                self.castling[castleside] = False

        # update the board in case of pawn promotion
        if move.isPawnPromotion:
            if self.autoPromoteToQueen:
                self.board[move.endRow][move.endCol] = move.pieceMoved[0] + "Q"

            else:
                self.board[move.endRow][move.endCol] = (
                    move.pieceMoved[0] + self.pawnPromotionDict[move.promotionPiece]
                )

        # en passant
        if move.enPassant:
            self.board[move.startRow][move.endCol] = "--"

        # update king's position and update castling rights
        if move.pieceMoved == "wK":
            self.castling["wKs"] = False
            self.castling["wQs"] = False
            self.whiteKingLocation = (move.endRow, move.endCol)

        elif move.pieceMoved == "bK":
            self.castling["bKs"] = False
            self.castling["bQs"] = False
            self.blackKingLocation = (move.endRow, move.endCol)

        # if castling move
        if move.castle:
            # if castling is queen side
            if move.castleSide == "Qs":
                # remove the rook
                self.board[move.startRow][0] = "--"
                # swap rook to next to king
                self.board[move.endRow][move.endCol + 1] = move.pieceMoved[0] + "R"
                # already castled, so castling rights is gone
                self.castling[move.pieceMoved[0] + "Qs"] = False

            # if castling is king side
            elif move.castleSide == "Ks":
                self.board[move.startRow][7] = "--"
                self.board[move.endRow][move.endCol - 1] = move.pieceMoved[0] + "R"
                self.castling[move.pieceMoved[0] + "Ks"] = False

        # swap players
        self.WhiteToMove = not self.WhiteToMove

        self.pgnAppend()

    def undoMove(self):

        """
        Undo the previous move
        """

        if len(self.moveLog) != 0:

            previousMove = self.moveLog.pop()  # get previous move

            # gain back castling rights if the previous move was a check and the king was moved
            inCheck, pins, checks = self.pinsAndChecks()
            if inCheck:
                piece = previousMove.pieceMoved
                if piece[1] == "K":
                    self.castling[piece[0] + "Ks"] = True
                    self.castling[piece[0] + "Qs"] = True

            # undo the move
            self.board[previousMove.startRow][
                previousMove.startCol
            ] = previousMove.pieceMoved

            self.board[previousMove.endRow][
                previousMove.endCol
            ] = previousMove.pieceCaptured

            self.WhiteToMove = not self.WhiteToMove

            # update the king's position during an undo
            if previousMove.pieceMoved == "wK":
                self.whiteKingLocation = (previousMove.startRow, previousMove.startCol)

            elif previousMove.pieceMoved == "bK":
                self.blackKingLocation = (previousMove.startRow, previousMove.startCol)

            # undo pawn promotion
            if previousMove.isPawnPromotion:
                self.board[previousMove.endRow][
                    previousMove.endCol
                ] = previousMove.pieceCaptured

            # undo en passant
            if previousMove.enPassant:

                piece = previousMove.pieceMoved
                if piece[0] == "w":
                    c = "b"
                elif piece[0] == "b":
                    c = "w"

                self.board[previousMove.startRow][previousMove.endCol] = c + "P"

            # undo castling move
            if previousMove.castle:
                # queen side
                if previousMove.castleSide == "Qs":
                    self.board[previousMove.startRow][0] = (
                        previousMove.pieceMoved[0] + "R"
                    )
                    self.board[previousMove.endRow][previousMove.endCol + 1] = "--"
                    self.castling[previousMove.pieceMoved[0] + "Qs"] = True

                # king side
                elif previousMove.castleSide == "Ks":
                    self.board[previousMove.startRow][7] = (
                        previousMove.pieceMoved[0] + "R"
                    )
                    self.board[previousMove.endRow][previousMove.endCol - 1] = "--"
                    self.castling[previousMove.pieceMoved[0] + "Ks"] = True

            if len(self.pgnMoveLog) != 0:
                if len(self.pgnMoveLog[-1]) == 1:
                    self.pgnMoveLog.remove(self.pgnMoveLog[-1])
                elif len(self.pgnMoveLog[-1]) == 2:
                    self.pgnMoveLog[-1] = [self.pgnMoveLog[-1][0]]

    def isCastlingPossible(self):

        "For a state of the board, check if castling is possible"

        if self.WhiteToMove:
            allyColor = "w"
            row = self.whiteKingLocation[0]
            col = self.whiteKingLocation[1]

        else:
            allyColor = "b"
            row = self.blackKingLocation[0]
            col = self.blackKingLocation[1]

        castlingSides = [((1, 4), "Qs"), ((5, 7), "Ks")]

        truestates = []

        for side in castlingSides:

            flag = False
            # if king and rooks have not been moved before
            if self.castling[allyColor + side[1]]:

                for i in range(side[0][0], side[0][1]):

                    # check if any pieces between king and rook are blocking
                    if self.board[row][i] != "--":
                        truestates.append(False)
                        flag = True
                        break

                    # check if any square between king and rook is under attacked
                    self.WhiteToMove = not self.WhiteToMove
                    moves = self.getAllPossibleMoves()
                    self.WhiteToMove = not self.WhiteToMove

                    for move in moves:
                        if (move.endCol == i) and (move.endRow == row):
                            truestates.append(False)
                            flag = True
                            break

                    if flag:
                        break

                    flag = False

                if not flag:
                    truestates.append(True)

        return truestates

    def isEnPassantPossible(self, row, col):

        """
        For a state of the board, check if en passant is possible
        """

        if self.WhiteToMove:
            rank = 3
            enemyColor = "b"
        else:
            rank = 4
            enemyColor = "w"

        # if pawn is on 3rd or 4th rank, check the previous move
        if row == rank:
            if len(self.moveLog) != 0:
                previousMove = self.moveLog[-1]
                # conditions:
                # 1. previous move was an enemy pawn
                # 2. enemy pawn is mved to the same rank as own pawn
                # 3. enemy pawn is next to our pawn
                # en passant is possible
                if (
                    previousMove.pieceMoved == (enemyColor + "P")
                    and previousMove.endRow == rank
                    and (
                        previousMove.endCol == (col - 1)
                        or previousMove.endCol == (col + 1)
                    )
                ):
                    # print("enpassant")
                    return True

        return False

    def getValidMoves(self):

        """
        Get all possible moves considering checks
        """

        moves = []
        self.inCheck, self.pins, self.checks = self.pinsAndChecks()

        if self.WhiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]

        if self.inCheck:
            # if only 1 check, block the check or move the king

            if len(self.checks) == 1:

                check = self.checks[0]
                moves = self.getAllPossibleMoves()

                checkRow = check[0]
                checkCol = check[1]

                checker = self.board[checkRow][checkCol]

                validSquares = []
                # if knight, capture knight or move king
                if checker[1] == "N":
                    validSquares = [(check[0], check[1])]
                else:

                    for i in range(1, 8):

                        checkDirection = check[2]
                        validSquare = (
                            kingRow + checkDirection[0] * i,
                            kingCol + checkDirection[1] * i,
                        )
                        validSquares.append(validSquare)

                        # if valid square has the piece that is checking the king, break
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break

                # remove all the moves that do not block or move king
                for i in range(len(moves) - 1, -1, -1):
                    # if doesnt move king or capture
                    if moves[i].pieceMoved[1] != "K":
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])

            # double check, must move the king
            else:
                self.getKingMoves(kingRow, kingCol, moves)

        # no checks, all moves are valid
        else:
            moves = self.getAllPossibleMoves()

        if len(moves) == 0:

            if self.inCheck:
                self.checkmate = True
            else:
                self.stalemate = True

        self.getCastlingMoves(moves)

        return moves

    def getAllPossibleMoves(self):

        """
        Get all possible moves without considering checks
        """

        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):

                turn = self.board[row][col][0]  # see who's turn is it
                if (turn == "w" and self.WhiteToMove) or (
                    turn == "b" and not self.WhiteToMove
                ):

                    piece = self.board[row][col][1]  # get the piece
                    self.getPieceMovesFunction[piece](row, col, moves)

        return moves

    def pinsAndChecks(self):

        """
        Check for pins and checks
        """

        inCheck = False
        pins = []
        checks = []

        if self.WhiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
            enemyColor = "b"
            allyColor = "w"

        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
            enemyColor = "w"
            allyColor = "b"

        # first 4 : moving left, up, down, right
        # last 4 : moving in diagonal direction
        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]

        for x in range(len(directions)):

            d = directions[x]
            possiblePin = ()

            for i in range(1, 8):

                endRow = kingRow + (i * d[0])
                endCol = kingCol + (i * d[1])

                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]

                    # is ally piece, thus it might be a pin
                    if endPiece[0] == allyColor:
                        # first piece, might be a possible pin
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, d)

                        # second ally piece, ignore it
                        else:
                            break

                    elif endPiece[0] == enemyColor:
                        pieceType = endPiece[1]

                        # 5 possibilities of piece check / piece pin
                        # 1. orthogonally from king and piece is rook
                        # 2. diagonally from king and piece is bishop
                        # 3. moving from all direction and piece is queen
                        # 4. 1 square away in diagonal direction and piece is pawn
                        # 5. more than 1 square away and piece is a king
                        if (
                            (pieceType == "R" and 0 <= x <= 3)
                            or (pieceType == "B" and 4 <= x <= 7)
                            or (pieceType == "Q")
                            or (
                                pieceType == "P"
                                and i == 1
                                and (
                                    (enemyColor == "b" and 4 <= x <= 5)
                                    or (enemyColor == "w" and 6 <= x <= 7)
                                )
                            )
                            or (pieceType == "K" and i == 1)
                        ):
                            # no piece is blocking, so check
                            if possiblePin == ():
                                inCheck = True
                                checks.append((endRow, endCol, d))
                                break

                            else:
                                pins.append((possiblePin[0], possiblePin[1], d))
                                # print(pins)
                                break

                        # enemy piece not checking the king
                        else:
                            break

        Ndirections = [
            (-2, -1),
            (-1, -2),
            (-1, 2),
            (-2, 1),
            (2, 1),
            (1, 2),
            (1, -2),
            (2, -1),
        ]

        # knight checks
        for d in Ndirections:
            endRow = kingRow + (1 * d[0])
            endCol = kingCol + (1 * d[1])

            if 0 <= endRow < 8 and 0 <= endCol < 8:
                # if is an enemy knight
                if self.board[endRow][endCol] == (enemyColor + "N"):
                    checks.append((endRow, endCol, (-d[0], -d[1])))
                    inCheck = True

        return inCheck, pins, checks

    def isInCheck(self):

        """
        Determine if a current player is in check
        """
        if self.WhiteToMove:
            return self.squareUnderAttack(
                self.whiteKingLocation[0], self.whiteKingLocation[1]
            )
        else:
            return self.squareUnderAttack(
                self.blackKingLocation[0], self.blackKingLocation[1]
            )

    def squareUnderAttack(self, row, col):

        """
        Determine if enemy can attack the square row col
        """

        self.WhiteToMove = not self.WhiteToMove  # switch to opponent's point of view
        opponents_moves = self.getAllPossibleMoves()
        self.WhiteToMove = not self.WhiteToMove

        for move in opponents_moves:
            if move.endRow == row and move.endCol == col:  # square is under attack
                return True

        return False

    def getPawnMoves(self, row, col, moves):

        """
        Get all possible moves for the pawn located at row, col
        """

        piecePinned = False
        pinDirection = []

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2][0], self.pins[i][2][1])
                self.pins.remove(self.pins[i])
                break

        # white pawn move
        if self.WhiteToMove:
            d = -1
            enemyColor = "b"
            rank = 6
        # black pawn move
        else:
            d = 1
            enemyColor = "w"
            rank = 1

        # check the square infront of the pawn
        if self.board[row + (1 * d)][col] == "--":
            if not piecePinned or pinDirection == (d, 0):
                moves.append(Move((row, col), (row + (1 * d), col), self.board))

                # if the pawn is on the 7th / 1st rank, it can move 2 squares forward given that the square is empty
                if 0 <= row + (2 * d) <= 7 and 0 <= col <= 7:
                    if self.board[row + (2 * d)][col] == "--" and row == rank:
                        moves.append(Move((row, col), (row + (2 * d), col), self.board))

        # capture piece on the left
        if col - 1 >= 0 and self.board[row + (1 * d)][col - 1][0] == enemyColor:
            if not piecePinned or pinDirection == (d, -1):
                moves.append(Move((row, col), (row + (1 * d), col - 1), self.board))

        # capture piece on the right
        if col + 1 <= 7 and self.board[row + (1 * d)][col + 1][0] == enemyColor:
            if not piecePinned or pinDirection == (d, 1):
                moves.append(Move((row, col), (row + (1 * d), col + 1), self.board))

        # check if en passant is possible or not
        if self.isEnPassantPossible(row, col):

            if not piecePinned:

                previousMove = self.moveLog[-1]
                epCapDir = previousMove.endCol

                eP = Move((row, col), (row + (1 * d), epCapDir), self.board)
                eP.enPassant = True
                moves.append(eP)

    def getRookMoves(self, row, col, moves):

        """
        Get all possible moves for the rook located at row, col
        """

        # which color can be captured
        captureColor = self.enemyColor(row, col)

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2][0], self.pins[i][2][1])
                if (
                    self.board[row][col][1] != "Q"
                ):  # can't remove queen from pin on rook moves, only remove it on bishop moves
                    self.pins.remove(self.pins[i])
                break

        for d in directions:

            for i in range(1, 8):
                endRow = row + (i * d[0])
                endCol = col + (i * d[1])

                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if (
                        not piecePinned
                        or pinDirection == d
                        or pinDirection == (-d[0], -d[1])
                    ):
                        if self.board[endRow][endCol] == "--":
                            moves.append(Move((row, col), (endRow, endCol), self.board))

                        elif self.board[endRow][endCol][0] == captureColor:
                            moves.append(Move((row, col), (endRow, endCol), self.board))
                            break

                        else:
                            break

                else:
                    break

    def getKnightMoves(self, row, col, moves):

        """
        Get all possible moves for the knight located at row, col
        """

        piecePinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break

        # which color can be captured
        captureColor = self.enemyColor(row, col)

        # grid to check whether the knight can move there or not
        knightGrid = [
            [0, 1, 0, 1, 0],
            [1, 0, 0, 0, 1],
            [0, 0, 0, 0, 0],
            [1, 0, 0, 0, 1],
            [0, 1, 0, 1, 0],
        ]

        for rIndex in range(row - 2, row + 3, 1):
            if rIndex >= 0 and rIndex < 8:
                for cIndex in range(col - 2, col + 3, 1):

                    if cIndex >= 0 and cIndex < 8:
                        # integers used for subtracting the index so that the product can be used for knightGrid
                        rBase = rIndex - (row - 2)
                        cBase = cIndex - (col - 2)

                        # check to see whether knight can move to that square
                        if knightGrid[rBase][cBase] == 1:
                            if not piecePinned:
                                if (
                                    self.board[rIndex][cIndex] == "--"
                                    or self.board[rIndex][cIndex][0] == captureColor
                                ):
                                    moves.append(
                                        Move(
                                            (row, col),
                                            (rIndex, cIndex),
                                            self.board,
                                        )
                                    )
                                else:
                                    pass

    def getBishopMoves(self, row, col, moves):

        """
        Get all possible moves for the bishop located at row, col
        """

        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2][0], self.pins[i][2][1])
                self.pins.remove(self.pins[i])
                break

        # which color can be captured
        captureColor = self.enemyColor(row, col)

        directions = [(-1, -1), (-1, 1), (1, 1), (1, -1)]

        for d in directions:

            for i in range(1, 8):
                endRow = row + (i * d[0])
                endCol = col + (i * d[1])

                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if (
                        not piecePinned
                        or pinDirection == d
                        or pinDirection == (-d[0], -d[1])
                    ):
                        if self.board[endRow][endCol] == "--":
                            moves.append(Move((row, col), (endRow, endCol), self.board))

                        elif self.board[endRow][endCol][0] == captureColor:
                            moves.append(Move((row, col), (endRow, endCol), self.board))
                            break

                        else:
                            break

                else:
                    break

    def getQueenMoves(self, row, col, moves):

        """
        Get all possible moves for queen located at row, col
        """
        self.getBishopMoves(row, col, moves)
        self.getRookMoves(row, col, moves)

    def getKingMoves(self, row, col, moves):

        """
        Get all possible moves for king located at row, col
        """

        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = "w" if self.WhiteToMove else "b"

        for i in range(8):

            endRow = row + rowMoves[i]
            endCol = col + colMoves[i]

            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # not an ally piece - empty or enemy

                    # place king on end square and check for checks
                    if allyColor == "w":
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)

                    inCheck, pins, checks = self.pinsAndChecks()
                    # for i in checks:
                    #     print(i)

                    if not inCheck:
                        moves.append(Move((row, col), (endRow, endCol), self.board))

                    # place king back on original location
                    if allyColor == "w":
                        self.whiteKingLocation = (row, col)
                    else:
                        self.blackKingLocation = (row, col)

    def getCastlingMoves(self, moves):

        """
        If castling is possible, move it a valid move
        """

        kingSq = self.whiteKingLocation if self.WhiteToMove else self.blackKingLocation
        row = kingSq[0]
        col = kingSq[1]

        allyColor = "w" if self.WhiteToMove else "b"

        inCheck, pins, checks = self.pinsAndChecks()
        if not inCheck:
            # if king is on 5th col and rooks
            if col == 4 and (
                self.board[row][0] == (allyColor + "R")
                or self.board[row][7] == (allyColor + "R")
            ):

                trueStates = self.isCastlingPossible()
                for i in range(0, len(trueStates)):
                    # if queen side
                    if i == 0:
                        side = "Qs"
                        endCol = 2
                    # if king side
                    elif i == 1:
                        side = "Ks"
                        endCol = 6

                    # castling is possible
                    if trueStates[i]:
                        castleMove = Move((row, col), (row, endCol), self.board)
                        castleMove.castle = True
                        castleMove.castleSide = side
                        moves.append(castleMove)

    def enemyColor(self, row, col):

        """
        Return the enemy piece color
        """

        if self.board[row][col][0] == "w":
            captureColor = "b"
        else:
            captureColor = "w"

        return captureColor

    def pgnAppend(self):

        """
        Append PGN line
        """

        move = self.moveLog[-1]
        piece = move.pieceMoved
        pieceCaptured = move.pieceCaptured
        startSq = (move.startRow, move.startCol)
        endSq = (move.endRow, move.endCol)

        pgnStartSq = (move.colsToFiles[startSq[1]], move.rowsToRanks[startSq[0]])
        pgnEndSq = (move.colsToFiles[endSq[1]], move.rowsToRanks[endSq[0]])

        if len(self.pgnMoveLog) != 0:

            if len(self.pgnMoveLog[-1]) == 1:
                moveLine = self.pgnMoveLog.pop()
            else:
                moveLine = []
        else:
            moveLine = []

        # king
        if piece[1] == "K":

            if (
                (startSq == ((0, 4)) and endSq == ((0, 2)))
                or (startSq == ((0, 4)) and endSq == ((0, 6)))
                or (startSq == ((7, 4)) and endSq == ((7, 2)))
                or (startSq == ((7, 4)) and endSq == ((7, 6)))
            ):
                # castling, queen side is O-O-O; king side is O-O
                if endSq[1] == 2:
                    string = "O-O-O"

                elif endSq[1] == 6:
                    string = "O-O"

            else:
                if pieceCaptured != "--":
                    string = "K" + f"{pgnEndSq[0]}{pgnEndSq[1]}"
                else:
                    string = "Kx" + f"{pgnEndSq[0]}{pgnEndSq[1]}"
        # pawn
        elif piece[1] == "P":

            # if pawn captured a piece or en passant,
            # move will be startRow x endSq
            if pieceCaptured != "--" or (
                (
                    (piece[0] == "w" and endSq[0] == 3)
                    or (piece[0] == "b" and endSq[0] == 4)
                )
                and ((endSq[1] == startSq[1] - 1) or (endSq[1] == startSq[1] + 1))
            ):
                string = f"{pgnStartSq[0]}x{pgnEndSq[0]}{pgnEndSq[1]}"

            # if pawn just moved normally, move will be endSq
            else:
                string = f"{pgnEndSq[0]}{pgnEndSq[1]}"

            # if pawn promotion, add "=piece promoted to" to the string
            if (piece[0] == "w" and endSq[0] == 0) or (
                piece[0] == "b" and endSq[0] == 7
            ):
                promotedPiece = self.board[endSq[0]][endSq[1]]
                string = string + f"={promotedPiece[1]}"

        # if any other piece moved
        else:

            # cases where there are 2 major pieces in the same col or same row
            # specify which row / col the piece moved start from
            m = Move
            rowFlag = False
            colFlag = False

            for i in range(0, 7):
                rowSqChecked = (i, startSq[1])
                colSqChecked = (startSq[0], i)

                if rowSqChecked != startSq:
                    if self.board[rowSqChecked[0]][rowSqChecked[1]] == piece:

                        rowFlag = True

                if colSqChecked != startSq:
                    if self.board[colSqChecked[0]][colSqChecked[1]] == piece:

                        colFlag = True

            tempString = f"{piece[1]}"
            if piece[1] != "N":
                if rowFlag:
                    tempString = f"{piece[1]}{pgnStartSq[1]}"

                elif colFlag:
                    tempString = f"{piece[1]}{pgnStartSq[0]}"

            if pieceCaptured != "--":
                string = tempString + f"x{pgnEndSq[0]}{pgnEndSq[1]}"

            else:
                string = tempString + f"{pgnEndSq[0]}{pgnEndSq[1]}"

        moveLine.append(string)
        self.pgnMoveLog.append(moveLine)

    def getPGN(self):

        """
        Get the portable game notation of the current game state
        """

        pgn = ""
        for no, line in enumerate(self.pgnMoveLog):

            if len(line) == 2:
                moveString = line[0] + " " + line[1]

            elif len(line) == 1:
                moveString = line[0]

            pgnString = str(no + 1) + ". " + moveString

            if len(line) == 2:
                pgnString += " "

            pgn += pgnString

        print(pgn)

    def convertToFEN(self):
        """
        Convert the current board state to FEN notation
        """

        fenString = ""
        board = self.board

        # piece placement
        for enu1, i in enumerate(board):
            count = 0
            for enu2, piece in enumerate(i):

                if piece != "--":

                    if count != 0:
                        fenString += f"{count}"

                    if piece[0] == "w":
                        pass

                    elif piece[0] == "b":
                        piece = piece.lower()

                    pieceType = piece[1]
                    fenString += f"{pieceType}"
                    count = 0

                else:
                    count += 1

                if enu2 == 7 and count != 0:
                    fenString += f"{count}"

            if enu1 != 7:
                fenString += "/"

        fenString += " "

        # who to move
        if self.WhiteToMove:
            fenString += "w"
        else:
            fenString += "b"

        fenString += " "

        # castling rights
        track = 0
        val = None
        for i in self.castling:

            if self.castling[i]:
                if i[0] == "w":
                    val = i
                elif i[0] == "b":
                    val = i.lower()

                fenString += val[1]

            else:
                track += 1

            if track == 4:
                fenString += "-"

        fenString += " "

        if len(self.moveLog) != 0:
            previousMove = self.moveLog[-1]

            # possible en passant target
            if previousMove.pieceMoved[1] == "P":

                if (
                    previousMove.pieceMoved[0] == "w"
                    and (previousMove.startRow == 6 and previousMove.endRow == 4)
                ) or (
                    previousMove.pieceMoved[0] == "b"
                    and (previousMove.startRow == 1 and previousMove.endRow == 3)
                ):
                    if previousMove.pieceMoved[0] == "w":
                        d = 1

                    else:
                        d = -1

                    enPassantString = (
                        previousMove.colsToFiles[previousMove.endCol]
                        + previousMove.rowsToRanks[previousMove.endRow + d]
                    )

                else:
                    enPassantString = "-"

                fenString += enPassantString

            else:
                fenString += "-"

        else:
            fenString += "-"

        fenString += " "

        track50 = 0
        for i in self.moveLog:
            if i.pieceMoved[1] == "P" or i.pieceMoved[1] == "K":
                track50 += 1

            else:
                track50 = 0

        fenString += str(track50 - 1)
        fenString += " "

        # full move
        length = len(self.moveLog)
        if length != 0:
            fenString += f"{int(length/2) + 1}"

        print(fenString)

    def loadFENposition(self, fen):

        """
        Load the given FEN position

        Example FEN:
            rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1

        """
        numbers = ["1", "2", "3", "4", "5", "6", "7", "8"]
        tempBoard = []

        fen = fen.split(" ")

        # piece placement data
        ppData = fen[0].split("/")

        for i in ppData:
            line = []
            for j in i:

                if j in numbers:
                    for k in range(int(j)):
                        line.append("--")

                else:
                    if j.islower():
                        color = "b"
                    else:
                        color = "w"

                    line.append(color + j.upper())

            tempBoard.append(line)

        for row in range(len(tempBoard)):
            for col in range(len(tempBoard[row])):

                piece = tempBoard[row][col]
                if piece == "wK":
                    self.whiteKingLocation = (row, col)

                elif piece == "bK":
                    self.blackKingLocation = (row, col)

        self.board = np.array(tempBoard)
        if fen[1] == "w":
            self.WhiteToMove = True
        else:
            self.WhiteToMove = False

        if fen[2] != "--":
            for letter in fen[2]:
                if letter.islower():
                    color = "b"

                else:
                    color = "w"

                if letter == "K":
                    side = "Ks"

                else:
                    side = "Qs"

                castleSide = color + side
                self.castling[castleSide] = True

        self.fiftyMoveCount = int(fen[4])

        # add the en passant pawn move to the movelog, then call is en passant possible
        enpassantMove = fen[3]
        if enpassantMove != "-":
            tempMove = Move

            enPSQ = (
                tempMove.ranksToRows[enpassantMove[1]],
                tempMove.filesToCols[enpassantMove[0]],
            )

            if fen[1] == "w":
                startSq = (enPSQ[0] - 1, enPSQ[1])
                endSq = (enPSQ[0] + 1, enPSQ[1])
                c = "b"

            elif fen[1] == "b":
                startSq = (enPSQ[0] + 1, enPSQ[1])
                endSq = (enPSQ[0] - 1, enPSQ[1])
                c = "w"

            epMove = Move(startSq, endSq, self.board)
            epMove.pieceMoved = c + "P"

            self.moveLog.append(epMove)

    def loadPGNposition(self, pgn):

        """
        Load PGN into the board
        """

        # get all the valid moves
        validMoves = self.getValidMoves()
        # flag variable
        flag = True

        # parsing
        tempMove = Move
        pgn = pgn.split("\n")

        moveLine = None
        if len(pgn) == 1:
            moveLine = pgn[0]
        else:
            moveLine = pgn[7]

        moveLine = moveLine.split(" ")
        for i in reversed(moveLine):
            if "." in i:
                moveLine.remove(i)

        if moveLine[-1] in ["1-0", "1/2-1/2", "0-1"]:
            moveLine.remove(moveLine[-1])

        pieceTypes = ["K", "Q", "N", "B", "R"]
        # make the moves
        for i in moveLine:

            i = i.replace("+", "")
            flag = True

            if self.WhiteToMove:
                d = 1
            else:
                d = -1

            # is a pawn move
            if len(i) == 2 or (not "x" in i and "=" in i):

                endSq = (tempMove.ranksToRows[i[1]], tempMove.filesToCols[i[0]])

                startSq = (endSq[0] + d, endSq[1])
                # move from 2nd and 7th rank, 2 squares at once
                if self.board[endSq[0] + d][endSq[1]] == "--":
                    startSq = (endSq[0] + (2 * d), endSq[1])

                move = Move(startSq, endSq, self.board)

                # promotion
                if "=" in i:
                    move.promotionPiece = self.pawnPromotionDictRev[i[-1].upper()]

            elif "x" in i:

                if len(i) == 4 or "=" in i:
                    # capture piece using pawn
                    if i[0] in list(Move.filesToCols.keys()) and i[1] == "x":
                        endSq = (tempMove.ranksToRows[i[3]], tempMove.filesToCols[i[2]])
                        startSq = (endSq[0] + d, tempMove.filesToCols[i[0]])
                        for j in validMoves:

                            if (
                                (j.endRow, j.endCol) == endSq
                                and (j.startRow, j.startCol) == startSq
                                and (j.pieceCaptured != "--")
                            ):
                                # promotion
                                if "=" in i:
                                    j.promotionPiece = self.pawnPromotionDictRev[
                                        i[-1].upper()
                                    ]

                                self.makeMove(j)

                    else:
                        flag = False
                        endSq = (tempMove.ranksToRows[i[3]], tempMove.filesToCols[i[2]])
                        for j in validMoves:

                            if (
                                (j.endRow, j.endCol) == endSq
                                and (j.pieceMoved[1] == i[0])
                                and (j.pieceCaptured != "--")
                            ):
                                self.makeMove(j)

                # if there exists a case where 2 same pieces are attacking each other
                elif len(i) == 5:

                    flag = False
                    clashFlag = None
                    if i[1] in Move.ranksToRows.keys():
                        start = Move.ranksToRows[i[1]]
                        clashFlag = True

                    elif i[1] in Move.filesToCols.keys():
                        start = Move.filesToCols[i[1]]
                        clashFlag = False

                    endSq = (tempMove.ranksToRows[i[4]], tempMove.filesToCols[i[3]])
                    for j in validMoves:

                        if (
                            (j.endRow, j.endCol) == endSq
                            and (j.pieceMoved[1] == i[0])
                            and (j.pieceCaptured != "--")
                        ):
                            # use the i[1] to differentiate captures using the same piece but
                            # different start squares
                            if clashFlag is True:
                                if j.startRow == start:
                                    self.makeMove(j)
                            elif clashFlag is False:
                                if j.startCol == start:
                                    self.makeMove(j)

            # major piece is being moved
            elif not "x" in i and (i[0] in pieceTypes):
                if not "O" in i:

                    if len(i) == 3:
                        endSq = (tempMove.ranksToRows[i[2]], tempMove.filesToCols[i[1]])
                        for j in validMoves:
                            if (j.endRow, j.endCol) == endSq and (
                                j.pieceMoved[1] == i[0]
                            ):
                                self.makeMove(j)
                                flag = False

                    # cases where the move is clashing with another similar move
                    elif len(i) == 4:

                        endSq = (tempMove.ranksToRows[i[3]], tempMove.filesToCols[i[2]])
                        clashFlag = None

                        if i[1] in Move.ranksToRows.keys():
                            start = Move.ranksToRows[i[1]]
                            clashFlag = True

                        elif i[1] in Move.filesToCols.keys():
                            start = Move.filesToCols[i[1]]
                            clashFlag = False

                        for j in validMoves:

                            if (j.endRow, j.endCol) == endSq and (
                                j.pieceMoved[1] == i[0]
                            ):

                                # use i[1] to different moves that are from the same row/ col and goes to the same square
                                if clashFlag is True:
                                    if j.startRow == start:
                                        self.makeMove(j)

                                elif clashFlag is False:
                                    if j.startCol == start:
                                        self.makeMove(j)

                # castling move
                else:
                    if len(i) == 3:  # O-O
                        castleside = "Ks"
                    elif len(i) == 5:  # O-O-O
                        castleside = "Qs"

                    for j in validMoves:
                        if j.castle == True and j.castleSide == castleside:
                            self.makeMove(j)

            if flag:
                if move in validMoves:
                    self.makeMove(move)

            validMoves = self.getValidMoves()


class Move:

    # dictionary for converting ranks to rows , rows to ranks
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    # dictionary for converting files to cols , cols to files
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):

        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]  # the piece being moved
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveId = (
            self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        )

        # Promotions
        self.isPawnPromotion = False

        # if piece moved is pawn and it has reached the opposite side of the board
        if (self.pieceMoved == "wP" and self.endRow == 0) or (
            self.pieceMoved == "bP" and self.endRow == 7
        ):
            self.isPawnPromotion = True

        self.promotionPiece = None

        self.enPassant = False

        # castling
        self.castle = False
        self.castleSide = None

    def __eq__(self, other):
        """
        Overriding equal method
        """

        if isinstance(other, Move):
            return self.moveId == other.moveId

        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(
            self.endRow, self.endCol
        )

    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]
