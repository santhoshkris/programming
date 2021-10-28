# TIC TAC TOE GAME

import os

winning_combos = [
				 	[1,2,3],
				 	[4,5,6],
				 	[7,8,9],
				 	[1,4,7],
				 	[2,5,8],
				 	[3,6,9],
				 	[1,5,9],
				 	[3,5,7]
				 ]
#board = ["   "]*9
board = ["{"+str(x+1)+"}" for x in range(9)]

def update_board(icon, pos):
	board[pos-1] = " "+icon+" "


def display_board():
	print (board[0]+"|"+board[1]+"|"+board[2])
	print ("-"*10)
	print (board[3]+"|"+board[4]+"|"+board[5])
	print ("-"*10)
	print (board[6]+"|"+board[7]+"|"+board[8])
	print ("\n")

def check_victory(pos_list):

	#print (f'Position to check is: {pos_list}')
	pos_list.sort()
	for i in winning_combos:
		# print (f'Checking for the combiniation: {i}')
		if set(i).issubset(set(pos_list)):
			#print (f'Matched here.... {i}')
			return True
	return False


def game_start():
	
	avail_cells = [1,2,3,4,5,6,7,8,9]
	x_pos = []
	o_pos=[]

	while True:

		display_board()
		p=0
		while p not in avail_cells:
			p = int(input('Enter the number of an empty position to play for "X"...'))
		update_board("X",p)
		display_board()
		x_pos.append(int(p))
		avail_cells.remove(p)
		r = check_victory(x_pos)
		if r:
			print ("X WINS.....\n\n")
			break
		elif len(avail_cells) == 0:
			print ("It is a TIE....")
			break

		p=0
		while p not in avail_cells:
			p = int(input('Enter the number of an empty position to play for "O"...'))
		update_board("O",int(p))
		display_board()
		o_pos.append(int(p))
		avail_cells.remove(p)
		r1 = check_victory(o_pos)
		if r1:
			print ("O WINS....\n\n")
			break
		elif len(avail_cells) == 0:
			print ("It is a TIE....\n\n")
			break

def main ():
	os.system("clear")
	print ( "Let's PLAY TIC TAC TOE..\n")
	game_start()

if __name__ == '__main__':
	main()
