import graphs
from boggle import *
from math import factorial
import random, string, csv

CSV_FILE = "results/results.csv"
DICT_FILE = "twl06.txt"
OUT_FILE = "boards/random_board.txt"
CHARLIST = string.ascii_uppercase


def boggleCombinations( N ):
    # Estimation: Each cell can start a path, with an exponential branching factor.
    # The branching factor is estimated based on available moves.
    avg_branching  =  6
    total_combinations = 0
    total_cells = N * N

    # Sum over all possible word lengths (starting from 2 letters)
    for k in range(2, total_cells + 1):
        total_combinations += total_cells * avg_branching ** k

    return total_combinations


def boggleCombinations(N):
    """Calculate an upper-bound estimate of the number of possible letter sequences on an NxN Boggle board."""
    avg_branching_factor = 6  # Approximate branching factor per step
    total_tiles = N * N  # Total number of tiles
    estimated_sequences = N**2 * (avg_branching_factor ** total_tiles)
    return estimated_sequences

def generateBoard( N:int, filename ):
    
    # open file
    with open( filename, "w" ) as file:

        # loop through N
        for z in range(0,N):

            # create a line
            line = ' '.join(random.choices(CHARLIST,k=N))

            # write to file
            file.write((line+"\n"))

def writeToCSV(filename, results):
    '''
    results: dictionary of board simulations

        KEY: simulation_num
        VALS: A dict of information
            - N
            - time
            - total_words
    '''

    # Open file in write mode
    with open(filename, "w", newline="") as file:

        # ensure proper quoting
        writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL) 

        # Create header
            # Extract keys from first entry 
        header = list(next(iter(results.values())).keys()) 

        # write row 
        writer.writerow(["simulation_num"] + header)

        # Loop through results
        for key, data_dict in results.items():

            # cast as a list?
            row = [key]

            # loop through data_dict
            for value in data_dict.values():

                # Convert lists to strings
                if isinstance(value, list):
                    row.append(";".join(map(str, value)))  # Join lists using semicolons
                
                # otherwise, simply append
                else:
                    row.append(value)
            
            # write row to file
            writer.writerow(row)

def main():

    # initialize variables
    boards = 1000
    results = {}
    boggle_combos = {}
    lower_bound = 2
    upper_bound = 5

    # compute boggle combos
    for index in range( lower_bound, upper_bound + 1):

        # find combos
        combos = boggleCombinations( index )
        boggle_combos[ index ] =  combos

    # loop through number of boards
    for index in range( boards ):

        # make sim num
        sim_num = str(index + 1)

        print(f"[{sim_num}] Running board...")

        # generate a N between upper and lower bounds
        N = random.randint( lower_bound, upper_bound)

        # generate a board
            # function: generate_board( N, OUT_FILE )
        generateBoard( N, OUT_FILE )

        # run the board solver
            # function: run_board( OUTFILE, DICT_FILE )
        sim_data = runBoard( OUT_FILE, DICT_FILE )

        # save sim data
        results[ sim_num ] = sim_data

    # put results in CSV
        # function: write_to_csv( CSV_FILE, results )
    writeToCSV( CSV_FILE, results )

    # analyze CSV file
    graphs.makeTable( CSV_FILE, boggle_combos, "graphs/boggleTable.png")
    graphs.graphTimeComplexity( CSV_FILE, "graphs/timeComplexity.png")

# main()