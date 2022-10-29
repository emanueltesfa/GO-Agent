import random
import sys
from read import readInput
from write import writeOutput
import numpy as np
import time

from host import GO

# minimax


class RandomPlayer():
    def __init__(self, piece_type):
        self.type = 'random'
        self.piece_type = piece_type

    
    def get_input(self, go, piece_type):
        '''
        Get one input.

        :param go: Go instance.
        :param self.piece_type: 1('X') or 2('O').
        :return: (row, column) coordinate of input.
        '''
        #possible_placements = []
        # print(go.score(self.piece_type))

        #place_chess or go.copy_board()



        best_score = -np.inf
        best_move = [-1, -1]
        temp_board = go.copy_board()
        #print(type(go))
        #print(type(temp_board))
        count = 0
        for i in range(temp_board.size):
            for j in range(temp_board.size):
                
                count += 1
                
                temp_board = go.copy_board()

                #print(i, j)
                if temp_board.valid_place_check(i, j, self.piece_type, test_check=False):
                    temp_board.place_chess(i, j, self.piece_type)
                    temp_board.died_pieces = temp_board.remove_died_pieces(3 - self.piece_type)
                    #temp_board.visualize_board()
                    score = self.minimax(temp_board, 0, False, 3- self.piece_type)

                    #print("score is: ", score, "best score is: ", best_move)
                    #print("score for board is: ", score)

                    if score > best_score :
                        #print("\n\n\nenter best score update \n\n\n")
                        best_score = score
                        #print("current i and j is: ", i , j)
                        best_move = i, j
                        #print("best move is: ",best_move, best_score)
                        # time.sleep(10)
        
        #print("Count is: ", count)
        if best_move == [-1,-1]:
            return "PASS"
        #print("\n\n\n RETURNED SCORE", best_score)
        #print("\n\n\n move i: ", best_move)
        return best_move

    def minimax(self, temp_go, depth, isMax,piece_type):
    
        if temp_go.judge_winner() == 1:
            # print ( " \n\n\n is a winner state \n\n\n")
            return 100
        elif temp_go.judge_winner() == 0:
            return 0 
        elif temp_go.judge_winner() == -1:
            return -100
        

        #print('depth is ', depth)
        if depth >= 2:
            # calc score funtion
            mid_game_score = calc_score(temp_go, self.piece_type)
            #print("\n\n\nFINAL SCORE", mid_game_score)
            return mid_game_score

        if isMax:
            best_score = -np.inf
            count = 0 
            for i in range(temp_go.size):
                for j in range(temp_go.size):
                    count += 1
                    #print( count , "max" , i, j)
                    temp_go_max = temp_go.copy_board()

                    if temp_go_max.valid_place_check(i, j, self.piece_type, test_check=False):
                        temp_go_max.place_chess(i, j, self.piece_type)
                        temp_go_max.died_pieces = temp_go_max.remove_died_pieces(3 - self.piece_type)
                        # temp_go_max.visualize_board()

                        score = self.minimax(temp_go_max, depth + 1, False, 3- self.piece_type)
                        # print("recursive max")

                        #temp_go_max.visualize_board()
#change wieghts
# changre heurtsic mid game 
                        #print("score for board is: ", score)
                        if score > best_score:
                            #print("enter max update!")

                            best_score = score
            return best_score
        else: # mini 
            best_score = np.inf
            count = 0 
            for i in range(temp_go.size):
                for j in range(temp_go.size):
                    count += 1 
                    #print(count, "min", i, j)
                    temp_go_mini = temp_go.copy_board()

                    if temp_go_mini.valid_place_check(i, j, self.piece_type, test_check=False):
                        #print("recursive")
                        temp_go_mini.place_chess(i, j, 3- self.piece_type)
                        temp_go_mini.died_pieces = temp_go_mini.remove_died_pieces(3 - self.piece_type)
                        #temp_go_mini.visualize_board()

                        score = self.minimax(temp_go_mini, depth + 1, True, 3 - self.piece_type)
                        #temp_go.visualize_board()

                        #print("score for board is: ", score)
                        if score < best_score:
                            #print("enter mini update!")
                            best_score = score
            return best_score

def calc_score ( go, piece_type ):
    # find_liberty
    score = 0 
    for i in range(go.size):
        for j in range(go.size):

            if go.board[i][j] == piece_type: 
                temp_neigh = go.detect_neighbor(i,j)
                for z in temp_neigh:
                    #print(z)
                    #print(len(z))
                    if go.board[z[0]][z[1]] == 0: # if empty 
                        score += 1 
    
    #print("score: ", score)
    tempScore = go.score(piece_type)
    score = score + tempScore
    #print("tempScore: ", tempScore)
    #print("final score: " , score)
    return score


if __name__ == "__main__":
    N = 5
    piece_type, previous_board, board = readInput(N)
    go = GO(N)
    go.set_board(piece_type, previous_board, board)
    player = RandomPlayer(piece_type)
    action = player.get_input(go, piece_type)
    #time.sleep(10)
    writeOutput(action)
