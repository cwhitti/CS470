from Halma import Halma
from halmaBoardHelper import *

# Attach all methods
Halma.add_home = add_home
Halma.add_highlight = add_highlight
Halma.add_piece = add_piece
Halma.bold_piece = bold_piece
Halma.clear_bolds = clear_bolds
Halma.clear_highlights = clear_highlights
Halma.create_piece = create_piece
Halma.check_win = check_win
Halma.draw_grid = draw_grid
Halma.end_game = end_game
Halma.end_turn = end_turn
Halma.find_jumps = find_jumps
Halma.is_in_bounds = is_in_bounds
Halma.initialize_board_from_file = initialize_board_from_file
Halma.initialize_empty_board = initialize_empty_board
Halma.initialize_board = initialize_board
Halma.get_all_pieces = get_all_pieces
Halma.get_moves_dict = get_moves_dict
Halma.get_piece_owner = get_piece_owner
Halma.get_valid_moves = get_valid_moves
Halma.move_piece = move_piece
Halma.occupied_by = occupied_by
Halma.place_initial_pieces = place_initial_pieces
Halma.set_homes = set_homes
Halma.set_current_player = set_current_player
Halma.update_scores = update_scores
