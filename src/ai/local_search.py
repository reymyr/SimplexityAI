
import copy
from time import time
from math import exp
from typing import Tuple

from src.model import State
from src.ai.ai import AI
from src.utility import place



class SimulatedAnnealing(AI):
    """
	A basic AI class that implement minimax and alpha-beta pruning for finding best move in 
	simplexity game. 

	[ATTRIBUTES]
	thinking_time_limit: int -> time when bot must finished searching move.
	This class also inherits attribute from AI class (time_limit, used_time).
	
    [MAIN METHOD]
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
            delta_e = self.calculateDeltaE(state, successor, n_player)
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

        # TODO : Remove this part after test end.
        # This part is for testing.
        player = (state.round - 1) % 2
        next_state = copy.deepcopy(state)
        place(next_state, player, best_movement[1], best_movement[0])
        
        print("Current algorithm is local search")
        print("Choosen movement is ", best_movement)
        print("Current is now player ", player + 1)
        print("Value for board below is ", self.calculateValue(next_state, player))
        # print("Available move for this turn is")
        # possible_move =self.generatingPossibleMoves(state, n_player)
        # print(possible_move)
        # End of testing.

        return best_movement



    def calculateTemperature(self) -> float:
        """
        Method to calculate the temperature based on the current time.
            
        [RETURN]
            float -> the temperature value of the current time.
        """
        current_time = time()
        diff = int(self.thinking_time - current_time)
        return (diff/self.time_limit)*100
        
    def calculateDeltaE(self, state: State, move: Tuple[str, str], n_player:int) -> float:
        """
        Method to calculate delta E value used in simulated annealing.
            
        [PARAMETER]
            state: State -> current game state.
            move: Tuple[str, str] -> move to calculate next state

        [RETURN]
            float -> the temperature value of the current time.
        """
        #TODO quickfix sudut pandang minmax
        next_state = copy.deepcopy(state)
        place(next_state, n_player, move[1], move[0])

        curr_value = self.calculateValue(state, n_player)
        next_value = self.calculateValue(next_state, n_player)

        if (n_player == 1):
            curr_value *= -1
            next_value *= -1
        
        return next_value - curr_value

