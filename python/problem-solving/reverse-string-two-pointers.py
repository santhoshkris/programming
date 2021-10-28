def reverse_string(str1):
    # fill this in
    pointer1 = 0
    pointer2 = len(str1) - 1
    strList = list(str1)
    while pointer1 < pointer2:
      temp = strList[pointer1]
      strList[pointer1] = strList[pointer2]
      strList[pointer2] = temp
      pointer1 += 1
      pointer2 -= 1
    return ''.join(strList)

s='hello world'
print(reverse_string(s))