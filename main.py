import pygame as p
import dimensions as dim
import board
import pieces
import game
import gui
import utils


board_sprite = gui.BoardSprite(gui.LIGHT_BLUE, gui.BLUE)

running = True

while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False

    gui.screen.fill(gui.BLACK)
    board_sprite.draw_board()
    p.display.flip()

p.quit()