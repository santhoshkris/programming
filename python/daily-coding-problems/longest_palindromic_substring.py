'''
Given a string s, return the longest palindromic substring in s.

Example 1:

Input: s = "babad"
Output: "bab"
Note: "aba" is also a valid answer.
'''

def expandAroundCenter(s,i,j):
    print ("expanding around indices...",i,j)
    while i>=0 and j<len(s) and s[i] == s[j]:
        print("matching....")
        i-=1
        j+=1
    return s[i+1:j]

def longest_palindrome_substring(s):
    substr=""
    for i in range(len(s)):
        tempstr = expandAroundCenter(s,i,i)
        if len(tempstr) > len(substr):
            substr = tempstr
        tempstr = expandAroundCenter(s,i,i+1)
        if len(tempstr) > len(substr):
            substr = tempstr
    return substr
                

# s='cbadab'
s='abbdabadbad'
print(longest_palindrome_substring(s))
