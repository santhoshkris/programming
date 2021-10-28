""" Caesar Cipher
    A Caesar cipher is a simple substitution cipher in which each letter of the
    plain text is substituted with a letter found by moving n places down the
    alphabet. For example, assume the input plain text is the following:

        abcd xyz

    If the shift value, n, is 4, then the encrypted text would be the following:

        efgh bcd

    You are to write a function that accepts two arguments, a plain-text
    message and a number of letters to shift in the cipher. The function will
    return an encrypted string with all letters transformed and all
    punctuation and whitespace remaining unchanged.

    Note: You can assume the plain text is all lowercase ASCII except for
    whitespace and punctuation.
"""
# caesar.py
# import string

# def shift_n(letter, table):
#     try:
#         index = string.ascii_lowercase.index(letter)
#         return table[index]
#     except ValueError:
#         return letter

# def caesar(message, amount):
#     amount = amount % 26
#     table = string.ascii_lowercase[amount:] + string.ascii_lowercase[:amount]
#     enc_list = [shift_n(letter, table) for letter in message]
#     return "".join(enc_list)

# def caesar(plain_text, shift_num=1):
#     letters = string.ascii_lowercase
#     mask = letters[shift_num:] + letters[:shift_num]
#     trantab = str.maketrans(letters, mask)
#     return plain_text.translate(trantab)


import string
def caesar_cipher(msg, n):
    letters = string.ascii_lowercase
    c_msg=""
    for i in msg:
        if i not in letters:
            c_msg+=i
        else:
            idx = letters.index(i)
            # print('Index in letter is: ', idx)
            if idx+n > len(letters):
                n1 = (idx+n)-26
            else:
                n1=idx+n
            # print("Updated index is : ", n1)
            c_msg+=letters[n1]
    return c_msg

s = input("Enter a sentence/msg followed by a number to cipher with: ").split(',')
print(caesar_cipher(s[0],int(s[1])))
