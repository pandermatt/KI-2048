import sys

import numpy as np

import game

# Author:				chrn (original by nneonneo)
# Date:				11.11.2016
# Description:			The logic of the AI to beat the game.

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
previous_board = None
next_move = None
stuck_counter = 0

FACTOR_EMPTY_FIELDS = 0.05
FACTOR_BORDER = 0.10


# [[8, 32, 16, 8],
#  [8, 16, 128, 2],
#  [2, 64, 0, 2],
#  [0, 0, 0, 0]]


def find_best_move(board):
    bestmove = find_best_move_with_rating(board)

    return bestmove


def find_best_move_with_rating(board):
    # UP, DOWN, LEFT, RIGHT
    # 1 best -- 0 worst
    rating = [0, 0, 0, 0]

    rating_methods = [
        validate_empty_fields,
        validate_place_biggest_number,
        validate_possible_move
    ]

    for rating_method in rating_methods:
        rating = merge_rating(rating, rating_method(board))

    # print(rating)
    return rating.index(max(rating))


def validate_possible_move(board):
    rating = [0, 0, 0, 0]
    for i in range(4):
        if board_equals(board, execute_move(i, board)):
            rating[i] = -np.Inf
    return rating


def merge_rating(main, merge):
    return [x + y for x, y in zip(main, merge)]


def validate_empty_fields(board):
    return FACTOR_EMPTY_FIELDS * (16 - np.array([
        np.count_nonzero(execute_move(UP, board)),
        np.count_nonzero(execute_move(DOWN, board)),
        np.count_nonzero(execute_move(LEFT, board)),
        np.count_nonzero(execute_move(RIGHT, board))
    ]))


def validate_place_biggest_number(board):
    np_board = np.array(board)
    rating = [0, 0, 0, 0]

    # UP, DOWN, LEFT, RIGHT
    return FACTOR_BORDER * np.array([
        np_board[0, np.argmax(np_board[0, :])],
        np_board[3, np.argmax(np_board[3, :])],
        np_board[np.argmax(np_board[:, 0]), 0],
        np_board[np.argmax(np_board[:, 3]), 3]
    ])


def get_valid_moves(board):
    moves = [UP, DOWN, LEFT, RIGHT]
    if np.array_equal(game.merge_down(board), board):
        moves.remove(DOWN)
    if np.array_equal(game.merge_up(board), board):
        moves.remove(UP)
    if np.array_equal(game.merge_left(board), board):
        moves.remove(LEFT)
    if np.array_equal(game.merge_right(board), board):
        moves.remove(RIGHT)
    return moves


def execute_move(move, board):
    """
    move and return the grid without a new random tile
	It won't affect the state of the game in the browser.
    """

    if move == UP:
        return game.merge_up(board)
    elif move == DOWN:
        return game.merge_down(board)
    elif move == LEFT:
        return game.merge_left(board)
    elif move == RIGHT:
        return game.merge_right(board)
    else:
        sys.exit("No valid move")


def board_equals(board, newboard):
    """
    Check if two boards are equal
    """
    return (newboard == board).all()
