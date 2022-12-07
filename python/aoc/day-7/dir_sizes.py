#!/usr/bin/env python

dir_and_sizes = {'/': 0}
dir_tree = []

with open("dir_structure.txt", "r") as f:
# with open("dir_details.txt", "r") as f:
    for aline in f:
        line = aline.rstrip('\n')
        # print(line)
        if line.startswith('$'):
            command = line[2:]
            print(f"Command: {command}")
            if command == 'ls':
                print('ls command called...')
            elif command == 'cd ..':
                print("cd .. called")
                dir_tree.pop()
                print(f"current dir stack : {dir_tree}")
            else:
                print("cd called")
                dir_name = command.split(' ')[1]
                dir_tree.append(dir_name)
                dir_and_sizes["->".join(dir_tree)] = 0
                print(f"current dir stack : {dir_tree}")
        elif line[:1].isdigit():
            file_name = line.split(' ')[1]
            file_size = line.split(' ')[0]
            print(f"file: {file_name} size: {file_size}")
            for i in range(len(dir_tree)):
                dir_and_sizes["->".join(dir_tree[0:i+1])] += int(file_size)
        elif line.startswith('dir'):
            dir_name = line.split(' ')[1]
            print(f"dir name {dir_name}")
# print(dir_and_sizes)
# print(len(dir_and_sizes.keys()))
total_size = 0
to_delete_dirs = []
for i in dir_and_sizes:
    # print(f"dir: {i}, size: {dir_and_sizes[i]}")
    # if dir_and_sizes[i] <= 100000:
    #     total_size += dir_and_sizes[i]
    if dir_and_sizes[i] >= 1035571:
        to_delete_dirs.append(dir_and_sizes[i])
        print(dir_and_sizes[i])
to_delete_dirs.sort()
print(to_delete_dirs)
# print(total_size)
