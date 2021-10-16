import random
import copy
from time import time

from src.constant import ShapeConstant
from src.model import State

from typing import Tuple, List
from src.ai.ai import AI
from src.utility import place, is_win, is_full

# class Minimax:
# def __init__(self):
# pass

# def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
# self.thinking_time = time() + thinking_time

# best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm

# return best_movement

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

    def __init__(self, max_depth : int = 3) -> None:
        """
		Constructor for Minimax class. Construct AI base class also.
		[ATTRIBUTES]
		time_limit : int -> time limit for finding move.
		max_depth: int -> maximum depth for searching.		
		"""
        self.max_depth = max_depth


    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
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
        self.thinking_time = time() + thinking_time

        best_movement = self.minimax(self.max_depth, state, float('-inf'), float('inf'), n_player) #minimax algorithm
        return (best_movement[0], best_movement[1])

    def minimax(self, depth: int, state: State, alpha: int, beta: int, n_player: int) -> Tuple[str, str, float]:
        current_time = time()
        if depth == 0 or is_win(state.board) or is_full(state.board) or current_time>self.thinking_time:
            return ("-", -1, self.calculateValue(state, n_player))

        possible_moves = self.generatingPossibleMoves(state, n_player)
        if(n_player == 0):
            maxEval = float('-inf')
            next_depth = depth - 1
            selected_move = ("-", 0, 0)
            for move in possible_moves:
                current_time = time()
                if(current_time>self.thinking_time):
                    if(selected_move == ("-", 0, 0)):
                        return self.generateRandomMove(state, n_player)
                    else:
                        return selected_move
                next_state = copy.deepcopy(state)
                place_move = place(next_state, n_player, move[1], move[0])
                eval = self.minimax(next_depth, next_state, alpha, beta, 1)
                if(eval[2] > maxEval):
                    maxEval = eval[2]
                    selected_move = (move[0], move[1], eval[2])
                alpha = max(alpha, eval[2])
                if(beta <= alpha):
                    break
                
            if(selected_move == ("-", 0, 0)):
                return self.generateRandomMove(state, n_player)
            else:
                return selected_move  
        else:
            minEval = float('inf')
            next_depth = depth - 1
            selected_move = ("-", 0, 0)
            for move in possible_moves:
                current_time = time()
                if(current_time>self.thinking_time):
                    if(selected_move == ("-", 0, 0)):
                        return self.generateRandomMove(state, n_player)
                    else:
                        return selected_move
                next_state = copy.deepcopy(state)
                place_move = place(next_state, n_player, move[1], move[0])
                eval = self.minimax(next_depth, next_state, alpha, beta, 0)
                if(eval[2] < minEval):
                    minEval = eval[2]
                    selected_move = (move[0], move[1], eval[2])
                beta = min(beta, eval[2])
                if(beta <= alpha):
                    break
            
            if(selected_move == ("-", 0, 0)):
                return self.generateRandomMove(state, n_player)
            else:
                return selected_move  
            
        # """
        # Minimax is a function to implement minimax alpha-beta pruning on every possible_move 
        # while monitoring time and depth constraint. If AI has not reached time limit or depth 
        # limit, then AI will continue to traverse tree until it's reach  leaf node or it's limit. Else if AI 
        # has reach it's limit then AI will immediately return the  best move so far or return null 
        # movement (depend on spek tubes)
		# [PARAMETER]
		# possible_move: List[Tuple[str, str]] -> current available move for current player.
		# depth: int -> current depth of minimax tree.
		# state: state -> current game state.
		# alpha: int -> the best solution so far.
		# beta : int -> the worst solution so far.
		# maximizing_player :bool -> boolean indicating to maximize objective function or not
        # [RETURN]
		# Tuple[str, str] -> the best move for current player.
		# """
        
    def countObjectiveIsWin(self, state: State, n_player:int):
        """
        [DESC]
        Function to count heuristic function if a winner is found
        [PARAMS]
        state: State -> current State
        [RETURN]
        0 if draw
        +(21-player.quota)*2 if PLayer_1 can win
        -(21-player.quota)*2 if Player_2 can win
        """
        return super().countObjectiveIsWin(state, n_player)

    def generatingPossibleMoves(self, state: State, n_player: int):
        result = []
        
        for col in range(state.board.col):
            if(state.players[n_player].quota[ShapeConstant.CROSS] > 0):
                next_state = copy.deepcopy(state)
                move = place(next_state, n_player, ShapeConstant.CROSS, col)
                if(move != -1):
                    result.append((col, ShapeConstant.CROSS))
            if(state.players[n_player].quota[ShapeConstant.CIRCLE] > 0):
                next_state = copy.deepcopy(state)
                move = place(next_state, n_player, ShapeConstant.CIRCLE, col)
                if(move != -1):
                    result.append((col, ShapeConstant.CIRCLE))
        return result
