import pygame as p
import utils
import pieces
import game_board as gb

board = gb.Board

new_pawn = pieces.Pawn("black", (1, 1), "bP", board)

new_knight = pieces.Knight("black", (1, 2), "bN", board)

new_knight.test_method()