import sys
import pygame as p

board_size = 500
square_size = board_size / 8
piece_size = piece_width, piece_height = int(square_size * .9), int(square_size * .9)

class GameState:
    def __init__(self):
        self.board = [
        ["bR", "bN", "bB", "bK", "bQ", "bB", "bN", "bR"],
        ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        ["wR", "wN", "wB", "wK", "wQ", "wB", "wN", "wR"]]
        
        self.white_to_move = True
        self.white_in_check = False
        self.black_in_check = False
        self.white_king_moved = False
        self.black_king_moved = False
        self.white_rook_left_moved = False
        self.white_rook_right_moved = False
        self.black_rook_left_moved = False
        self.black_rook_right_moved = False
    
class Piece: #for drawing purposes
    def __init__(self, image):
        self.image = image
        self.rect = image.get_rect()

class ChessPiece: #for analyzing purposes
    def __init__(self, piece_type, color, position):
        self.piece_type = piece_type
        self.color = color
        self.position = position
        self.possible_moves = []
        


    def __str__(self):
        return f"{self.color} {self.piece_type} at {self.position} with moves {self.possible_moves}"
    

    


