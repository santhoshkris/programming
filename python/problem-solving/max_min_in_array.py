'''
Write a Python function to find the maximum and minimum numbers from a sequence of numbers. 
PS: Do not use built-in functions.
'''

l=[3,6,5,7,8,2,9]

large,small = l[0],l[0]
for i in l:
    if i > large:
        large=i
    elif i < small:
        small=i
    else:
        pass
print(large,small)
