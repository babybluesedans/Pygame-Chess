import sys


class Piece:
    def __init__(self, color, position, piece_type):
        self.color = color
        self.position = position
        self.piece_type = piece_type
        self.possible_moves = [] # Moves that a piece can physically move to
        self.legal_moves = [] # Moves that a piece can physically move to AND do not result in check

    def change_type(): # Changes type of piece (promotion)
        pass

class Pawn(Piece):
    def pawn_moves(self): # Determines possible moves for pawn at that position
        pass

    def en_passant(self): # Determines if En Passant is possible and amends the move list
        pass

    def promotion(self): # Determines if a move is a promotion
        pass

class Knight(Pieces):
    def knight_moves(self): # Determines possible moves for a knight at that location
        pass

class Bishop(Piece):
    def bishop_moves(self): # Determines possible moves for a bishop at that location
        pass

class Rook(Piece):
    def rook_moves(self): # Determines possible moves for a rook at that location
        pass
    def rook_castling(self): # Determines if castling is possible with that rook
        pass


class Queen(Piece):
    def queen_moves(self): # Determines possible moves for queen at that location
        pass

class King(Piece):
     def king_moves(self): # Determines possible moves for King at that location 
        pass

    def king_castling(self): # Determines if king can castle and which side/amends king move list
        pass
