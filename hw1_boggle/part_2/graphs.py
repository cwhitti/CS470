import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def graphCurve(csv_file: str, graph_file: str):
    '''
    Generate a curve showing the average solving time per board size with error bars.
    '''

    # Load the CSV file
    df = pd.read_csv(csv_file)

    # Ensure relevant columns exist
    if not {'N', 'seconds'}.issubset(df.columns):
        raise ValueError("CSV file must contain 'N' and 'seconds' columns")

    # Aggregate statistics per board size
    stats = df.groupby('N')['seconds'].agg(['mean', 'std', 'count']).reset_index()

    # Sort values for plotting
    stats = stats.sort_values(by='N')

    # Compute standard error for error bars
    stats['stderr'] = stats['std'] / np.sqrt(stats['count'])

    # Generate X-axis ticks
    min_N, max_N = stats['N'].min(), stats['N'].max()
    x_ticks = np.arange(min_N, max_N + 1, 1)

    # Plot the curve with error bars
    plt.figure(figsize=(8, 5))
    plt.errorbar(stats['N'], stats['mean'], yerr=stats['stderr'], fmt='o-', capsize=5, label="Average Time")

    # Labeling the graph
    plt.xlabel("Board Size (N xN)", fontsize=13)
    plt.ylabel("Solving Time (s)", fontsize=13)
    plt.title(f"Boggle Board Solving Time vs. Board Size (n={df.shape[0]})", fontsize=13.5)
    plt.xticks(x_ticks)
    plt.grid(True)
    plt.legend()

    # Save the graph
    plt.savefig(graph_file)
    
def graphTimeComplexity( csv_file:str, graph_file:str ):
    '''
    Overall plot is a collection of boxplots for each N in CSV file
    For each N, graphs a boxplot of average 'seconds' 

    'Seconds' on X axis, 'N' on Y axis
    '''

    df = pd.read_csv(csv_file)
    
    plt.figure(figsize=(10, 6))
    sns.boxplot(y=df['N'], x=df['seconds'], orient='h', palette='bwr')
    
    plt.xlabel("Time (seconds)", fontsize=14)
    plt.ylabel("Board Size (N x N)", fontsize=14)
    plt.title(f"Time Complexity of Solving Boggle Board (n={df.shape[0]})", fontsize=16)
    
    plt.savefig(graph_file)
    plt.close()

def formatData( df, possibilities ):

    BOARD_SIZE_STR = "  Board Size \n(N x N)"
    NUM_BOARDS_STR = "Number \nof Boards"
    SOLVE_STR = "Average \nSolving Time (s)"
    AVG_MOVES_STR = "Average\nMoves"
    AVG_VALID_STR = "Average\nValid Words"
    TOTAL_STR = "Possible Combinations"
    
    # Aggregate data
    table_data = df.groupby("N").agg(
        Number_of_Boards=("simulation_num", "count"),
        Average_Solving_Time_s=("seconds", "mean"),
        Average_Moves=("moves", "mean"),
        Average_Words_Found=("word_count", "mean"),
    ).reset_index()

    #table_data["Possible_Combinations"] = table_data["N"].map(possibilities)

    # Rename column for readability
    table_data.rename(columns={
                            "N": BOARD_SIZE_STR,
                            "Number_of_Boards": NUM_BOARDS_STR,
                            "Average_Solving_Time_s": SOLVE_STR,
                            "Average_Moves": AVG_MOVES_STR,
                            "Average_Words_Found": AVG_VALID_STR,
    #                        "Possible_Combinations": TOTAL_STR
                            }, 
                            inplace=True)
    
    # Round numeric values for readability
    table_data[SOLVE_STR] = table_data[SOLVE_STR].round(2)
    table_data[AVG_VALID_STR] = table_data[AVG_VALID_STR].round(2)
    table_data[AVG_MOVES_STR] = table_data[AVG_MOVES_STR].round(2)
    
    # Format large numbers with commas
    table_data[NUM_BOARDS_STR] = table_data[NUM_BOARDS_STR].apply(lambda x: f"{x:,}")
    table_data[AVG_MOVES_STR] = table_data[AVG_MOVES_STR].apply(lambda x: f"{int(x):,}")
    table_data[AVG_VALID_STR] = table_data[AVG_VALID_STR].apply(lambda x: f"{int(x):,}")

    return table_data


def makeTable(csv_file, possibilities, graph_file):

    # Load data
    df = pd.read_csv(csv_file)

    # format the data
    table_data = formatData( df, possibilities )

    # Create figure
    fig, ax = plt.subplots(figsize=(4.6, 2.6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, len(table_data) + 2)
    ax.axis("off")
    
    # Define colors for alternating rows and headers
    colors = ["#FFFFFF", "#f0f0f0"]
    header_color = "#dbdbdb"

    NUM1 = 1
    NUM2 = 1.2
    
    # Draw alternating row colors
    for i in range(len(table_data)):
        ax.add_patch(patches.Rectangle((0, i), NUM1, NUM2, color=colors[i % 2]))
    
    # Draw header background
    ax.add_patch(patches.Rectangle((0, len(table_data)), NUM1, NUM2, color=header_color))
    
    shift_text_h = 0.09
    shift_text_v = 0.5
    # Draw table text
    for i, row in table_data.iterrows():
        for j, text in enumerate(row):
            #ax.text(j / len(table_data.columns) + 0.05, len(table_data) - i - 0.5, str(text),
            ax.text(j / len(table_data.columns) + shift_text_h, len(table_data) - i - shift_text_v, str(text),
                    va='center', 
                    ha='center', 
                    fontsize=6)
    
    # Draw header with bold text
    for j, header in enumerate(table_data.columns):
        ax.text(j / len(table_data.columns) + shift_text_h, len(table_data) + shift_text_v + 0.05, header,
                va='center', 
                ha='center', 
                fontsize=5.5, 
                fontweight='bold'
                )
    
    # Save the table as an image
    plt.savefig(graph_file, bbox_inches="tight", dpi=300)
    plt.close()

if __name__=="__main__":

    #makeTable( "results/results_2-6.csv",  )
    graphTimeComplexity( "results/results_2-6.csv", "graphs/test.png")