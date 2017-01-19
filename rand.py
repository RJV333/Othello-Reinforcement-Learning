import random
from player import *


def random_trail(player):

	games = 100
	n = 0
	rando = random_player()

	while n < games:
		pure_game( rando, player )
		n+=1

def vs_trail(player, player2):

	games = 100
	n = 0
	while n < games:
		pure_game( player, player2 )
		n+=1

def pure_game(black, white):
	
	board = Othello_game_state()

	board.startgame()


	while( board.gameon() ):
		#print board.valid_moves
		#print board.other_valid
		#print""
		if board.turn == 'B' and board.valid_moves:
			#print "black"
			move = black.pure_move( board.game_state(), board.output_valid(), board)
			board.make_move(move)
		if board.turn == 'W' and board.valid_moves:
			#print "white"
			move = white.pure_move( board.game_state(), board.output_valid(), board )
			board.make_move(move)
		#board.printboard()

		board.flip_players()
		board.available_moves()
		board.other_available()

	rewards = board.score()
	print "rewards", rewards
	if rewards[0] > rewards[1]:
		black.games_won+=1
	elif rewards[1] > rewards[0]:
		white.games_won+=1


class random_player():

	def __init__(self):
		self.games_won = 0

	def pure_move(self, NN, valid_moves, board):

		choice = random.randint(0, ( len(valid_moves)-1 ) )
		boardmove = [valid_moves[choice]/8, valid_moves[choice]%8  ]
		return boardmove

