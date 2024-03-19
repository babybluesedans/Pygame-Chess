import pygame as p
import dimensions as dim
import utils
p.init()
font = p.font.Font(None, 40)
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
    """Loads images to their name in an 'images' dictionary and a circle into a circle variable"""
    pieces = ['wB', 'wK', 'wN', 'wP', 'wQ', 'wR', 'bB', 'bK', 'bN', 'bP', 'bQ', 'bR']
    for piece in pieces: 
        images[piece] = p.transform.smoothscale(p.image.load("pieces/" + piece + ".png").convert_alpha(),
                                                      (dim.piece_size, dim.piece_size))
    
def load_circle():
    circle = p.transform.smoothscale(p.image.load("pieces/move_circle.png"),
                                    (dim.piece_size * .8 , dim.piece_size * .8))
    return circle
            
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


def draw_legal_moves(screen, board, legal_moves, circle):
    """Takes a list of legal squares for a piece as arguement, draws circles
    on those squares"""
    circle_rect = circle.get_rect()
    square_margin = (dim.square_size - circle_rect.width) // 2
    for move in legal_moves:
        screen_pos = utils.find_screen_position(*move)
        x = screen_pos[0]
        y = screen_pos[1]
        screen.blit(circle, (x + square_margin, y + square_margin))

def draw_promotion_popup(screen, board, images):
    """Draws the promotion popup and populates the clickable rects list
    for the promotion click processor. takes surface, board, and images list
    as arguements"""
    p.draw.rect(screen, WHITE, (dim.promotion_left, #Draw background
                                dim.promotion_top,
                                dim.promotion_width,
                                dim.promotion_height), 0, 10)
    color_alt = 0
    if not board.white_to_move:
        promotion_pieces = ["wQ", "wR", "wN", "wB"]
    else:
        promotion_pieces = ["bQ", "bR", "bN", "bB"]
    if not dim.promotion_rects:
        rects_added = False
    else:
        rects_added = True
    for i in range(1, 5): #Alternate Squares
        squares = i - 1
        if color_alt % 2 == 1:
            color = BLUE
        else:
            color = LIGHT_BLUE
        color_alt += 1
        p.draw.rect(screen, color, ((dim.promotion_left + #Draw squares
                                     (dim.promotion_x_margin * i) +
                                     (dim.square_size * squares)), 
                                     dim.promotion_top + 
                                     dim.promotion_y_margin, 
                                     dim.square_size,
                                     dim.square_size))
        
        if not rects_added:
            dim.promotion_rects.append((dim.promotion_left +
                                       (dim.promotion_x_margin * i) + 
                                       (dim.square_size * squares), 
                                       dim.promotion_top + 
                                       dim.promotion_y_margin))
            last_added = len(dim.promotion_rects) - 1
            dim.promotion_rects.append((dim.promotion_rects[last_added][0] + 
                                           dim.square_size, 
                                           dim.promotion_rects[last_added][1] +
                                           dim.square_size))
    for j in range(4):
        x = dim.promotion_piece_start + ((dim.promotion_piece_gap * j) +
                                         dim.piece_size / 2)
        y = dim.promotion_top + dim.promotion_y_margin
        new_piece = PieceSprite(images[promotion_pieces[j]])
        screen.blit(new_piece.image, (x, y + 3))

        
def proccess_promotion_click(mouse_x, mouse_y):
    """Compares user click to promotion window piece rects to return
    which piece is being selected. Returns 0 - 3 and takes mouse coords
    as arguement"""
    i = 0
    while i < 8:
        if dim.promotion_rects[i][0] < mouse_x < dim.promotion_rects[i + 1][0]:
            if dim.promotion_rects[i][1] < mouse_y < dim.promotion_rects[i + 1][1]:
                if i == 0:
                    return 0
                else:
                    return i // 2
        i += 2

def recalculate_dimensions(new_width, new_height):
    """Recalculates game dimensions if the screen size is updated.
    Takes screen width and height as arguements"""
    dim.screen_size = dim.width, dim.height = new_width, new_height
    dim.board_size = int(dim.height * .8)
    while dim.board_size % 8 != 0:
        dim.board_size += 1
    dim.square_size = dim.board_size // 8
    dim.board_left = dim.width // 2 - (dim.board_size // 2)
    dim.board_top = dim.height // 2 - (dim.board_size // 2)
    dim.piece_size = int(dim.square_size * .9)
    dim.promotion_size = dim.promotion_width, dim.promotion_height = (int(dim.board_size * .6),
                                                        int(dim.board_size * .15))
    dim.promotion_left = (dim.width // 2) - (dim.promotion_width // 2)
    dim.promotion_top = (dim.height // 2) - (dim.promotion_height // 2)
    dim.promotion_x_margin = (dim.promotion_width - (dim.square_size * 4)) / 5
    dim.promotion_y_margin = (dim.promotion_height - dim.square_size) / 2
    dim.promotion_piece_start = dim.promotion_left + dim.promotion_x_margin + ((dim.square_size / 2)
                                                                    - dim.piece_size)
    dim.promotion_piece_gap = dim.square_size + dim.promotion_x_margin
    dim.promotion_rects = []
    dim.move_log_top = dim.board_size + ((dim.height - dim.board_size) *.65)

def display_moves(screen, display_log):
    message = "Move Log:  "
    for move in display_log:
        message += f"{move}  "
    if len(display_log) >= 6:
        message += '...' 
    message_surface = font.render(message, True, WHITE)
    message_rect = message_surface.get_rect()
    message_rect.topleft = (dim.board_left, dim.move_log_top)
    screen.blit(message_surface, message_rect)
    

    