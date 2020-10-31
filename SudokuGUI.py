import pygame
import sys 
from SudokuSolverWithoutRecursion import board1, isValid , nums_valid , findZero , Is_solved
import pickle
import random

#GLOBAL VARIABLES
S_WIDTH = 720
S_HEIGHT = 780
GAME_WIDTH = 720
GAME_HEIGHT = 720
THICK_LINE_WIDTH = 8
THIN_LINE_WIDTH = 4

#Defining the colors
LINE_COLOR , MAIN_TEXT_COLOR = (0 , 0 , 0) , (0 , 0 , 0)
INPUT_TEXT_COLOR = (128 , 128 , 128)
BG_COLOR = (255 , 255 , 255)
HIGHLIGHT_COLOR = (0 , 255 , 2)

#Initialising the modules
pygame.init()
pygame.font.init()

#Initialising screen
SCREEN = pygame.display.set_mode((S_WIDTH , S_HEIGHT))
SCREEN.fill(BG_COLOR)
pygame.display.set_caption('Sudoku')
pygame.display.update()

#Initialising the fonts
LARGE_FONT = pygame.font.SysFont('console' , 40)
MEDIUM_FONT = pygame.font.SysFont('console' , 30)
SMALL_FONT = pygame.font.SysFont('console' , 20)

#Saving user's input in a board (for displaying purposes)
ENTERED_BOARD = [[0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0] , 
				 [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0] , 
				 [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0] , 
				 [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0] , 
				 [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0] , 
				 [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0] , 
				 [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0] , 
				 [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0] , 
				 [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0] ]

def genBoard():
	global BOARD
	with open('puzzles.dat' , 'rb') as f:
   		b = pickle.load(f)
	BOARD = random.choice(b)
	return BOARD
   	

BOARD = genBoard()

def print_Board(Board):
	for i in range(9):
		if (i % 3) == 0 and (i != 0):
			print ('-----------------------')

		for j in range(9):
			if (j % 3 == 0) and (j != 0):
				print ('|' , end = ' ')
			print (Board[i][j] , end = ' ')
		print ()

#Drawing the lines
def drawLines():
	#Drawing the borders
	#Top border
	pygame.draw.line(SCREEN , LINE_COLOR , (0 , THICK_LINE_WIDTH//2-1) , (GAME_WIDTH , THICK_LINE_WIDTH//2-1) , THICK_LINE_WIDTH)

	#Bottom Border
	pygame.draw.line(SCREEN , LINE_COLOR , (0 , GAME_HEIGHT - THICK_LINE_WIDTH//2) , 
		(GAME_WIDTH , GAME_HEIGHT - THICK_LINE_WIDTH//2) , THICK_LINE_WIDTH)

	#Left Border
	pygame.draw.line(SCREEN , LINE_COLOR , (THICK_LINE_WIDTH//2-1 , 0) , (THICK_LINE_WIDTH//2-1 , GAME_HEIGHT) , THICK_LINE_WIDTH)

	#Right Boarder
	pygame.draw.line(SCREEN , LINE_COLOR , (GAME_WIDTH - THICK_LINE_WIDTH//2 , 0) , 
		(GAME_WIDTH - THICK_LINE_WIDTH//2 , GAME_HEIGHT) , THICK_LINE_WIDTH)

	#Drawing the thick vertical lines
	for i in range(1 , 3):
		pygame.draw.line(SCREEN , LINE_COLOR , ((GAME_WIDTH//3)*i , 0) , ((GAME_WIDTH//3)*i , GAME_HEIGHT) , THICK_LINE_WIDTH)

	#Drawing the thick horizontal lines
	for i in range(1 , 3):
		pygame.draw.line(SCREEN , LINE_COLOR , (0 , (GAME_HEIGHT//3)*i) , (GAME_WIDTH , (GAME_HEIGHT//3)*i) , THICK_LINE_WIDTH)

	#Drawing the thin vertical lines
	for i in range(1 , 9):
		pygame.draw.line(SCREEN , LINE_COLOR , ((GAME_WIDTH//9)*i , 0) , ((GAME_WIDTH//9)*i , GAME_HEIGHT) , THIN_LINE_WIDTH)

	#Drawing the thin horizontal lines
	for i in range(1 , 9):
		pygame.draw.line(SCREEN , LINE_COLOR , (0 , (GAME_HEIGHT//9)*i) , (GAME_WIDTH , (GAME_HEIGHT//9)*i) , THIN_LINE_WIDTH)

drawLines()
pygame.display.update()

#Drawing the main board
def drawMainBoard():
	for i in range(9):
		for j in range(9):
			if BOARD[i][j] != 0:
				TEXT = LARGE_FONT.render(str(BOARD[i][j]) , 1 , MAIN_TEXT_COLOR)
				SCREEN.blit(TEXT , ((GAME_WIDTH//9) * j + GAME_WIDTH//24, (GAME_HEIGHT//9)*i + GAME_HEIGHT//24))

	
TEXT = MEDIUM_FONT.render('Time :' , 1 , MAIN_TEXT_COLOR)
SCREEN.blit(TEXT , (550 , 735))
drawMainBoard()
pygame.display.update()

#Function to draw the user's input
def drawInputBoard():
	for i in range(9):
		for j in range(9):
			#Clearing the number
			pygame.draw.rect(SCREEN , BG_COLOR , ((GAME_WIDTH//9) * j + 20 , (GAME_HEIGHT//9)*i + 20 ,
			 GAME_WIDTH//9 - 30 , GAME_HEIGHT//9 - 30))

			if ENTERED_BOARD[i][j] != 0:
				TEXT = SMALL_FONT.render(str(ENTERED_BOARD[i][j]) , 1 , INPUT_TEXT_COLOR)
				SCREEN.blit(TEXT , ((GAME_WIDTH//9) * j + GAME_WIDTH//36, (GAME_HEIGHT//9)*i + GAME_HEIGHT//36))

#Function to highlight the selected square			
def highlight(row : int , col : int):
	if row < 9 and col < 9 and BOARD[row][col] == 0:
		pygame.draw.rect(SCREEN , HIGHLIGHT_COLOR , ((GAME_WIDTH//9) * col + 1 ,  (GAME_HEIGHT//9) * row + 1 , 
			GAME_WIDTH//9 - 1 ,  GAME_HEIGHT//9 - 1) , THIN_LINE_WIDTH - 2)
	else:
		pass	

#Function to solve the board iteratively
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
	indices = findZero(board)
	for i in indices:
		valid_nums = nums_valid(board , i[0] , i[1])
		if len(valid_nums) == 1:
			board[i[0]][i[1]] = valid_nums[0]
	return BOARD

CLOSED = False
Selected = False
SelectedPos = (10 , 10)
Clock = pygame.time.Clock()
seconds = 0
minutes = 0
milleseconds = 0


while not(CLOSED):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			CLOSED = True 

		if event.type == pygame.MOUSEBUTTONDOWN:
			col , row = pygame.mouse.get_pos()
			col , row = row//(GAME_WIDTH//9) , col//(GAME_HEIGHT//9)
			SelectedPos = (col , row)
			drawLines()
			Selected = True 

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_1:
				if Selected:
					if BOARD[col][row] == 0:
						ENTERED_BOARD[col][row] = 1
						drawInputBoard()
						drawMainBoard()
						pygame.display.update()

			if event.key == pygame.K_2:
				if Selected:
					if BOARD[col][row] == 0:
						ENTERED_BOARD[col][row] = 2
						drawInputBoard()
						drawMainBoard()
						pygame.display.update()

			if event.key == pygame.K_3:
				if Selected:
					if BOARD[col][row] == 0:
						ENTERED_BOARD[col][row] = 3
						drawInputBoard()
						drawMainBoard()
						pygame.display.update()
			
			if event.key == pygame.K_4:
				if Selected:
					if BOARD[col][row] == 0:
						ENTERED_BOARD[col][row] = 4
						drawInputBoard()
						drawMainBoard()
						pygame.display.update()
			
			if event.key == pygame.K_5:
				if Selected:
					if BOARD[col][row] == 0:
						ENTERED_BOARD[col][row] = 5
						drawInputBoard()
						drawMainBoard()
						pygame.display.update()
			
			if event.key == pygame.K_6:
				if Selected:
					if BOARD[col][row] == 0:
						ENTERED_BOARD[col][row] = 6
						drawInputBoard()
						drawMainBoard()
						pygame.display.update()
			
			if event.key == pygame.K_7:
				if Selected:
					if BOARD[col][row] == 0:
						ENTERED_BOARD[col][row] = 7
						drawInputBoard()
						drawMainBoard()
						pygame.display.update()
			
			if event.key == pygame.K_8:
				if Selected:
					if BOARD[col][row] == 0:
						ENTERED_BOARD[col][row] = 8
						drawInputBoard()
						drawMainBoard()
						pygame.display.update()

			if event.key == pygame.K_9:
				if Selected:
					if BOARD[col][row] == 0:
						ENTERED_BOARD[col][row] = 9
						drawInputBoard()
						drawMainBoard()
						pygame.display.update()
			
			if event.key == pygame.K_p:
				if isValid(BOARD , ENTERED_BOARD[col][row] , SelectedPos[0] , SelectedPos[1]):
					BOARD[col][row] = ENTERED_BOARD[col][row]
					ENTERED_BOARD[col][row] = 0
					drawInputBoard()		
					drawMainBoard()
					pygame.display.update()
				else:
					ENTERED_BOARD[col][row] = 0
					drawInputBoard()
					drawMainBoard()

				Selected = False

			if event.key == pygame.K_BACKSPACE:
				ENTERED_BOARD[col][row] = 0
				drawInputBoard()
				drawMainBoard()

			if event.key == pygame.K_SPACE:
				while not(Is_solved(BOARD)):
					BOARD = Solve(BOARD)
					pygame.time.delay(200)
					drawMainBoard()
					pygame.display.update()

			if event.key == pygame.K_r:
				BOARD = genBoard()
				seconds , minutes = 0 , 0
				ENTERED_BOARD = [[0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0] , 
				 [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0] , 
				 [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0] , 
				 [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0] , 
				 [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0] , 
				 [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0] , 
				 [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0] , 
				 [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0] , 
				 [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0] ]
				drawInputBoard()
				drawMainBoard()
				pygame.display.update()
		
		
		if milleseconds >= 1000:
			seconds += 1
			milleseconds -= 1000

		if seconds >= 60:
			minutes += 1
			seconds -= 60

		if (Is_solved(BOARD)):
			pygame.time.delay(2000)
			seconds , minutes = 0 , 0

		if Selected:
			highlight(SelectedPos[0] , SelectedPos[1])
		else:
			drawLines()

	pygame.draw.rect(SCREEN , BG_COLOR , (650 , 735 , 80 , 80))
	milleseconds += Clock.tick_busy_loop(60)
	TEXT = MEDIUM_FONT.render('{}:{}'.format(minutes , seconds) , 1 , MAIN_TEXT_COLOR)
	SCREEN.blit(TEXT , ((650, 735)))

	pygame.display.update()
			

pygame.quit()
sys.exit()