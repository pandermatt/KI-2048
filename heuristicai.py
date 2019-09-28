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
stuck_counter = 0


def find_best_move(board):
    bestmove = -1

    # TODO:
    # Build a heuristic agent on your own that is much better than the random agent.
    # Your own agent don't have to beat the game.

    # bestmove = find_best_move_random_agent()
    # bestmove = find_best_move_check(board)
    bestmove = best_merge_score(board)
    # bestmove = mega2(board)

    return bestmove


def mega2(board):
    moves = get_valid_moves(board)
    maxScore = -np.inf
    bestmove = -1

    next_board_state_list = get_next_moves(board)

    for move in moves:
        next_board_state = next_board_state_list[move]
        next_move = best_merge_score(next_board_state)
        score = np.sum(get_next_moves(next_board_state)[next_move])

        if score >= maxScore:
            maxScore = score
            bestmove = move

    return bestmove


def mega(board):
    moves = get_valid_moves(board)
    maxScore = -np.inf
    bestmove = -1

    next_board_state = get_next_moves(board)

    for move in moves:
        score = np.sum(next_board_state[move])

        if score >= maxScore:
            maxScore = score
            bestmove = move

    return bestmove


def get_next_moves(board):
    return {
        DOWN: game.merge_down(board),
        UP: game.merge_up(board),
        LEFT: game.merge_left(board),
        RIGHT: game.merge_right(board)
    }


def find_best_move_random_agent():
    return random.choice([UP, DOWN, LEFT, RIGHT])


def get_highest_value_position(board):
    highest_value = 0
    x_pos = 0
    y_pos = 0

    for x in range(4):
        for y in range(4):
            if highest_value < board[x][y]:
                x_pos = x
                y_pos = y
                highest_value = board[x][y]

    print(highest_value)
    return x_pos, y_pos


def best_merge_score(board):
    score = {
        RIGHT: np.count_nonzero(game.merge_right(board)),
        LEFT: np.count_nonzero(game.merge_left(board)),
        UP: np.count_nonzero(game.merge_up(board)),
        DOWN: np.count_nonzero(game.merge_down(board))
    }

    valid_moves = get_valid_moves(board)

    if min(score, key=score.get) in valid_moves:
        return min(score, key=score.get)
    else:
        return find_best_move_check(board, valid_moves)


def find_best_move_check(board, valid_moves):
    moves = valid_moves

    if UP in moves:
        return UP
    if RIGHT in moves:
        return RIGHT

    if LEFT in moves:
        board_left = game.merge_left(board)
        if DOWN in moves:
            board_down = game.merge_down(board)
            if np.count_nonzero(board_left) < np.count_nonzero(board_down):
                return LEFT
        return LEFT

    return mega(board)


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


def find_best_move_random(board):
    global previous_board, next_move, stuck_counter

    if next_move:
        move = next_move
        next_move = None
        return move

    if np.array_equal(board, previous_board):
        stuck_counter = stuck_counter + 1

    previous_board = board
    score_tilde = board[0][3]
    board_is_full = np.count_nonzero(board) == 16

    print(stuck_counter)

    if score_tilde == 0:
        return UP

    if stuck_counter > 1:
        if stuck_counter > 2:
            stuck_counter = 0
            if np.count_nonzero(board[0]) != 4:
                next_move = RIGHT
            return LEFT
        if np.count_nonzero(board[0]) != 4:
            return UP
        # if board_is_full:
        #     return UP
        # next_move = RIGHT
        return RIGHT

    return UP
    # if np.count_nonzero(board[0]) < 4:
    #     if np.count_nonzero(board[1]) == 0:
    #         return random.choice([UP, RIGHT])
    #     return random.choice([UP, RIGHT])
    # return random.choice([UP, RIGHT])


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
