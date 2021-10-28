# mylist = [1,2,2,3,3,3,2,2,5,6,6]
# out_list = []

# for i,v in enumerate(mylist):
# 	try:
# 		if mylist[i] != mylist[i+1]:
# 			out_list.append(v)
# 		else:
# 			pass
# 	except:
# 		out_list.append(mylist[i])
# 		break
# print (out_list)

# mylist1 = ['aba', 'xyz', 'aa', 'x', 'bbb']
# count=0
# for i in mylist1:
# 	if len(i) >=2 and i[0]==i[-1]:
# 		count+=1
# print (count)

# mylist2 = [(1, 3), (3, 2), (2, 1)]
# mylist2 = [(2, 3), (1, 2), (3, 1)]
mylist2 = [(1, 7), (1, 3), (3, 4, 5), (2, 2)]

def last_elem(num_tuple):
	return num_tuple[-1]

print (sorted(mylist2, key=last_elem))


