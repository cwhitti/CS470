from classes.CONSTANTS import *
from classes.Frontier import Frontier
'''
DFS Algorithm
'''
class DFS( Frontier ):

    def __init__(self, verbose, nodeGraph) -> None:
        self.name = DFS_str
        self.verbose = verbose
        self.nodeGraph = nodeGraph

        # initialize helper class
        Frontier.__init__( self, nodeGraph, alg_type=self.name )

    def start( self, start_node, goal_node ):

        # initialize variables
        path = []
        prune_nodes = []

        # add start node to open
        self.open.append( start_node )

        # get path
        path = self._DFS_Helper( start_node, goal_node, 0, path, prune_nodes, )

        return self.prune_path( path, prune_nodes)
    
    def _DFS_Helper(self, node, goal_node, depth, path, prune_nodes=[]):

        # Pop from open list
        self.open.pop( self.open.index(node) )

        # set node depth
        depth = depth + 1
        node.depth = depth

        # Check if already visited
        if node.label in self.visited:
            return None

        # Visit the node
        self.visited.add( node.label )
        print("~" * 100)
        print(f"Exploring node: {node.label}")
        path.append(node)

        # Check if it's the goal node
        if node.label == goal_node.label:
            print("!!! We found the goal node :D !!!")
            return path  # Return the path to the goal

        # Expand children and add to open list
        successors = self.successors( node, depth )
        self.insert_front(successors)  # Add to the front to prioritize deeper search first

        # check if this is a prune node
        if self.is_pruneable( successors, goal_node ):
            prune_nodes.append( node )

        # Debug: Print open list
        if self.verbose:
           self.showOpen()

        # Recursively visit next nodes in the open list
        for child in self.open:
            result = self._DFS_Helper(child, goal_node, depth, path, prune_nodes)
            if result:
                return result  # Goal found
        
        # If no solution is found, backtrack
        path.pop()  # Backtrack by popping the current node
        return None
