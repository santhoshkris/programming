'''
There exists a staircase with N steps, and you can climb up either 1 or 2 steps at a time. 
Given N, write a function that returns the number of unique ways you can climb the staircase. The order of the steps matters.

For example, if N is 4, then there are 5 unique ways:

1, 1, 1, 1
2, 1, 1
1, 2, 1
1, 1, 2
2, 2
What if, instead of being able to climb 1 or 2 steps at a time, you could climb any number from a set of 
positive integers X? For example, if X = {1, 3, 5}, you could climb 1, 3, or 5 steps at a time.

'''


def num_ways_stairs(n,X):
    ways = [0]*(n+1)
    ways[0]=1
    ways[1]=1
    for i in range(2,n+1):
        for j in X:
            if i-j >= 0:
                ways[i] += ways[i-j]
    return ways[n]

valid_steps = [1,2,5]
target = 6
print(num_ways_stairs(target,valid_steps))
