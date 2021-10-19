import random
import copy
from time import time
from typing import Tuple, Dict

from src.constant import *
from src.model import *
from src.utility import *


class Minimax2:
    """
	A basic AI class that implement minimax and alpha-beta pruning for finding best move in 
	simplexity game. 

	[ATTRIBUTES]
        type1Heuristic : → dictionary for type1 heuristic value.
		type2Heuristic : → dictionary for type2 heuristic value.
		type3Heuristic : → dictionary for type3 heuristic value.
	    thingking_time_limit: int -> time when bot must finished searching move.
	    max_depth: int -> maximum depth for searching.
	    This class also inherits attribute from AI class (time_limit, used_time, and max_depth).

	[MAIN METHOD]
	    __init__(time_limit:int, max_depth:int):
	        Constructor for Minimax classes, Also construct the base AI class.
	    find(self, state: State, maximizing_player: bool, thinking_time: float) -> Tuple[str, str]:
	        Find the best move for AI using Minimax Alpha-Beta pruning algorithm.
	    minimax(possible_move: Tuple[str, str], depth: int, alpha: int, beta: int,  maximizing_player: bool) -> Tuple[str, str]:
	        Minimax Alpha-Beta Pruning algorithm implementation on every possible move.

	[BASIC METHOD]
        generateRandomMove(self, state: State, n_player: int) -> Tuple[str, str]:
            Generates a random move based on the current state of the game.
        generatingPossibleMoves(self, state: State, n_player: int) -> Tuple[int, str]:
            Function to generate possible move that current player can do. The order of the move are optimized 
            with static heuristic.
        is_placeable(self, board:Board, row:int, col:int ) -> bool:
            Function to check can we place piece at column "col" and row "row".
        check_placeable_tiles_at_direction(self, board:Board, start:Tuple[int, int], end:Tuple[int, int], dir:Tuple[int, int]) -> int:
            Function to check number of free placeable tile on direction.
        check_3_streak_split(self, board: Board, location:Tuple[int, int],  dir:Tuple[int, int]) -> Tuple[str, str]:
            Function to check 2 streak followed by blank then the same piece from row, col in current board 
            with specific direction.
        check_n_streak_at_direction(self, n_streak:int, board: Board, location:Tuple[int, int],  dir:Tuple[int, int]) -> Tuple[str, str]:
            Function to check n streak from row, col in current board with specific direction.
        countObjectiveIsWin(self, state: State) -> int
            Function to count heuristic function if a winner is found.
        countObjectiveType3(self, col:int) -> float:
            Function to count heuristic state value if current piece is single horsemen. 
            The heuristic value depend on how many streak is possible.
        countObjectiveType2(self, board:Board, location:Tuple[int, int],  dir:Tuple[int, int]) -> float:
            Function to count heuristic state value if Type2 exist. Type2 happen where there are 
            two connected piece in some way. The heuristic value depend on free tile on direction.
        countObjectiveType1(self, state:State, location:Tuple[int, int],  dir:Tuple[int, int]) -> float:
            Function to count heuristic state value if Type1 exist. Type1 happen where there are 
            three connected piece in some way.
        calculateValue(self, state: State, n_player:int) -> float:
            Function that is used to calculate the value of a state.
	"""
# Heuristic value for type 1.
    type1Heuristic:Dict[str, int] = {
		"SHAPE" : 10,
		"COLOR": 9
	}

	# Heuristic value for type 2.
	# Depend on number of free placeable tile.
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
	# Depend on column position
    type3Heuristic:Dict[int, float] = {
		0 : 0.1,
		1 : 0.2,
		2 : 0.3,
		3 : 0.4,
		4 : 0.3,
		5 : 0.2,
		6 : 0.1
	}
# ==========================================[BASIC METHOD]==========================================
    
    def calculateValue(self, state: State, n_player:int) -> float:
        """
		Function that is used to calculate the value of a state

		[ATTRIBUTES]
			state: state → current game state.

		[RETURN]
			float → the value of the state. 
		"""        
		# Winning case.
        if (is_win(state.board)):
            return self.countObjectiveIsWin(state)

		# Not Winning case -> checking feature(type) in board.
		# Initialize return value.
        ret_val:int = 0

		# Only check north, east, and northeast direction because checking otherwise will result
		# in duplicate feature.
		# Kanan, atas, ataskanan, bawahkanan
        streak_way = [(0, 1),(-1,0),(-1, 1),(1,1)]

		# Check for every piece exist on every streak direction.
        for row in range(state.board.row):
            for col in range(state.board.col):
                # Initialize type1Ortype2Exist as false for each specific piece.
                type1Ortype2Exist = False

                # Loop for every valid direction.
                for streak in streak_way:
                    # Only check if current piece is not blank.
                    if (state.board[row, col].shape != ShapeConstant.BLANK):
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

    def countObjectiveType1(self, state:State, location:Tuple[int, int],  dir:Tuple[int, int]) -> float:
        """
        countObjectiveType1 is a function to count heuristic state value if Type1 exist. Type1 happen
        where there are three connected piece in some way
        
        [PARAMS]
            state: State -> gamestate that will be checked.
            location: Tuple[int, int] -> row and col
            dir: Tuple[int, int] -> x direction and y direction
        [RETURN]
            0 if type 1 not exist on piece with specific row and column or the heuristic value is zero
            float if type 1 exist and the heuristic value is not 0.
        """
        # Initialize the return value.
        ret_val: int = 0
        # Get the streak.
        streak = self.check_n_streak_at_direction(3, state.board, location, dir)
        
        # If you get the streak.
        if streak != ["",""]:
            # Get the starting piece and ending piece.
            start = [location[0], location[1]]
            end = [int(location[0]) + 2*int(dir[0]), int(location[1])+ 2*int(dir[1])]

            before_start = [start[0] - dir[0], start[1] - dir[1]]
            after_end = [end[0] + dir[0], end[1] + dir[1]]

            placeable_start = self.is_placeable(state.board, before_start[0], before_start[1])
            placeable_end = self.is_placeable(state.board, after_end[0], after_end[1])

            # If able to place in both ends of the streak
            if placeable_start and placeable_end:
                next_state = copy.deepcopy(state)

                if streak[0] == GameConstant.PLAYER1_SHAPE and state.players[0].quota[GameConstant.PLAYER1_SHAPE] != 0:
                    place(next_state, 0, streak[0], before_start[1])
                    ret_val += self.type1Heuristic["SHAPE"] * 2
                elif streak[0] == GameConstant.PLAYER2_SHAPE and state.players[1].quota[GameConstant.PLAYER2_SHAPE] != 0:
                    place(next_state, 1, streak[0], before_start[1])
                    ret_val -= self.type1Heuristic["SHAPE"] * 2
                elif streak[1] == GameConstant.PLAYER1_COLOR:
                    shape = GameConstant.PLAYER1_SHAPE if state.players[0].quota[GameConstant.PLAYER1_SHAPE] > 0 else GameConstant.PLAYER2_SHAPE
                    place(next_state, 0, shape, before_start[1])
                    ret_val += self.type1Heuristic["COLOR"] * 2
                elif streak[1] == GameConstant.PLAYER2_COLOR:
                    shape = GameConstant.PLAYER2_SHAPE if state.players[1].quota[GameConstant.PLAYER2_SHAPE] > 0 else GameConstant.PLAYER1_SHAPE
                    place(next_state, 1, shape, before_start[1])
                    ret_val -= self.type1Heuristic["COLOR"] * 2
                return ret_val

            # if able to place in one end of the streak
            elif placeable_start or placeable_end:
                # Assuming player 1 will maximize the value and player 2 will minimize the value.
                # Streak[0] is shape.
                if streak[0] != "":
                    if streak[0] == GameConstant.PLAYER1_SHAPE:
                        ret_val += self.type1Heuristic["SHAPE"]
                    else:
                        ret_val -= self.type1Heuristic["SHAPE"]
                # Streak[1] is color.
                if streak[1] != "":
                    if streak[1] == GameConstant.PLAYER1_COLOR:
                        ret_val += self.type1Heuristic["COLOR"]
                    else:
                        ret_val -= self.type1Heuristic["COLOR"]

            # If piece cannot be placed on both ends of the streak
            else:
                ret_val += 0
            
            return ret_val

        # No streak with length 3
        else:
            two_streak = self.check_3_streak_split(state.board, location, dir)
            if two_streak != ["",""]:

                # Assuming player 1 will maximize the value and player 2 will minimize the value.
                # Streak[0] is shape.
                if two_streak[0] != "":
                    if two_streak[0] == GameConstant.PLAYER1_SHAPE:
                        ret_val += self.type1Heuristic["SHAPE"]
                    else:
                        ret_val -= self.type1Heuristic["SHAPE"]
                # Streak[1] is color.
                if two_streak[1] != "":
                    if two_streak[1] == GameConstant.PLAYER1_COLOR:
                        ret_val += self.type1Heuristic["COLOR"]
                    else:
                        ret_val -= self.type1Heuristic["COLOR"]
                return ret_val
            return 0

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
            end = [int(location[0]) + int(dir[0]), int(location[1])+ int(dir[1])]
            freeTiles = self.check_placeable_tiles_at_direction(board, start, end, dir)

            
            # # TODO: Testing
            # print("I Got streak type 2 of piece in row ",start[0]," col ",start[1],"ending in row ",end[0]," col ",end[1]," at direction ", dir[0], " ", dir[1])

            # Free tile must be greater or equal than 2 to make a score.
            if freeTiles >=2:

                # # TODO: Testing
                # print("I Got free tile more than 2", "free tile is: ", freeTiles)
                
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

        return 0

    def countObjectiveType3(self, col:int) -> float:
        """
        countObjectiveType3 is a function to count heuristic state value if current piece is single horsemen. 
        single horseman happen there are a single piece not connected to any piece. The heuristic value 
        depend on how many streak is possible.
        
        [PARAMS]
            board: Board  -> the game board
            row: int  -> row
            col: int  -> column
        [RETURN]
            float -> heuristic value.
        """
        return self.type3Heuristic[col]

    def countObjectiveIsWin(self, state: State) -> int:
        """
        [DESC]
            Function to count heuristic function if a winner is found
        [PARAMS]
            state: State -> current State
        [RETURN]
            0 if draw
            +inf if PLayer_1 can win
            -inf if Player_2 can win
        """
        winner = is_win(state.board)
        if winner:
            remainderP1 = 0
            remainderP2 = 0
            for k, v in state.players[0].quota.items():
                remainderP1 += v
            for k, v in state.players[1].quota.items():
                remainderP2 += v
            
            if winner[0] == state.players[0].shape:
                score = 10000 + remainderP1
            elif(winner[0] == state.players[1].shape):
                score = -10000 - remainderP2
            elif winner[1] == state.players[0].color:
                score = 10000 + remainderP1
            else:
                score = -10000 - remainderP2

            return score

        if is_full(state.board):
            #Draw
            return 0

        return 0

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

    def check_3_streak_split(self, board: Board, location:Tuple[int, int],  dir:Tuple[int, int]) -> Tuple[str, str]:
        """
            Function to check 2 streak followed by blank then the same piece from row, col in current board with specific direction
        [PARAMS]
            board: Board -> current board.
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
            row_ax = dir[0]
            col_ax = dir[1]

            # Count number of blank tiles and streak piece in the direction
            n_blank = 0
            n_piece = 1
            
            # Move with direction (row_ax, col_ax) one time.
            row_ = row + row_ax
            col_ = col + col_ax

            # Loop 3 times to check the next 3 pieces
            for _ in range(3):
                if is_out(board, row_, col_):
                    n_piece = 1
                    n_blank = 0
                    break

                # Streak checking.
                # If blank, incerement n_blank if currnet n_blank = 0 and if placeable
                if board[row_, col_].shape == ShapeConstant.BLANK:
                    if self.is_placeable(board, row_, col_) and n_blank == 0:
                        n_blank += 1
                    else:
                        n_piece = 1
                        n_blank = 0
                        break
                    
                # Checking for shape but current shape not equal with 'piece' shape.
                else:
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
                        n_piece = 1
                        n_blank = 0
                        break

                    n_piece += 1

                # Move with direction (row_ax, col_ax) one time.
                row_ += row_ax
                col_ += col_ax

            # If you get the streak.
            if n_piece == 3 and n_blank == 1:
                # Change the value of shape or color depending on the iteration.
                if prior == GameConstant.SHAPE:
                    ret_val[0] = piece.shape
                else:
                    ret_val[1] = piece.color

        # Return the value.
        return ret_val 

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
        while (self.is_placeable(board, start_row_, start_col_)):
            ret_val += 1
            start_row_ = start_row_ + start_row_ax
            start_col_ = start_col_ + start_col_ax
        
        # Count from end.
        # Count free tile from end with direction = dir
        end_row = end[0]
        end_col = end[1]
        end_row_ax = dir[0]
        end_col_ax = dir[1]
            
        # Move with direction (row_ax, col_ax) one time.
        end_row_ = end_row + end_row_ax
        end_col_ = end_col + end_col_ax

        # While place_able then loop.
        while (self.is_placeable(board, end_row_, end_col_)):
            ret_val += 1
            end_row_ = end_row_ + end_row_ax
            end_col_ = end_col_ + end_col_ax
        
        return ret_val

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
        if (row == 5):
            return True
        return board[row+1, col].shape != ShapeConstant.BLANK

    def generatingPossibleMoves(self, state: State, n_player: int) -> Tuple[int, str]:
        """
        Function to generate possible move that current player can do. The order of the move
        are optimized with static heuristic

        [PARAMS]
            state : State -> the game state.
            n_player: int -> number of current player.
        
        [RETURN]
            Tuple[int, str] -> first element(int) are the column you want to put new piece
                            -> second element(str) are the shape of piece you choose
        """
        result = []
        shape0 = [ShapeConstant.CIRCLE, ShapeConstant.CROSS]
        shape1 = [ShapeConstant.CROSS, ShapeConstant.CIRCLE]
        column = []
        if(state.board.col%2)==1:
            mid = int((state.board.col-1)/2)
            column.append(mid)
            for i in range(1,mid+1):
                column.append(mid+i)
                column.append(mid-i)
        else:
            midR = int(state.board.col/2)
            midL = midR-1
            column.append(midL)
            column.append(midR)
            for i in range(1,midL+1):
                column.append(midR+i)
                column.append(midL-i)
            
        if(n_player==0):
            for shape in shape0:
                for col in column:
                    if(state.players[n_player].quota[shape] > 0):
                        # # Hard way.
                        # next_state = copy.deepcopy(state)
                        # move = place(next_state, n_player, shape, col)
                        # if(move != -1):
                        # 	result.append((col, shape))

                        # Alternative way
                        if (state.board[0, col].shape == ShapeConstant.BLANK):
                            result.append((col, shape))
                    # else:
                    # 	break
        else:
            for shape in shape1:
                for col in column:
                    if(state.players[n_player].quota[shape] > 0):
                        # Hard way.
                        # next_state = copy.deepcopy(state)
                        # move = place(next_state, n_player, shape, col)
                        # if(move != -1):
                        # 	result.append((col, shape))
                        
                        # Alternative way
                        if (state.board[0, col].shape == ShapeConstant.BLANK):
                            result.append((col, shape))
                    # else:
                    # 	break
                    
        return result

    def generateRandomMove(self, state: State, n_player: int) -> Tuple[str, str]:
        '''
        Generates a random move based on the current state of the game
            
        [PARAMETER]
            state: State -> current game state.
            
        [RETURN]
            Tuple[str, str] -> a random move chosen based on the current state.
        '''
        possible_move =self.generatingPossibleMoves(state, n_player)
        random_number = random.randint(0, len(possible_move)-1)
        return possible_move[random_number]
# ==================================================================================================

# ==========================================[MAIN METHOD]==========================================
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
        
        # TODO : Remove this part after test end.
        # This part is for testing.
        player = (state.round - 1) % 2
        next_state = copy.deepcopy(state)
        place(next_state, player, best_movement[1], best_movement[0])
        
        print("Current algorithm is minimax")
        print("Choosen movement is ", best_movement)
        print("Current is now player ", player + 1)
        print("Value for board below is ", self.calculateValue(next_state, player))
        # print("Available move for this turn is")
        # possible_move =self.generatingPossibleMoves(state, n_player)
        # print(possible_move)
        # End of testing.
        
        return (best_movement[0], best_movement[1])

    def minimax(self, depth: int, state: State, alpha: int, beta: int, n_player: int) -> Tuple[str, str, float]:
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
        current_time = time()
        if depth == 0 or is_win(state.board) or is_full(state.board) or current_time>self.thinking_time:
            if(current_time>self.thinking_time):
                print("BOOM WAKTU ABIS")
            return ("-", -1, self.calculateValue(state, n_player))

        possible_moves = self.generatingPossibleMoves(state, n_player)
        if(n_player == 0):
            maxEval = float('-inf')
            next_depth = depth - 1
            selected_move = ("-", 0, 0)
            for move in possible_moves:
                current_time = time()
                if(current_time>self.thinking_time):
                    print("BOOM WAKTU ABIS")
                    if(selected_move == ("-", 0, 0)):
                        random_move = self.generateRandomMove(state, n_player)
                        next_state = copy.deepcopy(state)
                        place_random  = place(next_state, n_player, random_move[1], random_move[0])
                        return (random_move[0], random_move[1], self.calculateValue(next_state, n_player))
                    else:
                        return selected_move
                next_state = copy.deepcopy(state)
                place(next_state, n_player, move[1], move[0])
                eval = self.minimax(next_depth, next_state, alpha, beta, 1)
                if(eval[2] > maxEval):
                    maxEval = eval[2]
                    selected_move = (move[0], move[1], eval[2])
                alpha = max(alpha, eval[2])
                if(beta <= alpha):
                    break
                
            if(selected_move == ("-", 0, 0)):
                random_move = self.generateRandomMove(state, n_player)
                next_state = copy.deepcopy(state)
                place_random  = place(next_state, n_player, random_move[1], random_move[0])
                return (random_move[0], random_move[1], self.calculateValue(next_state, n_player))
            else:
                return selected_move  
        else:
            minEval = float('inf')
            next_depth = depth - 1
            selected_move = ("-", 0, 0)
            for move in possible_moves:
                current_time = time()
                if(current_time>self.thinking_time):
                    print("BOOM WAKTU ABIS")
                    if(selected_move == ("-", 0, 0)):
                        random_move = self.generateRandomMove(state, n_player)
                        next_state = copy.deepcopy(state)
                        place_random  = place(next_state, n_player, random_move[1], random_move[0])
                        return (random_move[0], random_move[1], self.calculateValue(next_state, n_player))
                    else:
                        return selected_move
                next_state = copy.deepcopy(state)
                place(next_state, n_player, move[1], move[0])
                eval = self.minimax(next_depth, next_state, alpha, beta, 0)
                if(eval[2] < minEval):
                    minEval = eval[2]
                    selected_move = (move[0], move[1], eval[2])
                beta = min(beta, eval[2])
                if(beta <= alpha):
                    break
            
            if(selected_move == ("-", 0, 0)):
                random_move = self.generateRandomMove(state, n_player)
                next_state = copy.deepcopy(state)
                place_random  = place(next_state, n_player, random_move[1], random_move[0])
                return (random_move[0], random_move[1], self.calculateValue(next_state, n_player))
            else:
                return selected_move  
#===================================================================================================
    

