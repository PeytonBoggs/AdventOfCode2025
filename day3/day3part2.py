file = open("day3/input.txt", "r").readlines()

def findmax(bank, batteries_left):
    max_index = 0
    i = 0
    for battery_joltage in bank:
        if battery_joltage > bank[max_index] and i < len(bank) - batteries_left + 1:
            max_index = i
        i += 1
    
    return max_index


total_joltage = 0

for bank in file:
    bank = bank.strip()

    batteries_left = 12
    flipped_battery_indices = []

    while batteries_left != 0:
        if flipped_battery_indices == []:
            max_index = findmax(bank, batteries_left)
        else:
            highest_index = flipped_battery_indices[len(flipped_battery_indices)-1]
            max_index = findmax(bank[highest_index+1:], batteries_left) + highest_index + 1

        flipped_battery_indices.append(max_index)

        batteries_left -= 1
    
    bank_joltage = ""
    for i in range(0, 12):
        bank_joltage += bank[flipped_battery_indices[i]]
    bank_joltage = int(bank_joltage)
    
    total_joltage += bank_joltage

print(total_joltage)