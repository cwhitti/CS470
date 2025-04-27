import time
from copy import deepcopy
from scoreHelper import calculate_score, visualize_board
from standardConstants import *
import random 

class Bot():
    
    def __init__(self, *, ABpruning=False, search_depth=3, mode=BOT_MODE) -> None:
        
        # initialize variables
        self.search_depth = search_depth
        self.ABpruning    = ABpruning
        self.mode = mode
        self.time_limit = TIME_LIMIT

    def decide_shuffle_or_sort(self, *, board, opponent, turn, keys=None, moveSet=None):

        # Set max turns to adjust decay speed
        max_turns = 25
        to_change = keys if keys else moveSet

        # Calculate how much randomness we still want
        randomness_probability = max(0.20, 0.80 * (1 - turn / max_turns))
        # After max_turns, randomness is 20%

        if random.random() < randomness_probability:
            random.shuffle(to_change)
            return to_change

        if keys:
            return self.sort_keys_by_camp(board=board, keys=keys, opponent=opponent)
        
        else:
            return self.sort_moves_by_camp(board=board, moves=moveSet, opponent=opponent)

    
    def sort_moves_by_camp( self, *, board, moves, opponent):

        queue = []
        end = []
        opSquares = opponent.homeSquares
        
        for (row, col) in moves:

            if (row, col) not in opSquares:
                queue.append( (row, col) )
            else:
                end.append( (row, col) )
        
        # combine the two
        return queue + end   


    def sort_keys_by_camp( self, *, board, keys, opponent ):

        queue = []
        end = []
        opSquares = opponent.homeSquares
        
        for key in keys:

            row, col = key.get_coords( board=board)

            if (row, col) not in opSquares:
                queue.append( key )
            else:
                end.append( key )
        
        # combine the two
        return queue + end      

    def minimax_search(self, *, board, player, opponent, turn):
        # initialize variables
        best_score = float("-inf")
        best_piece = None
        best_move = None
        found_win = False
        boards = [0]

        # get all valid moves for self
        validMoves = self.get_moves_dict(board=board, player=self)

        keys = list( validMoves.keys() )
        keys = self.decide_shuffle_or_sort(board=board, keys=keys, opponent=opponent, turn=turn)

        # start the clock
        self.start_time = time.time()

        # loop through each piece and its moveset
        for piece in keys:

            # get the moveset
            moveSet = list(validMoves[piece])
            moveSet = self.decide_shuffle_or_sort(board=board, moveSet=moveSet, opponent=opponent, turn=turn)

            # loop thru moveset
            for move in moveSet:

                # generate new board
                new_board = self.simulate_move(board=board, piece=piece, move=move)

                # check the win before we  go into minimax
                if self.check_win(board=new_board, player=player, opponent=opponent, displayBoard=False):
                    best_score = score
                    best_piece = piece
                    best_move = move
                    found_win = True
                    break

                # evaluate score with minimax + alpha-beta + time limit
                score = self.minimax(
                    board=new_board,
                    depth=self.search_depth, 
                    max_player=True,
                    player=player,
                    opponent=opponent,
                    rootPlayer=player,
                    rootOpponent=opponent,
                    alpha=float("-inf"),
                    beta=float("inf"),
                    boards=boards
                )   
                
                if score > best_score:
                    best_score = score
                    best_piece = piece
                    best_move = move

            if found_win:
                break

        # self.end_time = time.time()

        # print(f'''\n===== Statistics ===== 
        #       - ABpriuning: {self.ABpruning}
        #       - Plies: {plies[0]} 
        #       - Time: { round(self.end_time - self.start_time, 2)} seconds''')

        # quit()
        # print(best_piece.canvasPiece, best_move, best_score)
        return best_piece, best_move
    
    def minimax(self, board, depth, max_player, player, opponent, rootPlayer, rootOpponent, alpha, beta, boards):
        # Check if we have exceeded the allowed time limit
        if time.time() - self.start_time > self.time_limit:
            return calculate_score(board=board, player=rootPlayer, opponent=rootOpponent)

        # If maximum depth is reached or someone has won, return the evaluated score of the board
        if depth == 0 or self.check_win(board=board, player=rootPlayer, opponent=rootOpponent, displayBoard=False):
            return calculate_score(board=board, player=rootPlayer, opponent=rootOpponent)

        # Get all valid moves for the current player
        validMoves = self.get_moves_dict(board=board, player=player)

        # If no valid moves are available, return the evaluated score
        if not validMoves:
            return calculate_score(board=board, player=rootPlayer, opponent=rootOpponent)

        # If it's the maximizing player's turn
        if max_player:
            best_score = float("-inf")  # Initialize best score very low

            # Iterate over each piece and its possible moves
            for piece, moveSet in validMoves.items():
                boards[0] += 1  # Increment counter tracking number of board states explored

                for move in moveSet:
                    # Simulate making the move to get the new board state
                    new_board = self.simulate_move(board=board, piece=piece, move=move)

                    # Recursively call minimax for the minimizing player's turn
                    score = self.minimax(
                        board=new_board,
                        depth=depth - 1,
                        max_player=False,     # Now opponent's turn
                        player=opponent,      # Opponent becomes current player
                        opponent=player,      # Current player becomes opponent
                        rootPlayer=rootPlayer,
                        rootOpponent=rootOpponent,
                        alpha=alpha,
                        beta=beta,
                        boards=boards
                    )

                    # Choose the maximum score 
                    best_score = max(best_score, score)

                    # alpha beta
                    if self.ABpruning:
                        alpha = max(alpha, best_score)  # Update alpha
                        if beta <= alpha:
                            break  # Beta cutoff — prune the remaining sibling nodes

            return best_score  # Return the best score found for this branch

        # If it's the minimizing player's turn
        else:
            best_score = float("inf")  # initialize best score very high

            # Iterate over each piece
            for piece, moveSet in validMoves.items():

                # and its moves
                for move in moveSet:

                    # do the move
                    new_board = self.simulate_move(board=board, piece=piece, move=move)

                    # Recursively call minimax for the maximizing player's turn
                    score = self.minimax(
                        board=new_board,
                        depth=depth - 1,
                        max_player=True,     # Now it's maximizing player's turn
                        player=opponent,     # Opponent becomes current player
                        opponent=player,     # Current player becomes opponent
                        rootPlayer=rootPlayer,
                        rootOpponent=rootOpponent,
                        alpha=alpha,
                        beta=beta,
                        boards=boards
                    )

                    # Choose the minimum score 
                    best_score = min(best_score, score)

                    # alpha beta
                    if self.ABpruning:
                        beta = min(beta, best_score)  # Update beta
                        if beta <= alpha:
                            break  # prune the remaining nodes

            return best_score  # Return the best score found for this branch
        
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