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
loaded = False


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
    if loaded:
        move = input("input a move: ")
        piece = board.notation_to_move(move)
        if piece:
            print("success!")
            board.white_to_move = not board.white_to_move
            board.generate_legal_moves()
            board.update_move_log(piece)

    screen.fill(gui.BLACK)
    board_sprite.draw_board(screen)
    gui.draw_pieces(screen, board.board, images)
    gui.display_moves(screen, board.move_display)
    loaded = True

    p.display.flip()

p.quit()