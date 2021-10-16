import random
from time import time

from src.constant import ShapeConstant
from src.model import State

from typing import Tuple, List
from src.ai.ai import AI

# class Minimax:
#     def __init__(self):
#         pass

#     def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
#         self.thinking_time = time() + thinking_time

#         best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm

#         return best_movement

class Minimax(AI):
    """
	A basic AI class that implement minimax and alpha-beta pruning for finding best move in 
	simplexity game. 

	[ATTRIBUTES]
	thingking_time_limit: int -> time when bot must finished searching move.
	max_depth: int -> maximum depth for searching.
	This class also inherits attribute from AI class (time_limit, used_time, and max_depth).

	[METHOD]
	__init__(time_limit:int, max_depth:int):
	Constructor for Minimax classes, Also construct the base AI class.
	find(self, state: State, maximizing_player: bool, thinking_time: float) -> Tuple[str, str]:
	Find the best move for AI using Minimax Alpha-Beta pruning algorithm.
	minimax(possible_move: Tuple[str, str], depth: int, alpha: int, beta: int, 
	maximizing_player: bool) -> Tuple[str, str]:
	Minimax Alpha-Beta Pruning algorithm implementation on every possible move.
	This class also inherits methods from AI class (terminate)
	"""

    def __init__(self) -> None:
        """
        Constructor for Minimax class. Construct AI base class also.
        
        [ATTRIBUTES]
        time_limit : int -> time limit for finding move.
        max_depth: int -> maximum depth for searching.		
        """

    def find(self, state: State, maximizing_player: bool) -> Tuple[str, str]:
        """
		Find is a function to find best move using minimax alpha-beta prunning. 
		This method will initialize minimax method with it's default value parameter and update
        used time  attribute on class.
		
		[PARAMETER]
		state: state -> current game state.
		maximizing_player :bool -> boolean indicating to maximize objective function or not.
		
		[RETURN]
	    Tuple[str, str] -> the best move for current player.
		"""
        pass

    def minimax(possible_move: List[Tuple[str, str]], depth: int, state: State, alpha: int, beta: int, maximizing_player: bool) -> Tuple[str, str]:
    	"""
		Minimax is a function to implement minimax alpha-beta pruning on every possible_move 
		while monitoring time and depth constraint. If AI has not reached time limit or depth 
		limit, then AI will continue to traverse tree until it's reach  leaf node or it's limit. Else if AI 
		has reach it's limit then AI will immediately return the  best move so far or return null 
		movement (depend on spek tubes)

		[PARAMETER]
		possible_move: List[Tuple[str, str]] -> current available move for current player.
		depth: int -> current depth of minimax tree.
		state: state -> current game state.
		alpha: int -> the best solution so far.
		beta : int -> the worst solution so far.
		maximizing_player :bool -> boolean indicating to maximize objective function or not
		
		[RETURN]
		Tuple[str, str] -> the best move for current player.
		"""
    pass   
    
