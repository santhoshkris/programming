#!/usr/bin/env python

input_string = ""

# Part-I
# begin = 0
# end = 4
#
# with open("signal_chars.txt", mode="r") as f:
#     input_string = f.read()
#
# print(input_string)
#
# while end < len(input_string):
#     substr = input_string[begin:end]
#     if len(substr) == len(set(substr)):
#         break
#     begin += 1
#     end += 1
#
# print(end)

# Part-II
begin = 0
end = 14

with open("signal_chars.txt", mode="r") as f:
    input_string = f.read()

print(input_string)

while end < len(input_string):
    substr = input_string[begin:end]
    if len(substr) == len(set(substr)):
        break
    begin += 1
    end += 1

print(end)
