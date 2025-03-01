import math 

class SearchNode():

    def __init__(self, *, label, pathcost,  x, 
                                            y ) -> None:
        
        # initialize static variables
        self.label = label
        self.pathcost = pathcost
        self.x = x
        self.y = y

        # initialize dynamic variables
        self.children = []
    
    def addChild( self, childNode ):
        self.children.append( childNode )
        return True
    
    def getChildren(self):
        return sorted(self.children, key=lambda node: node.label)
    
    def showBasic( self ):
        print ( f"\nLabel: { self.label}" )
        print ( f"\t- Position: {self.x}, {self.y}" )
        print ( f"\t- Cost from Parent: {self.pathcost}" )
        return ( (self.label, self.pathcost) )

    def showChildren( self ):

        print("==========================")
        print(f"Showing children of {self.label}:")
        for childNode in self.children:
            childNode.showBasic()
            print ( f"\t- Heuristic from Parent: { self.hSLD( childNode ) }" )
        print("==========================")
    
    def hSLD(self, compNode):

        # Calculate the heuristic straight line distance (Euclidean distance)
        x1, y1 = self.x, self.y
        x2, y2 = compNode.x, compNode.y
        return round( math.sqrt((x1 - x2)**2 + (y1 - y2)**2), 4 )