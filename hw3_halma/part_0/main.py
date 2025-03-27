import tkinter as tk
from tkinter import messagebox
import random
from players import *
from standardConstants import *

# halma class
class Halma:

    # initializor function, takes root and optional board size
    def __init__(self, root, board_size=8, playerList=[]):

        # initialize custom variables
        self.root = root
        self.board_size = board_size
        self.colors = colors
        self.names  = names
        self.bots = []
        self.players = []

        # initialize canvas
        self.canvas = tk.Canvas(root, 
                                width=board_size*CELL_SIZE, 
                                height=board_size*CELL_SIZE
                                )
        self.canvas.pack()

        # set status
        self.status = tk.Label(root, 
                               text="Halma", 
                               font=("Arial", 14)
                               )
        self.status.pack()

        # initialize empty data structures
        self.board = None
        self.selected_piece = None
        self.home_squares = {}
        self.highlighted_squares = []

        # set up the players
        self.players = initialize_players( playerList )
        self.player1 = self.players[0]
        self.player2 = self.players[1]

        # set up the board
        self.display_players()
        self.initialize_board()

        # bind a button
        self.canvas.bind("<Button-1>", self.on_click)

        # assertions
        assert( self.board != None )

    def add_highlight( self, row, col, color, home=False ):

        # calculate x and y
        x0 = col * CELL_SIZE
        y0 = row * CELL_SIZE
        x1 = x0 + CELL_SIZE
        y1 = y0 + CELL_SIZE

        self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")

        if home:
            self.home_squares[(row, col)] = get_player_by_color( self.players, color )

        else:
            self.highlighted_squares.append( (row, col) )


    def add_piece(self, row, col, pieceColor, bgColor=None, ):

        # calc x and y
        x = col * CELL_SIZE + CELL_SIZE // 2
        y = row * CELL_SIZE + CELL_SIZE // 2

        # Draw background color for piece if applicable
        if bgColor:
            self.add_highlight( row, col, bgColor, home=True)

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

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=bg_color, outline="black")

            # If a piece exists here, bring it back on top
            piece = self.board[row][col]
            if piece:
                self.canvas.tag_raise(piece)

        self.highlighted_squares = []


        # # delete highlights
        # self.canvas.delete("highlight")

        # #
        # for row, col in self.highlighted_squares:

        #     if (row, col) in self.home_sqares:

        #         x0 = col * CELL_SIZE
        #         y0 = row * CELL_SIZE
        #         x1 = x0 + CELL_SIZE
        #         y1 = y0 + CELL_SIZE

        #         self.canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")
        #         piece = self.board[row][col]
        #         if piece:
        #             self.canvas.tag_raise(piece)

        # self.highlighted_squares = []

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
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.board_size and 0 <= c < self.board_size:
                if self.board[r][c] is None:
                    x0 = c * CELL_SIZE
                    y0 = r * CELL_SIZE
                    x1 = x0 + CELL_SIZE
                    y1 = y0 + CELL_SIZE
                    rect = self.canvas.create_rectangle(x0, y0, x1, y1, fill=HIGHLIGHT_COLOR)
                    self.highlighted_squares.append((r, c))

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

        row = event.y // CELL_SIZE
        col = event.x // CELL_SIZE

        if self.selected_piece:
            if (row, col) in self.highlighted_squares:
                self.move_piece(self.selected_piece, row, col)
                self.clear_highlights()
                self.selected_piece = None
            else:
                self.clear_highlights()
                self.selected_piece = None
        elif self.board[row][col]:
            self.selected_piece = (row, col)
            self.highlight_moves(row, col)

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

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Halma - Part 0 GUI")
    game = Halma(root, board_size=8)
    root.mainloop()