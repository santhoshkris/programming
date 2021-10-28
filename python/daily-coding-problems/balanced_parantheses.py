'''
Check if the given set of parantheses are balanced.
'''

def is_balanced(s):
    l=[]
    m = {'{' : '}', '[' : ']', '(' : ')'}
    for c in s:
        if c in m.keys():
            l.append(c)
        elif c in m.values():
            e = l.pop()
            if c != m[e]:
                return False
            else:
                pass
    return True

s1="([(]))"
s2="[](){([[[]]])}"
s="()(){]}"
print(f"Parantheses are : {s}")
if (is_balanced(s)):
    print("They are balanced...")
else:
    print("They are not balanced....")
