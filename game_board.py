import pygame as p
import pieces
import copy
import dimensions as dim
import utils


class Board:
    def __init__(self, board=None):
        if board is None:
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
        else:
            self.board = copy.deepcopy(board.board)
        
    def move(self, initial_y, initial_x, new_y, new_x, special=None): 
        """Move a piece to a square, update old square, move aux piece (castling, etc)
        Takes (y, x) of old square, (y, x) of new square, and special move arguement"""
        self.board[new_y][new_x] = self.board[initial_y][initial_x]
        if special == None:
            self.board[initial_y][initial_x] = '--' 

    def generate_legal_moves(self): # View moves for each piece and determine if they result in check
        pass

    def look_for_checks(self): # Looks at board and sees if a check is active
        pass

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

    def find_piece(self, y, x):
        """Searches piece lists and returns piece type as (y, x) location"""
        for piece in self.white_pieces + self.black_pieces:
            if piece.position == (y, x):
                return piece


    def checkmate(self): # Looks at move counter/check status and determines if checkmate is present
        pass
    
    def stalemate(self): # Looks at move counter/check status and determines if stalemate is present
        pass
        

    