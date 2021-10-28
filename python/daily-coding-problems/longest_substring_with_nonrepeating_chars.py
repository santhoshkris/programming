'''
Find the longest substring with non-repeating or all unique characters in a given string
'''


def longest_substring(s):
    m={}
    left=0
    right=0
    counter=0
    gmax=0
    substr=''
    while right < len(s):
        char = s[right]
        if not char in m:
            m[char]=1
        else:
            m[char]+=1        
            if m[char] > 1:
                counter+=1
        while counter == 1:
            if len(s[left:right]) > gmax:
                gmax = len(s[left:right])
                substr = s[left:right]
            char1 = s[left]
            if char1 in m:
                if m[char1]>1:
                    m[char1]-=1
                    counter-=1
                else:
                    m[char1]-=1
            left+=1
        right+=1
    return gmax,substr

# s='aabcbdede'
# s='GEEKSFORGEEKS'
len,str = longest_substring('aabcbdede')
print(len,str)
