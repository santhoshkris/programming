# s='santhoshKrishna'
s='hello world'

# def reverse(s,n):
#     if n == 1: 
#         return s[0]
#     return s[n-1] + reverse(s,n-1)

def reverse(s):
    if len(s) == 1:
        return s
    return s[len(s)-1] + reverse(s[:len(s)-1])

# print(reverse(s,len(s)))
print(reverse(s))
