from os import stat
import random
import sys
from read import readInput
from write import writeOutput
import numpy as np
import time

from host import GO

start = time.time()
MAX, MIN = 1000, -1000
# minimax


class RandomPlayer():
    def __init__(self, piece_type):
        self.type = 'random'
        self.piece_type = piece_type

    
    def get_input(self, go, piece_type):

        

        numPieces = 0
        for i in range(go.size):
            for j in range(go.size):
                if go.board[i][j] != 0:
                    numPieces += 1
        
        max_depth =  int((2 ** (numPieces / 10) ) + 3)
        if numPieces == 0 or numPieces == 1:
            if go.valid_place_check(1, 1, self.piece_type, test_check=False):
                return [1,1]

        print("DPETH WOULD BE: ", max_depth, "AT PIECE COUNT OF: ", numPieces)

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
                        if score == 100:
                            return  best_move
                        #print("best move is: ",best_move, best_score)
                        # time.sleep(10)
                    
                # check if move is too close to 10 seconds 
                mid_point_time = time.time() 
                if (mid_point_time - start) > 9.9: # return current best if near overtime! 
                    print('overtime!')
                    print(f"{(mid_point_time-start)*10**3:.03f}")
                    print (mid_point_time - start, "\n")
                    time.sleep(5)
                    return best_move
                    

        
        if best_move == [-1,-1]:
            return "PASS"
        #print("\n\n\n RETURNED SCORE", best_score)
        #print("\n\n\n move i: ", best_move)
        if len(temp_board.died_pieces  ) > 0:
            print("NUM OF KILLED PIECES WITH MOVE POITENTIALLY OR LITERALLY: ", temp_board.died_pieces, len(temp_board.died_pieces))
            time.sleep(5)
        return best_move

    def minimax(self, temp_go, depth, isMax,piece_type, max_depth, alpha, beta, counter):
    
        if temp_go.judge_winner() == 1:
            #print ( " \n\n\n is a WINNER MINIMAX state \n\n\n")
            return 100
        elif temp_go.judge_winner() == 0:
            return 0 
        elif temp_go.judge_winner() == -1:
            #print ( " \n\n\n is a LOSING MINIMAX state \n\n\n")

            return -100
        

        #print('current depth is ', depth, "Max depth: ", max_depth)
        if depth >=  max_depth :
            # calc score funtion
            mid_game_score = calc_score(temp_go, self.piece_type)
            #print("\n\n\nFINAL SCORE", mid_game_score)
            return mid_game_score

        if isMax:
            best_score = -np.inf
            best = MAX
            for i in range(temp_go.size):
                for j in range(temp_go.size):
                    counter +=1
                    temp_go_max = temp_go.copy_board()

                    if temp_go_max.valid_place_check(i, j, self.piece_type, test_check=False):
                        temp_go_max.place_chess(i, j, self.piece_type)
                        temp_go_max.died_pieces = temp_go_max.remove_died_pieces(3 - self.piece_type)
                        #temp_go_max.visualize_board()
                        # print("COUNTER: ", counter)
                        score = self.minimax(temp_go_max, depth + 1, False, 3- self.piece_type, max_depth, alpha, beta, counter)
                        #temp_go_max.visualize_board()
#change wieghts
# changre heurtsic mid game 
                        #print("score for board is: ", score)
                        if score > best_score:
                            #print("enter max update!")

                            best_score = score
                        
                        best = max(best, score)
                        alpha = max(alpha, best)
            
                        # Alpha Beta Pruning
                        if beta <= alpha:
                            #print("breaking loop")
                            break
                if beta <= alpha:
                    #print("breaking loop")
                    break
            return best_score
        else: # mini 
            best_score = np.inf
            best = MIN
            for i in range(temp_go.size):
                for j in range(temp_go.size):
                    temp_go_mini = temp_go.copy_board()
                    counter +=1

                    if temp_go_mini.valid_place_check(i, j, self.piece_type, test_check=False):
                        #print("recursive")
                        temp_go_mini.place_chess(i, j, 3- self.piece_type)
                        temp_go_mini.died_pieces = temp_go_mini.remove_died_pieces(3 - self.piece_type)
                        """if len(temp_go_mini.died_pieces  ) > 0:
                            temp_go_mini.visualize_board()"""

                        score = self.minimax(temp_go_mini, depth + 1, True, 3 - self.piece_type, max_depth, alpha, beta, counter)
                      
                        #print("score for board is: ", score)
                        if score < best_score:
                            #print("enter mini update!")
                            best_score = score
                        
                        #Alpha Beta Pruning
                        best = min(best, score)
                        beta = min(beta, best)
            
                        # Alpha Beta Pruning
                        if beta <= alpha:
                            #print("breaking loop")
                            break
                if beta <= alpha:
                    #print("breaking loop")
                    break

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
    num_died_pieces = go.died_pieces 
    """if len(num_died_pieces ) > 0:

        go.visualize_board()
        print(num_died_pieces)"""
    
    score = score + tempScore + (3 * len(num_died_pieces))
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
    end = time.time()
    print(f"Move took:\tTime taken: {(end-start)*10**3:.03f}ms")
    writeOutput(action)
