import random
import sys

import numpy as np

import game

# Author:				chrn (original by nneonneo)
# Date:				11.11.2016
# Description:			The logic of the AI to beat the game.

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
previous_board = None
next_move = None


def find_best_move(board):
    bestmove = -1

    # TODO:
    # Build a heuristic agent on your own that is much better than the random agent.
    # Your own agent don't have to beat the game.
    bestmove = find_best_move_random(board)
    return bestmove


def find_best_move_random_agent():
    return random.choice([UP, DOWN, LEFT, RIGHT])


def find_best_move_random(board):
    global previous_board, next_move

    score_tilde = board[0][3]
    print("hoi")

    if score_tilde == 0:
        return random.choice([UP, RIGHT])

    if next_move:
        move = next_move
        next_move = None
        return move

    stuck = False
    if np.array_equal(board, previous_board):
        stuck = True

    previous_board = board

    board_is_full = np.count_nonzero(board) == 16

    print(board)

    if stuck:
        if board_is_full:
            return UP
        next_move = RIGHT
        return LEFT

    if np.count_nonzero(board[0]) < 4:
        if np.count_nonzero(board[1]) == 0:
            return random.choice([UP, RIGHT])
        return random.choice([UP, RIGHT])
    return random.choice([UP, RIGHT])


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
