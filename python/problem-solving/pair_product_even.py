'''
Write a Python function to find a distinct pair of numbers whose product is odd from a sequence of integer values.
'''

l=[3,2,1,5,4,6,8]
pairs = []
i=0
while i < len(l):
    j=i+1
    while j < len(l):
        if (l[i]*l[j])%2 != 0:
            pairs.append(tuple([l[i],l[j]]))
        else:
            pass
        j+=1
    i+=1
print (pairs)