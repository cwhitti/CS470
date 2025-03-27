from classes.CONSTANTS import *
from classes.Frontier import Frontier

'''
BestFS
'''
class BestFS( Frontier ):

    def __init__(self, verbose, nodeGraph) -> None:
        self.name = BestFS_str
        self.verbose = verbose
        self.nodeGraph = nodeGraph

        # initialize helper class
        Frontier.__init__( self, nodeGraph, alg_type=self.name )

    def start( self, *, start_node, goal_node ):

        # initialize start node 
        path = []
        depth = 0
        self.insert_front( [start_node] )

        print()

        # loop  through open list
        while len(self.open) > 0:

            # add one to depth 
            depth = depth + 1

            # pop node
            node = self.open.pop(-1)

            # add to visited
            self.visited.add( node )

            # print exploring node
            if self.verbose:
                print(f"Exploring node: {node.label}")

            # check if the goal node
            if node.label == goal_node.label:
                # Add the node to the path
                path.append( node )
                return path
            
            # Add the node to the path
            path.append( node )

            # sort the current open list
            self.orderNodes( self.open, alpha=False, reverse=False)

            # grab successors
            successors = self.successors( node, depth, alpha=True )

            # insert them at the end 
            self.insert_end( successors, alpha=False, reverse=True )

            # show open
            self.showOpen()

        # return the path
        return path