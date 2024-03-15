import pygame as p
import dimensions as dim

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (13, 120, 219)
LIGHT_BLUE = (99, 161, 219)

screen = p.display.set_mode(dim.screen_size)
clock = p.time.Clock()


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
        p.draw.rect(screen, self.color_dark, p.Rect(dim.board_left,
                                                    dim.board_top,
                                                    dim.board_size, 
                                                    dim.board_size))
        y = dim.board_top
        square_i = 0
        for rank in range(dim.SQUARES_SIDE):
            x = dim.board_left
            if square_i % 2 == 1:
                x += dim.square_size
            for square in range(dim.SQUARES_SIDE // 2):
                p.draw.rect(screen, LIGHT_BLUE, p.Rect(x, y, dim.square_size, dim.square_size))
                x += dim.square_size * 2
            square_i += 1
            y += dim.square_size
            
            


