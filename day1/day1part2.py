import math

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

"""direction = "R"
distance = 150

if direction == "L":
    if pointer - distance <= 0:
        password += int(abs((pointer - distance) / 100) + 1)
    pointer -= distance
else:
    if distance + pointer >= 100:
        password += int(abs((distance + pointer) / 100))
    pointer += distance
pointer = pointer % 100

print(password)"""

for rotation in rotations:
    initialpointer = pointer
    direction = rotation[0]
    distance = int(rotation[1])
    if direction == "L":
        if pointer - distance <= 0:
            if pointer == 0 and distance >= 100:
                password += int(abs(pointer - distance) / 100)
            elif pointer == 0:
                pass
            else:
                password += int(abs((pointer - distance) / 100) + 1)
        pointer -= distance
    else:
        if distance + pointer >= 100:
            password += int(abs((distance + pointer) / 100))
        pointer += distance
    pointer = pointer % 100
    print(initialpointer, rotation, pointer, password)

print(password)