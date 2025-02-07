import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def graphTimeComplexity( csv_file:str, graph_file:str ):
    '''
    Overall plot is a collection of boxplots for each N in CSV file
    For each N, graphs a boxplot of average 'seconds' 

    'Seconds' on X axis, 'N' on Y axis

    Parameters:
        - csv_file: filename for existing csv file
        - graph_file: filename for output graphic

    CSV file contains:
        - simulation_num : The unique simulation number
        - N	             : integer representing NxN board
        - seconds	     : integer representing seconds to solve boggle board
        - word_count	 : number of words found in boggle board
        - word_list      : list of words found in boggle board
        - hamiltonian_paths : number of hamiltonian paths for this NxN board
    '''

    df = pd.read_csv(csv_file)
    
    plt.figure(figsize=(10, 6))
    sns.boxplot(y=df['N'], x=df['seconds'], orient='h', palette='coolwarm')
    
    plt.xlabel("Time (seconds)")
    plt.ylabel("Board Size (N x N)")
    plt.title("Time Complexity of Solving Boggle Board")
    
    plt.savefig(graph_file)
    plt.close()

def makeTable(csv_file, possibilities, graph_file):
    # Load data
    df = pd.read_csv(csv_file)
    
    # Aggregate data
    table_data = df.groupby("N").agg(
        Number_of_Boards=("simulation_num", "count"),
        Average_Solving_Time_s=("seconds", "mean"),
        Average_Words_Found=("word_count", "mean"),
        #Possible_Combinations=("possible_combos", "first")  # Taking first as a representative value
    ).reset_index()

    table_data["Possible_Combinations"] = table_data["N"].map(possibilities)

    # Rename column for readability
    table_data.rename(columns={
                            "N": "Board Size (N x N)",
                            "Number_of_Boards": "# of Boards",
                            "Average_Solving_Time_s": "Avg. Solving Time (s)",
                            "Average_Words_Found":"Avg. Words Found",
                            "Possible_Combinations":"Possible Combinations"
                            }, 
                            inplace=True)
    
    # Round numeric values for readability
    table_data["Avg. Solving Time (s)"] = table_data["Avg. Solving Time (s)"].round(4)
    table_data["Avg. Words Found"] = table_data["Avg. Words Found"].round(2)
    
    # Format large numbers with commas
    table_data["# of Boards"] = table_data["# of Boards"].apply(lambda x: f"{x:,}")
    table_data["Possible Combinations"] = table_data["Possible Combinations"].apply(lambda x: f"{int(x):,}")

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
    table.set_fontsize(6.5)
    table.scale(1.2, 1.2)
    
    # Save as image
    plt.savefig(graph_file, bbox_inches="tight", dpi=300)
    plt.close()
