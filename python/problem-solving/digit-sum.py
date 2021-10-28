# num = input("Enter a number : ")

# while len(num) != 1:
#     n=0
#     for i in num:
#         n+=int(i)
#     num=str(n)
# print(num)

def sumDigits(num,p):
    if p==0:
        return 0
    return (num%(10**p))//(10**(p-1)) + sumDigits(num,p-1)

print(sumDigits(4321,4))
print(sumDigits(5413,4))
print(sumDigits(54134,5))
