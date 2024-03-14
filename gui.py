import sys
import pygame as p

class PieceSprite:
    def __init__(self, image, width, height, position):
        self.image = image
        self.width = width
        self.height = height
        self.rect = image.get_rect()
        self.position = position
        self.legal_moves = []
    
    def draw_piece(self): # Draw image on board at position
        pass

    def draw_legal_moves(self, legal_moves): # Draw circles for piece's legal moves
        pass


class BoardSprite:
    def __init__(self, color_light, color_dark):
        self.color_light = color_light
        self.color_dark = color_dark
    
    def draw_board(self): # Draws board on screen at dimensions
        pass


