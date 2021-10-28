# out_list=[]
# for i in range(1000,3001):
#     flag=False
#     for c in str(i):
#         if int(c)%2!=0:
#             flag=False
#             break
#         else:
#             flag=True
#     if flag:
#         out_list.append(i)

# print(out_list)

def check_even_digits(n):
    for c in str(n):
        if int(c)%2!=0:
            return False
        else:
            pass
    return True

print(list(filter(check_even_digits,[x for x in range(1000,3001)])))

#Another interesting solution...
# from functools import reduce 
# #using reduce to check if the number has only even digits or not
# def is_even_and(bool_to_compare,num_as_char):
#     return int(num_as_char)%2==0 and bool_to_compare

# print(*(i for i in range(1000,3001) if reduce(is_even_and,str(i),True)),sep=',')