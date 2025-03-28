import graphs
from boggle import *
import random, string, csv

# numerical constants
LOWER_BOUND = 2
UPPER_BOUND = 10
BOARDS = 100

# string constants
CSV_FILE = f"results/results_{LOWER_BOUND}-{UPPER_BOUND}.csv"
DICT_FILE = "twl06.txt"
OUT_FILE = "boards/random_board.txt"
GRAPH_DEST = F"graphs/{LOWER_BOUND}-{UPPER_BOUND}"
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

def main( new_data = False ):

    # initialize variables
    boggle_combos = {}

    # compute boggle combos
    for index in range( LOWER_BOUND, UPPER_BOUND + 1):

        # find combos
        combos = boggleCombinations( index )
        boggle_combos[ index ] =  combos

    # generate new data if we want
    if new_data == True:

        # run the boards
        results = runBoards()

        # put results in CSV
            # function: write_to_csv( CSV_FILE, results )
        writeToCSV( CSV_FILE, results )

    # analyze CSV file
    graphs.graphCurve( CSV_FILE, f"{GRAPH_DEST}/curve-{LOWER_BOUND}-{UPPER_BOUND}.png" )
    graphs.makeTable( CSV_FILE, boggle_combos, f"{GRAPH_DEST}/boggleTable-{LOWER_BOUND}-{UPPER_BOUND}.png")

def runBoards():

    # initialize variables
    sim_num = 0
    results = {}

    # confirmation message
    print(f"Outputting to: {CSV_FILE}")

    # loop through number of boards
    for index in range( UPPER_BOUND - LOWER_BOUND + 1 ):

        # Grab the N
        N = 2 + index

        # run boards of size N
        for sim_board in range( BOARDS ):

            # increment sim num
            sim_num += 1

            # Output to console
            print(f"[{sim_num}] Running board size {N}...")

            # generate a board
                # function: generate_board( N, OUT_FILE )
            generateBoard( N, OUT_FILE )

            # run the board solver
                # function: run_board( OUTFILE, DICT_FILE )
            sim_data = runBoard( OUT_FILE, DICT_FILE )

            # save sim data
            results[ sim_num ] = sim_data

    # return results
    return results


main( new_data = False )