'''
You are required to write a program to sort the (name, age, score) tuples by ascending order where 
name is string, age and score are numbers. The tuples are input by console. 
The sort criteria is:

1: Sort based on name
2: Then sort based on age
3: Then sort by score
The priority is that name > age > score.

If the following tuples are given as input to the program:

Tom,19,80
John,20,90
Jony,17,91
Jony,17,93
Json,21,85
Then, the output of the program should be:

[('John', '20', '90'), ('Jony', '17', '91'), ('Jony', '17', '93'), ('Json', '21', '85'), ('Tom', '19', '80')]
'''
# input_dict={
#     'Tom': [[19,[80]]],
#     'John':[[21, [90]],[19,[93]]],
#     'Jony':[[17, [93,91]], [21, [90]]],
#     'Json':[[21,[85, 81]]]
# }

# input_nestdict= {
#         'Tom': {
#                 '19': [80]
#         },
#         'John': {
#                 '21': [90],
#                 '19': [93]
#         },
#         'Jony': {
#                 '17': [93,91],
#                 '21': [90]
#         },
#         'Json': {
#                 '21': [85,81]
#         }
# }

# def sort_name(t):
#     return t[0][0]

# def sort_age(t):
#     return t[0]

# def sort_score(t):
#     return t

# final_list=[]
# name_list = [i for i in input_dict.keys()]
# name_list.sort()

# for i in name_list:
  
#         # print ("For Name:", i)
#         ll=sorted(input_dict[i],key=sort_age)
#         for j in ll:
                
#                 # print("Age is: ",j[0])
#                 sll = sorted(j[1], key=sort_score)
#                 # print(sll)
#                 for l in sll:
#                         tlist = []
#                         # print (l)
#                         tlist.append(i)
#                         tlist.append(j[0])
#                         tlist.append(l)
#                         # print (tlist)
#                         final_list.append(tuple(tlist))
# print (final_list)

input_nestdict = {}
while True:
    s=input("Enter a 3-tuple...: ")
    if s == '':
        break
    l=s.split(',')

    if l[0] not in input_nestdict:
            input_nestdict[l[0]]={}

    if l[1] in input_nestdict[l[0]]:
            input_nestdict[l[0]][l[1]].append(l[2])
    else:
            input_nestdict[l[0]][l[1]] = [l[2]]

# print (input_nestdict)
final_list=[]
name_list=[i for i in input_nestdict.keys()]
name_list.sort()

# print (f"Name list is : {name_list}")
for i in name_list:
        a_list = [x for x in input_nestdict[i].keys()]
        a_list.sort()
        # print (f'Age list for name {i} is : {a_list}')
        for j in a_list:
                s_list = input_nestdict[i][j]
                s_list.sort()
                # print (f"Score list is {s_list}")
                for l in s_list:
                        tlist=[]
                        tlist.append(i)
                        tlist.append(j)
                        tlist.append(l)
                        final_list.append(tuple(tlist))
print (f'Final output is : {final_list}')





