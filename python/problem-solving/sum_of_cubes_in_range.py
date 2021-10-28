'''
Write a Python function that takes a positive integer and returns the sum of the cube of all the positive integers 
smaller than the specified number.
'''
from functools import reduce
n=8
print(reduce(lambda acc,x:acc+x**3, [i for i in range(1,n)]))

