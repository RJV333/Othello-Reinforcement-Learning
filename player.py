#from sklearn.neural_network import MLPRegressor
import NN
from NN import *
import random
import othello
from othello import *
from math import exp
import operator

QLR = .1


class RL_player():

	def __init__(self):
		self.mlp = MLP_NeuralNetwork(64, 44, 64, 1, .1, 0, 0)
		#self.board = Othello_game_state()
		self.a = 1
		self.b = 0.9999995
		self.c =0.002
		self.numgames = 1
		self.temp = self.get_temp()
		self.games_won = 0

	def get_temp(self):
		return pow( (self.a*self.b), self.numgames )

	def Q_learn(self, NNinputs, valid_moves, oldmove, oldQval):
		outputs = self.mlp.feedForward(NNinputs)

		maxQval = outputs[ valid_moves[0] ]
		for move in valid_moves:
			if maxQval < outputs[ move ]:
				maxQval = outputs[ move ]

		target = (1-QLR)*oldQval + (QLR)* maxQval
		#print "target here is ", target
		#print "oldmove", oldmove
		#print "outputs", len(outputs), outputs
		outputs[oldmove] = target

		self.mlp.backPropagate(outputs)

		#return target

	def Q_learn_final(self, NNinputs, valid_moves, oldmove, oldQval, reward):
		outputs = self.mlp.feedForward(NNinputs)


		target = (1-QLR)*oldQval + (QLR)* reward

		outputs[oldmove] = target

		self.mlp.backPropagate(outputs)

		#return target	

	def place_move(self, NNinputs, valid_moves, board):
		#inputs = self.board.game_state()
		outputs = self.mlp.feedForward(NNinputs)
		#index of valid moves
		#valid_moves = self.board.output_valid()
		#index of move to make
		move = self.select_move(outputs, valid_moves)
		#backtoboard
		boardmove = self.boardmove(move)
		return boardmove, outputs[move]

	def place_move2(self, NNinputs, valid_moves, board):
		outputs = self.mlp.feedForward(NNinputs)
		x = random.randint(1,5)
		if x < 5:
			#print"c1"
			move = self.pure_move( NNinputs, valid_moves, board)
			ind = move[0]*8 + move[1]%8
			#print move, outputs[ind]
			return move, outputs[ind]
		elif x==5:
			#print"c2"
			choice = random.randint(0, len(valid_moves)-1 )
			#print self.boardmove( valid_moves[choice] ), outputs[ valid_moves[choice] ]			
			return self.boardmove( valid_moves[choice] ), outputs[ valid_moves[choice] ]


	def select_move(self, outputs, moves):
		#print"testing", outputs, moves
		self.temp = self.get_temp()
		distr = []
		summ = 0
		for move in moves:
			val =  exp(  float(outputs[move])   / float( self.temp )    )
			summ += val
			distr.append(val)

		spot = random.uniform(0, summ)
		ind = -1

		if spot == 0:
			return moves[ind+1]

		while spot>=0:
			#print distr, spot, ind
			ind+=1
			#print distr, spot, ind
			spot = spot - distr[ind]

		return moves[ind]

	def boardmove(self, move):

		boardmove= []
		boardmove.append( move/8 )
		boardmove.append(move%8 )
		return boardmove

	def get_r_and_s(self):
		move = self.make_move()
		#mak move on board
		r = self.board.makemove(move[0], move[1])
		target = self.computetarget( r, outputs[move] )

		outputs[move] = target

		self.mlp.backPropagate

	def write_weights(self, filename):
		f = open(filename, 'w')
		for arr in range(len( self.mlp.wi)):
			for weight in range(len ( self.mlp.wi[arr] ) ):
				f.write( str(self.mlp.wi[arr][weight]) )
				#f.write(str(arr) )
				#f.write(" ")
				#f.write(str( weight) )
				f.write( "\n" ) 
		for arr in range(len( self.mlp.wo) ):
			for weight in range(len( self.mlp.wo[arr] ) ):
				#f.write(str(arr) )
				#f.write(" ")
				#f.write(str( weight) )
				f.write( str(self.mlp.wo[arr][weight]) )
				f.write( "\n" )

	def write_weights1(self, filename):
		f = open(filename, 'w')
		for arr in range(len( self.mlp.wi)):
			for weight in range(len ( self.mlp.wi[arr] ) ):
				f.write( str(self.mlp.wi[arr][weight]) )
				f.write(str(arr) )
				f.write(" ")
				f.write(str( weight) )
				f.write( "\n" ) 
	def write_weights2(self, filename):
		f = open(filename, 'w')
		for arr in range(len( self.mlp.wo) ):
			for weight in range(len( self.mlp.wo[arr] ) ):
				f.write(str(arr) )
				f.write(" ")
				f.write(str( weight) )
				f.write( str(self.mlp.wo[arr][weight]) )
				f.write( "\n" )

	def read_weights(self, filename):
		f = open(filename, 'r')

		for arr in range(len(self.mlp.wi) ):
			for weight in range(len( self.mlp.wi[arr] ) ) :
				l = f.readline()
				if l == "":
					l = 0
				l = float(l)
				self.mlp.wi[arr][weight] = l

		for arr in range(len(self.mlp.wo) ):
			for weight in range(len( self.mlp.wo[arr] ) ):
				l = f.readline()
				if l == "":
					l = 0
				l = float(l)
				self.mlp.wo[arr][weight] = l

	def read_weights1(self, filename):
		f = open(filename, 'r')
		for arr in range(len(self.mlp.wi) ):
			for weight in range(len( self.mlp.wi[arr] ) ) :
				l = f.readline()
				if l == "":
					l = 0
				l = float(l)
				self.mlp.wi[arr][weight] = l

	def read_weights2(self, filename):
		f = open(filename, 'r')
		for arr in range(len(self.mlp.wo) ):
			for weight in range(len( self.mlp.wo[arr] ) ):
				l = f.readline()
				if l == "":
					l = 0
				l = float(l)
				self.mlp.wo[arr][weight] = l

	def pure_move(self, NNinputs, valid_moves, board):
		moves = {}
		outputs = self.mlp.feedForward(NNinputs)
		for move in valid_moves:
			moves[move] = outputs[move]

		result = max(moves.iteritems(), key=operator.itemgetter(1))[0]
		return self.boardmove( result )

	def least_move(self, NNinputs, valid_moves, board):
		moves = {}
		outputs = self.mlp.feedForward(NNinputs)
		for move in valid_moves:
			moves[move] = outputs[move]

		result = max(moves.iteritems(), key=operator.itemgetter(1))[0]
		return self.boardmove( result )








