import random
import copy
from time import time
from math import exp

from src.constant import ShapeConstant
from src.model import State

from typing import Tuple, List
from src.ai.ai import AI
from src.utility import place, is_win, is_full

# class LocalSearch:
#     def __init__(self):
#         pass

#     def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
#         self.thinking_time = time() + thinking_time

#         best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm

#         return None

class SimulatedAnnealing(AI):
    """
	A basic AI class that implement minimax and alpha-beta pruning for finding best move in 
	simplexity game. 

	[ATTRIBUTES]
	thinking_time_limit: int -> time when bot must finished searching move.
	This class also inherits attribute from AI class (time_limit, used_time).
	
    [METHOD]
	__init__(time_limit:int):
	Constructor for SimulatedAnnealing classes, Also construct the base AI class.
	find(self, state: State, n_player: int) -> Tuple[str, str]:
	Find the best move for AI using Simulated Annealing algorithm.
	generateRandomMove(state: State) -> Tuple[str, str]:
	Generates a random move based on the current state of the game.
    calculateTemperature() -> float:
    Method to calculate the temperature based on the current time.
    calculateDeltaE(state: State, move: Tuple[str, str]) -> float:
    Method to calculate delta E value used in simulated annealing.
	"""

    def __init__(self) -> None:
        """
        Constructor for SimulatedAnnealing class, is the same as AI class.
        
        [ATTRIBUTES]
        time_limit : int → time limit for finding move.
        """
        pass


    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        """
        Find is a function to find best move using simulated annealing.
            
        [PARAMETER]
        state: State -> current game state.
        n_player :int -> which player (player 1 or 2)

        [RETURN]
        Tuple[str, str] -> the best move for current player.
        """
        self.thinking_time = time() + thinking_time
        self.time_limit = thinking_time

        best_movement = ("0", "-")
        found = False
        while(self.calculateTemperature() > 0):
            successor = self.generateRandomMove(state, n_player)
            delta_e = self.calculateDeltaE(state, successor)
            if(delta_e>0):
                best_movement = successor
                found = True
            else:
                t = self.calculateTemperature()
                if(self.calculateTemperature() <= 0):
                    break
                if(exp(delta_e/t) > 0.5):
                    best_movement = successor
                    found = True

        if(not(found)):
            best_movement = self.generateRandomMove(state, n_player)

        return best_movement

    def generateRandomMove(self, state: State, n_player: int) -> Tuple[str, str]:
        """
        Generates a random move based on the current state of the game
            
        [PARAMETER]
        state: State -> current game state.
            
        [RETURN]
        Tuple[str, str] -> a random move chosen based on the current state.
        """
        if (state.players[n_player].quota[ShapeConstant.CROSS] > 0 and state.players[n_player].quota[ShapeConstant.CIRCLE] > 0 ):
            return (random.randint(0, state.board.col - 1), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))
        elif (state.players[n_player].quota[ShapeConstant.CROSS] > 0):
            return (random.randint(0, state.board.col - 1), ShapeConstant.CROSS)
        elif (state.players[n_player].quota[ShapeConstant.CIRCLE] > 0):
            return (random.randint(0, state.board.col - 1), ShapeConstant.CIRCLE)
        else:
            return (0, "-")

    def calculateTemperature(self) -> float:
        """
        Method to calculate the temperature based on the current time.
            
        [RETURN]
        float -> the temperature value of the current time.
        """
        current_time = time()
        diff = int(self.thinking_time - current_time)
        return (diff/self.time_limit)*100
        
    def calculateDeltaE(self, state: State, move: Tuple[str, str]) -> float:
        """
        Method to calculate delta E value used in simulated annealing.
            
        [PARAMETER]
        state: State -> current game state.
        move: Tuple[str, str] -> move to calculate next state

        [RETURN]
        float -> the temperature value of the current time.
        """
        #TODO ubah fungsi heuristicnya
        n_player = (state.round - 1) % 2
        next_state = copy.deepcopy(state)
        next_state_move = place(next_state, n_player, move[1], move[0])
        return self.calculateValue(state, n_player) - self.calculateValue(next_state, n_player)

    # # Kalo Menang
    # def countObjectiveIsWin(self, state: State, n_player:int):
    #     """
    #     [DESC]
    #         Function to count heuristic function if a winner is found
    #     [PARAMS]
    #         state: State -> current State
    #     [RETURN]
    #         0 if draw
    #         +(21-player.quota)*2 if PLayer_1 can win
    #         -(21-player.quota)*2 if Player_2 can win
    #     """
    #     return super().countObjectiveIsWin(state, n_player)
    
    # def countObjectiveIsWin(self, state: State, n_player:int) -> int:
    #     """
    #     [DESC]
    #         Function to count heuristic function if a winner is found
    #     [PARAMS]
    #         state: State -> current State
    #     [RETURN]
    #         0 if draw
    #         +(21-player.quota)*2 if PLayer_1 can win
    #         -(21-player.quota)*2 if Player_2 can win
    #     """
    #     print(n_player)
    #     winner = is_win(state.board)
    #     if winner:
    #         remainder = 0
    #         for k, v in state.players[n_player].quota.items():
    #             remainder += v
    #         score = (remainder+1)*2
    #         if(n_player == 1):
    #             score = score*(-1)
    #         return score
    #     if is_full(state.board):
    #         #Draw
    #         return 0
    #     return 0