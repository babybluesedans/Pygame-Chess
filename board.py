import sys
import pygame as p_type
import pieces


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
    
    def move(self):
        pass

    def generate_legal_moves(self):
        pass

    def checkmate(self):
        pass
    
    def stalemate(self):
        pass
        

    