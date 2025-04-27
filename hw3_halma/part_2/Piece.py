class Piece():

    def __init__(self, *, canvasPiece, canvasText, owner) -> None:
        
        self.canvasPiece = canvasPiece
        self.canvasText = canvasText
        self.owner = owner

    def get_coords( self, *, board ):

        # get board len
        my_id = self.get_id()
        boardSize = len(board)

        # just make sure we have an ID here
        assert( my_id != None )

        # loop thru board
        for row in range( boardSize ):

            # iterate thru cols
            for col in range( boardSize ):

                # grab piece
                pieceObj = board[row][col]

                # check if not none and if the ID matches
                if pieceObj != None and pieceObj.get_id() == my_id:

                    # return the x and y
                    return row, col
        # return None, None
        return None, None
    
    def get_id( self ):
        return self.canvasPiece