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

while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
        elif event.type == p.MOUSEBUTTONDOWN and event.button == 1:
            location = p.mouse.get_pos()
            if not square_selected:
                square = utils.find_coords(*location)
                board.update_pieces()
                square_selected = True
                piece = board.find_piece(*square)
            else:
                new_square = utils.find_coords(*location)
                board.move(*square, *new_square)
                square_selected = False


            
    screen.fill(gui.BLACK)
    board_sprite.draw_board(screen)
    gui.draw_pieces(screen, board.board, images)
    if square_selected and piece != None:
        gui.draw_legal_moves(screen, board, piece.legal_moves)

    p.display.flip()

p.quit()