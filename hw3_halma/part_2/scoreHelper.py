import math 

def compute_distance_map( board, player, opponent, extraPieces ):

    distance_score = 0

    for piece in extraPieces:
        row, col = piece.get_coords( board=board )
        
        # Find the minimum straight line distance to any opponent home square
        min_distance = float('inf')
        for (home_row, home_col) in opponent.homeSquares:
            distance = math.sqrt((row - home_row) ** 2 + (col - home_col) ** 2)
            if distance < min_distance:
                min_distance = distance

        # Reward inversely proportional to distance (closer pieces score higher)
        distance_score += 1 / (1 + min_distance)

    return distance_score


        
def calculate_score(board, player, opponent):

    score = 0
    pieces = get_all_pieces( player=player, board=board)

    for (row, col) in opponent.homeSquares:
        piece = board[row][col]

        if piece in pieces:
            score +=1 
            pieces.pop( pieces.index(piece) )
    
    score += compute_distance_map(board, player, opponent, pieces  )

    return round(score, 4)


def get_all_pieces(player, board ):

    # initialize variables
    pieces = []

    boardSize = len( board )

    # get all pieces in the board
    for row in range( boardSize ):
        
        # iter through cols
        for col in range( boardSize ):

            # grab the square
            pieceObj = board[row][col]

            # if we've grabbed a piece...
            if pieceObj != None:

                # check if we care who owns it
                if player != None and pieceObj.owner.name == player.name:

                    # add to pieces list
                    pieces.append( pieceObj )

                # else if we don't care about player
                elif player == None:

                    # add to pieces list
                    pieces.append( pieceObj )
    # return pieces
    return pieces


def visualize_board( board ):

    print()

    for row in range( len( board ) ):
        for col in range( len( board) ):

            piece = board[row][col]

            if piece != None:

                print( f" {piece.owner.name[0]} ", end="" )
            
            else:
                print( ' X ', end="")
        print()

    print()