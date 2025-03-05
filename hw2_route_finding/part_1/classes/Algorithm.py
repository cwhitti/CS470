
from classes.CONSTANTS import *
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
        '''

        if alg_str == DFS_str:
            return DFS( self.verbose, self.nodeGraph )
        
        elif alg_str == BestFS_str:
            return BestFS( self.verbose, self.nodeGraph )
        
        elif alg_str == BFS_str:
            return BFS( self.verbose, self.nodeGraph )
        
        elif alg_str == ASTAR_str:
            return AStar( self.verbose, self.nodeGraph )
        
        return None
    
    def updateAlgNodeGraph( self ):
        self._alg.nodeGraph = self.nodeGraph