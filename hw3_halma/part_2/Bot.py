import time
from copy import deepcopy
from scoreHelper import calculate_score
from standardConstants import *
import random 

class Bot():
    
    def __init__(self, *, ABpruning=False, search_depth=3, mode=BOT_MODE) -> None:
        
        # initialize variables
        self.search_depth = search_depth
        self.ABpruning    = ABpruning
        self.mode = mode
        self.player = None

    def assign_player( self, player ):
        self.player = player

    def minimax_search(self, *, board, player, opponent):

        # initialize variables
        best_score = float("-inf")
        best_piece = None
        best_move = None

        # get all valid moves for self
        validMoves = self.get_moves_dict(board=board, player=self)

        # loop through each piece and its moveset
        for piece, moveSet in validMoves.items():

            for move in moveSet:
                # simulate move
                new_board = self.simulate_move(board=board, piece=piece, move=move)

                # evaluate score with minimax
                score = self.minimax(
                    board=new_board,
                    depth=self.search_depth, 
                    max_player=True,
                    player=player,
                    opponent=opponent,
                    rootPlayer=player,
                    rootOpponent=opponent
                )

                if score == 10:
                    print( new_board)
                    print(f"WE WIN! {piece.canvasPiece} -> {best_move}")
                    time.sleep( 10000 )
                    best_score = score
                    best_piece = piece
                    best_move = move
                    quit()
                    return best_piece, best_move

                # check if better than current best
                if score > best_score:
                    best_score = score
                    best_piece = piece
                    best_move = move

        print( best_piece.canvasPiece, best_move)
        return best_piece, best_move
    
    def minimax(self, board, depth, max_player, player, opponent, rootPlayer, rootOpponent):
        # base case: depth 0 or win
        if depth == 0 or self.check_win(board=board, player=player, opponent=opponent):
            return calculate_score(board=board, player=rootPlayer, opponent=rootOpponent)

        # get all valid moves
        validMoves = self.get_moves_dict(board=board, player=player)

        if not validMoves:  # no moves left
            return calculate_score(board=board, player=rootPlayer, opponent=rootOpponent)

        # MAX player's turn
        if max_player:
            best_score = float("-inf")
            for piece, moveSet in validMoves.items():
                for move in moveSet:
                    new_board = self.simulate_move(board=board, piece=piece, move=move)
                    score = self.minimax(
                        board=new_board,
                        depth=depth - 1,
                        max_player=False,
                        player=opponent,
                        opponent=player,
                        rootPlayer=rootPlayer,
                        rootOpponent=rootOpponent
                    )
                    best_score = max(best_score, score)
            return best_score
        
        # MIN player's turn
        else:
            best_score = float("inf")
            for piece, moveSet in validMoves.items():
                for move in moveSet:
                    new_board = self.simulate_move(board=board, piece=piece, move=move)
                    score = self.minimax(
                        board=new_board,
                        depth=depth - 1,
                        max_player=True,
                        player=opponent,
                        opponent=player,
                        rootPlayer=rootPlayer,
                        rootOpponent=rootOpponent
                    )
                    best_score = min(best_score, score)
            return best_score


    def simulate_move(self, *, board, piece, move):

        # initialize variables
        (newRow, newCol) = move

        # Deep copy the board
        new_board = deepcopy(board)

        # get current row/col
        row, col = piece.get_coords( board=new_board )

        # erase current row/col
        new_board[row][col]=None

        # assign new row/col
        new_board[newRow][newCol] = piece 

        # return new board 
        return new_board