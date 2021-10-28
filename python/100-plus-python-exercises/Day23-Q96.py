'''
You are given a string S and width W. Your task is to wrap the string into a paragraph of width.

If the following string is given as input to the program:

ABCDEFGHIJKLIMNOQRSTUVWXYZ
4
Then, the output of the program should be:

ABCD
EFGH
IJKL
IMNO
QRST
UVWX
YZ
'''

# s = 'ABCDEFGHIJKLIMNOQRSTUVWXYZ'
# new_s=[]

# i=0
# while i<len(s):
#     if (i+4) <= len(s):
#         print(i,s[i:i+4])
#         new_s.append(s[i:i+4])
#     else:
#         print("Remaining",i,s[i:])
#         new_s.append(s[i:])
#         break
#     i+=4
# print (new_s)

import itertools
string = input("> ")
width_length = int(input("What is the width of the groupings? "))

def grouper(string, width):
    iters = [iter(string)] * width
    print (itertools.zip_longest(*iters, fillvalue=''))
    return itertools.zip_longest(*iters, fillvalue='')

def displayer(groups):
    for x in groups:
        if x == '':
            continue
        else:
            print(''.join(x))

displayer(grouper(string, width_length))