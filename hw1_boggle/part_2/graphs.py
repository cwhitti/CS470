import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def graphCurve( csv_file:str, graph_file:str ):
    '''
    Come up with a curve showing your results.
    '''

    # Load the CSV file
    df = pd.read_csv(csv_file)

    # Ensure relevant columns exist
    if not {'N', 'seconds'}.issubset(df.columns):
        raise ValueError("CSV file must contain 'N' and 'seconds' columns")

    # Aggregate average seconds per board size
    avg_times = df.groupby('N')['seconds'].mean().reset_index()

    # Sort values for plotting
    avg_times = avg_times.sort_values(by='N')

    # Generate X-axis ticks from min to max N with a step of 1
    min_N, max_N = avg_times['N'].min(), avg_times['N'].max()
    x_ticks = np.arange(min_N, max_N + 1, 1)

    # Plot the curve
    plt.figure(figsize=(8, 5))
    plt.plot(avg_times['N'], avg_times['seconds'], marker='o', linestyle='-')

    # Labeling the graph
    plt.xlabel("Board Size (N)")
    plt.ylabel("Average Time to Solve (Seconds)")
    plt.title(f"Boggle Board Solving Time vs. Board Size (n={df.shape[0]})")
    plt.xticks(x_ticks)  # Ensure X-axis increments by 1
    plt.grid(True)

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

def makeTable(csv_file, possibilities, graph_file):

    BOARD_SIZE_STR = "Board Size (N x N)"
    NUM_BOARDS_STR = "# of Boards"
    SOLVE_STR = "Avg. Solving Time (s)"
    AVG_MOVES_STR = "Avg. Moves"
    AVG_VALID_STR = "Avg. Valid Words"
    TOTAL_STR = "Possible Combinations"

    # Load data
    df = pd.read_csv(csv_file)
    
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
    table_data[SOLVE_STR] = table_data[SOLVE_STR].round(4)
    table_data[AVG_VALID_STR] = table_data[AVG_VALID_STR].round(2)
    table_data[AVG_MOVES_STR] = table_data[AVG_MOVES_STR].round(2)
    
    # Format large numbers with commas
    table_data[NUM_BOARDS_STR] = table_data[NUM_BOARDS_STR].apply(lambda x: f"{x:,}")
    #table_data[TOTAL_STR] = table_data[TOTAL_STR].apply(lambda x: f"{int(x):,}")

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis("tight")
    ax.axis("off")
    
    # Create table
    table = ax.table(cellText=table_data.values,
                     colLabels=table_data.columns,
                     cellLoc="center",
                     loc="center")
    
    # Adjust table scaling
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1.2, 1.2)
    
    # Save as image
    plt.savefig(graph_file, bbox_inches="tight", dpi=300)
    plt.close()

if __name__=="__main__":

    #makeTable( "results/results_2-6.csv",  )
    graphTimeComplexity( "results/results_2-6.csv", "graphs/test.png")