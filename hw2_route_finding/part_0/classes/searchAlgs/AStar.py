'''
A_Star algorithm
'''
class AStar( ):
    
    def __init__(self, verbose, parent) -> None:
        self.name = "AStar"
        self.verbose = verbose
        self.parent = parent

    def start( self, *, graph, start, goal ):
        return self._AStarHelper()
    
    def _AStarHelper( self ):
        return None