import pygame as p
import dimensions as dim
import game_board
import pieces
import game
import gui
import utils

board_sprite = gui.BoardSprite(gui.LIGHT_BLUE, gui.BLUE)
screen = p.display.set_mode(dim.screen_size)
clock = p.time.Clock()
images = {}
board = game_board.Board()

gui.load_images(images)

running = True
square_selected = False
piece = None
board.generate_legal_moves()

while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
        elif event.type == p.MOUSEBUTTONDOWN and event.button == 1:
            location = p.mouse.get_pos()
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
                    board.special_moves(piece, *new_square)
                    board.update_move_log(piece, *new_square)
                    board.move(*square, *new_square)
                    square_selected = False
                    board.white_to_move = not board.white_to_move
                    board.generate_legal_moves()
                else:
                    square_selected = False

    screen.fill(gui.BLACK)
    board_sprite.draw_board(screen)
    gui.draw_pieces(screen, board.board, images)
    if square_selected and piece != None:
        gui.draw_legal_moves(screen, board, piece.legal_moves)
    if promotion:
        gui.draw_promotion_popup(screen, board, images)

    p.display.flip()

p.quit()