import re
import math
from itertools import combinations_with_replacement
from functools import cache

file = open("day10/sample_input.txt", "r").readlines()

machines = []
# Process machine
for line in file:
    line = line.strip().split()

    # Process buttons
    buttons = []
    for b in range(1, len(line) - 1):
        button = []
        nums = re.findall("[0-9]", line[b])
        for num in nums:
            button.append(int(num))
        buttons.append(button)

    # Process joltages
    str_required_joltages = (line[len(line) - 1][1:len(line[len(line) - 1]) - 1]).split(",")
    required_joltages = []
    for joltage in str_required_joltages:
        required_joltages.append(int(joltage))
            
    machine = [buttons, required_joltages]
    machines.append(machine)


# Start with the final joltages, then recursively work down to the base case (all 0s)
@cache
def get_combination(joltages, button):
    if joltages == [0] * len(required_joltages):
        return button
    
    for button in buttons:
        for toggle in button:
            joltages[toggle] -= 1
        return get_combination(joltages, button)

def configure(machine):
    buttons: list[int] = machine[0]
    required_joltages: list[int] = machine[1]

    # It does not matter in what order the buttons are pressed
    # So, to see if the joltages are correct, you can:
    # 1. Append some buttons to a list of buttons pressed
    # 2. See the number of times each of the toggles occurs in that list
    # 3. Add up the toggles, compare them against each joltage requirement

    # Brute force checking if some configuration of buttons works, going from none to all
    print("Buttons:", buttons)
    print("Required joltages:", required_joltages)

    # At minimum, you need the # buttons * num_pressed = highest joltage
    # So, you can set the initial num_pressed to ceiling(highest joltage / # buttons)
    num_pressed = math.ceil(max(required_joltages) / len(buttons))

    while True:
        # Find all possible combinations of buttons given the number to press
        # Note: with replacement so that the same button can be pressed multipe times
        button_combinations = list(combinations_with_replacement(buttons, num_pressed))

        # Test one combination of buttons at a time
        for combination in button_combinations:
            # (1) Get a list of toggles
            joltages = [0] * len(required_joltages)
            for button in combination:
                for toggle in button:
                    joltages[toggle] += 1

            if joltages == required_joltages:
                print(combination)
                return num_pressed
        
        num_pressed += 1

total_pressed = 0
for i, machine in enumerate(machines):
    print("Machine", i, "of", len(machines) - 1)
    total_pressed += configure(machine)

print(total_pressed)