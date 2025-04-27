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

    def minimax_search(self, *, board, opponent, max_player):
        best_score = float("-inf")
        best_piece = None
        best_move = None

        # get all valid moves for self
        validMoves = self.get_moves_dict(board=board, player=self)

        # loop thru piece and its movesets
        for piece, moveSet in validMoves.items():

            # loop through the moves in the moveset
            for move in moveSet:

                # create a new board with the move
                new_board = self.simulate_move(board=board, piece=piece, move=move)

                # if piece.canvasPiece == 107:
                #     print( new_board )
                #     print(f"If {self.name} moved {piece.canvasPiece} to {move}, {self.name} would have {score} points")

                # calculate score for that 
                score = calculate_score( board=new_board, player=self, opponent=opponent)

                # check if this score is better than old scores
                if score > best_score:

                    # reassign
                    best_score = score
                    best_piece = piece
                    best_move = move

        # return the best move and piece
        return best_piece, best_move


    def minimax(self, board, depth, max_player, player, opponent):

        # depth limit or we can win
        if depth == 0 or self.check_win(board=board, player=player, opponent=opponent):
            return calculate_score(board=board, player=player, opponent=opponent)

        # get the valid moves with this board
        validMoves = self.get_moves_dict( board=board, player=player)

        # No moves left, calculate score
        if not validMoves: 
            return calculate_score(board=board, player=player, opponent=opponent)
        
        # Check if we are max player or not
        if max_player:

            # worst move
            max_eval = float("-inf")

            # loop through the moves + moveset
            for piece, moveSet in validMoves.items():

                # loop through the moveset
                for move in moveSet:

                    # gen new board
                    new_board = self.simulate_move(board=board, piece=piece, move=move)

                    # evaluate down this moveset
                    eval = self.minimax(board=new_board, 
                                        depth=depth - 1, 
                                        max_player=max_player, 
                                        opponent=opponent, 
                                        player=player)
                
                    # reassign max eval 
                    max_eval = max(max_eval, eval)

            # return the max eval
            return max_eval
        
        # is minimum player
        else:

            # best move
            min_eval = float("inf")

            # loop through the moves + moveset
            for piece, moveSet in validMoves.items():

                # loop through the moveset
                for move in moveSet:

                    # gen new board
                    new_board = self.simulate_move(board=board, piece=piece, move=move)

                    # evalue down this moveset
                    eval = self.minimax(board=new_board, 
                                        depth=depth - 1, 
                                        max_player=max_player, 
                                        opponent=opponent, 
                                        player=player)

                    # reassign min eval 
                    min_eval = min(min_eval, eval)
            
            # return min value
            return min_eval

    def simulate_move(self, *, board, piece, move):

        # Deep copy the board
        new_board = deepcopy(board)

        # get current row/col
        row, col = piece.get_coords( board=new_board )

        # get new row/col 
        (newRow, newCol) = move

        # erase current row/col
        new_board[row][col]=None

        # assign new row/col
        new_board[newRow][newCol] = piece 



        # return new board 
        return new_board