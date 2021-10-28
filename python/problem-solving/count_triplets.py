'''
Given an array of distinct integers. The task is to count all the triplets such that sum of two elements equals the third element.
 
Example 1:

Input:
N = 4
arr[] = {1, 5, 3, 2}
Output: 2
Explanation: There are 2 triplets: 
1 + 2 = 3 and 3 +2 = 5 
'''

l=[1,5,3,2,4,6]
c=0
for i in range(0,len(l)):
    for j in range(i+1,len(l)):
        if l[i]+l[j] in l:
            print("Found the sum...",l[i]+l[j])
            print("At index..",l.index((l[i]+l[j])))
            c+=1
        else:
            pass
print (c)

