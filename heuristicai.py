import sys

import numpy as np

import game

# Author:				chrn (original by nneonneo)
# Date:				11.11.2016
# Description:			The logic of the AI to beat the game.

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

border_score = [[3, 1, 1, 3],
                [1, 0, 0, 1],
                [1, 0, 0, 1],
                [3, 1, 1, 3]]

smoothness_score = [[3, 2, 1, 0],
                    [3, 2, 1, 0],
                    [3, 2, 1, 0],
                    [3, 2, 1, 0]]

smoothness_scores = [
    np.array(smoothness_score),
    np.flip(smoothness_score),
    np.transpose(smoothness_score),
    np.transpose(np.flip(smoothness_score))
]

snake_score_base = [[15, 14, 13, 12],
                    [8, 9, 10, 11],
                    [7, 6, 5, 4],
                    [0, 1, 2, 3]]

snake_score = np.array([[2 for i in range(4)] for j in range(4)]) ** snake_score_base

snake_scores = [
    16 - np.transpose(np.flip(snake_score)),
    16 - np.transpose(snake_score),
    16 - np.flip(snake_score),
    16 - np.array(snake_score),
    np.array(snake_score),
    np.flip(snake_score),
    np.transpose(snake_score),
    np.transpose(np.flip(snake_score))
]


def find_best_move(board):
    best_score = -np.inf
    best_move = -1

    from benchmark import _run_benchmark
    _run_benchmark(board)

    for direction in range(4):
        new_board = execute_move(direction, board)
        if board_equals(board, new_board):
            continue
        new_score = check_score_methods(new_board)
        if new_score > best_score:
            best_move = direction
            best_score = new_score
    return best_move


def check_score_methods(board):
    score_methods = [
        [check_snake, 1],
        [check_border, 0.1],
        [check_empty_fields, 0.1],
        [check_biggest_number, 0.001],
        [check_smoothness, 0.01],
        [check_total_occurrence, 0.01],
        [check_count_occurrence, 0.1],
        [check_mean_occurrence, 0.1],
        [check_snake_look_ahead, 0.8],
    ]

    return sum([func[0](board) * func[1] for func in score_methods])


def check_snake(board):
    return max([np.sum(board * i) for i in snake_scores])


# def check_snake_square(board):
#     return max([np.sum(board * i * i) for i in snake_scores])


def check_snake_look_ahead(board):
    return max([check_snake(execute_move(i, board)) for i in range(4)])


def check_smoothness(board):
    return max([np.sum(board * i) for i in smoothness_scores])


def check_border(board):
    return np.multiply(board, border_score).sum()


def check_empty_fields(board):
    return 16 - np.count_nonzero(board)


def check_biggest_number(board):
    return np.max(board)


def check_total_occurrence(board):
    return _check_occurrence_in_row(board)[0] + _check_occurrence_in_row(np.transpose(board))[0]


def check_count_occurrence(board):
    return _check_occurrence_in_row(board)[1] + _check_occurrence_in_row(np.transpose(board))[1]


def check_mean_occurrence(board):
    row_sum, row_count = _check_occurrence_in_row(board)
    column_sum, column_count = _check_occurrence_in_row(np.transpose(board))
    if row_count == 0 or column_count == 0:
        return 0
    return row_sum / row_count + column_sum / column_count


def _check_occurrence_in_row(board):
    count = 0
    neighbor_sum = 0
    for row in board:
        previous_num = -1
        for num in row:
            if num != 0 and previous_num == num:
                neighbor_sum += num
                count += 1
            previous_num = num
    return [neighbor_sum, count]


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
