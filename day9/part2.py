import math
from scipy.sparse import dok_array

file = open("day9/input.txt", "r").readlines()

red_tiles = []
for line in file:
    line = line.strip().split(",")
    line[0], line[1] = int(line[1]), int(line[0])
    red_tiles.append(line)

max_row = max(red_tiles, key=lambda tile: tile[0])[0] + 1
max_col = max(red_tiles, key=lambda tile: tile[1])[1] + 1

min_row = min(red_tiles, key=lambda tile: tile[0])[0]
min_col = min(red_tiles, key=lambda tile: tile[1])[1]

# Create sparse 2d array that is the size of the graph to represent the border tiles, initialize with all False
border_tile_matrix = dok_array((max_row, max_col), dtype=bool)

# Add corner (red) tiles to border tile matric
for tile in red_tiles:
    border_tile_matrix[tile[0], tile[1]] = True

# Add first tile to the end so that the list wraps around
red_tiles.append(red_tiles[0])

# Add border tiles
for tile in range(len(red_tiles) - 1):
    # If the next tile is left or right
    if red_tiles[tile][0] == red_tiles[tile+1][0]:
        # If going left
        if red_tiles[tile][1] > red_tiles[tile+1][1]:
            for col in range(red_tiles[tile][1], red_tiles[tile+1][1], -1):
                border_tile_matrix[red_tiles[tile][0], col] = True
        # If going right
        if red_tiles[tile][1] < red_tiles[tile+1][1]:
            for col in range(red_tiles[tile][1], red_tiles[tile+1][1]):
                border_tile_matrix[red_tiles[tile][0], col] = True

    # If the next tile is up or down, put X's in between
    if red_tiles[tile][1] == red_tiles[tile+1][1]:
        # If going up
        if red_tiles[tile][0] > red_tiles[tile+1][0]:
            for row in range(red_tiles[tile][0], red_tiles[tile+1][0], -1):
                border_tile_matrix[row, red_tiles[tile][1]] = True
        # If going right
        if red_tiles[tile][0] < red_tiles[tile+1][0]:
            for row in range(red_tiles[tile][0], red_tiles[tile+1][0]):
                border_tile_matrix[row, red_tiles[tile][1]] = True

# Create sparse 2d array that is the size of the graph to represent the border tiles, initialize with all False
inside_tile_matrix = dok_array((max_row, max_col), dtype=bool)

# Definitively determine if a tile is inside the border by counting border tiles in all directions
def determine_tile_inside(row, col):
    # If on the border, tile is not inside
    if border_tile_matrix[row, col]:
        return False

    # Count border tiles to the left
    count_left = 0
    for i in range(0, col):
        if border_tile_matrix[row, i]:
            count_left += 1

    # Count border tiles to the right
    count_right = 0
    for i in range(col + 1, max_col):
        if border_tile_matrix[row, i]:
            count_right += 1

    # Count border tiles up
    count_up = 0
    for i in range(0, row):
        if border_tile_matrix[i, col]:
            count_up += 1

    # Count border tiles down
    count_down = 0
    for i in range(row + 1, max_row):
        if border_tile_matrix[i, col]:
            count_down += 1

    # Axiom: if there is an odd number of border crossings in all directions, a tile is in the boundary
    if count_left % 2 == 1 and count_right % 2 == 1 and count_up % 2 == 1 and count_down % 2 == 1:
        return True

# Fill the inside of the matrix by recursively checking around inside tiles after initializing one
def fill_tile_inside():
    inside_stack = []
    directions = [(1, 0), (1, -1), (1, 1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]
    for direction in directions:
        # When the inital inside tile is found
        if determine_tile_inside(red_tiles[0][0] + direction[0], red_tiles[0][1] + direction[1]):
            # Add to the sparse matrix
            inside_tile_matrix[red_tiles[0][0] + direction[0], red_tiles[0][1] + direction[1]] = True
            # Add to the stack
            inside_stack.append([red_tiles[0][0] + direction[0], red_tiles[0][1] + direction[1]])
            break

    while inside_stack != []:
        tile = inside_stack.pop()
        for direction in directions:
            if not inside_tile_matrix[tile[0] + direction[0], tile[1] + direction[1]] and not border_tile_matrix[tile[0] + direction[0], tile[1] + direction[1]]:
                # Add to the stack
                inside_stack.append([tile[0] + direction[0], tile[1] + direction[1]])
                # Add to the sparse matrix
                inside_tile_matrix[tile[0] + direction[0], tile[1] + direction[1]] = True

# fill_tile_inside()

def check_valid_rug(tile1, tile2):
    # If any of the tiles in the rug are outside the boundary, the rug will be invalid
    # Find the rug's borders
    if tile1[0] == tile2[0]:
        starti, endi = tile1[0], tile1[0] + 1
    elif tile1[0] < tile2[0]:
        starti, endi = tile1[0] + 1, tile2[0]
    else:
        starti, endi = tile2[0] + 1, tile1[0]

    if tile1[1] == tile2[1]:
        startj, endj = tile1[1], tile1[1] + 1
    elif tile1[1] < tile2[1]:
        startj, endj = tile1[1] + 1, tile2[1]
    else:
        startj, endj = tile2[1] + 1, tile1[1]

    # Include step to speed up
    stepi = math.ceil((endi - starti) / 50)
    stepj = math.ceil((endj - startj) / 50)

    # Look through each of the rug's tiles
    for i in range(starti, endi, stepi):
        for j in range(startj, endj, stepj):
            # if not determine_tile_inside(i, j):
            #     return False
            # if not border_tile_matrix[i, j] and not inside_tile_matrix[i, j]:
            #    return False
            if border_tile_matrix[i, j]:
                return False

    # Check opposite corners
    if not border_tile_matrix[tile1[0], tile2[1]] and not border_tile_matrix[tile2[0], tile1[1]]:
        return False

    return True

max_area = 0
max_pair = []
num_counted = 0
for tile1 in red_tiles:
    print(num_counted)
    for tile2 in red_tiles:
        area = (abs(tile1[0] - tile2[0]) + 1) * (abs(tile1[1] - tile2[1]) + 1)
        if area > max_area and check_valid_rug(tile1, tile2):
            max_area = area
    num_counted += 1

print(max_area)