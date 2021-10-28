'''
You are given an integer, N. Your task is to print an alphabet rangoli of size N. 
(Rangoli is a form of Indian folk art based on creation of patterns.)

Different sizes of alphabet rangoli are shown below:

#size 3

----c----
--c-b-c--
c-b-a-b-c
--c-b-c--
----c----

#size 5

--------e--------
------e-d-e------
----e-d-c-d-e----
--e-d-c-b-c-d-e--
e-d-c-b-a-b-c-d-e
--e-d-c-b-c-d-e--
----e-d-c-d-e----
------e-d-e------
--------e--------
Hints
First print the half of the Rangoli in the given way and save each line in a list. 
Then print the list in reverse order to get the rest.
'''
import string
size = int(input('Size > '))
alphabets = string.ascii_lowercase
str = alphabets[0:size]
# print (str)
r_str=str[::-1]
# print(r_str)
lines=[r_str[0]]
new_str=[]
i=0
j=0
while i<(len(r_str)-1):
    # print (i,j)
    to_add=r_str[i:i+2]
    ll=lines[i]
    ll = ll[0:j]+to_add+ll[j:]
    lines.append(ll)
    # print(ll)
    i+=1
    j+=1
all_lines=[]
# print(lines)
for i in lines:
    lll=list(i)
    all_lines.append('-'.join(lll))
for i in reversed(lines[0:len(lines)-1]):
    lll=list(i)
    all_lines.append('-'.join(lll))
# print(all_lines)
length = (4*size) - 3
for i,v in enumerate(all_lines):
    all_lines[i] = v.center(length,'-')
for i in all_lines:
    print(i)






