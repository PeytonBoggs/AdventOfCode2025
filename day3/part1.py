file = open("day3/input.txt", "r").readlines()

total_joltage = 0

for bank in file:
    bank = bank.strip()

    first_index = 0
    i = first_index
    for battery_joltage in bank:
        if battery_joltage > bank[first_index] and i != len(bank)-1:
            first_index = i
        i += 1

    second_index = first_index + 1
    j = second_index
    for battery_joltage in bank[second_index:]:
        if battery_joltage > bank[second_index]:
            second_index = j
        j += 1

    bank_joltage = int(bank[first_index] + bank[second_index])
    total_joltage += bank_joltage

print(total_joltage)