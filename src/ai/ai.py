from abc import ABC
from src.model import State

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
    def __init__(self, time_limit:int):
        """
		Constructor for AI base class. Construct used_time also.
		
		[ATTRIBUTES]
			time_limit : int → time limit for finding move.
		"""
        self.time_limit = time_limit
        self.used_time = 0

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
