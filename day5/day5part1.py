file = open("day5/input.txt", "r").readlines()

before_empty_line = True
fresh_ranges_unsplit = []
avaliable_ids = []
for line in file:
    if line == "\n":
        before_empty_line = False
        continue
    
    if before_empty_line:
        fresh_ranges_unsplit.append(line.rstrip())
    else:
        avaliable_ids.append(int(line.rstrip()))

fresh_ranges = []
for id_range in fresh_ranges_unsplit:
    id_range = id_range.split("-")
    fresh_ranges.append((int(id_range[0]), int(id_range[1])))

num_fresh = 0
for id in avaliable_ids:
    for range in fresh_ranges:
        if id >= range[0] and id <= range[1]:
            num_fresh += 1
            break

print(num_fresh)