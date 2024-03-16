import utils

class Piece:
    def __init__(self, color, position, piece_type, board):
        self.color = color
        self.position = position
        self.y = position[0]
        self.x = position[1]
        self.board = board
        self.piece_type = piece_type
        self.possible_moves = [] # Moves that a piece can physically move to
        self.legal_moves = [] # Moves that a piece can physically move to AND do not result in check

    def change_type(self): # Changes type of piece (promotion)
        pass

    def __str__(self):
        return f"{self.color} {self.piece_type} at {self.position} with moves {self.possible_moves}"

class Pawn(Piece):
    def __init__(self, color, position, piece_type, board):
        super().__init__(color, position, piece_type, board)
        self.possible_moves = self.pawn_moves()

    def pawn_moves(self): 
        """Determines possible moves for pawn at that position"""
        self.possible_moves.clear()
        if self.color == "white":
            if self.y >= 1:
                if self.board[self.y - 1][self.x] == "--":
                    self.possible_moves.append((self.y - 1, self.x))
                if self.y >= 2:
                    if self.board[self.y - 2][self.x] == "--":
                        if self.y == 6:
                            self.possible_moves.append((self.y - 2, self.x))
                if self.x > 0:
                    if self.board[self.y - 1][self.x - 1] != '--':
                        if utils.find_color(self.board, self.y - 1, self.x - 1) != self.color:
                            self.possible_moves.append((self.y - 1, self.x - 1))
                if self.x < 7:
                    if self.board[self.y - 1][self.x + 1] != '--':
                        if utils.find_color(self.board, self.y - 1, self.x + 1) != self.color:
                            self.possible_moves.append((self.y - 1, self.x + 1))
        if self.color == "black":
            if self.y <= 6:
                if self.board[self.y + 1][self.x] == "--":
                    self.possible_moves.append((self.y + 1, self.x))
                if self.y <= 5:
                    if self.board[self.y + 2][self.x] == "--":
                        if self.y == 1:
                            self.possible_moves.append((self.y + 2, self.x))
                if self.x > 0:
                    if self.board[self.y + 1][self.x - 1] != '--':
                        if utils.find_color(self.board, self.y + 1, self.x - 1) != self.color:
                            self.possible_moves.append((self.y + 1, self.x - 1))
                if self.x < 7:
                    if self.board[self.y + 1][self.x + 1] != '--':
                        if utils.find_color(self.board, self.y + 1, self.x + 1) != self.color:
                            self.possible_moves.append((self.y + 1, self.x + 1))
        self.legal_moves = self.possible_moves


    def en_passant(self): # Determines if En Passant is possible and amends the move list
        pass

    def promotion(self): # Determines if a move is a promotion
        pass

class Knight(Piece):
    def __init__(self, color, position, piece_type, board):
        super().__init__(color, position, piece_type, board)

    def knight_moves(self): # Determines possible moves for a knight at that location
        pass

class Bishop(Piece):
    def __init__(self, color, position, piece_type, board):
        super().__init__(color, position, piece_type, board)

    def bishop_moves(self): # Determines possible moves for a bishop at that location
        pass

class Rook(Piece):
    def __init__(self, color, position, piece_type, board):
        super().__init__(color, position, piece_type, board)

    def rook_moves(self): # Determines possible moves for a rook at that location
        pass

    def rook_castling(self): # Determines if castling is possible with that rook
        pass


class Queen(Piece):
    def __init__(self, color, position, piece_type, board):
        super().__init__(color, position, piece_type, board)

    def queen_moves(self): # Determines possible moves for queen at that location
        pass

class King(Piece):
    def __init__(self, color, position, piece_type, board):
        super().__init__(color, position, piece_type, board)

    def king_moves(self): # Determines possible moves for King at that location 
        pass

    def king_castling(self): # Determines if king can castle and which side/amends king move list
        pass
