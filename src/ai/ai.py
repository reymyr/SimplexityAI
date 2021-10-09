from abc import ABC
from src.model import State
from src.utility import is_win, is_full

class AI(ABC):
    """
	A base class for AI in Simplexity Game.

	[ATTRIBUTES]
		time_limit : int → time limit for finding move.
		used_time : int → total time used for bot for searching move.

	[METHOD]
		__init__(time_limit:int):
			Constructor for AI classes.

		terminate(curr_depth:int, state: state) → bool:
			Return boolean indicating whether AI must terminate it's searching or not. 
   		 calculateValue(state:state) → int:
     			Return the value of a state
	"""
    def __init__(self):
        """
		Constructor for AI base class.
		"""
        pass

    def terminate(self, curr_depth:int, state: State) -> bool:
        """
		Terminate is a function to evaluate whether AI must terminate it's searching or not. 
		Either because it's reached max depth, thinking lime limit or winner of game is found.
		
		[ATTRIBUTES]
			curr_depth : int → current depth of searching tree.
			state: state → current game state.
		
		[RETURN]
			bool → boolean indicating whether AI must terminate it's searching or not. 
		"""
        pass

    def calculateValue(state: State) -> int:
       	"""
		Function that is used to calculate the value of a state
		
		[ATTRIBUTES]
			state: state → current game state.
		
		[RETURN]
			int → the value of the state. 
		"""        
        pass

    # Kalo Menang
    def countObjectiveIsWin(state: State, n_player:int):
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
        winner = is_win(state.board)
        if winner:
            remainder = 0
            for k, v in state.players[n_player].quota.items():
                remainder += v
            score = (remainder+1)*2
            if(n_player == 1):
                score = score*(-1)
            return score

        if is_full(state.board):
            #Draw
            return 0
