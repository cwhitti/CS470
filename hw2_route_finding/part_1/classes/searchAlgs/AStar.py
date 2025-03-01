'''
A_Star algorithm
'''
class AStar( ):
    
    def __init__(self, verbose) -> None:
        self.name = "AStar"
        self.verbose = verbose
        self.parent = self

    def start( self, *, start_node, goal_node ):
        return self._AStarHelper()
    
    def _AStarHelper( self ):
        return None