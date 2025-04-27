# constants
TIME_LIMIT = 5
RANDOMNESS = 0.5
PLAYERS = 2
CELL_SIZE = 60
PIECE_RADIUS = 20
HIGHLIGHT_COLOR = "#f9f089"
DBG_SIZE = 100
SEP_LINE1 = "=" * DBG_SIZE
AB_PRUNE = True

NONE_MARKER = 'X'
P1_MARKER = '1'
P2_MARKER = '2'


# BOT MODES
BOT_MODE = 0                # Runs bot fully autonomously, simulates its own clicks
RECOMMENDER_MODE = 1        # Runs bot as recommender: takes a look the board recommends best move
HUMAN_MODE = 2              # manual player mode: uses on_click()
