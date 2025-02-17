import math

def hSLD(letter, searcher):

    filename = searcher.filename

    node_positions = {}

    with open(filename, "r") as file:
        for line in file:
            data = eval(line.strip())  # Convert string tuple to actual tuple
            node1, node2, _, coord1, coord2 = data
            
            # Store coordinates if the node is encountered
            if node1 not in node_positions:
                node_positions[node1] = coord1
            if node2 not in node_positions:
                node_positions[node2] = coord2

    if letter not in node_positions:
        raise ValueError(f"Node {letter} not found in the file.")

    # Calculate Euclidean distance from the node to all other nodes
    x1, y1 = node_positions[letter]
    distances = {
        other: round(math.sqrt((x1 - x2)**2 + (y1 - y2)**2), 4)
        for other, (x2, y2) in node_positions.items() if other != letter
    }

    printPretty(letter,  distances )

def printPretty(letter, distances):

    print("\n" + "*" * 100)
    print()
    print(f"Origin: {letter}  ")
    print()
    print("----------------")
    print("Node  | Distance")
    print("----------------")
    for node, distance in sorted(distances.items(), key=lambda x: x[1]):  # Sort by distance
        print(f"{node:<5} | {distance:.4f}")