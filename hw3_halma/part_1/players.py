import random 
from standardConstants import *

from lists.names import names
from lists.colors import colors

class Player:

    def __init__(self, name, *, colorName, mainColor, homeColor, bot=False) -> None:
        self.name = name
        self.colorName = colorName
        self.mainColor = mainColor
        self.homeColor = homeColor
        self.order = None
        self.homeSquares = []
        self.score = 0
    
    def add_home_square( self, row, col ):
        self.homeSquares.append( (row, col) )

    def assign_order( self, order:int ):
        self.order = order

    def display( self ):

        print(f'''
    - Player {self.order} 
        - Name: {self.name}
        - Color Name: {self.colorName}
        - Main Color: {self.mainColor}
        - Home Color: {self.homeColor}
'''
              )
        
    def get_home_squares( self ):
        return self.homeSquares


def generate_order( orderList:list ):
    order = random.choice( orderList )
    orderList.remove( order )
    return order

def get_player_by_color( players, color ):

    # loop through players
    for player in players:

        # compare by color
        if color in [player.mainColor,player.homeColor]:

            # return the player obj
            return player
        
    # else, return None
    return None

def initialize_player( name, *, colorName, colorScheme, bot=False):

    # create player
    player = Player( name, 
                        colorName=colorName, 
                        mainColor=colorScheme[0], 
                        homeColor=colorScheme[1], 
                        bot=bot )
    # return player
    return player

def initialize_bot( ):

    # initialize variables
        # none

    # generate name
    name = random.choice( names  )
    names.pop( names.index( name ) )

    # generate color scheme
    color= random.choice( list(colors.keys()) )
    colorScheme=colors[color]
    colors.pop( color )

    # return an instance of a player
    # return initialize_player( name + "Bot", colorName=color, colorScheme=colorScheme, bot=True )
    return initialize_player( name, colorName=color, colorScheme=colorScheme, bot=True )

def initialize_players( playerList ):

    # initialize variables
    humans = len( playerList )
    bots = PLAYERS - humans if humans <= PLAYERS else 0

    # create bots
    for botNum in range( bots ):

        # initialize bot
        bot = initialize_bot()

        # add to player list
        playerList.append( bot )

    # assert len of playerList == PLAYERS
    assert len(playerList) == PLAYERS

    # order players
    return order_players( playerList ), bots


def swap_players(player_1, player_2):
    return player_2, player_1

def order_players( playerList) -> list :

    # initialize variables
    orderList = list( range (1, len(playerList) + 1 ) ) 
    players = [0] * len(playerList)

    # loop through players
    for player in playerList:

        # grab the order (destructive)
        order = generate_order( orderList )

        # assign the order
        player.assign_order( order )

        # throw in the dict
        players[order - 1] = player
    
    assert( len(orderList ) == 0)
    return players