import math
from classes.CONSTANTS import *
from classes.SearchNode import SearchNode

class Frontier():

    def __init__(self, nodeGraph, alg_type="Basic") -> None:
        self.open = []
        self.visited = set()
        self.nodeGraph = nodeGraph 
        self.careCost = False

        # see if we care about cost
        if alg_type in [ASTAR_str]:
            self.careCost = True

    def bestPath( self, paths ):

        index = 1


        if self.verbose:
            for path in paths:

                print(f"Path #{index}: {[elm.label for elm in path]}")

        return paths[0]
    
    def showOpen( self ):
        print("Open list: ", end = "")

        print( [elm.showBasic() for elm in self.open] )

    def findNode( self, label ):
        
        # initialize variables
        keys      = list( self.nodeGraph.keys() )
        index     = 0
        foundNode = None
        
        # loop through parentNode in self.nodeGraph
        while index < len( keys ) and label != keys[index].label:

            # increment index
            index += 1

        # set key if label != keys[index].label
        if label == keys[index].label:
            foundNode = keys[index]

        # return foundNode
        return foundNode
    
    def inListLabel( self, label, list ):
        labels = [node.label for node in list]
        return label in labels

    def insertToList( self, index:int, node:SearchNode, saveList:list ):
        
        # initialize variables 
        inserted = False 

        # check not in open already
        if not self.inListLabel( node.label, saveList ) and node.label not in self.visited:

            # insert
            saveList.insert( index, node )

            # change bool
            inserted = True

        # return inserted
        return inserted

    def insertToListMultiple( self, unorderedList:list, officialList, index = None, localVerbose=False, alpha=True, reverse=True ):

        # initialize variables
        ignored = []
        added = []

        # pluck out ignored
        for node in unorderedList:

            # assert N is an object
            assert( type(node) == SearchNode)

            # check if node has been visited
            if node not in self.visited:

                # check if node is in the actual list
                if self.inListLabel( node.label, officialList ):

                    # if so, pop it
                    officialList.pop( officialList.index( node ) )

                # append to added
                added.append( node )
                    
            # ignore it if esle
            else:
                ignored.append( node )
        
        # sort added list 
        added = self.orderNodes( added, alpha, reverse )

        # extend list
        officialList[index:index] = added

        # extend high priority

        # verbose
        if self.verbose and localVerbose:

            # grab child letters
            children = [n.label for n in added]

            # print verbose
            print(f"inserting new children: {children}")

        # return ignored
        return ignored
    
    def insert_end( self, unorderedList:list, saveList=None, alpha=True, reverse=True ):

        # throw in save list
        if saveList != None:

            # define variables
            insert_index = len( saveList )

            # grab ignored
            ignored = self.insertToListMultiple( unorderedList, saveList, index=insert_index, 
                                                            alpha=alpha, reverse=reverse)
        
        # throw in open list
        else:

            # define variables
            insert_index = len( self.open )
            
            # grab ignored
            ignored = self.insertToListMultiple( unorderedList, self.open, index=insert_index, 
                                                            alpha=alpha, reverse=reverse )

        # return ignored 
        return ignored 

    def insert_front( self, unorderedList:list, saveList=None, alpha=True, reverse=True ):

        # initialize variables 
        insert_index = 0

        # throw in save list
        if saveList != None:

            # grab ignored
            ignored = self.insertToListMultiple( unorderedList, saveList, index=insert_index, 
                                                                alpha=alpha, reverse=reverse )
        
        # throw in open list
        else:
            
            # grab ignored
            ignored = self.insertToListMultiple( unorderedList, self.open, index=insert_index, 
                                                                alpha=alpha, reverse=reverse )

        # return ignored 
        return ignored 

    def insert_ordered(self, unorderedList:list, saveList=None, alpha=True, localVerbose=False, reverse=True ):

        # inititalized variables
        insert_index = 0

        # order the list 
        ordered_list = self.orderNodes( unorderedList, alpha=alpha, reverse=reverse)

        # throw in save list
        if saveList != None:

            # grab ignored
            ignored = self.insertToListMultiple( ordered_list, saveList, index=insert_index, localVerbose=localVerbose, 
                                                                                                alpha=alpha, reverse=reverse )
        
        # throw in open list
        else:
            
            # grab ignored
            ignored = self.insertToListMultiple( ordered_list, self.open, index=insert_index, localVerbose=localVerbose, 
                                                                                                alpha=alpha, reverse=reverse)

        # return ignored
        return ignored
    
    def is_pruneable( self, successors, goal_node):
        return goal_node.label in [child.label for child in successors]
        
    def orderNodes( self, unorderedList:list, alpha=True, reverse=True ):

        # initialize variables 

        # print(f"Alpha: {alpha}, Reversing: {reverse}")

        # order by letter for now
        if alpha:
            unorderedList.sort(key=lambda node: node.label)

        # order by heuristics
        else:
            unorderedList.sort(key=lambda node: node.totalCost, reverse=reverse)

        # print(f"Ordiering by alpha: {alpha}: {[elm.showBasic() for elm in unorderedList]}")

        # return ordered nodes
        return unorderedList
        
    def successors( self, parentNode:SearchNode, depth=None, alpha=True, reverse=True ) -> list[SearchNode]:

        # initialize variables
        nodes = []
        successors = []

        # print(f"Alpha: {alpha}, Reversing: {reverse}")

        # check if letter is in graph
        if parentNode != None and parentNode in self.nodeGraph:

            # get list of child data
            childrenList = self.nodeGraph[ parentNode ]

            # loop through children list
            for child in childrenList:

                # find the node
                foundNode = self.findNode( child.label )

                # copy everything over. sigh.
                # if not self.careCost:
                foundNode.pathcost = child.pathcost
                foundNode.hSLD = child.hSLD
                # foundNode.totalCost = child.hSLD
                foundNode.totalCost =  child.totalCost + parentNode.totalCost
                foundNode.depth = depth
                    
                # append the node
                if foundNode.label not in self.visited and foundNode.label not in [elm.label for elm in self.open]:
                    nodes.append( foundNode )

            # insert childrenList to successors 
            self.insert_ordered( nodes, successors, alpha=alpha, localVerbose=True, reverse=reverse )

        # return successors
        return successors

    def hSLD(self, node1, node2):

        # Calculate the heuristic straight line distance (Euclidean distance)
        x1, y1 = node1.x, node1.y
        x2, y2 = node2.x, node2.y
        return float(round( math.sqrt((x1 - x2)**2 + (y1 - y2)**2), 2 ))