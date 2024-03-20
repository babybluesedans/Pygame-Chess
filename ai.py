import game_board

piece_values = {"P": 10, "B": 35, "N": 30, "R": 50, "Q": 90, "K" 10000}
#create values for pieces

#get all available moves
#make a move on a test board
#add score if a piece is captured
#check all available enemy moves
# add negative value to score if captured
#repeat for depth

board = game_board.Board

def depth_search(depth, move=None, board=None):
    if move:
        
