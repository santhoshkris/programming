import re
s=input("Enter a sentence: ")
c_upper = len(re.findall(r'[A-Z]', s))
c_lower = len(re.findall(r'[a-z]', s))

print (f"UPPER CASE: {c_upper}\nLOWER CASE: {c_lower}")