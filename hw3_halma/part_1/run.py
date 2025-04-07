import tkinter as tk
import argparse
from Halma import Halma

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start the Halma game with a specific board file.')
    parser.add_argument('--board', type=str, default=None,
                        help='Path to the board file (default: None')
    args = parser.parse_args()

    root = tk.Tk()
    root.title("Halma - Part 0 GUI")
    game = Halma(root, board_size=8, filename=args.board)
    root.mainloop()
