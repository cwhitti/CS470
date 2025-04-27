from standardConstants import *
from playersHelper import switch_players
from scoreHelper import calculate_score, visualize_board
from scoreHelper import *
from Piece import Piece

def add_home( self, row, col, player ):
    self.home_squares[(row, col)] = player
    player.add_home_square( row, col )

def add_highlight( self, row, col, color ):

    # calculate x and y
    x0 = col * CELL_SIZE
    y0 = row * CELL_SIZE
    x1 = x0 + CELL_SIZE
    y1 = y0 + CELL_SIZE

    # create the highlight
    self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")

    # add the highlight
    self.highlighted_squares.append( (row, col) )

def add_piece(self, row, col, owner ):

    # calc x and y
    x = col * CELL_SIZE + CELL_SIZE // 2
    y = row * CELL_SIZE + CELL_SIZE // 2

    # add the piece
    self.board[row][col] = self.create_piece(owner=owner, x=x, y=y)

def bold_piece(self, row, col):
    # Clear any existing bold effects first
    self.clear_bolds()
    pieceObj = self.board[row][col]  # Assuming you store Canvas item IDs in a dict

    if pieceObj:
        piece_id = pieceObj.get_id()
        self.canvas.itemconfig(piece_id, width=4, outline='black')  # Thicker border for bold effect
        self.bolded_pieces.append( (row, col) )

def check_win(self, *, player, opponent, board=None, displayBoard=False) -> bool:

    opHomeSquares = opponent.get_home_squares()

    if board==None:
        board = self.board

    if displayBoard:
        visualize_board( board )

    for row, col in opHomeSquares:

        if not self.occupied_by(row, col, player=player, board=board):
            return False  # one of the opponent's home squares is not occupied by self

    if ( displayBoard ):

        print("^^^ GIRL YOU WON THAT!!! ^^^ ")

    return True  # all opponent's home squares are occupied by self

def create_piece( self, owner, x, y ):

    # create the piece
    canvasPiece = self.canvas.create_oval(
        x - PIECE_RADIUS, y - PIECE_RADIUS,
        x + PIECE_RADIUS, y + PIECE_RADIUS,
        fill=owner.mainColor
    )

    # create its text
    canvasText = self.canvas.create_text(
            x, y,            # center position (same as oval center)
            text=str(canvasPiece),       
            fill="Black",    # text color
            font=("Helvetica", 12, "bold"),  # optional font styling,
            tags=("piece_text", f"text_{canvasPiece}")
            )

    # create the object
    pieceObj = Piece( canvasPiece = canvasPiece,
                      canvasText = canvasText,
                      owner=owner )

    # return piece object
    return pieceObj

def clear_bolds( self ):

    # go through the highlighted squares
    for row, col in self.bolded_pieces:

        pieceObj = self.board[row][col] # Assuming you store Canvas item IDs in a dict

        if pieceObj:
            piece_id = pieceObj.get_id()
            self.canvas.itemconfig(piece_id, width=1, outline='white')  # Thicker border for bold effect
            self.bolded_piece = (row, col)
            self.bolded_pieces = (row, col)
        
        # self.canvas.tag_raise(piece)
    self.bolded_pieces = []

def clear_highlights(self):

    # remove highlights
    self.canvas.delete("highlight")

    # go through the highlighted squares
    for row, col in self.highlighted_squares:

        # get the rect size
        x0 = col * CELL_SIZE
        y0 = row * CELL_SIZE
        x1 = x0 + CELL_SIZE
        y1 = y0 + CELL_SIZE

        # Restore correct background color
        if (row, col) in self.home_squares:
            bg_color = self.home_squares[(row, col)].homeColor
        else:
            bg_color = "white"

        # make a new rectangle
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=bg_color, outline="black")

        # If a piece exists here, bring it back on top
        pieceObj = self.board[row][col]

        # make sure it exists
        if pieceObj:
            piece_id = pieceObj.get_id()
            self.canvas.tag_raise(piece_id)

    # raise text tags back up 
    self.canvas.tag_raise("piece_text")  

    # clear the square
    self.highlighted_squares = []

def draw_grid(self):

    # loop though rows
    for row in range(self.board_size):

        # loop through cols
        for col in range(self.board_size):

            # bottom point
            x0 = col * CELL_SIZE
            y0 = row * CELL_SIZE

            # top point
            x1 = x0 + CELL_SIZE
            y1 = y0 + CELL_SIZE

            # create the rectangle
            self.canvas.create_rectangle(x0, y0, 
                                            x1, y1, 
                                            fill="white", 
                                            outline="black")
            

def end_game(self, winner=None):

    # player has won
    self._log_move( f"\n{self.current_player.name} has won!\n")

    self.player1.score = calculate_score( self.board, self.player1, self.player2 )
    self.player2.score = calculate_score( self.board, self.player2, self.player1 )
    self.update_scores()

    self._log_move( f"Game Over.")
    self._log_move( f"{self.current_player.name}'s score: {calculate_score(self.board, self.current_player, self.opponent)}")
    self._log_move( f"{self.opponent.name}'s score: {calculate_score(self.board, self.opponent, self.current_player)}")

    # messagebox.showinfo("Game Over", f"{winner} wins!")
    self.canvas.unbind("<Button-1>")  # Prevent further moves
    # self.root.after(1000, self.root.destroy)  # Wait 1s, then close

def end_turn( self ):

    print(f"Ending {self.current_player.name}'s turn.")

    # check for a valid win
    if self.check_win( player=self.current_player, opponent=self.opponent ):

        # end game
        self.end_game( winner = self.current_player )

    # nobody has won so swap players
    else:
        self.current_player, self.opponent = self.opponent, self.current_player
        self._update_turn_label()

        self.player1.score = calculate_score( self.board, self.player1, self.player2)
        self.player2.score = calculate_score( self.board, self.player2, self.player1)
        self.update_scores()

        # start the next player!
        self.start_turn()

def get_piece_owner( self, row, col ):

    # get the piece
    piece = self.board[row][col]

    # check that the space is occupied
    if piece != None:

        # return the owner
        return piece.owner
    
    # return None
    return None

def get_all_pieces( self, *, player = None, board=None ):

    # initialize variables
    pieces = []
    if board == None:
        board=self.board

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
                if player != None and pieceObj.owner == player:

                    # add to pieces list
                    pieces.append( pieceObj )

                # else if we don't care about player
                elif player == None:

                    # add to pieces list
                    pieces.append( pieceObj )
    # return pieces
    return pieces

def get_valid_moves( self, row, col, highlight=False, board=None ):

    # initialize variables
    visited = set()

    # set board to self if in halma class
    if board == None:
        board = self.board

     # Adjacent single-step moves
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                (-1, -1), (-1, 1), (1, -1), (1, 1)]

    # Step 1: Add single-step moves
    for dr, dc in directions:
        r, c = row + dr, col + dc

        # ensure it's in bounds
        if self.is_in_bounds(r, c, board) and board[r][c] is None:

            # highlight if told to 
            if highlight:
                self.add_highlight(r, c, HIGHLIGHT_COLOR)

            # add to visited
            visited.add((r, c))

    # Step 2: Add multi-hop jump moves
    self.find_jumps(row=row, col=col, visited=visited, highlight=highlight, board=board)

    # return visited
    return visited

def find_jumps(self, *, row, col, visited:set, highlight=False, board=None):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                (-1, -1), (-1, 1), (1, -1), (1, 1)]

    if board == None:
        board = self.board

    assert (board != None)

    for dr, dc in directions:
        mid_r, mid_c = row + dr, col + dc
        jump_r, jump_c = row + 2*dr, col + 2*dc

        if self.is_in_bounds(jump_r, jump_c, board):
            if board[mid_r][mid_c] is not None and board[jump_r][jump_c] is None:
                if (jump_r, jump_c) not in visited:

                    # highlight if told to
                    if highlight:
                        self.add_highlight(jump_r, jump_c,HIGHLIGHT_COLOR)

                    # add to visited
                    visited.add((jump_r, jump_c))

                    # Recursive jump chain
                    self.find_jumps(row=jump_r, col=jump_c, visited=visited, highlight=highlight, board=board)

def is_in_bounds(self, r, c, board ):
    return 0 <= r < len(board) and 0 <= c < len(board)

def initialize_board_from_file( self, filename ):
    
    # initialize board
    board = []
    size = 0

    #TODO: Check if file exists

    # open filename
    with open( filename ) as file:

        # read the lines
        gameState = file.readlines()

        # grab current player string
        self.current_player = gameState[0].strip()

        # go by lines in the file
        for row in gameState[1:]:

            # ignore accidental new lines
            if row != "\n":

                # strip the newline, split by space
                elms = row.strip().split(" ")

                # append to board
                board.append( elms )
                
                # increment size
                size += 1
    
    # set board size 
    self.board_size = size 

    # return board
    return board

def initialize_empty_board( self ):

    # initialize variables
    half = self.board_size // 2
    board = []

    '''
    Initialize board with all nones
    '''
    for row in range( self.board_size ):
        
        new_row = []

        for col in range( self.board_size ):
            
            # put in none
            new_row.append(None)

        board.append( new_row )

    '''
    Top left player
    '''

    # loop through rows
    for row in range( half ):

        # loop through cols
        for col in range( half ):

            # ensure triangle shape
            if row + col < half:

                # set to p1 marker
                board[row][col] = P1_MARKER
                
    '''
    Bottom right player
    '''

    # loop through rows, starting from middle
    for row in range(self.board_size - half , self.board_size):

        # loop through cols, starting from middle
        for col in range(self.board_size-half, self.board_size):

            # see if col is in the bottom right
            if col >= self.board_size - (row - (self.board_size - half)) - 1:

                # set to p2 marker
                board[row][col] = P2_MARKER

    return board
                
def initialize_board( self, filename ):

    # initialize custom board for debug
    if filename != None:
        self.board = self.initialize_board_from_file( filename )

    # initialize empty board
    else:
        self.board = self.initialize_empty_board()

def get_moves_dict(self, player, board=None):

    # initialize variables
    validMoves = {}

    if board ==None:
        board = self.boards

    pieces = self.get_all_pieces( player = player, board=board )

    # iterate thru pieces
    for pieceObj in pieces:

        # get the x, y
        x, y = pieceObj.get_coords( board=board )

        # assert that x & y exist
        assert (x != None and y != None )

        # get valid moves
        moves = self.get_valid_moves( row=x, col=y, highlight=False, board=board )

        # add validmoves to moves
        validMoves[pieceObj] = moves

    return validMoves

def move_piece(self, from_pos, to_row, to_col):

    from_row, from_col = from_pos
    piece = self.board[from_row][from_col]
    self.board[from_row][from_col] = None
    self.board[to_row][to_col] = piece

    x = to_col * CELL_SIZE + CELL_SIZE // 2
    y = to_row * CELL_SIZE + CELL_SIZE // 2
    self.canvas.coords(piece.canvasPiece,
                        x - PIECE_RADIUS, y - PIECE_RADIUS,
                        x + PIECE_RADIUS, y + PIECE_RADIUS)
    
    self.canvas.coords(piece.canvasText, x, y)
    self.canvas.tag_raise(piece.canvasPiece)
    self.canvas.tag_raise(piece.canvasText)
    
    self._log_move( f"{self.current_player.name}: [{piece.canvasPiece}] ({from_row}, {from_col})-> ({to_row}, {to_col})" )
    
def occupied_by( self, row, col, player, board=None ):

    # get the piece
    if board==None:
        board=self.board

    piece = board[row][col]

    # check that the space is occupied
    if piece != None:

        # compare to the player 
        return piece.owner == player

    # return False
    return False

def place_initial_pieces(self):

    # set row index 
    rowIndex = 0

    # Set the homes
    self.set_homes()

    # loop thru rows
    for row in self.board:

        # reset col index
        colIndex = 0 

        # loop thru cols
        for letter in row:

            # initialize spot as None since nothing is there
            if letter == NONE_MARKER:
                
                # board = None
                self.board[rowIndex][colIndex] = None

            # encounters P1 marker
            if letter == P1_MARKER:

                # add the piece 
                self.add_piece( rowIndex, colIndex, owner=self.player1 )

            # encounters P2 marker
            elif letter == P2_MARKER:
                
                # add the piece 
                self.add_piece( rowIndex, colIndex, owner=self.player2 )

            # increment colIndex
            colIndex += 1
        
        # increment rowIndex
        rowIndex += 1

        # raise text tags
        self.canvas.tag_raise("piece_text")

def set_current_player( self ):

    if self.current_player != None:

        if self.current_player == "1":
            self.current_player = self.player1
            self.opponent = self.player2

        elif self.current_player == "2":
            self.current_player = self.player2
            self.opponent = self.player1
        else:
            raise "Current Player not set in file"
    
    else:
        self.current_player = self.player1
        self.opponent = self.player2


def set_homes( self ):

    # initialize variables
    half = self.board_size // 2

    '''
    Top left player
    '''

    # loop through rows
    for row in range( half ):

        # loop through cols
        for col in range( half ):

            # ensure triangle shape
            if row + col < half:

                # set to p1 marker
                self.add_highlight( row, col, self.player1.homeColor)
                self.add_home( row, col, self.player1 )
                
                
    '''
    Bottom right player
    '''

    # loop through rows, starting from middle
    for row in range(self.board_size - half , self.board_size):

        # loop through cols, starting from middle
        for col in range(self.board_size-half, self.board_size):

            # see if col is in the bottom right
            if col >= self.board_size - (row - (self.board_size - half)) - 1:

                # set to p2 marker
                self.add_highlight( row, col, self.player2.homeColor)
                self.add_home( row, col, self.player2 )

def update_scores(self):
    self.player1_score_label.config(text=f"Score: {self.player1.score}")
    self.player2_score_label.config(text=f"Score: {self.player2.score}")

def update_rec_move( self, selectedPiece, newCoords, player ):

    if player == self.player1:
        self.recommended_move_label1.config(text=f"Recommended Move: {selectedPiece.canvasPiece} -> {newCoords}")
    else:
        self.recommended_move_label2.config(text=f"Recommended Move: {selectedPiece.canvasPiece} -> {newCoords}")