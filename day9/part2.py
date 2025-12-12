import functools
from scipy.sparse import dok_array
import multiprocessing as mp

file = open("day9/input.txt", "r").readlines()

expanded_red_tiles = []
for line in file:
    line = line.strip().split(",")
    # Reverse the rows and cols to be consistent with question
    expanded_red_tiles.append([int(line[1]), int(line[0])])

# Compress the coordinates
expanded_rows = [tile[0] for tile in expanded_red_tiles]
expanded_rows = sorted(list(set(expanded_rows)))
row_dict = {row: i for i, row in enumerate(expanded_rows)}

expanded_cols = [tile[1] for tile in expanded_red_tiles]
expanded_cols = sorted(list(set(expanded_cols)))
col_dict = {col: j for j, col in enumerate(expanded_cols)}

red_tiles = [[row_dict[tile[0]], col_dict[tile[1]]] for tile in expanded_red_tiles]

# Find the min/max coordinates
max_row = max(red_tiles, key=lambda tile: tile[0])[0] + 1
max_col = max(red_tiles, key=lambda tile: tile[1])[1] + 1

min_row = min(red_tiles, key=lambda tile: tile[0])[0]
min_col = min(red_tiles, key=lambda tile: tile[1])[1]

# Create sparse 2d array that is the size of the graph to represent the border tiles, initialize with all False
border_tile_matrix = dok_array((max_row, max_col), dtype=bool)

# Add corner (red) tiles to border tile matrix
for tile in red_tiles:
    border_tile_matrix[tile[0], tile[1]] = True

# Add first tile to the end so that the list wraps around
red_tiles.append(red_tiles[0])

# Print tiles before adding borders
'''
print("   ", end="")

for j in range(max_col):
    print(str(j % 100).zfill(2), end="")

print()

for i in range(max_row):
    print(str(i).zfill(3), end="")
    for j in range(max_col):
        if border_tile_matrix[i, j] == True:
            print("# ", end="")
        else:
            print(". ", end="")
    print()
'''

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

print("Border tiles added")
# Print tiles after adding borders
'''
print("   ", end="")

for j in range(max_col):
    print(str(j % 100).zfill(2), end="")

print()

for i in range(max_row):
    print(str(i).zfill(3), end="")
    for j in range(max_col):
        if border_tile_matrix[i, j] == True:
            print("# ", end="")
        else:
            print(". ", end="")
    print()
'''

# Determines if a tile is inside or on the border
@functools.cache
def determine_valid_tile(row, col):
    # If on the border, tile is valid
    if border_tile_matrix[row, col]:
        return True

    # If a tile has a boundary tile above, below, left, and right, it is valid (this method has edge cases, but those do not appear in the input)

    # Get all tiles in the tile's row (vertical intersection cols) and col (horizontal intersection rows)
    horizontal_intersection_cols = []
    for key in border_tile_matrix[[row]].keys():
        horizontal_intersection_cols.append(key[1])

    vertical_intersection_rows = []
    for key in border_tile_matrix[:, [col]].keys():
        vertical_intersection_rows.append(key[0])

    min_boundary_row = min(vertical_intersection_rows)
    max_boundary_row = max(vertical_intersection_rows)

    min_boundary_col = min(horizontal_intersection_cols)
    max_boundary_col = max(horizontal_intersection_cols)

    if row >= min_boundary_row and row <= max_boundary_row and col >= min_boundary_col and col <= max_boundary_col:
        return True
    
    return False

 # Checks a rug for validity; if any of the tiles of the rug's boundary are not a red or greed (valid) tile, the rug will be invalid
def check_valid_rug(corners):
    # Find the rug's boundary indices
    if corners[0][0] == corners[1][0]:
        start_row, end_row = corners[0][0], corners[0][0]
    elif corners[0][0] < corners[1][0]:
        start_row, end_row = corners[0][0], corners[1][0]
    else:
        start_row, end_row = corners[1][0], corners[0][0]

    if corners[0][1] == corners[1][1]:
        start_col, end_col = corners[0][1], corners[0][1]
    elif corners[0][1] < corners[1][1]:
        start_col, end_col = corners[0][1], corners[1][1]
    else:
        start_col, end_col = corners[1][1], corners[0][1]
    
    # Iterate through all tiles
    for i in range(start_row, end_row + 1):
        for j in range(start_col, end_col + 1):
            if not determine_valid_tile(i, j):
                return False
        
    return True

# Returns the area of a rug
def rug_area(tile1, tile2):
    return (abs(tile1[0] - tile2[0]) + 1) * (abs(tile1[1] - tile2[1]) + 1)

# Undoes the coordinate compression to get the original coordinates for a tile
def expand_tile_coordinates(tile):
    return_row = -1
    return_col = -1
    
    for expanded_row, row in row_dict.items():
        if row == tile[0]:
            return_row = expanded_row

    for expanded_col, col in col_dict.items():
        if col == tile[1]:
            return_col = expanded_col
    
    # print(return_row, return_col)
    return [return_row, return_col]

# In order to do multiprocessing, we first have to find a list of max_area candidates, then run to determine if valid
def get_areas():
    areas=[]
    num_counted = 0
    for i in range(len(red_tiles)):
        # print("OUTER LOOP:", num_counted)
        #num_inner = 0
        for j in range(i, len(red_tiles)):
            #print(num_inner)
            areas.append([rug_area(expand_tile_coordinates(red_tiles[i]), expand_tile_coordinates(red_tiles[j])), i, j])
            #num_inner += 1
        num_counted += 1
    
    areas.sort(reverse=True)
    return(areas)

# Find areas of all potential rugs (have to do this first in order to multiprocess over all of them later)
print("Getting areas")
areas = get_areas()
print("Areas returned")

# Search through set of areas until first valid area is found
max_area_found = False
search_start = 0
search_end = 20
while not max_area_found:
    print("Searching areas from", search_start, "to", search_end)
    search_areas = areas[search_start:search_end]

    # Put the pairs to validate into a list that is comprehensible for multithreading
    potential_max_pairs = []
    for area in search_areas:
        potential_max_pairs.append(tuple([red_tiles[area[1]], red_tiles[area[2]]]))

    # Multithread the check_valid_rug function
    with mp.Pool() as pool:
        valid_areas = (pool.map(check_valid_rug, potential_max_pairs))

    # Take the first valid rug in the sorted list of areas
    for i in range(len(valid_areas)):
        if valid_areas[i] == True:
            max_area_found = True
            max_tile1_index = search_areas[i][1]
            max_tile2_index = search_areas[i][2]
            print(expand_tile_coordinates(red_tiles[max_tile1_index]), expand_tile_coordinates(red_tiles[max_tile2_index]))
            break
    
    # If no rug is valid, expand the search area
    search_start = search_end
    search_end *= 2

print(rug_area(expand_tile_coordinates(red_tiles[max_tile1_index]), expand_tile_coordinates(red_tiles[max_tile2_index])))