import re

s='malayalam'
# s='abracadabra'
pat_list=[]
for c in s:
    i_list=[]
    pat = c
    if pat not in pat_list:
        # print ( f"checking with pat {c}")
        for m in re.finditer(pat, s):
            i_list.append(m.span())
        # print(i_list)
        i=0
        while i<len(i_list)-1:
            j=i+1
            while j<len(i_list):
                nstr = s[i_list[i][0]:i_list[j][1]]
                if nstr == nstr[::-1]:
                    print (f"Found a Palindrome : {nstr}")
                j+=1
            i+=1
        pat_list.append(pat)
