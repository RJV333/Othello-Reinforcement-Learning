from player import *
import copy

class pos_player():

	def __init__(self):

		self.pos_values = self.make_values()
		self.games_won= 0

	def make_values(self):

		values = [ [100, -20, 10, 5, 5, 10, -20, 100] ,
				[-20, -50, -2, -2, -2, -2, -50, -20],
				[10, -2, -1, -1, -1, -1, -2, 10],
				[5, -2, -1, -1, -1, -1, -2, 5],
				[5, -2, -1, -1, -1, -1, -2, 5],
				[10, -2, -1, -1, -1, -1, -2, 10],
				[-20, -50, -2, -2, -2, -2, -50, -20],
				[100, -20, 10, 5, 5, 10, -20, 100]  ]
		return values

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

		evaluation = 0

		game_state = board.game_state()
		for r in range( len(self.pos_values) ):
			for c in range( len( self.pos_values[r] ) ):
				x = game_state.pop(0)
				evaluation += (x * self.pos_values[r][c] )

		return evaluation



