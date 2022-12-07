#!/usr/bin/env python

temp_stack = []
stack = {
	1: ["F", "H", "B", "V", "R", "Q", "D", "P"],
	2: ["L", "D", "Z", "Q", "W", "V"],
	3: ["H", "L", "Z", "Q", "G", "R", "P", "C"],
	4: ["R", "D", "H", "F", "J", "V", "B"],
	5: ["Z", "W", "L", "C"],
	6: ["J", "R", "P", "N", "T", "G", "V", "M"],
	7: ["J", "R", "L", "V", "M", "B", "S"],
	8: ["D", "P", "J"],
	9: ["D", "C", "N", "W", "V"]
}

# - Part I
# with open("stack_changes.txt", "r") as f:
# 	for aline in f:
# 		line = aline.rstrip('\n').split(' ')
# 		print(line)
# 		count = line[1]
# 		from_stack = line[3]
# 		to_stack = line[5]
# 		for i in range(int(count)):
# 			print(i)
# 			stack[int(to_stack)].append(stack[int(from_stack)].pop())
#
# 	line = f.readline().rstrip('\n').split(' ')
# 	print(line)
# 	count = line[1]
# 	from_stack = line[3]
# 	to_stack = line[5]
# 	print(f"count: {count}, from_stack: {from_stack}, to_stack: {to_stack} ")
# 	for i in range(int(count)):
# 		print(i)
# 		stack[int(to_stack)].append(stack[int(from_stack)].pop())
#
# print(stack)

# - Part II


def process_stacks():
	global temp_stack
	with open("stack_changes.txt", "r") as f:
		for aline in f:
			line = aline.rstrip('\n').split(' ')
			print(line)
			count = line[1]
			from_stack = line[3]
			to_stack = line[5]
			temp_stack = []
			print(f"count: {count}, from_stack: {from_stack}, to_stack: {to_stack} ")
			for i in range(int(count)):
				print(i)
				temp_stack.append(stack[int(from_stack)].pop())
				print(temp_stack)
			temp_stack.reverse()
			print(temp_stack)
			for i in temp_stack:
				stack[int(to_stack)].append(i)

	# 	print(line)
		# 	count = line[1]
		# 	from_stack = line[3]
		# 	to_stack = line[5]
		# 	for i in range(int(count)):
		# 		print(i)
		# 		stack[int(to_stack)].append(stack[int(from_stack)].pop())
		# line = f.readline().rstrip('\n').split(' ')
		# print(line)
		# count = line[1]
		# from_stack = line[3]
		# to_stack = line[5]
		# print(f"count: {count}, from_stack: {from_stack}, to_stack: {to_stack} ")
		# for i in range(int(count)):
		# 	print(i)
		# 	temp_stack.append(stack[int(from_stack)].pop())
		# 	print(temp_stack)
		# temp_stack.reverse()
		# print(temp_stack)
		# for i in temp_stack:
		# 	stack[int(to_stack)].append(i)

print(stack)
process_stacks()
print(stack)
