def loadBoard( filename ):

    # initialize variables
    board = []
    contents = loadFile( filename )

    # loop through lines of the file
    for line in contents:

        # strip \n and split for the letters
        row = line.strip().split(" ")

        # add to board
        board.append( row )

    return board

def loadFile( filename ):

    # open the file
    with open( filename, "r" ) as file:

        # return file lines
        return file.readlines()

def moveDiagDownLeft( xy_pair, n ):

    # go down
    xy_pair = moveDown( xy_pair, n )

    # check for valid move
    if xy_pair != None:

        # go left 
         xy_pair = moveLeft( xy_pair, n )

    return xy_pair

def moveDiagDownRight( xy_pair, n ):
    
    # go down
    xy_pair = moveDown( xy_pair, n )

    # check for valid move
    if xy_pair != None:

        # go right 
        xy_pair = moveRight( xy_pair, n )

    return xy_pair

def moveDiagUpLeft( xy_pair, n ):

    # go up
    xy_pair = moveUp( xy_pair, n )

    # check for valid move
    if xy_pair != None:

        # go left 
        xy_pair = moveLeft( xy_pair, n )

    return xy_pair

def moveDiagUpRight( xy_pair, n ):

    # go up 
    xy_pair = moveUp( xy_pair, n )

    # check for valid move
    if xy_pair != None:

        # go right
        xy_pair = moveRight( xy_pair, n )

    # return movement
    return xy_pair

def moveDown( xy_pair, n ):

    # initialize variables
    movement = None
    x, y = xy_pair
    y = y + 1

    # check if y + 1 > n
    if y <= n:
        movement = ( x, y ) # increase y
    
    return movement

def moveLeft( xy_pair, n ):

    # initialize variables
    movement = None
    x, y = xy_pair
    x = x - 1

    # check if y + 1 > n
    if x >= 0:
        movement = ( x, y ) # decrease x
    
    return movement

def moveRight( xy_pair, n ):
    
    # initialize variables
    movement = None
    x, y = xy_pair
    x = x + 1

    # check if y + 1 > n
    if x <= n:
        movement = ( x, y ) # increase x
    
    return movement

def moveUp( xy_pair, n ):

    # initialize variables
    movement = None
    x, y = xy_pair
    y = y - 1

    # check if y + 1 > n
    if y >= 0:
        movement = ( x, y ) # decrease y
    
    return movement

def possibleMoves(xy_pair, board_object):

    # define variables
    moves = set()
    n = len( board_object ) - 1

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
        if movement != None:

            # add to set
            moves.add( movement )

    # print moves
    print( moves )

def printBoard( board_object ):

    # initialize variables
        # None

    # loop thru rows
    for row in board_object:
    
        # loop thru cols
        for letter in row:

            # print letter
            print( letter, end=" " )
        # end letter loop
    
        # print newline
        print()

    # end row loop