from abc import ABC
from typing import Tuple, Dict

from src.model import Piece, Board, State
from src.utility import is_win, is_full, is_out
from src.constant import ShapeConstant, GameConstant

class AI(ABC):
	"""
	A base class for AI in Simplexity Game.

	[ATTRIBUTES]
		time_limit : int → time limit for finding move.
		used_time : int → total time used for bot for searching move.
		type2Heuristic : dictionary for type2 heuristic value.

	[METHOD]
		__init__(time_limit:int):
			Constructor for AI classes.

		terminate(curr_depth:int, state: state) → bool:
			Return boolean indicating whether AI must terminate it's searching or not. 
   		 calculateValue(state:state) → int:
	 			Return the value of a state
	"""
	# Heuristic value for type 1.
	# TODO : Create heuristic value for type 1.

	# Heuristic value for type 2.
	# Depend on number of free placeable tile.
	# TODO : Re-evaluate the heuristic value.
	type2Heuristic:Dict[str, Dict[int, int]] = {
		"SHAPE" : {
			0:0,
			1:0,
			2:1.5,
			3:2.5,
			4:3.5,
			5:4.5
		},
		"COLOR": {
			0:0,
			1:0,
			2:1,
			3:2,
			4:3,
			5:4
		}
	}

	# Heuristic value for type 3.
	# TODO : Create heuristic value for type 3.
	
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

	# TODO : Finish heuristic value for a state. 
	def calculateValue(self, state: State, n_player:int) -> float:
		"""
		Function that is used to calculate the value of a state

		[ATTRIBUTES]
			state: state → current game state.

		[RETURN]
			float → the value of the state. 
		"""        
		# Winning case.
		if (is_win(state)):
			return self.countObjectiveIsWin(state, n_player)

		# Not Winning case -> checking feature(type) in board.
		# Initialize return value.
		ret_val:int = 0

		# Only check north, east, and northeast direction because checking otherwise will result
		# in duplicate feature.
		streak_way = [(0, 1),(1,0),(1, 1)]

		# Check for every piece exist on every streak direction.
		for row in range(state.board.row):
			for col in range(state.board.col):
				# Initialize type1Ortype2Exist as false for each specific piece.
				type1Ortype2Exist = False

				# Loop for every valid direction.
				for streak in streak_way:
					# Only check if current piece is not blank.
					if (state.board[row, col] != ShapeConstant.BLANK):
						# Count type 1 and type 2.
						type1 = self.countObjectiveType1(state, (row, col), streak)
						type2 = self.countObjectiveType2(state.board, (row, col), streak)
						
						# If type 1 or type 2 exist then mark as true.
						if (type1 or type2):
							type1Ortype2Exist = True
	
						# Add type 1 or type 2 to return value.
						if (type1):
							ret_val += type1
						if(type2):
							ret_val += type2
				
				# If for a specific you cannot generate type1 or type2 feature then it's must be a
				# single horseman (not connected piece).
				if (not(type1Ortype2Exist)):
					ret_val += self.countObjectiveType3(col)		
		return ret_val

	# TODO : Finish heuristic value for a type 1. 
	def countObjectiveType1(self, state:State, location:Tuple[int, int],  dir:Tuple[int, int]) -> float:
		"""
		countObjectiveType1 is a function to count heuristic state value if Type1 exist. Type1 happen
		where there are three connected piece in some way
		
		[PARAMS]
			state: State -> gamestate that will be checked.
			location: Tuple[int, int] -> row and col
			dir: Tuple[int, int] -> x direction and y direction
		[RETURN]
			None if type 3 not exist on piece with specific row and column or the heuristic value is zero
			float if type 3 exist and the heuristic value is not 0.
		"""
		
		return None
	
	# TODO : Finish heuristic value for a type 2. 
	# TODO : Check this function usability.
	def countObjectiveType2(self, board:Board, location:Tuple[int, int],  dir:Tuple[int, int]) -> float:
		"""
		countObjectiveType2 is a function to count heuristic state value if Type2 exist. Type2 happen
		where there are two connected piece in some way. The heuristic value depend on free tile on 
		direction.
		
		[PARAMS]
			board : Board -> the game board
			location: Tuple[int, int] -> row and col
			dir: Tuple[int, int] -> x direction and y direction
		[RETURN]
			None if type 2 not exist on piece with specific row and column or the heuristic value is zero
			int if type 2 exist and the heuristic value is not 0.
		"""
		# Initialize the return value.
		ret_val: int = 0
		# Get the streak.
		streak = self.check_n_streak_at_direction(2, board, location, dir)
		# If you get the streak.
		if streak != ["",""]:
			# Calculate free placeable tiles.
			# Get the starting piece and ending piece.
			start = [location[0], location[1]]
			end = [location[0] + dir[0], location[1]+ dir[1]]
			freeTiles = self.check_placeable_tiles_at_direction(board, start, end, dir)

			# Free tile must be greater or equal than 2 to make a score.
			if freeTiles >=2:
				
				# Count the score.
				# Assuming player 1 will maximize the value and player 2 will minimize the value.
				# Streak[0] is shape.
				if streak[0] != "":
					if streak[0] == GameConstant.PLAYER1_SHAPE:
						ret_val += self.type2Heuristic["SHAPE"][freeTiles]
					else:
						ret_val -= self.type2Heuristic["SHAPE"][freeTiles]
				# Streak[1] is color.
				if streak[1] != "":
					if streak[1] == GameConstant.PLAYER1_COLOR:
						ret_val += self.type2Heuristic["COLOR"][freeTiles]
					else:
						ret_val -= self.type2Heuristic["COLOR"][freeTiles]
				
				# Return the heuristic evaluation.
				return ret_val

		return None

	# TODO : Finish heuristic value for a type 3. 
	def countObjectiveType3(self, col:int) -> float:
		"""
		countObjectiveType3 is a function to count heuristic state value if current piece is single horsemen. 
		single horseman happen there are a single piece not connected to any piece. The heuristic value 
		depend on column.
		
		[PARAMS]
			col: int  -> column
		[RETURN]
			float -> heuristic value.
		"""
		
		return None

	def countObjectiveIsWin(self, state: State, n_player:int) -> int:
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

	# TODO : Check this function usability.		
	def check_n_streak_at_direction(self, n_streak:int, board: Board, location:Tuple[int, int],  dir:Tuple[int, int]) -> Tuple[str, str]:
		"""
			Function to check n streak from row, col in current board with specific direction
		[PARAMS]
			board: Board -> current board.
			n_streak: int -> number of streak you want to check.
			location: Tuple[int, int] -> row and col
			dir: Tuple[int, int] -> x direction and y direction
		[RETURN]
			Tuple[shape|"", color|""] if match on shape then shape will be player_1 or player_2 shape, 
			if match on color then color will be player_1 or player_2 color.  
		"""
		# Initialize return value.
		ret_val = ["",""]

		# Get the current piece in specific row and column and mark the 'piece'.
		row = location[0]
		col = location[1]
		piece = board[row, col]
		
		# Skip checking if current piece is blank piece. 
		if piece.shape == ShapeConstant.BLANK:
			return None
		
		# Check if equal in shape and equal in color.
		for prior in GameConstant.WIN_PRIOR:
			# Initialize the streak and get the direction.
			# If mark-1 = n_streak then you get the streak.
			mark = 0
			row_ax = dir[0]
			col_ax = dir[1]
			
			# Move with direction (row_ax, col_ax) one time.
			row_ = row + row_ax
			col_ = col + col_ax

			# Move n_streak-1 times until n_streak equal piece (by color or shape) is found or break if
			# not equal piece found.
			for _ in range(n_streak - 1):
				if is_out(board, row_, col_):
					mark = 0
					break

				# Streak checking.
				# Checking for shape but current shape not equal with 'piece' shape.
				shape_condition = (
					prior == GameConstant.SHAPE
					and piece.shape != board[row_, col_].shape
				)
				# Checking for color but current color not equal with  'piece' color.
				color_condition = (
					prior == GameConstant.COLOR
					and piece.color != board[row_, col_].color
				)
				# Break if not equal.
				if shape_condition or color_condition:
					mark = 0
					break

				# Move with direction (row_ax, col_ax) one time and increase the mark.
				row_ += row_ax
				col_ += col_ax
				mark += 1

			# If you get the streak.
			if mark == n_streak -1:
				# Change the value of shape or color depending on the iteration.
				if prior == GameConstant.SHAPE:
					ret_val[0] = piece.shape
				else:
					ret_val[1] = piece.color

		# Return the value.
		return ret_val 

	# TODO : Check this function usability.
	def check_placeable_tiles_at_direction(self, board:Board, start:Tuple[int, int], end:Tuple[int, int], dir:Tuple[int, int]) -> int:
		"""
			Function to check number of free placeable tile on direction.
		[PARAMS]
			start: Tuple[int, int] -> row and column of starting piece who make connection.
			end: Tuple[int, int] -> row and column of end piece who make connection.
			dir: Tuple[int, int] -> x direction and y direction
		[RETURN]
			int -> indicating number of free tiles on direction.
		"""

		# Initialize return value.
		ret_val:int = 0

		# Count from start.
		# Count free tile from start with direction = - dir
		start_row = start[0]
		start_col = start[1]
		start_row_ax = -1 * dir[0]
		start_col_ax = -1 * dir[1]
			
		# Move with direction (row_ax, col_ax) one time.
		start_row_ = start_row + start_row_ax
		start_col_ = start_col + start_col_ax

		# While place_able then loop.
		while (self.is_placeable(board, start_col_)):
			ret_val += 1
			start_row_ = start_row_ + start_row_ax
			start_col_ = start_col_ + start_col_ax
		
		# Count from end.
		# Count free tile from end with direction = dir
		end_row = start[0]
		end_col = start[1]
		end_row_ax = dir[0]
		end_col_ax = dir[1]
			
		# Move with direction (row_ax, col_ax) one time.
		end_row_ = end_row + end_row_ax
		end_col_ = end_col + end_col_ax

		# While place_able then loop.
		while (self.is_placeable(board, end_col_)):
			ret_val += 1
			end_row_ = end_row_ + end_row_ax
			end_col_ = end_col_ + end_col_ax
		
		return ret_val

	# TODO : Check this function usability.
	def is_placeable(self, board:Board, row:int, col:int ) -> bool:
		"""
			Function to check can we place piece at column "col" and row "row".

		[PARAMS]
			board : Board -> the game board
			col: int -> column of the piece.
			row : int -> row of the piece.
		
		[RETURN]
			bool -> true if you can place piece on specific row and column, false if not.
		"""

		# False if out of index. 
		if is_out(board, row, col):
			return False
		
		# False if current tile is already occupied. 
		if board[row, col].shape != ShapeConstant.BLANK:
			return False

		# True if tile under current tile is already occupied, or if current tile at depth zero then 
		# true.
		if (row ==0):
			return True
		return board[row-1, col].shape != ShapeConstant.BLANK
		
