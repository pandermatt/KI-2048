# import sys
#
# import numpy as np
#
# import game
#
# # Author:				chrn (original by nneonneo)
# # Date:				11.11.2016
# # Description:			The logic of the AI to beat the game.
#
# UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
#
# score = [[15, 14, 13, 12], [11, 10, 9, 8], [7, 6, 5, 4], [3, 2, 1, 0]]
# scores = [
#     16 - np.transpose(np.flip(score)),
#     16 - np.transpose(score),
#     16 - np.flip(score),
#     16 - np.array(score),
#     np.array(score),
#     np.flip(score),
#     np.transpose(score),
#     np.transpose(np.flip(score))
# ]
#
#
# def find_best_move(board):
#     bestmove = -1
#     score = 0
#     for direction in range(4):
#         new_board = execute_move(direction, board)
#         if board_equals(board, new_board):
#             continue
#         if score < merge_score_short(new_board):
#             bestmove = direction
#
#     return bestmove
#
#
# def merge_score(board):
#     high_score = 0
#     for i in scores:
#         new_score = np.sum(board * i)
#         if high_score < new_score:
#             high_score = new_score
#     return high_score
#
#
# def merge_score_short(board):
#     return max([np.sum(board * i * i) for i in scores])
#
#
# def execute_move(move, board):
#     """
#     move and return the grid without a new random tile
# 	It won't affect the state of the game in the browser.
#     """
#
#     if move == UP:
#         return game.merge_up(board)
#     elif move == DOWN:
#         return game.merge_down(board)
#     elif move == LEFT:
#         return game.merge_left(board)
#     elif move == RIGHT:
#         return game.merge_right(board)
#     else:
#         sys.exit("No valid move")
#
#
# def board_equals(board, newboard):
#     """
#     Check if two boards are equal
#     """
#     return (newboard == board).all()
#
#
# if __name__ == '__main__':
#     board = [[8, 32, 16, 8],
#              [8, 16, 128, 2],
#              [2, 64, 0, 2],
#              [0, 0, 0, 0]]
#     assert merge_score_short(board) == merge_score(board)
