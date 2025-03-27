from classes.CONSTANTS import *
from classes.Frontier import Frontier

'''
BFS algorithm
'''
class BFS( Frontier ):

    def __init__(self, verbose, nodeGraph) -> None:
        self.name = BFS_str
        self.verbose = verbose
        self.nodeGraph = nodeGraph

        # initialize helper class
        Frontier.__init__( self, nodeGraph, alg_type=self.name )

    def start(self, start_node, goal_node):

        # initialize variables
        self.insert_end( [start_node] )

        # call bfs
        paths = self._BFS_helper( goal_node )

        # return the pruned path
        return self.bestPath( paths )
        
    def _BFS_helper( self, goal_node ):

        # initialize variables
        path = []
        paths = []
        depth = "-"
        depth = 0

        # Loop until we find the goal or run out of nodes to explore
        while len(self.open) > 0:

            depth += 1

            # pop top of stack
            node = self.open.pop(0)

            # print exploring node 
            if self.verbose:
                print(f"Exploring node: {node.label}")
            
            # add to visited
            self.visited.add( node )
            
            # Add the node to the path
            path.append( node )

            # Check if we reached the goal
            if node.label == goal_node.label:
                # print(f"Success! Found goal node: {goal_node.label}")
                return paths  # Return the path to the goal node

            # not reached, get successors
            successors = self.successors(node, depth)
            self.insert_end(successors)

            # check if this is a prune node
            if self.is_pruneable( successors, goal_node ):
                path.append( goal_node )
                paths.append( path.copy() )

            # display open
            if self.verbose:
                self.showOpen()

        # If no path is found (queue is empty)
        print("Goal not found!")
        return None