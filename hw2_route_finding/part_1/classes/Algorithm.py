
from classes.Frontier import Frontier
from classes.searchAlgs.BFS import BFS
from classes.searchAlgs.DFS import DFS
from classes.SearchNode import SearchNode
from classes.searchAlgs.AStar import AStar
from classes.searchAlgs.BestFS import BestFS

class Algorithm( Frontier ):

    '''
    Init Function
    '''
    def __init__(self, *, alg_type, verbose) -> None:

        # initialize variables
        self.verbose = verbose
        self.parent = self

        # Nonetype objects
        self.start_letter = None
        self.goal_letter = None
        self.nodeGraph = None
        self.letterGraph = None
        self._alg = None

        # set the algorithm type
        assert ( self.setAlgorithm( alg_type ) == True )


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
        parentNode.addChild( childNode )

        # return true
        return True

    # def findNode( self, label ):
        
    #     # initialize variables
    #     keys      = list( self.nodeGraph.keys() )
    #     index     = 0
    #     foundNode = None
        
    #     # loop through parentNode in self.nodeGraph
    #     while index < len( keys ) and label != keys[index].label:

    #         # increment index
    #         index += 1

    #     # set key if label != keys[index].label
    #     if label == keys[index].label:
    #         foundNode = keys[index]

    #     # return foundNode
    #     return foundNode
    
    def initializeGoals( self, start_letter, end_letter, graph):

        # set variables
        start_letter = start_letter.upper()
        end_letter   = end_letter.upper()
        
        # assign start and end node!
        self.start_letter = start_letter.upper()
        self.goal_letter = end_letter.upper()

        # initialize graph and helper module
        self.initializeNodeGraph( graph )

        # print( len( self.nodeGraph))
        self.updateAlgNodeGraph()
        Frontier.__init__( self, self.nodeGraph )

        # grab starting node 
        startNode = self.findNode( self.start_letter )

        # insert starting Node
        self.insert_end( [ startNode ] )

    def initializeLetterGraph( self, letterGraph ):
        self.letterGraph = letterGraph
        return self.letterGraph != None
        
    def initializeNode( self, *, label, pathcost, x, y ):
        return SearchNode( label=label, pathcost=pathcost, x=x, y=y)
    
    def initializeNodeGraph( self, letterGraph ):

        #initialize variables
        self.initializeLetterGraph( letterGraph )
        ignore = [".POS"]
        self.nodeGraph = {}
        rememberNodes = {}
        
        # loop through graph object
        for parentLetter, childrenList in letterGraph.items():

            # get coords 
            x, y = childrenList[".POS"]

            # create parent node
            parentNode = self.initializeNode(  
                                            label=parentLetter,
                                            pathcost=0,
                                            x=x,
                                            y=y
                                            )
            
            # add to remember nodes
            rememberNodes[ parentLetter ] = parentNode 

            # initialize parentNode in dictionary
            if parentNode not in self.nodeGraph.keys():
                self.nodeGraph[ parentNode ] = []

            # create children nodes
            for childLetter, childInfo in childrenList.items():

                # ignore .POS element
                if childLetter in ignore:
                    continue

                # grab info
                cost, (x, y) = childInfo

                # create child node
                childNode = self.initializeNode(  
                                                label=childLetter,
                                                pathcost=cost,
                                                x=x,
                                                y=y
                                            )

                
                # put childNode in graph
                self.appendChildToParent( parentNode, childNode )
                
    # def inListLabel( self, label, list ):
    #     labels = [node.label for node in list]
    #     return label in labels
    
    # def insertToList( self, index, node, saveList ):
        
    #     # initialize variables 
    #     inserted = False 

    #     # check not in open already
    #     if not self.inListLabel( node.label, saveList ):

    #         # insert
    #         saveList.insert( index, node )

    #         # change bool
    #         inserted = True

    #     # return inserted
    #     return inserted

    # def insert_end( self, unorderedList, saveList=None ):
        
    #     # define variables
    #     ignored = []

    #     # verbose
    #     if self.verbose:

    #         # grab child letters
    #         children = [n.label for n in unorderedList]

    #         # print verbose
    #         print(f"Now inserting: {children}\n")

    #     # insert new list at the end of current list
    #     for newNode in unorderedList:

    #         # assert N is an object
    #         assert( type(newNode) == SearchNode)

    #         # check for save list
    #         if saveList != None:

    #             # insert to saved list
    #             inserted = self.insertToList( len( saveList ), newNode, saveList )
            
    #         # otherwise, insert to open
    #         else:
    #             inserted = self.insertToList( len( self.open ), newNode, self.open )

    #         # Try inserting and track ignored nodes
    #         if not inserted:

    #             # track ignored nodes
    #             ignored.append(newNode)

    #     # return ignored 
    #     return ignored 

    # def insert_front( self, unorderedList, saveList=None ):

    #     # initialize variables 
    #     ignored = []

    #     # verbose
    #     if self.verbose:

    #         # grab child letters
    #         children = [n.label for n in unorderedList]

    #         # print verbose
    #         print(f"Now inserting: {children}\n")
        
    #     # insert new list at the end of current list
    #     for newNode in unorderedList:

    #         # assert N is an object
    #         assert( type(newNode) == SearchNode)
            
    #         # check for save list
    #         if saveList != None:

    #             # insert to saved list
    #             inserted = self.insertToList( 0, newNode, saveList )
            
    #         # otherwise, insert to open
    #         else:
    #             inserted = self.insertToList( 0, newNode, self.open )

    #         # Try inserting and track ignored nodes
    #         if not inserted:

    #             # track ignored nodes
    #             ignored.append(newNode)

    #     # return ignored 
    #     return ignored 

    # def insert_ordered(self, unorderedList, saveList=None, alpha=False):

    #     # inititalized variables
    #     ignored = []
        
    #     # verbose
    #     if self.verbose:

    #         # grab child letters
    #         children = [n.label for n in unorderedList]

    #         # print verbose
    #         print(f"Now inserting ordered: {children}\n")
        
    #     # loop through unordered list 
    #     for newNode in unorderedList:

    #         # Reset index for each new node
    #         index = 0 

    #         # logic for saveList provided 
    #         if saveList != None:

    #             # Sort by alpha
    #             if alpha == True:

    #                 # Find the correct insertion index
    #                 while index < len( saveList ) and saveList[index].label < newNode.label:

    #                     # incremement index
    #                     index += 1

    #             # sort by cost
    #             else:
    #                 # Find the correct insertion index
    #                 while index < len( saveList ) and saveList[index].pathcost < newNode.pathcost:

    #                     # incremement index
    #                     index += 1

    #             # Try inserting and track ignored nodes
    #             if not self.insertToList( index, newNode, saveList ):

    #                 # track ignored nodes
    #                 ignored.append(newNode)

    #         # logic for self.open list
    #         else:

    #             # sort by alpha
    #             if alpha == True:

    #                 # Find the correct insertion index
    #                 while index < len( self.open ) and self.open[index].label < newNode.label:

    #                     # incremement index
    #                     index += 1

    #             # sort by cost
    #             else:

    #                 # Find the correct insertion index
    #                 while index < len( self.open ) and self.open[index].pathcost < newNode.pathcost:

    #                     # incremement index
    #                     index += 1

    #             # Try inserting and track ignored nodes
    #             if not self.insertToList( index, newNode, self.open ):

    #                 # track ignored nodes
    #                 ignored.append(newNode)

    #     # return ignored
    #     return ignored

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
                print(f"{self.getAlgorithmName()} search from {self.start_letter} to {self.goal_letter}")

            # runs the alg
            return self._alg.start( start_node  = self.findNode( self.start_letter ),
                                    goal_node   = self.findNode( self.goal_letter ),
                                    )
        # print debug
        if self.verbose:
            print("Algoritm not set")

        # return None
        return None

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

        if alg_str == "DEPTH":
            return DFS( self.verbose, self.nodeGraph )
        
        elif alg_str == "BEST":
            return BestFS( self.verbose, self.nodeGraph )
        
        elif alg_str == "BREADTH":
            return BFS( self.verbose, self.nodeGraph )
        
        elif alg_str == "A*":
            return AStar( self.verbose, self.nodeGraph )
        
        return None
    
    def updateAlgNodeGraph( self ):
        self._alg.nodeGraph = self.nodeGraph