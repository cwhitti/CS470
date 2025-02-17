
from classes.SearchNode import SearchNode
from classes.searchAlgs.AStar import AStar
from classes.searchAlgs.BestFS import BestFS
from classes.searchAlgs.BFS import BFS
from classes.searchAlgs.DFS import DFS

class Algorithm():

    '''
    Init Function
    '''
    def __init__(self, *, alg_type, verbose) -> None:

        # initialize variables
        self.verbose = verbose
        self.parent = self
        self.open = []

        # Nonetype objects
        self.start_letter = None
        self.goal_letter = None
        self.nodeGraph = None
        self.letterGraph = None
        self._alg = None

        # set the algorithm typeverifyNodeExists
        self.setAlgorithm( alg_type )

    '''
    Public Functions
    '''
    def appendChildToParent( self, parentNode, childNode ):

        # ensure parent in graph already and it has a list
        #assert( parentNode.label in self.nodeGraph.keys() and type( self.nodeGraph[parentNode.label] == list) )
        assert( parentNode in self.nodeGraph.keys() and type( self.nodeGraph[parentNode] == list) )

        # append child
        # self.nodeGraph[ parentNode.label ].append( childNode )
        self.nodeGraph[ parentNode ].append( childNode )

        # return true
        return True

    def displayOpen( self ):
        print( f"Open list: {[n.showBasic() for n in self.open]}" )

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
    
    def initializeGoals( self, start_letter, end_letter, graph):

        # set variables
        start_letter = start_letter.upper()
        end_letter   = end_letter.upper()
        
        # assign start and end node!
        self.start_letter = start_letter.upper()
        self.goal_letter = end_letter.upper()

        # initialize graph 
        self.initializeNodeGraph( graph )

        # grab starting node 
        startNode = self.findNode( self.start_letter )

        # insert starting Node
        self.insert_end( [ startNode ] )

    def initializeLetterGraph( self, letterGraph ):
        self.letterGraph = letterGraph
        return self.letterGraph != None
        
    def initializeNode( self, *, label, cost ):
        return SearchNode( label=label, pathcost=cost)
    
    def initializeNodeGraph( self, letterGraph ):

        #initialize variables
        self.initializeLetterGraph( letterGraph )
        self.nodeGraph = {}

        # loop through graph object
        for parentLetter, childrenList in letterGraph.items():

            # create parent node
            parentNode = self.initializeNode(  
                                            label=parentLetter,
                                            cost=0
                                            )
            
            # initialize parentNode in dictionary
            if parentNode not in self.nodeGraph.keys():
                self.nodeGraph[ parentNode ] = []

            # create children nodes
            for childLetter, cost in childrenList.items():

                # create child node
                childNode = self.initializeNode(  
                                                label=childLetter,
                                                cost=cost
                                            )
                
                # put childNode in graph
                self.appendChildToParent( parentNode, childNode )
                
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

    def insert_end( self, unorderedList, saveList=None ):
        
        # define variables
        ignored = []

        # verbose
        if self.verbose:

            # grab child letters
            children = [n.label for n in unorderedList]

            # print verbose
            print(f"Now inserting: {children}\n")

        # insert new list at the end of current list
        for newNode in unorderedList:

            # assert N is an object
            assert( type(newNode) == SearchNode)

            # check for save list
            if saveList != None:

                # insert to saved list
                inserted = self.insertToList( len( saveList ), newNode, saveList )
            
            # otherwise, insert to open
            else:
                inserted = self.insertToList( len( self.open ), newNode, self.open )

            # Try inserting and track ignored nodes
            if not inserted:

                # track ignored nodes
                ignored.append(newNode)

        # return ignored 
        return ignored 

    def insert_front( self, unorderedList, saveList=None ):

        # initialize variables 
        ignored = []

        # verbose
        if self.verbose:

            # grab child letters
            children = [n.label for n in unorderedList]

            # print verbose
            print(f"Now inserting: {children}\n")
        
        # insert new list at the end of current list
        for newNode in unorderedList:

            # assert N is an object
            assert( type(newNode) == SearchNode)
            
            # check for save list
            if saveList != None:

                # insert to saved list
                inserted = self.insertToList( 0, newNode, saveList )
            
            # otherwise, insert to open
            else:
                inserted = self.insertToList( 0, newNode, self.open )

            # Try inserting and track ignored nodes
            if not inserted:

                # track ignored nodes
                ignored.append(newNode)

        # return ignored 
        return ignored 

    def insert_ordered(self, unorderedList, saveList=None):

        # inititalized variables
        ignored = []
        
        # verbose
        if self.verbose:

            # grab child letters
            children = [n.label for n in unorderedList]

            # print verbose
            print(f"Now inserting ordered: {children}\n")
        
        # loop through unordered list 
        for newNode in unorderedList:

            # Reset index for each new node
            index = 0 

            # logic for saveList provided 
            if saveList != None:

                # Find the correct insertion index
                while index < len( saveList ) and saveList[index].label < newNode.label:

                    # incremement index
                    index += 1

                # Try inserting and track ignored nodes
                if not self.insertToList( index, newNode, saveList ):

                    # track ignored nodes
                    ignored.append(newNode)

            # logic for self.open list
            else:

                # Find the correct insertion index
                while index < len( self.open ) and self.open[index].label < newNode.label:

                    # incremement index
                    index += 1

                # Try inserting and track ignored nodes
                if not self.insertToList( index, newNode, self.open ):

                    # track ignored nodes
                    ignored.append(newNode)

        # return ignored
        return ignored
        
    def reset( self ):

        # clear self.open
        self.open.clear()

        # grab starting node 
        startNode = self.findNode( self.start_letter )

        # insert starting Node
        self.insert_end( [ startNode ] )

    def setAlgorithm( self, alg_str:str ):
        '''
        Sets the _alg obhect given a string
        
        Alg Types:
            - DFS: "DFS"
            - BFS: "BFS"
            - AStar: "AStar"
        '''
        # grabs the alg object
        self._alg = self._getAlgorithmObj( alg_str )

        # returns bool if we successfully set it
        return self._alg != None

    def setGraph( self, graph ):
        self.nodeGraph = graph

    def startAlgorithm( self ):

        # checks alg exists
        if self._alg != None:

            # print debug
            if self.verbose:
                print(f"{self.getAlgorithmName()} search from {self.start_node} to {self.end_node}")

            # runs the alg
            return self._alg.start( graph = self.nodeGraph, 
                                    start = self.start_node,
                                    goal  = self.start_node 
                                    )
        # print debug
        if self.verbose:
            print("Algoritm not set")

        # return None
        return None
    
    def successors( self, parentNode:SearchNode ) -> list[SearchNode]:

        # initialize variables
        successors = []

        # check if letter is in graph
        if parentNode != None and parentNode in self.nodeGraph:

            # get list of child data
            childrenList = self.nodeGraph[ parentNode ]

            # insert childrenList to successors 
            self.insert_ordered( childrenList, successors )

        # return successors
        return successors

    '''
    Private Functions
    '''
    def _getAlgorithmObj( self, alg_str ):
        '''
        Gets the corresponding algorithm for the algorithm string

        Alg Types:
            - DFS: "DFS"
            - BestFS: "BestFS"
            - BFS: "BFS"
            - AStar: "AStar"
        '''

        if alg_str == "DFS":
            return DFS( self.verbose )
        
        elif alg_str == "BestFS":
            return BestFS( self.verbose, self )
        
        elif alg_str == "BFS":
            return BFS( self.verbose, self )
        
        elif alg_str == "AStar":
            return AStar( self.verbose, self )
        
        return None