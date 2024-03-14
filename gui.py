import sys
import pygame as p

class PieceSprite:
    def __init__(self, image, width, height):
        self.image = image
        self.width = width
        self.height = height
        self.rect = image.get_rect()
        self.legal_moves = []
    
    def draw_piece(self):
        pass

    def draw_legal_moves(self, legal_moves):
        pass


class BoardSprite:
    def __init__(self, color_light, color_dark):
        self.color_light = color_light
        self.color_dark = color_dark
    
    def draw_board(self):
        pass


