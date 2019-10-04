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

FACTOR_EMPTY_FIELDS = 3
FACTOR_BORDER = 0.8
FACTOR_BORDER_ROW = 0.5
FACTOR_MERGE_SCORE = 0.9
FACTOR_MERGE_SCORE_2X = 0.8
FACTOR_MERGE_SCORE_3X = 0.7
FACTOR_NEIGHBOURS = 1.5


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
        validate_top_row,
        validate_merge_top_row,
        validate_merge_second_row,
        validate_merge_third_row_row,
        validate_neighbour,
        validate_empty_fields,
        validate_new_board,
        validate_place_biggest_number,
        validate_end_row,
        validate_merge_score,
        validate_merge_score2x,
        validate_merge_score3x,
        validate_possible_move
    ]

    for rating_method in rating_methods:
        add_rating = rating_method(board)
        rating = merge_rating(rating, add_rating)

    return rating.index(max(rating))


def merge_rating(main, merge):
    return [x + y for x, y in zip(main, merge)]


def validate_new_board(board):
    if np.max(board) < 128:
        # UP, DOWN, LEFT, RIGHT
        return [4, -1, 1, -1]
    return [0, 0, 0, 0]


def validate_top_row(board):
    if not is_n_row_full(board, 0):
        # UP, DOWN, LEFT, RIGHT
        return [2, -10, 1, -5]
    return [0, -5, 0, 0]


def check_neighbour(board, x, y, good_merge):
    value = board[x][y]
    if value >= good_merge:
        # UP, DOWN, LEFT, RIGHT
        try:
            if value == board[x + 1][y]:
                return [0, 0, 6, 0]
        except:
            pass
        try:
            if value == board[x + 1][y + 1]:
                return [2, 0, 4, 0]
        except:
            pass
        try:
            if value == board[x][y + 1]:
                return [4, 0, 0, 0]
        except:
            pass
        try:
            if value == board[x - 1][y + 1]:
                return [2, 0, 0, 3]
        except:
            pass
        try:
            if value == board[x - 1][y]:
                return [0, 0, 0, 4]
        except:
            pass
        return [0, 0, 0, 0]
    else:
        return [0, 0, 0, 0]


def validate_neighbour(board):
    good_merge = np.max(board) / 8
    rating = np.array([0, 0, 0, 0])
    for x in range(4):
        rating = merge_rating(rating, check_neighbour(board, 0, x, good_merge))
    return rank_score(rating, total=FACTOR_NEIGHBOURS)


def validate_merge_top_row(board):
    if np.count_nonzero(execute_move(LEFT, board)[0]) < np.count_nonzero(board[0]):
        # UP, DOWN, LEFT, RIGHT
        return [0, 0, 2, 0]
    return [0, 0, 0, 0]


def validate_merge_second_row(board):
    if np.count_nonzero(execute_move(LEFT, board)[1]) < np.count_nonzero(board[1]):
        # UP, DOWN, LEFT, RIGHT
        return [0, 0, 0, 2]
    return [0, 0, 0, 0]


def validate_merge_third_row_row(board):
    if is_n_row_full(board, 0) and is_n_row_full(board, 1) and \
            np.count_nonzero(execute_move(LEFT, board)[1]) < np.count_nonzero(board[1]):
        # UP, DOWN, LEFT, RIGHT
        return [0, 0, 2, 0]
    return [0, 0, 0, 0]


def is_n_row_full(board, n):
    return np.count_nonzero(board[n]) == 4


def validate_possible_move(board):
    rating = [0, 0, 0, 0]
    for i in range(4):
        if board_equals(board, execute_move(i, board)):
            rating[i] = -np.Inf
    return rating


def validate_merge_score(board):
    max_nr = np.max(board)

    rating = [0, 0, 0, 0]

    new_max = [
        np.max(execute_move(UP, board)),
        np.max(execute_move(DOWN, board)),
        np.max(execute_move(LEFT, board)),
        np.max(execute_move(RIGHT, board))
    ]
    for i in range(4):
        if new_max[i] > max_nr:
            rating[i] = 1 * FACTOR_MERGE_SCORE
    return rating


def validate_merge_score2x(board):
    max_nr = np.max(board)
    rating = [0, 0, 0, 0]
    new_max = [0, 0, 0, 0]

    new_boards = [
        execute_move(UP, board),
        execute_move(DOWN, board),
        execute_move(LEFT, board),
        execute_move(RIGHT, board)
    ]

    for i in range(4):
        new_maxs = [
            np.max(execute_move(UP, new_boards[i])),
            np.max(execute_move(DOWN, new_boards[i])),
            np.max(execute_move(LEFT, new_boards[i])),
            np.max(execute_move(RIGHT, new_boards[i]))
        ]
        new_max[i] = np.max(new_maxs)

    for i in range(4):
        if new_max[i] > max_nr:
            rating[i] = 1 * FACTOR_MERGE_SCORE_2X
    return rating


def validate_merge_score3x(board):
    max_nr = np.max(board)
    rating = [0, 0, 0, 0]
    new_max2x = [0, 0, 0, 0]
    new_max = [0, 0, 0, 0]

    new_boards = [
        execute_move(UP, board),
        execute_move(DOWN, board),
        execute_move(LEFT, board),
        execute_move(RIGHT, board)
    ]

    for i in range(4):
        new_maxs = [
            execute_move(UP, new_boards[i]),
            execute_move(DOWN, new_boards[i]),
            execute_move(LEFT, new_boards[i]),
            execute_move(RIGHT, new_boards[i])
        ]

        for j in range(4):
            new_maxs2x = [
                np.max(execute_move(UP, new_maxs[j])),
                np.max(execute_move(DOWN, new_maxs[j])),
                np.max(execute_move(LEFT, new_maxs[j])),
                np.max(execute_move(RIGHT, new_maxs[j]))
            ]
            new_max2x[j] = np.max(new_maxs2x)
        new_max[i] = np.max(new_max2x)
        new_max2x = [0, 0, 0, 0]

    for i in range(4):
        if new_max[i] > np.max(max_nr):
            rating[i] = 1 * FACTOR_MERGE_SCORE_3X
    return rating


def validate_empty_fields(board):
    return FACTOR_EMPTY_FIELDS * rank_score((16 - np.array([
        np.count_nonzero(execute_move(UP, board)),
        np.count_nonzero(execute_move(DOWN, board)),
        np.count_nonzero(execute_move(LEFT, board)),
        np.count_nonzero(execute_move(RIGHT, board))
    ])).tolist())


def validate_place_biggest_number(board):
    np_board = np.array(board)

    # UP, DOWN, LEFT, RIGHT
    return FACTOR_BORDER * rank_score([
        np_board[0, np.argmax(np_board[0, :])],
        np_board[3, np.argmax(np_board[3, :])],
        np_board[np.argmax(np_board[:, 0]), 0],
        np_board[np.argmax(np_board[:, 3]), 3]
    ])


def validate_end_row(board):
    np_board = np.array(board)

    # UP, DOWN, LEFT, RIGHT
    return FACTOR_BORDER_ROW * rank_score([
        sum(np_board[0, :]),
        sum(np_board[3, :]),
        sum(np_board[:, 0]),
        sum(np_board[:, 3])
    ])


def rank_score(array, total=1.0):
    rank_array_indexes = [0, 0, 0, 0]
    sorted_array = array.copy()
    sorted_array.sort()

    for i in range(4):
        rank_array_indexes[i] = (total / 4) * (sorted_array.index(array[i]) + 1)

    return np.array(rank_array_indexes)


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


if __name__ == '__main__':
    print(rank_score([1, 2, 1, 1]))
