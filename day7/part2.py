from functools import lru_cache

file = open("day7/input.txt", "r").readlines()

diagram = []
for line in file:
    diagram.append(line.strip())

# Follow the beam, recursively splitting at each splitter
@lru_cache
def timelinesAtPoint(row, col):
    for decrementingRow in range(row, len(diagram)):
        if diagram[decrementingRow][col] == "^":
            return timelinesAtPoint(decrementingRow, col-1) + timelinesAtPoint(decrementingRow, col+1)
    return 1

for col in range(len(diagram[0])):
    if diagram[0][col] == "S":
        print(timelinesAtPoint(0, col))