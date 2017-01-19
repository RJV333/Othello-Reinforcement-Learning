from player import *
import copy	

class greedy_player():


	def __init__(self):
		self.games_won = 0


	def pure_move(self, NNinputs, valid_moves, board):

			return self.method2(valid_moves, board)

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