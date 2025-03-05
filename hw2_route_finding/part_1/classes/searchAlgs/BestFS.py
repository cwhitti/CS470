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
        self.insert_front( start_node )

        while len(self.open) > 0:



        
        return None

    def _BestFSHelper(self, graph, start, goal):

        pass