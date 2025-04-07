import tkinter as tk
from tkinter import messagebox
import random
from players import *
from standardConstants import *

# halma class
class Halma:

    def __init__(self, root, board_size=8, playerList=[]):
        self.root = root
        self.board_size = board_size
        self.colors = colors
        self.names = names
        self.bots = []
        self.players = []

        # Set up players
        self.players = initialize_players(playerList)
        self.player1 = self.players[0]
        self.player2 = self.players[1]

        # setup visuals
        self._setup_visuals()

        # Internal board and state variables
        self.board = None
        self.selected_piece = None
        self.home_squares = {}
        self.highlighted_squares = []

        # Set up board
        self.display_players()
        self.initialize_board()

        # Mouse click binding
        self.canvas.bind("<Button-1>", self.on_click)

        # Sanity check
        assert self.board is not None


   
    
    def add_home( self, row, col, player ):
        self.home_squares[(row, col)] = player

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

    def check_win(self) -> bool:

        print(self.board)


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

        print(f"Playing with {len(self.players)} players\n")

        for player in self.players:
            player.display()
    
    def highlight_moves(self, row, col):
        visited = set()
        self.highlighted_squares = []

        # Adjacent single-step moves
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                    (-1, -1), (-1, 1), (1, -1), (1, 1)]

        # Step 1: Add single-step moves
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if self.is_in_bounds(r, c) and self.board[r][c] is None:
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

                 
    # def highlight_moves(self, row, col):
    #     directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
    #                   (-1, -1), (-1, 1), (1, -1), (1, 1)]
    #     for dr, dc in directions:
    #         r, c = row + dr, col + dc
    #         if 0 <= r < self.board_size and 0 <= c < self.board_size:
    #             if self.board[r][c] is None:
    #                 x0 = c * CELL_SIZE
    #                 y0 = r * CELL_SIZE
    #                 x1 = x0 + CELL_SIZE
    #                 y1 = y0 + CELL_SIZE
    #                 rect = self.canvas.create_rectangle(x0, y0, x1, y1, fill=HIGHLIGHT_COLOR)
    #                 self.highlighted_squares.append((r, c))

    def initialize_board( self ):

        # initialize variables
        self.board = []

        # loop through rows
        for row in range( self.board_size ):

            # create empty list
            new_row = []

            # loop through cols
            for col in range( self.board_size ):

                # throw a None in
                new_row.append( None )

            # append to board
            self.board.append( new_row )

        # draw the grid
        self.draw_grid()

        # place the initial pieces
        self.place_initial_pieces()


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
        self.status.config(text=f"Moved to ({to_row}, {to_col})")

    def on_click(self, event):

        # get row and col
        row = event.y // CELL_SIZE
        col = event.x // CELL_SIZE

        # if a piece has been selected
        if self.selected_piece:

            # and is being moved to a highlighted space
            if (row, col) in self.highlighted_squares:

                # move it
                self.move_piece(self.selected_piece, row, col)

                # clear all highlights
                self.clear_highlights()

                # reset selected piece
                self.selected_piece = None
            
            # the movement is invalid 
            else:
                # clear highlights
                self.clear_highlights()

                # reset selected piece
                self.selected_piece = None

        # base case: no piece selected but the click is legit
        elif self.board[row][col]:

            # select the piece
            self.selected_piece = (row, col)

            # highlight the moves
            self.highlight_moves(row, col)

        # bad click:
        else:

            # clear highlights
            self.clear_highlights()

            # reset selected piece
            self.selected_piece = None

    def place_initial_pieces(self):

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

                    # add the piece to the board
                    self.add_piece( row, col, self.player1.mainColor, self.player1.homeColor )

                    # record it as a home spot
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

                    # add the piece to the board
                    self.add_piece(row, col, self.player2.mainColor, self.player2.homeColor)

                    # record it as a home spot
                    self.add_home( row, col, self.player2 )

    '''
    Private functions
    '''
    def _setup_visuals(self):

# Main container frame with white background
        self.main_frame = tk.Frame(root, bg="white")
        self.main_frame.pack(padx=50, pady=50)

        # Top label frame inside main_frame
        self.top_label_frame = tk.Frame(self.main_frame, bg="white")
        self.top_label_frame.pack(fill='x')

        self.top_player_label = tk.Label(self.top_label_frame, 
                                        text=f"Player 1: {self.player1.name}", 
                                        bg=self.player1.homeColor, 
                                        fg="black", 
                                        font=("Arial", 12), 
                                        anchor='w')
        self.top_player_label.pack(side='left', padx=5, pady=5)

        # # Canvas frame with padding for white border
        self.canvas_frame = tk.Frame(self.main_frame, bg="white", padx=5, pady=5)
        self.canvas_frame.pack()

        self.canvas = tk.Canvas(self.canvas_frame, 
                                width=self.board_size * CELL_SIZE, 
                                height=self.board_size * CELL_SIZE,
                                bg="white", 
                                highlightthickness=4)
        self.canvas.pack()

        # Bottom label frame inside main_frame
        self.bottom_label_frame = tk.Frame(self.main_frame, bg="white")
        self.bottom_label_frame.pack(fill='x')

        self.bottom_player_label = tk.Label(self.bottom_label_frame, 
                                            text=f"Player 2: {self.player2.name}", 
                                            bg=self.player2.homeColor, 
                                            fg="black", 
                                            font=("Arial", 12), 
                                            anchor='w')
        self.bottom_player_label.pack(side='left', padx=5, pady=5)

        # Status label (below everything)
        self.status = tk.Label(root, 
                            text="Halma", 
                            font=("Arial", 14))
        self.status.pack(pady=5)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Halma - Part 0 GUI")
    game = Halma(root, board_size=8)
    root.mainloop()