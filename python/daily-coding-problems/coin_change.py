'''
a) You are given coins of different denominations and a total amount of money. 
Write a function to compute the number of combinations that make up that amount. 
You may assume that you have infinite number of each kind of coin. 

Example 1:

Input: amount = 5, coins = [1, 2, 5]
Output: 4
Explanation: there are four ways to make up the amount:
5=5
5=2+2+1
5=2+1+1+1
5=1+1+1+1+1

b) You are given coins of different denominations and a total amount of money amount. 
Write a function to compute the fewest number of coins that you need to make up that amount. 
If that amount of money cannot be made up by any combination of the coins, return -1.

You may assume that you have an infinite number of each kind of coin.

Example 1:

Input: coins = [1,2,5], amount = 11
Output: 3
Explanation: 11 = 5 + 5 + 1
'''

def num_ways(amount, coins):
    a = [0]*(amount+1)
    a[0]=1
    for i in coins:
        for j in range(0,amount+1):
            if j >= i:
                a[j] = a[j] + a[j-i]
    return (a[amount])

def min_coins(amount,coins):
    a = [float('inf')]*(amount+1)
    a[0]=0
    for i in coins:
        for j in range(0,amount+1):
            if j >= i:
                a[j] = min(a[j], 1+a[j-i])
    return a[amount] if a[amount] != float('inf') else -1

amount=12
coins=[1,2,5]
print(f"Number of ways to make {amount} with {coins} : ", num_ways(amount,coins))
print(f"Minimum number of coins needed to make {amount} with {coins} : ",min_coins(amount,coins))
