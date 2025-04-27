import tkinter as tk
import argparse
from Player import Player
from Bot import Bot
from Halma import Halma
from standardConstants import *
import halmaBoardBinder
import botBinder
from lists.colors import colors
import boardGenerator

BOARD_SIZE = 8

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start the Halma game with a specific board file.')
    parser.add_argument('--board', type=str, default=None,
                        help='Path to the board file (default: None')

    parser.add_argument('--boardgen', action='store_true',
                        help='Generate a random board (no input needed)')
    args = parser.parse_args()

    if args.boardgen:
        filename = boardGenerator.generate_board( board_size=BOARD_SIZE)

    elif args.board:
        filename = args.board
    
    else:
        filename = None

    root = tk.Tk()

    # bot = Player(
    #     name="Luke",
    #     colorName="Red",
    #     mainColor=colors["red"][0], # main color
    #     homeColor=colors["red"][1],  # home color
    #     # mode=BOT_MODE,
    #     mode=BOT_MODE,
    # )

    # me = Player(
    #     name="Claire",
    #     colorName="Blue",
    #     mainColor=colors["blue"][0], # main color
    #     homeColor=colors["blue"][1],  # home color
    #     # mode=RECOMMENDER_MODE,
    #     mode=,
    # )

    playerList = [ ]
    root.title("Halma - Part 0 GUI")
    game = Halma(root, board_size=BOARD_SIZE, filename=filename, playerDict=playerList)
    root.mainloop()
