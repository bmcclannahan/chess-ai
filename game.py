import sys
import numpy as np
import logging
from Piece import Pawn, Bishop, Knight, Rook, Queen, King

class Game:

	#king = 6, queen = 5, rook = 4, horse = 3, bishop = 2, pawn = 1

	def __init__(self):		
		self.currentPlayer = 1
		self.gameState = GameState(np.array(self._createBoard(), dtype=np.int), 1)
		self.actionSpace = np.array(self._createBoard(), dtype=np.int)
		self.pieces = {'1':'WP', '2':'WB', '3':'WH', '4':'WR', '5':'WQ', '6':'WK', '0': '-', '-1':'BP', '-2':'BB', '-3':'BH', '-4':'BR', '-5':'BQ', '-6':'BK'}
		self.grid_shape = (8,8)
		self.input_shape = (2,8,8)
		self.name = 'chess'
		self.state_size = len(self.gameState.binary)
		self.action_size = len(self.actionSpace)

	def reset(self):
		self.gameState = GameState(np.array([0]*64, dtype=np.int), 1)
		self.currentPlayer = 1
		return self.gameState

	def step(self, action):
		next_state, value, done = self.gameState.takeAction(action)
		self.gameState = next_state
		self.currentPlayer = -self.currentPlayer
		info = None
		return ((next_state, value, done, info))

	def identities(self, state, actionValues):
		identities = [(state,actionValues)]

		currentBoard = state.board
		currentAV = actionValues

		currentBoard = np.array([
			  currentBoard[7], currentBoard[6], currentBoard[5],currentBoard[4], currentBoard[3], currentBoard[2], currentBoard[1], currentBoard[0]
			,currentBoard[15], currentBoard[14], currentBoard[13],currentBoard[12], currentBoard[11], currentBoard[10], currentBoard[9], currentBoard[0]
			,currentBoard[23], currentBoard[22], currentBoard[21],currentBoard[20], currentBoard[19], currentBoard[18], currentBoard[17], currentBoard[8]
			,currentBoard[31], currentBoard[30], currentBoard[29],currentBoard[28], currentBoard[27], currentBoard[26], currentBoard[25], currentBoard[16]
			,currentBoard[39], currentBoard[38], currentBoard[37],currentBoard[36], currentBoard[35], currentBoard[34], currentBoard[33], currentBoard[24]
			,currentBoard[47], currentBoard[46], currentBoard[45],currentBoard[44], currentBoard[43], currentBoard[42], currentBoard[41], currentBoard[32]
			,currentBoard[55], currentBoard[54], currentBoard[53],currentBoard[52], currentBoard[51], currentBoard[50], currentBoard[49], currentBoard[40]
			,currentBoard[63], currentBoard[62], currentBoard[61],currentBoard[60], currentBoard[59], currentBoard[58], currentBoard[57], currentBoard[56]
			])

		currentAV = np.array([
			  currentAV[7], currentAV[6], currentAV[5],currentAV[4], currentAV[3], currentAV[2], currentAV[1], currentAV[0]
			,currentAV[15], currentAV[14], currentAV[13],currentAV[12], currentAV[11], currentAV[10], currentAV[9], currentAV[0]
			,currentAV[23], currentAV[22], currentAV[21],currentAV[20], currentAV[19], currentAV[18], currentAV[17], currentAV[8]
			,currentAV[31], currentAV[30], currentAV[29],currentAV[28], currentAV[27], currentAV[26], currentAV[25], currentAV[16]
			,currentAV[39], currentAV[38], currentAV[37],currentAV[36], currentAV[35], currentAV[34], currentAV[33], currentAV[24]
			,currentAV[47], currentAV[46], currentAV[45],currentAV[44], currentAV[43], currentAV[42], currentAV[41], currentAV[32]
			,currentAV[55], currentAV[54], currentAV[53],currentAV[52], currentAV[51], currentAV[50], currentAV[49], currentAV[40]
			,currentAV[63], currentAV[62], currentAV[61],currentAV[60], currentAV[59], currentAV[58], currentAV[57], currentAV[56]
			])

		identities.append((GameState(currentBoard, state.playerTurn), currentAV))

		return identities

	def _createBoard(self):
		return [4,3,2,6,5,2,3,4,1,1,1,1,1,1,1,1]+[0]*32+[-1,-1,-1,-1,-1,-1,-1,-1,-4,-3,-2,-5,-6,-2,-3,-4]


class GameState():
	def __init__(self, board, playerTurn):
		self.board = board
		self.pieces = {'1':'WP', '2':'WB', '3':'WH', '4':'WR', '5':'WQ', '6':'WK', '0': '-', '-1':'BP', '-2':'BB', '-3':'BH', '-4':'BR', '-5':'BQ', '-6':'BK'}
		
		self.playerTurn = playerTurn
		self.binary = self._binary()
		self.id = self._convertStateToId()
		self.allowedActions = self._allowedActions()
		self.isEndGame = self._checkForEndGame()
		self.value = self._getValue()
		self.score = self._getScore()

	def _allowedActions(self):
		allowed = []
		for i in range(len(self.board)):
			if i >= len(self.board) - 7:
				if self.board[i]==0:
					allowed.append(i)
			else:
				if self.board[i] == 0 and self.board[i+7] != 0:
					allowed.append(i)

		return allowed

	def _binary(self):

		currentplayer_position = np.zeros(len(self.board), dtype=np.int)
		currentplayer_position[self.board==self.playerTurn] = 1

		other_position = np.zeros(len(self.board), dtype=np.int)
		other_position[self.board==-self.playerTurn] = 1

		position = np.append(currentplayer_position,other_position)

		return (position)

	def _convertStateToId(self):
		player1_position = np.zeros(len(self.board), dtype=np.int)
		player1_position[self.board==1] = 1

		other_position = np.zeros(len(self.board), dtype=np.int)
		other_position[self.board==-1] = 1

		position = np.append(player1_position,other_position)

		id = ''.join(map(str,position))

		return id

	def _checkForEndGame(self):
		kingInCheck = self._isAKingInCheck()
		if kingInCheck != 0:
			return 1

		return 0

	def _isAKingInCheck(self):
		whiteKing = np.where(self.board == 6)[0][0]
		blackKing = np.where(self.board == -6)[0][0]



	def _getValue(self):
		# This is the value of the state for the current player
		# i.e. if the previous player played a winning move, you lose
		for x,y,z,a in self.winners:
			if (self.board[x] + self.board[y] + self.board[z] + self.board[a] == 4 * -self.playerTurn):
				return (-1, -1, 1)
		return (0, 0, 0)


	def _getScore(self):
		tmp = self.value
		return (tmp[1], tmp[2])




	def takeAction(self, action):
		newBoard = np.array(self.board)
		newBoard[action]=self.playerTurn
		
		newState = GameState(newBoard, -self.playerTurn)

		value = 0
		done = 0

		if newState.isEndGame:
			value = newState.value[0]
			done = 1

		return (newState, value, done) 


	def renderP(self):
		print()
		print('1 2 3 4 5 6 7')
		for i in range(6):
			for j in range(7):
				sys.stdout.write(self.pieces[str(self.board[i*7+j])] + " ")
			print()
		print('--------------')


	def render(self, logger):
		for r in range(6):
			logger.info([self.pieces[str(x)] for x in self.board[7*r : (7*r + 7)]])
		logger.info('--------------')