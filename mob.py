from player import *
import copy

class mob_player():

	def __init__(self):
		self.w1 = 10
		self.w2 = 1
		self.games_won = 0


	def pure_move(self, NNinputs, valid_moves, board):
		if board.emp_board() > 13:
			#print board.emp_board()
			return self.method1(valid_moves, board)
		else: 
			return self.method2(valid_moves, board)


	def method1(self, valid_moves, board):
		possible_moves= []

		for move in valid_moves:
			newboard = copy.deepcopy( board )
			boardmove = [ move/8 , move%8 ]
			newboard.make_move( boardmove ) 
			possible_moves.append( newboard )

		mx = self.evaluate( possible_moves[0] )

		evaluations = []
		for b in range( len( possible_moves) ):
			evaluations.append( self.evaluate( possible_moves[b] ) )
		
		ind = evaluations.index( max(evaluations) )
		move = valid_moves[ind]

		return [move/8, move%8]

	def method2(self, valid_moves, board):
		possible_moves= []

		for move in valid_moves:
			newboard = copy.deepcopy( board )
			boardmove = [ move/8 , move%8 ]
			newboard.make_move( boardmove ) 
			possible_moves.append( newboard )

		mx = self.pieces( possible_moves[0] )

		evaluations = []
		for b in range( len( possible_moves) ):
			evaluations.append( self.pieces( possible_moves[b] ) )
		
		ind = evaluations.index( max(evaluations) )
		move = valid_moves[ind]

		return [move/8, move%8]

	def pieces(self, board):
		mob=0
		opp=0
		for row in range(len(board.board) ):
			for col in range(len(board.board[row] ) ):
				if board.board[row][col] == board.turn:
					mob+=1
				elif board.board[row][col] == board.other_piece:
					opp+=1
		return mob - opp

	def evaluate(self, board):

		c = self.corners(board)
		m = self.mobility(board)

		if m[0] == 0 and m[1] == 0:
			return -40000

		eva = self.w1 * (c[0] -c[1]) + self.w2* ( float(m[0]-m[1]) / float(m[0]+m[1]) )
		return eva

	def corners(self, board):
		mob = 0
		opp = 0
		if board.board[0][0] == board.turn:
			mob+=1
		if board.board[0][0] == board.other_piece:
			opp+=1
		if board.board[0][7] == board.turn:
			mob+=1
		if board.board[0][7] == board.other_piece:
			opp+=1
		if board.board[7][0] == board.turn:
			mob+=1
		if board.board[7][0] == board.other_piece:
			opp+=1
		if board.board[7][7] == board.turn:
			mob+=1
		if board.board[7][7] == board.other_piece:
			opp+=1
		return mob, opp

	def mobility(self, board):
		mob = len( board.available_moves() )
		opp = len( board.other_available() )
		#print mob, opp
		return mob, opp