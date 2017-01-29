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
	player_token = get_input("Choose you token [%s, %s]>"%tokens,
					"Please enter %s or %s" %tokens,
					lambda x: x in tokens)

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
	p_move = get_input("Your turn>",
						"Enter column letter, row number (ex: a1).",
						lambda x: is_valid(x, board))
	
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
	return random.choice(allmax(scores, key = scores.get))

def play_game(board = [[' ']*3 for i in range(3)], strategy = computer_move):
	tokens = ('X', 'O')
	player, computer = get_player_computer_tokens(tokens)

	i = 0
	while i < 9:
		current_token = tokens[i%2]

		display_board(board)
		
		if current_token is player:
			player_move(player, board)

		elif current_token is computer:
			make_move(strategy(player, computer, board), computer, board)

		winner = check_winner(board)
		if winner:
			print winner, "wins!"
			return

		i += 1
	print "Draw"

def almost_win(board, token):
	diagonal_one = [board[i][i] for i in range(3)]
	diagonal_two = [board[i][2-i] for i in range(3)]
	columns = [[row[i] for row in board] for i in range(3)]

	for row_number, row in enumerate(board):
		if row.count(token) == 2 and row.count(" ") == 1:
			empty_slot = row.index(" ")
			return row_number, empty_slot

	for col_num, col in enumerate(columns):
		if col.count(token) == 2 and col.count(" ") == 1:
			empty_slot = col.index(" ")
			return empty_slot, col_num

	if diagonal_one.count(token) == 2 and diagonal_one.count(" ") == 1:
		empty_slot = diagonal_one.index(" ")
		return empty_slot, empty_slot

	elif diagonal_two.count(token) == 2 and diagonal_two.count(" ") == 1:
		empty_slot = diagonal_two.index(" ")
		return empty_slot, 2-empty_slot
	else:
		return None

def normal_difficulty(player, computer, board):
	win_play = almost_win(board, computer)
	block_play = almost_win(board, player)
	if win_play:
		return indices_to_letters(win_play)
	elif block_play:
		return indices_to_letters(block_play)
	else:
		return random.choice(possible_moves(board))

def get_empty_slot(lst):
	return lst.index(" ")

def indices_to_letters(indices):
	row, column = indices
	return ("abc"[column], row + 1)

if __name__ == '__main__':
	difficulty = get_input("Choose difficulty [easy, normal, impossible]> ",
						   "Enter easy ,normal or impossible> ",
						   lambda x : x.lower() in ["easy", "normal", "impossible"])
	if difficulty.lower() == "easy":
		computer_strategy = lambda _, __, board: random.choice(possible_moves(board))

	elif difficulty.lower() == "normal":
		computer_strategy = normal_difficulty

	elif difficulty.lower() == "impossible":
		computer_strategy = computer_move

	play_game(strategy = computer_strategy)