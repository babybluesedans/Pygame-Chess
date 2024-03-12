import sys
import pygame as p
from math import sqrt
import gamestate as gs
import copy

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
black = (0, 0, 0)
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

def piece_type(board, x, y):
    piece = board[y][x]
    return piece
    
def move_processor(board, piece, x, y):
    move_list = []
    match piece:
        case "wP":

            move_list = pawn_moves(board, "white", x, y)
        case "wB":
            move_list = diagonal_moves(board, "white", x, y)
        case "wK":
            move_list = king_moves(board, "white", x, y)
        case "wN":
            move_list = knight_moves(board, "white", x, y)
        case "wQ":
            move_list = queen_moves(board, "white", x, y)
        case "wR":
            move_list = straight_moves(board, "white", x, y)
        case "bP":
            move_list = pawn_moves(board, "black", x, y)
        case "bB":
            move_list = diagonal_moves(board, "black", x, y)
        case "bK":
            move_list = king_moves(board, "black", x, y)
        case "bN":
            move_list = knight_moves(board, "black", x, y)
        case "bQ":
            move_list = queen_moves(board, "black", x, y)
        case "bR":
            move_list = straight_moves(board, "black", x, y)
    return move_list
        
def pawn_moves(board, color, x, y):#
    legal_white_pawn_moves =[(y - 1, x),
                             (y - 2, x),
                             (y - 1, x - 1),
                             (y - 1, x + 1)]
    legal_black_pawn_moves = [(y + 1, x),
                             (y + 2, x),
                             (y + 1, x + 1),
                             (y + 1, x - 1)]
    illegal_white_pawn_moves = []
    illegal_black_pawn_moves = []

    if color == "white":
        if board[y - 2][x] != '--':
            illegal_white_pawn_moves.append((y - 2, x))
        if board[y - 1][x] != '--':
            illegal_white_pawn_moves.append((y - 1, x))
            illegal_white_pawn_moves.append((y - 2, x))
        if x > 0:
            if board[y - 1][x - 1] != '--':
                if find_color(board, x - 1, y - 1) == color:
                    illegal_white_pawn_moves.append((y - 1, x - 1))
            else: 
                illegal_white_pawn_moves.append((y - 1, x - 1))
        else:
                illegal_white_pawn_moves.append((y - 1, x - 1))
        if x < 7:
            if board[y - 1][x + 1] != '--':
                if find_color(board, x + 1, y - 1) == color:
                    illegal_white_pawn_moves.append((y - 1, x + 1))
            else:
                    illegal_white_pawn_moves.append((y - 1, x + 1))
        else:
            illegal_white_pawn_moves.append((y - 1, x + 1))
        if y != 6:
            illegal_white_pawn_moves.append((y - 2, x))
        set1 = set(legal_white_pawn_moves)
        set2 = set(illegal_white_pawn_moves)
        legal_white_pawn_moves = list(set1.symmetric_difference(set2))
    else:
        if board[y + 2][x] != '--':
            illegal_black_pawn_moves.append((y + 2, x))
        if board[y + 1][x] != '--':
            illegal_black_pawn_moves.append((y + 1, x))
            illegal_black_pawn_moves.append((y + 2, x))
        if x > 0:
            if board[y + 1][x - 1] != '--':
                if find_color(board, x - 1, y + 1) == color:
                    illegal_black_pawn_moves.append((y + 1, x - 1))
            else: 
                illegal_black_pawn_moves.append((y + 1, x - 1))
        else:
            illegal_black_pawn_moves.append((y + 1, x - 1))
        if x < 7:
            if board[y + 1][x + 1] != '--':
                if find_color(board, x + 1, y + 1) == color:
                    illegal_black_pawn_moves.append((y + 1, x + 1))
            else:
                illegal_black_pawn_moves.append((y + 1, x + 1))
        else:
            illegal_black_pawn_moves.append((y + 1, x + 1))
        if y != 1:
            illegal_black_pawn_moves.append((y + 2, x))
        set1 = set(legal_black_pawn_moves)
        set2 = set(illegal_black_pawn_moves)
        legal_black_pawn_moves = list(set1.symmetric_difference(set2))    

    if color == "white":
        return legal_white_pawn_moves
    else:
        return legal_black_pawn_moves


def diagonal_moves(board, color, x, y):#
    diagonal_legal_moves = []
    diagonal_illegal_moves = []

    for i in range(1, 8):
        if x + i <= 7 and y + i <= 7:
            diagonal_legal_moves.append((y + i, x + i))   
        if x - i >= 0 and y - i >= 0:
            diagonal_legal_moves.append((y - i, x - i))
        if x + i <= 7 and y - i >= 0:
            diagonal_legal_moves.append((y - i, x + i))
        if y + i <= 7 and x - i >= 0:
            diagonal_legal_moves.append((y + i, x - i))

    temp_set = set(diagonal_legal_moves)
    diagonal_legal_moves = list(temp_set)
    for square in diagonal_legal_moves:
        if board[square[0]][square[1]] != "--":
            if find_color(board, square[1], square[0]) == find_color(board, x, y):
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
                    diagonal_illegal_moves.append((square[0] + y_iter, square[1] + x_iter))
                    y_iter += 1
                    x_iter += 1

            if not x_add and not y_add:
                y_iter = -1
                x_iter = -1
                while (square[1] + x_iter) >= 0 and (square[0] + y_iter) >= 0:
                    diagonal_illegal_moves.append((square[0] + y_iter, square[1] + x_iter))
                    y_iter -= 1
                    x_iter -= 1

            if x_add and not y_add:
                y_iter = -1
                x_iter = 1
                while y_iter + square[0] >= 0 and square[1] + x_iter <= 7:
                    diagonal_illegal_moves.append((square[0] + y_iter, square[1] + x_iter))
                    x_iter += 1
                    y_iter -= 1

            if y_add and not x_add:
                y_iter = 1
                x_iter = -1
                while y_iter + square[0] <= 7 and square[1] + x_iter >= 0:
                    diagonal_illegal_moves.append((square[0] + y_iter, square[1] + x_iter))
                    x_iter -= 1
                    y_iter += 1

            if not can_take:
                if ((square[0], square[1])) in diagonal_legal_moves: 
                    diagonal_illegal_moves.append((square[0], square[1]))

    set1 = set(diagonal_legal_moves)
    set2 = set(diagonal_illegal_moves)
    diagonal_legal_moves = list(set1.symmetric_difference(set2))

    return diagonal_legal_moves

def straight_moves(board, color, x, y):#
    straight_legal_moves = []
    straight_illegal_moves = []

    for i in range(1, 8):
        if (x + i) <= 7:
            straight_legal_moves.append((y, x + i))
        if (x - i) >= 0:
            straight_legal_moves.append((y, x - i))
        if (y + i) <= 7:
            straight_legal_moves.append((y + i, x))
        if (y - i) >=0:
            straight_legal_moves.append((y - i, x))
    temp_set = set(straight_legal_moves)
    straight_legal_moves = list(temp_set)
    
    for square in straight_legal_moves:
        if board[square[0]][square[1]] != "--":
            if find_color(board, square[1], square[0]) == color:
                can_take = False
            else: 
                can_take = True
            if square[0] > y:
                i = square[0] + 1
                while i <= 7:
                    straight_illegal_moves.append((i, x))
                    i += 1
            if square[0] < y:
                i = square[0] - 1
                while i >= 0:
                    straight_illegal_moves.append((i, x))
                    i -= 1
            if square[1] > x:
                i = square[1] + 1
                while i <= 7:
                    straight_illegal_moves.append((y, i))
                    i += 1
            if square[1] < x:
                i = square[1] - 1
                while i >= 0:
                    straight_illegal_moves.append((y, i))
                    i -= 1
            if not can_take:
                straight_illegal_moves.append((square[0], square[1]))

    set1 = set(straight_legal_moves)
    set2 = set(straight_illegal_moves)
    straight_legal_moves = list(set1.symmetric_difference(set2))
                    
    return straight_legal_moves
        
def knight_moves(board, color, x, y):#
    knight_legal_moves = [(y + 2, x -1),
                          (y + 2, x + 1),
                          (y - 2, x + 1),
                          (y - 2, x - 1),
                          (y + 1, x + 2),
                          (y - 1, x + 2),
                          (y + 1, x - 2),
                          (y - 1, x - 2)]
    knight_illegal_moves = []


    for square in knight_legal_moves:
        if square[0] < 0 or square[0] > 7:
            knight_illegal_moves.append((square[0], square[1]))
        else:
            if square[1] < 0 or square[1] > 7:
                knight_illegal_moves.append((square[0], square[1]))
            else:
                if board[square[0]][square[1]] != '--':
                    if find_color(board, square[1], square[0]) == color:
                        knight_illegal_moves.append((square[0], square[1]))


    set1 = set(knight_legal_moves)
    set2 = set(knight_illegal_moves)
    knight_legal_moves = list(set1.symmetric_difference(set2))            
    
    
    return knight_legal_moves

def queen_moves(board, color, x, y):
    legal_queen_moves = straight_moves(board, color, x, y) + diagonal_moves(board, color, x, y)

    return legal_queen_moves

def king_moves(board, color, x, y):#
    king_legal_moves = [(y + 1, x),
                          (y + 1, x + 1),
                          (y + 1, x - 1),
                          (y - 1, x),
                          (y - 1, x + 1),
                          (y - 1, x - 1),
                          (y, x + 1),
                          (y, x - 1)]
    king_illegal_moves = []


    for square in king_legal_moves:
        if square[0] < 0 or square[0] > 7:
            king_illegal_moves.append((square[0], square[1]))
        else:
            if square[1] < 0 or square[1] > 7:
                king_illegal_moves.append((square[0], square[1]))
            else:
                if board[square[0]][square[1]] != "--":
                    if find_color(board, square[1], square[0]) == color:
                        king_illegal_moves.append((square[0], square[1]))

    set1 = set(king_legal_moves)
    set2 = set(king_illegal_moves)
    king_legal_moves = list(set1.symmetric_difference(set2))  

    return king_legal_moves

def find_color(board, x, y):#
    square = board[y][x]
    if square[0] == 'w':
        return "white"
    if square[0] == 'b':
        return "black"

def analyze_board(board, white_list, black_list):
    white_list.clear()
    black_list.clear()
    for rank in range(8):
        for file in range(8):
            if file != '--':
                color = find_color(board, file, rank)
                p_type = piece_type(board, file, rank)
                position = (rank, file)
                new_piece = gs.ChessPiece(p_type, color, position)
                new_piece.possible_moves = move_processor(board, new_piece.piece_type,
                new_piece.position[1], new_piece.position[0])

                if color == "white":
                    white_list.append(new_piece)
                
                if color == "black":
                    black_list.append(new_piece)


def find_position(board, piece):#
    for y in range(8):
        for x in range(8):
            if board[y][x] == piece:
                return (y, x)

def find_coordinates(y, x):
    y_coord = (y * square_size) + 50
    x_coord = (x * square_size) + 150
    return (int(y_coord), int(x_coord))

def draw_legal_moves(position):
    selected_piece = None
    for piece in black_pieces + white_pieces:
        if piece.position == position:
            selected_piece = piece
            break
    if selected_piece == None:
        return
    for move in selected_piece.possible_moves:
        coords = find_coordinates(*move)
        x = coords[1] + square_size //2
        y = coords[0] + square_size //2
        p.draw.circle(screen, black, (x, y), piece_width / 3, width = 5)


def check_for_checks(board, white_list, black_list):
    white_king = find_position(board, "wK")
    black_king = find_position(board, "bK")
    white = 0
    black = 0
    
    for piece in black_list:
        if white_king in piece.possible_moves:
            white = 1

    for piece in white_list:
        if black_king in piece.possible_moves:
            black = 1

    return (white, black)

            
def generate_legal_moves():
    #get all legal moves
    analyze_board(game.board, white_pieces, black_pieces)
    #test all legal moves for whose in turn, delete any that result in check
    test_board = copy.deepcopy(game.board)
    if game.white_to_move:
        move_counter = 0
        for piece in white_pieces:
            #print(piece)
            legal_moves = []
            for move in piece.possible_moves: 
                storage = test_board[move[0]][move[1]]
                test_board[move[0]][move[1]] = test_board[piece.position[0]][piece.position[1]]
                test_board[piece.position[0]][piece.position[1]] = '--'

                analyze_board(test_board, temp_white, temp_black)
                check = check_for_checks(test_board, temp_white, temp_black)
                if check == (0, 0) or check == (0, 1):
                    legal_moves.append((move[0], move[1]))
                
                test_board[piece.position[0]][piece.position[1]] = test_board[move[0]][move[1]]
                test_board[move[0]][move[1]] = storage
            piece.possible_moves = legal_moves

        for piece in white_pieces:
            if piece.possible_moves:
                move_counter += 1
        if move_counter == 0:
            print("CHECKMATE!")



    else:
        if not game.white_to_move:
            move_counter = 0
            for piece in black_pieces:
                legal_moves = []
                for move in piece.possible_moves: 
                    storage = test_board[move[0]][move[1]]
                    test_board[move[0]][move[1]] = test_board[piece.position[0]][piece.position[1]]
                    test_board[piece.position[0]][piece.position[1]] = '--'

                    analyze_board(test_board, temp_white, temp_black)
                    check = check_for_checks(test_board, temp_white, temp_black)
                    if check == (1, 0) or check == (0, 0):
                        legal_moves.append((move[0], move[1]))
                    
                    test_board[piece.position[0]][piece.position[1]] = test_board[move[0]][move[1]]
                    test_board[move[0]][move[1]] = storage
                piece.possible_moves = legal_moves

            for piece in black_pieces:
                if piece.possible_moves:
                    move_counter += 1
            if move_counter == 0:
                print("CHECKMATE!")
                
    #determine which color to move, delete rest
    if game.white_to_move:
        for piece in black_pieces:
            piece.possible_moves = []

    if not game.white_to_move:
        for piece in white_pieces:
            piece.possible_moves = []

def is_move_legal(initial_y, initial_x, new_y, new_x):
    selected_piece = None
    for piece in black_pieces + white_pieces:
        if piece.position == (initial_y, initial_x):
            selected_piece = piece
    if selected_piece == None:
        return False
    if (new_y, new_x) in selected_piece.possible_moves:
        return True
    else:
        return False


game = gs.GameState()
load_images()

running = True
square_selected_flag = False

black_pieces = []
white_pieces = []
temp_white = []
temp_black = []
generate_legal_moves()

while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
        elif event.type == p.MOUSEBUTTONDOWN and event.button == 1:
            location = p.mouse.get_pos()
            if not square_selected_flag:
                square_selected = find_square(*location)
                square_selected_flag = True
            else:
                new_square = find_square(*location)
                if is_move_legal(square_selected[1], square_selected[0], new_square[1], new_square[0]):
                    game.board[new_square[1]][new_square[0]] = game.board[square_selected[1]][square_selected[0]]
                    game.board[square_selected[1]][square_selected[0]] = "--"
                    game.white_to_move = not game.white_to_move
                    generate_legal_moves()
                square_selected_flag = False
    
    screen.fill("black")
    draw_board(screen)
    draw_pieces(screen, game.board, board_left, board_top)

    if square_selected_flag:
        draw_legal_moves((square_selected[1], square_selected[0]))

    p.display.flip()
    clock.tick(60)

p.quit()
