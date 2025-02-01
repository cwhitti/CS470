def isValidPosition( xy_pair, board):

    # ensure both variables != None
    if board != None and xy_pair != None:

        # grab x and y
        x, y = xy_pair

        # grab upper bounds
        upper_bound = len( board )

        # return valid position
        return ( x >= 0 and x < upper_bound ) and ( y >= 0 and y < upper_bound )

    # return false, not set up correctly
    return False

def legalMoves( moves, path):
    '''
    Takes in a list of possible moves as well as a path (list of x-y pairs) of places you’ve already been, 
    and essentially subtracts the latter from the former: the only legal moves are possible moves minus 
    any places that you’ve already been.
    '''
    # initialize variables
    legalMoves = set()

    #print( moves, path )

    # loop through path
    for move in moves:
        
        # determine if move has been visited
        if move not in path:

            # destructively remove the move
            legalMoves.add( move )
            
    # return moves
    return legalMoves

def possibleMoves(xy_pair, board_object):

    '''
    INITIALIZE PRIVATE FUNCTIONS
    '''
    # moveDiagDownLeft
    def moveDiagDownLeft( xy_pair, n ):

        # go down
        xy_pair = moveDown( xy_pair, n )

        # check for valid move
        if xy_pair != None:

            # go left 
            xy_pair = moveLeft( xy_pair, n )

        return xy_pair

    # moveDiagDownRight
    def moveDiagDownRight( xy_pair, n ):
        
        # go down
        xy_pair = moveDown( xy_pair, n )

        # check for valid move
        if xy_pair != None:

            # go right 
            xy_pair = moveRight( xy_pair, n )

        return xy_pair

    # moveDiagUpLeft
    def moveDiagUpLeft( xy_pair, n ):

        # go up
        xy_pair = moveUp( xy_pair, n )

        # check for valid move
        if xy_pair != None:

            # go left 
            xy_pair = moveLeft( xy_pair, n )

        return xy_pair

    # moveDiagUpRight
    def moveDiagUpRight( xy_pair, n ):

        # go up 
        xy_pair = moveUp( xy_pair, n )

        # check for valid move
        if xy_pair != None:

            # go right
            xy_pair = moveRight( xy_pair, n )

        # return movement
        return xy_pair

    # moveDown
    def moveDown( xy_pair, n ):

        # initialize variables
        movement = None
        x, y = xy_pair
        y = y + 1

        # check if y + 1 < n
        if y < n:
            movement = ( x, y ) # increase y
        
        return movement

    # moveLeft
    def moveLeft( xy_pair, n ):

        # initialize variables
        movement = None
        x, y = xy_pair
        x = x - 1

        # check if  x - 1 >= 0
        if x >= 0:
            movement = ( x, y ) # decrease x
        
        return movement

    # moveRight
    def moveRight( xy_pair, n ):
        
        # initialize variables
        movement = None
        x, y = xy_pair
        x = x + 1

        # check if x + 1 < n
        if x < n:

            movement = ( x, y ) # increase x
        
        return movement

    # moveUp
    def moveUp( xy_pair, n ):

        # initialize variables
        movement = None
        x, y = xy_pair
        y = y - 1

        # check if y - 1 > n
        if y >= 0:
            movement = ( x, y ) # decrease y
        
        return movement

    # define variables
    moves = set()
    n = len( board_object )

    # define movement list
    actions = [
        
            # true movements
            moveRight, 
            moveLeft, 
            moveUp, 
            moveDown,
            
            # diagonal movements
            moveDiagDownLeft, 
            moveDiagDownRight, 
            moveDiagUpLeft, 
            moveDiagUpRight 
        ]
    
    # try moves
    for action in actions:

        # try moving to new position
        movement = action( xy_pair, n )

        # validate movement 
        if movement != None and isValidPosition( movement, board_object ):

            # add to set
            moves.add( movement )

    # print moves
    return moves 