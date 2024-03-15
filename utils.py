import pygame as p


files = ["a", "b", "c", "d", "e", "f", "g", "h"]
ranks = ["8", "7", "6", "5", "4", "3", "2", "1"]

def notation_to_coords(file, rank): 
    """Converts chess notation ("a", "4") to coordinates on the board instance (y, x).
    EX: notation_to_coords("a", "5") == (3, 0)"""
    y = ranks.index(rank)
    x = files.index(file)
    return (y, x)

def coords_to_notation(y, x): 
    """Converts coordinates (y, x) to chess notation ("4, "a"). 
    EX: coord_to_notation(3, 0) == ("a", "4")"""
    file = files[x]
    rank = ranks[y]
    return (file, rank)

def find_color(board, y, x): # Determines color of piece from coordinates. Returns None if no piece exists
    pass

def find_type(board, y, x): # Determines type of a piece from coordinates, Returns None if no piece exists
    pass

def find_coords(screen_x, screen_y): # Determines square that is clicked, returns (y, x) 
    pass

