file = open("day6/input.txt", "r").readlines()

scroll = []
for line in file:
    line = line.strip().split()
    scroll.append(line)

num_rows = len(scroll)
num_cols = len(scroll[0])

grand_total = 0
for col in range(num_cols):
    
    if scroll[num_rows - 1][col] == "+":
        total = 0
        for row in range(num_rows - 1):
            total = total + int(scroll[row][col])
        grand_total += total

    elif scroll[num_rows - 1][col] == "*":
        total = 1
        for row in range(num_rows - 1):
            total = total * int(scroll[row][col])
        grand_total += total

print(grand_total)