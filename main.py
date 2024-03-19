import pygame as p
import dimensions as dim
import game_board
import game
import gui
import utils

p.init()

board_sprite = gui.BoardSprite(gui.LIGHT_BLUE, gui.BLUE)
screen = p.display.set_mode((dim.screen_size), p.RESIZABLE)
p.display.set_caption("chess :)")
clock = p.time.Clock()
images = {}
board = game_board.Board()

gui.load_images(images)
circle = gui.load_circle()

running = True
square_selected = False
piece = None
board.generate_legal_moves()
promotion = False


while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
        elif event.type == p.WINDOWSIZECHANGED:
            new_width = screen.get_width()
            new_height = screen.get_height()
            gui.recalculate_dimensions(new_width, new_height)
            board_sprite = gui.BoardSprite(gui.LIGHT_BLUE, gui.BLUE)
            gui.load_images(images)
            circle = gui.load_circle()
        elif event.type == p.MOUSEBUTTONDOWN and event.button == 1:
            location = p.mouse.get_pos()
            if promotion:
                promo_piece = gui.proccess_promotion_click(*location)
                if promo_piece != None:
                    board.promotion(*new_square, promo_piece)
                    promotion = False
                    new_piece = board.find_piece_from_coords(*new_square)
                    board.update_move_log(piece)
                    board.generate_legal_moves()
            else:
                if not square_selected:
                    square = utils.find_coords(*location)
                    square_selected = True
                    piece = board.find_piece_from_coords(*square)
                    if piece == None:
                        square_selected = False
                else:
                    new_square = utils.find_coords(*location)
                    if board.move_is_legal(piece, *new_square):
                        board.update_castling_flags(piece)
                        promotion = board.is_move_promotion(piece, *new_square)
                        board.special_moves(piece, *new_square)
                        board.move(*square, *new_square)
                        square_selected = False
                        board.white_to_move = not board.white_to_move
                        if not promotion:
                            board.generate_legal_moves()
                            board.update_move_log(piece)
                    else:
                        square_selected = False

    screen.fill(gui.BLACK)
    board_sprite.draw_board(screen)
    gui.draw_pieces(screen, board.board, images)
    if square_selected and piece != None:
        gui.draw_legal_moves(screen, board, piece.legal_moves, circle)
    if promotion:
        gui.draw_promotion_popup(screen, board, images)
    gui.display_moves(screen, board.move_display)

    p.display.flip()

p.quit()