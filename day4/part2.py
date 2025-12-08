file = open("day4/input.txt", "r").readlines()

# Put input into a 2D array
grid = []

for line in file:
    line = line.strip()
    
    row = []
    for char in line:
        row.append(char)

    grid.append(row)

def passthroughAndRemove(grid): 
    # For each roll, check if they are accessible. If so, remove them.
    current_pass_removed = 0
    i = 0
    for row in grid:
        j = 0
        for char in row:
            if char == "@":
                # Check for a roll in each direction
                num_adjacent_rolls = 0

                # North
                if i - 1 >= 0 and grid[i - 1][j] == "@":
                    num_adjacent_rolls += 1

                # North East
                if i - 1 >= 0 and j + 1 < len(row) and grid[i - 1][j + 1] == "@":
                    num_adjacent_rolls += 1

                # East
                if j + 1 < len(row) and grid[i][j + 1] == "@":
                    num_adjacent_rolls += 1

                # South East
                if i + 1 < len(grid) and j + 1 < len(row) and grid[i + 1][j + 1] == "@":
                    num_adjacent_rolls += 1

                # South
                if i + 1 < len(grid) and grid[i + 1][j] == "@":
                    num_adjacent_rolls += 1

                # South West
                if i + 1 < len(grid) and j - 1 >= 0 and grid[i + 1][j - 1] == "@":
                    num_adjacent_rolls += 1

                # West
                if j - 1 >= 0 and grid[i][j - 1] == "@":
                    num_adjacent_rolls += 1

                # North West
                if i - 1 >= 0 and j - 1 >= 0 and grid[i - 1][j - 1] == "@":
                    num_adjacent_rolls += 1

                if num_adjacent_rolls < 4:
                    current_pass_removed += 1
                    grid[i][j] = "."
            j += 1
        i += 1

    return grid, current_pass_removed

total_num_removed = 0
current_pass_removed = None

while current_pass_removed != 0:
    grid, current_pass_removed = passthroughAndRemove(grid)
    total_num_removed += current_pass_removed

print(total_num_removed)

