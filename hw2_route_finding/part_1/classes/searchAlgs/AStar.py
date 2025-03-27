from classes.CONSTANTS import *
from classes.Frontier import Frontier

'''
AStar
'''
class AStar( Frontier ):

    def __init__(self, verbose, nodeGraph) -> None:
        self.name = ASTAR_str
        self.verbose = verbose
        self.nodeGraph = nodeGraph

        # initialize helper class
        Frontier.__init__( self, nodeGraph, alg_type=self.name )

    def start(self, *, start_node, goal_node):
        # Initialize start node 
        depth = 0
        path = []
        # start_node.totalCost = 0

        self.insert_front([start_node], reverse=False)

        print()

        # Loop through open list
        while len(self.open) > 0:

            # increment depth
            depth += 1

            # Pop node with the lowest total cost
            node = self.open.pop(0)

            # Add to visited
            self.visited.add(node)

            if self.verbose:
                print(f"Exploring node: {node.label}")

            # Check if goal reached
            if node.label == goal_node.label:
                
                path.append(node)
                return path  # Return path to goal
            
            # Add the node to the path
            path.append(node)

            # Generate successors
            successors = self.successors(node, depth, alpha=True, reverse=False)

            # Update pathcost and totalCost for each successor
            for successor in successors:
                successor.pathcost = node.pathcost + successor.pathcost  # accumulate g(n)
                successor.totalCost = successor.pathcost + successor.hSLD  # update f(n)

            # Insert successors 
            self.insert_end(successors, alpha=False, reverse=False)

            # force the list to be ordered
            self.orderNodes(self.open, alpha=False, reverse=False)

            # Show open list
            self.showOpen()

        # return the path
        return path  
