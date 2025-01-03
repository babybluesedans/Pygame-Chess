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
        self.black_checked = False
        self.white_checked = False
        self.black_checkmated = False
        self.white_checkmated = False
        self.game_stalemate = False
        self.white_can_castle_KS = True
        self.white_can_castle_QS = True
        self.black_can_castle_KS = True
        self.black_can_castle_QS = True
        self.move_log = []
        self.move_display = []
        self.white_pieces = []
        self.black_pieces = []
        self.castling_QS = False
        self.castling_KS = False
        self.last_move = ()
        self.en_passant = False
        self.capture = False
        self.promotion_piece = ""
        self.last_board = copy.deepcopy(self)
    
    def move(self, initial_y, initial_x, new_y, new_x): 
        """Move a piece to a square, update old square, move aux piece (castling, etc)
        Takes (y, x) of old square, (y, x) of new square"""
        if self.board[new_y][new_x] != '--':
            self.capture = True
        self.board[new_y][new_x] = self.board[initial_y][initial_x]
        self.board[initial_y][initial_x] = '--' 
        self.last_move = ((initial_y, initial_x,), (new_y, new_x))


    def generate_legal_moves(self):
        """Generates possible moves for all pieces, creates a test board, attempts all moves
        and looks if that move results in check. If not, it appends the move to that pieces
        legal move list. Also checks white_to_move status/check status and updates moves accordingly"""
        self.update_pieces()
        move_counter = 0

        checks = self.look_for_checks()
        if checks[0] == True:
            self.white_checked = True
        else:
            self.white_checked = False
        if checks[1] == True:
            self.black_checked = True
        else:
            self.black_checked = False

        self.castling_move_generator()
        self.en_passant_generator()
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
                        move_counter += 1
                    test_board_instance.move(*move, *piece.position)
                    test_board[y][x] = temp_square
            if move_counter == 0:
                if self.white_checked == True:
                    self.white_checkmated = True
                else:
                    self.game_stalemate = True
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
                        move_counter += 1
                    test_board_instance.move(*move, *piece.position)
                    test_board[y][x] = temp_square
            if move_counter == 0:
                if self.black_checked == True:
                    self.black_checkmated = True
                else:
                    self.game_stalemate = True

                
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


    def update_move_log(self, piece):
        """Constructs a move log entry based on move. Takes piece object
        and new square coords as arguements"""
        message = ""
        if self.en_passant:
            self.capture = True

        if piece.symbol == "P":
            if self.capture:
                message += (piece.notation[0])
                self.en_passant = False
        else:
            message += (piece.symbol)
        
        if piece.symbol == 'R' or piece.symbol == "N" or piece.symbol == "Q":
            # long bit of code to detect if multiple pieces of the same can move
            # to the same square, so that i can add a rank or file to notation
            piece_counter = 0
            second_piece = None
            for pieces in self.last_board.white_pieces + self.last_board.black_pieces:
                if piece.piece_type == pieces.piece_type:
                    if self.last_move[1] in pieces.possible_moves:
                        piece_counter += 1
                        if pieces.position != self.last_move[0]:
                            second_piece = pieces
            if piece_counter > 1:
                position = utils.coords_to_notation(*self.last_move[0])
                if self.last_move[0][1] == second_piece.x:
                    message += position[1]
                else:
                    message += position[0]
                
                
            

        if self.capture:
            message += ("x")
            self.capture = False
        
        message += (utils.coords_to_notation(*self.last_move[1]))

        if self.castling_QS:
            message = 'O-O-O'
            self.castling_QS = False
        if self.castling_KS:
            message = 'O-O'
            self.castling_KS = False
        
        if self.white_checked or self.black_checked:
            if self.white_checkmated or self.black_checkmated:
                message += ('#')
            else:
                message += ('+')
        if self.promotion_piece:
            message += f"={self.promotion_piece}"
            self.promotion_piece = ""


        self.move_log.append(message)
        self.move_display.insert(0, message)
        if len(self.move_display) > 6:
            self.move_display.pop()
    

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
        qs = False
        ks = False
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
            if king != None:
                king.possible_moves.append((7, 2))
        if ks:
            king = self.find_piece_from_coords(7, 4)
            if king != None:
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
            if king != None:
                king.possible_moves.append((0, 2))
        if ks:
            king = self.find_piece_from_coords(0, 4)
            if king != None:
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
        #en passant
        if piece.symbol == "P":
            if new_x == piece.x + 1 or new_x == piece.x - 1:
                if self.board[new_y][new_x] == '--':
                    if self.white_to_move:
                        self.board[new_y + 1][new_x] = '--'
                    else:
                        self.board[new_y - 1][new_x] = '--'
                    self.en_passant = True
    
    def is_move_promotion(self, piece, new_y, new_x):
        """Detects if a move is promotion for promotion event.
        Takes piece object and move coords as arguements"""
        if piece.symbol == "P":
            if new_y == 0 or new_y == 7:
                return True
        return False
    
    def promotion(self, new_y, new_x, new_piece):
        """Actually swaps a piece for promtion. Takes move
        coords and piece selection (0-3) from promotion processor as
        arguements"""
        piece = ''
        if not self.white_to_move:
            piece += 'w'
        else:
            piece += 'b'
        match new_piece:
            case 0:
                piece += 'Q' 
                self.board[new_y][new_x] = piece
                self.promotion_piece = 'Q'
            case 1:
                piece += 'R'
                self.board[new_y][new_x] = piece
                self.promotion_piece = 'R'
            case 2:
                piece += 'N'  
                self.board[new_y][new_x] = piece
                self.promotion_piece = 'N'
            case 3:
                piece += "B"
                self.board[new_y][new_x] = piece
                self.promotion_piece = 'B'

    def en_passant_generator(self):
        """Checks if white pawn has a pawn next to it that just moved its first
        two squares, then adds en passant to its possible moves."""
        square = None
        last_move_index = len(self.move_log) - 1
        for piece in self.white_pieces:
            if piece.y == 3 and piece.piece_type == "wP":
                possible_squares = []
                if piece.x < 7:
                    square = (piece.y, piece.x + 1)
                    possible_squares.append(square)
                if piece.x > 0:
                    square = (piece.y, piece.x - 1)
                    possible_squares.append(square)
                if self.last_move[1] in possible_squares:
                    coords = self.last_move[1]
                    black_piece = self.find_piece_from_coords(*coords)
                    if black_piece.piece_type == "bP":
                        if self.last_move[0][0] == 1:
                            piece.possible_moves.append((black_piece.y - 1, black_piece.x))

        for piece in self.black_pieces:
            if piece.y == 4 and piece.piece_type == "bP":
                possible_squares = []
                if piece.x < 7:
                    square = (piece.y, piece.x + 1)
                    possible_squares.append(square)
                if piece.x > 0:
                    square = (piece.y, piece.x - 1)
                    possible_squares.append(square)
                if self.last_move[1] in possible_squares:
                    coords = self.last_move[1]
                    white_piece = self.find_piece_from_coords(*coords)
                    if white_piece.piece_type == "wP":
                        if self.last_move[0][0] == 6:
                            piece.possible_moves.append((white_piece.y + 1, white_piece.x))
                
    def notation_to_move(self, move=None):
        """Parses chess move notation to make a move. Useful for CLI 
        moves and for AI communication"""
         #basically a notation parser
        for i in range(len(move) - 1):
            if move[i] == 'x': #removes capture status, not important
                temp_string = move[:i] + move[i + 1:]
                move = temp_string
        length = len(move)
        if move[length - 1] == "+" or move[length - 1] == "#":
            length =- 1 #removes check statuses, not important for moving piece

        if length == 2: #pawn move
            square = utils.notation_to_coords(move)
            for piece in self.white_pieces + self.black_pieces:
                if piece.symbol == "P":
                    if square in piece.legal_moves:
                        self.last_board = copy.deepcopy(self)
                        self.update_castling_flags(piece)
                        self.special_moves(piece, *square)
                        self.move(*piece.position, *square)
                        return piece

        if move == "O-O": # ks castle
            for piece in self.white_pieces + self.black_pieces:
                if piece.symbol == "K":
                    for moves in piece.legal_moves:
                        if moves[1] == piece.x + 2:
                            self.last_board = copy.deepcopy(self)
                            self.update_castling_flags(piece)
                            self.special_moves(piece, *moves)
                            self.move(*piece.position, *moves)
                            return piece
        
        if move == 'O-O-O': # qs castle
            for piece in self.white_pieces + self.black_pieces:
                if piece.symbol == "K":
                    for moves in piece.legal_moves:
                        if moves[1] == piece.x - 2:
                            self.last_board = copy.deepcopy(self)
                            self.update_castling_flags(piece)
                            self.special_moves(piece, *moves)
                            self.move(*piece.position, *moves)
                            return piece
        
        if move[0].isupper(): #Not a pawn
            if length == 3:
                notation = ''
                notation += move[1] + move[2]
                square = utils.notation_to_coords(notation)
                for piece in self.white_pieces + self.black_pieces:
                    if piece.symbol == move[0]:
                        if square in piece.legal_moves:
                            self.last_board = copy.deepcopy(self)
                            self.update_castling_flags(piece)
                            self.special_moves(piece, *square)
                            self.move(*piece.position, *square)
                            return piece
            else: #EX. two rooks staring at same square
                if move[1].isalpha(): #both on same rank
                    x = utils.notation_to_coords(move[1])
                    notation = ''
                    notation += move[2] + move[3]
                    square = utils.notation_to_coords(notation)
                    for piece in self.white_pieces + self.black_pieces:
                        if piece.symbol == move[0]:
                            if piece.x == x:
                                if square in piece.legal_moves:
                                    self.last_board = copy.deepcopy(self)
                                    self.update_castling_flags(piece)
                                    self.special_moves(piece, *square)
                                    self.move(*piece.position, *square)
                                    return piece
                else: #both on same file
                    y = utils.notation_to_coords(move[1])
                    notation = ''
                    notation += move[2] + move[3]
                    square = utils.notation_to_coords(notation)
                    for piece in self.white_pieces + self.black_pieces:
                        if piece.symbol == move[0]:
                            if piece.y == y:
                                if square in piece.legal_moves:
                                    self.last_board = copy.deepcopy(self)
                                    self.update_castling_flags(piece)
                                    self.special_moves(piece, *square)
                                    self.move(*piece.position, *square)
                                    return piece
       
        else: #pawn capturing
            notation = ""
            notation += move[1] + move[2]
            square = utils.notation_to_coords(notation)
            for piece in self.white_pieces + self.black_pieces:
                if square in piece.legal_moves:
                    self.last_board = copy.deepcopy(self)
                    self.update_castling_flags(piece)
                    self.special_moves(piece, *square)
                    self.move(*piece.position, *square)
                    return piece     
        
        return 0

    