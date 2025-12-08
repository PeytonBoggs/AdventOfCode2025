from functools import lru_cache

file = open("day7/input.txt", "r").readlines()

diagram = []
for line in file:
    diagram.append(line.strip())

@lru_cache
def isSplit(splitter_row, splitter_col):
    # If there is 1. a splitter above and 2. one to the left or right of this splitter that has split and 3. none dirctly above after (2) happens, this splitter will split
    
    if diagram[splitter_row - 2][splitter_col] == "S":
        return True

    left = False
    right = False
    for row in range(splitter_row, 0, -1):
        # Look above and 1 to the left
        if diagram[row][splitter_col - 1] == "^":
            # Check directly above
            for row2 in range(splitter_row - 1, row, -1):
                if diagram[row2][splitter_col] == "^":
                    return False
                
            left = isSplit(row, splitter_col - 1)
        
        # Look above and 1 to the right
        if diagram[row][splitter_col + 1] == "^":
            # Check directly above
            for row2 in range(splitter_row - 1, row, -1):
                if diagram[row2][splitter_col] == "^":
                    return False
                
            right = isSplit(row, splitter_col + 1)

        if left or right:
            return True
        
    return False

num_split = 0
for row in range(len(diagram)):
    for col in range(len(diagram[0])):
        if diagram[row][col] == "^" and isSplit(row, col):
            # print("S", end='')
            num_split += 1
    #     elif diagram[row][col] == ".":
    #         print(".", end='')
    #     else:
    #         print("^", end='')
    # print()

print(num_split)