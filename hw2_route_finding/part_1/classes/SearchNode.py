from classes.CONSTANTS import *
import math 

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
        self.totalCost = 0
        self.heur = self.pathcost

        # initialize dynamic variables
        self.children = []
    
    def addChild( self, childNode ):
        self.children.append( childNode )
        return True

    def constructBasic( self ):
        return f"{self.label};{self.depth};{self.pathcost:.2f} {self.totalCost:.2f};{self.heur:.2f}"
    
    def getChildren(self):
        return sorted(self.children, key=lambda node: node.label)
    
    def showBasic( self ):
        return self.constructBasic( )

    def showChildren( self ):

        print("==========================")
        print(f"Showing children of {self.label}:")
        for childNode in self.children:
            childNode.showBasic()
            print ( f"\t- Heuristic from Parent: { self.hSLD( childNode ) }" )
        print("==========================")