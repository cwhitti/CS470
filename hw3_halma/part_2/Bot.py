import time
from copy import deepcopy
from scoreHelper import calculate_score, visualize_board
from standardConstants import *
import random 

class Bot():
    
    def __init__(self, *, ABpruning=False, search_depth=2, mode=BOT_MODE) -> None:
        
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
        found_win = False

        # get all valid moves for self
        validMoves = self.get_moves_dict(board=board, player=self)

        # loop through each piece and its moveset
        for piece, moveSet in validMoves.items():

            # loop through all moves
            for move in moveSet:
                
                # print(f"Following down the {piece.canvasPiece} -> {move} path")

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
                
                if self.check_win(board=new_board, player=player, opponent=opponent, displayBoard=False):

                    best_score = score
                    best_piece = piece
                    best_move = move
                    found_win = True
                    break
                
                else:
                    if score > best_score:
                        best_score = score
                        best_piece = piece
                        best_move = move
                
            if found_win:
                break

        print( best_piece.canvasPiece, best_move, best_score)
        return best_piece, best_move
    
    def minimax(self, board, depth, max_player, player, opponent, rootPlayer, rootOpponent):

        if depth == 0 or self.check_win(board=board, player=rootPlayer, opponent=rootOpponent, displayBoard=False):
            return calculate_score(board=board, player=rootPlayer, opponent=rootOpponent)

        validMoves = self.get_moves_dict(board=board, player=player)

        if not validMoves:
            return calculate_score(board=board, player=rootPlayer, opponent=rootOpponent)

        if max_player:
            best_score = float("-inf")
            for piece, moveSet in validMoves.items():
                for move in moveSet:
                    new_board = self.simulate_move(board=board, piece=piece, move=move)
                    # **Notice the player is opponent now**
                    score = self.minimax(
                        board=new_board,
                        depth=depth - 1,
                        max_player=False,  # min next
                        player=opponent,  # <-- now opponent moves
                        opponent=player,  # <-- player becomes opponent
                        rootPlayer=rootPlayer,
                        rootOpponent=rootOpponent
                    )
                    best_score = max(best_score, score)
            return best_score

        else:
            best_score = float("inf")
            for piece, moveSet in validMoves.items():
                for move in moveSet:
                    new_board = self.simulate_move(board=board, piece=piece, move=move)
                    # **Swap again**
                    score = self.minimax(
                        board=new_board,
                        depth=depth - 1,
                        max_player=True,  # max next
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
        new_board = self.copy_board(board)

        # get current row/col
        row, col = piece.get_coords( board=new_board )

        # erase current row/col
        new_board[row][col]=None

        # assign new row/col
        new_board[newRow][newCol] = piece 

        # return new board 
        return new_board
    
    def copy_board( self, board ):

        newBoard = []

        for row in range( len( board ) ):

            newRow = []

            for col in range( len( board ) ):

                piece = board[row][col]

                newRow.append( piece )
            
            newBoard.append( newRow )
         
        return newBoard