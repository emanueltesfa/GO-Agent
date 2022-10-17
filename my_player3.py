import random
import sys
from read import readInput
from write import writeOutput
from QLearner import QLearner

from host import GO


class RandomPlayer():
    def __init__(self):
        self.type = 'random'
              

    def get_input(self, go, piece_type, qLearner):
        possible_placements = []
        """for i in range(go.size):
            for j in range(go.size):
                if go.valid_place_check(i, j, piece_type, test_check=True):
                    possible_placements.append((i, j)) #returns random index ex. (3,3)"""

        # print(possible_placements)
        # go.score()

        
        #print(qlearner.move(go, piece_type))
       
        #print(go.game_end)
        #while not go.game_end:
           # print()

        #self.qlearner.move(go)
        #print("ello")
        
        return qlearner.move(go, piece_type)
        
        print("type of piece_type", (piece_type))
        


       


if __name__ == "__main__":
    #if arg # do new function learn #else move
    qlearner = QLearner()
    N = 5
    piece_type, previous_board, board = readInput(N)
    go = GO(N)
    go.set_board(piece_type, previous_board, board)
    player = RandomPlayer()
    action = player.get_input(go, piece_type, qlearner)
     
    writeOutput(action)
