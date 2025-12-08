file = open("day6/input.txt", "r").readlines()

scroll = []
for line in file:
    scroll.append(list(line.strip("\n")))

num_rows = len(scroll)
num_cols = len(scroll[0])

grand_total = 0
col_num = ""
cur_nums = []
for col in range(num_cols - 1, -1, -1):
    col_num = ""
    operator = ""

    for row in range(num_rows):
        if scroll[row][col] == "+" or scroll[row][col] == "*":
            operator = scroll[row][col]
            continue

        col_num = col_num + scroll[row][col]
    
    if col_num.strip() == '':
        continue
    else:
        cur_nums.append(int(col_num))

    if operator == "+":
        total = 0
        for num in cur_nums:
            total = total + num
        grand_total += total
        cur_nums = []

    if operator == "*":
        total = 1
        for num in cur_nums:
            total = total * num
        grand_total += total
        cur_nums = []

print(grand_total)