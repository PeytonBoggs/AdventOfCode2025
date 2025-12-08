input = []
with open('day1/day1_input.txt', 'r') as file:
    for line in file:
        input.append(line.strip())

rotations = []
for line in input:
    direction = line[0]
    distance = line[1:]
    rotations.append((direction, distance))

pointer = 50
password = 0

for rotation in rotations:
    direction = rotation[0]
    distance = int(rotation[1])
    if direction == "L":
        pointer -= distance
    else:
        pointer += distance
    pointer = pointer % 100
    if pointer == 0:
        password += 1

print(password)