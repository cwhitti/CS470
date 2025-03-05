from classes.CONSTANTS import *
from classes.Frontier import Frontier
'''
A_Star algorithm
'''
class AStar( ):
    
    def __init__(self, verbose) -> None:
        self.name = "AStar"
        self.verbose = verbose
        self.parent = self

        Frontier.__init__( self, nodeGraph={}, alg_type=self.name)

    def start( self, *, start_node, goal_node ):
        return self._AStarHelper()
    
    def _AStarHelper( self ):
        return None