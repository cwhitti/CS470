import tkinter as tk
import argparse
from Player import Player
from Bot import Bot
from Halma import Halma
from standardConstants import *
import halmaBoardBinder
import botBinder
from lists.colors import colors

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start the Halma game with a specific board file.')
    parser.add_argument('--board', type=str, default=None,
                        help='Path to the board file (default: None')
    args = parser.parse_args()

    root = tk.Tk()

    bot = Player(
        name="Luke",
        colorName="Red",
        mainColor=colors["red"][0], # main color
        homeColor=colors["red"][1],  # home color
        # mode=BOT_MODE,
        mode=BOT_MODE,
    )

    me = Player(
        name="Claire",
        colorName="Blue",
        mainColor=colors["blue"][0], # main color
        homeColor=colors["blue"][1],  # home color
        # mode=RECOMMENDER_MODE,
        mode=BOT_MODE,
    )

    playerList = [ me, bot ]
    root.title("Halma - Part 0 GUI")
    game = Halma(root, board_size=8, filename=args.board, playerDict=playerList)
    root.mainloop()
