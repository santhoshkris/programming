from functools import reduce

s=input("Enter a number: ")
l=[s*n for n in range(1,5)]
total = reduce(lambda acc,i:int(acc)+int(i), l)
print('Total: {}'.format(total))