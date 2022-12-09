#!/usr/bin/env python
"""Advent of Code - Day-8."""
tree_grid = []

with open("grid-of-trees.txt") as f:
# with open("sample_grid.txt") as f:
    for aline in f:
        line = aline.rstrip('\n')
        row = []
        for i in line:
            row.append(int(i))
        tree_grid.append(row)

print("The Grid...")
for row in range(len(tree_grid)):
    print(tree_grid[row])

# Trees on the edges
cur_tree_count = (len(tree_grid[0]) * 4) - 4
print(f"# of tree visible along the edges are: {cur_tree_count}")
row_count = len(tree_grid)
col_count = len(tree_grid[0])
print(row_count)
print(col_count)


# def check_if_visible(x, y):
#     visible_top = False
#     visible_below = False
#     score_top = 0
#     score_below = 0
#     score_left = 0
#     score_right = 0
#
#     # check for top
#     for m in range(x):
#         if tree_grid[x][y] > tree_grid[m][y]:
#             visible_top = True
#             score_top += 1
#         else:
#             visible_top = False
#             break
#
#     # check for below
#     for m in range(row_count):
#         if m <= x:
#             pass
#         else:
#             if tree_grid[x][y] > tree_grid[m][y]:
#                 visible_below = True
#                 score_below += 1
#             else:
#                 visible_below = False
#                 break
#
#     visible_left = False
#     visible_right = False
#
#     # check to the left
#     for n in range(c):
#         if tree_grid[x][y] > tree_grid[x][n]:
#             visible_left = True
#             score_left += 1
#         else:
#             visible_left = False
#             break
#
#     # check to the right
#     for n in range(col_count):
#         if n <= y:
#             pass
#         else:
#             if tree_grid[x][y] > tree_grid[x][n]:
#                 visible_right = True
#                 score_right += 1
#             else:
#                 visible_right = False
#                 break
#
#     return visible_left or visible_right or visible_top or visible_below

scenic_scores = []
def calc_scenic_score(x, y):
    score_top = 0
    score_below = 0
    score_left = 0
    score_right = 0

    # check for top
    for m in reversed(range(x)):
        if tree_grid[x][y] > tree_grid[m][y]:
            score_top += 1
        else:
            score_top += 1
            break

    # check for below
    for m in range(row_count):
        if m <= x:
            pass
        else:
            if tree_grid[x][y] > tree_grid[m][y]:
                score_below += 1
            else:
                score_below += 1
                break

    # check to the left
    for n in reversed(range(c)):
        if tree_grid[x][y] > tree_grid[x][n]:
            score_left += 1
        else:
            score_left += 1
            break

    # check to the right
    for n in range(col_count):
        if n <= y:
            pass
        else:
            if tree_grid[x][y] > tree_grid[x][n]:
                score_right += 1
            else:
                score_right += 1
                break
    print(score_top, score_below, score_left, score_right)
    return score_top * score_below * score_right * score_left


r = 1
while r < row_count - 1:
    c = 1
    while c < col_count - 1:
        print(f"checking for tree {tree_grid[r][c]} at {r} , {c}")
        # result = check_if_visible(r, c)
        result = calc_scenic_score(r, c)
        print(f"scenic score for the tree is: {result}")
        scenic_scores.append(result)
        c += 1
    r += 1

print(scenic_scores)
print(max(scenic_scores))