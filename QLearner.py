import numpy as np

WIN_REWARD = 1.0
DRAW_REWARD = 0.5
LOSS_REWARD = 0.0


class QLearner:

    GAME_NUM = 100000

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
        state = board.encode_state() #####################################
        q_values = self.Q(state)
        row, col = 0, 0
        curr_max = -np.inf
        while True:
            i, j = self._find_max(q_values)
            if board.valid_place_check(i, j, piece_type):
                return i, j
            else:
                q_values[i][j] = -1.0

    def _find_max(self, q_values):
        curr_max = -np.inf
        row, col = 0, 0
        for i in range(0, 5):
            for j in range(0, 5):
                if q_values[i][j] > curr_max:
                    curr_max = q_values[i][j]
                    row, col = i, j
        print(row,col)
        return row, col

    def move(self, board, piece_type):
        """ make a move
        """
        if board.game_end(piece_type):
            return
        row, col = self._select_best_move(board, piece_type)
        self.history_states.append((board.encode_state(), (row, col)))
        return row, col

    def learn(self, board):
        """ when games ended, this method will be called to update the qvalues
        """
        if board.judge_winner == 0:
            reward = DRAW_REWARD
        elif board.judge_winner == self.side:
            reward = WIN_REWARD
        else:
            reward = LOSS_REWARD
        self.history_states.reverse()
        max_q_value = -1.0
        for hist in self.history_states:
            print("enter learn")

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
        #print(q)
