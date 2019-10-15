import sys

import numpy as np

import game
# Author:      chrn (original by nneonneo)
# Date:        11.11.2016
# Copyright:   Algorithm from https://github.com/nneonneo/2048-ai
# Description: The logic to beat the game. Based on expectimax algorithm.
from heuristicai import check_snake


def find_best_move(board):
    """
    find the best move for the next turn.
    """
    bestmove = -1
    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
    move_args = [UP, DOWN, LEFT, RIGHT]

    result = [score_toplevel_move(i, board) for i in range(len(move_args))]
    bestmove = result.index(max(result))

    # for m in move_args:
    #     print("move: %d score: %.4f" % (m, result[m]))

    return bestmove


def score_toplevel_move(move, board):
    """
    Entry Point to score the first move.
    """
    newboard = execute_move(move, board)

    if board_equals(board, newboard):
        return 0

    empty_fields = 16 - np.count_nonzero(newboard)

    # if np.max(board) < 4000:
    #     if empty_fields <= 4:
    #         return expectimax(newboard, 2)
    #     return expectimax(newboard, 1)
    #
    # if empty_fields > 9:
    #     return expectimax(newboard, 0)
    # if empty_fields > 5:
    #     return expectimax(newboard, 1)
    # if empty_fields > 3:
    #     return expectimax(newboard, 2)
    return expectimax(newboard, 3)


def all_spawns(board, tile):
    spawns = []
    for x in range(4):
        for y in range(4):
            if board[x][y] != 0:
                continue
            spawn_board = np.copy(board)
            spawn_board[x][y] = tile
            spawns.append(spawn_board)
    return spawns


def expectimax(board, depth):
    if depth == 0:
        return check_snake(board)
    score_sum = 0
    for tile, possibility in {2: 0.1, 4: 0.9}.items():
        for spawn in all_spawns(board, tile):
            move_score = [0, 0, 0, 0]
            for direction in range(4):
                moved_spawn = execute_move(direction, spawn)
                if board_equals(moved_spawn, spawn):
                    move_score[direction] = 0
                    continue
                move_score[direction] = expectimax(moved_spawn, depth - 1)
            score = max(move_score)
            score_sum += possibility * score
    return score_sum / (16 - np.count_nonzero(board))


def execute_move(move, board):
    """
    move and return the grid without a new random tile
	It won't affect the state of the game in the browser.
    """

    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

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
