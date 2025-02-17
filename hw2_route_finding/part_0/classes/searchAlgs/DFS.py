'''
DFS Algorithm
'''
class DFS():

    def __init__(self, verbose, parent) -> None:
        self.name = "DFS"
        self.verbose = verbose
        self.parent = parent
    
    def start( self, *, graph, start, goal ):
        return self._DFS_Helper()


    def _DFS_Helper( self ):
        return None