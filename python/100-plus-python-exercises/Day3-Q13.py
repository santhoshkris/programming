# import re
# s = input("Enter a sentence: ")
# p_letters=r'([a-zA-Z])'
# p_digits=r'(\d)'

# res=re.findall(p_letters,s)
# res1=re.findall(p_digits,s)
# print(f"Letters: {len(res)}")
# print(f"Numbers: {len(res1)}")
#using reduce for to count
#Another interesting solution using reduce
from functools import reduce

def count_letters_digits(counters,char_to_check):
    counters[0] += char_to_check.isalpha()
    counters[1] += char_to_check.isnumeric()
    return counters
print('LETTERS {0}\nDIGITS {1}'.format(*reduce(count_letters_digits,input("Enter a sentence: "),[0,0])))