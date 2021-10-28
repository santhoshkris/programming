'''
Find the longest substring with k unique characters in a given string
"aabbcc", k = 2
Max substring can be any one from {"aabb" , "bbcc"}
'''
def countDistinctChars(str):
    m={}
    for i in str:
        if i in m:
            m[i]+=1
        else:
            m[i]=1
    return len(m.keys())

def longest_substring(s,k):
    left=0
    right=0
    count_dist_chars=0
    gmax = 0
    substr=""
    while right <= len(s):
        count_dist_chars = countDistinctChars(s[left:right])
        print("Currently looking at ", s[left:right])
        print(count_dist_chars)
        while count_dist_chars == k+1:
            print("Crossed the limit of distinct chars ", s[left:right])
            if len(s[left:right-1]) > gmax:
                gmax = len(s[left+1:right])
                substr = s[left:right-1]
            left+=1
            count_dist_chars = countDistinctChars(s[left:right])
        right+=1
    return gmax,substr

# len,str = longest_substring("abdcabaad",2)
len,str = longest_substring("aabbcc",2)
print(str,len)
