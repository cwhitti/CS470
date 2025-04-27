import tkinter as tk
from tkinter import messagebox
import random
from scoreHelper import *
from playersHelper import *
from standardConstants import *
from Player import Player
from Piece import Piece
import time

# halma class
class Halma( ):

    # init
    def __init__(self, root, board_size=8, playerDict=[], filename=None):

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
        self.accepting_clicks = False
        self.home_squares = {}
        self.pieces = {}
        self.highlighted_squares = []
        self.bolded_pieces = []

        # initialize the board
        self.initialize_board( filename )

        # Set up players
        self.players, self.bot_count = initialize_players(playerDict)
        self.player1 = self.players[0]
        self.player2 = self.players[1]

        # set the current player
        self.set_current_player()
            
        # setup visuals
        self._setup_visuals()
        self.display_players()

        # Mouse click binding
        # if self.player1.mode != BOT_MODE or self.player2.mode != BOT_MODE:
        self.canvas.bind("<Button-1>", self.on_click)

        # Sanity check
        assert self.board is not None

        # Set up board
        self.display_players()

        # set up extra cogs
        self.root.after(0, self.on_start)

        # start the first turn
        self.start_turn()

    def clicks_enable( self ):
        self.accepting_clicks = True
    
    def clicks_disable( self ):
        self.accepting_clicks = False

    def display_players(self):

        print(f"Playing with {len(self.players)} players, {self.bot_count} bots\n")

        for player in self.players:
            player.display()

    def on_click(self, event):

        # get row and col
        row = event.y // CELL_SIZE
        col = event.x // CELL_SIZE

        # disregard if not accepting clicks
        if not self.accepting_clicks:
            return

        # if a piece has been selected
        if self.selected_piece:

            # and is being moved to a highlighted space
            if (row, col) in self.highlighted_squares:

                # clear all bolds 
                self.clear_bolds()

                # move it
                self.move_piece(self.selected_piece, row, col)

                # clear all highlights
                self.clear_highlights()

                # reset selected piece
                self.selected_piece = None

                # end the turn
                self.end_turn()

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
            self.get_valid_moves(row, col, highlight=True)

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

        self.player1.score = calculate_score( self.board, self.player1, self.player2 )
        self.player2.score = calculate_score( self.board, self.player2, self.player1 )
        self.update_scores()

        if self.check_win(self.current_player, self.opponent) or self.check_win( self.opponent, self.current_player):
            self.end_game()

    def run_bot_move( self, player ):

        # SLEEP FIRST
        selectedPiece, bestMove = player.minimax_search( board=self.board, opponent=self.opponent, max_player=player.order%2 )

        # grab row, col to move
        (from_pos) = selectedPiece.get_coords( board=self.board )
        (bestRow, bestCol) = bestMove

        # move it
        self.move_piece(from_pos, bestRow, bestCol)

        # clear all highlights
        self.clear_highlights()

        # end the turn
        self.end_turn()

    def show_bot_recommendation( self, player ):

        # initialize variables
            # None

        # I need to implement a minmax algorithm here, which is probably a method in the Bot class
        selectedPiece, bestMove = player.minimax_search( board=self.board, opponent=self.opponent, max_player=player.order%2 )

        # grab row, col to move
        # selectedRow, selectedCol = selectedPiece.get_coords( board=self.board )
        (bestRow, bestCol) = bestMove

        # print the recommended move
        print(f"Recommended move: {selectedPiece.canvasPiece} -> ({bestRow}, {bestCol})" )

    def start_turn(self):

        # grab the player
        player = self.current_player

        # debug
        print(f"Beginning {player.name}'s turn.")
        
        # if it's a bot...
        if player.mode == BOT_MODE:

            # run the bot
            self.run_bot_move( player=player )

        # otherwise, it's a human!
        else:

            # enable clicks
            self.clicks_enable()

            # show recommended move
            if player.mode == RECOMMENDER_MODE:

                # recommend for the player
                self.show_bot_recommendation( player=player )
        

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

    def _add_grid_labels(self):
        # Label columns (top side)
        for col in range(self.board_size):
            x = col * CELL_SIZE + CELL_SIZE / 2
            self.canvas.create_text(
                x, 
                -CELL_SIZE / 2,  # Slightly above the top row
                text=str(col), 
                font=("Arial", 12),
                anchor='center'
            )
            
        # Label rows (left side)
        for row in range(self.board_size):
            y = row * CELL_SIZE + CELL_SIZE / 2
            self.canvas.create_text(
                -CELL_SIZE / 2, 
                y,
                text=str(row), 
                font=("Arial", 12),
                anchor='center'
            )

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
        self._add_grid_labels()
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