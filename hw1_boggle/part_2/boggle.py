import time
from movement import *

DEBUG = False
CLEVER = False
LINE_LEN = 120
LINE_SEP = "="
LEVEL_SEP = "   "
LINE_SEP_1 = "%"
MIN_WORD_LEN = 2

def dfs( myBoard:list, valid_words:list ):

    # initialize variable
    recursions = [0]
    level = 0
    results = set()
    prefixes = loadPrefixes( valid_words )

    # run on every letter
    for row in range( 0, len(myBoard) ):

        # loop though letters
        for col in range( 0, len( myBoard) ):

            if DEBUG:
                print(LINE_SEP_1 * ( LINE_LEN ) )
                print(f"NEW STARTING LETTER: {myBoard[row][col]} ({row, col})")
                print(LINE_SEP_1 * ( LINE_LEN ) )

            # reset path
            path = []
            level = 0

            # construct position    
            position = (row, col)

            # run DFS helper
            dfs_helper( position, myBoard, path, valid_words, prefixes, results, level, recursions )

        if DEBUG:
            print(LINE_SEP *  LINE_LEN)

    # return results 
    return results, recursions[0]

def dfs_helper( position:tuple, myBoard:list, path:list, valid_words:list, prefixes:set, results:set, level:int, recursions:list):

    # initialize variables
    level += 1
    recursions[0] += 1

    # print debug
    if DEBUG:
        print(LINE_SEP *  LINE_LEN)

    # initialize variables 
    word, in_prefixes = examineState( myBoard, position, path, prefixes )

    if DEBUG :
        print(f'''
(!) LEVEL {level} RECURSION

{LEVEL_SEP * level} Now examining: {position}
{LEVEL_SEP * level}- Letter: {word[-1]}
{LEVEL_SEP * level}- Word: {word}
{LEVEL_SEP * level}- In Dict: { word in valid_words }
            ''')

    # check if word is NOT in prefix set. dead end!
    if not in_prefixes:

        if DEBUG:
            print(LEVEL_SEP * level, end="")
            print(f"(!) {word} is a dead end.")
        # fall out early
        return 

    # save 
    if word in valid_words:

        # add to results
        results.add(word)

    # add path explored
    path.append( position )

    # get possble moves
    possible_moves = possibleMoves( position, myBoard )

    # filter legal moves
    legal_moves = legalMoves( possible_moves, path )

    if DEBUG and len( legal_moves ) > 0:

        print( f'''
{LEVEL_SEP * level}Possible Moves : {possible_moves} 
{LEVEL_SEP * level}Path           : {path}
{LEVEL_SEP * level}Legal Moves    : {legal_moves}
''')
            
        print(LEVEL_SEP * level, end="")
        print(f"{position}: Letters from {word}: ", end ="")

        for position in legal_moves:
            print( myBoard[ position[0] ][position[1]], end=", " )
        print()
        print()

    # recursively explore each legal move 
    for position in legal_moves:

        # recurse
        dfs_helper( position, myBoard, path, valid_words, prefixes, results, level, recursions )

    # backtrack
    path.pop()
        
def examineState( myBoard, position, path, myDict ):

    # initialize variables
    word = ""

    # construct current word
    for ( x, y ) in path:

        # grab letter
        letter = myBoard[x][y]

        # add to word str
        word = word + letter

    # grab current letter at x, y 
    letter = myBoard[position[0]][position[1]]

    # add to word str
    word = word + letter

    # return (<current word generated>, <yes/no depending on whether that word is in dictionary>).
    return ( word, word in myDict )

def legalMoves( moves, path):
    '''
    Takes in a list of possible moves as well as a path (list of x-y pairs) of places you’ve already been, 
    and essentially subtracts the latter from the former: the only legal moves are possible moves minus 
    any places that you’ve already been.
    '''
    # initialize variables
    legalMoves = set()

    # loop through path
    for move in moves:
        
        # determine if move has been visited
        if move not in path:

            # destructively remove the move
            legalMoves.add( move )
            
    # return moves
    return legalMoves

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

def loadPrefixes( valid_words ):

    # initialize variables 
    prefixes = set()

    # loop though words
    for word in valid_words:

        # loop through word, saving index
        for index in range( len( word ) ):

            # add chunk of text to prefixes
            prefixes.add( word[:index+1].upper() )

    # return prefixes
    return prefixes

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

def printResults( results, recursions, seconds ):

    current_len = MIN_WORD_LEN
    total_words = len( results )
    results = list( results )
    #results.sort() # sorts normally by alphabetical order
    results.sort(key=len) # sorts by descending length

    # results have been found 
    if total_words > 0 :
    
        # summary
        print(f"\nSearched a total of {recursions} moves in {seconds} seconds.\n")

        # words found
        print("Words found:")

        # prime the loop
        print(f"{current_len}-letter words: {results[0]}", end="")

        # print the rest of results
        for index in range(1, len(results) ):

            # grab result at index
            result = results[index]

            if len(result) == current_len:
                print( ", " + result, end="")
            else:
                current_len = len(result)
                print()
                print(f"{current_len}-letter words: {result}", end="")

        print()
        print()
        print(f"Found { total_words } words in total.")
        print("Alpha-sorted list words:")
        results.sort()

        # prime the loop
        print( results[0], end="" )

        for index in range(1, len( results ) ):

            print( f", {results[index]}", end="")

        print()

    else:
        print("No valid words in this puzzle :(")

    print()

# reads the dictionary into python as a list.
def readDictionary( filename ):

    # initialize variables
    word_list = []

    # open the file
    with open( filename, "r" ) as fp:

        # get lines
        lines = fp.readlines()

        # loop thru lines
        for line in lines:

            # append word to word_list
            word_list.append( line.strip().upper() )

    # return word list
    return word_list

def runBoard(board_filename, dictionary_filename):

    # Initialize variables
        # None

    # grab objects
    myBoard = loadBoard( board_filename )
    valid_words = readDictionary( dictionary_filename )
    
    # display board
    # printBoard( myBoard )

    # dfs
    start_time = time.time()
    results, recursions = dfs( myBoard, valid_words )
    end_time = time.time()

    # calculate seconds
    seconds = round(end_time - start_time, 4)

    data = {
        "N": len( myBoard ),
        "moves": recursions,
        "seconds": seconds,
        "word_count": len( results ), 
        "word_list": list(results)
    }

    return data