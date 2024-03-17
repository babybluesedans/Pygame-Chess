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
promotion_size = promotion_width, promotion_height = (int(board_size * .6),
                                                      int(board_size * .15))
promotion_left = (width // 2) - (promotion_width // 2)
promotion_top = (height // 2) - (promotion_height // 2)
promotion_x_margin = (promotion_width - (square_size * 4)) / 5
promotion_y_margin = (promotion_height - square_size) / 2
promotion_piece_start = promotion_left + promotion_x_margin + ((square_size / 2)
                                                                - piece_size)
promotion_piece_gap = square_size + promotion_x_margin

def recalculate_dimensions(new_width, new_height): # Recalculates game dimensions if the screen size is updated
    pass