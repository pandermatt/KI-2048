#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author:      chrn (original by nneonneo)
# Date:        11.11.2016, updated by scik 30.08.2019
# Copyright:   https://github.com/nneonneo/2048-ai
# Description: Helps the user achieve a high score in a real game of 2048 by using a move searcher.
#              This Script initialize the AI and controls the game flow.


# from __future__ import print_function

import time

#import heuristicai as ai  # for task 4
import searchai as ai #for task 5
# import heuristicai_SOLUTION as ai #for task 4
# import searchai_SOLUTION as ai #for task 5

def print_board(m):
    for row in m:
        for c in row:
            print('%8d' % c, end=' ')
        print()


def _to_val(c):
    if c == 0: return 0
    return c


def to_val(m):
    return [[_to_val(c) for c in row] for row in m]


def _to_score(c):
    if c <= 1:
        return 0
    return (c - 1) * (2 ** c)


def to_score(m):
    return [[_to_score(c) for c in row] for row in m]


def find_best_move(board):
    return ai.find_best_move(board)


def movename(move):
    return ['up', 'down', 'left', 'right'][move]


def play_game(gamectrl):
    moveno = 0
    start = time.time()
    while 1:
        state = gamectrl.get_status()
        if state == 'ended':
            # from subprocess import call
            # call(["screencapture", str(time.time()) + ".jpg"])
            break
        elif state == 'won':
            time.sleep(0.75)
            gamectrl.continue_game()

        moveno += 1
        board = gamectrl.get_board()
        move = find_best_move(board)
        if move < 0:
            break
        print("%010.6f: Score %d, Move %d: %s" % (time.time() - start, gamectrl.get_score(), moveno, movename(move)))
        gamectrl.execute_move(move)

    score = gamectrl.get_score()
    board = gamectrl.get_board()
    maxval = max(max(row) for row in to_val(board))
    end = time.time()
    avgtime = 1.0*(end-start)/moveno
    print(f'Game over. Final score {score}; highest tile {maxval}. Average Time: {avgtime}')
    return board, Scores(score, maxval)


def parse_args(argv):
    import argparse

    parser = argparse.ArgumentParser(description="Use the AI to play 2048 via browser control")
    parser.add_argument('-p', '--port', help="Port number to control on (default: 32000 for Firefox, 9222 for Chrome)",
                        type=int)
    parser.add_argument('-b', '--browser',
                        help="Browser you're using. Only Firefox with the Remote Control extension, and Chrome with remote debugging (default), are supported right now.",
                        default='chrome', choices=('firefox', 'chrome'))
    parser.add_argument('-k', '--ctrlmode',
                        help="Control mode to use. If the browser control doesn't seem to work, try changing this.",
                        default='hybrid', choices=('keyboard', 'fast', 'hybrid'))

    return parser.parse_args(argv)


def main(argv):
    args = parse_args(argv)

    if args.browser == 'firefox':
        from ffctrl import FirefoxRemoteControl
        if args.port is None:
            args.port = 32000
        ctrl = FirefoxRemoteControl(args.port)
    elif args.browser == 'chrome':
        from chromectrl import ChromeDebuggerControl
        if args.port is None:
            args.port = 9222
        ctrl = ChromeDebuggerControl(args.port)

    # if args.ctrlmode == 'keyboard':
    #     from gamectrl import Keyboard2048Control
    #     gamectrl = Keyboard2048Control(ctrl)
    # elif args.ctrlmode == 'fast':
    #     from gamectrl import Fast2048Control
    #     gamectrl = Fast2048Control(ctrl)
    # elif args.ctrlmode == 'hybrid':
    #     from gamectrl import Hybrid2048Control
    #     gamectrl = Hybrid2048Control(ctrl)
    from gamectrl import Fast2048Control
    gamectrl = Fast2048Control(ctrl)

    if gamectrl.get_status() == 'ended':
        gamectrl.restart_game()

    score_list = []
    high_score = 0
    sum_tile = 0
    sum_score = 0
    iterations = 10
    for i in range(iterations):
        board, game = play_game(gamectrl)
        score_list.append(game)
        with open("score.txt", "a") as myfile:
            myfile.write("Score %d \n" % game.final_score)
            myfile.write("Tile %d \n" % game.maxval)
            myfile.write("Board:\n")
            myfile.write(str(board))
            myfile.write("\n --------------\n")
            myfile.close()
        if high_score < game.final_score:
            high_score = game.final_score
        time.sleep(0.3)
        gamectrl.restart_game()
    for score in score_list:
        sum_tile = sum_tile + score.maxval
        sum_score = sum_score + score.final_score
        print("Score %d; highest tile %d." % (score.final_score, score.maxval))
    print("Final score %d" % high_score)
    print("Avg score %d" % (sum_score / iterations))
    print("Avg Tile %d" % (sum_tile / iterations))


class Scores:
    def __init__(self, final_score, maxval):
        self.final_score = final_score
        self.maxval = maxval


if __name__ == '__main__':
    import sys

    exit(main(sys.argv[1:]))
