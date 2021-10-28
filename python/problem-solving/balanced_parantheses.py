s="([(]))"
s2="[](){([[[]]])}"
s3="()(){]}"
l=[]
m = {'{' : '}', '[' : ']', '(' : ')'}
def is_balanced(s):
    for c in s:
        if c in m.keys():
            print ("Pushing this onto stack : ",c)
            l.append(c)
            print(l)
        elif c in m.values():
            print('Got closing parans ',c)
            e = l.pop()
            print("What's there on the stack is : ", e)
            print("Expecting to see this :", m[e])
            if c != m[e]:
                print ("But, found this instead : ", c)
                return False
            else:
                print("Found a match : ", c)
    return True
print(is_balanced(s))
