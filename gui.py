import pygame as p
import dimensions as dim
import utils

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (13, 120, 219)
LIGHT_BLUE = (99, 161, 219)

class PieceSprite:
    def __init__(self, image):
        self.image = image
        self.rect = image.get_rect()
        

class BoardSprite:
    def __init__(self, color_light, color_dark):
        self.color_light = color_light
        self.color_dark = color_dark
    
    def draw_board(self, screen):
        """Draws board on screen at dimensions. Takes surface as arguement"""
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
            
def load_images(images):
    """Loads images to their name in an 'images' dictionary"""
    pieces = ['wB', 'wK', 'wN', 'wP', 'wQ', 'wR', 'bB', 'bK', 'bN', 'bP', 'bQ', 'bR']
    for piece in pieces: 
        images[piece] = p.transform.scale(p.image.load("pieces/" + piece + ".png").convert_alpha(),
                                                      (dim.piece_size, dim.piece_size))
    
            
def draw_pieces(screen, board, images):
    """Nested for loop through a board 2D list that drawsthe piece that is
    represented on the board. (wP = white pawn at square (6, 0)) etc.
    Arguements are a surface to draw on, 2D List board, and an images
    dictionary of loaded images"""
    y_square = dim.board_top + dim.square_size // 2
    for rank in range(dim.SQUARES_SIDE):
        x_square = dim.board_left + dim.square_size // 2
        for file in range(dim.SQUARES_SIDE):
            piece = board[rank][file]
            if piece != "--":
                new_piece = PieceSprite(images[piece])
                x = x_square - new_piece.rect.width // 2
                y = y_square - new_piece.rect.width // 2
                screen.blit(new_piece.image, (x, y))
            x_square += dim.square_size
        y_square += dim.square_size

def draw_legal_moves(screen, board, legal_moves):
    for move in legal_moves:
        screen_pos = utils.find_screen_position(*move)
        x = screen_pos[0] + dim.square_size // 2
        y = screen_pos[1] + dim.square_size //2
        p.draw.circle(screen, BLACK, (x, y), dim.piece_size / 3, width = 5)