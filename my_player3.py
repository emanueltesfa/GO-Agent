from operator import truediv
from os import stat
import random
import sys
from read import readInput
from write import writeOutput
import numpy as np
import time
from numpy.random import normal
from host import GO

start = time.time()
MAX, MIN = 1000, -1000


class RandomPlayer():
    def __init__(self, piece_type):
        self.type = 'random'
        self.piece_type = piece_type

    
    def get_input(self, go, piece_type):
        if go.game_end(self.piece_type) == True:
            return "PASS"
        
        numPieces = 0
        valid_places = 0
        for i in range(go.size):
            for j in range(go.size):
                if go.board[i][j] != 0:
                    numPieces += 1
                if go.valid_place_check(i, j, self.piece_type, test_check=False):
                    valid_places += 1
        if valid_places == 0:
            return "PASS"
        
        max_depth =  int((2 ** (numPieces / 10) ) + 2)

        if go.valid_place_check(1, 1, self.piece_type, test_check=False): return [1,1]
        if go.valid_place_check(2, 2, self.piece_type, test_check=False): return [2,2] 
        if go.valid_place_check(3, 3, self.piece_type, test_check=False): return [3,3] 
        if go.valid_place_check(3, 1, self.piece_type, test_check=False): return [3,1]
        if go.valid_place_check(1, 3, self.piece_type, test_check=False): return [1,3]
   
        best_score = -np.inf
        best_move = [-1, -1]
        temp_board = go.copy_board()

        mid_point_time = 0
        for i in range(temp_board.size):
            for j in range(temp_board.size):
                
                temp_board = go.copy_board()
                if temp_board.valid_place_check(i, j, self.piece_type, test_check=False):
                    temp_board.place_chess(i, j, self.piece_type)
                    temp_board.died_pieces = temp_board.remove_died_pieces(3 - self.piece_type)
                    #temp_board.visualize_board()
                    score = self.minimax(temp_board, 0, False, 3- self.piece_type, max_depth, -np.inf, np.inf, 0)

                    if score > best_score :
                        best_score = score
                        best_move = i, j
                        if score == 1000:
                            return  best_move
                    
                # check if move is too close to 10 seconds 
                mid_point_time = time.time() 
                if (mid_point_time - start) > 9.9: # return current best if near overtime! 
                    return best_move
                    
        
        if best_move == [-1,-1]:
            return "PASS"
        return best_move

    def minimax(self, temp_go, depth, isMax,piece_type, max_depth, alpha, beta, counter):
        mid_point_time = time.time() 
        if (mid_point_time - start) > 9.7: # return current best if near overtime! 
            return calc_score(temp_go, self.piece_type)
        
        if temp_go.game_end(self.piece_type) == True:
            print("Terminal State")
        
        if depth >=  max_depth :
            # calc score funtion
            mid_game_score = calc_score(temp_go, self.piece_type)
            return mid_game_score

        if isMax:
            best_score = -np.inf
            best = MIN
            for i in range(temp_go.size):
                for j in range(temp_go.size):
                    counter +=1
                    temp_go_max = temp_go.copy_board()

                    if temp_go_max.valid_place_check(i, j, self.piece_type, test_check=False):
                        temp_go_max.place_chess(i, j, self.piece_type)
                        temp_go_max.died_pieces = temp_go_max.remove_died_pieces(3 - self.piece_type)
                        score = self.minimax(temp_go_max, depth + 1, False, 3- self.piece_type, max_depth, alpha, beta, counter)
                        
                        if score > best_score:
                            best_score = score
                        
                        best = max(best, best_score)
                        alpha = max(alpha, best)
            
                        # Alpha Beta Pruning
                        if beta <= alpha:
                            return score
                if beta <= alpha:
                    return score
            return best_score
        else: # mini 
            best_score = np.inf
            best = MAX
            for i in range(temp_go.size):
                for j in range(temp_go.size):
                    temp_go_mini = temp_go.copy_board()
                    counter +=1

                    if temp_go_mini.valid_place_check(i, j, self.piece_type, test_check=False):
                        temp_go_mini.place_chess(i, j, 3 - self.piece_type)
                        temp_go_mini.died_pieces = temp_go_mini.remove_died_pieces(3 - self.piece_type)
                        score = self.minimax(temp_go_mini, depth + 1, True, 3 - self.piece_type, max_depth, alpha, beta, counter)
                      
                        if score < best_score:
                            best_score = score
                        
                        #Alpha Beta Pruning
                        best = min(best, best_score)
                        beta = min(beta, best)
            
                        # Alpha Beta Pruning
                        if beta <= alpha:
                            return score
                if beta <= alpha:
                    return score

            return best_score

  
def calc_score( go, piece_type ):
    # find_liberty
  
    score = 0 
    tempScore = go.score(piece_type)
    died_pieces = go.died_pieces 
    dead_piece_score = 0
    rem_piece_type = None
    if piece_type == 1 and go.judge_winner == 1:
        return 500

    for i in range(go.size):
        for j in range(go.size):
            if go.board[i][j] == piece_type: 
                temp_neigh = go.detect_neighbor(i,j)
                for z in temp_neigh:
                    if go.board[z[0]][z[1]] == 0: # if empty 
                        score += 1 

    score = score + tempScore + (100 * len(died_pieces))
    return score



def is_overtime():
    mid_point_time = time.time() 
    if (mid_point_time - start) > 9.5: # return current best if near overtime! 
        print('overtime!')
        print(f"{(mid_point_time-start)*10**3:.03f}")
        print (mid_point_time - start, "\n")
        #time.sleep(5)
        return True
    else: 
        return False

if __name__ == "__main__":
    N = 5
    #time.sleep(5)
    piece_type, previous_board, board = readInput(N)
    go = GO(N)
    go.set_board(piece_type, previous_board, board)
    player = RandomPlayer(piece_type)
    action = player.get_input(go, piece_type)
    #time.sleep(10)
    end = time.time()
    print(f"Move took:\tTime taken: {(end-start)*10**3:.03f}ms")
    writeOutput(action)
