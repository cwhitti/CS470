class SearchNode():

    def __init__(self, *, label, pathcost) -> None:
        self.label = label
        self.pathcost = pathcost
    
    def showBasic( self ):
        print ( (self.label, self.pathcost) )
