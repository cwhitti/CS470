import tkinter as tk
from tkinter import messagebox
import random
from players import *
from standardConstants import *

# halma class
class Halma:

    # init
    def __init__(self, root, board_size=8, playerList=[], filename=None):

        # initialize variables
        self.filename = filename
        self.root = root
        self.board_size = board_size
        self.colors = colors
        self.names = names
        self.bots = []
        self.players = []

        # Internal board and state variables
        self.current_player = None
        self.opponent = None
        self.board = None
        self.selected_piece = None
        self.home_squares = {}
        self.pieces = {}
        self.highlighted_squares = []
        self.bolded_pieces = []

        # initialize the board
        self.initialize_board( filename )

        # Set up players
        self.players, self.bot_count = initialize_players(playerList)
        self.player1 = self.players[0]
        self.player2 = self.players[1]

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
            

        # setup visuals
        self._setup_visuals()

        # Mouse click binding
        self.canvas.bind("<Button-1>", self.on_click)

        # Sanity check
        assert self.board is not None

        # Set up board
        # self.display_players()

        # set up extra cogs
        self.root.after(0, self.on_start)


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

    def add_piece(self, row, col, pieceColor, bgColor=None, ):

        # calc x and y
        x = col * CELL_SIZE + CELL_SIZE // 2
        y = row * CELL_SIZE + CELL_SIZE // 2

        # Draw background color for piece if applicable
        if bgColor:
            self.add_highlight( row, col, bgColor )

        # create the piece
        piece = self.canvas.create_oval(
            x - PIECE_RADIUS, y - PIECE_RADIUS,
            x + PIECE_RADIUS, y + PIECE_RADIUS,
            fill=pieceColor
        )

        # add the piece
        self.board[row][col] = piece

    def bold_piece(self, row, col):
        # Clear any existing bold effects first
        self.clear_bolds()
        piece_id = self.board[row][col]  # Assuming you store Canvas item IDs in a dict

        if piece_id:
            self.canvas.itemconfig(piece_id, width=4, outline='black')  # Thicker border for bold effect
            self.bolded_pieces.append( (row, col) )

    def compute_distance_map(self, goal_cells):
            
            # Breadth-first search from all goal cells
            visited = {}
            frontier = list(goal_cells)
            for cell in frontier:
                visited[cell] = 0

            while frontier:
                current = frontier.pop(0)
                r, c = current
                for dr, dc in [(-1,0),(1,0),(0,-1),(0,1), (-1,-1),(1,1),(-1,1),(1,-1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.board_size and 0 <= nc < self.board_size:
                        neighbor = (nr, nc)
                        if neighbor not in visited:
                            visited[neighbor] = visited[current] + 1
                            frontier.append(neighbor)

            return visited
    
    def calculate_score(self, player, opponent):
        
        # initialize variables
        goal_cells = player.homeSquares
        score = 0
        pieces = []

        # loop thru rows
        for row in range(self.board_size):

            # loop thru cols
            for col in range(self.board_size):

                # get player for that space
                if self.get_piece_owner( row, col ) == player:

                    # One point for being in opponent's territory
                    if (row, col) in opponent.homeSquares:
                        score += 1

                    # save pieces to get HSLD
                    else:
                        pieces.append((row, col))

        # Precompute all distances from each board cell to the nearest goal cell using BFS
        distance_map = self.compute_distance_map(goal_cells)

        for r, c in pieces:
            d = distance_map.get((r, c), float('inf'))
            if d != float('inf') and d != 0:
                score += 1 / d

        return round(score, 3)
    
    def clear_bolds( self ):

        # remove highlights
        # self.canvas.delete("bolded_piece")

        # print( self.bolded_pieces )

        # go through the highlighted squares
        for row, col in self.bolded_pieces:

            # print("De-bolding")

            piece_id = self.board[row][col]  # Assuming you store Canvas item IDs in a dict

            # print(piece_id)

            if piece_id:
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
            piece = self.board[row][col]
            if piece:
                self.canvas.tag_raise(piece)

        self.highlighted_squares = []

    def check_win(self, player, opponent) -> bool:

        # initialize variables 
        index = 0

        # get home squares for opposite player
        opHomeSquares = opponent.get_home_squares()

        # set length variable
        opHomeLen = len(opHomeSquares)

        # prime the loop
        row, col = opHomeSquares[ index ]

        # loop through home squares of opposing player, until the home square is NOT occupied by the current player
        while index < opHomeLen - 1 and self.occupied_by( row, col, player ):

            # increment index
            index += 1

            # get new 
            row, col = opHomeSquares[ index ]

        # check status of index, see if we ended the while loop early
        return index == opHomeLen - 1

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

    def display_players(self):

        print(f"Playing with {len(self.players)} players, {self.bot_count} bots\n")

        for player in self.players:
            player.display()
    
    def end_game(self, winner=None):

        # player has won
        self._log_move( f"\n{self.current_player.name} has won!\n")

        self.player1.score = self.calculate_score( self.player1, self.player2 )
        self.player2.score = self.calculate_score( self.player2, self.player1 )
        self.update_scores()

        self._log_move( f"Game Over.")
        self._log_move( f"{self.current_player.name}'s score: {self.calculate_score(self.current_player, self.opponent)}")
        self._log_move( f"{self.opponent.name}'s score: {self.calculate_score(self.opponent, self.current_player)}")

        # messagebox.showinfo("Game Over", f"{winner} wins!")
        self.canvas.unbind("<Button-1>")  # Prevent further moves
        # self.root.after(1000, self.root.destroy)  # Wait 1s, then close

    def get_piece_owner( self, row, col ):

        # get the piece
        piece = self.board[row][col]

        # check that the space is occupied
        if piece != None:

            # get the color
            color = self.canvas.itemcget(piece, "fill")

            # compare to the player 
            return get_player_by_color( self.players, color )
        
        # return None
        return None

    def highlight_moves(self, row, col):

        visited = set()
        self.highlighted_squares = []

        # Adjacent single-step moves
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                    (-1, -1), (-1, 1), (1, -1), (1, 1)]

        # Step 1: Add single-step moves
        for dr, dc in directions:
            r, c = row + dr, col + dc

            # print( self.board[r][c] )
            if self.is_in_bounds(r, c) and self.board[r][c] is None:

                # print("adding highlight")
                self.add_highlight(r, c, HIGHLIGHT_COLOR)
                visited.add((r, c))

        # Step 2: Add multi-hop jump moves
        self.find_jumps(row, col, visited)


    def find_jumps(self, row, col, visited):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                    (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            mid_r, mid_c = row + dr, col + dc
            jump_r, jump_c = row + 2*dr, col + 2*dc

            if self.is_in_bounds(jump_r, jump_c):
                if self.board[mid_r][mid_c] is not None and self.board[jump_r][jump_c] is None:
                    if (jump_r, jump_c) not in visited:
                        self.add_highlight(jump_r, jump_c,HIGHLIGHT_COLOR)
                        visited.add((jump_r, jump_c))
                        # Recursive jump chain
                        self.find_jumps(jump_r, jump_c, visited)

    def is_in_bounds(self, r, c):
        return 0 <= r < self.board_size and 0 <= c < self.board_size

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

    def move_piece(self, from_pos, to_row, to_col):

        from_row, from_col = from_pos
        piece = self.board[from_row][from_col]
        self.board[from_row][from_col] = None
        self.board[to_row][to_col] = piece

        x = to_col * CELL_SIZE + CELL_SIZE // 2
        y = to_row * CELL_SIZE + CELL_SIZE // 2
        self.canvas.coords(piece,
                           x - PIECE_RADIUS, y - PIECE_RADIUS,
                           x + PIECE_RADIUS, y + PIECE_RADIUS)
        
    def occupied_by( self, row, col, player ):

        # get the piece
        piece = self.board[row][col]

        # check that the space is occupied
        if piece != None:

            # get the color
            color = self.canvas.itemcget(piece, "fill")

            # compare to the player 
            return get_player_by_color( self.players, color ) == player
    

        # return False
        return False
    
    def on_click(self, event):

        # get row and col
        row = event.y // CELL_SIZE
        col = event.x // CELL_SIZE

        # if a piece has been selected
        if self.selected_piece:

            # and is being moved to a highlighted space
            if (row, col) in self.highlighted_squares:

                # clear all bolds 
                self.clear_bolds()

                # move it
                self.move_piece(self.selected_piece, row, col)

                # log it
                self._log_move( f"{self.current_player.name}: {self.selected_piece} -> ({row}, {col})" )

                # clear all highlights
                self.clear_highlights()

                # reset selected piece
                self.selected_piece = None

                # check for a valid win
                if self.check_win( self.current_player, self.opponent ):

                    # end game
                    self.end_game( winner = self.current_player )

                # nobody has won so swap players
                else:
                    self.current_player, self.opponent = self.opponent, self.current_player
                    self._update_turn_label()

                    self.player1.score = self.calculate_score( self.player1, self.player2)
                    self.player2.score = self.calculate_score( self.player2, self.player1)
                    self.update_scores()

            # the movement is invalid 
            else:
                # clear all bold 
                self.clear_bolds()

                # clear highlights
                self.clear_highlights()

                # reset selected piece
                self.selected_piece = None

        # base case: no piece selected but the click is legit, AND it's their own piece
        elif self.board[row][col] and self.get_piece_owner( row, col ) == self.current_player:

            # select the piece
            self.selected_piece = (row, col)

            self.bold_piece( row, col )

            # highlight the moves
            self.highlight_moves(row, col)

        # bad click:
        else:

            # clear all bold 
            self.clear_bolds()

            # clear highlights
            self.clear_highlights()

            # reset selected piece
            self.selected_piece = None
        
    def on_start( self ):
        self._log_move( f"Welcome to Halma!")
        self._log_move( f"Good luck, {self.player1.name} and {self.player2.name}.\n")

        if self.filename != None:
            self._log_move( f"<imported {self.filename}>\n")

        self.player1.score = self.calculate_score( self.player1, self.player2 )
        self.player2.score = self.calculate_score( self.player2, self.player1 )
        self.update_scores()

        if self.check_win(self.current_player, self.opponent) or self.check_win( self.opponent, self.current_player):
            self.end_game()

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
                    self.add_piece( rowIndex, colIndex, self.player1.mainColor )

                # encounters P2 marker
                elif letter == P2_MARKER:
                    
                    # add the piece 
                    self.add_piece( rowIndex, colIndex, self.player2.mainColor )


                # increment colIndex
                colIndex += 1
            
            # increment rowIndex
            rowIndex += 1

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

    '''
    Private functions
    '''

    def _setup_visuals(self):
        self._pack_main_frame()
        self._pack_player_1()
        self._pack_board_and_log()
        self._pack_player_2()
        self._pack_status_label()
        self.draw_grid()
        self.place_initial_pieces()

    def _log_move(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert('end', f"{message}\n")
        self.log_text.see('end')
        self.log_text.config(state='disabled')

    def _pack_main_frame(self):
        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(padx=50, pady=50)

    def _update_turn_label(self):
        self.turn_label.config(
            text=f"{self.current_player.name}'s Turn",
            fg=self.current_player.mainColor,
            bg=self.current_player.homeColor,
        )

    def _pack_player_1(self):
        self.top_label_frame = tk.Frame(self.main_frame, bg="white")
        self.top_label_frame.pack(fill='x')

        # Subframe to vertically stack name + score
        self.top_player_info = tk.Frame(self.top_label_frame, bg=self.player1.homeColor)
        self.top_player_info.pack(anchor='w', padx=5, pady=5)

        self.top_player_label = tk.Label(
            self.top_player_info, 
            text=f"Player 1: {self.player1.name}", 
            bg=self.player1.homeColor, 
            fg=self.player1.mainColor, 
            font=("Arial", 15, "bold"), 
            anchor='w'
        )
        self.top_player_label.pack(side='top', anchor='w')

        self.player1_score_label = tk.Label(
            self.top_player_info,
            text=f"Score: {self.player1.score}",
            bg=self.player1.homeColor,
            fg=self.player1.mainColor,
            font=("Arial", 12),
            anchor='w'
        )
        self.player1_score_label.pack(side='top', anchor='w')

    def _pack_player_2(self):
        self.bottom_label_frame = tk.Frame(self.main_frame, bg="white")
        self.bottom_label_frame.pack(fill='x')

        self.bottom_player_info = tk.Frame(self.bottom_label_frame, bg=self.player2.homeColor)
        self.bottom_player_info.pack(anchor='w', padx=5, pady=5)

        self.bottom_player_label = tk.Label(
            self.bottom_player_info, 
            text=f"Player 2: {self.player2.name}", 
            bg=self.player2.homeColor, 
            fg=self.player2.mainColor, 
            font=("Arial", 15, "bold"), 
            anchor='w'
        )
        self.bottom_player_label.pack(side='top', anchor='w')

        self.player2_score_label = tk.Label(
            self.bottom_player_info,
            text=f"Score: {self.player2.score}",
            bg=self.player2.homeColor,
            fg=self.player2.mainColor,
            font=("Arial", 12),
            anchor='w'
        )
        self.player2_score_label.pack(side='top', anchor='w')
        

    def _pack_board_and_log(self):

        # Container for canvas and log side-by-side
        self.board_and_log_frame = tk.Frame(self.main_frame, bg="white")
        self.board_and_log_frame.pack()

        # --- Board (Canvas) on the left ---
        self.canvas_frame = tk.Frame(self.board_and_log_frame, bg="white", padx=5, pady=5)
        self.canvas_frame.pack(side="left")

        self.canvas = tk.Canvas(
            self.canvas_frame, 
            width=self.board_size * CELL_SIZE, 
            height=self.board_size * CELL_SIZE,
            bg="white", 
            highlightthickness=4
        )
        self.canvas.pack()

        # --- Log + Turn Label on the right ---
        self.log_frame = tk.Frame(self.board_and_log_frame, bg="white")
        self.log_frame.pack(side="left", padx=10, pady=5)

        # Current Turn label (goes above the text log)
        self.turn_label = tk.Label(
            self.log_frame,
            text=f"{self.current_player.name}'s Turn",
            fg=self.current_player.mainColor,
            font=("Arial", 17, "bold"),
            bg=self.current_player.homeColor
        )
        self.turn_label.pack(anchor="w", pady=(0, 5))  # Left-aligned with padding below

        # Scrollable Text Log
        self.log_text = tk.Text(
            self.log_frame, 
            width=30, 
            height=int(self.board_size * CELL_SIZE / 15),
            wrap='word', 
            state='disabled', 
            bg="lightgray",
            fg="black"
        )
        self.log_text.pack(side='left', fill='y')

        self.log_scrollbar = tk.Scrollbar(self.log_frame, command=self.log_text.yview)
        self.log_scrollbar.pack(side='right', fill='y')
        self.log_text.config(yscrollcommand=self.log_scrollbar.set)

    def _pack_board(self):
        self.canvas_frame = tk.Frame(self.main_frame, bg="white", padx=5, pady=5)
        self.canvas_frame.pack()

        self.canvas = tk.Canvas(
            self.canvas_frame, 
            width=self.board_size * CELL_SIZE, 
            height=self.board_size * CELL_SIZE,
            bg="white", 
            highlightthickness=4
        )
        self.canvas.pack()

    def _pack_status_label(self):
        self.status = tk.Label(
            self.root, 
            text="Halma", 
            font=("Arial", 14)
        )
        self.status.pack(pady=5)