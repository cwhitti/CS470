from Bot import Bot
from standardConstants import * 

class Player( Bot ):

    def __init__(self, name, *, colorName, mainColor, homeColor, is_bot=False, mode=HUMAN_MODE) -> None:

        super().__init__( ABpruning=AB_PRUNE, mode=mode ) 
        self.name = name
        self.colorName = colorName
        self.mainColor = mainColor
        self.homeColor = homeColor
        self.order = None
        self.homeSquares = []
        self.score = 0
        self.mode = mode
        self.maxPlayer = None

        


    
    def assign_minmax( self, *, maxPlayer ):
        self.maxPlayer = maxPlayer

    def add_home_square( self, row, col ):
        self.homeSquares.append( (row, col) )

    def assign_order( self, order:int ):
        self.order = order

    def display( self ):

        print(f'''
    - Player {self.order} (mode={self.mode})
        - Name: {self.name}
        - Color Name: {self.colorName}
        - Main Color: {self.mainColor}
        - Home Color: {self.homeColor}
'''
              )
        
    def get_home_squares( self ):
        return self.homeSquares
