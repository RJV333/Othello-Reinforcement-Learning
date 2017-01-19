import copy
import random

direction_list=[[-1,0],[-1,-1],[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1]]


class Othello_game_state:

    def __init__(self):
        self.board = self.make_startboard()
        self.turn = 'B'
        self.other_piece = self.opponent()
        self.valid_moves = self.available_moves()
        self.other_valid = self.other_available()

    def gameon(self):

        self.valid_moves = self.available_moves()
        self.other_valid = self.other_available()

        if self.valid_moves:
            return True
        elif self.other_valid:
            return True
        else:
            return False

    def playgame(self):

        while ( self.gameon() ):
            if self.valid_moves:
                self.playround()
                self.flip_players()
            else:
                self.flip_players()
                self.playround()
                self.flip_players()

    def game_state(self):
        NN_inputs = []

        for row in range(len(self.board)):
            for col in range(len(self.board[row] ) ):
                if self.board[row][col] == self.turn:
                    NN_inputs.append(1)
                elif self.board[row][col] == self.other_piece:
                    NN_inputs.append(-1)
                else:
                    NN_inputs.append(0)

        return NN_inputs

    def output_valid(self):
        results = []
        for move in self.valid_moves:
            t = (move[0]*8) + move[1]
            results.append(t)
        return results


    def make_startboard(self):
        board = []

        for row in range(8):
            newrow = []
            for col in range(8):
                newrow.append("_")
            board.append(newrow)

        board[3][3]= 'W'
        board[3][4] = 'B'
        board[4][3] = 'B'
        board[4][4] = 'W'
        return board

    def inbounds(self, cords):
        if 0 <= cords[0] and cords[0]<8 and 0<= cords[1] and cords[1] <8:
            return True
        else:
            return False

    def printboard(self):
        for row in range( len(self.board) ):
            print self.board[row]

    def scoreboard(self):
        B = 0
        W = 0
        for row in range(len(self.board)):
            for col in range( len(self.board[row] ) ):
                if self.board[row][col] == 'B':
                    B+=1
                if self.board[row][col] == 'W':
                    W+=1
        return B, W

    def opposite_turn(self):
# switch to other player's turn after making a move and update the board. if self.game_turn == Black_player:
        if self.turn ==B:
            self.turn = W
        elif self.turn == W:
            self.turn = B
        return self.turn

    def opponent(self):
        if self.turn == 'B': 
            self.other_piece = 'W'
        elif self.turn == 'W': 
            self.other_piece = 'B'
        return self.other_piece

    def flip_players(self):
        if self.turn == 'B': 
            self.other_piece = 'B'
            self.turn = 'W'
        elif self.turn == 'W': 
            self.turn = 'B'
            self.other_piece = 'W'

    def play_round(self):
        self.make_move(move)

    def make_move(self, move):
        #print self.turn, self.other_piece

        self.board[move[0]][move[1]] = self.turn
        for d in direction_list:
            self.make_flips(move, d)

        #self.flip_players()
        #print self.turn, self.other_piec


    def make_flips(self, move, direction):
        #print "make flips"
        bracket = self.find_bracket(move, direction)
        if not bracket:
            return None
        #print bracket, direction
        for pos in bracket:
            #print "here"
            self.board[pos[0]][pos[1]] = self.turn

    def find_bracket(self, move, direction):
        #print "find brack", direction, move
        nmove = copy.copy(move)
        bracket = nmove
        bracket[0] +=direction[0]
        bracket[1] +=direction[1]
        res = []
        if self.inbounds(bracket) == False:
            return None
        #res.append( bracket)
        if self.board[bracket[0]][bracket[1]] == self.turn:
            #print "first case", bracket[0], bracket[1], move
            return None
        while self.inbounds(bracket) and self.board[bracket[0]][bracket[1]] == self.other_piece:
            #print "second case", bracket
            res.append( copy.copy(bracket) )
            bracket[0] += direction[0]
            bracket[1] += direction[1]
            #res.append( bracket )
        #print "bottom", bracket, move, nmove
        if self.inbounds(bracket) == False:
            return None
        if self.board[ bracket[0] ][ bracket[1] ] == self.turn:
            #print "made it", res
            return res
        return None

    def available_moves(self):
        valid_moves = []
        for row in range (len(self.board) ):
            for col in range( len(self.board[row]) ):
                if self.is_valid( row, col ):
                    valid_moves.append( [row, col] )

        self.valid_moves = valid_moves
        return valid_moves

    def is_valid(self, row, col):
        if self.board[row][col] != '_':
            return False
        for d in direction_list:
            bracket = self.find_bracket([row, col], d)
            if bracket:
                return True
        return False


    def other_available(self):
        valid_moves = []
        for row in range (len(self.board) ):
            for col in range( len(self.board[row]) ):
                if self.other_is_valid( row, col ):
                    valid_moves.append( [row, col] )

        self.other_valid = valid_moves
        return valid_moves

    def other_is_valid(self, row, col):
        if self.board[row][col] != '_':
            return False
        for d in direction_list:
            bracket = self.other_find_bracket([row, col], d)
            if bracket:
                return True
        return False

    def other_find_bracket(self, move, direction):
        #print "find brack", direction, move
        nmove = copy.copy(move)
        bracket = nmove
        bracket[0] +=direction[0]
        bracket[1] +=direction[1]
        res = []
        if self.inbounds(bracket) == False:
            return None
        #res.append( bracket)
        if self.board[bracket[0]][bracket[1]] == self.other_piece:
            #print "first case", bracket[0], bracket[1], move
            return None
        while self.inbounds(bracket) and self.board[bracket[0]][bracket[1]] == self.turn:
            #print "second case", bracket
            res.append( copy.copy(bracket) )
            bracket[0] += direction[0]
            bracket[1] += direction[1]
            #res.append( bracket )
        #print "bottom", bracket, move, nmove
        if self.inbounds(bracket) == False:
            return None
        if self.board[ bracket[0] ][ bracket[1] ] == self.other_piece:
            #print "made it", res
            return res
        return None

    def score(self):
        B = 0
        W = 0
        for row in range(len(self.board)):
            for col in range(len(self.board[row]) ):
                if self.board[row][col] == 'B':
                    B+=1
                if self.board[row][col] == 'W':
                    W+=1
        if B > W:
            return (1,-1)
        elif W > B:
            return (-1, 1)
        else:
            return (0,0)
    def startgame(self):
        x = 0
        while( x <4 ):

            self.valid_moves = self.available_moves()
            self.other_valid = self.other_available()
            choice = random.randint(0, len(self.valid_moves)-1 )
            self.make_move( self.valid_moves[choice]  )
            self.flip_players()
            x+=1
    def emp_board(self):
        emp = 0
        for row in range(len(self.board) ):
            for col in range(len(self.board[row] ) ):
                if self.board[row][col] == "_":
                    emp+=1
        return emp






