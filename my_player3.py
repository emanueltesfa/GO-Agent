import argparse
import random
import sys
from read import readInput
from write import writeOutput
from host import GO
import numpy as np
import pickle
import os


WIN_REWARD = 1.0
DRAW_REWARD = 0.5
LOSS_REWARD = 0.0
BOARD_SIZE = 5


def encode_state(instance):
    """ Encode the current state of the board as a string
        """
    return ''.join([str(instance.board[i][j]) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)])


class QLearner:

    GAME_NUM = 100000
    BOARD_SIZE = 5

    def __init__(self, alpha=.7, gamma=.9, initial_value=0.5, side=None):
        if not (0 < gamma <= 1):
            raise ValueError("An MDP must have 0 < gamma <= 1")

        self.side = side
        self.alpha = alpha
        self.gamma = gamma
        self.q_values = {}
        self.history_states = []
        self.initial_value = initial_value
        # self.state = ?

    def set_side(self, side):
        self.side = side

    def Q(self, state):
        if state not in self.q_values:
            q_val = np.zeros((5, 5))
            q_val.fill(self.initial_value)
            self.q_values[state] = q_val
        return self.q_values[state]

    def _select_best_move(self, board, piece_type):
        state = encode_state(board)
        q_values = self.Q(state)
        row, col = 0, 0
        curr_max = -np.inf
        count = 0
        while count < 26:
            i, j = self._find_max(q_values)
            #print("loop best move")
            # board.visualize_board()
            #print(board.valid_place_check(i, j, piece_type))
            #print(i, j)
            if board.valid_place_check(i, j, piece_type):
                return i, j
            else:
                q_values[i][j] = -1.0
                """if i == 0 and j == 0:
                return None, None"""
            count += 1

    def _find_max(self, q_values):
        curr_max = -np.inf
        row, col = 0, 0
        for i in range(0, 5):
            for j in range(0, 5):
                if q_values[i][j] > curr_max:
                    curr_max = q_values[i][j]
                    row, col = i, j
                    if q_values[i][j] == -1.0 or curr_max == -np.inf:
                        continue
            if q_values[i][j] == -1.0 or curr_max == -np.inf:
                continue
        #print("loop findmax")
        return row, col

    def move(self, board, piece_type):
        """ make a move
        """
        if board.game_end(piece_type):
            return
        row, col = self._select_best_move(board, piece_type)
        if row == None and col == None:
            return
        temp_key = encode_state(board)
        self.history_states.append((temp_key, (row, col)))
        #print("loop move")

        pickle.dump(self.history_states, open(
            "temp_qval_hist.txt", "wb"))  # to send

        # favorite_color = pickle.load(open("save.p", "rb"))

        return row, col

    def learn(self, board, winner, piece_type):
        """ when games ended, this method will be called to update the qvalues
        Param: piece_type ,1('X') or 2('O') 
        """

        # im x = 1 = black and winner = 1 then win reward
        # im o = 2 = white and winner = 2 then win reward
        print("enter the learn")
        if winner == '0':
            reward = DRAW_REWARD
        elif winner == '1' and piece_type == 1:
            reward = WIN_REWARD
        elif winner == '1' and piece_type == 2:
            reward = LOSS_REWARD
        elif winner == '2' and piece_type == 2:
            reward = WIN_REWARD
        elif winner == '1' and piece_type == 2:
            reward = LOSS_REWARD
        else:
            reward = LOSS_REWARD
        self.history_states.reverse()
        max_q_value = -1.0

        print("Winner: ", type(winner),"PieceType: ",  type(piece_type), "Reward: ", reward)
        for hist in self.history_states:
            print("Enter history of states")
            state, move = hist
            q = self.Q(state)
            if max_q_value < 0:
                q[move[0]][move[1]] = reward
            else:
                q[move[0]][move[1]] = q[move[0]][move[1]] * \
                    (1 - self.alpha) + self.alpha * self.gamma * max_q_value
            max_q_value = np.max(q)
            print("q is: ", q)
        self.history_states = []
        open('temp_qval_hist.txt', 'w').close() # clear contents of my file, only need history of states for learn then reset 
        # print(q)


class RandomPlayer():
    def __init__(self):
        self.type = 'random'

    def get_input(self, go, piece_type, qLearner):
        return qlearner.move(go, piece_type)


if __name__ == "__main__":
    # if arg # do new function learn #else move
    parser = argparse.ArgumentParser()
    parser.add_argument("--learn", "-l", type=str)
    parser.add_argument("--winner", "-w", type=str)
    args = parser.parse_args()
    print("arg winner and learn is: ",  args.learn, args.winner)

    qlearner = QLearner()
    N = 5
    piece_type, previous_board, board = readInput(N)
    go = GO(N)
    go.set_board(piece_type, previous_board, board)
    player = RandomPlayer()
    
    bool_empty = os.stat("temp_qval_hist.txt").st_size == 0
    if (bool_empty) == False:
        qlearner.history_states = pickle.load(open("temp_qval_hist.txt", "rb"))
    print(len(qlearner.history_states))

    if args.learn == "T":
        # learn
        qlearner.learn(board, args.winner, piece_type)
    else:
        action = player.get_input(go, piece_type, qlearner)
        writeOutput(action)
