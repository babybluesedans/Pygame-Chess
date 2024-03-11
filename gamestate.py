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
    
class Piece:
    def __init__(self, image):
        self.image = image
        self.rect = image.get_rect()



