'''
Sudoku solver ( 9x9 ) without using recursion
Author : DeStRoYeR4	
'''

board1 = [
[7,8,0,4,0,0,1,2,0],	#0
[6,0,0,0,7,5,0,0,9],	#1
[0,0,0,6,0,1,0,7,8],	#2
[0,0,7,0,4,0,2,6,0],	#3
[0,0,1,0,5,0,9,3,0],	#4
[9,0,4,0,6,0,0,0,5],	#5
[0,7,0,3,0,0,0,1,2],	#6
[1,2,0,0,0,7,4,0,0],	#7
[0,4,9,2,0,6,0,0,7]		#8
]
#0,1,2,3,4,5,6,7,8

board2 = [
[0,0,7,5,0,8,9,0,0],	#0
[0,3,0,9,0,2,0,1,0],	#1
[1,0,0,3,0,6,0,0,8],	#2
[0,5,3,0,0,0,1,4,0],	#3
[0,0,0,0,0,0,0,0,0],	#4
[0,8,2,0,0,0,6,5,0],	#5
[9,0,0,7,0,4,0,0,1],	#6
[0,6,0,8,0,5,0,9,0],	#7
[0,0,4,1,0,3,8,0,0],	#8
]
#0,1,2,3,4,5,6,7,8

def findZero(board):
	'''
	Takes a parameter board
	:returns a list of tuple containing row and column where number is zero (empty)
	:tuple format - (row , column)
	'''
	positions = []
	for i in range(0,9):
		for j in range(0,9):
			if (board[i][j] == 0):
				positions.append((i,j))

	return positions

def isValid(board , number , row , column):
	'''
	Takes parameters board, number, row and column
	Validates the number if it fits in the given row and column
	:returns True if valid
	:returns False if not valid
	'''

	#Checking if the number is in the same row
	for i in board[row]:
		if (i == number) :
			return False

	#Checking if the number is in the same column
	for i in board:
		if (i[column] == number) :
			return False

	#Checking whether the number is in the same reigon (3x3)
	base_row = (row//3) * 3
	base_column = (column//3) * 3
	for i in range(base_row , base_row+3):
		for j in range(base_column , base_column+3):
			if (board[i][j] == number):
				return False

	#After checking all the possibilites
	return True

def nums_valid(board, row, column):
	'''
	Takes in parameter board,row and column
	:returns a list of all possible numbers that can fit in that position
	'''
	val = []
	for i in range(1,10):
		if isValid(board , i , row , column):
			val.append(i)
	return val

def Is_solved(board):
	'''
	Takes in a parameter board
	:returns True if board is solved
	:returns False if board is not solved
	'''
	for i in range(9):
		for j in range(9):
			if board[i][j] == 0:
				return False
	return True

#Logic to solving a Sudoku Board
def Solve(board):
	'''
	Takes a parameter board
	:returns a solved board
	:method :- 
		for all position having 0 (no number
		checks for all the possible numbers 
		puts number if its unique (only number that fits)
		(iteraively looping this process over and over)
	'''

	while not(Is_solved(board)):
		indices = findZero(board)
		for i in indices:
			valid_nums = nums_valid(board , i[0] , i[1])
			if len(valid_nums) == 1:
				board[i[0]][i[1]] = valid_nums[0]


def print_Board(Board):
	for i in range(9):
		if (i % 3) == 0 and (i != 0):
			print ('-----------------------')

		for j in range(9):
			if (j % 3 == 0) and (j != 0):
				print ('|' , end = ' ')
			print (Board[i][j] , end = ' ')
		print ()
