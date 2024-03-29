import pygame as p
import dimensions as dim


files = ["a", "b", "c", "d", "e", "f", "g", "h"]
ranks = ["8", "7", "6", "5", "4", "3", "2", "1"]

def notation_to_coords(notation): 
    """Converts chess notation ("a4") to coordinates on the board instance (y, x).
    EX: notation_to_coords("a4") == (4, 0)"""
    length = len(notation)
    if length == 2:
        y = ranks.index(notation[1])
        x = files.index(notation[0])
        return (y, x)
    else:
        if notation.isdigit():
            return ranks.index(notation)
        else:
            return files.index(notation)


def coords_to_notation(y, x): 
    """Converts coordinates (y, x) to chess notation ("a", "4"). 
    EX: coord_to_notation(3, 0) == ("a", "4")"""
    file = files[x]
    rank = ranks[y]
    return f"{file}{rank}"


def find_color(board, y, x): 
    """Determines color of piece from coordinates
    EX: find_color(board, (3, 2)) == "white"""
    piece = board[y][x]
    if piece[0] == "w":
        return "white"
    else:
        return "black"


def find_coords(screen_x, screen_y): 
    """Determines square that is clicked, returns (y, x)
    EX: find_coords(350, 175) == (3, 2)""" 
    x_margin = (dim.width - dim.board_size) // 2
    y_margin = (dim.height - dim.board_size) // 2
    x = screen_x - x_margin
    y = screen_y - y_margin
    x_square = x // dim.square_size
    y_square = y // dim.square_size
    return (y_square, x_square)


def find_screen_position(y, x):
    """Takes 2D list coordinates (y, x) and returns pixel coordinates (x, y)
    EX find_screen_position(3, 2) == (350, 175)"""
    y_coord = (y * dim.square_size) + dim.board_top
    x_coord = (x * dim.square_size) + dim.board_left
    return (x_coord, y_coord)

