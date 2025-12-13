import re
from itertools import combinations

file = open("day10/input.txt", "r").readlines()

machines = []
# Process machine
for line in file:
    line = line.strip().split()

    # Process lights
    lights = list(line[0][1:len(line[0]) - 1])

    # Process buttons
    buttons = []
    for b in range(1, len(line) - 1):
        button = []
        nums = re.findall("[0-9]", line[b])
        for num in nums:
            button.append(int(num))
        buttons.append(button)
            
    machine = [lights, buttons]
    machines.append(machine)

def configure(machine):
    lights: list[int] = machine[0]
    buttons: list[int] = machine[1]

    # It does not matter in what order the buttons are pressed
    # So, to see if the machine is configued, you can:
    # 1. Append some buttons to a list of buttons pressed
    # 2. See the number of times each of the lights occurs in that list (toggles)
    # 3. If each number of toggles is odd, the lights are toggled on, and vice versa

    # Brute force checking if some configuration of buttons works, going from none to all
    configured = False
    num_pressed = 0
    while not configured:
        num_pressed += 1
        # Find all possible combinations of buttons given the number to press
        button_combinations = list(combinations(buttons, num_pressed))

        for combination in button_combinations:
            # (1) Get a list of toggles
            toggles = []
            for button in combination:
                toggles.extend(button)
            
            # (2) Count the number of times each light was toggled
            # Even -> the light is off, Odd -> the light is on
            configured = True
            for i, light in enumerate(lights):
                if light == "." and toggles.count(i) % 2 == 1:
                    configured = False
                    break
                if light == "#" and toggles.count(i) % 2 == 0:
                    configured = False
                    break
            if configured:
                return num_pressed

total_pressed = 0
for machine in machines:
    total_pressed += configure(machine)

print(total_pressed)