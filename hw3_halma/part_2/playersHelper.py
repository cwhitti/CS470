import random 
from standardConstants import *
from lists.names import names
from lists.colors import colors
from standardConstants import *
from Player import Player
from Bot import Bot

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

def initialize_player( name, *, colorName, colorScheme, mode):

    # create player obj
    player = Player( name, 
                        colorName=colorName, 
                        mainColor=colorScheme[0], 
                        homeColor=colorScheme[1], 
                        mode=mode )
    
    # return player
    return player

def initialize_bot( mode ):

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
    return initialize_player( name, colorName=color, colorScheme=colorScheme, mode=mode )

def initialize_players( playerList ):

    # initialize variables
    players = len( playerList )
    autoBots = PLAYERS - players if players <= PLAYERS else 0

    # take out the colors already picked
    for human in playerList:

        try:
            colors.pop( human.colorName )

        except KeyError:
            pass

    # debug
    print(f"Generating [{autoBots}] bots...")

    # create bots
    for botNum in range( autoBots ):

        # initialize bot
        bot = initialize_bot( mode=BOT_MODE ) 

        print(f"Generated {bot.name}!")

        # add to player list
        playerList.append( bot )

    # assert len of playerList == PLAYERS
    assert len(playerList) == PLAYERS

    # order players
    return order_players( playerList ), autoBots


def switch_players(player_1, player_2):
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