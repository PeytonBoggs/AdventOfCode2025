file = open("day9/input.txt", "r").readlines()

red_tiles = []
for line in file:
    line = line.strip().split(",")
    line[0], line[1] = int(line[1]), int(line[0])
    red_tiles.append(line)

# Add first tile to the end so that the list wraps around
red_tiles.append(red_tiles[0])

max_row = max(red_tiles, key=lambda tile: tile[0])[0]
max_col = max(red_tiles, key=lambda tile: tile[1])[1]

min_row = min(red_tiles, key=lambda tile: tile[0])[0]
min_col = min(red_tiles, key=lambda tile: tile[1])[1]

print("Max row:", max_row, "Min row:", min_row, "Max col:", max_col, "Min col:", min_col)

boundary_tiles = []

# Add boundary tiles
for tile in range(len(red_tiles) - 1):
    # If the next tile is left or right
    if red_tiles[tile][0] == red_tiles[tile+1][0]:
        # If going left
        if red_tiles[tile][1] > red_tiles[tile+1][1]:
            for col in range(red_tiles[tile][1], red_tiles[tile+1][1], -1):
                boundary_tiles.append([red_tiles[tile][0], col])
        # If going right
        if red_tiles[tile][1] < red_tiles[tile+1][1]:
            for col in range(red_tiles[tile][1], red_tiles[tile+1][1]):
                boundary_tiles.append([red_tiles[tile][0], col])

    # If the next tile is up or down, put X's in between
    if red_tiles[tile][1] == red_tiles[tile+1][1]:
        # If going up
        if red_tiles[tile][0] > red_tiles[tile+1][0]:
            for row in range(red_tiles[tile][0], red_tiles[tile+1][0], -1):
                boundary_tiles.append([row, red_tiles[tile][1]])
        # If going right
        if red_tiles[tile][0] < red_tiles[tile+1][0]:
            for row in range(red_tiles[tile][0], red_tiles[tile+1][0]):
                boundary_tiles.append([row, red_tiles[tile][1]])

print(len(boundary_tiles))

# Check if a tile is inside the boundary
def is_inside(tile):
    if tile in boundary_tiles:
        return True
    
    boundary_tiles_in_row = list(filter(lambda boundary_tile: boundary_tile[0] == tile[0], boundary_tiles))
    boundary_tiles_in_col = list(filter(lambda boundary_tile: boundary_tile[1] == tile[1], boundary_tiles))

    min_boundary_row = min(boundary_tiles_in_col, key=lambda tile: tile[0])[0]
    max_boundary_row = max(boundary_tiles_in_col, key=lambda tile: tile[0])[0]

    min_boundary_col = min(boundary_tiles_in_row, key=lambda tile: tile[1])[1]
    max_boundary_col = max(boundary_tiles_in_row, key=lambda tile: tile[1])[1]

    # Must have a boundary tile above, below, left, and right of the tile

    if tile[0] >= min_boundary_row and tile[0] <= max_boundary_row and tile[1] >= min_boundary_col and tile[1] <= max_boundary_col:
        return True

    return False

# Conditionally add the area between two tiles
areas = []
def add_area(tile1, tile2):
    area = ((abs(tile1[0] - tile2[0]) + 1) * (abs(tile1[1] - tile2[1]) + 1))
    areas.append(area)

# Returns whether or not all tiles between two tiles are valid
def valid_area(tile1, tile2):
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

    # print("Validating area", tile1, tile2)

    # Look through each of the rug's tiles
    for i in range(starti, endi):
        for j in range(startj, endj):
            # print("Checking tile", i, j)
            if not is_inside([i, j]):
                return False

    return True

num_counted = 0
areas = []
for tile in red_tiles:
    for other_tile in red_tiles:
        areas.append([(abs(tile[0] - other_tile[0]) + 1) * (abs(tile[1] - other_tile[1]) + 1), tile, other_tile])
    num_counted += 1

areas.sort(reverse=True)

print(areas[0])

# for area in areas:
#     print("Checking area", area)
#     if valid_area(area[1], area[2]):
#         print("Largest valid area", area[0])
#         break