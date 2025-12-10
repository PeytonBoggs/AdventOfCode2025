file = open("day9/input.txt", "r").readlines()

tile_locations = []
for line in file:
    line = line.strip().split(",")
    line[0], line[1] = int(line[0]), int(line[1])
    tile_locations.append(line)

def area_between(tile1, tile2):
    return ((abs(tile1[0] - tile2[0]) + 1) * (abs(tile1[1] - tile2[1]) + 1))

areas = []
for tile in tile_locations:
    for other_tile in tile_locations:
        areas.append(area_between(tile, other_tile))

areas.sort(reverse=True)

print(areas[0])