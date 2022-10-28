import datetime
import os
import pickle
import shutil
from copy import deepcopy

import numpy as np

from Game import Game
from host import judge
from random_player import getRandomMove
from read import readInput
from QLearner import getQLearningMove, QLearn_learn
from torch.utils.tensorboard import SummaryWriter

verbose = False


def play_white(piece_type, previous_board, board, q_table):
    moves = 0
    game = Game()
    if debug: print('Start play White')
    while True:
        if debug: print("Before black", piece_type)
        if debug: print('Black makes move...')
        action = getRandomMove(piece_type, previous_board, board)
        moves += 1

        rst, piece_type, previous_board, board = judge(moves, verbose, piece_type, previous_board, board, action)

        if rst != 0:
            break
        if debug: print("Before white", piece_type)
        if debug: print('White makes move...')
        action, q_table, game = getQLearningMove(q_table, game, piece_type, previous_board, board)
        moves += 1

        rst, piece_type, previous_board, board = judge(moves, verbose, piece_type, previous_board, board, action)

        if rst != 0:
            break

    return rst, q_table, game


def play_black(piece_type, previous_board, board, q_table):
    moves = 0
    game = Game()
    while True:
        if debug: print("Before black", piece_type)
        if debug: print('Black makes move...')
        action, q_table, game = getQLearningMove(q_table, game, piece_type, previous_board, board)
        moves += 1
        rst, piece_type, previous_board, board = judge(moves, verbose, piece_type, previous_board, board, action)

        if rst != 0:
            break

        if debug: print("Before white", piece_type)
        if debug: print('White makes move...')
        action = getRandomMove(piece_type, previous_board, board)
        moves += 1

        rst, piece_type, previous_board, board = judge(moves, verbose, piece_type, previous_board, board, action)

        if rst != 0:
            break

    return rst, q_table, game


if __name__ == "__main__":
    writer = SummaryWriter()

    N = 5
    shutil.copy(r"init/input.txt", r"input.txt")
    piece_type_master_copy, previous_board_master_copy, board_master_copy = readInput(N)

    q_table_file = open('QTables/Testing', 'rb')
    q_table = pickle.load(q_table_file)
    q_table_file.close()
    debug = False

    for i in range(10000):

        you_win_w = 0
        opp_win_w = 0
        you_lose_w = 0
        opp_lose_w = 0
        you_tie_w = 0
        opp_tie_w = 0

        you_win_b = 0
        opp_win_b = 0
        you_lose_b = 0
        opp_lose_b = 0
        you_tie_b = 0
        opp_tie_b = 0

        num_games = 10

        start = datetime.datetime.now()
        for game_i in range(num_games):
            if debug: print("Black:TA White:You")
            piece_type, previous_board, board = deepcopy(piece_type_master_copy), \
                                                deepcopy(previous_board_master_copy), \
                                                deepcopy(board_master_copy)
            winner, q_table, game = play_white(piece_type, previous_board, board, q_table)

            if winner == 2:
                print("You Won on White")
                you_win_w += 1
                opp_lose_w += 1
            elif winner == 1:
                print("You Lost on White")
                opp_win_w += 1
                you_lose_w += 1
            else:
                print("You Tied on White")
                you_tie_w += 1
                opp_tie_w += 1
            piece_type = 2
            q_table = QLearn_learn(q_table, game, piece_type, winner, board)

            piece_type, previous_board, board = deepcopy(piece_type_master_copy), \
                                                deepcopy(previous_board_master_copy), \
                                                deepcopy(board_master_copy)

            if debug: print("Black:You White:TA")
            winner, q_table, game = play_black(piece_type, previous_board, board, q_table)

            if winner == 1:
                print("You Won on Black")
                you_win_b += 1
                opp_lose_b += 1
            elif winner == 2:
                print("You Lose on Black")
                opp_win_b += 1
                you_lose_b += 1
            else:
                print("You Tie on Black")
                you_tie_b += 1
                opp_tie_b += 1
            piece_type = 1
            q_table = QLearn_learn(q_table, game, piece_type, winner, board)
            if i % 50 == 0:
                q_table_file = open(f'QTables/MatchTesting', 'wb')
                pickle.dump(q_table, q_table_file)
                q_table_file.close()
        end = datetime.datetime.now()
        if debug: print(end - start)

        writer.add_scalar('Win on Black', you_win_b, i * num_games)
        writer.add_scalar('Loss on Black', you_lose_b, i * num_games)
        writer.add_scalar('Tie on Black', you_tie_b, i * num_games)

        writer.add_scalar('Win on White', you_win_w, i * num_games)
        writer.add_scalar('Loss on White', you_lose_w, i * num_games)
        writer.add_scalar('Tie on White', you_tie_w, i * num_games)

        # if debug: print(f"You:   Win: {you_win},   Tie: {you_tie},  Lose: {you_lose}")
        # print(f"Opp:   Win: {opp_win},   Tie: {opp_tie},  Lose: {opp_lose}")
    q_table_file = open(f'QTables/MatchTesting', 'wb')
    pickle.dump(q_table, q_table_file)
    q_table_file.close()
    print(q_table['000000000'])
    print('Win on Black', you_win_b)
    print('Loss on Black', you_lose_b)
    print('Tie on Black', you_tie_b)

    print('Win on White', you_win_w)
    print('Loss on White', you_lose_w)
    print('Tie on White', you_tie_w)