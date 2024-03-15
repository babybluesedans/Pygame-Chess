SQUARES = 64
SQUARES_SIDE = 8
GRAY = None
BLUE = None



screen_size = width, height = 800, 600
board_size = int(width * .625)
while board_size % 8 != 0:
    board_size += 1
square_size = board_size // 8
board_left = width // 2 - (board_size // 2)
board_top = height // 2 - (board_size // 2)
piece_size = int(square_size * .9)
promotion_size = promotion_width, promotion_height = None, None
promotion_left = None
promotion_top = None
promotion_x_margin = None
promotion_y_margin = None
promotion_piece_start = None
promotion_piece_gap = None

def recalculate_dimensions(new_width, new_height): # Recalculates game dimensions if the screen size is updated
    pass