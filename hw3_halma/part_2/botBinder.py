from Bot import Bot
from halmaBoardHelper import *

# Attach all methods
Bot.check_win = check_win
Bot.get_all_pieces = get_all_pieces
Bot.get_piece_owner = get_piece_owner
Bot.get_valid_moves = get_valid_moves
Bot.find_jumps = find_jumps
Bot.is_in_bounds = is_in_bounds
Bot.occupied_by = occupied_by
Bot.get_moves_dict = get_moves_dict