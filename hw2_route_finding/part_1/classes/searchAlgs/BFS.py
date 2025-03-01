
'''
BFS algorithm
'''
class BFS():

    def __init__(self, verbose) -> None:
        self.name = "BFS"
        self.verbose = verbose
        self.parent = self

    def start( self, *, start_node, goal_node ):
        return self._BFS()

    def _BFS( self ):
        pass

    def _BFS_helper(self, graph, current, goal, path,  ):
        pass