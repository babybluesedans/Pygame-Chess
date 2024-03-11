import sys
import pygame as p
from math import sqrt
import gamestate as gs

p.init()

screen_size = width, height = 800, 600
screen = p.display.set_mode(screen_size)
clock = p.time.Clock()
board_size = 500
squares = 64
square_perimeter = 8
board_left = width / 2 - board_size / 2
board_top = height / 2 - board_size / 2
blue = (13,120,219)
gray = (99,161,219)
square_size = board_size / 8
piece_size = piece_width, piece_height = int(square_size * .9), int(square_size * .9)
images = {}


def load_images():
    pieces = ['wB', 'wK', 'wN', 'wP', 'wQ', 'wR', 'bB', 'bK', 'bN', 'bP', 'bQ', 'bR']
    for piece in pieces: 
        images[piece] = p.transform.scale(p.image.load("pieces/" + piece + ".png"), (piece_size))

def draw_pieces(screen, board, board_left, board_top):
    draw_y = board_top + square_size // 2
    for rank in range(8):
        draw_x = board_left + square_size // 2
        for file in range(8):
            piece = board[rank][file]
            if piece != "--":
                new_piece = gs.Piece(images[piece])
                screen.blit(new_piece.image, (draw_x - new_piece.rect.width // 2, 
                draw_y - new_piece.rect.width // 2))
            draw_x += square_size
        draw_y += square_size

def draw_board(screen):
    board = p.draw.rect(screen, blue, p.Rect(board_left, board_top, 500, 500))
    draw_y = board_top
    square_iter = 0
    for y_square in range(square_perimeter):
        draw_x = board_left
        if square_iter % 2 == 1:
            draw_x += square_size
            square_iter -= 2
        for x_square in range(square_perimeter // 2):
            p.draw.rect(screen, gray, p.Rect(draw_x, draw_y, square_size, square_size))
            draw_x += square_size * 2
        square_iter += 1
        draw_y += square_size

def find_square(x, y):
    x -= 150
    y -= 50
    x_square = x // square_size
    y_square = y // square_size
    return (int(x_square), int(y_square))

def piece_type(x, y):
    piece = game.board[y][x]
    return piece
    
def move_processor(piece, x, y):
    match piece:
        case "wP":
            pawn_moves("white", x, y)
            print("wP")
        case "wB":
            bishop_moves("white", x, y)
            print("bB")
        case "wK":
            pass
        case "wN":
            pass
        case "wQ":
            pass
        case "wR":
            pass
        case "bP":
            pawn_moves("black", x, y)
            print("bP")
        case "bB":
            bishop_moves("black", x, y)
            print("bB")
        case "bK":
            pass
        case "bN":
            pass
        case "bQ":
            pass
        case "bR":
            pass
        
def pawn_moves(color, x, y):
    blocked = False
    can_capture_left = False
    can_capture_right = False
    first_move = False
    in_turn = True
    can_move = True
    two_spaces_blocked = False
    possible_moves_white = [(y - 1, x),
                            (y - 2, x),
                            (y - 1, x + 1),
                            (y - 1, x - 1)]
    possible_moves_black = [(y + 1, x),
                            (y + 2, x),
                            (y + 1, x - 1),
                            (y + 1, x + 1)]
    
    if color == "white":
        if game.white_to_move == True:
            in_turn = True
        else:
            in_turn = False
        if y == 6:
            first_move = True
        else:
            first_move = False
        if game.board[y - 1][x] != "--":
            blocked = True
        else:
            blocked = False
        if x > 0:
            if game.board[y - 1][x - 1] != "--":
                can_capture_left = True
            else:
                can_capture_left = False
        else:
            can_capture_left = False
        if x < 7:
            if game.board[y - 1][x + 1] != "--":
                can_capture_right = True
            else:
                can_capture_right = False
        else:
            can_capture_right = False
        if not blocked and first_move and game.board[y - 2][x] != "--":
            two_spaces_blocked = True
        else:
            two_spaces_blocked = False

    if color == "black":
        if game.white_to_move == False:
            in_turn = True
        else: 
            in_turn = False
        if y == 1:
            first_move = True
        else:
            first_move = False
        if game.board[y + 1][x] != "--":
            blocked = True
        else:
            blocked = False
        if x > 0:
            if game.board[y + 1][x - 1] != "--":
                can_capture_left = True
            else:
                can_capture_left = False
        else:
            can_capture_left = False
        if x < 7:
            if game.board[y + 1][x + 1] != "--":
                can_capture_right = True
            else:
                can_capture_right = False
        else:
            can_capture_right = False
        if not blocked and first_move and game.board[y + 2][x] != "--":
            two_spaces_blocked = True
        else:
            two_spaces_blocked = False

    if color == "white":
        if can_move and in_turn:
            if blocked:
                possible_moves_white.remove((y - 1, x))
            if first_move == False or two_spaces_blocked == True:
                possible_moves_white.remove((y - 2, x))
            if not can_capture_left:
                possible_moves_white.remove((y - 1, x - 1))
            if not can_capture_right:
                possible_moves_white.remove((y - 1, x + 1))
        else:
            possible_moves_white.clear()
        print(f"legal moves {possible_moves_white}")
        return possible_moves_white

    if color == "black":
        if can_move and in_turn:
            if blocked:
                possible_moves_black.remove ((y + 1, x))
            if first_move == False or two_spaces_blocked == True:
                possible_moves_black.remove((y + 2, x))
            if not can_capture_left:
                possible_moves_black.remove((y + 1, x - 1))
            if not can_capture_right:
                possible_moves_black.remove((y + 1, x + 1))
        else:
            possible_moves_black.clear()
        print(f"legal moves {possible_moves_black}")
        return possible_moves_black

def bishop_moves(color, x, y):
    bishop_legal_moves = []
    bishop_illegal_moves = []

    if (color == "white" and game.white_to_move == True) or (color == "black" 
    and game.white_to_move == False):
        for i in range(1, 8):
            if x + i <= 7 and y + i <= 7:
                bishop_legal_moves.append((y + i, x + i))   
            if x - i >= 0 and y - i >= 0:
                bishop_legal_moves.append((y - i, x - i))
            if x + i <= 7 and y - i >= 0:
                bishop_legal_moves.append((y - i, x + i))
            if y + i <= 7 and x - i >= 0:
                bishop_legal_moves.append((y + i, x - i))
        temp_set = set(bishop_legal_moves)
        bishop_legal_moves = list(temp_set)
        for square in bishop_legal_moves:
            if game.board[square[0]][square[1]] != "--":
                if find_color(square[1], square[0]) == find_color(x, y):
                    can_take = False
                else:
                    can_take = True
                if square[1] > x:
                    x_add = True
                else:
                    x_add = False
                if square[0] > y:
                    y_add = True
                else:
                    y_add = False
                if x_add and y_add:
                    y_iter = 1
                    x_iter = 1
                    while (square[0] + y_iter) <= 7 and (square[1] + x_iter) <= 7:
                        bishop_illegal_moves.append((square[0] + y_iter, square[1] + x_iter))
                        y_iter += 1
                        x_iter += 1
                if not x_add and not y_add:
                    y_iter = -1
                    x_iter = -1
                    while (square[1] + x_iter) >= 0 and (square[0] + y_iter) >= 0:
                        bishop_illegal_moves.append((square[0] + y_iter, square[1] + x_iter))
                        y_iter -= 1
                        x_iter -= 1
                if x_add and not y_add:
                    y_iter = -1
                    x_iter = 1
                    while y_iter + square[0] >= 0 and square[1] + x_iter <= 7:
                        bishop_illegal_moves.append((square[0] + y_iter, square[1] + x_iter))
                        x_iter += 1
                        y_iter -= 1

                if y_add and not x_add:
                    y_iter = 1
                    x_iter = -1
                    while y_iter + square[0] <= 7 and square[1] + x_iter >= 0:
                        bishop_illegal_moves.append((square[0] + y_iter, square[1] + x_iter))
                        x_iter -= 1
                        y_iter += 1
                if not can_take:
                    if ((square[0], square[1])) in bishop_legal_moves: 
                        bishop_illegal_moves.append((square[0], square[1]))

        set1 = set(bishop_legal_moves)
        set2 = set(bishop_illegal_moves)

        bishop_legal_moves = list(set1.symmetric_difference(set2))

    print(f"legal moves {bishop_legal_moves}")
    return bishop_legal_moves


        
def find_color(x, y):
    square = game.board[y][x]
    if square[0] == 'w':
        return "white"
    if square[0] == 'b':
        return "black"



game = gs.GameState()
load_images()

running = True
square_selected_flag = False

while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
        elif event.type == p.MOUSEBUTTONDOWN and event.button == 1:
            location = p.mouse.get_pos()
            if not square_selected_flag:
                square_selected = find_square(*location)
                move_processor(piece_type(*square_selected), *square_selected)
                square_selected_flag = True
            else:
                new_square = find_square(*location)
                game.board[new_square[1]][new_square[0]] = game.board[square_selected[1]][square_selected[0]]
                game.board[square_selected[1]][square_selected[0]] = "--"
                square_selected_flag = False
                game.white_to_move = not game.white_to_move

    screen.fill("black")
    draw_board(screen)
    draw_pieces(screen, game.board, board_left, board_top)

    p.display.flip()
    clock.tick(60)

p.quit()
