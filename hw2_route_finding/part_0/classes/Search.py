from classes.SearchNode import SearchNode
from classes.Algorithm import Algorithm
from classes.DRDViz import DRDViz

ALG_TYPE = "BFS"
VERBOSE = True

class Searcher( Algorithm ):

    def __init__( self, filename ) -> None:
        
        # initialize variables
        self.myViz = DRDViz()
        self.verbose = VERBOSE
        self.filename = filename

        # initialize algorithm
        Algorithm.__init__(self, 
                                alg_type=ALG_TYPE, 
                                verbose=VERBOSE
                        )
        
        # set graph
        self.letterGraph = self.loadGraph( filename )

        # print loading statement
        if self.verbose:
            print(f"Loaded search type {self.getAlgorithmName()} with map in file: {filename}")
            print()
            print("Generated graph:")
            print(self.letterGraph)

    def getAlgorithmName( self ):
        '''
        Gets the name of the current algorithm
        '''
        # initialize variables
        name = None

        # check if alg != None
        if self._alg != None:

            # set the name
            name = self._alg.name

        # return the name 
        return name
    
    # def go( self ):

    #     print("Starting alg...")
    #     self.startAlgorithm()


    def loadGraph( self, filename ):
        '''
        Reads a file and constructs an adjacency dictionary.
        '''

        # initialize variables
        graph = {}

        # ensure filename != None
        if filename != None:

            # open the file
            with open(filename, 'r') as file:

                # loop through file
                for line in file.readlines():

                    # Parse tuple from text
                    parts = eval(line.strip())  # Converts string to tuple

                    '''
                    ASK ABOUT WHAT THE GRAOH SHOULD LOOK LIKE, HOW WE SHOULD REPRESENT
                    RELATIONSHIPS?
                    
                    IS IT LETTERS RELATING TO LETTERS, OR NODES RELATING TO NODES
                    '''

                    # grab nodes and weight
                    node1, node2, weight = parts[:3]  # Extract relevant values
                    
                    # Add node1 to graph if not exist
                    if node1 not in graph:
                        graph[node1] = {}
                    
                    # Add node2 to graph if not exist
                    if node2 not in graph:
                        graph[node2] = {}

                    # Add bidirectional edges
                    graph[node1][node2] = weight
                    graph[node2][node1] = weight  
        else:
            raise f"Filename {filename} does not exist."

        return graph

    def setStartGoal( self, start_letter, goal_letter):

        # initialize variables 
        start_letter = start_letter.upper()
        goal_letter  = goal_letter.upper()

        # assert graph != None and stuff in graph
        assert self.letterGraph != None and len(self.letterGraph) > 0

        # verify in graph
        assert ( self.verifyNodeExists( start_letter ) and self.verifyNodeExists( goal_letter ) )
            
        # load graph from file
        self.myViz.loadGraphFromFile( self.filename )
        self.myViz.plot()

        # mark start and end goals
        self.myViz.markStart( start_letter )
        self.myViz.markGoal( goal_letter )

        # self.myViz.save("thisworks.png")

        # initialize goals for algorithm
        self.initializeGoals( start_letter, goal_letter, self.letterGraph )

    def verifyNodeExists( self, letter ):
        return letter in self.letterGraph.keys()
        
            