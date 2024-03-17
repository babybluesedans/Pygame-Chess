import utils

class Piece:
    def __init__(self, color, position, piece_type, board):
        self.color = color
        self.position = position
        self.y = position[0]
        self.x = position[1]
        self.notation = utils.coords_to_notation(*position)
        self.symbol = piece_type[1]
        self.board = board
        self.piece_type = piece_type
        self.move_log = []
        self.possible_moves = [] # Moves that a piece can physically move to
        self.legal_moves = [] # Moves that a piece can physically move to AND that do not result in check

    def change_type(self): # Changes type of piece (promotion)
        pass

    def __str__(self):
        return f"{self.color} {self.piece_type} at {self.position}"

class Pawn(Piece):
    def __init__(self, color, position, piece_type, board):
        super().__init__(color, position, piece_type, board)
        self.possible_moves = self.pawn_moves()

    def pawn_moves(self): 
        """Creates and returns list of possible pawn moves from that position"""
        possible_moves = []
        x = self.x
        y = self.y
        if self.color == "white":
            if y >= 1:
                if self.board[y - 1][x] == "--":
                    possible_moves.append((y - 1, x))
                if y >= 2:
                    if self.board[y - 2][x] == "--":
                        if y == 6:
                            possible_moves.append((y - 2, x))
                if x > 0:
                    if self.board[y - 1][x - 1] != '--':
                        if utils.find_color(self.board, y - 1, x - 1) != self.color:
                            possible_moves.append((y - 1, x - 1))
                if x < 7:
                    if self.board[y - 1][x + 1] != '--':
                        if utils.find_color(self.board, self.y - 1, x + 1) != self.color:
                            possible_moves.append((y - 1, x + 1))
        if self.color == "black":
            if y <= 6:
                if self.board[y + 1][x] == "--":
                    possible_moves.append((y + 1, x))
                if self.y <= 5:
                    if self.board[y + 2][x] == "--":
                        if y == 1:
                            possible_moves.append((y + 2, x))
                if x > 0:
                    if self.board[y + 1][x - 1] != '--':
                        if utils.find_color(self.board, y + 1, x - 1) != self.color:
                            possible_moves.append((y + 1, x - 1))
                if x < 7:
                    if self.board[y + 1][x + 1] != '--':
                        if utils.find_color(self.board, y + 1, x + 1) != self.color:
                            possible_moves.append((y + 1, x + 1))
        return possible_moves


    def en_passant(self): # Determines if En Passant is possible and amends the move list
        pass

    def promotion(self): # Determines if a move is a promotion
        pass

class Knight(Piece):
    def __init__(self, color, position, piece_type, board):
        super().__init__(color, position, piece_type, board)
        self.possible_moves = self.knight_moves()

    def knight_moves(self):
        """Creates and returns list of possible knight moves from that position"""
        possible_moves = []
        x = self.x
        y = self.y
        moves = [(y + 2, x - 1),
                 (y + 2, x + 1),
                 (y - 2, x - 1),
                 (y - 2, x + 1),
                 (y - 1, x + 2),
                 (y + 1, x + 2), 
                 (y - 1, x - 2),
                 (y + 1, x - 2),]
        for move in moves:
            y = move[0]
            x = move[1]
            if y >= 0 and y <= 7:
                if x >= 0 and x <= 7:
                    if self.board[y][x] != '--':
                        if utils.find_color(self.board, y, x) != self.color:
                            possible_moves.append(move)
                    else:
                        possible_moves.append(move)
        return possible_moves
        

class Bishop(Piece):
    def __init__(self, color, position, piece_type, board):
        super().__init__(color, position, piece_type, board)
        self.possible_moves = self.bishop_moves()

    def bishop_moves(self):
        """Creates and returns list of possible bishop moves from that position"""
        possible_moves = []
        x = self.x
        y = self.y
        while (y - 1 >= 0 and x - 1 >= 0):
            y -= 1 
            x -= 1 
            if self.board[y][x] == '--':
                possible_moves.append((y, x))
            else:
                if utils.find_color(self.board, y, x) != self.color:
                    possible_moves.append((y, x))
                break
        x = self.x
        y = self.y
        while (y - 1 >= 0 and x + 1 <= 7):
            y -= 1
            x += 1 
            if self.board[y][x] == '--':
                possible_moves.append((y, x))
            else:
                if utils.find_color(self.board, y, x) != self.color:
                    possible_moves.append((y, x))
                break
        x = self.x
        y = self.y
        while (y + 1 <= 7 and x - 1 >= 0):
            y += 1
            x -= 1
            if self.board[y][x] == '--':
                possible_moves.append((y, x))
            else:
                if utils.find_color(self.board, y, x) != self.color:
                    possible_moves.append((y, x))
                break
        x = self.x
        y = self.y
        while (y + 1 <= 7 and x + 1 <= 7):
            y += 1
            x += 1 
            if self.board[y][x] == '--':
                possible_moves.append((y, x))
            else:
                if utils.find_color(self.board, y, x) != self.color:
                    possible_moves.append((y, x))
                break
        return possible_moves

class Rook(Piece):
    def __init__(self, color, position, piece_type, board):
        super().__init__(color, position, piece_type, board)
        self.possible_moves = self.rook_moves()

    def rook_moves(self):
        """Creates and returns list of possible rook moves from that position"""
        possible_moves = []
        x = self.x
        y = self.y
        while x + 1 <= 7:
            x += 1
            if self.board[y][x] == '--':
                possible_moves.append((y, x))
            else:
                if utils.find_color(self.board, y, x) != self.color:
                    possible_moves.append((y, x))
                break
        x = self.x
        while x - 1 >= 0:
            x -= 1
            if self.board[y][x] == '--':
                possible_moves.append((y, x))
            else:
                if utils.find_color(self.board, y, x) != self.color:
                    possible_moves.append((y, x))
                break
        x = self.x
        while y + 1 <= 7:
            y += 1
            if self.board[y][x] == '--':
                possible_moves.append((y, x))
            else:
                if utils.find_color(self.board, y, x) != self.color:
                    possible_moves.append((y, x))
                break
        y = self.y
        while y - 1 >= 0:
            y -= 1
            if self.board[y][x] == '--':
                possible_moves.append((y, x))
            else:
                if utils.find_color(self.board, y, x) != self.color:
                    possible_moves.append((y, x))
                break
        return possible_moves

    def rook_castling(self): # Determines if castling is possible with that rook
        pass


class Queen(Piece):
    def __init__(self, color, position, piece_type, board):
        super().__init__(color, position, piece_type, board)
        self.possible_moves = self.queen_moves()

    def queen_moves(self):
        """Creates and returns list of possible queen moves from that position"""
        possible_moves = []
        temp_rook = Rook(self.color, self.position, self.piece_type, self.board)
        temp_bishop = Bishop(self.color, self.position, self.piece_type, self.board)
        possible_moves = temp_rook.rook_moves() + temp_bishop.bishop_moves()
        return possible_moves

class King(Piece):
    def __init__(self, color, position, piece_type, board):
        super().__init__(color, position, piece_type, board)
        self.possible_moves = self.king_moves()

    def king_moves(self):
        """Creates and returns list of possible king moves from that position""" 
        possible_moves = []
        x = self.x
        y = self.y
        moves = [(y, x + 1),
                 (y, x - 1),
                 (y + 1, x),
                 (y - 1, x),
                 (y + 1, x + 1),
                 (y + 1, x - 1),
                 (y - 1, x + 1),
                 (y - 1, x - 1)]
        for move in moves:
            y = move[0]
            x = move[1]
            if x >= 0 and x <= 7:
                if y >= 0 and y <= 7:
                    if self.board[y][x] == '--':
                        possible_moves.append((y, x))
                    else:
                        if utils.find_color(self.board, y, x) != self.color:
                            possible_moves.append((y, x))
        return possible_moves


    def king_castling(self): # Determines if king can castle and which side/amends king move list
        pass
