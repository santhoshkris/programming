#!/usr/bin/env python3

nums = [3,2,5,7,4]
sum = 9
res = {}
for i,v in enumerate(nums):
    if v in res.keys():
       print("found a pair at indices: ", i, res[v])
       exit()
    else:
        res[sum-v] = i
print("did not find a pair")
