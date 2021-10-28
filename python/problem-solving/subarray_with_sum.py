'''
Given an unsorted array A of size N of non-negative integers, find a continuous sub-array which adds to a given number S
'''

l=[2,3,1,4,6,2,7,9,8]
s=8
lll=[]
for i in range(0,len(l)):
    tt=l[i]
    ll=[]
    ll.append(l[i])
    for j in range(i+1,len(l)):
        tt+=l[j]
        ll.append(l[j])
        if tt==s:
            print("Found....")
            lll.append(ll)
            break
        elif tt>s:
            break
        else:
            pass
print(lll)

