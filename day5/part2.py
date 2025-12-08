file = open("day5/input.txt", "r").readlines()

fresh_ranges = []
for line in file:
    if line == "\n":
        break

    line = line.split("-")
    fresh_ranges.append((int(line[0]), int(line[1])))

fresh_ranges.sort()

combined_range_starts = []
combined_range_ends = []

total_ids = 0
cut_start = fresh_ranges[0][0]
for cur_range in fresh_ranges:
    # Principle: we want to combine ranges, then add up all of the unique ranges
    #
    # A range has a unique starting point of a combined range if it's (starting number - 1) is not in any other range
    # A range has a unique ending point of a combined range if it's (ending number + 1) is not in any other range

    # Check if (starting number - 1) is in any other range:
    unique_starting_point = True
    unique_ending_point = True
    for comparing_range in fresh_ranges:
        if comparing_range == cur_range:
            continue

        if cur_range[0] - 1 > comparing_range[0] and cur_range[0] - 1 < comparing_range[1]:
            unique_starting_point = False

        if cur_range[1] + 1 > comparing_range[0] and cur_range[1] + 1 < comparing_range[1]:
            unique_ending_point = False

    if unique_starting_point:
        combined_range_starts.append(cur_range[0])
    
    if unique_ending_point:
        combined_range_ends.append(cur_range[1])

combined_range_starts = list(set(combined_range_starts))
combined_range_ends = list(set(combined_range_ends))

combined_range_starts.sort()
combined_range_ends.sort()

# Add ids of combined ranges to total
for i in range(len(combined_range_starts)):
    total_ids += combined_range_ends[i] - combined_range_starts[i] + 1

print(total_ids)