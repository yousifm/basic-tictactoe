from tictactoe import *

def test():
	board1 = [["X"]*3 for i in range(3)]
	assert possible_moves(board1) == []
	assert check_winner(board1) == 'X'
	assert indices("a1") == (0, 0)
	assert indices("b2") == (1, 1)
	assert indices("c3") == (2, 2)
	board2 = [["O", "O", "X"], ["X", "O", "X"], ["O", "X", "X"]]
	assert check_winner(board2) == 'X'
	board3 = [[" "]*3 for i in range(3)]
	assert check_winner(board3) is None
	assert possible_moves(board3) == [c+r for c in "abc" for r in "123"]

test()