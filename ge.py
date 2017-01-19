import player
from player import *
import timeit
import pickle
import mob
from mob import *
import pos
from pos import *
import rand
from rand import *
import greedy
from greedy import *

def train_players():
	board = Othello_game_state()
	black = RL_player()
	white = RL_player()
	#black = pickle.load( open("newblack3.p", "rb") )
	#white = pickle.load( open("newwhite3.p", "rb") )

	print black.mlp.wi
	print black.mlp.wo
	start = timeit.timeit()

	n = 0
	while  n < 1000000:
		if n%100 == 0:
			print n
		traingame(board, black, white)
		board = Othello_game_state()
		n+=1
	
	pickle.dump( black, open( "bbnewsel.p", "wb" ) )
	pickle.dump( white, open( "bwnewsel.p", "wb" ) )


	n = 0
	while  n < 1000000:
		if n%100 == 0:
			print n
		traingame(board, black, white)
		board = Othello_game_state()
		n+=1
	
	pickle.dump( black, open( "bbnewsel2.p", "wb" ) )
	pickle.dump( white, open( "bwnewsel2.p", "wb" ) )


	black.write_weights("whyb2.txt")
	white.write_weights("whyw2.txt")

	return black, white

def traingame(board, black, white):

	move = black.place_move2(board.game_state(), board.output_valid(), 1 )
	board.make_move( move[0] )
	black_oldQval = move[1]
	black_oldmove = (move[0][0]*8) + (move[0][1]%8)

	board.flip_players()
	board.available_moves()
	board.other_available()


	move = white.place_move2(board.game_state(), board.output_valid(), 1 )
	board.make_move( move[0] )
	white_oldQval = move[1]
	white_oldmove = (move[0][0]*8) + (move[0][1]%8)

	board.flip_players()
	board.available_moves()
	board.other_available()
	while ( board.gameon() ):

		if board.turn == 'B' and board.valid_moves:
			black.Q_learn(  board.game_state(), board.output_valid(), black_oldmove, black_oldQval )
			move = black.place_move2( board.game_state(), board.output_valid(), 1 )
			board.make_move(move[0])
			black_oldQval = move[1]
			black_oldmove = (move[0][0]*8) + (move[0][1]%8)

		if board.turn == 'W' and board.valid_moves:
			white.Q_learn( board.game_state(), board.output_valid(), white_oldmove, white_oldQval )
			move = white.place_move2( board.game_state(), board.output_valid(), 1 )
			board.make_move(move[0])
			white_oldmove = (move[0][0]*8) + (move[0][1]%8)

		
		#board.printboard()
		#print ""
		board.flip_players()
		board.available_moves()
		board.other_available()


	#rewards are returned in a tuple, the reward for black and then white
	rewards = board.score()
	black.Q_learn_final(  board.game_state(), board.output_valid(), black_oldmove, black_oldQval, rewards[0] )
	white.Q_learn_final( board.game_state(), board.output_valid(), white_oldmove, white_oldQval, rewards[1] )
	black.numgames+=1
	white.numgames+=1

def train_rand():
	board = Othello_game_state()
	black = RL_player()
	white = random_player()

	n = 0
	while  n < 1000000:
		if n%100 == 0:
			print n
		fixedtraingame(board, black, white)
		board = Othello_game_state()
		n+=1

	pickle.dump( black, open( "ranb.p", "wb" ) )

	n = 0
	while  n < 1000000:
		if n%100 == 0:
			print n
		fixedtraingame(board, black, white)
		board = Othello_game_state()
		n+=1

	pickle.dump( black, open( "ranb2.p", "wb" ) )

	return black, white

def train_greedy():
	board = Othello_game_state()
	black = RL_player()
	white = greedy_player()

	n = 0
	while  n < 1000000:
		if n%100 == 0:
			print n
		fixedtraingame(board, black, white)
		board = Othello_game_state()
		n+=1

	pickle.dump( black, open( "greed.p", "wb" ) )

	n = 0
	while  n < 1000000:
		if n%100 == 0:
			print n
		fixedtraingame(board, black, white)
		board = Othello_game_state()
		n+=1

	pickle.dump( black, open( "greed2.p", "wb" ) )

	return black, white


def train_mob():
	board = Othello_game_state()
	black = RL_player()
	white = mob_player()

	n = 0
	while  n < 1000000:
		if n%100 == 0:
			print n
		fixedtraingame(board, black, white)
		board = Othello_game_state()
		n+=1

	pickle.dump( black, open( "mob_bos.p", "wb" ) )

	n = 0
	while  n < 1000000:
		if n%100 == 0:
			print n
		fixedtraingame(board, black, white)
		board = Othello_game_state()
		n+=1

	pickle.dump( black, open( "mob_b2os.p", "wb" ) )

	return black, white

def train_pos():
	board = Othello_game_state()
	black = RL_player()
	white = pos_player()

	n = 0
	while  n < 1000000:
		if n%100 == 0:
			print n
		fixedtraingame(board, black, white)
		board = Othello_game_state()
		n+=1

	pickle.dump( black, open( "npos_bos.p", "wb" ) )

	n = 0
	while  n < 1000000:
		if n%100 == 0:
			print n
		fixedtraingame(board, black, white)
		board = Othello_game_state()
		n+=1

	pickle.dump( black, open( "npos_b2os.p", "wb" ) )

	return black, white


def fixedtraingame(board, black, whitefixed):

	board.startgame()


	move = black.place_move(board.game_state(), board.output_valid(), 1 )
	board.make_move( move[0] )
	black_oldQval = move[1]
	black_oldmove = (move[0][0]*8) + (move[0][1]%8)

	board.flip_players()
	board.available_moves()
	board.other_available()


	move = whitefixed.pure_move(board.game_state(), board.output_valid(), board )
	board.make_move( move )

	board.flip_players()
	board.available_moves()
	board.other_available()

	while ( board.gameon() ):

		if board.turn == 'B' and board.valid_moves:
			black.Q_learn(  board.game_state(), board.output_valid(), black_oldmove, black_oldQval )
			move = black.place_move( board.game_state(), board.output_valid(), 1 )
			board.make_move(move[0])
			black_oldQval = move[1]
			black_oldmove = (move[0][0]*8) + (move[0][1]%8)

		if board.turn == 'W' and board.valid_moves:
			move = whitefixed.pure_move( board.game_state(), board.output_valid(), board )
			board.make_move(move)

		
		#board.printboard()
		#print ""
		board.flip_players()
		board.available_moves()
		board.other_available()


	#rewards are returned in a tuple, the reward for black and then white
	rewards = board.score()
	#print rewards
	black.Q_learn_final(  board.game_state(), board.output_valid(), black_oldmove, black_oldQval, rewards[0] )
	black.numgames+=1

	



