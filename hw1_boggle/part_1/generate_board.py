import random
import string

def generate_boggle_board(size=100):
    """Generates a square Boggle board of the given size."""
    board = [[random.choice(string.ascii_uppercase) for _ in range(size)] for _ in range(size)]
    return board

def print_boggle_board(board):
    """Prints the Boggle board in a formatted way."""
    for row in board:
        print(" ".join(row))

if __name__ == "__main__":
    boggle_board = generate_boggle_board()
    print_boggle_board(boggle_board)