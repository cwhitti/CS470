from classes.SearchNode import SearchNode

class Frontier():

    def __init__(self, nodeGraph) -> None:
        self.open = []
        self.visited = set()
        self.nodeGraph = nodeGraph 

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

    def insertToList( self, index, node, saveList ):
        
        # initialize variables 
        inserted = False 

        # check not in open already
        if not self.inListLabel( node.label, saveList ):

            # insert
            saveList.insert( index, node )

            # change bool
            inserted = True

        # return inserted
        return inserted

    def insertToListMultiple( self, unorderedList, officialList, index = None, localVerbose=False ):

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

                # move it to "added"
                added.append( node )
                    
            # ignore it if esle
            else:
                ignored.append( node )
        
        # sort added list 
        added = self.orderNodes( added )

        # extend list
        officialList[index:index] = added

        # verbose
        if self.verbose and localVerbose:

            # grab child letters
            children = [n.label for n in added]

            # print verbose
            print(f"inserting new children: {children}")

        # return ignored
        return ignored
    
    def insert_end( self, unorderedList, saveList=None ):

        # throw in save list
        if saveList != None:

            # define variables
            insert_index = len( saveList )

            # grab ignored
            ignored = self.insertToListMultiple( unorderedList, saveList, index=insert_index )
        
        # throw in open list
        else:

            # define variables
            insert_index = len( self.open )
            
            # grab ignored
            ignored = self.insertToListMultiple( unorderedList, self.open, index=insert_index )

        # return ignored 
        return ignored 

    def insert_front( self, unorderedList, saveList=None ):

        # initialize variables 
        insert_index = 0

        # throw in save list
        if saveList != None:

            # grab ignored
            ignored = self.insertToListMultiple( unorderedList, saveList, index=insert_index )
        
        # throw in open list
        else:
            
            # grab ignored
            ignored = self.insertToListMultiple( unorderedList, self.open, index=insert_index )

        # return ignored 
        return ignored 

    def insert_ordered(self, unorderedList, saveList=None, alpha=True, localVerbose=False ):

        # inititalized variables
        insert_index = 0

        # order the list 
        ordered_list = self.orderNodes( unorderedList, alpha=alpha)

        # throw in save list
        if saveList != None:

            # grab ignored
            ignored = self.insertToListMultiple( ordered_list, saveList, index=insert_index, localVerbose=localVerbose )
        
        # throw in open list
        else:
            
            # grab ignored
            ignored = self.insertToListMultiple( ordered_list, self.open, index=insert_index, localVerbose=localVerbose)

        # return ignored
        return ignored
    

    def prune_path( self, path, prune_nodes ):

        print("\n" + "+" * 100)
        print("ATTEMPTING TO PRUNE")

        # initialize indexes
        best_index = 1000000000

        # turn path to letters
        letter_path = [ node.label for node in path]

        # loop through all valud prune nodes
        for node in prune_nodes:

            # get the index of the pruned node
            index = letter_path.index( node.label )

            assert( index < best_index )

            # if its the shortest terminal letter
            if index < best_index:

                # reassign best index
                best_index = index
            
        print(f"Best letter to prune on: {letter_path[best_index]} - index {best_index}")
        
        # cut down the path
        best_path = path[ 0:best_index + 1 ] + [path[-1]]
        print("+" * 100 + "\n")

        # return best path
        return best_path

        
    def orderNodes( self, unorderedList, alpha=True ):

        # initialize variables 

        # order by letter for now
        if alpha:
            unorderedList.sort(key=lambda node: node.label)

        # TODO: implement by heuristics

        # return ordered nodes
        return unorderedList
        
    def successors( self, parentNode:SearchNode ) -> list[SearchNode]:

        # initialize variables
        nodes = []
        successors = []

        # check if letter is in graph
        if parentNode != None and parentNode in self.nodeGraph:

            # get list of child data
            childrenList = self.nodeGraph[ parentNode ]

            # loop through children list
            for child in childrenList:

                # find the node
                foundNode = self.findNode( child.label )
                nodes.append( foundNode )

            # insert childrenList to successors 
            self.insert_ordered( nodes, successors, alpha=True, localVerbose=True )

        # return successors
        return successors

