'''
BFS algorithm
'''
class BFS():

    def __init__(self, verbose, parent) -> None:
        self.name = "BFS"
        self.verbose = verbose
        self.parent = parent

    def start( self ):
        return self._BFS()

    def _BFS( self ):
        pass

    def _BFS_helper(self, graph, current, goal, path,  ):
        pass