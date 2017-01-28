import re
import random
from copy import deepcopy

def display_board(board):
	separator = "-"*15
	print "  | a | b | c |"
	print separator
	for number, row in enumerate(board):
		print number + 1, "| %s | %s | %s |" % tuple(row)
		print separator

def has_identical_elements(list):
	return len(set(list)) == 1

def check_winner(board):
	winner = None
	columns = [[row[i] for row in board] for i in range(len(board))]

	for row in board: winner = row[0] if   (has_identical_elements(row)
									   and row[0] != " ") else winner

	for col in columns: winner = col[0] if (has_identical_elements(col)
							             and col[0] != " ") else winner

	if board[0][0] == board[1][1] == board[2][2] and board[1][1] != " ":
		winner = board[1][1]
	if board[0][2] == board[1][1] == board[2][0] and board[1][1] != " ":
		winner = board[1][1]

	return winner

def get_input(message, fail_message, validation):
	user_input = raw_input(message)
	if not validation(user_input):
		print fail_message
		return get_input(message, fail_message, validation)
	return user_input
	
def get_player_computer_tokens(tokens):
	player_token = raw_input("Choose your token [%s, %s]>" %tokens)
	while player_token not in tokens:
		print "Please enter %s or %s" %tokens
		player_token = raw_input("Choose your token [%s, %s]>" %tokens)

	if player_token == tokens[0]:
		computer_token = tokens[1]
	else:
		computer_token = tokens[0]

	return player_token, computer_token	

def is_valid(move, board):
	if len(move) != 2: return False
	try:
		row, column = indices(move)
		if board[row][column] == " ": return True

	except:
		return False

def possible_moves(board):
	return [c + r for c in "abc" for r in '123' if is_valid(c+r, board)]

def indices(move):
	column, row = move
	return (int(row) - 1, "abc".index(column))

def make_move(mv, token, board):
	row, column = indices(mv)
	board[row][column] = token

def player_move(token, board):
	p_move = raw_input("Your turn> ").strip()
	
	while not is_valid(p_move, board):
		p_move = raw_input("Enter column letter, row number (ex: a1)>").strip()
	
	make_move(p_move, token, board)

def get_opponent(token, player, computer):
	if token == player: return computer
	elif token == computer: return player

def minimax(move, current, player, computer, board, a = float("-inf"), b = float("inf")):
	bn = deepcopy(board)
	make_move(move, current, bn)

	if check_winner(bn) == player: return -1
	elif check_winner(bn) == computer: return 1
	elif not len(possible_moves(bn)): return 0

	opponent = get_opponent(current, player, computer)

	if opponent == player:
		for move in possible_moves(bn):
			b = min(minimax(move, opponent, player, computer, bn, a, b), b)
			if b <= a: break
		return b

	elif opponent == computer:
		for move in possible_moves(bn):
			a = max(minimax(move, opponent, player, computer, bn, a, b), a)
			if b <= a: break
		return a

def allmax(iterable, key = lambda x: x):
	maximum = max(map(key, iterable))
	return [element for element in iterable if key(element) == maximum]

def computer_move(player, computer, board):
	scores = {}
	for move in possible_moves(board):
		scores[move] = minimax(move, computer, player, computer, board)
	make_move(random.choice(allmax(scores, key = scores.get)), computer, board)

def play_game(board = [[' ']*3 for i in range(3)]):
	tokens = ('X', 'O')
	player, computer = get_player_computer_tokens(tokens)

	i = 0
	while i < 9:
		current_token = tokens[i%2]

		if current_token is player:
			player_move(player, board)

		elif current_token is computer:
			computer_move(player, computer, board)
		
		display_board(board)

		winner = check_winner(board)
		if winner:
			print winner, "wins!"
			return

		i += 1
	print "Draw"


if __name__ == '__main__':
	Difficulty = get_input("Choose difficulty")
	play_game()