import os
import random
import string

def generate_string( adjectives, nouns ):
    
    # Choose one random adjective and noun
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    
    # Combine them into <adjectiveNoun> format
    combination = f"{adjective.capitalize()}{noun.capitalize()}"
    return combination

def random_placement(numPieces, boardSize, placed):
    nums = list(range(boardSize))
    placement = set()

    while len(placement) < numPieces:
        row = random.choice(nums)
        col = random.choice(nums)

        if (row, col) not in placed:
            placement.add((row, col))
    
    return list(placement)


def generate_board(board_size=8):

    placed = set()
    board=[]

    # Make sure generated_boards/ exists
    os.makedirs("generated_boards", exist_ok=True)

    # Read adjectives
    with open("lists/adjectives.txt", "r") as f:
        adjectives = [line.strip() for line in f if line.strip()]
    
    # Read nouns
    with open("lists/nouns.txt", "r") as f:
        nouns = [line.strip() for line in f if line.strip()]

    # Choose 1 or 2 randomly
    game_type = random.choice([1, 2])

    # How many pieces to place in each corner depends on board size
    # We'll do the standard triangle for Halma pieces:
    player1_pieces = random_placement( 10, board_size, placed )
    placed = player1_pieces
    player2_pieces = random_placement( 10, board_size, placed )

    for row in range(board_size):

        newRow = []

        for col in range(board_size):

            if (row, col) in player1_pieces:
                newRow.append("1")
            
            elif (row, col) in player2_pieces:
                newRow.append("2")

            else:
                newRow.append("X")

        board.append( newRow )


    # Now create a random silly filename
    filename = "board_" + generate_string( adjectives, nouns ) + ".txt"
    filepath = os.path.join("generated_boards", filename)

    # Write to the file
    with open(filepath, "w") as f:
        f.write(f"{game_type}\n\n")
        for row in board:
            f.write(" ".join(row) + "\n")

    print(f"Generated board saved as {filepath}")
    return filepath

if __name__ == "__main__":

    for i in range(100):
        generate_board()