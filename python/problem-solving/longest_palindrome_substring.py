s='cbbd'
#s='babad'

def isPalin(s):
    if len(s) == 1 or len(s) == 0:
        return False
    return s==s[::-1]

left=0
right=0
gmax = 0
palin=False
longPalin = ""
while right<=len(s):
    print("Expanding window....")
    substr=s[left:right+1]
    print(substr)
    palin = isPalin(substr)
    print(palin)
    while palin:
        print('Contracting the window...')
        if (right-left) > gmax:
            gmax = right-left
            longPalin = s[left:right]
        print(gmax)
        print(longPalin)
        substr1 = s[left:right+1]
        print(substr1)
        palin=isPalin(substr1)
        print(palin)
        left+=1
    right+=1

print(gmax)
print(longPalin)

