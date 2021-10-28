'''
A robot moves in a plane starting from the original point (0,0). 
The robot can move toward UP, DOWN, LEFT and RIGHT with a given steps. 
The trace of robot movement is shown as the following:

UP 5
DOWN 3
LEFT 3
RIGHT 2

The numbers after the direction are steps. 
Please write a program to compute the distance from current position after a sequence of movement and original point.
 If the distance is a float, then just print the nearest integer. 
 Example: If the following tuples are given as input to the program:

UP 5
DOWN 3
LEFT 3
RIGHT 2
Then, the output of the program should be:

2

'''
vert_list=[]
horiz_list=[]
while True:
    s=input('Enter movement of the Robot as {Direction} and {Steps} : ')
    if s=='':
        break
    l=s.split(' ')
    if l[0].lower() == 'up':
        vert_list.append(int(l[1]))
    elif l[0].lower() == 'down':
        vert_list.append(-int(l[1]))
    elif l[0].lower() == 'left':
        horiz_list.append(-int(l[1]))
    elif l[0].lower() == 'right':
        horiz_list.append(int(l[1]))
    else:
        pass
print ("Vertical list: ", vert_list)
print ("Horizontal list: ", horiz_list)

rob_horiz_pos=sum(horiz_list)
rob_vert_pos=sum(vert_list)

# print ("Vertical pos: ", rob_vert_pos)
# print ("Horizontal ps: ", rob_horiz_pos)

distance = round((abs(rob_horiz_pos)**2 + abs(rob_vert_pos)**2)**0.5)
print (f'Distance of the Robot from the original position is : {distance}')
