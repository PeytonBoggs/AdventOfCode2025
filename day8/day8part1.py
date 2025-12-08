import math

file = open("day8/sample_input.txt", "r")

# Store all box location and circit data in junction_boxes list
# Box syntax: (x, y, z, circuit_num)
junction_boxes = []
circuit_num = 0
for line in file:
    box = line.strip().split(",")
    box = [int(box[0]), int(box[1]), int(box[2]), circuit_num]
    circuit_num += 1
    junction_boxes.append(box)

def distance(box1, box2):
    return math.sqrt((box1[0] - box2[0]) * (box1[0] - box2[0]) + (box1[1] - box2[1]) * (box1[1] - box2[1]) + (box1[2] - box2[2]) * (box1[2] - box2[2]))

# Store distances of all pairs in top-right half of "distances" 2d matrix
distances = [[float('inf') for _ in range(len(junction_boxes))] for _ in range(len(junction_boxes))]
for i, box1 in enumerate(junction_boxes):
    for j, box2 in enumerate(junction_boxes):
        if i < j:
            distances[i][j] = distance(box1, box2)

def find_min_distance_pair(distances):
    # Min syntax: [minimum distance, row, col]
    min = (float('inf'), -1, -1)
    for i in range(len(distances)):
        for j in range(len(distances[0])):
            if distances[i][j] < min[0]:
                min = [distances[i][j], i, j]
    
    return [min[1], min[2]]

# Find the minumum distance pair, connect the cirucits
num_connected = 10
for _ in range(num_connected):
    # Get the minimum distance pair
    closest_pair = find_min_distance_pair(distances)

    # Set the distance of this pair to inf to make sure they are not connected again
    distances[closest_pair[0]][closest_pair[1]] = float('inf')

    # box1 is the first box in the pair, box2 is the second
    box1 = junction_boxes[closest_pair[0]]
    box2 = junction_boxes[closest_pair[1]]

    # Set the circuit number of any box in box2's circuit to box1's circuit
    for i in range(len(junction_boxes)):
        if junction_boxes[i][3] == box2[3]:
            junction_boxes[i][3] = box1[3]

# Count the number of boxes in each circuit
count = [0] * len(junction_boxes)
for i in range(len(junction_boxes)):
    count[junction_boxes[i][3]] += 1

# Find and multiply the three largest circuits
count.sort(reverse=True)
multiplied_three_largest = count[0] * count[1] * count[2]

print(multiplied_three_largest)