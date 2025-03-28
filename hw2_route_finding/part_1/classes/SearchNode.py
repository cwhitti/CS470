from classes.CONSTANTS import *

class SearchNode():

    def __init__(self, *, label, pathcost,  x, 
                                            y ) -> None:
        
        # initialize static variables
        self.label = label
        self.pathcost = pathcost
        self.x = x
        self.y = y

        # set extras
        self.depth = 0   
        self.hSLD = 0 # Best FS cares about this

        # total cost
        self.totalCost = self.pathcost

        # initialize dynamic variables
        self.children = []
    
    def addChild( self, childNode ):
        self.children.append( childNode )
        return True

    def constructBasic( self ):
        return f"{self.label};{self.depth};{self.pathcost};{self.hSLD:.2f};{self.totalCost:.2f}"
    
    def getChildren(self):
        return sorted(self.children, key=lambda node: node.label)
    
    def showBasic( self ):
        return self.constructBasic( )