'''
Given an array arr of N integers. Find the contiguous sub-array with maximum sum.
'''

l=[1,2,-2,3,1,-3,-1,-1,-5,4]

ll=[]
max=0
for i in range(len(l)):
    for j in range(i+1,len(l)):
        ss=l[i:j+1]
        if sum(ss) > max:
            max = sum(ss)
            ll = ss.copy()
print(max)
print (ll)