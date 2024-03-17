import pygame as p
import pieces
import copy
import dimensions as dim
import utils


class Board:
    def __init__(self):
        self.board = [
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        self.white_to_move = True
        self.black_check = False
        self.white_check = False
        self.white_can_castle_KS = True
        self.white_can_castle_QS = True
        self.black_can_castle_KS = True
        self.black_can_castle_QS = True
        self.move_log = []
        self.white_pieces = []
        self.black_pieces = []
        self.castling_QS = False
        self.castling_KS = False

    
    def move(self, initial_y, initial_x, new_y, new_x): 
        """Move a piece to a square, update old square, move aux piece (castling, etc)
        Takes (y, x) of old square, (y, x) of new square"""
        self.board[new_y][new_x] = self.board[initial_y][initial_x]
        self.board[initial_y][initial_x] = '--' 


    def generate_legal_moves(self):
        """Generates possible moves for all pieces, creates a test board, attempts all moves
        and looks if that move results in check. If not, it appends the move to that pieces
        legal move list. Also checks white_to_move status/check status and updates moves accordingly"""
        self.update_pieces()

        checks = self.look_for_checks()
        if checks[0] == True:
            self.white_check = True
        else:
            self.white_check = False
        if checks[1] == True:
            self.black_check = True
        else:
            self.black_check = False

        self.castling_move_generator()
        test_board_instance = copy.deepcopy(self)
        test_board = test_board_instance.board
        
        if self.white_to_move:
            for piece in self.white_pieces:
                piece.legal_moves.clear()
                for move in piece.possible_moves:
                    y = move[0]
                    x = move[1]
                    temp_square = test_board[y][x]
                    test_board_instance.move(*piece.position, *move)
                    test_board_instance.update_pieces()
                    check = test_board_instance.look_for_checks()
                    if check[0] == False:
                        piece.legal_moves.append(move)
                    test_board_instance.move(*move, *piece.position)
                    test_board[y][x] = temp_square
        else:
            for piece in self.black_pieces:
                piece.legal_moves.clear()
                for move in piece.possible_moves:
                    y = move[0]
                    x = move[1]
                    temp_square = test_board[y][x]
                    test_board_instance.move(*piece.position, *move)
                    test_board_instance.update_pieces()
                    check = test_board_instance.look_for_checks()
                    if check[1] == False:
                        piece.legal_moves.append(move)
                    test_board_instance.move(*move, *piece.position)
                    test_board[y][x] = temp_square

                
    def look_for_checks(self):
        """Scans all moves to see if a king is targeted. Returns a tuple,
        (white_in_check, black_in_check), values of each are True or False"""
        white_in_check = False
        black_in_check = False

        for piece in self.white_pieces + self.black_pieces:
            if piece.piece_type == "wK":
                white_king = piece.position
            if piece.piece_type == "bK":
                black_king = piece.position
        
        for piece in self.white_pieces + self.black_pieces:
            for move in piece.possible_moves:
                if move == white_king:
                    white_in_check = True
                if move == black_king:
                    black_in_check = True

        return (white_in_check, black_in_check)


    def update_pieces(self):
        """Clears pieces lists, iterates board, constructs each piece and their moves, 
        adds them to their respective lists"""
        self.white_pieces.clear()
        self.black_pieces.clear()
        for rank in range(dim.SQUARES_SIDE):
            for file in range(dim.SQUARES_SIDE):
                type = self.board[rank][file]
                new_piece = None
                if type != '--':
                    color = utils.find_color(self.board, rank, file)
                    
                    match type:
                        case "wP" | "bP":
                            new_piece = pieces.Pawn(color, (rank, file), type, self.board)

                        case "wB" | "bB":
                            new_piece = pieces.Bishop(color, (rank, file), type, self.board)
                        
                        case "wN" | "bN":
                            new_piece = pieces.Knight(color, (rank, file), type, self.board)

                        case "wR" | "bR":
                            new_piece = pieces.Rook(color, (rank, file), type, self.board)

                        case "wQ" | "bQ":
                            new_piece = pieces.Queen(color, (rank, file), type, self.board)

                        case "wK" | "bK":
                            new_piece = pieces.King(color, (rank, file), type, self.board)
                    
                    if color == "white":
                        self.white_pieces.append(new_piece)
                    else:
                        self.black_pieces.append(new_piece)


    def find_piece_from_coords(self, y, x):
        """Searches piece lists and returns piece type as (y, x) location. Takes coordinates
        as argument"""
        for piece in self.white_pieces + self.black_pieces:
            if piece.position == (y, x):
                return piece


    def move_is_legal(self, piece, move_y, move_x):
        """Checks if a move is in a pieces legal moves list. Takes a piece object 
        and its move coordinates as arguements, returns True or False"""
        if (move_y, move_x) in piece.legal_moves:
            return True
        else:
            return False


    def update_move_log(self, piece, new_y, new_x):
        """Constructs a move log entry based on move. Takes piece object
        and new square coords as arguements"""
        message = ""

        if self.board[new_y][new_x] != '--':
            capture = True
        else:
            capture = False

        if piece.symbol == "P":
            if capture:
                message += (piece.notation[0])
        else:
            message += (piece.symbol)

        if capture:
            message += ("x")
        
        message += (utils.coords_to_notation(new_y, new_x))

        if self.castling_QS:
            message = 'O-O-O'
            self.castling_QS = False
        if self.castling_KS:
            message = 'O-O'
            self.castling_KS = False

        self.move_log.append(message)
        piece.move_log.append(message)
    

    def update_castling_flags(self, piece):
        """Checks if rooks or king as moved, if so, updates game flag. Takes piece
        being moved as arguement"""
        if piece.piece_type == "wR":
            if piece.x == 0:
                self.white_can_castle_QS = False
            if piece.x == 7:
                self.white_can_castle_KS = False
        if piece.piece_type == "bR":
            if piece.x == 0:
                self.black_can_castle_QS = False
            if piece.x == 7:
                self.black_can_castle_KS = False
        if piece.piece_type == "wK":
            self.white_can_castle_KS = False
            self.white_can_castle_QS = False
        if piece.piece_type == "bK":
            self.black_can_castle_KS = False
            self.black_can_castle_QS = False

    
    def castling_move_generator(self):
        """Checks if there are pieces in the way of castling, then checks if the
        king would be in check during his castling journey. Updates possible moves accordingly"""
        #white
        ks_pieces = [(7, 5), (7, 6)]
        ks_checks = [(7, 4), (7, 5), (7, 6)]
        qs_pieces = [(7, 1), (7, 2), (7, 3)]
        qs_checks = [(7, 4), (7, 3), (7, 2)]

        if self.white_can_castle_QS:
            qs = True
        if self.white_can_castle_KS:
            ks = True
        for square in qs_pieces:
            y = square[0]
            x = square[1]
            if self.board[y][x] != '--':
                qs = False
        for square in ks_pieces:
            y = square[0]
            x = square[1]
            if self.board[y][x] != '--':
                ks = False
        if qs or ks:
            for piece in self.black_pieces:
                for move in piece.possible_moves:
                    if move in qs_checks:
                        qs = False
                    if move in ks_checks:
                        ks = False
        if qs:
            king = self.find_piece_from_coords(7, 4)
            king.possible_moves.append((7, 2))
        if ks:
            king = self.find_piece_from_coords(7, 4)
            king.possible_moves.append((7, 6))

        #black
        qs_pieces = [(0, 1), (0, 2), (0, 3)]
        qs_checks = [(0, 4), (0, 3), (0, 2)]
        ks_pieces = [(0, 5), (0, 6)]
        ks_checks = [(0, 4), (0, 5), (0, 6)]
        if self.black_can_castle_QS:
            qs = True
        if self.black_can_castle_KS:
            ks = True
        for square in qs_pieces:
            y = square[0]
            x = square[1]
            if self.board[y][x] != '--':
                qs = False
        for square in ks_pieces:
            y = square[0]
            x = square[1]
            if self.board[y][x] != '--':
                ks = False

        if qs or ks:
            for piece in self.white_pieces:
                for move in piece.possible_moves:
                    if move in qs_checks:
                        qs = False
                    if move in ks_checks:
                        ks = False
        if qs:
            king = self.find_piece_from_coords(0, 4)
            king.possible_moves.append((0, 2))
        if ks:
            king = self.find_piece_from_coords(0, 4)
            king.possible_moves.append((0, 6))

    def special_moves(self, piece, new_y, new_x):
        """Deals with special moves like castling and en_passant. Usually when
        a move involves more than two squares. Takes initial piece and new square
        as arguements"""
        #castling
        if piece.symbol == "K":
            if new_x == piece.x + 2:
                self.castling_KS = True
                self.board[new_y][7] = '--'
                if piece.color == "white":
                    self.board[new_y][5] = 'wR'
                else:
                    self.board[new_y][5] = 'bR'
            if new_x == piece.x - 2:
                self.castling_QS = True
                self.board[new_y][0] = '--'
                if piece.color == "white":
                    self.board[new_y][3] = "wR"
                else:
                    self.board[new_y][3] = "bR"
        



    def checkmate(self): # Looks at move counter/check status and determines if checkmate is present
        pass


    def stalemate(self): # Looks at move counter/check status and determines if stalemate is present
        pass
        

    