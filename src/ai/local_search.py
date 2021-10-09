import random
import copy
from time import time
from math import exp

from src.constant import ShapeConstant
from src.model import State

from typing import Tuple, List
from ai import AI
from src.utility import countObjectiveIsWin, place

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

    def __init__(self, time_limit:int) -> None:
        """
        Constructor for SimulatedAnnealing class, is the same as AI class.
        
        [ATTRIBUTES]
        time_limit : int → time limit for finding move.
        """
        AI.__init__(self, time_limit)


    def find(self, state: State, n_player: int) -> Tuple[str, str]:
        """
        Find is a function to find best move using simulated annealing.
            
        [PARAMETER]
        state: State -> current game state.
        n_player :int -> which player (player 1 or 2)

        [RETURN]
        Tuple[str, str] -> the best move for current player.
        """
        best_movement = ("-", "0")
        found = False
        while(self.calculateTemperature() > 0):
            successor = self.generateRandomMove(state)
            delta_e = self.calculateDeltaE(state, successor)
            if(delta_e>0):
                best_movement = successor
                found = True
            else:
                t = self.calculateTemperature()
                if(exp(delta_e/t) > 0.5):
                    best_movement = successor
                    found = True

        if(not(found)):
            best_movement = self.generateRandomMove(state)
        return best_movement

    def generateRandomMove(state: State) -> Tuple[str, str]:
        """
        Generates a random move based on the current state of the game
            
        [PARAMETER]
        state: State -> current game state.
            
        [RETURN]
        Tuple[str, str] -> a random move chosen based on the current state.
        """
        return (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))

    def calculateTemperature(self) -> float:
        """
        Method to calculate the temperature based on the current time.
            
        [RETURN]
        float -> the temperature value of the current time.
        """
        return ((self.time_limit-self.used_time)/self.time_limit)*100
        
    def calculateDeltaE(state: State, move: Tuple[str, str]) -> float:
        """
        Method to calculate delta E value used in simulated annealing.
            
        [PARAMETER]
        state: State -> current game state.
        move: Tuple[str, str] -> move to calculate next state

        [RETURN]
        float -> the temperature value of the current time.
        """
        #TODO ubah fungsi heuristicnya
        current_value = countObjectiveIsWin(state)
        
        player = (state.round - 1) % 2
        next_state = copy.deepcopy(state)
        next_state_move = place(next_state, player, move[0], move[1])
        return countObjectiveIsWin(state) - countObjectiveIsWin(next_state)
