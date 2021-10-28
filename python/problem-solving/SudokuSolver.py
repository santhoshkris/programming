# sudokusolve.py
""" Sudoku Solver
    Note: A description of the sudoku puzzle can be found at:

        https://en.wikipedia.org/wiki/Sudoku

    Given a string in SDM format, described below, write a program to find and
    return the solution for the sudoku puzzle in the string. The solution should
    be returned in the same SDM format as the input.

    Some puzzles will not be solvable. In that case, return the string
    "Unsolvable".

    The general SDM format is described here:

        http://www.sudocue.net/fileformats.php

    For our purposes, each SDM string will be a sequence of 81 digits, one for
    each position on the sudoku puzzle. Known numbers will be given, and unknown
    positions will have a zero value.

    For example, assume you're given this string of digits (split into two lines
    for readability):

        0040060790000006020560923000780610305090004
             06020540890007410920105000000840600100

    The string represents this starting sudoku puzzle:

             0 0 4   0 0 6   0 7 9
             0 0 0   0 0 0   6 0 2
             0 5 6   0 9 2   3 0 0

             0 7 8   0 6 1   0 3 0
             5 0 9   0 0 0   4 0 6
             0 2 0   5 4 0   8 9 0

             0 0 7   4 1 0   9 2 0
             1 0 5   0 0 0   0 0 0
             8 4 0   6 0 0   1 0 0

    The provided unit tests may take a while to run, so be patient.
"""
#Easy
#puzzle = '049000203026080005070900001000100000680000009702050000000400008800060904030700000'
#Easy-664
#puzzle = '082000010000000083100040709007210600000605900000900000301000000060000400945000302'
#Med-665
# puzzle = '000010500600030001900040007000802000006000900002067000001020300070300090080000000'
#Med-666
#puzzle='080000002010060000000950030600000900070080000000200504900000000140000605068030000'
#Med-664
#puzzle = '570000000000100800040007020908050000000086000000070609700630005009000040300200090'
#Med-669
#puzzle = '000000001120008040000023060090800070000070000004900003200300105000000900009004000'
#Med-671
puzzle='000000023000710008000000060005006800080130050000400001100000045296000000050009000'
#Med-672
# puzzle=''

boxes = [(0,0),(0,3),(0,6),(3,0),(3,3),(3,6),(6,0),(6,3),(6,6)]
all_rows = []
empty_cells=[]

#Read the SDM and create the puzzle rows 

def populate_puzzle():
    i=0
    while i<len(puzzle):
        l = [int(i) for i in puzzle[i:i+9]]
        all_rows.append(l)
        i+=9
    print('\nSudoku puzzle is: \n')

def display_puzzle():
    print('-'*37)
    for i in all_rows:
        print('| ', end='')
        for j in i:
            print(j, end=' | ')
        print('')
        print('-'*37)

def pass_through_and_update():
    global empty_cells
    empty_cells=[]
    for i in range(0,9):
        for j in range(0,9):
            if all_rows[i][j] == 0:
                empty_cells.append(tuple([i,j]))
    # print ("Empty cells are: ", empty_cells)
    # print("# of empty cells: ", len(empty_cells))
    possibilites = {}
    #1st PASS
    for i in empty_cells:
        cell = i
        chances=[]
        current_row = all_rows[cell[0]]
        current_col = [i[cell[1]] for i in all_rows]
        box = 0
        # print(cell[0], cell[1])
        for i,a in enumerate(boxes):
            # print(i, a[0]+2, a[1]+2)
            if cell[0]<=a[0]+2 and cell[1]<=a[1]+2:
                box = i
                break

        # print ('For cell: ', cell)
        # print ('Row is : ', current_row)
        # print ('Column is: ', current_col)
        # print("The cell falls in the box: ", box+1)
        #check possiblities for given empty cell
        box_items = []
        for i in range(boxes[box][0],boxes[box][0]+3):
            for j in range(boxes[box][1],boxes[box][1]+3):
                box_items.append(all_rows[i][j])
        # print ("The box items are: ", box_items)

        for i in range(1, 10):
            if (i not in current_row) and (i not in current_col) and (i not in box_items):
                chances.append(i)
        possibilites[cell] = chances
    print(possibilites)

    #check box possiblities and update

    for i in boxes:
        for j in range(i[0],i[0]+3):
            for k in range(i[1],i[1]+3):
                c_cell = tuple([j,k])
                if c_cell in possibilites.keys():
                    # print('Checking for possiblities from cell ', c_cell)
                    for x in possibilites[c_cell]:
                        not_found = True
                        # print('Possiblities checking for is: ', x)
                        for l in range(i[0], i[0]+3):
                            for m in range(i[1], i[1]+3):
                                if tuple([l,m]) != c_cell and (l,m) in possibilites.keys():
                                    # print (f"Now looking at cell {l},{m} or value {x}")
                                    if x not in possibilites[l,m] and not_found:
                                        not_found=True
                                    else:
                                        not_found=False
                        # print("Not found value is ", not_found)
                        if not_found:
                            # print(f'Value {x} is unique to cell', c_cell)
                            possibilites[c_cell]=[x]
    
    for k,v in possibilites.items():
        if len(v)==1:
            print("Only 1 possiblity found at...",k)
            all_rows[k[0]][k[1]]=v[0]


populate_puzzle()

display_puzzle()

passes=0
while True:
    pass_through_and_update()
    passes+=1    
    if len(empty_cells) == 0:
        print("No more empty cells....")
        break
    if passes>25:
        print("Seems like a deadlock....")
        break

print("\nSolved....Solution is : \n")

display_puzzle()

print('\nPasses : ', passes, '\n')