import sys
import pygame as p_type
import pieces
import copy


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
        else:
            self.board = copy.deepcopy(board.board)
        
    def move(self): # Move a piece to a square, update old square, move aux piece (castling, etc)
        pass

    def generate_legal_moves(self): # View moves for each piece and determine if it results in check
        pass

    def look_for_checks(self): # Looks at board and sees if a check is active
        pass

    def checkmate(self): # Looks at move counter/check status and determines if checkmate is present
        pass
    
    def stalemate(self): # Looks at move counter/check status and determines if stalemate is present
        pass
        

    