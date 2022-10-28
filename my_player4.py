import random
import sys
from read import readInput
from write import writeOutput
import numpy as np


from host import GO

# minimax


class RandomPlayer():
    def __init__(self):
        self.type = 'random'

    def get_input(self, go, piece_type):
        '''
        Get one input.

        :param go: Go instance.
        :param piece_type: 1('X') or 2('O').
        :return: (row, column) coordinate of input.
        '''
        #possible_placements = []
        # print(go.score(piece_type))

        #place_chess or go.copy_board()

        best_score = -np.inf
        best_move = [-1, -1]
        temp_board = go.copy_board()

        for i in range(temp_board.size):
            for j in range(temp_board.size):
                if temp_board.valid_place_check(i, j, piece_type, test_check=False):
                    #possible_placements.append((i, j))
                    temp_board.place_chess(i, j, piece_type)
                    temp_board.visualize_board()
                    score = minimax(temp_board, 0, True, piece_type)

                    if score > best_score:
                        score = best_score
                        best_move = [i, j]

        """if not possible_placements:
            return "PASS"
        else:
            return random.choice(possible_placements)"""
        return best_move


def minimax(temp_go, depth, isMax, piece_type):
    # generate game tree
    # check if next move wins
    # then check if isMax == true
    #temp_board = temp_go.copy_board()

    if isMax:
        best_score = -np.inf

        for i in range(temp_go.size):
            for j in range(temp_go.size):
                if temp_go.valid_place_check(i, j, piece_type, test_check=False):
                    temp_go.place_chess(i, j, piece_type)
                    score = minimax(temp_go, 0, False, piece_type)

                    if score > best_score:
                        best_score = score
        return best_score
    else:
        best_score = np.inf

        for i in range(temp_go.size):
            for j in range(temp_go.size):
                if temp_go.valid_place_check(i, j, piece_type, test_check=False):
                    temp_go.place_chess(i, j, piece_type)
                    score = minimax(temp_go, 0, True, piece_type)

                    if score < best_score:
                        best_score = score
        return best_score


if __name__ == "__main__":
    N = 5
    piece_type, previous_board, board = readInput(N)
    go = GO(N)
    go.set_board(piece_type, previous_board, board)
    player = RandomPlayer()
    action = player.get_input(go, piece_type)
    writeOutput(action)
