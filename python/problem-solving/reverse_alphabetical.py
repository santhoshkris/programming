'''
You are given a string that contains alphabetical characters (a - z, A - Z) and some other characters ($, !, etc.). For example, one input may be:

'sea!$hells3'

Can you reverse only the alphabetical ones?

reverseOnlyAlphabetical('sea!$hells3');
// 'sll!$ehaes3'
'''
def reverse_string(str1):
    # fill this in
    pointer1 = 0
    pointer2 = len(str1) - 1
    strList = list(str1)
    while pointer1 < pointer2:
        if strList[pointer1].isalpha() and strList[pointer2].isalpha():
            temp = strList[pointer1]
            strList[pointer1] = strList[pointer2]
            strList[pointer2] = temp
            pointer1 += 1
            pointer2 -= 1
        else:
            if not strList[pointer1].isalpha():
                pointer1+=1
            elif not strList[pointer2].isalpha():
                pointer2-=1
            else:
                pass
    return ''.join(strList)

s='sea!$hells3'
print(reverse_string(s))