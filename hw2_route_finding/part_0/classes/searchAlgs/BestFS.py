'''
BestFS
'''
class BestFS:

    def __init__(self, verbose, parent) -> None:
        self.name = "BestFS"
        self.verbose = verbose
        self.parent = parent

    def start(self, *, graph, start, goal):

        # run helper
        return self._BestFSHelper(graph, start, goal)

    def _BestFSHelper(self, graph, start, goal):

        pass