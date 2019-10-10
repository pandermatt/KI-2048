from heuristicai import check_snake, check_border, check_empty_fields, check_biggest_number, check_smoothness, \
    check_total_occurrence, check_count_occurrence, check_mean_occurrence, check_snake_look_ahead, board_equals, \
    execute_move


def _run_benchmark(board):
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

    for func in score_methods:
        import csv
        file = r'' + func[0].__name__ + '.csv'
        with open(file, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([_execute_possible_move(i, board, func[0]) * func[1] for i in range(4)])


def _execute_possible_move(direction, board, func):
    new_board = execute_move(direction, board)
    if board_equals(board, new_board):
        return 0
    return func(new_board)
