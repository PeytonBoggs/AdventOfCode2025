import math

file = open("day8/input.txt", "r")

# Store all box location and circit data in junction_boxes list
# Box syntax: (x, y, z, circuit_num)
junction_boxes = []
circuit_num = 0
for line in file:
    box = line.strip().split(",")
    box = [int(box[0]), int(box[1]), int(box[2]), circuit_num]
    circuit_num += 1
    junction_boxes.append(box)

# Helper function: Distance formula
def distance(box1, box2):
    return math.sqrt((box1[0] - box2[0]) * (box1[0] - box2[0]) + (box1[1] - box2[1]) * (box1[1] - box2[1]) + (box1[2] - box2[2]) * (box1[2] - box2[2]))

# Find distances of all pairs, keep in list of pairs with syntax pair = [distance, box1_index, box2_index]
distances = []
for i, box1 in enumerate(junction_boxes):
    for j, box2 in enumerate(junction_boxes):
        if i < j:
            distances.append([distance(box1, box2), i, j])

# Sort all distances and retain box information
distances.sort(key=lambda pair: pair[0])

num_circuits = len(junction_boxes)

# Connect circuits until only 1 remains
for i in range(len(distances)):
    box1_index = distances[i][1]
    box2_index = distances[i][2]

    # If they are on the same circuit, continue, if not, add all boxes in box2's circuit to box1's circuit  
    if junction_boxes[box1_index][3] == junction_boxes[box2_index][3]:
        continue
    else:
        circuit_num_to_be_kept = junction_boxes[box1_index][3]
        circuit_num_to_be_replaced = junction_boxes[box2_index][3]
        for j in range(len(junction_boxes)):
            if junction_boxes[j][3] == circuit_num_to_be_replaced:
                junction_boxes[j][3] = circuit_num_to_be_kept
        num_circuits -= 1
        
        if num_circuits == 1:
            answer = junction_boxes[box1_index][0] * junction_boxes[box2_index][0] 
            print(answer)
            break