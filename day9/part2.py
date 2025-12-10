import math
from functools import lru_cache
from scipy.sparse import dok_array, coo_array

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

# Definitively determine if a tile is inside the border by counting border tiles in all directions
@lru_cache
def determine_tile_inside(row, col):
    # If on the border, tile is not inside
    if border_tile_matrix[row, col]:
        return False
    
    horizontal_intersection_cols = []
    for key in border_tile_matrix[[row]].keys():
        horizontal_intersection_cols.append(key[1])

    vertical_intersection_rows = []
    for key in border_tile_matrix[:, [col]].keys():
        vertical_intersection_rows.append(key[0])

    # Edge case: remove rows/cols that form a straight line
    j = 0
    while j < len(horizontal_intersection_cols) - 1:
        if horizontal_intersection_cols[j] == horizontal_intersection_cols[j+1] - 1:
            horizontal_intersection_cols.remove(horizontal_intersection_cols[j])
            j -= 1
        j += 1

    i = 0
    while i < len(vertical_intersection_rows) - 1:
        if vertical_intersection_rows[i] == vertical_intersection_rows[i+1] - 1:
            vertical_intersection_rows.remove(vertical_intersection_rows[i])
            i -= 1
        i += 1
    
    count_left = len(list(filter(lambda j: j < col, horizontal_intersection_cols)))
    count_right = len(horizontal_intersection_cols) - count_left

    count_up = len(list(filter(lambda i: i < row, vertical_intersection_rows)))
    count_down = len(vertical_intersection_rows) - count_up

    # Axiom: if there is an odd number of border crossings in all directions, a tile is in the boundary
    if count_left % 2 == 1 and count_right % 2 == 1 and count_up % 2 == 1 and count_down % 2 == 1:
        return True
    return False

def check_valid_rug(tile1, tile2):
    # If any of the tiles in the rug are outside the boundary, the rug will be invalid
    # Find the rug's borders
    if tile1[0] == tile2[0]:
        starti, endi = tile1[0], tile1[0] + 1
    elif tile1[0] < tile2[0]:
        starti, endi = tile1[0], tile2[0] + 1
    else:
        starti, endi = tile2[0], tile1[0] + 1

    if tile1[1] == tile2[1]:
        startj, endj = tile1[1], tile1[1] + 1
    elif tile1[1] < tile2[1]:
        startj, endj = tile1[1], tile2[1] + 1
    else:
        startj, endj = tile2[1], tile1[1] + 1

    # Include step to speed up
    stepi = math.ceil((endi - starti) / 2)
    stepj = math.ceil((endj - startj) / 2)

    # Look through each of the rug's tiles
    for i in range(starti, endi, stepi):
        for j in range(startj, endj, stepj):
            if not border_tile_matrix[i, j] and not determine_tile_inside(i, j):
                return False

    return True

max_area = 0
max_pair = []
num_counted = 0
num_inner_counted = 0
for tile1 in red_tiles:
    for tile2 in red_tiles:
        area = (abs(tile1[0] - tile2[0]) + 1) * (abs(tile1[1] - tile2[1]) + 1)
        if area > max_area and check_valid_rug(tile1, tile2):
            max_area = area
        print(num_inner_counted)
        num_inner_counted += 1
    print(num_counted)
    num_counted += 1

print(max_area)